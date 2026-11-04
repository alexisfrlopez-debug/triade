#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""construire_scenario_e3.py — LE SCÉNARIO e3 (garde d'armement FONCTIONNELLE
+ verdicts post-mortem, D145) depuis le scénario e2 du dépôt, par REMPLACEMENTS
ANCRÉS ASSERTÉS (modèle construire_v8_scenario.py, R1–R11) : tout ce qui n'est
pas nommé ci-dessous est repris OCTET POUR OCTET de l'e2 (le décor e2/v8 est
verrouillé par les runs précédents).

Les changements (Entrée 138, « la correction proposée », D145) :
  R1   le titre porte e3 ;
  R2   l'en-tête documente POURQUOI e3 (le refus du run e2 + D145) ;
  R3   REFUS PROXY-SANS-ARMEMENT -> PROXY-PAS-ARME ;
  R4   Attendre-Ligne (la garde en live, COUPABLE du run e2) -> Sonde-Armement
       (fonctionnelle : requête forme-absolue http:// au mandataire, réponse
       recopiée en pièce page-sonde-armement.txt) ;
  R5   DIAG-EDGE-VERSION par (Get-Item).VersionInfo (le --version du run e2
       était muet) + pièce edge-version.txt aux preuves ;
  R6   le journal de démarrage porte kit e3 ;
  R7   LA GARDE : la sonde remplace l'attente de ligne en live — REFUS
       PROXY-PAS-ARME si la page 200 de l'autorité A n'est pas reçue ;
  R8   AUTORITE-A-SERVIE : le détail nomme la sonde (elle aussi est servie) ;
  R9   RELEVER-ARME / TUNNEL-A / FLUX-A-V0 : verdicts post-mortem, détails
       honnêtes (la sonde produit AUSSI une ligne v=0 et un tunnel) ;
  R10  le témoin porte kit e3 + la sonde ;
  R11  la liste A ENVOYER gagne page-sonde-armement.txt + edge-version.txt.

Usage : python3 scripts/construire_scenario_e3.py
Code de sortie : 0 = scénario e3 écrit et vérifié ; 2 = refus nommé."""

import sys

REPO = "/home/z/my-project/triade-repo"
SOURCE = REPO + "/m5/vm/scenario-m5b-e2.ps1"
SORTIE = REPO + "/m5/vm/scenario-m5b-e3.ps1"


def refus(nom, detail):
    print(f"[e3] REFUS {nom} : {detail}")
    sys.exit(2)


def crlf(bloc):
    """Les blocs sont écrits en \\n lisibles puis passés en CRLF (le fichier
    est BOM+CRLF, contrat PowerShell 5.1 — v2)."""
    return bloc.replace("\n", "\r\n")


REMPLACEMENTS = []


def remplacer(numero, ancien, nouveau, attendu=1):
    REMPLACEMENTS.append((numero, crlf(ancien.strip("\n")), crlf(nouveau.strip("\n")), attendu))


# ------------------------------------------------------------------ R1 : titre
remplacer(1,
          "# TRIADE M5-b ETAPE 2 — LE FLUX NAVIGATEUR EN VM ISOLEE (reseau coupe) — e2.",
          "# TRIADE M5-b ETAPE 2 — LE FLUX NAVIGATEUR EN VM ISOLEE (reseau coupe) — e3.")

# ------------------------------------------------- R2 : l'en-tête documente e3
remplacer(2,
          "#\n"
          "# POURQUOI L'ETAPE 2 (faits consignes, pas des opinions) :",
          "#\n"
          "# POURQUOI L'ETAPE e3 (le run e2 a nomme la cause — la correction est D145) :\n"
          "#   le run e2 s'est arrete au REFUS PROXY-SANS-ARMEMENT : sa garde lisait EN\n"
          "#   LIVE le journal proxy, encore ouvert par le proxy vivant — et la VM rend\n"
          "#   ZERO octet pour un fichier en cours d'ecriture (« vues vides », le\n"
          "#   symptome des runs v7/v8 — D138). Le scellé 0.6.0-rc.1 est INNOCENT :\n"
          "#   l'armement A EU LIEU (la ligne vit a la piece post-mortem), l'ecoute\n"
          "#   etait posee, le quit a opere. D145 : les gardes sont FONCTIONNELLES\n"
          "#   (port ouvert, reponse attendue) ou POST-MORTEM — la preuve declarative\n"
          "#   CONSTATE, la preuve operative GARDE. TROIS changements e3 : (1) la garde\n"
          "#   d'armement devient la SONDE forme-absolue « GET http://127.0.0.1/ » au\n"
          "#   mandataire — la page 200 de l'autorite recue est la preuve OPERATIVE\n"
          "#   (un 0.5.1, ou un rc.1 non arme, routerait vers l'origine port 80,\n"
          "#   muette : 502) ; (2) la ligne « relever-https arme » devient un VERDICT\n"
          "#   POST-MORTEM (apres le quit, modele v8) ; (3) la version d'Edge se lit\n"
          "#   par VersionInfo (le --version du run e2 etait muet en console). TOUT LE\n"
          "#   RESTE EST L'ETAPE e2 INTACTE (decor v8 entier, Edge headless, IP\n"
          "#   litterale D139, matrice curl, parefeu 0bis, temoin D99 en dernier acte).\n"
          "#\n"
          "# POURQUOI L'ETAPE 2 (faits consignes, pas des opinions) :")

# --------------------------------------------------- R3 : le nom du refus e3
remplacer(3,
          "#   PROXY-MUET | PROXY-SANS-ARMEMENT | NAVIGATEUR-A-ECHEC | NAVIGATEUR-B-ECHEC |",
          "#   PROXY-MUET | PROXY-PAS-ARME | NAVIGATEUR-A-ECHEC | NAVIGATEUR-B-ECHEC |")

# ------------------------- R4 : Attendre-Ligne (la garde en live) -> la sonde
remplacer(4,
          """function Attendre-Ligne([string]$Fichier, [string]$Aiguille, [int]$Secondes) {
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
}""",
          """function Sonde-Armement([string]$Cible, [int]$Port, [int]$Secondes) {
  # e3 (D145) : la garde d'armement est FONCTIONNELLE — le scenario envoie
  # LUI-MEME au mandataire la requete forme-absolue CLAIRE du navigateur
  # (« GET http://cible/ HTTP/1.1 » + Host) et recopie la reponse : un 0.6.0
  # ARME releve vers https://cible:443, tunnelise et REND la page 200 de
  # l'autorite ; un 0.5.1 — ou un rc.1 non arme — routerait vers l'origine
  # port 80 (muette) : 502. La piece page-sonde-armement.txt est POSEE dans
  # TOUS les cas (reponse complete ou octets partiels) ; AUCUNE lecture en
  # live du journal proxy (le run e2 a nomme la cause : « vues vides »,
  # D138/D145 — le journal ne se lit qu'APRES le quit).
  $Sortie = "$Preuves\\page-sonde-armement.txt"
  $Recu = New-Object System.Collections.Generic.List[byte]
  $Client = $null
  try {
    $Client = New-Object Net.Sockets.TcpClient("127.0.0.1", $Port)
    $Client.ReceiveTimeout = $Secondes * 1000
    $Flux = $Client.GetStream()
    $OctetsReq = [Text.Encoding]::ASCII.GetBytes("GET http://$Cible/ HTTP/1.1`r`nHost: $Cible`r`n`r`n")
    $Flux.Write($OctetsReq, 0, $OctetsReq.Length)
    $Tampon = New-Object byte[] 65536
    while (($Lu = $Flux.Read($Tampon, 0, 65536)) -gt 0) {
      for ($i = 0; $i -lt $Lu; $i++) { $Recu.Add($Tampon[$i]) | Out-Null }
    }
  } catch {
    Journal ("sonde d'armement : lecture terminee — " + $_.Exception.GetType().Name + " — " + $Recu.Count + " octets recus")
  }
  try { if ($Client) { $Client.Close() } } catch { }
  $OctetsPage = $Recu.ToArray()
  [IO.File]::WriteAllBytes($Sortie, $OctetsPage)
  return [Text.Encoding]::UTF8.GetString($OctetsPage)
}""")

# ------------------------------------- R5 : DIAG-EDGE-VERSION par VersionInfo
remplacer(5,
          """# la version du navigateur est une PIECE (comparabilite inter-machines,
# modele 17-H tampon OS) — diagnostique ADDITIF, jamais un verdict : si
# --version se tait, le run continue, le DOM dira.
$VersionEdge = ""
try {
  $PVer = Start-Process -FilePath $CheminEdge -ArgumentList @("--version") `
    -RedirectStandardOutput "$Griffe\\edge-version.txt" `
    -RedirectStandardError "$Griffe\\edge-version-err.txt" `
    -WindowStyle Hidden -PassThru
  if ($PVer.WaitForExit(30000)) {
    $VersionEdge = ([IO.File]::ReadAllText("$Griffe\\edge-version.txt")).Trim()
  }
} catch { }
if ($VersionEdge.Length -gt 0) {
  Diagnostic "DIAG-EDGE-VERSION" $true ($VersionEdge + " — " + $CheminEdge)
} else {
  Diagnostic "DIAG-EDGE-VERSION" $false ("--version muet — piece edge-version.txt vide ou absente — le run continue")
}""",
          """# la version du navigateur est une PIECE (comparabilite inter-machines,
# modele 17-H tampon OS) — diagnostique ADDITIF, jamais un verdict. Le run
# e2 a nomme le fait : msedge.exe LOCALISE mais MUET a --version en console
# — e3 lit la VersionInfo du FICHIER (Get-Item, aucune invocation) et pose
# la piece edge-version.txt AUX PREUVES ; si elle se tait, le run continue,
# le DOM dira.
$VersionEdge = ""
try {
  $VersionEdge = [string](Get-Item $CheminEdge).VersionInfo.ProductVersion
} catch { }
if ($VersionEdge.Length -gt 0) {
  [IO.File]::WriteAllText("$Preuves\\edge-version.txt", "msedge : $VersionEdge`r`nchemin : $CheminEdge`r`nlecture : (Get-Item).VersionInfo — e3 (le run e2 : --version muet en console)`r`n")
  Diagnostic "DIAG-EDGE-VERSION" $true ($VersionEdge + " — " + $CheminEdge + " — piece edge-version.txt")
} else {
  [IO.File]::WriteAllText("$Preuves\\edge-version.txt", "msedge : VERSION INTROUVABLE par VersionInfo`r`nchemin : $CheminEdge`r`nlecture : (Get-Item).VersionInfo — e3`r`n")
  Diagnostic "DIAG-EDGE-VERSION" $false ("VersionInfo muet — piece edge-version.txt posee — le run continue")
}""")

# ------------------------------------------------- R6 : le journal de démarrage
remplacer(6,
          "kit e2 labo (proxy 0.6.0-rc.1 scelle, carte generation 7 ; LE NAVIGATEUR du bac a sable juge — critere (b) de D136)\"",
          "kit e3 labo (proxy 0.6.0-rc.1 scelle, carte generation 7 ; LE NAVIGATEUR du bac a sable juge — critere (b) de D136 ; garde d'armement FONCTIONNELLE + verdicts post-mortem, D145)\"")

# ------------------------------------------------ R7 : LA GARDE devient sonde
remplacer(7,
          """# L'ARMEMENT EST CONSTATE AVANT LE NAVIGATEUR (fail-closed tot) : la ligne
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
Journal "armement constate : ligne « relever-https arme » au journal proxy — le relèvement http->https est EN SERVICE\"""",
          """# L'ARMEMENT EST PROUVE PAR OPERATION AVANT LE NAVIGATEUR (e3, D145 —
# fail-closed tot, SANS aucune lecture en live du journal proxy) : la SONDE
# forme-absolue http:// traverse le mandataire ; un 0.6.0 ARME releve vers
# https://127.0.0.1:443, tunnelise et rend la page 200 de l'autorite A ; un
# 0.5.1 — ou un rc.1 non arme — routerait vers l'origine port 80, muette :
# 502. La ligne « relever-https arme » devient un VERDICT POST-MORTEM
# (section 5, apres le quit — modele v8 : plus AUCUNE lecture en live d'un
# fichier vivant, D145).
$ReponseSonde = Sonde-Armement $Origine 25000 25
$Sonde200 = ($ReponseSonde -match '^HTTP/1\\.1 200')
$SondeMarqueur = $ReponseSonde.Contains("TRIADE-M5B-PAGE-200")
if (-not ($Sonde200 -and $SondeMarqueur)) {
  $ExtraitSonde = ($ReponseSonde -replace '[^\\x20-\\x7E]', '.')
  if ($ExtraitSonde.Length -gt 160) { $ExtraitSonde = $ExtraitSonde.Substring(0, 160) }
  $VueSonde = $(if ($ExtraitSonde.Length -gt 0) { "« $ExtraitSonde »" } else { "RIEN (0 octet recu)" })
  Journal ("REFUS PROXY-PAS-ARME : la sonde forme-absolue « GET http://$Origine/ » n'a pas recu la page 200 de l'autorite A — reponse : $VueSonde — piece page-sonde-armement.txt ; un 0.5.1, ou un rc.1 non arme, routerait vers l'origine port 80 (muette : 502)")
  try { $Proxy.StandardInput.WriteLine("quit") } catch { }
  Start-Sleep -Seconds 2
  Tuer $Proxy "proxy"
  exit 2
}
Journal "armement PROUVE PAR OPERATION : la sonde « GET http://$Origine/ » a recupere la page 200 de l'autorite A (marqueur TRIADE-M5B-PAGE-200) — relevement http->https + tunnel + reponse, le mandataire est ARME (piece page-sonde-armement.txt)\"""")

# ------------------------------- R8 : AUTORITE-A-SERVIE nomme la sonde (honnêteté)
remplacer(8,
          "\"requete servie\" \"ligne « requete servie » au journal autorite (le navigateur peut faire PLUSIEURS requetes : page, favicon — toutes servies par le tunnel)\" $RcNavA",
          "\"requete servie\" \"ligne « requete servie » au journal autorite (la sonde d'armement e3 ET le navigateur y passent — page, favicon — toutes servies par le tunnel)\" $RcNavA")

# ------------------- R9 : les trois verdicts de journal honnêtes (post-mortem)
remplacer(9,
          """Verdict-Vue "RELEVER-ARME" @($JournalProxy) "relever-https arme" "ligne « relever-https arme » au journal proxy (l'armement du relèvement, http-12:R3 — deja constatee avant le navigateur)" $RcProxy
Verdict-Vue "TUNNEL-A" @($JournalProxy) "tunnel chiffre etabli" "ligne « tunnel chiffre etabli » au journal proxy (run A)" $RcProxy
Verdict-Vue "FLUX-A-V0" @($JournalProxy) "flux GET 127.0.0.1:443 v=0" "ligne de flux du run A (http-10:R3 : « flux GET 127.0.0.1:443 v=0 e=NN s=NN » — cible relevée, verdict 0 aboutie)" $RcProxy""",
          """Verdict-Vue "RELEVER-ARME" @($JournalProxy) "relever-https arme" "ligne « relever-https arme » au journal proxy (l'armement du relèvement, http-12:R3 — VERDICT POST-MORTEM apres le quit, D145 : la ligne CONSTATE, c'est la SONDE d'armement qui a garde)" $RcProxy
Verdict-Vue "TUNNEL-A" @($JournalProxy) "tunnel chiffre etabli" "ligne « tunnel chiffre etabli » au journal proxy (la sonde d'armement et le run A l'etablissent chacun)" $RcProxy
Verdict-Vue "FLUX-A-V0" @($JournalProxy) "flux GET 127.0.0.1:443 v=0" "ligne de flux v=0 (http-10:R3 : « flux GET 127.0.0.1:443 v=0 e=NN s=NN » — la sonde d'armement ET le run A la produisent, cible relevée, verdict 0 aboutie)" $RcProxy""")

# ---------------------------------------------------------- R10 : le témoin e3
remplacer(10,
          """  "kit e2 : proxy 0.6.0-rc.1 (sha256 4b8f6af6…) ; fixtures v5 (SAN DNS+IP) ;",
  "parefeu neutralise des l'ouverture (decor v8) ; ligne de flux + armement",
  "constates au journal proxy ; matrice curl heritee en controle ADDITIF.",""",
          """  "kit e3 : proxy 0.6.0-rc.1 (sha256 4b8f6af6…) ; fixtures v5 (SAN DNS+IP) ;",
  "parefeu neutralise des l'ouverture (decor v8) ; armement PROUVE PAR",
  "OPERATION (sonde forme-absolue, piece page-sonde-armement.txt) ; ligne de",
  "flux constatee au journal proxy POST-MORTEM (D145) ; matrice curl",
  "heritee en controle ADDITIF.",""")

# --------------------------------------- R11 : la liste des pièces à renvoyer
remplacer(11,
          "A ENVOYER AU LABO : ce temoin + scenario-m5b-journal.log + proxy-journal.log + dom-a.txt",
          "A ENVOYER AU LABO : ce temoin + scenario-m5b-journal.log + proxy-journal.log + page-sonde-armement.txt + edge-version.txt + dom-a.txt")


def main():
    data = open(SOURCE, "rb").read()
    if not data.startswith(b"\xef\xbb\xbf"):
        refus("SOURCE", "BOM UTF-8 absent du scénario e2")
    texte = data.decode("utf-8")
    if "\r\n" not in texte:
        refus("SOURCE", "CRLF absent du scénario e2")
    if texte.replace("\r\n", "").count("\n"):
        refus("SOURCE", "saut de ligne solitaire (LF sans CR) dans l'e2 — contrat CRLF rompu")

    for numero, ancien, nouveau, attendu in REMPLACEMENTS:
        vus = texte.count(ancien)
        if vus != attendu:
            refus(f"R{numero}", f"ancre présente {vus} fois ({attendu} attendue) — "
                                f"l'e2 a changé sous les pieds du constructeur")
        texte = texte.replace(ancien, nouveau)
        print(f"[e3] R{numero} appliqué ({len(ancien)} -> {len(nouveau)} caractères)")

    # -- vérifications du fichier né ------------------------------------------
    if not texte.startswith("\ufeff# TRIADE M5-b ETAPE 2 — LE FLUX NAVIGATEUR EN VM ISOLEE (reseau coupe) — e3."):
        refus("SORTIE", "le titre e3 n'est pas en tête")
    if texte.replace("\r\n", "").count("\n"):
        refus("SORTIE", "saut de ligne solitaire introduit — le contrat CRLF est rompu")
    for marqueur in ("PROXY-PAS-ARME", "Sonde-Armement", "page-sonde-armement.txt",
                     "VersionInfo", "POST-MORTEM", "TRIADE-M5B-PAGE-200",
                     "--relever-https", "NAVIGATEUR-ABSENT", "DIAG-EDGE-VERSION"):
        if marqueur not in texte:
            refus("SORTIE", f"marqueur e3 absent : {marqueur}")
    for vestige in ("Attendre-Ligne", "Attendre-Ligne $JournalProxy"):
        if vestige in texte:
            refus("SORTIE", f"vestige e2 encore présent : {vestige}")
    # « PROXY-SANS-ARMEMENT » ne survit qu'UNE fois : la mention HISTORIQUE du
    # refus du run e2 dans l'en-tête (R2) — le refus ACTIF est PROXY-PAS-ARME.
    vus = texte.count("PROXY-SANS-ARMEMENT")
    if vus != 1 or "REFUS PROXY-SANS-ARMEMENT : sa garde lisait EN" not in texte.split("param(", 1)[0]:
        refus("SORTIE", f"PROXY-SANS-ARMEMENT present {vus} fois (1 attendue : "
                        "la mention historique de l'en-tête uniquement)")
    # le seul --version INVOCQUÉ restant est celui de CURL (matrice 5bis) ; les
    # autres mentions sont historiques (commentaires e2/e3), jamais des appels.
    if '@("--version")' in texte:
        refus("SORTIE", "l'invocation Edge --version survit (elle doit être morte)")
    if texte.count("& $CurlExe --version") != 1:
        refus("SORTIE", "l'invocation curl --version absente ou dupliquée")

    octets = texte.encode("utf-8")
    open(SORTIE, "wb").write(octets)
    lignes = texte.count("\r\n") + 1
    print(f"[e3] scénario e3 ÉCRIT : {SORTIE}")
    print(f"[e3] {len(octets)} octets, {lignes} lignes, BOM+CRLF, {len(REMPLACEMENTS)} remplacements ancrés")
    print(f"[e3] la garde d'armement est FONCTIONNELLE (sonde forme-absolue), "
          f"RELEVER-ARME est post-mortem, DIAG-EDGE-VERSION lit VersionInfo")


if __name__ == "__main__":
    main()
