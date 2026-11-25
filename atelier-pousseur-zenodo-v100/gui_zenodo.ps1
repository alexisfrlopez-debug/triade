# gui_zenodo.ps1 — TRIADE : le pousseur Zenodo 1-clic (interface Windows Forms).
# Un clic sur le bouton vert lance moteur_zenodo.ps1 (le patron v19 : newversion ->
# fichiers -> metadonnees -> PUBLISH -> verification md5) ; le journal est suivi
# en direct ; le jeton est lu de token-zenodo.txt par le moteur (jamais affiche).
# Correctif b (26/11/2026) : en PowerShell, $l et $L sont UNE seule variable (noms
# insensibles a la casse) — l'etiquette est $etq, la largeur $Largeur, la hauteur
# $Hauteur (l'edition a echouait : « convertir Label en Int32 » a chaque appel).
param(
    [string]$LotDir    = (Join-Path $PSScriptRoot 'lot'),
    [string]$TokenFile = (Join-Path $PSScriptRoot 'token-zenodo.txt'),
    [string]$Journal   = (Join-Path $PSScriptRoot 'PUSHER-JOURNAL.log')
)
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$Moteur = Join-Path $PSScriptRoot 'moteur_zenodo.ps1'
$BleuNuit  = [System.Drawing.Color]::FromArgb(20, 33, 61)
$Vert      = [System.Drawing.Color]::FromArgb(0, 120, 60)
$Rouge     = [System.Drawing.Color]::FromArgb(178, 34, 34)
$GrisFonce = [System.Drawing.Color]::FromArgb(70, 70, 70)

$form = New-Object System.Windows.Forms.Form
$form.Text = 'TRIADE — Pousseur Zenodo (1 clic) — protocole v0.31.0 + participation v1.2.0'
$form.Size = New-Object System.Drawing.Size(960, 745)
$form.StartPosition = 'CenterScreen'
$form.FormBorderStyle = 'FixedSingle'
$form.MaximizeBox = $false
$form.BackColor = [System.Drawing.Color]::FromArgb(250, 250, 246)

function Nouv-Etiquette {
    param([string]$Texte, [int]$X, [int]$Y, [int]$Largeur, [int]$Hauteur, [float]$Taille,
          [switch]$Gras, $Couleur)
    $etq = New-Object System.Windows.Forms.Label
    $etq.Text = $Texte
    $etq.Location = New-Object System.Drawing.Point($X, $Y)
    $etq.Size = New-Object System.Drawing.Size($Largeur, $Hauteur)
    $st = [System.Drawing.FontStyle]::Regular
    if ($Gras) { $st = [System.Drawing.FontStyle]::Bold }
    $etq.Font = New-Object System.Drawing.Font('Segoe UI', $Taille, $st)
    $etq.ForeColor = $Couleur
    $form.Controls.Add($etq)
    return $etq
}

[void](Nouv-Etiquette 'PUBLIER LES MISES À JOUR ZENODO — LE GESTE À UN CLIC' 15 12 920 26 14 -Gras $BleuNuit)
[void](Nouv-Etiquette 'Le lot pousse : protocole v0.26.0 → v0.31.0 (les trois packs) · participation v1.1.0 → v1.2.0 (le pack des cinq kits).' 15 42 920 20 9.5 $GrisFonce)
[void](Nouv-Etiquette 'Kit développeur v1.3.0, corpus v2.1 et TRIADE-TRAIN v1.0.0 : INCHANGÉS — aucune version creuse (la doctrine), ils ne sont pas republiés.' 15 61 920 20 9.5 $GrisFonce)
[void](Nouv-Etiquette 'LE LOT — quatre packs, empreintes vérifiées au manifeste au chargement :' 15 92 920 20 10 -Gras $BleuNuit)

$liste = New-Object System.Windows.Forms.ListView
$liste.View = 'Details'
$liste.FullRowSelect = $true
$liste.HeaderStyle = 'Nonclickable'
$liste.Location = New-Object System.Drawing.Point(15, 114)
$liste.Size = New-Object System.Drawing.Size(925, 132)
$liste.Font = New-Object System.Drawing.Font('Consolas', 8.5)
[void]$liste.Columns.Add('fichier (le lot)', 380)
[void]$liste.Columns.Add('octets', 90)
[void]$liste.Columns.Add('sha256 (32 premiers)', 340)
[void]$liste.Columns.Add('état', 90)
$form.Controls.Add($liste)

[void](Nouv-Etiquette 'LES CIBLES ZENODO :' 15 256 920 20 10 -Gras $BleuNuit)
[void](Nouv-Etiquette '1. PROTOCOLE — record 24499428 (concept 10.5281/zenodo.24367343) : v0.26.0 → v0.31.0 — soumission · présentation · complet' 15 278 920 20 9.5 $GrisFonce)
[void](Nouv-Etiquette '2. PARTICIPATION — record 24499847 (concept 10.5281/zenodo.24497299) : v1.1.0 → v1.2.0 — le pack des cinq kits' 15 298 920 20 9.5 $GrisFonce)

$bouton = New-Object System.Windows.Forms.Button
$bouton.Text = 'PUBLIER SUR ZENODO — 1 CLIC'
$bouton.Location = New-Object System.Drawing.Point(15, 326)
$bouton.Size = New-Object System.Drawing.Size(925, 50)
$bouton.BackColor = $Vert
$bouton.ForeColor = [System.Drawing.Color]::White
$bouton.Font = New-Object System.Drawing.Font('Segoe UI', 12, [System.Drawing.FontStyle]::Bold)
$bouton.FlatStyle = 'Standard'
$form.Controls.Add($bouton)

[void](Nouv-Etiquette 'LE JOURNAL DU MOTEUR (suivi en direct — la preuve de chaque geste) :' 15 386 920 20 10 -Gras $BleuNuit)

$rtb = New-Object System.Windows.Forms.RichTextBox
$rtb.Location = New-Object System.Drawing.Point(15, 408)
$rtb.Size = New-Object System.Drawing.Size(925, 268)
$rtb.Font = New-Object System.Drawing.Font('Consolas', 9)
$rtb.ReadOnly = $true
$rtb.BackColor = [System.Drawing.Color]::White
$rtb.DetectUrls = $false
$form.Controls.Add($rtb)

$statut = New-Object System.Windows.Forms.Label
$statut.Text = 'Chargement du lot…'
$statut.Location = New-Object System.Drawing.Point(15, 682)
$statut.Size = New-Object System.Drawing.Size(925, 20)
$statut.Font = New-Object System.Drawing.Font('Segoe UI', 9)
$statut.ForeColor = $BleuNuit
$form.Controls.Add($statut)

$script:LotOk = $false
$script:proc = $null
$script:vu = 0

$timer = New-Object System.Windows.Forms.Timer
$timer.Interval = 400

# --------- le chargement : la verification byte-byte du lot au manifeste -------
$form.Add_Load({
    $script:LotOk = $true
    $man = $null
    $mp = Join-Path $LotDir 'MANIFESTE-PACKS-v0.31.0.json'
    if (Test-Path -LiteralPath $mp) { $man = Get-Content -LiteralPath $mp -Raw | ConvertFrom-Json }
    foreach ($nom in @('TRIADE_soumission_v0.31.0.zip', 'TRIADE_presentation_v0.31.0.zip',
                       'TRIADE_complet_v0.31.0.zip', 'TRIADE_participer_v1.2.0.zip')) {
        $p = Join-Path $LotDir $nom
        $taille = '—'; $sha = '—'; $etat = 'MANQUANT'; $couleur = $Rouge
        if (Test-Path -LiteralPath $p) {
            $taille = (Get-Item -LiteralPath $p).Length
            $h = (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLower()
            $sha = $h.Substring(0, 32)
            $m = $null
            if ($man) { $m = $man.PSObject.Properties[$nom].Value }
            if ($m -and ([int64]$m.bytes -eq $taille) -and ($m.sha256 -eq $h)) {
                $etat = 'OK'; $couleur = $Vert
            } elseif ($m) {
                $etat = 'ÉCART!'; $couleur = $Rouge; $script:LotOk = $false
            }
        } else { $script:LotOk = $false }
        $it = New-Object System.Windows.Forms.ListViewItem($nom)
        [void]$it.SubItems.Add([string]$taille)
        [void]$it.SubItems.Add($sha)
        [void]$it.SubItems.Add($etat)
        $it.ForeColor = $couleur
        [void]$liste.Items.Add($it)
        [System.Windows.Forms.Application]::DoEvents()
    }
    if (-not (Test-Path -LiteralPath $Moteur)) {
        $bouton.Enabled = $false
        $statut.Text = 'moteur_zenodo.ps1 introuvable — le clic est désactivé.'
        $statut.ForeColor = $Rouge
        return
    }
    $jetonPresent = (Test-Path -LiteralPath $TokenFile) -and
        ((Get-Content -LiteralPath $TokenFile -Raw).Trim().Length -gt 0)
    if (-not $jetonPresent) {
        $script:LotOk = $false
        $bouton.Enabled = $false
        $statut.Text = 'JETON ABSENT (token-zenodo.txt) — le clic est désactivé.'
        $statut.ForeColor = $Rouge
    } elseif ($script:LotOk) {
        $statut.Text = 'Lot vérifié 4/4 byte-byte — prêt. Un clic fait le geste (idempotent : brouillon repris, publié sauté).'
    } else {
        $bouton.Enabled = $false
        $statut.Text = 'ÉCART au lot — le clic est désactivé (retélécharge le lot).'
        $statut.ForeColor = $Rouge
    }
    # l'historique éventuel d'un run précédent, affiché dès l'ouverture
    if (Test-Path -LiteralPath $Journal) {
        $anciennes = [System.IO.File]::ReadAllLines($Journal)
        foreach ($t in $anciennes) { $rtb.AppendText($t + "`r`n") }
        $rtb.SelectionStart = $rtb.Text.Length
        [void]$rtb.ScrollToCaret()
    }
})

# -------------------------------- le clic unique : le moteur est lancé --------
$bouton.Add_Click({
    if (-not $script:LotOk) { return }
    $bouton.Enabled = $false
    $form.Cursor = [System.Windows.Forms.Cursors]::WaitCursor
    $statut.Text = 'EN COURS — newversion, fichiers, métadonnées, PUBLISH, vérification md5…'
    if (Test-Path -LiteralPath $Journal) {
        $script:vu = [System.IO.File]::ReadAllLines($Journal).Count
    } else { $script:vu = 0 }
    $a = "-NoProfile -ExecutionPolicy Bypass -File ""$Moteur"" -LotDir ""$LotDir"" -TokenFile ""$TokenFile"" -Journal ""$Journal"""
    $script:proc = Start-Process -FilePath 'powershell.exe' -ArgumentList $a -WindowStyle Hidden -PassThru
    $timer.Start()
})

# ------------------------- le journal suivi en direct (toutes les 400 ms) ----
$timer.Add_Tick({
    if (-not $script:proc) { return }
    if (Test-Path -LiteralPath $Journal) {
        try {
            $lignes = [System.IO.File]::ReadAllLines($Journal)
            $n = $lignes.Count
            $fini = $script:proc.HasExited
            $limite = $n - 1
            if (-not $fini) { $limite = $n - 2 }   # la dernière ligne peut être partielle
            while ($script:vu -le $limite) {
                $t = $lignes[$script:vu]
                if ($t -match 'VERT') { $rtb.SelectionColor = $Vert }
                elseif ($t -match 'ROUGE|ÉCART|BLOCAGE|refus') { $rtb.SelectionColor = $Rouge }
                else { $rtb.SelectionColor = [System.Drawing.Color]::Black }
                $rtb.AppendText($t + "`r`n")
                $script:vu++
            }
            $rtb.SelectionStart = $rtb.Text.Length
            [void]$rtb.ScrollToCaret()
        } catch { }
    }
    if (-not $script:proc.HasExited) { return }
    $timer.Stop()
    $form.Cursor = [System.Windows.Forms.Cursors]::Default
    $code = $script:proc.ExitCode
    $prot = '(pas de verdict)'; $part = '(pas de verdict)'
    if (Test-Path -LiteralPath $Journal) {
        foreach ($l in [System.IO.File]::ReadAllLines($Journal)) {
            if ($l -like 'RESULTAT|protocole|*') {
                $champs = $l -split '\|'
                $prot = ('{0} — {1}' -f $champs[2], $champs[3])
            }
            if ($l -like 'RESULTAT|participation|*') {
                $champs = $l -split '\|'
                $part = ('{0} — {1}' -f $champs[2], $champs[3])
            }
            if ($l -like 'DEJA|protocole|*') { $prot = 'DÉJÀ PUBLIÉE (sauté)' }
            if ($l -like 'DEJA|participation|*') { $part = 'DÉJÀ PUBLIÉE (sauté)' }
        }
    }
    $msg = "PROTOCOLE v0.31.0 : $prot`r`nPARTICIPATION v1.2.0 : $part`r`n`r`n" +
        'Les DOI de version résolvent chez doi.org sous quelques minutes.' + "`r`n" +
        'DIS-LE AU BAC : la chaîne complète suivra (livrables du coffre, ARCHIVE, miroirs, worklog).'
    [void][System.Windows.Forms.MessageBox]::Show($form, $msg, 'TRIADE — publication Zenodo', 'OK', 'Information')
    $statut.Text = "Terminé (code $code). Relance = reprise idempotente."
    $bouton.Text = 'REPRENDRE / RELANCER (idempotent)'
    $bouton.Enabled = $true
})

[void]$form.ShowDialog()
$form.Dispose()
