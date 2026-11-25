# moteur_zenodo.ps1 — TRIADE : le moteur de publication Zenodo
# Portage PowerShell du patron Python depot/scripts/vague19/publier_zenodo_v0310.py
# (Entrée 429) — trait pour trait :
#   newversion -> fichiers -> metadonnees -> PUBLISH -> verification md5 au bord
# Idempotent : reprend un brouillon existant, saute une version deja publiee.
# Le jeton est lu du fichier (jamais affiche, jamais ecrit ailleurs).
# Le kit developpeur v1.3.0, le corpus v2.1 et TRIADE-TRAIN v1.0.0 sont
# INCHANGES — aucune version creuse (la doctrine), ils ne sont pas republies.
# usage : powershell -NoProfile -ExecutionPolicy Bypass -File moteur_zenodo.ps1 [-DryRun]
#         [-BrouillonProtocole <id>] [-BrouillonParticipation <id>]

param(
    [string]$LotDir    = (Join-Path $PSScriptRoot 'lot'),
    [string]$TokenFile = (Join-Path $PSScriptRoot 'token-zenodo.txt'),
    [string]$Journal   = (Join-Path $PSScriptRoot 'PUSHER-JOURNAL.log'),
    [int]$BrouillonProtocole = 0,
    [int]$BrouillonParticipation = 0,
    [switch]$DryRun
)

$Api = 'https://zenodo.org/api'
$DatePub = '2026-11-26'
try { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 } catch {}

# ---------------------------------------------------------------- le journal
function Ecrire([string]$Ligne) {
    Write-Host $Ligne
    try { Add-Content -LiteralPath $Journal -Value $Ligne -Encoding UTF8 } catch {}
}

function Convertir-Corps { param($Objet)
    ConvertTo-Json -InputObject $Objet -Depth 8
}

# ------------------------------------------- l'appel au bord (reprises 5xx)
function Invoke-Zenodo {
    param([string]$Methode, [string]$Uri, [string]$CorpsJson, [string]$Fichier,
          [int]$Essais = 6)
    for ($i = 1; $i -le $Essais; $i++) {
        try {
            $p = @{ Uri = $Uri; Method = $Methode; TimeoutSec = 1800
                    Headers = @{ Authorization = "Bearer $Jeton" } }
            if ($CorpsJson) { $p['ContentType'] = 'application/json';   $p['Body'] = $CorpsJson }
            if ($Fichier)   { $p['ContentType'] = 'application/octet-stream'; $p['InFile'] = $Fichier }
            $d = Invoke-RestMethod @p
            return @{ Code = 200; Donnees = $d }
        } catch {
            $code = $null; $corps = ''
            try { $code = [int]$_.Exception.Response.StatusCode } catch {}
            try {
                $rep = $_.Exception.Response
                if ($rep -and $rep.GetResponseStream) {
                    $sr = New-Object System.IO.StreamReader($rep.GetResponseStream())
                    $corps = $sr.ReadToEnd()
                } elseif ($rep -and $rep.Content) {
                    $corps = $rep.Content.ReadAsStringAsync().Result
                }
            } catch {}
            if (-not $corps) { $corps = $_.Exception.Message }
            if ($corps.Length -gt 600) { $corps = $corps.Substring(0, 600) }
            $rajouable = ((-not $code) -or ($code -in 500, 502, 503, 504))
            if ($rajouable -and $i -lt $Essais) {
                Ecrire "  [reprise] $Methode $Uri — HTTP $code $corps (essai $i/$Essais)"
                Start-Sleep -Seconds (3 * $i)
                continue
            }
            return @{ Code = $code; Corps = $corps }
        }
    }
    return @{ Code = 0; Corps = 'essais épuisés' }
}

function Trouve-Entree { param($Donnees, [string]$Nom)
    if (-not $Donnees) { return $null }
    if ($Donnees -is [System.Array]) {
        return @($Donnees) | Where-Object { $_.key -eq $Nom } | Select-Object -First 1
    }
    if ($Donnees.entries) {
        return @($Donnees.entries) | Where-Object { $_.key -eq $Nom } | Select-Object -First 1
    }
    return $null
}

# ------------------------------------------------------- 0. le journal ouvre
Ecrire ("`n===== {0} — démarrage du moteur (DryRun = {1}) =====" -f `
    (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), [bool]$DryRun)

# ------------------------------- 1. le lot : verification byte-byte d'abord
$CheminManifeste = Join-Path $LotDir 'MANIFESTE-PACKS-v0.31.0.json'
if (-not (Test-Path -LiteralPath $CheminManifeste)) {
    Ecrire 'ROUGE : MANIFESTE-PACKS-v0.31.0.json introuvable dans le lot.'
    exit 2
}
$Manifeste = Get-Content -LiteralPath $CheminManifeste -Raw | ConvertFrom-Json

$CiblesFichiers = @(
    'TRIADE_soumission_v0.31.0.zip',
    'TRIADE_presentation_v0.31.0.zip',
    'TRIADE_complet_v0.31.0.zip',
    'TRIADE_participer_v1.2.0.zip'
)

Ecrire 'LE LOT — les quatre packs, empreintes vérifiées au manifeste :'
$LotOk = $true
foreach ($nom in $CiblesFichiers) {
    $p = Join-Path $LotDir $nom
    if (-not (Test-Path -LiteralPath $p)) {
        Ecrire "  [lot] MANQUANT : $nom"; $LotOk = $false; continue
    }
    $m = $Manifeste.PSObject.Properties[$nom].Value
    if (-not $m) { Ecrire "  [lot] le manifeste ne connaît pas $nom"; $LotOk = $false; continue }
    $taille = (Get-Item -LiteralPath $p).Length
    $sha = (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLower()
    $bon = ($taille -eq [int64]$m.bytes) -and ($sha -eq $m.sha256)
    $verdict = 'OK'; if (-not $bon) { $verdict = 'ECART!'; $LotOk = $false }
    Ecrire ("  [empreinte] {0} — {1} o — sha256 {2}… {3}" -f $nom, $taille, $sha.Substring(0, 16), $verdict)
}
if (-not $LotOk) {
    Ecrire 'RESULTAT|protocole|ROUGE|lot-ecart|—'
    Ecrire 'RESULTAT|participation|ROUGE|lot-ecart|—'
    Ecrire 'ROUGE : le lot diverge du manifeste — RIEN n est envoyé (retélécharge le lot).'
    exit 2
}
Ecrire '  4/4 OK — le lot est byte-byte conforme au manifeste.'

# ----------------------------------------------------------------- 2. le jeton
if (-not (Test-Path -LiteralPath $TokenFile)) { Ecrire 'ROUGE : token-zenodo.txt introuvable.'; exit 2 }
$Jeton = (Get-Content -LiteralPath $TokenFile -Raw).Trim()
if (-not $Jeton) { Ecrire 'ROUGE : token-zenodo.txt est vide.'; exit 2 }
Ecrire '  jeton lu (jamais affiché).'

if ($DryRun) {
    Ecrire 'DRY-RUN : le bord ne sera pas touché. Le plan :'
    Ecrire '  PROTOCOLE : record 24499428 (concept 10.5281/zenodo.24367343) -> v0.31.0 (trois packs)'
    Ecrire '  PARTICIPATION : record 24499847 (concept 10.5281/zenodo.24497299) -> v1.2.0 (un pack)'
    Ecrire '  Le kit dev v1.3.0, le corpus v2.1 et TRIADE-TRAIN v1.0.0 : INCHANGÉS, non republiés.'
    Ecrire 'DRY-RUN TERMINÉ — lot OK.'
    exit 0
}

# --------------------------- 3. le bord repond ? les concepts deja a jour ?
function Version-Concepte { param([int]$Id)
    $r = Invoke-Zenodo -Methode Get -Uri "$Api/records/$Id"
    if ($r.Code -ne 200) { return @{ Code = $r.Code; Corps = $r.Corps } }
    return @{ Code = 200; Version = [string]$r.Donnees.metadata.version }
}

$FaireProto = $true; $FairePart = $true
$r = Version-Concepte 24367343
if ($r.Code -ne 200) {
    Ecrire ("BLOCAGE|concept 24367343 : HTTP {0} {1}" -f $r.Code, $r.Corps)
    if ([string]$r.Code -eq '403') {
        Ecrire '  (le bord refuse ce réseau aussi — attends ou change de réseau ; le retry du bac veille)'
    }
    Ecrire ('RESULTAT|protocole|ROUGE|bord-HTTP-{0}|—' -f $r.Code)
    Ecrire ('RESULTAT|participation|ROUGE|bord-HTTP-{0}|—' -f $r.Code)
    exit 3
}
if ($r.Version -eq 'v0.31.0') { $FaireProto = $false; Ecrire 'DEJA|protocole|v0.31.0 — concept 24367343 y résout déjà : sauté' }
$r = Version-Concepte 24497299
if ($r.Code -ne 200) {
    Ecrire ("BLOCAGE|concept 24497299 : HTTP {0} {1}" -f $r.Code, $r.Corps)
    Ecrire ('RESULTAT|protocole|ROUGE|bord-HTTP-{0}|—' -f $r.Code)
    Ecrire ('RESULTAT|participation|ROUGE|bord-HTTP-{0}|—' -f $r.Code)
    exit 3
}
if ($r.Version -eq 'v1.2.0') { $FairePart = $false; Ecrire 'DEJA|participation|v1.2.0 — concept 24497299 y résout déjà : sautée' }
if (-not ($FaireProto -or $FairePart)) {
    Ecrire 'RESULTAT|les-deux|DEJA|—|—'
    Ecrire 'Les deux versions sont déjà publiées — rien à faire.'
    exit 0
}

# ------------------------------------------------------------- 4. le flux v19
function Publier-Flux {
    param([string]$NomFlux, [int]$Ancien, [int]$BrouillonId, [string]$Titre,
          [string]$Version, [string]$Description, [string[]]$Chemins)

    Ecrire ("`n=== {0} : {1} -> {2} ===" -f $NomFlux, $Ancien, $Version)

    # 1. le brouillon : newversion, ou reprise d'un brouillon existant
    $brouillon = $null
    if ($BrouillonId -gt 0) {
        $r = Invoke-Zenodo -Methode Get -Uri "$Api/records/$BrouillonId/draft"
        if ($r.Code -eq 200) { $brouillon = $r.Donnees }
        else {
            Ecrire "  [brouillon] GET HTTP $($r.Code) — liens reconstruits (précédent v19)"
            $brouillon = @{ id = $BrouillonId; links = @{
                files   = "$Api/records/$BrouillonId/draft/files"
                self    = "$Api/records/$BrouillonId/draft"
                publish = "$Api/records/$BrouillonId/draft/actions/publish" } }
        }
    } else {
        $r = Invoke-Zenodo -Methode Post -Uri "$Api/records/$Ancien/versions"
        if ($r.Code -in 200, 201) { $brouillon = $r.Donnees }
        else {
            $r2 = Invoke-Zenodo -Methode Get -Uri "$Api/records/$Ancien/draft"
            if ($r2.Code -eq 200) {
                $brouillon = $r2.Donnees
                Ecrire "  [newversion] refusé HTTP $($r.Code) — brouillon existant repris"
            } else {
                Ecrire ('RESULTAT|{0}|ROUGE|newversion-HTTP-{1}|—' -f $NomFlux, $r.Code)
                throw "newversion $Ancien : HTTP $($r.Code) $($r.Corps)"
            }
        }
    }
    Ecrire ("  [newversion] brouillon {0}" -f $brouillon.id)

    # 2. les fichiers
    $FilesUrl = $brouillon.links.files
    foreach ($chemin in $Chemins) {
        $nom = [System.IO.Path]::GetFileName($chemin)
        $r = Invoke-Zenodo -Methode Post -Uri $FilesUrl -CorpsJson (Convertir-Corps @(@{ key = $nom }))
        $entree = $null
        if ($r.Code -in 200, 201) { $entree = Trouve-Entree $r.Donnees $nom }
        if (-not $entree) {
            # peut-être déjà créé (reprise) : relire la table
            $r3 = Invoke-Zenodo -Methode Get -Uri $FilesUrl
            if ($r3.Code -eq 200) { $entree = Trouve-Entree $r3.Donnees $nom }
        }
        if (-not $entree) {
            Ecrire ('RESULTAT|{0}|ROUGE|fichier-{1}-HTTP-{2}|—' -f $NomFlux, $nom, $r.Code)
            throw "fichier $nom : HTTP $($r.Code) $($r.Corps)"
        }
        $r = Invoke-Zenodo -Methode Put -Uri $entree.links.content -Fichier $chemin
        if ($r.Code -notin 200, 201, 202) {
            Ecrire ('RESULTAT|{0}|ROUGE|upload-{1}-HTTP-{2}|—' -f $NomFlux, $nom, $r.Code)
            throw "upload $nom : HTTP $($r.Code) $($r.Corps)"
        }
        $r = Invoke-Zenodo -Methode Post -Uri $entree.links.commit
        if ($r.Code -notin 200, 201) {
            Ecrire ('RESULTAT|{0}|ROUGE|commit-{1}-HTTP-{2}|—' -f $NomFlux, $nom, $r.Code)
            throw "commit $nom : HTTP $($r.Code) $($r.Corps)"
        }
        Ecrire ("  [fichier] {0} déposé ({1} o)" -f $nom, (Get-Item -LiteralPath $chemin).Length)
    }

    # 3. les métadonnées (celles du script préparé et vérifié à l'Entrée 429)
    $meta = @{
        title = $Titre; version = $Version; description = $Description
        creators = @(@{ name = 'Lopez, Alexis' })
        license = @{ id = 'busl-1.1' }
        resource_type = @{ id = 'publication-article' }
        publication_date = $DatePub; publisher = 'Zenodo'
    }
    $r = Invoke-Zenodo -Methode Put -Uri $brouillon.links.self -CorpsJson (Convertir-Corps @{ metadata = $meta })
    if ($r.Code -in 200, 201) { Ecrire '  [metadata] posées' }
    else {
        # le PUT 500-persistant (vu vague 19) : relire — la valeur peut vivre
        $r4 = Invoke-Zenodo -Methode Get -Uri "$Api/records/$($brouillon.id)/draft"
        if ($r4.Code -eq 200 -and ([string]$r4.Donnees.metadata.version -eq $Version)) {
            Ecrire "  [metadata] PUT HTTP $($r.Code) — REPRIS : la valeur persiste (précédent v19)"
        } else {
            Ecrire ('RESULTAT|{0}|ROUGE|metadata-HTTP-{1}|—' -f $NomFlux, $r.Code)
            throw "metadata : HTTP $($r.Code) $($r.Corps)"
        }
    }

    # 4. PUBLISH — aucun publish partiel : les fichiers sont déjà vérifiés
    $r = Invoke-Zenodo -Methode Post -Uri $brouillon.links.publish
    if ($r.Code -notin 200, 201, 202) {
        Ecrire ('RESULTAT|{0}|ROUGE|PUBLISH-HTTP-{1}|—' -f $NomFlux, $r.Code)
        throw "PUBLISH : HTTP $($r.Code) $($r.Corps)"
    }
    $rid = $r.Donnees.id
    $doi = $r.Donnees.doi
    if (-not $doi) { try { $doi = $r.Donnees.pids.doi.identifier } catch {} }
    Ecrire "  [PUBLISH] record $rid — DOI $doi"

    # 5. la vérification md5 au bord authentifié
    Start-Sleep -Seconds 2
    $r = Invoke-Zenodo -Methode Get -Uri "$Api/records/$rid"
    $ecarts = @()
    if ($r.Code -ne 200) { $ecarts += ('HTTP-' + $r.Code) }
    else {
        foreach ($chemin in $Chemins) {
            $nom = [System.IO.Path]::GetFileName($chemin)
            $attendu = (Get-FileHash -LiteralPath $chemin -Algorithm MD5).Hash.ToLower()
            $ent = $null
            if ($r.Donnees.files -and $r.Donnees.files.entries) { $ent = Trouve-Entree $r.Donnees.files $nom }
            if (-not $ent) { $ecarts += $nom; continue }
            $api = ([string]$ent.checksum) -replace '^md5:', ''
            if ($api -and ($api.ToLower() -ne $attendu)) { $ecarts += $nom }
        }
    }
    if ($ecarts.Count -eq 0) {
        Ecrire ('RESULTAT|{0}|VERT|{1}|{2}' -f $NomFlux, $doi, $rid)
        Ecrire '  [vérification] VERT — les md5 du bord == le lot, pièce à pièce'
        return @{ Record = $rid; Doi = $doi }
    } else {
        Ecrire ('RESULTAT|{0}|ROUGE|md5-ecarts-{1}|{2}' -f $NomFlux, ($ecarts -join ','), $rid)
        Ecrire "  [vérification] ROUGE — écarts : $($ecarts -join ', ')"
        return $null
    }
}

$TitreProtocole = 'TRIADE: Enabling LLM Agents to Write Native Code by Hand Under Signed-Intent Governance (Academic Edition v0.31.0) — manuscript, data tables, complete sources and verification evidence'
$TitreParticipation = 'TRIADE Participation Pack v1.2.0: the five kits, evaluation and contribution'

$DescriptionProtocole = @'
<p><strong>TRIADE v0.31.0 — the edition waves 20–26 (24 November 2026).</strong> No
measured value changed. The generation gate now reads the prose: the edition linter runs
twenty-five fail-closed classes (C1–C25) over the five pieces — version prose, wave
continuity, abstract length, reader-test counts, DOI registry, English prose, derived
proof statuses, operand order and every target-registry line recomposed from the
published proofs. The target registry CIBLES.md carries eleven targets, one line each,
verdicts carried as published (5/18; 4,604 against 4,500 missed by 104; 3.264 against
3.0; 95/235 at generation; budgets held 674 ≤ 3,000 and 51 ≤ 64), no target re-drawn;
the AES-GCM 1.05× subject is named (the VAES corridor, unwritten). The five pieces are
regenerated (manuscript v0.31.0, specification v0.15.16, Book v1.15, proofs and
presentation v0.31.0); the v0.26.0 PDFs remain byte for byte. Named post-generation lab
results, consigned at the journal, to be carried by the next edition: the per-block
harness P3 was executed at 235/235 vectors (pre-registered target ≥ 200/235 held) and the
witness campaigns ran across field siliciums — an Ivy Bridge laptop, a Blackview phone
(Cortex-A78), a Colab Xeon and the GitHub Actions runners (AMD EPYC 7763 and 9V74, an
ARM64 server, a virtualised Apple M1 — the first Apple measure, FEAT_SHA256 ratio
6.89/8.00) — the sealed four silent on the three server siliciums. Named limits: served
structured output (P4), VAES metal (P5) and Tamarin/ProVerif (P6) remain AWAITING the
real post.</p>
'@

$DescriptionParticipation = @'
<p><strong>TRIADE Participation Pack v1.2.0 (26 November 2026).</strong> The five kits —
the complete sources v0.31.0 (1,044 entries), the soumission and presentation packs of
the v0.31.0 edition, the developer kit v1.3.0 (unchanged since record 24499840) and the
training pack v1.0.0 — with CONTRIBUTING, EVALUATION (six commands, each lived at the
lab before assembly) and INDEX-DOI (the corrected concept identifiers; participation
concept 24497299). Everything needed to evaluate the protocol and contribute to it.</p>
'@

# ------------------------------------------------------------------ le geste
$sortie = @{}
if ($FaireProto) {
    $f = @((Join-Path $LotDir 'TRIADE_soumission_v0.31.0.zip'),
           (Join-Path $LotDir 'TRIADE_presentation_v0.31.0.zip'),
           (Join-Path $LotDir 'TRIADE_complet_v0.31.0.zip'))
    try {
        $sortie['protocole'] = Publier-Flux -NomFlux 'protocole' -Ancien 24499428 `
            -BrouillonId $BrouillonProtocole -Titre $TitreProtocole -Version 'v0.31.0' `
            -Description $DescriptionProtocole -Chemins $f
    } catch { Ecrire "  ROUGE — $($_.Exception.Message)"; $sortie['protocole'] = $null }
} else { Ecrire '  (protocole déjà publié — sauté)' }

if ($FairePart) {
    $f = @(Join-Path $LotDir 'TRIADE_participer_v1.2.0.zip')
    try {
        $sortie['participation'] = Publier-Flux -NomFlux 'participation' -Ancien 24499847 `
            -BrouillonId $BrouillonParticipation -Titre $TitreParticipation -Version 'v1.2.0' `
            -Description $DescriptionParticipation -Chemins $f
    } catch { Ecrire "  ROUGE — $($_.Exception.Message)"; $sortie['participation'] = $null }
} else { Ecrire '  (participation déjà publiée — sautée)' }

Ecrire ("===== {0} — fin du moteur =====" -f (Get-Date -Format 'HH:mm:ss'))
$echecs = @($sortie.Keys | Where-Object { -not $sortie[$_] })
if ($echecs.Count -gt 0) {
    Ecrire ("FIN — échecs : {0}. Relance sûre : le moteur est idempotent (brouillon repris, publié sauté)." -f ($echecs -join ', '))
    exit 1
}
Ecrire 'FIN — VERT partout. Dis-le au bac : la chaîne complète suivra (livrables du coffre, ARCHIVE, miroirs, worklog).'
exit 0
