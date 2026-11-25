# surveillant-cpu.ps1 - LE COCKPIT DU POSTE DE TEST (edition PC-WINDOWS, v1.0.1)
# ============================================================================
# La commande (le developpeur, 25/11/2026) : « concerning les etats
# processeurs du pc de test, tu n'as pas moyen d'englober les tests dans
# une GUI qui affiche et log les valeurs de frequence cpu etc... en temps
# reel (type cpu-z) mais durant les tests ? »
#
# LE CORRECTIF v1.0.1 (25/11 au soir : le terrain a parle, D189) : la classe
# ProcessorInformation expose un AGREGAT PAR NOEUD (« 0,_Total ») que la
# v1.0.0 laissait entrer dans la table des coeurs — la ligne C4 fantome du
# terrain et l'erreur Sort-Object a chaque echantillon. Desormais seules les
# instances « noeud,coeur » toutes numeriques vivent parmi les coeurs ; la
# mockerie d'autotest GAGNE cette instance et l'autotest REFUSE tout agregat
# parmi les coeurs. L'histoire complete vit a ERRATUM-SURVEILLANT-v101.txt.
#
# CE QUE CE COCKPIT EST :
#   - l'OBSERVATOIRE : la frequence effective de CHAQUE coeur (le compteur
#     Processor Information de Windows — ProcessorFrequency en MHz, sinon
#     la base x %ProcessorPerformance), la charge par coeur, la temperature
#     (MSAcpi_ThermalZoneTemperature, la zone thermique que Windows expose
#     — la seule lisible sans pilote), lues ~1 fois par seconde (500 ms
#     pendant un run), AFFICHEES et JOURNALISEES dans un csv ;
#   - L'ENVELOPPE : les boutons lancent les kits eux-memes (leurs .bat
#     eprouves, jamais reecrits) — kit-2 N60/N200/N400, la BATTERIE
#     60->200->400 dans l'ordre du LISEZMOI, kit-3 loupe, kit-1 shani ;
#     chaque lancement MARQUE le journal (DEBUT-RUN-... / FIN-RUN-...),
#     le BROUILLON du kit-2 est RENOMME automatiquement
#     (temoin-dudect-N<n>.txt — le geste que le LISEZMOI demandait a la
#     main), le journal csv du run est nomine, les dernieres lignes de
#     sortie-run.txt sont montrees au cockpit ;
#   - LE TEMOIN : un bout (et la fermeture) compose
#     temoin-surveillant-<horodatage>.txt — machine, silicium, base,
#     sources, stats globales, ET PAR RUN : freq min/med/max, charge
#     moy/max, temperature min/max DANS LA FENETRE du run ; la PREUVE DU
#     TURBO (le nombre d'echantillons au-dessus de la base = le turbo
#     VECU ; sous la base = economie/throttle) ;
#   - LA CAUSE (pourquoi il existe) : le premier run terrain du kit-2
#     (24/11, i7-3667U Ivy Bridge 2 coeurs) rendit trois divergences
#     |t|>5 sur une fenetre de mesure totale de 92 ms, classes
#     SEQUENTIELLES : le t de Welch y mesure la classe ET le temps (la
#     derive DVFS lue aux quartiles du csv). Ce cockpit ne maquille rien :
#     il CONSIGNE la frequence pour que la prochaine lecture des
#     divergences se fasse sur pieces.
#
# LES REFUS NOMMES (fail-closed, comme tout le kit) :
#   - compteur Processor Information illisible -> l'ecart est NOMME,
#     l'echantillon porte ses colonnes vides, le cockpit continue ;
#   - temperature illisible -> « ABSENT (nomme) », jamais un chiffre
#     invente ;
#   - .bat introuvable -> le bout REFUSE et le dit ;
#   - un run qui rend un code non nul -> la batterie S'ARRETE (jamais
#     une mesure habillee en batterie).
#
# LA MESURE D'OBSERVATEUR (dite honnetement) : la lecture des compteurs
# ajoute une legere charge a la machine (WMI ~2 requetes/seconde). Les
# runs dudect epinglent le coeur 0 par eux-memes ; les compteurs
# vivent ailleurs. La granularite du compteur Windows est ~1 s : le
# journal dessine le CADRE de frequence autour du run (le regime turbo
# ou throttle), pas l'instant intra-run (le run dudect du 24/11 ne
# mesura que 92 ms au total).
#
# L'EPROUVAGE : le mode -TestMode vit la LOGIQUE sans GUI (12
# echantillons simules, deux fenetres de run, un marqueur manuel, le
# csv et le temoin composes) — eprouve au laboratoire sous PowerShell
# 7.4.6 (Linux). La GUI vit par Windows PowerShell 5.1 (livre avec
# Windows 10 et 11 — AUCUNE installation) ; elle ne put etre vecue au
# laboratoire (aucun Windows au labo) : votre run en est le premier
# temoin, l'ecart est nomme ici (D189).
#
# Usage : SURVEILLANT-CPU.bat            (le lanceur eprouve)
#         powershell -File surveillant-cpu.ps1 -TestMode   (l'autotest)
# ============================================================================

param([switch]$TestMode)

# ----------------------------------------------------------------------------
# L'ETAT PARTAGE
# ----------------------------------------------------------------------------
$script:Depart        = Get-Date
$script:JournalCsv    = $null
$script:Lignes        = New-Object System.Collections.ArrayList
$script:Fenetres      = New-Object System.Collections.ArrayList
$script:FenetreOuverte = -1
$script:FenetreLabel  = ''
$script:TemoinEcrit   = $false
$script:BaseMHz       = 0.0
$script:NomCpu        = '?'
$script:CoeursLogiques = 0
$script:NomMachine    = $env:COMPUTERNAME
$script:OsVersion     = [System.Environment]::OSVersion.Version.ToString()
$script:BatKit2       = $null
$script:BatKit3       = $null
$script:BatKit1       = $null
$script:Proc          = $null
$script:RunLabel      = ''
$script:RunKit2       = $false
$script:File          = New-Object System.Collections.ArrayList
$script:FichierStdin  = $null

# ----------------------------------------------------------------------------
# LES OUTILS DE FORME (culture INVARIANTE : la virgule decimale ne vivra
# jamais dans un csv separe par des virgules)
# ----------------------------------------------------------------------------
$script:Inv = [System.Globalization.CultureInfo]::InvariantCulture
function F([double]$v) {
    if ($v -le -1e17 -or $v -ge 1e17) { return 'nan' }
    return [math]::Round($v, 1).ToString($script:Inv)
}
function F0([double]$v) {
    return [math]::Round($v, 0).ToString($script:Inv)
}
function Iso([datetime]$t) {
    return $t.ToString('yyyy-MM-dd HH:mm:ss.fff', $script:Inv)
}

# ----------------------------------------------------------------------------
# LA LECTURE DU SILICIUM (les compteurs de Windows, locaux-indépendants :
# jamais un chemin de compteur localise — la classe WMI fait foi)
# ----------------------------------------------------------------------------
function Get-Echantillon {
    $ret = @{ FreqTot = $null; ChargeTot = $null; SourceFreq = '';
              Coeurs = @() }
    $perf = Get-CimInstance -ClassName 'Win32_PerfFormattedData_Counters_ProcessorInformation' -ErrorAction SilentlyContinue
    if (-not $perf) { return $ret }
    # v1.0.1 : la classe expose TROIS familles d'instances — les coeurs
    # (« noeud,coeur » : 0,0 0,1 ...), l'agregat global (« _Total ») ET
    # L'AGREGAT PAR NOEUD (« 0,_Total ») que la v1.0.0 laissait entrer parmi
    # les coeurs. L'agregat global reste cherche sous ses deux noms ; ne
    # vivent parmi les coeurs que les instances toutes numeriques.
    $total = $null
    foreach ($row in $perf) { if ($row.Name -eq '_Total') { $total = $row; break } }
    if (-not $total) {
        foreach ($row in $perf) { if ($row.Name -like '*,_Total') { $total = $row; break } }
    }
    foreach ($row in $perf) {
        if ($row.Name -notmatch '^[0-9]+,[0-9]+$') { continue }
        $freq = 0.0
        if ($row.PSObject.Properties['ProcessorFrequency'] -and
            $row.ProcessorFrequency -and [double]$row.ProcessorFrequency -gt 0) {
            $freq = [double]$row.ProcessorFrequency
            $ret.SourceFreq = 'ProcessorFrequency (MHz, le compteur de Windows)'
        } elseif ($row.PSObject.Properties['PercentProcessorPerformance'] -and
                  $null -ne $row.PercentProcessorPerformance -and $script:BaseMHz -gt 0) {
            $freq = $script:BaseMHz * [double]$row.PercentProcessorPerformance / 100.0
            $ret.SourceFreq = 'base x PercentProcessorPerformance (le calcul du cockpit)'
        }
        $charge = 0.0
        if ($row.PSObject.Properties['PercentProcessorTime'] -and
            $null -ne $row.PercentProcessorTime) {
            $charge = [double]$row.PercentProcessorTime
        }
        $ret.Coeurs += @{ Nom = $row.Name; Freq = $freq; Charge = $charge }
    }
    $ret.Coeurs = @($ret.Coeurs |
        Sort-Object { [int]($_.Nom.Split(',')[0]) }, { [int]($_.Nom.Split(',')[1]) })
    if ($total) {
        if ($total.PSObject.Properties['ProcessorFrequency'] -and
            $total.ProcessorFrequency -and [double]$total.ProcessorFrequency -gt 0) {
            $ret.FreqTot = [double]$total.ProcessorFrequency
        } elseif ($total.PSObject.Properties['PercentProcessorPerformance'] -and
                  $null -ne $total.PercentProcessorPerformance -and $script:BaseMHz -gt 0) {
            $ret.FreqTot = $script:BaseMHz * [double]$total.PercentProcessorPerformance / 100.0
        }
        if ($total.PSObject.Properties['PercentProcessorTime'] -and
            $null -ne $total.PercentProcessorTime) {
            $ret.ChargeTot = [double]$total.PercentProcessorTime
        }
    }
    if ($null -eq $ret.FreqTot -and $ret.Coeurs.Count -gt 0) {
        $s = 0.0; $n = 0
        foreach ($c in $ret.Coeurs) { if ($c.Freq -gt 0) { $s += $c.Freq; $n++ } }
        if ($n -gt 0) { $ret.FreqTot = $s / $n }
    }
    if ($null -eq $ret.ChargeTot -and $ret.Coeurs.Count -gt 0) {
        $s = 0.0
        foreach ($c in $ret.Coeurs) { $s += $c.Charge }
        $ret.ChargeTot = $s / $ret.Coeurs.Count
    }
    return $ret
}

function Get-Temperature {
    $t = Get-CimInstance -Namespace 'root/wmi' -ClassName 'MSAcpi_ThermalZoneTemperature' -ErrorAction SilentlyContinue
    if ($t) {
        $max = ($t | ForEach-Object { [double]$_.CurrentTemperature } |
                Measure-Object -Maximum).Maximum
        if ($max -gt 0) {
            return @{ C = [math]::Round($max / 10.0 - 273.15, 1)
                      Src = 'MSAcpi_ThermalZoneTemperature (root/wmi)' }
        }
    }
    $z = Get-CimInstance -ClassName 'Win32_PerfFormattedData_Counters_ThermalZoneInformation' -ErrorAction SilentlyContinue
    if ($z) {
        $max = ($z | ForEach-Object { [double]$_.Temperature } |
                Measure-Object -Maximum).Maximum
        if ($max -gt 0) {
            return @{ C = [math]::Round($max - 273.15, 1)
                      Src = 'ThermalZoneInformation (le compteur)' }
        }
    }
    return @{ C = $null; Src = 'ABSENT (nomme — aucune zone thermique lisible sans pilote)' }
}

# ----------------------------------------------------------------------------
# LE JOURNAL (une ligne par echantillon ; l'evenement vit dans sa colonne)
# ----------------------------------------------------------------------------
function Add-Ligne($e, $tmp, $evenement) {
    $freqJoin = ($e.Coeurs | ForEach-Object { F $_.Freq }) -join ';'
    $chargeJoin = ($e.Coeurs | ForEach-Object { F0 $_.Charge }) -join ';'
    $tC = ''
    if ($null -ne $tmp.C) { $tC = F $tmp.C }
    $ft = ''
    if ($null -ne $e.FreqTot) { $ft = F $e.FreqTot }
    $ct = ''
    if ($null -ne $e.ChargeTot) { $ct = F0 $e.ChargeTot }
    $row = (Iso (Get-Date)) + ',' + $evenement + ',' + $ft + ',' + $ct +
           ',' + $tC + ',' + $freqJoin + ',' + $chargeJoin
    if ($script:JournalCsv) {
        Add-Content -Path $script:JournalCsv -Value $row -Encoding UTF8
    }
    [void]$script:Lignes.Add(@{ T = (Get-Date); Ev = $evenement
                                Freq = $e.FreqTot; Charge = $e.ChargeTot
                                Temp = $tmp.C })
}

function Mark-Evenement([string]$label) {
    $e = Get-Echantillon
    $tmp = Get-Temperature
    Add-Ligne $e $tmp $label
    if ($label -like 'DEBUT-RUN-*') {
        $script:FenetreOuverte = $script:Lignes.Count - 1
        $script:FenetreLabel = $label.Substring('DEBUT-RUN-'.Length)
    } elseif ($label -like 'FIN-RUN-*' -and $script:FenetreOuverte -ge 0) {
        [void]$script:Fenetres.Add(@{ Label = $script:FenetreLabel
                                       Debut = $script:FenetreOuverte
                                       Fin = $script:Lignes.Count - 1 })
        $script:FenetreOuverte = -1
    }
    if (-not $TestMode -and $script:TxtConsole) {
        $script:TxtConsole.AppendText((Iso (Get-Date)) + '  ' + $label + "`r`n")
    }
}

# ----------------------------------------------------------------------------
# LES STATS (min / mediane / max d'une tranche de lignes)
# ----------------------------------------------------------------------------
function Stats-Freq([int]$d, [int]$f) {
    $v = @()
    for ($i = $d; $i -le $f; $i++) {
        if ($null -ne $script:Lignes[$i].Freq) { $v += [double]$script:Lignes[$i].Freq }
    }
    if ($v.Count -eq 0) { return $null }
    $s = $v | Sort-Object
    return @{ Min = $s[0]; Med = $s[[int]($s.Count / 2)]; Max = $s[-1]
              N = $v.Count }
}

function Compose-Temoin([string]$raison) {
    if ($script:TemoinEcrit -and $raison -eq 'FERMETURE') { return $null }
    if ($script:Lignes.Count -eq 0) { return $null }
    $l = New-Object System.Collections.ArrayList
    [void]$l.Add('LE TEMOIN SURVEILLANT — le cockpit du poste de test (v1.0.1)')
    [void]$l.Add('=' * 68)
    [void]$l.Add(('compose le    : ' + (Iso (Get-Date)) + ' (' + $raison + ')'))
    [void]$l.Add(('la machine    : ' + $script:NomMachine + '  OS ' + $script:OsVersion))
    [void]$l.Add(('le silicium   : ' + $script:NomCpu))
    [void]$l.Add(('la base       : ' + (F0 $script:BaseMHz) + ' MHz annonces (Win32_Processor.MaxClockSpeed)'))
    [void]$l.Add(('la source freq: ' + $script:SourceFreqVue))
    [void]$l.Add(('la source temp: ' + $script:SourceTempVue))
    [void]$l.Add('')
    [void]$l.Add('LE JOURNAL    : ' + (Split-Path $script:JournalCsv -Leaf))
    if ($script:JournalCsv -and (Test-Path $script:JournalCsv)) {
        $h = Get-FileHash -Path $script:JournalCsv -Algorithm SHA256
        [void]$l.Add(('  sha256      : ' + $h.Hash.ToLower()))
    }
    [void]$l.Add(('les echantillons : ' + $script:Lignes.Count))
    $g = Stats-Freq 0 ($script:Lignes.Count - 1)
    if ($g) {
        [void]$l.Add(('LA FREQUENCE GLOBALE : min ' + (F0 $g.Min) + '  med ' + (F0 $g.Med) +
                      '  max ' + (F0 $g.Max) + ' MHz'))
    }
    $charges = @($script:Lignes | ForEach-Object { $_.Charge } |
                 Where-Object { $null -ne $_ })
    if ($charges.Count -gt 0) {
        $moy = ($charges | Measure-Object -Average).Average
        $mx = ($charges | Measure-Object -Maximum).Maximum
        [void]$l.Add(('LA CHARGE            : moy ' + (F0 $moy) + ' %  max ' + (F0 $mx) + ' %'))
    }
    $temps = @($script:Lignes | ForEach-Object { $_.Temp } |
              Where-Object { $null -ne $_ })
    if ($temps.Count -gt 0) {
        [void]$l.Add(('LA TEMPERATURE       : min ' + (F ($temps | Measure-Object -Minimum).Minimum) +
                      '  max ' + (F ($temps | Measure-Object -Maximum).Maximum) + ' degC'))
    }
    if ($script:BaseMHz -gt 0 -and $g) {
        $turbo = 0; $sous = 0
        foreach ($ln in $script:Lignes) {
            if ($null -ne $ln.Freq) {
                if ([double]$ln.Freq -gt $script:BaseMHz * 1.02) { $turbo++ }
                elseif ([double]$ln.Freq -lt $script:BaseMHz * 0.98) { $sous++ }
            }
        }
        [void]$l.Add(('LA PREUVE DU TURBO   : ' + $turbo + '/' + $script:Lignes.Count +
                      ' echantillons AU-DESSUS de la base (turbo vecu) ; ' + $sous +
                      ' SOUS la base (economie/throttle)'))
    }
    if ($script:Fenetres.Count -gt 0) {
        [void]$l.Add('')
        [void]$l.Add('LES FENETRES DE RUN (la frequence VECUE pendant chaque test) :')
        foreach ($fen in $script:Fenetres) {
            $s = Stats-Freq $fen.Debut $fen.Fin
            $duree = ($script:Lignes[$fen.Fin].T - $script:Lignes[$fen.Debut].T).TotalSeconds
            $ligne = '  ' + $fen.Label + ' (' + (F $duree) + ' s) : '
            if ($s) {
                $ligne += 'freq min ' + (F0 $s.Min) + '  med ' + (F0 $s.Med) +
                          '  max ' + (F0 $s.Max) + ' MHz'
            } else {
                $ligne += 'freq ILLISIBLE (nomme)'
            }
            $tc = @()
            for ($i = $fen.Debut; $i -le $fen.Fin; $i++) {
                if ($null -ne $script:Lignes[$i].Temp) { $tc += [double]$script:Lignes[$i].Temp }
            }
            if ($tc.Count -gt 0) {
                $ligne += '  temp ' + (F ($tc | Measure-Object -Minimum).Minimum) + '-' +
                          (F ($tc | Measure-Object -Maximum).Maximum) + ' degC'
            }
            [void]$l.Add($ligne)
        }
    }
    $evts = @($script:Lignes | Where-Object { $_.Ev })
    if ($evts.Count -gt 0) {
        [void]$l.Add('')
        [void]$l.Add("LES EVENEMENTS (l'horodatage exact de chaque geste) :")
        foreach ($ln in $evts) { [void]$l.Add('  ' + (Iso $ln.T) + '  ' + $ln.Ev) }
    }
    [void]$l.Add('')
    [void]$l.Add('LA LECTURE HONNETE : ce temoin CONSTATE la frequence, la charge et')
    [void]$l.Add("la temperature VECUES pendant les runs — il ne mesure aucun temps")
    [void]$l.Add("d'execution (le mesureur du kit-2 fait cela, sur ses pieces scellees).")
    [void]$l.Add('La granularite du compteur Windows est ~1 s : le journal dessine le')
    [void]$l.Add("CADRE de frequence du run (le regime turbo/throttle), pas l'instant")
    [void]$l.Add('intra-run. Les divergences |t|>5 du kit-2 se lisent AVEC ce cadre.')
    [void]$l.Add('')
    [void]$l.Add('signature du geste : a dater et a signer de la main du developpeur.')
    $nom = 'temoin-surveillant-' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '.txt'
    $chemin = Join-Path $PSScriptRoot $nom
    $l | Out-File -FilePath $chemin -Encoding UTF8
    $script:TemoinEcrit = $true
    return $chemin
}

# ----------------------------------------------------------------------------
# LA RECHERCHE DES KITS (les .bat eprouves, jamais reecrits)
# ----------------------------------------------------------------------------
function Trouver-Bat([string]$nom) {
    $r = Get-ChildItem -Path $PSScriptRoot -Recurse -Filter $nom -ErrorAction SilentlyContinue |
         Select-Object -First 1
    if ($r) { return $r.FullName }
    return $null
}

# ----------------------------------------------------------------------------
# LES RUNS (l'enveloppe : les .bat des kits, lances tels quels)
# ----------------------------------------------------------------------------
function Demarrer-Bat([string]$bat, [string]$arguments, [string]$label, [bool]$estKit2) {
    if ($script:Proc) { return }
    if (-not $bat -or -not (Test-Path $bat)) {
        Mark-Evenement ('REFUS-NOMME ' + $label + ' : le .bat du kit est introuvable')
        return
    }
    $argsBat = "/c `"" + $bat + "`""
    if ($arguments) { $argsBat += ' ' + $arguments }
    $script:Proc = Start-Process -FilePath 'cmd.exe' -ArgumentList $argsBat `
        -WorkingDirectory (Split-Path $bat) `
        -RedirectStandardInput $script:FichierStdin -PassThru
    $script:RunLabel = $label
    $script:RunKit2 = $estKit2
    Mark-Evenement ('DEBUT-RUN-' + $label)
    if (-not $TestMode -and $script:Timer) { $script:Timer.Interval = 500 }
    if (-not $TestMode) {
        foreach ($b in $script:BoutonsRun) { $b.Enabled = $false }
        $script:LblStatut.Text = ('EN COURS : ' + $label + ' — la surveillance continue (500 ms)')
    }
}

function Demarrer-Run([int]$n) {
    Demarrer-Bat $script:BatKit2 ([string]$n) ('N' + $n) $true
}

function Finaliser-Run {
    $code = 0
    try { $code = $script:Proc.ExitCode } catch { $code = -1 }
    Mark-Evenement ('FIN-RUN-' + $script:RunLabel + ' code=' + $code)
    if ($script:RunKit2 -and $script:BatKit2) {
        $kit2dir = Split-Path $script:BatKit2
        $brouillon = Join-Path $kit2dir 'temoin-dudect-BROUILLON.txt'
        if (Test-Path $brouillon) {
            $cible = Join-Path $kit2dir ('temoin-dudect-' + $script:RunLabel + '.txt')
            if (Test-Path $cible) {
                $cible = Join-Path $kit2dir ('temoin-dudect-' + $script:RunLabel + '-' +
                         (Get-Date -Format 'HHmmss') + '.txt')
            }
            Move-Item -Path $brouillon -Destination $cible -Force
            if ($script:TxtConsole) {
                $script:TxtConsole.AppendText('  le BROUILLON renomme : ' +
                    (Split-Path $cible -Leaf) + " (le geste du LISEZMOI-dudect)`r`n")
            }
        }
        $csv = Get-ChildItem -Path $kit2dir -Filter 'journal-dudect-*.csv' -ErrorAction SilentlyContinue |
               Sort-Object LastWriteTime | Select-Object -Last 1
        if ($csv) {
            Mark-Evenement ('journal-du-run : ' + $csv.Name)
            if ($script:TxtConsole) {
                $script:TxtConsole.AppendText('  le journal du run : ' + $csv.Name + "`r`n")
            }
        }
        $sortie = Join-Path $kit2dir 'sortie-run.txt'
        if ((Test-Path $sortie) -and $script:TxtConsole) {
            $script:TxtConsole.AppendText("--- les dernieres lignes du run (sortie-run.txt) ---`r`n")
            Get-Content $sortie -Tail 6 | ForEach-Object {
                $script:TxtConsole.AppendText('  ' + $_ + "`r`n")
            }
        }
    }
    $script:Proc = $null
    if (-not $TestMode -and $script:Timer) { $script:Timer.Interval = 1000 }
    if (-not $TestMode) {
        foreach ($b in $script:BoutonsRun) { $b.Enabled = $true }
        $script:LblStatut.Text = ('TERMINE : ' + $script:RunLabel + ' (code ' + $code + ')')
    }
    if ($script:File.Count -gt 0) {
        if ($code -eq 0) {
            $suivant = [int]$script:File[0]
            $script:File.RemoveAt(0)
            Demarrer-Run $suivant
        } elseif ($script:TxtConsole) {
            $script:TxtConsole.AppendText("  la BATTERIE S'ARRETE : code " + $code +
                " (fail-closed — l'ecart est nomme ci-dessus, D189)`r`n")
        }
    }
}

# ----------------------------------------------------------------------------
# L'INITIALISATION COMMUNE (GUI et TestMode)
# ----------------------------------------------------------------------------
function Init-Commun {
    $p = Get-CimInstance -ClassName Win32_Processor -ErrorAction SilentlyContinue |
         Select-Object -First 1
    if ($p) {
        $script:NomCpu = [string]$p.Name
        $script:BaseMHz = [double]$p.MaxClockSpeed
        $script:CoeursLogiques = [int]$p.NumberOfLogicalProcessors
    }
    $script:BatKit2 = Trouver-Bat 'LANCER-KIT-2-DUDECT.bat'
    $script:BatKit3 = Trouver-Bat 'LANCER-KIT-3-LOUPE.bat'
    $script:BatKit1 = Trouver-Bat 'LANCER-KIT-1-SHANI.bat'
    $nomCsv = 'journal-surveillant-' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '.csv'
    $script:JournalCsv = Join-Path $PSScriptRoot $nomCsv
    'horodatage,evenement,freq_MHz,charge_pct,temp_C,freq_par_coeur_MHz,charge_par_coeur_pct' |
        Out-File -FilePath $script:JournalCsv -Encoding UTF8
    if ($env:TEMP) {
        $script:FichierStdin = Join-Path $env:TEMP 'triade-stdin-vide.txt'
    } else {
        $script:FichierStdin = Join-Path $PSScriptRoot 'stdin-vide.txt'
    }
    Set-Content -Path $script:FichierStdin -Value ''
}

# ============================================================================
# LE MODE AUTOTEST (la logique sans GUI — eprouve au laboratoire)
# ============================================================================
if ($TestMode) {
    # la MOCKERIE honnete : Get-CimInstance rend un silicium simule dont la
    # frequence RAMPE (2500 -> 2380 -> 2140 : un throttle), puis remonte
    function Get-CimInstance {
        param($ClassName, $Namespace, $ErrorAction)
        switch ($ClassName) {
            'Win32_Processor' {
                return @([PSCustomObject]@{
                    Name = 'Intel(R) Test(TM) i7-SIMULE @ 2.00GHz (la mockerie du labo)'
                    MaxClockSpeed = 2501
                    NumberOfCores = 2
                    NumberOfLogicalProcessors = 4 })
            }
            'Win32_PerfFormattedData_Counters_ProcessorInformation' {
                $script:SimuTick++
                $ramp = @(2500, 2490, 2470, 2380, 2140, 2130, 2160, 2290,
                          2400, 2440, 2450, 2460)
                $f = $ramp[([math]::Min($script:SimuTick - 1, $ramp.Count - 1))]
                $ch = @(12, 14, 99, 100, 100, 100, 98, 60, 30, 20, 15, 13)[
                    ([math]::Min($script:SimuTick - 1, 11))]
                $lignes = @()
                for ($i = 0; $i -lt 4; $i++) {
                    $lignes += [PSCustomObject]@{
                        Name = ('0,' + $i)
                        ProcessorFrequency = ($f + 7 * $i)
                        PercentProcessorPerformance = (100 * ($f + 7 * $i) / 2501)
                        PercentProcessorTime = [math]::Min($ch + 5 * $i, 100) }
                }
                # v1.0.1 : la mockerie GAGNE l'instance vue au terrain et
                # absente de la mockerie v1.0.0 (l'ecart nomme) — l'agregat
                # par noeud, le faux coeur de la v1.0.0
                $lignes += [PSCustomObject]@{
                    Name = '0,_Total'
                    ProcessorFrequency = $f
                    PercentProcessorPerformance = (100 * $f / 2501)
                    PercentProcessorTime = $ch }
                $lignes += [PSCustomObject]@{
                    Name = '_Total'
                    ProcessorFrequency = $f
                    PercentProcessorPerformance = (100 * $f / 2501)
                    PercentProcessorTime = $ch }
                return $lignes
            }
            'MSAcpi_ThermalZoneTemperature' {
                $t = @(3335, 3338, 3342, 3350, 3358, 3361, 3363, 3359, 3352)
                return @([PSCustomObject]@{
                    CurrentTemperature = $t[([math]::Min($script:SimuTick - 1, 8))] })
            }
            default { return $null }
        }
    }
    $script:SimuTick = 0

    Write-Output '=== AUTOTEST SURVEILLANT-CPU — la logique sans GUI (le labo, v1.0.1) ==='
    $script:AgregatVuDansCoeurs = $false
    $script:OrdreCoeursFaux = $false
    Init-Commun
    Write-Output ('le silicium simule : ' + $script:NomCpu)
    Write-Output ('la base            : ' + (F0 $script:BaseMHz) + ' MHz')
    Write-Output ('le journal         : ' + $script:JournalCsv)
    if (-not $script:BatKit2) {
        Write-Output ('[ecart nomme] LANCER-KIT-2-DUDECT.bat introuvable depuis ce dossier — ' +
                     'normal au labo : le refus correspondant est MOQUE ci-dessous')
        $script:BatKit2 = 'C:\SIMULE\LANCER-KIT-2-DUDECT.bat'
    }

    for ($i = 0; $i -lt 12; $i++) {
        if ($i -eq 3) {
            # un run simule : DEBUT, echantillons, FIN code 0
            $script:RunLabel = 'N200'; $script:RunKit2 = $true
            Mark-Evenement 'DEBUT-RUN-N200'
        }
        if ($i -eq 7) { Mark-Evenement 'FIN-RUN-N200 code=0' }
        if ($i -eq 9) { Mark-Evenement 'MARQUE: observation manuelle du developpeur' }
        $e = Get-Echantillon
        $tmp = Get-Temperature
        # v1.0.1 : LE CONTROLE DU TERRAIN — aucun agregat ne vit parmi les
        # coeurs, et l'ordre est noeud puis coeur (le controle qui refusait
        # la v1.0.0 si la mockerie avait vecu l'instance 0,_Total)
        if ($e.Coeurs.Count -ne 4 -or
            @($e.Coeurs | Where-Object { $_.Nom -like '*_Total*' }).Count -gt 0) {
            $script:AgregatVuDansCoeurs = $true
        }
        for ($c = 0; $c -lt $e.Coeurs.Count; $c++) {
            if ($e.Coeurs[$c].Nom -ne ('0,' + $c)) { $script:OrdreCoeursFaux = $true }
        }
        Add-Ligne $e $tmp ''
        $script:SourceFreqVue = $e.SourceFreq
        $script:SourceTempVue = $tmp.Src
    }
    # un deuxieme run, refus fail-closed (code 2)
    $script:RunLabel = 'N400'; $script:RunKit2 = $true
    Mark-Evenement 'DEBUT-RUN-N400'
    Mark-Evenement 'FIN-RUN-N400 code=2'

    Write-Output ''
    Write-Output ('lignes journalisees : ' + $script:Lignes.Count)
    Write-Output ('fenetres de run     : ' + $script:Fenetres.Count)
    $chemin = Compose-Temoin 'AUTOTEST'
    Write-Output ('le temoin compose   : ' + $chemin)
    Write-Output ''
    Write-Output '--- le temoin (integral) ---'
    Get-Content $chemin | ForEach-Object { Write-Output $_ }
    Write-Output ''
    Write-Output '--- les 6 premieres lignes du csv ---'
    Get-Content $script:JournalCsv -TotalCount 6 | ForEach-Object { Write-Output $_ }
    if ($script:Lignes.Count -ne 17) {
        Write-Output ('[REFUS] AUTOTEST : attendu 17 lignes (12 echantillons + 5 lignes d evenement), vu ' +
                     $script:Lignes.Count)
        exit 2
    }
    if ($script:Fenetres.Count -ne 2) {
        Write-Output ('[REFUS] AUTOTEST : attendu 2 fenetres, vu ' + $script:Fenetres.Count)
        exit 2
    }
    if ($script:AgregatVuDansCoeurs) {
        Write-Output '[REFUS] AUTOTEST : un agregat _Total vit parmi les coeurs'
        Write-Output '  (le bug du terrain 25/11 — la ligne C4 fantome — corrige en v1.0.1)'
        exit 2
    }
    if ($script:OrdreCoeursFaux) {
        Write-Output "[REFUS] AUTOTEST : l'ordre des coeurs n'est pas noeud puis coeur"
        exit 2
    }
    Write-Output ''
    Write-Output '=== AUTOTEST VECU : la logique est eprouvee (17 lignes, 2 fenetres, le temoin et le csv composes ; aucun agregat parmi les coeurs — le controle du terrain) ==='
    exit 0
}
# ----------------------------------------------------------------------------
# LA GUI vit dans SA PIECE SEPAREE (surveillant-cpu-gui.ps1) — dot-sourcee
# ici : MEME portee script, memes fonctions, memes etats. La separation a une
# cause nommee : les types Drawing/WinForms n'ont PAS a charger pour
# l'autotest de la logique (-TestMode) — la piece GUI ne se compile que la
# ou elle vivra (Windows PowerShell 5.1, livre avec Windows 10 et 11).
. (Join-Path $PSScriptRoot 'surveillant-cpu-gui.ps1')
