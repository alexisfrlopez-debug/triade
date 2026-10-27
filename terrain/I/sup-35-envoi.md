sup-35 · test T3 — envoi Drive (téléversement automatique) · révision 1
Intention : fermer la boucle du constat — le journal du superviseur part
DANS le dossier test du Drive SANS intervention : lecture du fichier
annexe terrain_jetons.bin (pose côté livraison, JAMAIS dans le dépôt —
interdit 11), rafraîchissement OAuth par curl.exe (POST requête
urlencodée, composée octet par octet), extraction du jeton (sup-22),
ouverture d'une session resumable (POST métadonnées, lecture de l'URL de
session dans les en-têtes -D), téléversement du journal (PUT --data-binary
@journal), vérification par code de sortie. La voie est EXACTEMENT celle
de drive_sync.py (même API, même uploadType) : le canal terrain et le
canal laboratoire convergent.
Contrat :
  pre  : P1 terrain_jetons.bin présent à côté de l'exécutable — format :
         4 champs ASCII NUL-terminés contigus, client_id, client_secret,
         refresh_token, token_uri (<= 480 o total) ; absent -> S31 «
         jetons absents » + S36 KO + rax = 0 (échec honnête, le journal
         reste local) ; P2 curl.exe résoluble ; P3 TAMPON_JETON (480 o),
         TAMPON_CMD (672 o) recyclables ; P4 BUF_CHEMIN contient le chemin
         complet du journal (posé par sup-11 à l'ouverture — le fichier
         existe donc au moins une ligne a été écrite) ; P5 pile alignée.
  post : Q1 lecture jetons (<= 480 o) + repérage des 4 champs par scan
         NUL ; Q2 requête OAuth composée dans TAMPON_CMD : "client_id=" +
         cid + "&client_secret=" + sec + "&refresh_token=" + rt +
         "&grant_type=refresh_token" (les valeurs OAuth sont sûres pour
         urlencoded : alphanumériques, tirets, points — aucun encodage
         requis) -> terrain_req.txt (CREATE_ALWAYS) -> S32 ; Q3 curl
         jeton : "-s --max-time 30 -o terrain_jeton.json --data
         @terrain_req.txt <uri>" (--fail retiré, D65 : une erreur HTTP
         doit écrire sa réponse — la preuve survit) -> code (35 s) ; code
         != 0 -> S33 KO code=NN + S36 KO + nettoyage + rax = 0 ; Q4
         terrain_jeton.json lu (<= 600 o) -> sup-22("access_token": \"",
         '"') -> TAMPON_JETON (NUL posé, longueur > 0) -> S33 ; introuvable/
         vide -> S33 KO code=NN + KO. [D69 : le format RÉEL de Google est
         INDENTÉ — « \"access_token\": \" » avec un espace — constaté sur le
         run terrain.14 et un rafraîchissement bac byte-identiques ; la
         forme compacte d'origine a masqué la panne des terrains 9-14.] ; Q5 métadonnées composées : {"name":"<TAMPON_NOM>",
         "parents":["<ID dossier test>"]} -> terrain_meta.json ; Q6 curl
         session : "-s --http1.1 -m 30 -o NUL -D terrain_session.txt
         -X POST -H \"Content-Type: application/json\" -H
         \"Authorization: Bearer <jeton>\" --data @terrain_meta.json
         https://www.googleapis.com/upload/drive/v3/files?uploadType=
         resumable" [D69 : --http1.1 forcée + -m 30 — en HTTP/2 curl -D
         écrit les en-têtes en minuscules (location:) et l'étiquette
         raterait ; en HTTP/1.1 Google répond « Location: » (sonde bac,
         octet ~194, sous la limite 600 o)] -> code -> terrain_session.txt
         lu (<= 600 o) ->
         sup-22("Location: ", 0x0D) -> URL de session dans TAMPON_JETON
         -> S34 ; Q7 curl téléversement : "-s --fail --max-time 120 -o
         NUL -X PUT --data-binary @<BUF_CHEMIN> <URL session>" -> code
         0 -> S35 OK ; tout autre code -> S35 ECHEC ; Q8 verdict : les
         trois codes 0 ET jeton extrait ET session extraite -> S36 OK +
         rax = 1 ; sinon S36 KO + rax = 0 ; Q9 nettoyage TOUT chemin :
         DeleteFileA des 5 fichiers temporaires (terrain_req.txt,
         terrain_jeton.json, terrain_meta.json, terrain_session.txt,
         terrain_rep.json si posé), fermeture des handles, ZÉRO jeton
         résiduel en mémoire au-delà de TAMPON_JETON (jamais journalisé —
         le journal ne contient AUCUN octet de secret).
  inv  : I1 les secrets ne passent JAMAIS par le journal (aucune ligne
         S* ne contient un octet des champs jetons — le journal embarqué
         côté Drive ne doit pas fuiter ses propres clés) ; I2 le chemin
         du journal téléversé est BUF_CHEMIN (chemin complet, la source
         de vérité de sup-11) — jamais recomposé ; I3 un seul but :
         TAMPON_JETON porte le jeton PUIS l'URL de session (cycle de vie
         séquentiel, jamais simultané) ; I4 chaque curl est attendu avec
         timeout (35 s / 35 s / 130 s) — pas de gel possible ; I5
         l'échec à une phase court-circuite les phases SUIVANTES mais
         JAMAIS le nettoyage.
Échecs :
  E1 : jetons absents -> S31, KO, journal local seulement (le terrain
       peut tout de même tester T1/T2 : l'envoi est un service, pas une
       condition).
  E2 : OAuth refuse (jeton révoqué, horloge) -> code != 0 ou jeton
       absent -> S33 ECHEC, KO.
  E3 : session refused (quota, droit) -> code != 0 ou Location absente
       -> S34 ECHEC, KO.
  E4 : téléversement interrompu (réseau) -> code != 0 -> S35 ECHEC, KO.
Vecteurs :
  V1 : round-trip 100 %.
  V2 : émulation nominale COMPLÈTE — jetons servis (4 champs), requête
       capturée == composition attendue octet par octet, réponse OAuth
       réaliste (jeton 40 o), métadonnées capturées contenant le nom
       TAMPON_NOM et l'ID dossier test, en-têtes réalistes avec
       Location, PUT --data-binary @<chemin journal> exact, code 0 ->
       S30..S36 OK, rax = 1, 5 DeleteFileA observés.
  V3 : jetons absents -> S31 + KO, AUCUN spawn curl.
  V4 : réponse OAuth sans access_token -> S33 ECHEC + KO, pas de
       session tentée (ordre des appels observé).
  V5 : falsification — corrompre l'étiquette "access_token": \""
       (un octet) fait échouer l'extraction -> V2 échoue ; omettre le
       nettoyage fait échouer le verrou « 5 DeleteFileA ».
Fixtures    : étiquettes sup-22 (16 o, 10 o, 4 o), ID dossier test (33 o),
              URL token OAuth, URL upload resumable, 3 gabarits cmdline,
              noms des 5 temporaires, lignes S30..S36.
Provenance  : écrite-avant-code.
Décisions   : D48 ; uploadType=resumable (voie drive_sync.py éprouvée,
              multipart/related évité — fabrication manuelle pénible et
              fragile) ; jetons en ANNEXE hors dépôt (interdit 11 : le
              dépôt reste propre, l'annexe voyage par le canal de livraison
              uniquement) ; curl.exe relais TLS (D48) — le superviseur ne
              déchiffre rien, ne signe rien : il compose des requêtes et
              lit des réponses, la cryptographie vit dans schannel.
