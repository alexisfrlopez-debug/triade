# runner.ps1 — LE RUNNER ORACLE NATIF (le troisième régime, PREPARÉ au labo,
# exécuté au Windows du CI — jamais le terrain du développeur)
# La vague 9, l'instruction bkobf06nu point 3 — le PLAN-BKOBF06NU H3.
#
# LES ÉTAPES (fail-closed à chaque ligne) :
#   1. L'ACQUISITION : le clone frais du dépôt public (D220) ;
#   2. LES EMPREINTES SCELLÉES vérifiées AVANT TOUTE EXÉCUTION — tout
#      écart : arrêt immédiat (EMPREINTE-DIVERGENTE, nommée) ;
#   3. LES SCÉNARIOS consignés (scenarios.json — les mêmes que la
#      campagne, la graine 20261120) ;
#   4. LES TÉMOINS : chaque observable hashé (SHA-256) ;
#   5. LA SIGNATURE Ed25519 du témoin (la clé du CI — publique au dépôt) ;
#   6. LE RETOUR du témoin signé (la pièce que confronter.py juge au labo).
param(
    [string]$Depot = "https://github.com/TRIADE/public.git",
    [string]$Sortie = "temoin-natif.json"
)
$ErrorActionPreference = "Stop"

# --- 1. l'acquisition --------------------------------------------------------
Write-Host "[natif] 1. l'acquisition : le clone frais du depot public"
if (Test-Path .\depot) { Remove-Item -Recurse -Force .\depot }
git clone --depth 1 $Depot .\depot
if ($LASTEXITCODE -ne 0) { throw "ACQUISITION-ÉCHOUÉE" }

# --- 2. les empreintes scellées (AVANT toute exécution) ----------------------
Write-Host "[natif] 2. les empreintes scellées — la vérification d'abord"
$attendues = @{
    "depot\loupe\loupe.exe"     = "c111510535767a40b0122d4e42261c9d8e1ec10d94d95ef666fd76ceb93e61d1"
    "depot\tls13\proxy.exe"     = "446279f3ab356900870cc3b3e1700654a4216ec0b264172340e453db3b00d93d"
    "depot\m1\selftest.exe"     = "8038585b7af83c9fe5e6fdccd197e67888b9e5fb09d8d6c84cb998c684bff3c0"
}
foreach ($k in $attendues.Keys) {
    $h = (Get-FileHash -Algorithm SHA256 $k).Hash.ToLower()
    if ($h -ne $attendues[$k]) {
        throw "EMPREINTE-DIVERGENTE : $k attendu $($attendues[$k]) rendu $h"
    }
    Write-Host "[natif]    $k : VERT"
}

# --- 3-4. les scénarios consignés, les témoins hashés -------------------------
Write-Host "[natif] 3-4. les scénarios consignés, les témoins hashés"
$scenarios = Get-Content .\depot\atelier-boucle-bkobf06nu\oracle_natif\scenarios.json | ConvertFrom-Json
$temoins = @()
foreach ($s in $scenarios.scenarios) {
    $obs = & .\depot\atelier-boucle-bkobf06nu\oracle_natif\executer_scenario.ps1 -Id $s.id
    $temoins += @{
        id      = $s.id
        exit    = $obs.exit
        disque  = $obs.disque      # le hash SHA-256 du fichier témoin après
        ecran   = $obs.ecran       # le hash de la capture (la vitrine)
        console = $obs.console     # le hash de la sortie console
    }
    Write-Host "[natif]    $($s.id) : exit=$($obs.exit) disque=$($obs.disque.Substring(0,12))…"
}

# --- 5. la signature du témoin ------------------------------------------------
Write-Host "[natif] 5. la signature Ed25519 (la clé du CI)"
$corps = @{
    regime   = "oracle-natif/1"
    machine  = $env:COMPUTERNAME
    windows  = [System.Environment]::OSVersion.VersionString
    horodatage = (Get-Date).ToUniversalTime().ToString("o")
    temoins  = $temoins
} | ConvertTo-Json -Depth 4
# la signature : la clé privée au SECRET DU CI (natif_signing_key — JAMAIS au
# dépôt) ; l'outillage : python -c "import nacl..." (le CI porte python)
$corps | Out-File -Encoding utf8 temoin-corps.json
python .\depot\atelier-boucle-bkobf06nu\oracle_natif\signer_temoin.py temoin-corps.json $Sortie
if ($LASTEXITCODE -ne 0) { throw "SIGNATURE-ÉCHOUÉE" }
Write-Host "[natif] 6. LE TÉMOIN SIGNÉ : $Sortie — la pièce que confronter.py juge"
