#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Écrit LISEZMOI-proxy.txt (M3 étape c) en CP1252 — TRIADE D47."""

TEXTE = """TRIADE M3 — proxy transparent pour curl (premier run terrain)
==============================================================

proxy.exe  (19 456 octets, PE32+ console x86-64, écrit à la main)
version 0.4.0-dev.1 — sha256 85d2aa21c1532a50…

POURQUOI CETTE VERSION : le jalon M3 (entrées non fiables) franchit
son étape (b) — proxy.exe est scellé. Le parseur HTTP complet (huit
blocs feuilles purs + session + orchestrateur, treize notations
écrites à la main) a passé l'oracle à scénarios : 153 036 cas verts,
falsification détectée, carte génération 5 (38 blocs sur 4 artefacts).
Treize blocs sont octet-identiques aux artefacts scellés M0/M1/M2
(hello.exe, selftest.exe, echo.exe) — la réutilisation R7 prouvée à
l'échelle d'une application complète. Le proxy écoute au port 25000,
une requête par connexion, réponse jamais parsée (ce qui n'est pas
parsé ne peut pas être mal parsé).

C'EST LA PREMIÈRE FOIS que le parseur touche le monde réel : chaque
octet du réseau est non fiable par contrat, et l'émulation ne prouve
pas le terrain (leçons X1-X8). Le but de ce run : curl traverse le
proxy.

1. Ouvrez une console (cmd) et lancez proxy.exe. Attendu :
     TRIADE M3 : proxy demarre (port 25000)
   C'est tout — il écoute sur 127.0.0.1:25000.

2. Dans une AUTRE console, requête HTTP ordinaire (forme absolue,
   le client envoie « GET http://... HTTP/1.1 » au proxy) :
     curl -x http://127.0.0.1:25000 http://neverssl.com/
   Attendu côté curl : la page s'affiche (HTTP 200).
   Attendu côté console proxy :
     connexion entrante
     fin connexion

3. Tunnel HTTPS (CONNECT — le parseur découpe l'autorité, connecte,
   répond « 200 Tunnel etabli », puis relaie les octets sans les
   lire) :
     curl -x http://127.0.0.1:25000 https://example.com/
   Attendu côté curl : la page s'affiche (certificat vérifié par
   curl, PAS par le proxy — M3 ne déchiffre rien).
   Attendu côté console proxy :
     connexion entrante
     tunnel
     fin connexion

4. Arrêt propre : tapez dans la console DU PROXY :
     quit
   puis Entrée. Attendu :
     arret
   et le processus se termine (code 0).

LECTURE DES ISSUES (si quelque chose casse) :
- « TRIADE M3 : integrite KO, arret » au démarrage : un octet du
  binaire a bougé pendant le transfert (la porte R10 a fait son
  travail AVANT tout effet réseau) — re-télécharger proxy.exe.
- « erreur reseau, arret » : l'écoute au port 25000 a échoué (port
  occupé par l'echo.exe d'un run précédent ? fermez-le).
- curl affiche une réponse 4xx/5xx courte (400/411/431/501/502/505) :
  c'est le proxy qui REFUSE la requête avec sa ligne d'état — chaque
  code a un propriétaire nommé dans la couche I ; notez l'URL exacte.
- console proxy muette, curl en attente : notez ce qui a été envoyé
  avant le gel — comme en M2, le dernier événement visible localise
  l'intervalle.

Après le run : copiez-collez le contenu de la console proxy (ou
déposez un fichier proxy_journal.txt dans le dossier test du Drive,
comme pour demo) — le protocole § 8.4 (constat terrain normé) fera
le reste.

Rappels : machine de test autorisée uniquement ; le proxy ne journalise
RIEN du contenu traversant (les lignes sont des événements, pas des
octets) ; une requête par connexion cliente (curl reconnecte tout
seul — comportement attendu, pas un défaut).
"""

with open("/home/z/my-project/triade/LISEZMOI-proxy.txt", "wb") as f:
    f.write(TEXTE.encode("cp1252"))
print("LISEZMOI-proxy.txt écrit (CP1252,", len(TEXTE.encode("cp1252")), "octets)")
