# TRIADE M5-b ETAPE 1 — LE SCENARIO COMPLET EN VM ISOLEE (reseau coupe) :
# l'autorite de test LOCALE remplace example.com et self-signed.badssl.com ;
# le critere M4 (tunnel + certificat + 502 exacte) est rejoue DANS la VM,
# SANS aucun reseau externe, avec journal + TEMOIN SUR LE DISQUE (D99) qui
# SURVIT a la destruction de la VM (dossier mappe preuves-m5b).
#
# Chaine : client forme-absolue (client-m5b.ps1) -> proxy.exe 0.5.0 scelle
# (127.0.0.1:25000) -> tunnel TLS -> autorite locale (127.0.0.1:443).
# Run A : certificat VALIDE (racine installee)  -> 200 + page + "tunnel chiffre etabli".
# Run B : certificat AUTO-SIGNE (autonome)      -> 502 "Certificat rejete" 34 octets EXACTS
#                                                + "certificat rejete" au journal proxy
#                                                + poignee refusee au journal autorite.
# LES DEUX RUNS DANS LE MEME scenario (le critere (b) l'exige).
#
# Le proxy est lance par cmd /c avec redirection NATIVE de sa console vers
# proxy-journal.log (le meme capture que les tuyaux du superviseur
# terrain.17) et son stdin reste pilotable : le scenario lui envoie
# « quit » a la fin (arret propre, code de sortie attendu 0, lecon D99).
#
# REFUS NOMMES (le scenario lui-meme est fail-closed) :
#   KIT-ABSENT | RACINE-NON-INSTALLEE | AUTORITE-MUETTE | PROXY-MUET |
#   CLIENT-ECHEC | PAGE-A-INVALIDE | PAGE-B-INVALIDE | AUTORITE-SORTIE-ANORMALE |
#   PROXY-SORTIE-ANORMALE
# Code de sortie : 0 = verdict OK ; 1 = au moins un echec NOMME ; 2 = refus d'entree.
param(
  [string]$Kit = "C:\kit",
  [string]$Preuves = "C:\preuves",
  [string]$Hote = "autorite.test"
)

$JournalScenario = "$Preuves\scenario-m5b-journal.log"
$FichierTemoignage = "$Preuves\temoin-m5b.txt"
$JournalProxy = "$Preuves\proxy-journal.log"
$Echecs = New-Object System.Collections.Generic.List[string]
$Temoignages = New-Object System.Collections.Generic.List[string]

function Journal([string]$Message) {
  $Ligne = "[{0}] [scenario] {1}" -f (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"), $Message
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

function Attendre-Journal([string]$Fichier, [string]$Aiguille, [int]$Secondes) {
  $Borne = (Get-Date).AddSeconds($Secondes)
  while ((Get-Date) -lt $Borne) {
    if ((Test-Path $Fichier) -and ([IO.File]::ReadAllText($Fichier) -match [regex]::Escape($Aiguille))) {
      return $true
    }
    Start-Sleep -Milliseconds 300
  }
  return $false
}

function Empreinte([string]$Fichier) {
  $Sha = (Get-FileHash -Algorithm SHA256 -Path $Fichier).Hash.ToLower()
  $Md5 = (certutil -hashfile $Fichier MD5 | Where-Object { $_ -match '^[0-9a-f]{32}$' }).ToLower()
  return "sha256 $Sha · md5 $Md5 · $((Get-Item $Fichier).Length) o — $Fichier"
}

# ---------------------------------------------------------------- 0. entree
Journal "demarrage — scenario M5-b ETAPE 1 (VM isolee, reseau coupe par .wsb) — machine $env:COMPUTERNAME"
$Requis = @(
  "$Kit\proxy.exe",
  "$Kit\autorite\autorite_test.py",
  "$Kit\autorite\fixtures\racine-autorite.pem",
  "$Kit\autorite\fixtures\serv-valide.pem",
  "$Kit\autorite\fixtures\serv-valide.key",
  "$Kit\autorite\fixtures\serv-autonome.pem",
  "$Kit\autorite\fixtures\serv-autonome.key",
  "$Kit\client-m5b.ps1",
  "$Kit\python\python.exe"
)
$Manquants = @($Requis | Where-Object { -not (Test-Path $_) })
if ($Manquants.Count -gt 0) {
  Journal ("REFUS KIT-ABSENT : {0}" -f ($Manquants -join " | "))
  exit 2
}
Journal ("kit complet — {0} fichiers requis presents" -f $Requis.Count)

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
Journal "hosts pose : $LigneHosts"

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

# ---------------------------------------------------------------- 3. RUN A (valide)
Journal "RUN A — mode VALIDE (certificat signe par la racine installee)"
$ProcA = Start-Process -FilePath "$Kit\python\python.exe" `
  -ArgumentList @("$Kit\autorite\autorite_test.py", "--mode", "valide",
                  "--port", "443", "--journal", "$Preuves\autorite-a.log",
                  "--arret-apres", "1") `
  -RedirectStandardOutput "$Preuves\autorite-a-console.log" `
  -RedirectStandardError "$Preuves\autorite-a-err.log" `
  -WindowStyle Hidden -PassThru
if (-not (Attendre-Journal "$Preuves\autorite-a.log" "en ecoute" 30)) {
  Journal "REFUS AUTORITE-MUETTE : aucune ligne « en ecoute » — voir autorite-a-err.log"
  exit 2
}
Journal "autorite A en ecoute (journal autorite-a.log)"

# le proxy : cmd /c relaye son stdin et capture sa console NATIVEMENT en fichier
$Psi = New-Object System.Diagnostics.ProcessStartInfo
$Psi.FileName = $env:ComSpec
$Psi.Arguments = '/c ""' + $Kit + '\proxy.exe" > "' + $JournalProxy + '" 2>&1"'
$Psi.WorkingDirectory = $Preuves
$Psi.UseShellExecute = $false
$Psi.CreateNoWindow = $true
$Psi.RedirectStandardInput = $true
$Proxy = [System.Diagnostics.Process]::Start($Psi)
if (-not (Attendre-Journal $JournalProxy "demarre" 30)) {
  Journal "REFUS PROXY-MUET : aucune banniere « demarre » — le proxy 0.5.0 scelle est attendu"
  $Proxy.StandardInput.WriteLine("quit")
  Start-Sleep -Seconds 2
  exit 2
}
Journal "proxy demarre (journal proxy-journal.log)"

$ClientA = Start-Process -FilePath "powershell" `
  -ArgumentList @("-NoProfile", "-ExecutionPolicy", "Bypass",
                  "-File", "$Kit\client-m5b.ps1", "-Hote", $Hote,
                  "-Sortie", "$Preuves\page-a.txt") `
  -WindowStyle Hidden -Wait -PassThru
Verdict "CLIENT-A" ($ClientA.ExitCode -eq 0) ("client forme absolue — code $($ClientA.ExitCode)")

$PageA = ""
if (Test-Path "$Preuves\page-a.txt") { $PageA = [IO.File]::ReadAllText("$Preuves\page-a.txt") }
$PremiereLigneA = (($PageA -split "`r`n")[0])
Verdict "PAGE-A-200" ($PageA -match "^HTTP/1\.1 200") ("premiere ligne : « $PremiereLigneA »")
Verdict "PAGE-A-MARQUEUR" ($PageA -match "TRIADE-M5B-PAGE-200") ("marqueur de l'autorite locale : " + $(if ($PageA -match "TRIADE-M5B-PAGE-200") { "present" } else { "ABSENT" }))
Verdict "TUNNEL-A" (([IO.File]::ReadAllText($JournalProxy)) -match "tunnel chiffre etabli") "ligne « tunnel chiffre etabli » au journal proxy"
Verdict "AUTORITE-A-SERVIE" (([IO.File]::ReadAllText("$Preuves\autorite-a.log")) -match "requete servie") "ligne « requete servie » au journal autorite"

if (-not $ProcA.WaitForExit(30000)) { $ProcA.Kill() }
Verdict "AUTORITE-A-ARRET" ($ProcA.ExitCode -eq 0) ("arret propre attendu (rc=0) — recu $($ProcA.ExitCode)")
if (Test-Path "$Preuves\page-a.txt") {
  $Temoignages.Add("RUN A : page-a.txt " + (Empreinte "$Preuves\page-a.txt")) | Out-Null
}

# ---------------------------------------------------------------- 4. RUN B (autonome)
Journal "RUN B — mode AUTONOME (certificat auto-signe, la mauvaise heresie de terrain.17)"
$ProcB = Start-Process -FilePath "$Kit\python\python.exe" `
  -ArgumentList @("$Kit\autorite\autorite_test.py", "--mode", "autonome",
                  "--port", "443", "--journal", "$Preuves\autorite-b.log",
                  "--arret-apres-secondes", "20") `
  -RedirectStandardOutput "$Preuves\autorite-b-console.log" `
  -RedirectStandardError "$Preuves\autorite-b-err.log" `
  -WindowStyle Hidden -PassThru
if (-not (Attendre-Journal "$Preuves\autorite-b.log" "en ecoute" 30)) {
  Journal "REFUS AUTORITE-MUETTE : aucune ligne « en ecoute » (run B)"
  exit 2
}
Journal "autorite B en ecoute (journal autorite-b.log)"

$ClientB = Start-Process -FilePath "powershell" `
  -ArgumentList @("-NoProfile", "-ExecutionPolicy", "Bypass",
                  "-File", "$Kit\client-m5b.ps1", "-Hote", $Hote,
                  "-Sortie", "$Preuves\page-b.txt") `
  -WindowStyle Hidden -Wait -PassThru
Verdict "CLIENT-B" ($ClientB.ExitCode -eq 0) ("client forme absolue — code $($ClientB.ExitCode)")

$OctetsB = New-Object byte[] 0
if (Test-Path "$Preuves\page-b.txt") { $OctetsB = [IO.File]::ReadAllBytes("$Preuves\page-b.txt") }
$AttenduB = [Text.Encoding]::ASCII.GetBytes("HTTP/1.1 502 Certificat rejete`r`n`r`n")
$Identiques = ($OctetsB.Length -eq 34)
if ($Identiques) {
  for ($i = 0; $i -lt 34; $i++) {
    if ($OctetsB[$i] -ne $AttenduB[$i]) { $Identiques = $false; break }
  }
}
Verdict "PAGE-B-502-EXACTE" $Identiques ("34 octets exacts attendus — recu $($OctetsB.Length) o" + $(if ($Identiques) { " IDENTIQUES" } else { " DIVERGENTS" }))
Verdict "CERTIFICAT-REJETE" (([IO.File]::ReadAllText($JournalProxy)) -match "certificat rejete") "ligne « certificat rejete » au journal proxy (LE critere)"
Verdict "POIGNEE-B-REFUSEE" (([IO.File]::ReadAllText("$Preuves\autorite-b.log")) -match "poignee de main refusee") "poignee refusee NOMMEE au journal autorite"

if (-not $ProcB.WaitForExit(40000)) { $ProcB.Kill() }
Verdict "AUTORITE-B-ARRET" ($ProcB.ExitCode -eq 0) ("arret propre par delai attendu (rc=0) — recu $($ProcB.ExitCode)")
if (Test-Path "$Preuves\page-b.txt") {
  $Temoignages.Add("RUN B : page-b.txt " + (Empreinte "$Preuves\page-b.txt")) | Out-Null
}

# ---------------------------------------------------------------- 5. arret du proxy
$Proxy.StandardInput.WriteLine("quit")
if (-not $Proxy.WaitForExit(30000)) { $Proxy.Kill() }
Verdict "PROXY-ARRET" ($Proxy.ExitCode -eq 0) ("quit console — code de sortie $($Proxy.ExitCode) (S47, lecon D99)")
$TexteJournalProxy = ""
if (Test-Path $JournalProxy) { $TexteJournalProxy = [IO.File]::ReadAllText($JournalProxy) }
Verdict "PROXY-ARRET-CONSOLE" ($TexteJournalProxy -match "arret") "ligne finale « arret » au journal proxy"

# ---------------------------------------------------------------- 6. temoin (D99)
$Entete = @(
  "TRIADE M5-b ETAPE 1 — TEMOIN SUR LE DISQUE (lecon D99)",
  "machine : $env:COMPUTERNAME (VM isolee — ce fichier SURVIT a la destruction de la VM)",
  "date : $(Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ')",
  "hote de test : $Hote (hosts -> 127.0.0.1, reseau coupe par .wsb)",
  "",
  "ARTEFACTS JUGES :"
)
[IO.File]::WriteAllText($FichierTemoignage, ($Entete -join "`r`n") + "`r`n")
foreach ($T in $Temoignages) { [IO.File]::AppendAllText($FichierTemoignage, "  $T`r`n") }
[IO.File]::AppendAllText($FichierTemoignage, "`r`nVERDICT DU SCENARIO :`r`n")
if ($Echecs.Count -eq 0) {
  [IO.File]::AppendAllText($FichierTemoignage, "  M5-B ETAPE 1 : TUNNEL + AUTORITE LOCALE — VERDICT : OK`r`n")
  [IO.File]::AppendAllText($FichierTemoignage, "  (200 + marqueur + tunnel chiffre etabli PUIS 502 exacte + certificat rejete,`r`n")
  [IO.File]::AppendAllText($FichierTemoignage, "   dans le MEME run, sans aucun reseau externe)`r`n")
} else {
  [IO.File]::AppendAllText($FichierTemoignage, "  M5-B ETAPE 1 — VERDICT : ECHEC NOMME ($($Echecs.Count))`r`n")
  foreach ($UnEchec in $Echecs) { [IO.File]::AppendAllText($FichierTemoignage, "  $UnEchec`r`n") }
}
[IO.File]::AppendAllText($FichierTemoignage, "`r`nA ENVOYER AU LABO : ce temoin + scenario-m5b-journal.log + proxy-journal.log + autorite-a.log + autorite-b.log + page-a.txt + page-b.txt`r`n")

Journal ("temoin pose : $FichierTemoignage")
if ($Echecs.Count -eq 0) {
  Journal "VERDICT : M5-B ETAPE 1 — OK (tunnel + autorite locale, sans reseau)"
  exit 0
} else {
  Journal ("VERDICT : M5-B ETAPE 1 — ECHEC NOMME ($($Echecs.Count))")
  exit 1
}
