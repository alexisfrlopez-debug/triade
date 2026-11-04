# TRIADE M5-b ETAPE 2 — LE FLUX NAVIGATEUR EN VM ISOLEE (reseau coupe) — e2.
#
# POURQUOI L'ETAPE 2 (faits consignes, pas des opinions) :
#   LE CRITERE (b) DE D136 : « un flux navigateur intercepte de bout en bout
#   dans la VM ; echec propre sur certificat invalide constate dans LE MEME
#   run ». L'etape 1 (runs v7/v8, verdicts OK 0 reserve) a prouve le tunnel
#   et l'autorite locale avec le CLIENT CLI forme-absolue ; AUCUN navigateur
#   n'a encore joue le run — c'est l'objet de CE scenario.
#   LE PROXY EST LE 0.6.0-rc.1 SCELLE (carte generation 7, 04/11) :
#   sha256 4b8f6af6caedb3e17811e6e25da1f1680068866bd1b417154fc54474170ec236,
#   36 352 octets. La ligne de commande NAÎT avec lui (http-12:R3) :
#   --relever-https arme le relèvement amont http->https (D136), TOUT autre
#   argument = refus nomme « TRIADE M5 : argument inconnu, arret » avant
#   toute initialisation ; l'armement est NOMME au journal (« relever-https
#   arme », une fois, entre la banniere et l'ecoute) ; la SESSION EMET LA
#   LIGNE DE FLUX (http-10:R3) : « flux GET 127.0.0.1:443 v=0 e=NN s=NN » —
#   le verdict de session (0 aboutie ; 3 = certificat rejete, transporte tel
#   quel de tls-08 ; 400..505 reponse nommee).
#   LE NAVIGATEUR DU BAC A SABLE (Edge, fourni avec l'image Windows) est
#   lance HEADLESS avec le mandataire EXPLICITE 127.0.0.1:25000 vers la page
#   http://127.0.0.1/ (IP LITTERALE — D139 : le fichier hosts est ignore par
#   la resolution dans la VM, l'IP litterale supprime TOUTE resolution
#   amont ; les fixtures v5 portent SAN IP Address:127.0.0.1). Le drapeau
#   --proxy-bypass-list="<-loopback>" RETIRE la derivee de boucle implicite
#   de Chromium (sinon 127.0.0.1 contournerait le mandataire) ;
#   --disable-features=HttpsUpgrades... DESACTIVE la montee https au
#   navigateur (l'upgrade parlerait CONNECT, que le protocole REJETE —
#   D136 ; meme en cas d'upgrade malgre tout, le repli http:// d'Edge
#   aboutit au meme chemin releve).
#   LA PREUVE COTE NAVIGATEUR (D99 — sur le disque, survit a la VM) : le
#   DOM RENDU par le navigateur (dump-dom : le marqueur de l'autorite en
#   run A, la page d'erreur « 502 » en run B) ET la CAPTURE d'ecran
#   (screenshot). Le rc du producteur fait foi (D138) ; les vues lues
#   depuis la VM restent des diagnostics, les pieces host sont juges au
#   laboratoire.
#
# Chaine : Edge headless (mandataire explicite 127.0.0.1:25000, page
# http://127.0.0.1/) -> proxy.exe 0.6.0-rc.1 scelle ARMÉ --relever-https ->
# RELEVEMENT amont vers https://127.0.0.1:443 -> tunnel TLS (Schannel,
# heritage M4) -> autorite locale (127.0.0.1:443).
# Run A : certificat VALIDE (racine installee) -> le NAVIGATEUR REND la page
#         (marqueur TRIADE-M5B-PAGE-200 au DOM) + ligne de flux v=0 +
#         « tunnel chiffre etabli ».
# Run B : certificat AUTO-SIGNE (autonome) -> le NAVIGATEUR RECOIT la 502
#         « Certificat rejete » (page d'erreur « 502 » au DOM, SANS le
#         marqueur) + ligne de flux v=3 + « certificat rejete » au journal
#         proxy + poignee refusee au journal autorite.
# LES DEUX RUNS DANS LE MEME scenario (le critere (b) l'exige).
#
# REFUS NOMMES (le scenario lui-meme est fail-closed) :
#   KIT-ABSENT | NAVIGATEUR-ABSENT | RACINE-NON-INSTALLEE | AUTORITE-MUETTE |
#   PROXY-MUET | PROXY-SANS-ARMEMENT | NAVIGATEUR-A-ECHEC | NAVIGATEUR-B-ECHEC |
#   DOM-A-INVALIDE | DOM-B-INVALIDE | DOM-B-PAGE-SERVIE | FLUX-A-MANQUANT |
#   FLUX-B-MANQUANT | AUTORITE-SORTIE-ANORMALE | PROXY-SORTIE-ANORMALE
# Code de sortie : 0 = verdict OK (ou OK-SOUS-RESERVE, reserves nommees au
# temoin) ; 1 = au moins un echec NOMME ; 2 = refus d'entree.
param(
  [string]$Kit = "C:\kit",
  [string]$Preuves = "C:\preuves",
  [string]$Hote = "autorite.test"
)

$JournalScenario = "$Preuves\scenario-m5b-journal.log"
$FichierTemoignage = "$Preuves\temoin-m5b.txt"
$Griffe = Join-Path $env:TEMP "m5b-griffe"
New-Item -ItemType Directory -Force -Path $Griffe | Out-Null
$JournalProxy = "$Preuves\proxy-journal.log"
$Origine = "127.0.0.1"          # D139 : l'IP litterale, le decisif n'a pas de nom a resoudre
$PageNav = "http://$Origine/"
$DelaiAutorite = 150            # secondes — arret propre par delai (le navigateur
                                # fait un nombre de requetes INCONNU : jamais
                                # --arret-apres N, un N trop bas couperait le run)
$Echecs = New-Object System.Collections.Generic.List[string]
$Reserves = New-Object System.Collections.Generic.List[string]
$Temoignages = New-Object System.Collections.Generic.List[string]

function Journal([string]$Message) {
  $Ligne = "[{0}] [scenario] {1}" -f (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ"), $Message
  [IO.File]::AppendAllText($JournalScenario, $Ligne + "`r`n")
  Write-Host $Ligne
}

function Verdict([string]$Nom, [bool]$Ok, [string]$Detail) {
  if ($Ok) {
    Journal ("PASS {0} — {1}" -f $Nom, $Detail)
  } else {
    Journal ("ECHEC {0} — {1}" -f $Nom, $Detail)
    $Echecs.Add("REFUS $Nom : $Detail") | Out-Null
  }
}

function Lire-Preuve([string[]]$Chemins) {
  # v4 lecture double : premiere vue non vide parmi les chemins (griffe
  # d'abord, montage ensuite). Retourne "" si toutes les vues sont vides.
  foreach ($F in $Chemins) {
    if (Test-Path $F) {
      $Octets = [IO.File]::ReadAllBytes($F)
      if ($Octets.Length -gt 0) {
        return [Text.Encoding]::UTF8.GetString($Octets)
      }
    }
  }
  return ""
}

function Verdict-Vue([string]$Nom, [string[]]$Chemins, [string]$Aiguille,
                     [string]$Detail, $RcProducteur) {
  # PASS si l'aiguille est vue ; ECHEC si du contenu SANS l'aiguille ;
  # RESERVE si vues vides MAIS producteur sorti code 0 (D138 : une vue
  # aveugle n'est pas un fait) ; ECHEC si vues vides ET producteur en echec.
  $Texte = Lire-Preuve $Chemins
  if ($Texte.Contains($Aiguille)) {
    Journal ("PASS {0} — {1}" -f $Nom, $Detail)
    return
  }
  if ($Texte.Length -gt 0) {
    Journal ("ECHEC {0} — contenu vu sans l'aiguille — {1}" -f $Nom, $Detail)
    $Echecs.Add("REFUS $Nom : $Detail") | Out-Null
    return
  }
  if ($RcProducteur -ne $null -and $RcProducteur -eq 0) {
    Journal ("RESERVE {0} — vues vides depuis la VM mais producteur rc=0 — piece a confirmer au labo" -f $Nom)
    $Reserves.Add("$Nom : vues vides depuis la VM, producteur rc=0 — juger la piece host au labo") | Out-Null
    return
  }
  Journal ("ECHEC {0} — vues vides et producteur rc=$RcProducteur — {1}" -f $Nom, $Detail)
  $Echecs.Add("REFUS $Nom : $Detail") | Out-Null
}

function Attendre-Port([int]$Port, [int]$Secondes) {
  # v4 : le signal de vie EST le fait — un connect TCP reussi sur
  # 127.0.0.1:$Port. Aucune lecture de fichier. La sonde connect+close
  # laisse une trace nommee chez l'ecouteur (signature de la sonde, cf. tete).
  $Borne = (Get-Date).AddSeconds($Secondes)
  while ((Get-Date) -lt $Borne) {
    $C = New-Object Net.Sockets.TcpClient
    try {
      $T = $C.BeginConnect("127.0.0.1", $Port, $null, $null)
      if ($T.AsyncWaitHandle.WaitOne(600) -and $C.Connected) {
        $C.EndConnect($T)
        $C.Close()
        return $true
      }
    } catch { }
    try { $C.Close() } catch { }
    Start-Sleep -Milliseconds 400
  }
  return $false
}

function Attendre-Ligne([string]$Fichier, [string]$Aiguille, [int]$Secondes) {
  # e2 : attente bornee d'UNE ligne dans un fichier journal (l'armement
  # « relever-https arme » est constate AVANT de lancer le navigateur —
  # fail-closed tot, pas apres le run).
  $Borne = (Get-Date).AddSeconds($Secondes)
  while ((Get-Date) -lt $Borne) {
    if ((Test-Path $Fichier) -and ([IO.File]::ReadAllText($Fichier) -match [regex]::Escape($Aiguille))) {
      return $true
    }
    Start-Sleep -Milliseconds 300
  }
  return $false
}

function Apercu([string]$Fichier) {
  if (-not (Test-Path $Fichier)) { return "ABSENT" }
  $Octets = [IO.File]::ReadAllBytes($Fichier)
  $N = [Math]::Min(200, $Octets.Length)
  $Texte = [Text.Encoding]::UTF8.GetString($Octets, 0, $N)
  return ("{0} o, debut : {1}" -f $Octets.Length, ($Texte -replace '[^\x20-\x7E]', '.'))
}

function Tuer($Proc, [string]$Nom) {
  try {
    if ($Proc -and -not $Proc.HasExited) { $Proc.Kill() ; Journal "processus $Nom tue (nettoyage de refus)" }
  } catch { }
}

function Copier-Preuve([string]$De, [string]$Vers) {
  try {
    Copy-Item -Force -Path $De -Destination $Vers
    Journal ("preuve copiee : " + (Split-Path $Vers -Leaf))
  } catch {
    Journal ("REFUS COPIE-PREUVE " + (Split-Path $Vers -Leaf) + " : " + $_.Exception.Message)
  }
}

function Empreinte([string]$Fichier) {
  $Sha = (Get-FileHash -Algorithm SHA256 -Path $Fichier).Hash.ToLower()
  $Md5 = "indisponible"
  foreach ($Ligne in (certutil -hashfile $Fichier MD5)) {
    $Compacte = $Ligne -replace '\s', ''
    if ($Compacte -match '^[0-9a-fA-F]{32}$') { $Md5 = $Compacte.ToLower(); break }
  }
  return "sha256 $Sha · md5 $Md5 · $((Get-Item $Fichier).Length) o — $Fichier"
}

$Diagnostics = New-Object System.Collections.Generic.List[string]

function Diagnostic([string]$Nom, [bool]$Ok, [string]$Detail) {
  # v6 : les diagnostics sont ADDITIFS — ils journalisent et temoignent,
  # mais n'entrent JAMAIS dans $Echecs ni $Reserves.
  $Sortie = $(if ($Ok) { "PASS" } else { "ECHEC" })
  Journal ("diagnostic {0} {1} — {2}" -f $Sortie, $Nom, $Detail)
  $Diagnostics.Add("$Nom : $Sortie — $Detail") | Out-Null
}

# ------------------------------------------------- 0bis. parefeu des l'ouverture (v8 — D142/D143)
# Decor verrouille par le run v8, REJOUE A L'IDENTIQUE : l'invite du parefeu
# est declenchee par la MISE EN ECOUTE (bind 0.0.0.0:25000 du proxy scelle),
# pas par un trafic ; la boucle locale 127.0.0.1 est EXEMPTE des regles (le
# navigateur, client pur sur boucle locale, ne demande AUCUNE regle).
foreach ($B in @("$Kit\proxy.exe", "$Kit\python\python.exe")) {
  if (Test-Path $B) {
    netsh advfirewall firewall delete rule name="TRIADE-M5B" program="$B" *> $null
    netsh advfirewall firewall add rule name="TRIADE-M5B" dir=in action=allow enable=yes profile=any program="$B" *> $null
    Diagnostic "DIAG-PAREFEU-REGLE" ($LASTEXITCODE -eq 0) ("regle ALLOW TRIADE-M5B posee pour $B — netsh rc=$LASTEXITCODE")
  }
}
netsh advfirewall set allprofiles settings inboundusernotification disable *> $null
Diagnostic "DIAG-PAREFEU-NOTIF" ($LASTEXITCODE -eq 0) ("inboundusernotification desactivee — plus aucune invite d'ecoute — netsh rc=$LASTEXITCODE")
$EtatParefeu = @(netsh advfirewall show allprofiles state 2>&1 | ForEach-Object { "$_" })
$EnteteParefeu = @(
  "TRIADE M5-b ETAPE 2 — ETAT PAREFEU DE LA VM (section 0bis, decor v8)",
  "machine : $env:COMPUTERNAME",
  "date : $((Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ'))",
  "D142 : l'invite = bind 0.0.0.0:25000, pas un trafic ; boucle locale exempte.",
  "regles posees : TRIADE-M5B (ALLOW, in) pour proxy.exe et python.exe du kit ;",
  "notification d'ecoute utilisateur (inboundusernotification) : DESACTIVEE.",
  ""
) + $EtatParefeu
[IO.File]::WriteAllText("$Preuves\parefeu-vm.txt", ($EnteteParefeu -join "`r`n") + "`r`n")
Diagnostic "DIAG-PAREFEU-ETAT" $true ("etat parefeu consigne — parefeu-vm.txt (" + (Get-Item "$Preuves\parefeu-vm.txt").Length + " o)")

# ---------------------------------------------------------------- 0. entree
Journal "demarrage — scenario M5-b ETAPE 2 (VM isolee, reseau coupe par .wsb) — machine $env:COMPUTERNAME — kit e2 labo (proxy 0.6.0-rc.1 scelle, carte generation 7 ; LE NAVIGATEUR du bac a sable juge — critere (b) de D136)"
$Requis = @(
  "$Kit\proxy.exe",
  "$Kit\autorite\autorite_test.py",
  "$Kit\autorite\fixtures\racine-autorite.pem",
  "$Kit\autorite\fixtures\serv-valide.pem",
  "$Kit\autorite\fixtures\serv-valide.key",
  "$Kit\autorite\fixtures\serv-autonome.pem",
  "$Kit\autorite\fixtures\serv-autonome.key",
  "$Kit\python\python.exe"
)
$Manquants = @($Requis | Where-Object { -not (Test-Path $_) })
if ($Manquants.Count -gt 0) {
  Journal ("REFUS KIT-ABSENT : {0}" -f ($Manquants -join " | "))
  exit 2
}
Journal ("kit complet — {0} fichiers requis presents" -f $Requis.Count)

# le navigateur du bac a sable : Edge, fourni avec l'image Windows. Le
# chemin est PROBE (x86 d'abord, la casse installee la plus courante, puis
# Program Files, puis la cle App Paths, puis le PATH) ; introuvable = refus
# NOMME d'entree (le critere (b) est un critere NAVIGATEUR : sans navigateur,
# le run ne dit rien).
$CheminEdge = $null
foreach ($Candidat in @(
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
    "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe")) {
  if ($Candidat -and (Test-Path $Candidat)) { $CheminEdge = $Candidat ; break }
}
if (-not $CheminEdge) {
  try {
    $Cle = Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe" -ErrorAction Stop
    if ($Cle.'(default)' -and (Test-Path $Cle.'(default)')) { $CheminEdge = $Cle.'(default)' }
  } catch { }
}
if (-not $CheminEdge) {
  $Trouve = Get-Command msedge.exe -ErrorAction SilentlyContinue
  if ($Trouve) { $CheminEdge = $Trouve.Source }
}
if (-not $CheminEdge) {
  Journal "REFUS NAVIGATEUR-ABSENT : msedge.exe introuvable (Program Files (x86), Program Files, App Paths, PATH) — le bac a sable est-il bien fourni d'Edge ?"
  exit 2
}
Journal "navigateur du bac a sable : $CheminEdge"

# la version du navigateur est une PIECE (comparabilite inter-machines,
# modele 17-H tampon OS) — diagnostique ADDITIF, jamais un verdict : si
# --version se tait, le run continue, le DOM dira.
$VersionEdge = ""
try {
  $PVer = Start-Process -FilePath $CheminEdge -ArgumentList @("--version") `
    -RedirectStandardOutput "$Griffe\edge-version.txt" `
    -RedirectStandardError "$Griffe\edge-version-err.txt" `
    -WindowStyle Hidden -PassThru
  if ($PVer.WaitForExit(30000)) {
    $VersionEdge = ([IO.File]::ReadAllText("$Griffe\edge-version.txt")).Trim()
  }
} catch { }
if ($VersionEdge.Length -gt 0) {
  Diagnostic "DIAG-EDGE-VERSION" $true ($VersionEdge + " — " + $CheminEdge)
} else {
  Diagnostic "DIAG-EDGE-VERSION" $false ("--version muet — piece edge-version.txt vide ou absente — le run continue")
}

# ---------------------------------------------------------------- 1. DNS + racine
$LigneHosts = "127.0.0.1 $Hote"
$FichierHosts = "$env:SystemRoot\System32\drivers\etc\hosts"
$ContenuHosts = [IO.File]::ReadAllText($FichierHosts)
if (-not ($ContenuHosts -match [regex]::Escape($LigneHosts))) {
  if ($ContenuHosts.Length -gt 0 -and -not $ContenuHosts.EndsWith("`n")) {
    [IO.File]::AppendAllText($FichierHosts, "`r`n")
  }
  [IO.File]::AppendAllText($FichierHosts, $LigneHosts + "`r`n")
}
Journal "hosts pose : $LigneHosts (DIAGNOSTIQUE D139 — le decisif de l'etape 2 vit sur l'IP litterale $Origine, aucune resolution n'y participe)"

# v5 : sonde de resolution — purement DIAGNOSTIQUE (D139 : le fichier hosts
# est relu present mais ignore par la resolution dans la VM ; le fait est
# consigne pour le journal des decisions).
try {
  $Resolues = [Net.Dns]::GetHostAddresses("autorite.test")
  Journal ("sonde resolution : autorite.test -> " + (($Resolues | ForEach-Object { $_.ToString() }) -join ", "))
} catch {
  Journal ("sonde resolution : autorite.test -> ECHEC " + $_.Exception.Message)
}

certutil -addstore -f Root "$Kit\autorite\fixtures\racine-autorite.pem" *> $null
Verdict "RACINE-INSTALLEE" ($LASTEXITCODE -eq 0) ("certutil -addstore Root — code $LASTEXITCODE")

# ---------------------------------------------------------------- 2. empreintes
foreach ($F in @("$Kit\proxy.exe", "$Kit\autorite\fixtures\racine-autorite.pem",
                 "$Kit\autorite\fixtures\serv-valide.pem",
                 "$Kit\autorite\fixtures\serv-autonome.pem")) {
  $E = Empreinte $F
  Journal "empreinte : $E"
  $Temoignages.Add($E) | Out-Null
}
if ($VersionEdge.Length -gt 0) { $Temoignages.Add("navigateur : $VersionEdge") | Out-Null }

# ---------------------------------------------------------------- 3. RUN A (valide)
Journal "RUN A — mode VALIDE (certificat signe par la racine installee) — le NAVIGATEUR rend la page"
$T0AutoriteA = [DateTime]::UtcNow
$ProcA = Start-Process -FilePath "$Kit\python\python.exe" `
  -ArgumentList @("$Kit\autorite\autorite_test.py", "--mode", "valide",
                  "--port", "443", "--journal", "$Griffe\autorite-a.log",
                  "--arret-apres-secondes", "$DelaiAutorite") `
  -RedirectStandardOutput "$Preuves\autorite-a-console.log" `
  -RedirectStandardError "$Preuves\autorite-a-err.log" `
  -WindowStyle Hidden -PassThru
if (-not (Attendre-Port 443 60)) {
  Journal ("REFUS AUTORITE-MUETTE : port 443 jamais ouvert en 60 s — journal : " + (Apercu "$Griffe\autorite-a.log") + " — console : " + (Apercu "$Preuves\autorite-a-console.log") + " — err : " + (Apercu "$Preuves\autorite-a-err.log"))
  Tuer $ProcA "autorite-a"
  exit 2
}
Journal "autorite A en ecoute — sonde : connect 127.0.0.1:443 reussi"

# le proxy : cmd /c relaye son stdin et capture sa console NATIVEMENT vers
# C:\preuves (chemin d'ecriture prouve) — MEME capture que terrain.17, avec
# le drapeau --relever-https ARMANT la politique (http-12:R3 : le drapeau
# est exact, casse sensible ; tout autre argument tuerait le processus
# avant toute ecoute — le scenario ne lui en donne AUCUN autre).
$Psi = New-Object System.Diagnostics.ProcessStartInfo
$Psi.FileName = $env:ComSpec
$Psi.Arguments = '/c ""' + $Kit + '\proxy.exe" --relever-https > "' + $JournalProxy + '" 2>&1"'
$Psi.WorkingDirectory = $Preuves
$Psi.UseShellExecute = $false
$Psi.CreateNoWindow = $true
$Psi.RedirectStandardInput = $true
$Proxy = [System.Diagnostics.Process]::Start($Psi)
if (-not (Attendre-Port 25000 90)) {
  Journal ("REFUS PROXY-MUET : port 25000 jamais ouvert en 90 s — journal proxy : " + (Apercu $JournalProxy))
  try { $Proxy.StandardInput.WriteLine("quit") } catch { }
  Start-Sleep -Seconds 2
  Tuer $Proxy "proxy"
  exit 2
}
Journal "proxy demarre — sonde : connect 127.0.0.1:25000 reussi"

# L'ARMEMENT EST CONSTATE AVANT LE NAVIGATEUR (fail-closed tot) : la ligne
# « relever-https arme » est emise UNE fois entre la banniere et l'ecoute
# (http-12:R3, Q3/I2). Sans elle, le proxy tournerait en 0.5.1 MUET sur le
# relèvement — le navigateur recevrait une erreur, le run ne prouverait rien.
if (-not (Attendre-Ligne $JournalProxy "relever-https arme" 20)) {
  Journal ("REFUS PROXY-SANS-ARMEMENT : aucune ligne « relever-https arme » au journal proxy en 20 s — journal : " + (Apercu $JournalProxy))
  try { $Proxy.StandardInput.WriteLine("quit") } catch { }
  Start-Sleep -Seconds 2
  Tuer $Proxy "proxy"
  exit 2
}
Journal "armement constate : ligne « relever-https arme » au journal proxy — le relèvement http->https est EN SERVICE"

# --- le navigateur, run A : LE DOM ---------------------------------------------
# Edge headless charge la page PAR LE MANDATAIRE ; le DOM SERIALISE (dump-
# dom) est la piece : le marqueur TRIADE-M5B-PAGE-200 n'y vit que si le
# NAVIGATEUR l'a RECU ET PARSE (la page vient du tunnel, il n'existe AUCUN
# autre chemin vers l'autorite). <-loopback> retire la derivee de boucle
# implicite de Chromium ; HttpsUpgrades et ses freres sont DESACTIVES.
$ProfilDomA = Join-Path $Griffe "edge-dom-a"
$ArgsDomA = @(
  "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
  "--disable-sync", "--disable-extensions", "--disable-background-networking",
  "--disable-component-update", "--window-size=1280,800",
  ('--user-data-dir="' + $ProfilDomA + '"'),
  "--proxy-server=127.0.0.1:25000",
  '--proxy-bypass-list="<-loopback>"',
  "--disable-features=HttpsUpgrades,HttpsFirstBalancedModeAutoEnable,HttpsFirstModeEnabled",
  "--dump-dom", $PageNav
)
$NavA = Start-Process -FilePath $CheminEdge -ArgumentList $ArgsDomA `
  -RedirectStandardOutput "$Preuves\dom-a.txt" `
  -RedirectStandardError "$Preuves\nav-a-err.txt" `
  -WindowStyle Hidden -PassThru
if (-not $NavA.WaitForExit(100000)) {
  Tuer $NavA "edge-dom-a"
  Journal "REFUS NAVIGATEUR-A-ECHEC : Edge (dump-dom) n'a pas rendu la main en 100 s — tue"
  Verdict "NAVIGATEUR-A" $false "Edge headless dump-dom hors delai (100 s)"
} else {
  Verdict "NAVIGATEUR-A" ($NavA.ExitCode -eq 0) ("Edge headless dump-dom — code de sortie $($NavA.ExitCode)")
}
$RcNavA = $null
if ($NavA.HasExited) { $RcNavA = $NavA.ExitCode }
Journal ("DOM A vu : " + (Apercu "$Preuves\dom-a.txt") + " — err : " + (Apercu "$Preuves\nav-a-err.txt"))

# --- le navigateur, run A : LA CAPTURE -----------------------------------------
# Deuxieme invocation (profil NEUF, aucune memoire entre les deux) : la
# capture d'ecran est la piece LISIBLE par l'oeil — diagnostique ADDITIF
# (le DOM est le decisive navigateur ; une capture manquee ne siffle pas
# le run, elle est nommee et jointe si presente).
$ProfilCapA = Join-Path $Griffe "edge-cap-a"
$ArgsCapA = @(
  "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
  "--disable-sync", "--disable-extensions", "--disable-background-networking",
  "--disable-component-update", "--window-size=1280,800",
  ('--user-data-dir="' + $ProfilCapA + '"'),
  "--proxy-server=127.0.0.1:25000",
  '--proxy-bypass-list="<-loopback>"',
  "--disable-features=HttpsUpgrades,HttpsFirstBalancedModeAutoEnable,HttpsFirstModeEnabled",
  ('--screenshot="' + "$Preuves\nav-a.png" + '"'),
  $PageNav
)
$CapA = Start-Process -FilePath $CheminEdge -ArgumentList $ArgsCapA `
  -RedirectStandardOutput "$Griffe\cap-a-console.txt" `
  -RedirectStandardError "$Preuves\nav-a-cap-err.txt" `
  -WindowStyle Hidden -PassThru
if (-not $CapA.WaitForExit(80000)) {
  Tuer $CapA "edge-cap-a"
  Diagnostic "DIAG-CAPTURE-A" $false "Edge (screenshot) hors delai (80 s) — tue — la capture nav-a.png n'a pas ete produite"
} else {
  $CaptureOkA = ((Test-Path "$Preuves\nav-a.png") -and ((Get-Item "$Preuves\nav-a.png").Length -gt 0))
  Diagnostic "DIAG-CAPTURE-A" $CaptureOkA ("Edge headless screenshot — rc=$($CapA.ExitCode) — nav-a.png " + $(if ($CaptureOkA) { (Get-Item "$Preuves\nav-a.png").Length.ToString() + " o" } else { "ABSENTE" }))
}

# --- les pieces du run A --------------------------------------------------------
Verdict-Vue "DOM-A-MARQUEUR" @("$Preuves\dom-a.txt") "TRIADE-M5B-PAGE-200" ("le NAVIGATEUR a rendu la page de l'autorite (marqueur au DOM serialize) — page $PageNav par le mandataire") $RcNavA
Verdict-Vue "AUTORITE-A-SERVIE" @("$Griffe\autorite-a.log", "$Preuves\autorite-a.log", "$Preuves\autorite-a-console.log") "requete servie" "ligne « requete servie » au journal autorite (le navigateur peut faire PLUSIEURS requetes : page, favicon — toutes servies par le tunnel)" $RcNavA

# l'autorite s'arrete ELLE-MEME par delai (le compte de requetes du
# navigateur est inconnu — jamais --arret-apres N) ; attente du RESTANT du
# delai + 20 s de marge, bornee.
$EcouleA = ([DateTime]::UtcNow - $T0AutoriteA).TotalSeconds
$ResteA = [int]($DelaiAutorite - $EcouleA) + 20
if ($ResteA -lt 10) { $ResteA = 10 }
if (-not $ProcA.WaitForExit($ResteA * 1000)) { $ProcA.Kill() }
Verdict-Vue "AUTORITE-A-ARRET" @("$Griffe\autorite-a.log") "arret propre" ("ligne « arret propre » au journal autorite — instrument : ligne (D138 : capture rc aveugle, recu $($ProcA.ExitCode))") $ProcA.ExitCode
if (Test-Path "$Preuves\dom-a.txt") {
  $Temoignages.Add("RUN A : dom-a.txt " + (Empreinte "$Preuves\dom-a.txt")) | Out-Null
}
if (Test-Path "$Preuves\nav-a.png") {
  $Temoignages.Add("RUN A : nav-a.png " + (Empreinte "$Preuves\nav-a.png")) | Out-Null
}
Copier-Preuve "$Griffe\autorite-a.log" "$Preuves\autorite-a.log"

# ---------------------------------------------------------------- 4. RUN B (autonome)
Journal "RUN B — mode AUTONOME (certificat auto-signe, la mauvaise heresie de terrain.17) — le NAVIGATEUR recoit la 502"
$T0AutoriteB = [DateTime]::UtcNow
$ProcB = Start-Process -FilePath "$Kit\python\python.exe" `
  -ArgumentList @("$Kit\autorite\autorite_test.py", "--mode", "autonome",
                  "--port", "443", "--journal", "$Griffe\autorite-b.log",
                  "--arret-apres-secondes", "$DelaiAutorite") `
  -RedirectStandardOutput "$Preuves\autorite-b-console.log" `
  -RedirectStandardError "$Preuves\autorite-b-err.log" `
  -WindowStyle Hidden -PassThru
if (-not (Attendre-Port 443 60)) {
  Journal ("REFUS AUTORITE-MUETTE (run B) : port 443 jamais ouvert en 60 s — journal : " + (Apercu "$Griffe\autorite-b.log") + " — console : " + (Apercu "$Preuves\autorite-b-console.log") + " — err : " + (Apercu "$Preuves\autorite-b-err.log"))
  Tuer $ProcB "autorite-b"
  exit 2
}
Journal "autorite B en ecoute — sonde : connect 127.0.0.1:443 reussi"

# --- le navigateur, run B : LE DOM ---------------------------------------------
# MEME invocation que le run A (profil neuf) : la cible relevee presente un
# certificat AUTO-SIGNE ; le proxy scelle refuse la poignee (verdict tls-08
# = 3) et repond AU NAVIGATEUR la 502 heritee « HTTP/1.1 502 Certificat
# rejete » (34 octets, sans corps) — Edge rend SA page d'erreur : le DOM
# serialize porte le code (« HTTP ERROR 502 ») ; l'aiguille est « 502 »,
# aucun locale n'ecrit le chiffre autrement.
$ProfilDomB = Join-Path $Griffe "edge-dom-b"
$ArgsDomB = @(
  "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
  "--disable-sync", "--disable-extensions", "--disable-background-networking",
  "--disable-component-update", "--window-size=1280,800",
  ('--user-data-dir="' + $ProfilDomB + '"'),
  "--proxy-server=127.0.0.1:25000",
  '--proxy-bypass-list="<-loopback>"',
  "--disable-features=HttpsUpgrades,HttpsFirstBalancedModeAutoEnable,HttpsFirstModeEnabled",
  "--dump-dom", $PageNav
)
$NavB = Start-Process -FilePath $CheminEdge -ArgumentList $ArgsDomB `
  -RedirectStandardOutput "$Preuves\dom-b.txt" `
  -RedirectStandardError "$Preuves\nav-b-err.txt" `
  -WindowStyle Hidden -PassThru
if (-not $NavB.WaitForExit(100000)) {
  Tuer $NavB "edge-dom-b"
  Journal "REFUS NAVIGATEUR-B-ECHEC : Edge (dump-dom) n'a pas rendu la main en 100 s — tue"
  Verdict "NAVIGATEUR-B" $false "Edge headless dump-dom hors delai (100 s)"
} else {
  Verdict "NAVIGATEUR-B" ($NavB.ExitCode -eq 0) ("Edge headless dump-dom — code de sortie $($NavB.ExitCode)")
}
$RcNavB = $null
if ($NavB.HasExited) { $RcNavB = $NavB.ExitCode }
Journal ("DOM B vu : " + (Apercu "$Preuves\dom-b.txt") + " — err : " + (Apercu "$Preuves\nav-b-err.txt"))

# --- le navigateur, run B : LA CAPTURE -----------------------------------------
$ProfilCapB = Join-Path $Griffe "edge-cap-b"
$ArgsCapB = @(
  "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
  "--disable-sync", "--disable-extensions", "--disable-background-networking",
  "--disable-component-update", "--window-size=1280,800",
  ('--user-data-dir="' + $ProfilCapB + '"'),
  "--proxy-server=127.0.0.1:25000",
  '--proxy-bypass-list="<-loopback>"',
  "--disable-features=HttpsUpgrades,HttpsFirstBalancedModeAutoEnable,HttpsFirstModeEnabled",
  ('--screenshot="' + "$Preuves\nav-b.png" + '"'),
  $PageNav
)
$CapB = Start-Process -FilePath $CheminEdge -ArgumentList $ArgsCapB `
  -RedirectStandardOutput "$Griffe\cap-b-console.txt" `
  -RedirectStandardError "$Preuves\nav-b-cap-err.txt" `
  -WindowStyle Hidden -PassThru
if (-not $CapB.WaitForExit(80000)) {
  Tuer $CapB "edge-cap-b"
  Diagnostic "DIAG-CAPTURE-B" $false "Edge (screenshot) hors delai (80 s) — tue — la capture nav-b.png n'a pas ete produite"
} else {
  $CaptureOkB = ((Test-Path "$Preuves\nav-b.png") -and ((Get-Item "$Preuves\nav-b.png").Length -gt 0))
  Diagnostic "DIAG-CAPTURE-B" $CaptureOkB ("Edge headless screenshot — rc=$($CapB.ExitCode) — nav-b.png " + $(if ($CaptureOkB) { (Get-Item "$Preuves\nav-b.png").Length.ToString() + " o" } else { "ABSENTE" }))
}

# --- les pieces du run B --------------------------------------------------------
# DOM-B-502 : le navigateur a RECU la 502 (page d'erreur d'Edge portant le
# code). DOM-B-SANS-PAGE : la page de l'autorite N'A PAS ete servie en
# run B (le marqueur serait une contre-preuve — l'autorite autonome ne sert
# RIEN, sa poignee est refusee AVANT tout octet HTTP).
$TexteDomB = Lire-Preuve @("$Preuves\dom-b.txt")
if ($TexteDomB.Length -gt 0) {
  $ExtraitB = ($TexteDomB -replace '[^\x20-\x7E]', '.')
  $PlageB = $ExtraitB.IndexOf("502")
  $FragmentB = ""
  if ($PlageB -ge 0) {
    $DebutB = [Math]::Max(0, $PlageB - 60)
    $LongB = [Math]::Min(140, $ExtraitB.Length - $DebutB)
    $FragmentB = $ExtraitB.Substring($DebutB, $LongB)
  }
  Verdict "DOM-B-502" ($TexteDomB.Contains("502")) ("le NAVIGATEUR a rendu sa page d'erreur — extrait autour du code : « $FragmentB »")
  Verdict "DOM-B-SANS-PAGE" (-not $TexteDomB.Contains("TRIADE-M5B-PAGE-200")) ("le marqueur de la page servie est ABSENT du DOM du run B (attendu : l'autorite autonome ne sert rien)")
} else {
  if ($RcNavB -ne $null -and $RcNavB -eq 0) {
    Journal "RESERVE DOM-B — vues vides depuis la VM mais Edge rc=0 — piece a confirmer au labo"
    $Reserves.Add("DOM-B-502/DOM-B-SANS-PAGE : vues vides depuis la VM, Edge rc=0 — juger C:\preuves\dom-b.txt au labo") | Out-Null
  } else {
    Verdict "DOM-B-INVALIDE" $false "DOM du run B illisible et navigateur en echec"
  }
}
Verdict-Vue "POIGNEE-B-REFUSEE" @("$Griffe\autorite-b.log", "$Preuves\autorite-b.log", "$Preuves\autorite-b-console.log") "poignee de main refusee" "poignee refusee NOMMEE au journal autorite" $RcNavB

$EcouleB = ([DateTime]::UtcNow - $T0AutoriteB).TotalSeconds
$ResteB = [int]($DelaiAutorite - $EcouleB) + 20
if ($ResteB -lt 10) { $ResteB = 10 }
if (-not $ProcB.WaitForExit($ResteB * 1000)) { $ProcB.Kill() }
Verdict-Vue "AUTORITE-B-ARRET" @("$Griffe\autorite-b.log") "arret propre" ("ligne « arret propre » au journal autorite — instrument : ligne (D138 : capture rc aveugle, recu $($ProcB.ExitCode))") $ProcB.ExitCode
if (Test-Path "$Preuves\dom-b.txt") {
  $Temoignages.Add("RUN B : dom-b.txt " + (Empreinte "$Preuves\dom-b.txt")) | Out-Null
}
if (Test-Path "$Preuves\nav-b.png") {
  $Temoignages.Add("RUN B : nav-b.png " + (Empreinte "$Preuves\nav-b.png")) | Out-Null
}
Copier-Preuve "$Griffe\autorite-b.log" "$Preuves\autorite-b.log"

# ---------------------------------------------------------------- 5. arret du proxy + journal
try {
  $Proxy.StandardInput.WriteLine("quit")
} catch {
  Journal ("stdin du proxy deja ferme — " + $_.Exception.GetType().Name)
}
if (-not $Proxy.WaitForExit(30000)) { $Proxy.Kill() }
Verdict "PROXY-ARRET" ($Proxy.ExitCode -eq 0) ("quit console — code de sortie $($Proxy.ExitCode) (S47, lecon D99)")
$RcProxy = $Proxy.ExitCode
Verdict-Vue "PROXY-BANNIERE" @($JournalProxy) "demarre" "ligne « demarre » au journal proxy" $RcProxy
Verdict-Vue "RELEVER-ARME" @($JournalProxy) "relever-https arme" "ligne « relever-https arme » au journal proxy (l'armement du relèvement, http-12:R3 — deja constatee avant le navigateur)" $RcProxy
Verdict-Vue "TUNNEL-A" @($JournalProxy) "tunnel chiffre etabli" "ligne « tunnel chiffre etabli » au journal proxy (run A)" $RcProxy
Verdict-Vue "FLUX-A-V0" @($JournalProxy) "flux GET 127.0.0.1:443 v=0" "ligne de flux du run A (http-10:R3 : « flux GET 127.0.0.1:443 v=0 e=NN s=NN » — cible relevée, verdict 0 aboutie)" $RcProxy
Verdict-Vue "CERTIFICAT-REJETE" @($JournalProxy) "certificat rejete" "ligne « certificat rejete » au journal proxy (run B — LE critere)" $RcProxy
Verdict-Vue "FLUX-B-V3" @($JournalProxy) "flux GET 127.0.0.1:443 v=3" "ligne de flux du run B (verdict 3 = certificat rejete, TRANSPORTE tel quel de tls-08 — la ligne nomme la CAUSE, la 502 nomme l'effet)" $RcProxy
Verdict-Vue "PROXY-ARRET-CONSOLE" @($JournalProxy) "arret" "ligne finale « arret » au journal proxy" $RcProxy

# ------------------------------------------------ 5bis. DIAGNOSTICS (matrice curl heritee v8 + T6)
# Matrice curl.exe (Schannel de Windows — temoin independant du proxy ET du
# navigateur), ports dedies 4443/4444 : 443 reste aux runs A/B. Controle de
# stabilite ADDITIF (lecon v6 : rien n'entre dans $Echecs ni $Reserves) ;
# attendus inchanges depuis v7/v8 : T2a/T3 rc=60 (revocation), T2b rc=0,
# T5 rejet autonome.
$Branche = "NON JOUEE — curl.exe absent ou autorites de diagnostic muettes"
$CurlExe = "$env:SystemRoot\System32\curl.exe"
if (-not (Test-Path $CurlExe)) {
  $Trouve = Get-Command curl.exe -ErrorAction SilentlyContinue
  if ($Trouve) { $CurlExe = $Trouve.Source }
}
if (-not (Test-Path $CurlExe)) {
  Journal "diagnostic IMPOSSIBLE — curl.exe introuvable — matrice non jouable ce run (fait nomme)"
} else {
  $VersionCurl = (& $CurlExe --version | Select-Object -First 1)
  Diagnostic "DIAG-CURL-PRESENT" $true ("$CurlExe — $VersionCurl")

  # T1 — le fait hosts (D139) : le fichier pose est-il relu, et la
  # resolution marche-t-elle apres purge du cache DNS ?
  $HostsRelu = [IO.File]::ReadAllText($FichierHosts)
  $PoseEtLu = $HostsRelu -match [regex]::Escape($LigneHosts)
  [IO.File]::WriteAllText("$Preuves\hosts-lu.txt", $HostsRelu)
  Diagnostic "DIAG-HOSTS-POSE-ET-LU" $PoseEtLu ("relecture de $FichierHosts — ligne presente : " + $(if ($PoseEtLu) { "oui" } else { "NON" }))
  ipconfig /flushdns *> $null
  try {
    $ApresFlush = [Net.Dns]::GetHostAddresses("autorite.test")
    Diagnostic "DIAG-HOSTS-RESOLU" $true ("apres flushdns : " + (($ApresFlush | ForEach-Object { $_.ToString() }) -join ", "))
  } catch {
    Diagnostic "DIAG-HOSTS-IGNORE" $false ("apres flushdns : " + $_.Exception.Message)
  }

  # T6 — mecanisme D139 : la consultation de hosts appartient au service
  # Client DNS (Dnscache). Mesure PUREMENT diagnostique (hors verdict).
  $SvcDns = Get-Service Dnscache -ErrorAction SilentlyContinue
  if ($SvcDns) {
    Diagnostic "DIAG-DNSCACHE-ETAT" $true ("service Dnscache : Status=" + $SvcDns.Status + " StartType=" + $SvcDns.StartType)
  } else {
    Diagnostic "DIAG-DNSCACHE-ETAT" $false "service Dnscache INTROUVABLE (Get-Service Dnscache vide) — mecanisme D139 nomme : hosts n'est consulte par personne"
  }
  sc.exe query dnscache > "$Preuves\dnscache.txt" 2>&1
  ipconfig /all > "$Preuves\ipconfig-vm.txt" 2>&1
  Journal ("diagnostic T6 : dnscache.txt " + (Get-Item "$Preuves\dnscache.txt").Length + " o — ipconfig-vm.txt " + (Get-Item "$Preuves\ipconfig-vm.txt").Length + " o")

  # T2a/T2b/T3 — Schannel face a l'autorite python, SANS le proxy.
  $Racine = "$Kit\autorite\fixtures\racine-autorite.pem"
  $ProcD = Start-Process -FilePath "$Kit\python\python.exe" `
    -ArgumentList @("$Kit\autorite\autorite_test.py", "--mode", "valide",
                    "--port", "4443", "--journal", "$Griffe\autorite-d.log",
                    "--arret-apres-secondes", "90") `
    -RedirectStandardOutput "$Preuves\autorite-d-console.log" `
    -RedirectStandardError "$Preuves\autorite-d-err.log" `
    -WindowStyle Hidden -PassThru
  if (-not (Attendre-Port 4443 60)) {
    Diagnostic "DIAG-AUTORITE-D-MUETTE" $false ("port 4443 jamais ouvert en 60 s — console : " + (Apercu "$Preuves\autorite-d-console.log") + " — err : " + (Apercu "$Preuves\autorite-d-err.log"))
    Tuer $ProcD "autorite-d"
  } else {
    Journal "diagnostic : autorite D (valide) en ecoute sur 4443"
    $T2a = Start-Process -FilePath $CurlExe `
      -ArgumentList @("-sS", "-v", "--cacert", $Racine, "--max-time", "12",
                      "https://127.0.0.1:4443/") `
      -RedirectStandardOutput "$Preuves\page-d2a.txt" `
      -RedirectStandardError "$Preuves\curl-d2a.txt" `
      -WindowStyle Hidden -Wait -PassThru
    $PageD2a = Lire-Preuve @("$Preuves\page-d2a.txt")
    $Ok2a = ($T2a.ExitCode -eq 0)   # v7 : rc du producteur fait foi (D138)
    Diagnostic "DIAG-CURL-IP-STRICT" $Ok2a ("curl direct (Schannel) par l'IP litterale — rc=$($T2a.ExitCode) — premiere ligne : « " + (($PageD2a -split "`r`n")[0]) + " » — details : " + (Apercu "$Preuves\curl-d2a.txt"))

    $T2b = Start-Process -FilePath $CurlExe `
      -ArgumentList @("-sS", "-v", "--ssl-no-revoke", "--cacert", $Racine,
                      "--max-time", "12", "https://127.0.0.1:4443/") `
      -RedirectStandardOutput "$Preuves\page-d2b.txt" `
      -RedirectStandardError "$Preuves\curl-d2b.txt" `
      -WindowStyle Hidden -Wait -PassThru
    $TexteD2b = Lire-Preuve @("$Preuves\curl-d2b.txt")
    if ($TexteD2b -match "unknown option") {
      Diagnostic "DIAG-CURL-SANS-REVOCATION-IMPOSSIBLE" $false "curl.exe refuse --ssl-no-revoke (backend non Schannel ?) — la branche S3 n'est pas testable ce run"
    } else {
      $PageD2b = Lire-Preuve @("$Preuves\page-d2b.txt")
      $Ok2b = ($T2b.ExitCode -eq 0)   # v7 : rc fait foi (D138)
      Diagnostic "DIAG-CURL-IP-SANS-REVOCATION" $Ok2b ("curl direct + --ssl-no-revoke par l'IP litterale — rc=$($T2b.ExitCode) — details : " + (Apercu "$Preuves\curl-d2b.txt"))
    }

    $T3 = Start-Process -FilePath $CurlExe `
      -ArgumentList @("-sS", "-v", "--cacert", $Racine, "--resolve",
                      "autorite.test:4443:127.0.0.1", "--max-time", "12",
                      "https://autorite.test:4443/") `
      -RedirectStandardOutput "$Preuves\page-d3.txt" `
      -RedirectStandardError "$Preuves\curl-d3.txt" `
      -WindowStyle Hidden -Wait -PassThru
    $PageD3 = Lire-Preuve @("$Preuves\page-d3.txt")
    $Ok3 = ($T3.ExitCode -eq 0)   # v7 : rc fait foi (D138)
    Diagnostic "DIAG-CURL-NOM-RESOLVE" $Ok3 ("curl direct par le NOM (sans hosts) — rc=$($T3.ExitCode) — premiere ligne : « " + (($PageD3 -split "`r`n")[0]) + " »")

    if (-not $ProcD.WaitForExit(5000)) {
      $ProcD.Kill()
      Journal "diagnostic : autorite D tuee apres usage (nettoyage)"
    }
    Copier-Preuve "$Griffe\autorite-d.log" "$Preuves\autorite-d.log"
  }

  # T5 — controle negatif : face au certificat AUTONOME, Schannel doit
  # rejeter. Si ce juge-la ne rejette pas, la matrice ne vaut rien.
  $ProcE = Start-Process -FilePath "$Kit\python\python.exe" `
    -ArgumentList @("$Kit\autorite\autorite_test.py", "--mode", "autonome",
                    "--port", "4444", "--journal", "$Griffe\autorite-e.log",
                    "--arret-apres-secondes", "20") `
    -RedirectStandardOutput "$Preuves\autorite-e-console.log" `
    -RedirectStandardError "$Preuves\autorite-e-err.log" `
    -WindowStyle Hidden -PassThru
  # (la branche nommee ci-dessous est calculee APRES T5, comme en v8)
  if (-not (Attendre-Port 4444 60)) {
    Diagnostic "DIAG-AUTORITE-E-MUETTE" $false ("port 4444 jamais ouvert en 60 s — console : " + (Apercu "$Preuves\autorite-e-console.log") + " — err : " + (Apercu "$Preuves\autorite-e-err.log"))
    Tuer $ProcE "autorite-e"
  } else {
    Journal "diagnostic : autorite E (autonome) en ecoute sur 4444"
    $T5 = Start-Process -FilePath $CurlExe `
      -ArgumentList @("-sS", "-v", "--cacert", $Racine, "--max-time", "12",
                      "https://127.0.0.1:4444/") `
      -RedirectStandardOutput "$Preuves\page-d5.txt" `
      -RedirectStandardError "$Preuves\curl-d5.txt" `
      -WindowStyle Hidden -Wait -PassThru
    Diagnostic "DIAG-CURL-REJET-HERESIE" ($T5.ExitCode -ne 0) ("curl direct face au certificat AUTO-SIGNE — rc=$($T5.ExitCode) (rejet attendu) — details : " + (Apercu "$Preuves\curl-d5.txt"))
    if (-not $ProcE.WaitForExit(25000)) { $ProcE.Kill() }
    Copier-Preuve "$Griffe\autorite-e.log" "$Preuves\autorite-e.log"
  }

  # La branche nommee (cf. table de la v8) — UNE action suivante par branche ;
  # 0.5.1 ayant RENTRE le jalon (runs v7/v8), la branche attendue est S4.
  $Ok2aVue = ($Ok2a -eq $true)
  $Ok2bVue = ($Ok2b -eq $true)   # rc du producteur, pas la vue aveugle (D138)
  if ($Ok2aVue) {
    $Branche = "S4 — le Schannel de la VM valide lui-meme la chaine (IP litterale comprise) : attendu depuis 0.5.1 (runs v7/v8) — si le run navigateur echoue, le coupable est ailleurs (navigateur ou proxy rc.1), pas Schannel"
  } elseif ($Ok2bVue) {
    $Branche = "S3 — revocation hors ligne : la validation echoue faute de CRL joignable — D140 dit RESOLU depuis 0.5.1 : REGRESSION a nommer"
  } elseif ($Ok3 -eq $true) {
    $Branche = "S1 — le nom cible IP-litterale casse la poignee (pszTargetName) — inattendu depuis les runs v7/v8 : a juger sur pieces"
  } else {
    $Branche = "S2 — Schannel ne valide pas la chaine/racine dans la VM : verifier l'installation de la racine (certutil -verify, magasin)"
  }
  Journal ("diagnostic branche nommee : " + $Branche)
}

# ---------------------------------------------------------------- 6. temoin (D99)
$Entete = @(
  "TRIADE M5-b ETAPE 2 — TEMOIN SUR LE DISQUE (lecon D99)",
  "machine : $env:COMPUTERNAME (VM isolee — ce fichier SURVIT a la destruction de la VM)",
  "os : $([Environment]::OSVersion.VersionString) (build $([Environment]::OSVersion.Version.Build))",
  "date : $((Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ'))",
  "LE CRITERE (b) DE D136 — le flux NAVIGATEUR intercepte de bout en bout :",
  "  page chargee par le navigateur du bac a sable (Edge headless, mandataire",
  "  127.0.0.1:25000, $PageNav — IP litterale D139) PAR LE PROXY 0.6.0-rc.1",
  "  scelle (carte generation 7) ARMÉ --relever-https : relèvement amont",
  "  http->https, tunnel Schannel, autorite locale 127.0.0.1:443 ;",
  "  run A (certificat VALIDE) : page rendue par le navigateur (marqueur au",
  "  DOM) ; run B (certificat AUTO-SIGNE) : la 502 « Certificat rejete »",
  "  RECUE PAR LE NAVIGATEUR (page d'erreur au DOM) — LES DEUX DANS LE MEME RUN.",
  "kit e2 : proxy 0.6.0-rc.1 (sha256 4b8f6af6…) ; fixtures v5 (SAN DNS+IP) ;",
  "parefeu neutralise des l'ouverture (decor v8) ; ligne de flux + armement",
  "constates au journal proxy ; matrice curl heritee en controle ADDITIF.",
  "",
  "ARTEFACTS JUGES :"
)
[IO.File]::WriteAllText($FichierTemoignage, ($Entete -join "`r`n") + "`r`n")
foreach ($T in $Temoignages) { [IO.File]::AppendAllText($FichierTemoignage, "  $T`r`n") }
[IO.File]::AppendAllText($FichierTemoignage, "`r`nRESERVES DE LECTURE (a confirmer au labo sur les pieces host) :`r`n")
if ($Reserves.Count -eq 0) {
  [IO.File]::AppendAllText($FichierTemoignage, "  aucune`r`n")
} else {
  foreach ($R in $Reserves) { [IO.File]::AppendAllText($FichierTemoignage, "  $R`r`n") }
}
[IO.File]::AppendAllText($FichierTemoignage, "`r`nDIAGNOSTICS (additifs — hors verdict) :`r`n")
if ($Diagnostics.Count -eq 0) {
  [IO.File]::AppendAllText($FichierTemoignage, "  aucun`r`n")
} else {
  foreach ($D in $Diagnostics) { [IO.File]::AppendAllText($FichierTemoignage, "  $D`r`n") }
}
[IO.File]::AppendAllText($FichierTemoignage, "  branche nommee (matrice curl) : $Branche`r`n")
[IO.File]::AppendAllText($FichierTemoignage, "`r`nVERDICT DU SCENARIO :`r`n")
if ($Echecs.Count -eq 0 -and $Reserves.Count -eq 0) {
  [IO.File]::AppendAllText($FichierTemoignage, "  M5-B ETAPE 2 : FLUX NAVIGATEUR — VERDICT : OK`r`n")
  [IO.File]::AppendAllText($FichierTemoignage, "  (page rendue par le navigateur PUIS 502 recue par le navigateur,`r`n")
  [IO.File]::AppendAllText($FichierTemoignage, "   ligne de flux v=0 puis v=3, armement relever-https constate,`r`n")
  [IO.File]::AppendAllText($FichierTemoignage, "   dans le MEME run, sans aucun reseau externe)`r`n")
} elseif ($Echecs.Count -eq 0) {
  [IO.File]::AppendAllText($FichierTemoignage, "  M5-B ETAPE 2 — VERDICT : OK-SOUS-RESERVE ($($Reserves.Count) lecture(s) aveugle(s))`r`n")
  [IO.File]::AppendAllText($FichierTemoignage, "  (la chaine a tourne : sondes port reussies, producteurs rc=0 ; les pieces`r`n")
  [IO.File]::AppendAllText($FichierTemoignage, "   marquees RESERVE sont a confirmer au labo sur les fichiers host)`r`n")
} else {
  [IO.File]::AppendAllText($FichierTemoignage, "  M5-B ETAPE 2 — VERDICT : ECHEC NOMME ($($Echecs.Count))`r`n")
  foreach ($UnEchec in $Echecs) { [IO.File]::AppendAllText($FichierTemoignage, "  $UnEchec`r`n") }
}
[IO.File]::AppendAllText($FichierTemoignage, "`r`nA ENVOYER AU LABO : ce temoin + scenario-m5b-journal.log + proxy-journal.log + dom-a.txt + dom-b.txt + nav-a.png + nav-b.png + nav-a-err.txt + nav-b-err.txt + nav-a-cap-err.txt + nav-b-cap-err.txt + autorite-a/b.log + autorite-a/b-console.log + autorite-a/b-err.log + hosts-lu.txt + curl-*.txt + page-d*.txt + autorite-d/e*.log + autorite-d/e-console.log + autorite-d/e-err.log + dnscache.txt + ipconfig-vm.txt + parefeu-vm.txt`r`n")

Journal ("temoin pose : $FichierTemoignage")
if ($Echecs.Count -gt 0) {
  Journal ("VERDICT : M5-B ETAPE 2 — ECHEC NOMME ($($Echecs.Count))")
  exit 1
} elseif ($Reserves.Count -gt 0) {
  Journal ("VERDICT : M5-B ETAPE 2 — OK-SOUS-RESERVE ($($Reserves.Count)) — pieces a confirmer au labo")
  exit 0
} else {
  Journal "VERDICT : M5-B ETAPE 2 — OK (flux navigateur intercepte de bout en bout, sans reseau)"
  exit 0
}
