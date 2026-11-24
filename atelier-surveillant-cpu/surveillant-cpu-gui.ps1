# surveillant-cpu-gui.ps1 - LA PIECE GUI DU COCKPIT (v1.0.0)
# ============================================================================
# Cette piece est DOT-SOURCEE par surveillant-cpu.ps1 (meme portee script) :
# elle porte les types WinForms/Drawing et la fenetre — RIEN de la logique.
# Elle ne vit que sur le poste Windows du terrain (PowerShell 5.1 d'origine,
# AUCUNE installation) ; jamais chargee par l'autotest -TestMode.
# ============================================================================

# ============================================================================
# LA GUI (Windows PowerShell 5.1 — AUCUNE installation ; WinForms)
# ============================================================================
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$script:SourceFreqVue = ''
$script:SourceTempVue = ''
$script:HistoFreq = New-Object System.Collections.Generic.List[double]
$script:HistoCharge = New-Object System.Collections.Generic.List[double]
$script:FontPetite = New-Object System.Drawing.Font('Consolas', 8)
$script:PenBase = New-Object System.Drawing.Pen([System.Drawing.Color]::Orange, 1)
$script:PenBase.DashStyle = [System.Drawing.Drawing2D.DashStyle]::Dash

function Mini([string]$texte) {
    if ($script:TxtConsole) {
        $script:TxtConsole.AppendText($texte + "`r`n")
    }
}

function Main-Gui {
    Init-Commun

    $form = New-Object System.Windows.Forms.Form
    $form.Text = 'TRIADE — SURVEILLANT-CPU : le cockpit du poste de test (v1.0.0)'
    $form.FormBorderStyle = [System.Windows.Forms.FormBorderStyle]::FixedSingle
    $form.MaximizeBox = $false
    $form.Size = New-Object System.Drawing.Size(1000, 750)
    $form.StartPosition = 'CenterScreen'

    # ---- les lignes d'information ----
    $lbl0 = New-Object System.Windows.Forms.Label
    $lbl0.Location = New-Object 'System.Drawing.Point' -ArgumentList (15, 12)
    $lbl0.Size = New-Object System.Drawing.Size(950, 20)
    $lbl0.Text = ('machine : ' + $script:NomMachine + '   OS : ' + $script:OsVersion +
                  "   (le cockpit ne mesure AUCUN temps d'execution — il constate la frequence)")
    $form.Controls.Add($lbl0)
    $lbl1 = New-Object System.Windows.Forms.Label
    $lbl1.Location = New-Object 'System.Drawing.Point' -ArgumentList (15, 32)
    $lbl1.Size = New-Object System.Drawing.Size(950, 20)
    $lbl1.Text = ('silicium : ' + $script:NomCpu)
    $form.Controls.Add($lbl1)
    $lbl2 = New-Object System.Windows.Forms.Label
    $lbl2.Location = New-Object 'System.Drawing.Point' -ArgumentList (15, 52)
    $lbl2.Size = New-Object System.Drawing.Size(950, 20)
    $lbl2.Text = ('base annoncee : ' + (F0 $script:BaseMHz) + ' MHz  ·  coeurs logiques : ' +
                  $script:CoeursLogiques + '  ·  kits : ' +
                  $(if ($script:BatKit2) { 'kit-2 VU' } else { 'kit-2 ABSENT' }) + ' · ' +
                  $(if ($script:BatKit3) { 'kit-3 VU' } else { 'kit-3 ABSENT' }) + ' · ' +
                  $(if ($script:BatKit1) { 'kit-1 VU' } else { 'kit-1 ABSENT' }))
    $form.Controls.Add($lbl2)
    $lbl3 = New-Object System.Windows.Forms.Label
    $lbl3.Location = New-Object 'System.Drawing.Point' -ArgumentList (15, 72)
    $lbl3.Size = New-Object System.Drawing.Size(950, 20)
    $lbl3.Text = 'frequence : compteur Processor Information de Windows  ·  temperature : zone thermique WMI  ·  granularite ~1 s'
    $form.Controls.Add($lbl3)

    # ---- les trois grandes lectures ----
    function Nouvelle-Lecture([int]$x, [string]$cap) {
        $c = New-Object System.Windows.Forms.Label
        $c.Location = New-Object 'System.Drawing.Point' -ArgumentList ($x, 100)
        $c.Size = New-Object System.Drawing.Size(300, 16)
        $c.Text = $cap
        $form.Controls.Add($c)
        $v = New-Object System.Windows.Forms.Label
        $v.Location = New-Object 'System.Drawing.Point' -ArgumentList ($x, 116)
        $v.Size = New-Object System.Drawing.Size(300, 44)
        $v.Font = New-Object System.Drawing.Font('Consolas', 24,
            [System.Drawing.FontStyle]::Bold)
        $v.Text = '…'
        $form.Controls.Add($v)
        return $v
    }
    $script:LblFreq = Nouvelle-Lecture 15 'FREQUENCE EFFECTIVE (MHz)'
    $script:LblCharge = Nouvelle-Lecture 340 'CHARGE TOTALE (%)'
    $script:LblTemp = Nouvelle-Lecture 665 'TEMPERATURE (degC)'

    # ---- la grille par coeur ----
    $lv = New-Object System.Windows.Forms.ListView
    $lv.Location = New-Object 'System.Drawing.Point' -ArgumentList (15, 175)
    $lv.Size = New-Object System.Drawing.Size(265, 250)
    $lv.View = [System.Windows.Forms.View]::Details
    $lv.FullRowSelect = $true
    [void]$lv.Columns.Add('Cœur', 50)
    [void]$lv.Columns.Add('Fréq (MHz)', 100)
    [void]$lv.Columns.Add('Charge (%)', 90)
    $form.Controls.Add($lv)
    $script:LvCoeurs = $lv

    # ---- le graphique (la peinture du cockpit — type cpu-z) ----
    $pnl = New-Object System.Windows.Forms.Panel
    $pnl.Location = New-Object 'System.Drawing.Point' -ArgumentList (295, 175)
    $pnl.Size = New-Object System.Drawing.Size(670, 250)
    $pnl.BorderStyle = [System.Windows.Forms.BorderStyle]::FixedSingle
    $pnl.BackColor = [System.Drawing.Color]::FromArgb(16, 20, 28)
    $form.Controls.Add($pnl)
    $script:PnlChart = $pnl
    $pnl.Add_Paint({
        param($s, $ev)
        $g = $ev.Graphics
        $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
        $w = $s.Width; $h = $s.Height
        $margeG = 46; $margeB = 18; $margeH = 8
        $maxF = 3000.0
        foreach ($v in $script:HistoFreq) { if ($v -gt $maxF) { $maxF = $v } }
        $maxF = [math]::Ceiling(($maxF + 250) / 500.0) * 500.0
        $blanc = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
        $gris = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(60, 70, 90), 1)
        # la grille : une ligne tous les 500 MHz, l'etiquette a gauche
        $pasY = ($h - $margeH - $margeB) / ($maxF / 500.0)
        $mhz = 0
        for ($y = $h - $margeB; $y -ge $margeH; $y -= $pasY) {
            $g.DrawLine($gris, $margeG, $y, $w - 8, $y)
            $g.DrawString([string]$mhz, $script:FontPetite, $blanc, 4, ($y - 7))
            $mhz += 500
        }
        if ($script:BaseMHz -gt 0) {
            $yB = $h - $margeB - ($script:BaseMHz / $maxF) * ($h - $margeH - $margeB)
            $g.DrawLine($script:PenBase, $margeG, $yB, $w - 8, $yB)
            $g.DrawString('base ' + (F0 $script:BaseMHz), $script:FontPetite,
                (New-Object System.Drawing.SolidBrush([System.Drawing.Color]::Orange)),
                ($margeG + 6), ($yB - 15))
        }
        $n = $script:HistoFreq.Count
        if ($n -ge 2) {
            $pasX = ($w - $margeG - 16) / [double]([math]::Max($n - 1, 1))
            $pts = New-Object 'System.Collections.Generic.List[System.Drawing.Point]'
            $ptsC = New-Object 'System.Collections.Generic.List[System.Drawing.Point]'
            for ($i = 0; $i -lt $n; $i++) {
                $x = $margeG + $i * $pasX
                $yF = $h - $margeB - ([math]::Min($script:HistoFreq[$i], $maxF) / $maxF) * ($h - $margeH - $margeB)
                $yC = $h - $margeB - ([math]::Min($script:HistoCharge[$i], 100.0) / 100.0) * ($h - $margeH - $margeB)
                $pts.Add((New-Object 'System.Drawing.Point' -ArgumentList ([int]$x, [int]$yF)))
                $ptsC.Add((New-Object 'System.Drawing.Point' -ArgumentList ([int]$x, [int]$yC)))
            }
            $g.DrawLines([System.Drawing.Pens]::LimeGreen, $ptsC.ToArray())
            $g.DrawLines((New-Object System.Drawing.Pen([System.Drawing.Color]::DeepSkyBlue, 2)), $pts.ToArray())
            $g.FillEllipse((New-Object System.Drawing.SolidBrush([System.Drawing.Color]::DeepSkyBlue)),
                ($pts[$n - 1].X - 3), ($pts[$n - 1].Y - 3), 6, 6)
        }
        $g.DrawString('frequence (MHz) — bleu', $script:FontPetite, $blanc, ($margeG + 4), 4)
        $g.DrawString('charge (%) — vert', $script:FontPetite,
            (New-Object System.Drawing.SolidBrush([System.Drawing.Color]::LimeGreen)), ($w - 140), 4)
        $blanc.Dispose(); $gris.Dispose()
    })

    # ---- les boutons des runs ----
    function Nouveau-Bouton([int]$x, [int]$y, [int]$w, [string]$texte, $action) {
        $b = New-Object System.Windows.Forms.Button
        $b.Location = New-Object 'System.Drawing.Point' -ArgumentList ($x, $y)
        $b.Size = New-Object System.Drawing.Size($w, 30)
        $b.Text = $texte
        $b.Add_Click($action)
        $form.Controls.Add($b)
        return $b
    }
    $script:BoutonsRun = @()
    $script:BoutonsRun += Nouveau-Bouton 15 440 100 'RUN N60'   { Demarrer-Run 60 }
    $script:BoutonsRun += Nouveau-Bouton 120 440 100 'RUN N200'  { Demarrer-Run 200 }
    $script:BoutonsRun += Nouveau-Bouton 225 440 100 'RUN N400'  { Demarrer-Run 400 }
    $script:BoutonsRun += Nouveau-Bouton 330 440 210 'BATTERIE 60-200-400' {
        $script:File.Clear()
        [void]$script:File.Add(60); [void]$script:File.Add(200); [void]$script:File.Add(400)
        Mini "LA BATTERIE : les trois runs dans l'ordre du LISEZMOI (60, puis 200, puis 400)."
        $suivant = [int]$script:File[0]; $script:File.RemoveAt(0)
        Demarrer-Run $suivant
    }
    $script:BoutonsRun += Nouveau-Bouton 560 440 130 'KIT-3 LOUPE' {
        Demarrer-Bat $script:BatKit3 '' 'KIT3-LOUPE' $false
    }
    $script:BoutonsRun += Nouveau-Bouton 700 440 130 'KIT-1 SHANI' {
        Demarrer-Bat $script:BatKit1 '' 'KIT1-SHANI' $false
    }

    # ---- les marqueurs et le temoin ----
    $txtMarque = New-Object System.Windows.Forms.TextBox
    $txtMarque.Location = New-Object 'System.Drawing.Point' -ArgumentList (15, 478)
    $txtMarque.Size = New-Object System.Drawing.Size(560, 24)
    $form.Controls.Add($txtMarque)
    $bMarquer = Nouveau-Bouton 585 476 110 'MARQUER' {
        if ($txtMarque.Text.Trim()) {
            Mark-Evenement ('MARQUE: ' + $txtMarque.Text.Trim())
            $txtMarque.Text = ''
        }
    }
    $bTemoin = Nouveau-Bouton 705 476 125 'ECRIRE LE TEMOIN' {
        $c = Compose-Temoin 'BOUTON'
        if ($c) { Mini ('le temoin compose : ' + (Split-Path $c -Leaf)) }
    }

    # ---- quitter et le statut ----
    $bQuitter = Nouveau-Bouton 15 514 110 'QUITTER' { $form.Close() }
    $script:LblStatut = New-Object System.Windows.Forms.Label
    $script:LblStatut.Location = New-Object 'System.Drawing.Point' -ArgumentList (135, 518)
    $script:LblStatut.Size = New-Object System.Drawing.Size(830, 22)
    $script:LblStatut.Text = 'PRET — la surveillance tourne (echantillon : 1 s ; 500 ms pendant un run).'
    $form.Controls.Add($script:LblStatut)

    # ---- la mini-console ----
    $script:TxtConsole = New-Object System.Windows.Forms.TextBox
    $script:TxtConsole.Location = New-Object 'System.Drawing.Point' -ArgumentList (15, 548)
    $script:TxtConsole.Size = New-Object System.Drawing.Size(950, 155)
    $script:TxtConsole.Multiline = $true
    $script:TxtConsole.ReadOnly = $true
    $script:TxtConsole.ScrollBars = 'Vertical'
    $script:TxtConsole.Font = New-Object System.Drawing.Font('Consolas', 8.5)
    $script:TxtConsole.BackColor = [System.Drawing.Color]::FromArgb(16, 20, 28)
    $script:TxtConsole.ForeColor = [System.Drawing.Color]::Gainsboro
    $form.Controls.Add($script:TxtConsole)

    # ---- la fermeture : le temoin se compose tout seul ----
    $form.Add_FormClosing({
        if ($script:Lignes.Count -gt 0 -and -not $script:TemoinEcrit) {
            $c = Compose-Temoin 'FERMETURE'
            if ($c) {
                $script:TxtConsole.AppendText('le temoin de fermeture est compose : ' +
                    (Split-Path $c -Leaf) + "`r`n")
                $script:TxtConsole.AppendText('A VOTRE MAIN : datez et signez le temoin, renvoyez le dossier ENTIER au coffre /test.')
            }
        }
    })

    # ---- le coeur : l'echantillonneur ----
    $script:Timer = New-Object System.Windows.Forms.Timer
    $script:Timer.Interval = 1000
    $script:Timer.Add_Tick({
        $e = Get-Echantillon
        $tmp = Get-Temperature
        if ($e.SourceFreq) { $script:SourceFreqVue = $e.SourceFreq }
        if ($tmp.Src) { $script:SourceTempVue = $tmp.Src }
        Add-Ligne $e $tmp ''
        # les lectures
        if ($null -ne $e.FreqTot) {
            $script:LblFreq.Text = F0 $e.FreqTot
            $script:HistoFreq.Add([double]$e.FreqTot)
        } else {
            $script:LblFreq.Text = 'ILLISIBLE'
            $script:HistoFreq.Add(0.0)
        }
        if ($null -ne $e.ChargeTot) {
            $script:LblCharge.Text = F0 $e.ChargeTot
            $script:HistoCharge.Add([double]$e.ChargeTot)
        } else {
            $script:LblCharge.Text = 'ILLISIBLE'
            $script:HistoCharge.Add(0.0)
        }
        if ($null -ne $tmp.C) { $script:LblTemp.Text = F $tmp.C }
        else { $script:LblTemp.Text = 'ABSENT' }
        # la grille par coeur
        if ($script:LvCoeurs.Items.Count -ne $e.Coeurs.Count) {
            $script:LvCoeurs.Items.Clear()
            for ($i = 0; $i -lt $e.Coeurs.Count; $i++) {
                [void]$script:LvCoeurs.Items.Add(('C' + $i))
                [void]$script:LvCoeurs.Items[$i].SubItems.Add('')
                [void]$script:LvCoeurs.Items[$i].SubItems.Add('')
            }
        }
        for ($i = 0; $i -lt $e.Coeurs.Count; $i++) {
            $script:LvCoeurs.Items[$i].SubItems[1].Text = F0 $e.Coeurs[$i].Freq
            $script:LvCoeurs.Items[$i].SubItems[2].Text = F0 $e.Coeurs[$i].Charge
        }
        if ($script:HistoFreq.Count -gt 360) { $script:HistoFreq.RemoveAt(0) }
        if ($script:HistoCharge.Count -gt 360) { $script:HistoCharge.RemoveAt(0) }
        $script:PnlChart.Invalidate()
        # le suivi des runs lances par le cockpit
        if ($script:Proc -and $script:Proc.HasExited) { Finaliser-Run }
        # le statut
        $script:LblStatut.Text = ('SURVEILLANCE EN COURS — echantillon n ' + $script:Lignes.Count +
            '  ·  ' + $(if ($script:Proc) { 'RUN EN COURS : ' + $script:RunLabel } else { 'aucun run lance par le cockpit' }))
    })
    $script:Timer.Start()

    Mini 'LE COCKPIT EST VIVANT. La surveillance tourne : chaque seconde, la frequence,'
    Mini 'la charge et la temperature sont affichees ET journalisees (csv ci-dessous).'
    Mini ('Le journal    : ' + (Split-Path $script:JournalCsv -Leaf))
    Mini 'Les boutons lancent les kits TELS QUELS (leurs .bat eprouves) ; chaque run est'
    Mini 'marque dans le journal ; le BROUILLON du kit-2 est renomme automatiquement.'
    Mini 'Mode surveillant seul : lancez vos kits vous-memes, MARQUEZ les instants.'
    Mini 'Le temoin se compose tout seul a la fermeture (bouton pour le composer avant).'
    if (-not $script:BatKit2) {
        Mini "[ECART NOMME] LANCER-KIT-2-DUDECT.bat introuvable depuis ce dossier — les"
        Mini '  boutons de run REFUSERONT nommement. Le cockpit doit vivre au RACINE du'
        Mini '  kit terrain (a cote de COMMENCER-ICI.bat) pour envelopper les kits.'
    }

    [void]$form.ShowDialog()
    $script:Timer.Stop()
    $form.Dispose()
}

Main-Gui
