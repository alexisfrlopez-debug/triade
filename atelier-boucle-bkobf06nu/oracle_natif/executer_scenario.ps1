# executer_scenario.ps1 — L'EXÉCUTION D'UN SCÉNARIO CONSIGNÉ au Windows du CI
# (le témoin : les hashes des observables — jamais l'affirmation muette)
param([string]$Id)
$ErrorActionPreference = "Stop"
# les témoins du scénario (posés par le runner avant l'exécution)
switch ($Id) {
    "T0-ouverture-384"     { $exe = "depot\loupe\loupe.exe"; $args = "temoin-384.bin" }
    "T1-ouverture-196609"  { $exe = "depot\loupe\loupe.exe"; $args = "temoin-196609.bin" }
    "T2-saisie-sauve"      { $exe = "depot\loupe\loupe.exe"; $args = "temoin-384.bin" }
    "T3-vecteurs-loupe13"  { $exe = "depot\m1\selftest.exe"; $args = "--loupe-13 --graine 20261120" }
}
# l'exécution (la boucle de messages pilotée par le scénario — le kit du CI)
$sortie = & .\depot\atelier-boucle-bkobf06nu\oracle_natif\piloter.ps1 -Exe $exe -Args $args -Id $Id
$sortie | ConvertTo-Json
