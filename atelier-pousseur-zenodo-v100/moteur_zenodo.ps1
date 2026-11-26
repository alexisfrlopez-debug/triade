# moteur_zenodo.ps1 — TRIADE : le moteur de publication Zenodo
# Portage PowerShell du patron Python depot/scripts/vague19/publier_zenodo_v0310.py
# (Entrée 429) — trait pour trait :
#   newversion -> fichiers -> metadonnees -> PUBLISH -> verification md5 au bord
# Idempotent : reprend un brouillon existant, saute une version deja publiee.
# Le jeton est lu du fichier (jamais affiche, jamais ecrit ailleurs).
# Le kit developpeur v1.3.0, le corpus v2.1 et TRIADE-TRAIN v1.0.0 sont
# INCHANGES — aucune version creuse (la doctrine), ils ne sont pas republies.
# correctif b (26/11/2026) — fidelite au patron python, trois gestes :
#   1. le corps JSON part en octets UTF-8 (PowerShell 5.1 l'eut envoye Latin-1 :
#      les accents des metadonnees seraient devenus mojibake au bord) ;
#   2. Trouve-Entree gere la forme «carte» de entries (le patron l'autorisait) ;
#   3. $ProgressPreference coupe (Invoke-RestMethod glisse sinon sous 5.1).
# correctif c (26/11/2026, apres le retour 00:31) — le PUBLISH seul rendait 400
#   aux DEUX flux (brouillon, fichiers et metadonnees acceptes) : le bord vit
#   en UTC et publication_date = 2026-11-26 etait ENCORE DEMAIN a 23:31 UTC —
#   la fenetre 23:00-01:00 (Paris) quand la date est le jour de Paris. Deux gestes :
#   1. la garde UTC : Attendre-Passage-Utc attend minuit UTC du jour voulu avant
#      le PUBLISH (au plus une heure ; les brouillons vivent, rien ne se perd) ;
#   2. les mots exacts du bord : le corps JSON du refus vit dans
#      ErrorDetails.Message sous 5.1 comme sous 7 — on le lit D ABORD (le 400
#      de 00:31 n avait rendu que le message .NET faute de le lire).
# correctif d (26/11/2026, apres le retour 01:14) — la reprise des FICHIERS :
#   les brouillons de 00:31 avaient leurs packs DEJA COMMIS ; la relance
#   re-POSTait, re-PUTait et re-committait ces pieces engagees : le bord
#   rendait 404 au commit («Record '24545339' has no file 'TRIADE_soumission
#   _v0.31.0.zip'.») et coupait la connexion au corps de 31 Mo (participation,
#   six essais). Les fichiers sont desormais idempotents au bord : une piece
#   conforme (md5 du bord == md5 du lot) est SAUTEE ; une piece presente mais
#   divergente (ou jamais commise) est RETIREE du brouillon puis redeposee a
#   l identique ; une piece absente est deposee (le geste eprouve de 00:31).
#   Le patron python porte le meme geste (televerse).
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
$ProgressPreference = 'SilentlyContinue'

# ---------------------------------------------------------------- le journal
function Ecrire([string]$Ligne) {
    Write-Host $Ligne
    try { Add-Content -LiteralPath $Journal -Value $Ligne -Encoding UTF8 } catch {}
}

function Convertir-Corps { param($Objet)
    ConvertTo-Json -InputObject $Objet -Depth 8
}

# les mots EXACTS du bord : sous 5.1 comme sous 7, Invoke-RestMethod pose le
# corps JSON du refus dans ErrorDetails.Message (le flux brut est deja bu) —
# on le lit D ABORD, sinon le flux, sinon le message .NET (le 400 du 26/11
# 00:31 n avait rendu que le message .NET faute de le lire).
function Corps-Erreur { param($Erreur)
    $corps = ''
    try { if ($Erreur.ErrorDetails -and $Erreur.ErrorDetails.Message) { $corps = [string]$Erreur.ErrorDetails.Message } } catch {}
    if (-not $corps) {
        try {
            $rep = $Erreur.Exception.Response
            if ($rep -and $rep.GetResponseStream) {
                $sr = New-Object System.IO.StreamReader($rep.GetResponseStream())
                $corps = $sr.ReadToEnd()
            } elseif ($rep -and $rep.Content) {
                $corps = $rep.Content.ReadAsStringAsync().Result
            }
        } catch {}
    }
    if (-not $corps) { $corps = [string]$Erreur.Exception.Message }
    return $corps
}

# ------------------------------------------- l'appel au bord (reprises 5xx)
function Invoke-Zenodo {
    param([string]$Methode, [string]$Uri, [string]$CorpsJson, [string]$Fichier,
          [int]$Essais = 6)
    for ($i = 1; $i -le $Essais; $i++) {
        try {
            $p = @{ Uri = $Uri; Method = $Methode; TimeoutSec = 1800
                    Headers = @{ Authorization = "Bearer $Jeton" } }
            if ($CorpsJson) { $p['ContentType'] = 'application/json';   $p['Body'] = [System.Text.Encoding]::UTF8.GetBytes($CorpsJson) }
            if ($Fichier)   { $p['ContentType'] = 'application/octet-stream'; $p['InFile'] = $Fichier }
            $d = Invoke-RestMethod @p
            return @{ Code = 200; Donnees = $d }
        } catch {
            $code = $null; $corps = ''
            try { $code = [int]$_.Exception.Response.StatusCode } catch {}
            $corps = Corps-Erreur $_
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

# ---------------------- la garde UTC : le bord vit la date UTC, pas la tienne
# Decision pure (injectable en test) : $null = rien a faire (la date est deja
# vECUE au bord) ; @{ Cible/Minutes } = attendre ; @{ Refus } = refus net.
function Decision-Garde-Utc { param([string]$DatePub, [datetime]$MaintenantUtc)
    if (-not $DatePub) { return $null }
    $aujourdhui = $MaintenantUtc.ToString('yyyy-MM-dd')
    if ($DatePub -le $aujourdhui) { return $null }   # hier ou aujourd hui au bord : passe
    $cible = [datetime]::ParseExact($DatePub, 'yyyy-MM-dd', $null)
    $cible = [datetime]::SpecifyKind($cible, [datetimekind]::Utc)
    $ecart = ($cible - $MaintenantUtc).TotalSeconds
    if ($ecart -gt 93600) {
        return @{ Refus = ("publication_date {0} est a plus d un jour dans le futur UTC ({1}) — corrige la date." -f $DatePub, $aujourdhui) }
    }
    return @{ Cible = $cible; Minutes = [int][math]::Ceiling($ecart / 60.0); AujourdHui = $aujourdhui }
}

function Attendre-Passage-Utc { param([string]$DatePub, [datetime]$MaintenantUtc = [datetime]::UtcNow)
    # la fenetre 23:00-01:00 (Paris) vue de l UTC : publication_date encore
    # «demain» au bord — le PUBLISH rend 400. On attend minuit UTC du jour voulu
    # (au plus une heure), puis le PUBLISH passe. Les brouillons vivent entre-temps.
    $d = Decision-Garde-Utc -DatePub $DatePub -MaintenantUtc $MaintenantUtc
    if (-not $d) { return }
    if ($d.Refus) { throw "garde UTC : $($d.Refus)" }
    Ecrire ("  [garde UTC] le bord vit encore le {0} : publication_date = {1} est DEMAIN au bord — un PUBLISH maintenant serait 400." -f $d.AujourdHui, $DatePub)
    Ecrire ("  [garde UTC] attente de {0} min jusqu a 00:00 UTC ({1} a ton poste) — les brouillons vivent, rien ne se perd." -f $d.Minutes, $d.Cible.ToLocalTime().ToString('HH:mm'))
    while (([datetime]::UtcNow - $d.Cible).TotalSeconds -lt 0) { Start-Sleep -Seconds 20 }
    Ecrire "  [garde UTC] minuit UTC passe — le bord vit le $DatePub : le PUBLISH suit."
}

function Trouve-Entree { param($Donnees, [string]$Nom)
    if (-not $Donnees) { return $null }
    if ($Donnees -is [System.Array]) {
        return @($Donnees) | Where-Object { $_.key -eq $Nom } | Select-Object -First 1
    }
    if ($Donnees.entries) {
        $es = $Donnees.entries
        if ($es -is [System.Array]) {
            return @($es) | Where-Object { $_.key -eq $Nom } | Select-Object -First 1
        }
        # la forme «carte» (nom -> objet) : acces direct, comme le patron python
        $prop = $es.PSObject.Properties[$Nom]
        if ($prop) { return $prop.Value }
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

    # 2. les fichiers — idempotents au bord (correctif d : le retour 01:14 —
    #    la reprise re-deposait les pieces DEJA COMMISES des brouillons de
    #    00:31 : le bord rendait 404 au commit et coupait la connexion au
    #    corps de 31 Mo ; une piece conforme n est plus re-téléversée).
    $FilesUrl = $brouillon.links.files
    $table = $null
    $r = Invoke-Zenodo -Methode Get -Uri $FilesUrl
    if ($r.Code -eq 200) { $table = $r.Donnees }
    foreach ($chemin in $Chemins) {
        $nom = [System.IO.Path]::GetFileName($chemin)
        $taille = (Get-Item -LiteralPath $chemin).Length
        $attendu = (Get-FileHash -LiteralPath $chemin -Algorithm MD5).Hash.ToLower()
        $entree = $null
        if ($table) { $entree = Trouve-Entree $table $nom }
        if ($entree) {
            $apiMd5 = ([string]$entree.checksum) -replace '^md5:', ''
            $tailleBord = 0
            try { $tailleBord = [int64]$entree.size } catch {}
            if ($apiMd5 -and ($apiMd5.ToLower() -eq $attendu) -and ($tailleBord -eq $taille)) {
                Ecrire ("  [fichier] {0} déjà déposé (md5 conforme) — sauté" -f $nom)
                continue
            }
            # present mais divergent (ou jamais commis) : le retirer d abord
            $r = Invoke-Zenodo -Methode Delete -Uri "$FilesUrl/$nom"
            if ($r.Code -notin 200, 201, 204, 404) {
                Ecrire ('RESULTAT|{0}|ROUGE|retrait-{1}-HTTP-{2}|—' -f $NomFlux, $nom, $r.Code)
                throw "retrait $nom : HTTP $($r.Code) $($r.Corps)"
            }
            $apibref = $apiMd5
            if (-not $apibref) { $apibref = '—' }
            Ecrire ("  [fichier] {0} retiré du brouillon (divergent au bord : {1} o, md5 {2}) — redéposé" -f $nom, $tailleBord, $apibref)
        }
        $r = Invoke-Zenodo -Methode Post -Uri $FilesUrl -CorpsJson (Convertir-Corps @(@{ key = $nom }))
        $entree = $null
        if ($r.Code -in 200, 201) { $entree = Trouve-Entree $r.Donnees $nom }
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
        Ecrire ("  [fichier] {0} déposé ({1} o)" -f $nom, $taille)
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

    # 4. PUBLISH — la garde UTC d abord : le bord vit la date UTC et refuse une
    #    publication_date encore «demain» (le 400 du 26/11 00:31, les deux flux).
    #    Aucun publish partiel : les fichiers sont deja verifies et engages.
    Attendre-Passage-Utc -DatePub $DatePub
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
            $apiMd5 = ([string]$ent.checksum) -replace '^md5:', ''
            if ($apiMd5 -and ($apiMd5.ToLower() -ne $attendu)) { $ecarts += $nom }
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
