#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_entree193.py — LA CONSIGNATION DU GESTE DE LA GRANDE ŒUVRE
« LE SEPTIÈME RUN M9-(f) VERT SUR PIÈCES (LA SESSION RÉELLE ÉTABLIE) ;
LE RECOUP LABO VERT 34/34 SUR PIÈCES CROISÉES ; LA FINALE 1.0.0
SCELLÉE (FAIT DE CARTE) — LE JALON M9 FRANCHI » : la rangée (f) du plan
reçoit le constat, l'État du programme reçoit la phrase du geste, le
journal reçoit l'Entrée 193, DECISIONS reçoit la D170, le worklog
reçoit la Task ID 111. Rejeu REFUSÉ ; tout ancrage absent ou compté
autrement qu'UNE fois = ÉCHEC NOMMÉ, rien n'est écrit. Les ancres
RANGEE/ÉTAT sont importées de consigner_entree192 (les constats du
geste précédent — la chaîne des remplacements tient sans
retranscription)."""
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
DECISIONS = REPO / "docs" / "DECISIONS.md"
WORKLOG = REPO / "worklog.md"

sys.path.insert(0, str(REPO / "scripts"))
import consigner_entree192 as _c192  # noqa: E402  # la chaîne des gestes

# --- la rangée (f) : le constat du jalon remplace l'attente ------------------------

ANCIEN_RANGEE = _c192.NOUVELLE_RANGEE   # le constat 192 (la 3e signature + le kit réparé)

MOUVELLE_RANGEE = (
    " ; **LE SEPTIÈME RUN M9-(f) REÇU, RECROPÉ ET RECOPÉ VERT SUR PIÈCES "
    "le 07/11/2026 (Entrée 193, Task 111) : LA SESSION RÉELLE ÉTABLIE — "
    "LE JALON M9 FRANCHI, LA FINALE 1.0.0 SCELLÉE** [recouper_run7_m9f.py : "
    "LES SIX pièces md5-contrôlées, LE JUGE EST LE CODE — l'échelle "
    "REJOUÉE sur la clé privée DU RUN rend la clé du témoin (RFC 7748), "
    "la construction CH re-jouée (114 o, le vol 119 o), LA LIGNE REÇUE "
    "LUE EN CLAIR sur la pièce (1369 o — « HTTP/1.1 200 OK », LA "
    "PREMIÈRE LIGNE APPLICATIVE EN CLAIR DU PROJET), LES ÉMISSIONS "
    "RECADRÉES record par record (436 o en CINQ records SANS RESTE : "
    "119/58/116/119/24) ; LE RUN : LES VINGT T0 [ok] (les DEUX "
    "erratum-9 ET LES DEUX erratum-10 relus DANS L'IMAGE), le VRAI "
    "ntdll (SSN 85/7/15), le socket par LE VRAI afd.sys (zéro ws2_32), "
    "LA POIGNÉE OUVERTE (T3.ouvrir rax 0 état 3 — LA MORT -7 DES RUNS "
    "5/6 FRANCHIE : le contrat réparé de l'erratum n° 10 A VÉCU), LA "
    "GARDE -6 NOMMÉE contre le vrai serveur, LA FERMETURE PROPRE "
    "(close_notify 24 o, NtClose ×2, l'artefact relu inchangé) — VERDICT "
    "34/34] ; **LE SCELLAGE** (build_m9.py --sceller-final, le miroir M8 "
    "Entrée 164 : LE FAIT DE CARTE) [le garde 13/13 AVANT, le recoup "
    "terrain EXIGÉ SUR PIÈCES (VERT 34/34 + les six attestations A), la "
    "cristallisation R6 86 blocs à 10/10 (dix passes --verifier : M4 560 "
    "+ M5 365 + harnais 131 à chaque passe, verrou croisé 86/86), la "
    "bascule version=1.0.0-dev.4 → version=1.0.0 dans frag-bld "
    "(occurrence UNIQUE, vérifiée EN MÉMOIRE), les fragments re-chiffrés, "
    "la racine re-dérivée, L'ENTÊTE PORTE LA BALISE, la signature "
    "Ed25519 re-signée (graine durable D144 — le témoin ne bouge pas), "
    "le tableau de bord suit (« 1.0.0 SCELLÉE sur le recoup terrain "
    "M9-(f) VERT 34/34 sur pièces croisées ») ; POST-SEALLAGE : verrou "
    "croisé 86/86, **proxy.exe INTACT (446279f3…, 65 024 o — LE MÊME "
    "binaire que LE SEPTIÈME RUN a couru)**, la reconstruction REFUSÉE "
    "par l'anti-rollback (constaté : « carte scellée (1.0.0) : "
    "reconstruction interdite »), la re-vérification sous 1.0.0 VERTE] ; "
    "**LA CLÔTURE D143** [archiver_run7_m9f.py : preuves-run-m9f-7/ créé "
    "dans archives-preuves/ (D99), les CINQ pièces DÉPLACÉES du "
    "réceptacle vers l'archive (md5 constatés après — jamais un jet), "
    "le VERDICT-recoup-labo-m9f-7.txt déposé AVEC les pièces, "
    "preuves-m9f/ ré-armé (son LISEZMOI seul), LES DEUX INDEX mis à "
    "jour, la racine 19 entrées en ordre — le kit RÉPARÉ 92098687… "
    "INCHANGÉ]** — **LA GRANDE ŒUVRE : LE JALON M9 FRANCHI, L'ÈRE 1.0.0 "
    "SCELLÉE (TLS 1.3 pur en blocs scellés — AUCUN import réseau, "
    "AUCUN site syscall hors du tromphone, le socle AFD par syscalls "
    "directs)**"
)
NOUVELLE_RANGEE = MOUVELLE_RANGEE.replace("POST-SEALLAGE", "POST-SCELLAGE")

# --- l'État du programme : la phrase du jalon remplace l'attente -------------------

ANCIEN_ETAT = _c192.NOUVEL_ETAT        # l'État 192 (la 3e signature installée)

NOUVEL_ETAT = (
    "**LE SEPTIÈME RUN M9-(f) VERT SUR PIÈCES le 07/11/2026 (Entrée 193, "
    "D170, Task 111) : LA SESSION RÉELLE ÉTABLIE — LA LIGNE APPLICATIVE "
    "CHIFFRÉE ÉCHANGÉE AVEC UN SERVEUR RÉEL (le témoin « HTTP/1.1 200 OK » "
    "DÉCHIFFRÉ PAR LA MACHINE — LA PREMIÈRE LIGNE APPLICATIVE EN CLAIR DU "
    "PROJET), LA POIGNÉE ENTIÈRE PAR LE CLIENT TLS 1.3 DE L'ARTEFACT (la "
    "mort -7 des runs 5/6 FRANCHIE — le contrat réparé de l'erratum n° 10 "
    "A VÉCU), L'ÉPINGLAGE -6 NOMMÉ CONTRE LE VRAI SERVEUR, LA FERMETURE "
    "PROPRE ; LE RECOUP LABO VERT 34/34 SUR PIÈCES CROISÉES (l'échelle "
    "rejouée sur la clé du run, la ligne reçue lue en clair, les cinq "
    "émissions recadrées sans reste) ; LA FINALE 1.0.0 SCELLÉE — FAIT DE "
    "CARTE, L'ARTEFACT 446279f3… INTACT (la balise vit dans frag-bld, "
    "l'entête la porte, l'anti-rollback armé : la reconstruction "
    "interdite, la re-vérification sous 1.0.0 VERTE)** ; **LE JALON M9 "
    "FRANCHI — LA GRANDE ŒUVRE DE LA SOUVERAINETÉ COMPLÈTE : TLS 1.3 pur "
    "en blocs scellés, le socket par LE VRAI afd.sys aux syscalls "
    "directs, AUCUN import réseau, le programme des deux premières "
    "familles (D160) ACCOMPLI — win 1.0.0 / linux 0.7.0 / riscv 0.8.0 ; "
    "la clôture D143 passée (le run archivé AVEC son jugement), la "
    "passation D141 suit (la série 090 poursuit à la pointe)**"
)

# --- l'Entrée 193 au journal --------------------------------------------------------

ENTREE_193 = """## Entrée 193 — « preuves déposées dans le drive /test » : LE SEPTIÈME RUN M9-(f) VERT SUR PIÈCES (LA SESSION RÉELLE ÉTABLIE), LE RECOUP LABO VERT 34/34 SUR PIÈCES CROISÉES, LA FINALE 1.0.0 SCELLÉE — LE JALON M9 FRANCHI, LA GRANDE ŒUVRE (07/11)

**La reprise (le geste qui ouvre la session : LE PUSH GITHUB RÉPARÉ — la demande du développeur « répare le push git »).** Le labo recyclé avait perdu `.gdrive/` (les jetons) ET la pointe locale était en retard de DIX commits (les gestes 106-110 passés ailleurs). LES JETONS RAPATRIÉS du coffre Drive `/Tokens` (la procédure Task 79 rejouée : octets aux tailles identiques — 355/900/2344/93 o, chmod 600, JAMAIS affichés), `git-credentials` RÉGÉNÉRÉ depuis `token_git.txt` (133 o — la mécanique Entrée 133), `check_auth.py` : OAuth Drive 200 + GitHub 200 (compte alexisfrlopez-debug), la remote intacte (github.com/alexisfrlopez-debug/triade.git). Le diagnostic : « No configured push destination » au premier regard PUIS « fetch first » au premier push — la pointe locale était SEULEMENT EN RETARD (zéro divergence, `0 10`). LE FAST-FORWARD PROPRE ffcdf19 → 9ac03eb (la passation Task 110 embarquée), LE PUSH VERT (origin == HEAD == 9ac03eb, exit 0), la cohérence git ↔ Drive re-vérifiée au point R3 (`verifier_coherence_git_drive_r3.py` [labo] : 15 portes — git 4/4 [HEAD == origin, l'arbre propre, le fetch relit], le coffre /test 9/9 [la racine 19 entrées, le kit RÉPARÉ 92098687…, les DEUX sondes, LA TROISIÈME remise 0978c117… + l'ancre 188a7d42…, SANS copie de bundle, le réceptacle, l'index], le miroir 2/2 [le bundle courant 090-96d2b8d == 09ee7a1d…, 19 183 316 o par requête directe — la taille n'est pas servie par list_folder, l'empreinte FAIT FOI ; 55 archives, rien supprimé]) ; la réserve instrumentale D149 réinstallée AVANT usage (pynacl + keystone + capstone + pefile + unicorn).

**Le geste du développeur (l'annonce « preuves déposées dans le drive /test »).** LE SEPTIÈME RUN — le premier du contrat réparé — est au réceptacle preuves-m9f/ : les CINQ pièces nées du run ENTIER (temoin-m9f.txt, scenario-m9f-journal.log, ligne-recue.txt, journal-emissions.txt, VERDICT-run-m9f.txt). Le témoin (run du 2026-11-07 12:21:26, heure locale) : Windows 10.0 build 26300 · Python 3.14.3 · AMD64 ; le VRAI ntdll (base, chemin System32, sha256 b072efae…) consigné ; l'artefact ASSERTÉ (446279f3…, 65 024 o — le rebuild 1.0.0-dev.4) ; **LES VINGT T0 tranchés [ok]** (dont LES DEUX erratum-9 : la pose du WSABUF canonique relue DANS L'IMAGE aux DEUX blocs — ET LES DEUX erratum-10 : LE CONTRAT D'APPEL relu aux DEUX sites, AfdFlags = 0 et TdiFlags = TDI_RECEIVE_NORMAL 0x20), le SSN(NtDeviceIoControlFile) résolu par les DEUX lecteurs (SSN 7, jamais un numéro en cache), le socket par LE VRAI afd.sys (sys-04 : create + bind + connect, TROIS appels NT, zéro ws2_32), **LA POIGNÉE OUVERTE : T3.ouvrir rax 0, état 3 (CONNECTÉ) — LA MORT -7 DES RUNS 5/6 EST FRANCHIE**, LE RECOUP DU CH (119 o == la construction re-jouée : l'aléa @ +6, la clé publique @ +82 == l'échelle Python), **LA LIGNE APPLICATIVE CHIFFRÉE ÉCHANGÉE** (T4.emettre rax 0 ; le témoin « HTTP/1.1 200 OK » DANS LE FLUX DÉCHIFFRÉ PAR LA MACHINE — 1369 o reconstitués), **LA GARDE CONTRE LE VRAI SERVEUR** (T5.falsification : l'épinglage divergent -6 NOMMÉ, état 5 ; T5.discipline : la session morte n'a émis QUE son offre), **LA FERMETURE PROPRE** (le close_notify composé scellé émis — 24 o, 5 + 2 + 17 ; NtClose ×2 par le tromphone sys-01, NTSTATUS 0x0 ; l'artefact relu INCHANGÉ) ; les émissions du run : 5 enregistrements, 436 o. Le journal : HUIT lignes, TOUTES à 12:21:26, TOUTES VERTES (T0/T1/T2/T3/T4/T5/T6 — le run entier dans SA seconde). VERDICT DU RUN : **VERT — LA SESSION RÉELLE ÉTABLIE**.

**Le recoup labo (scripts/recouper_run7_m9f.py — le juge est le code).** Les SIX pièces rapatriées du coffre /test/preuves-m9f/ (md5 contrôlés par le rapatriement, RE-contrôlés au recoup contre les métadonnées Drive). TRENTE-QUATRE contrôles tranchés : A les pièces md5 + LES PIÈCES T4/T6 NÉES (le run a VÉCU jusqu'à la fermeture) ; B le témoin (LES VINGT T0, l'artefact du dépôt re-haché au geste même == 446279f3… INTACT, LE TERRAIN TENU — la machine familiale des runs 4/5/6, LA POIGNÉE OUVERTE, LE RECOUP DU CH, LA LIGNE, LA GARDE, LA FERMETURE, AUCUN rappel émission — sys-05 a rendu 0 à CHAQUE émission) ; C le journal (HUIT lignes à 12:21:26, les textes exacts de la source, AUCUN échec) ; D le verdict croisé (l'en-tête, le run daté, LE VERT NOMMÉ ; le témoin embarqué LIGNE POUR LIGNE — 49/49) ; E LE LABO PARLE (l'échelle X25519 REJOUÉE sur LA CLÉ PRIVÉE DU RUN rend LA CLÉ PUBLIQUE DU TÉMOIN — RFC 7748 ; la construction CH re-jouée : 114 o, l'aléa et la clé DU RUN, la référence que LA MACHINE a égalee octet pour octet ; **LA LIGNE REÇUE SUR PIÈCES : 1369 o, la tête « HTTP/1.1 200 OK\\r\\nDate: Sat, 07 Nov 2026 … » EN CLAIR — LA PREMIÈRE LIGNE APPLICATIVE EN CLAIR DU PROJET** ; LE JOURNAL DES ÉMISSIONS SUR PIÈCES : 436 o recadrés en CINQ records TLS SANS RESTE [119, 58, 116, 119, 24] — la discipline d'émission CONSTATÉE sur la pièce binaire ; le kit RÉPARÉ au coffre INCHANGÉ + la source porte l'empreinte ÉPINGLÉE du run + T0.erratum-10, AUCUNE écriture .raw ; le LISEZMOI du kit nomme LE SEPTIÈME run) ; F LA CONDITION NOMMÉE D'AVANCE (la passation 110 : « ET SI LE VERT TIENT : LA FINALE 1.0.0, LE JALON M9 — LA GRANDE ŒUVRE » ; le verdict du run la répète). VERDICT : **RECOUP VERT 34/34 — la finale 1.0.0 DÉBLOQUÉE**.

**La cristallisation R6 (exigée au scellage).** Dix passes --verifier (graine 20261106, volume complet : oracle M4 560 + oracle M5 365 + harnais sys 131 cas verts à chaque passe, verrou croisé 86/86) : **86 blocs à 10/10**.

**Le scellage (tls13/build_m9.py --sceller-final — né au geste, modèle D147/corpus, le miroir M8 Entrée 164).** LES PORTES tranchées AVANT l'unique écriture : le garde sceau I (13 arbres d'intention, clé « réelle ») ; LE RECOUP TERRAIN EXIGÉ SUR PIÈCES (le verdict VERT 34/34 + les six attestations A — absent ou rouge : REFUS NOMMÉ) ; la cristallisation 86 × 10/10 ; le verrou croisé R8 et la balise encore dev.4 ; la bascule version=1.0.0-dev.4 → version=1.0.0 dans frag-bld (occurrence UNIQUE, vérifiée EN MÉMOIRE, l'ancienne absente après) ; les fragments re-chiffrés, la racine re-dérivée, L'ENTÊTE PORTE LA BALISE (construire_entete paramétré), la signature Ed25519 re-signée (graine durable D144 : LE TÉMOIN NE BOUGE PAS) ; le tableau de bord suit (la ligne preversions CONSCIENTE de la balise : « 1.0.0 SCELLÉE sur le recoup terrain M9-(f) VERT 34/34 sur pièces croisées ») ; post-scellage : verrou croisé 86/86, **proxy.exe INTACT (446279f3…, 65 024 o — LE SCELLAGE EST UN FAIT DE CARTE, l'artefact ne bouge jamais : LE MÊME binaire que LE SEPTIÈME RUN a couru)**, la reconstruction désormais REFUSÉE par l'anti-rollback (constaté : « carte scellée (1.0.0) : reconstruction interdite »), la re-vérification sous 1.0.0 VERTE (la balise préservée, cristallisation maintenue).

**La clôture D143 (le geste qui suit le scellage).** scripts/archiver_run7_m9f.py : preuves-run-m9f-7/ créé dans archives-preuves/ (D99 : jamais mélanger les runs) ; les CINQ pièces DU RUN DÉPLACÉES du réceptacle vers l'archive (md5 constatés après le geste — un déplacement, jamais un jet) ; le VERDICT-recoup-labo-m9f-7.txt déposé AVEC les pièces (l'archive porte le jugement) ; preuves-m9f/ ré-armé (son LISEZMOI seul — le réceptacle demeure) ; LES DEUX INDEX mis à jour (LISEZMOI-archives-preuves.txt + LISEZMOI-archives-livraisons.txt) ; la racine 19 entrées en ordre — le kit RÉPARÉ 92098687… INCHANGÉ.

**Détail.** FRONTIÈRES : le scellé 0.9.0 INTACT (l'ancre R7 — l'héritage recomposé octet par octet au build même) ; l'artefact 446279f3… DEMEURE L'ARTEFACT FINAL 1.0.0 (le fait de carte D104/D165 : la balise vit dans frag-bld, l'entête la porte, le binaire ne bouge jamais) ; le kit RÉPARÉ demeure au /test (la pièce du jalon — le MÊME zip que le run a exécuté) ; les pièces de cérémonie demeurent (la TROISIÈME remise 0978c117… INSTALLÉE + l'ancre 188a7d42…) ; la clé privée jamais traversée (D87) ; les balises sœurs INTACTES (linux 0.7.0 / riscv 0.8.0). Livrables : scripts/recouper_run7_m9f.py, scripts/archiver_run7_m9f.py, tls13/build_m9.py (--sceller-final), tls13/carte_m9.py (VERSION_FINALE), tls13/carte/ (la balise 1.0.0), download/preuves-run-m9f-7/ (les pièces + VERDICT-recoup-labo-m9f-7.txt) ; consignations : la présente Entrée PAR SCRIPT, D170 PAR SCRIPT (docs/DECISIONS.md), PLAN (la rangée (f) + l'État du programme — LE JALON M9 FRANCHI), worklog +Task ID 111. SUITE : LA PASSATION D141 (la série 090 poursuit : le bundle à la pointe, l'ancien 090-96d2b8d archivé versionné) + LE PUSH GITHUB À LA POINTE — LES TROIS MIROIRS ALIGNÉS À LA FINALE 1.0.0.

"""

# --- la D170 au registre des décisions ---------------------------------------------

D170 = """
## D170 — LE JALON M9 FRANCHI : LA FINALE 1.0.0 SCELLÉE SUR LE RECOUP TERRAIN EXIGÉ COMME PIÈCE (le miroir D165 porté à l'ère M9 : le scellage REFUSE en l'absence du verdict du recoup vert — la porte est de PROCESSUS, jamais de console) ; LE SCELLAGE EST UN FAIT DE CARTE, L'ARTEFACT NE BOUGE JAMAIS (la balise 1.0.0 vit dans frag-bld, l'entête la porte, proxy.exe demeure byte-identique 446279f3… — LE MÊME binaire que LE SEPTIÈME RUN a couru) ; LA SESSION RÉELLE EST LE CRITÈRE DE LA RANGÉE (f) (la ligne applicative chiffrée ÉCHANGÉE avec un serveur réel, le témoin « HTTP/1.1 200 OK » DÉCHIFFRÉ PAR LA MACHINE, l'épinglage -6 NOMMÉ contre le vrai serveur, la fermeture propre — D166 tenue)

**Le contexte qui fonde la décision (07/11, au geste de la grande œuvre).** LE SEPTIÈME run M9-(f) — le premier du contrat réparé (l'erratum n° 10 : AfdFlags = 0, TdiFlags = TDI_RECEIVE_NORMAL 0x20) — est VERT sur pièces : LA SESSION RÉELLE ÉTABLIE (la poignée ENTIÈRE par LE CLIENT TLS 1.3 DE L'ARTEFACT, la mort -7 des runs 5/6 FRANCHIE, la ligne applicative déchiffrée par la machine, la garde contre le vrai serveur, la fermeture propre). Le recoup labo 34/34 sur pièces croisées (l'échelle rejouée sur la clé du run, la ligne reçue lue en clair, les cinq émissions recadrées sans reste). La condition nommée d'avance par la passation 110 (« ET SI LE VERT TIENT : LA FINALE 1.0.0, LE JALON M9 — LA GRANDE ŒUVRE ») est REMPLIE.

**Les règles.** (1) **La finale se scelle sur pièces, jamais sur console** : le --sceller-final EXIGE le verdict du recoup terrain VERT (34/34 + les six attestations) — D138/D145/D148/D154 étendues au geste final, le miroir de D165 à l'ère M9. (2) **Le scellage est un fait de carte** : la balise 1.0.0 vit dans frag-bld (occurrence unique, bascule vérifiée EN MÉMOIRE), l'entête la porte, la racine re-dérivée, la signature Ed25519 re-signée (graine durable D144) — proxy.exe INTACT, le binaire que le terrain a couru EST le binaire final. (3) **L'anti-rollback ARME l'ère refermée** : la carte scellée (1.0.0) interdit la reconstruction (R6) — constaté au geste même ; la re-vérification sous la balise scellée demeure licite (R5/R7). (4) **La clôture D143 accompagne le scellage** : le run archivé AVEC son jugement (preuves-run-m9f-7/), le réceptacle ré-armé, le kit du jalon demeuré au coffre. (5) **Aucune règle du cœur n'est modifiée** — la décision constate un franchissement, elle ne légifère pas.

**Alternatives rejetées.** Sceller sans le recoup (rejeté : la porte est de processus — D165) ; rebâtir l'artefact à la balise 1.0.0 (rejeté : le fait de carte — l'artefact que le terrain a établi ne bouge jamais, un rebuild serait UN AUTRE binaire) ; poser la version PE 0x01000000 dans l'image (rejeté : la version PE @0x2820 demeure 0x01000004 — le geste de BUILD est passé, le scellage n'est pas un build) ; archiver le kit avec le run (rejeté : le kit RÉPARÉ demeure au /test, la pièce du jalon) ; ouvrir aussitôt l'ère suivante (rejeté : l'ouverture d'une famille est la décision du développeur — D160, le modèle D149).

**Frontières.** Le scellé 0.9.0 INTACT (l'ancre R7) ; les balises sœurs INTACTES (linux 0.7.0 / riscv 0.8.0) ; la clé privée jamais traversée (D87) ; les pièces de cérémonie demeurées (la TROISIÈME remise 0978c117… + l'ancre 188a7d42…). Les pièces : les SIX du run + le verdict du recoup aux archives-preuves/preuves-run-m9f-7/, la carte scellée tls13/carte/ (la balise 1.0.0), le verdict du recoup download/preuves-run-m9f-7/VERDICT-recoup-labo-m9f-7.txt (34/34).
"""

# --- le worklog racine : la Task ID 111, À LA SUITE (append) ------------------------

TASK_111 = """
## Task ID 111 — LE SEPTIÈME RUN VERT SUR PIÈCES (LA SESSION RÉELLE ÉTABLIE) ; LE RECOUP LABO VERT 34/34 SUR PIÈCES CROISÉES ; LA FINALE 1.0.0 SCELLÉE (FAIT DE CARTE — L'ARTEFACT 446279f3… INTACT) — LE JALON M9 FRANCHI, LA GRANDE ŒUVRE (07/11)

Work Log:
- LA REPRISE DU GESTE : LE PUSH GITHUB RÉPARÉ (la demande du
  développeur « répare le push git ») — les jetons .gdrive/ perdus au
  recyclage RAPATRIÉS du coffre Drive /Tokens (la procédure Task 79 :
  octets identiques, 600, JAMAIS affichés), git-credentials régénéré
  (133 o, la mécanique Entrée 133), check_auth.py : OAuth Drive 200 +
  GitHub 200 (alexisfrlopez-debug) ; la pointe locale EN RETARD DE DIX
  commits (zéro divergence) — fast-forward PROPRE ffcdf19 → 9ac03eb,
  LE PUSH VERT (origin == HEAD, exit 0) ; la cohérence git ↔ Drive
  re-vérifiée (verifier_coherence_git_drive_r3.py [labo] : 15 portes —
  git 4/4, le coffre /test 9/9, le miroir 2/2) ; la réserve
  instrumentale D149 réinstallée (pynacl, keystone, capstone, pefile,
  unicorn).
- LE SEPTIÈME RUN REÇU (« preuves déposées dans le drive /test ») :
  LES CINQ pièces au réceptacle preuves-m9f/ — le run ENTIER A VÉCU
  (les pièces T4/T6 nées : ligne-recue.txt + journal-emissions.txt).
  LE TÉMOIN : LES VINGT T0 [ok] (les DEUX erratum-9 + LES DEUX
  erratum-10 relus DANS L'IMAGE), le VRAI ntdll (SSN 85/7/15), le
  socket par LE VRAI afd.sys (zéro ws2_32), **LA POIGNÉE OUVERTE
  (T3.ouvrir rax 0 état 3 — LA MORT -7 DES RUNS 5/6 FRANCHIE)**, LE
  RECOUP DU CH (119 o), LA LIGNE APPLICATIVE ÉCHANGÉE (le témoin
  « HTTP/1.1 200 OK » DÉCHIFFRÉ PAR LA MACHINE — 1369 o), LA GARDE -6
  NOMMÉE, LA FERMETURE PROPRE (close_notify 24 o, NtClose ×2,
  l'artefact relu inchangé) ; le journal HUIT lignes TOUTES VERTES
  dans SA seconde (12:21:26) — VERDICT DU RUN : VERT, LA SESSION
  RÉELLE ÉTABLIE.
- LE RECOUP LABO (recouper_run7_m9f.py — le juge est le code) : LES
  SIX pièces md5 == Drive ; TRENTE-QUATRE contrôles VERTS — l'échelle
  REJOUÉE sur la clé privée DU RUN rend la clé du témoin (RFC 7748),
  la construction CH re-jouée (114 o), **LA LIGNE REÇUE LUE EN CLAIR
  sur la pièce (1369 o — LA PREMIÈRE LIGNE APPLICATIVE EN CLAIR DU
  PROJET)**, LES CINQ ÉMISSIONS RECADRÉES SANS RESTE (436 o :
  119/58/116/119/24), le kit 92098687… INCHANGÉ + l'empreinte
  épinglée dans la source ; LA CONDITION NOMMÉE D'AVANCE lue au
  worklog + au JOURNAL (Entrée 192) — VERDICT : RECOUP VERT 34/34,
  la finale DÉBLOQUÉE. (DEUX défauts d'instrument nommés par le
  fail-closed en cours de geste : une clé publique recopiée à la main
  FAUTIVE — corrigée : les TROIS valeurs du run PARSÉES de la pièce ;
  la ligne BILAN absente du verdict écrit — corrigée : le bilan vit
  dans la pièce. Les pièces immuables, D154.)
- LA CRISTALLISATION R6 : dix passes --verifier (graine 20261106,
  volume complet : M4 560 + M5 365 + harnais 131 à chaque passe,
  verrou croisé 86/86) — 86 blocs à 10/10.
- LE SCELLAGE (build_m9.py --sceller-final — né au geste, le miroir
  M8 Entrée 164) : le garde 13/13 AVANT ; LE RECOUP TERRAIN EXIGÉ SUR
  PIÈCES (VERT 34/34 + les six attestations A) ; la cristallisation
  86×10/10 ; le verrou croisé + la balise encore dev.4 ; la bascule
  version=1.0.0-dev.4 → version=1.0.0 dans frag-bld (occurrence
  UNIQUE, EN MÉMOIRE) ; les fragments re-chiffrés, la racine
  re-dérivée, L'ENTÊTE PORTE LA BALISE, la signature Ed25519
  re-signée (graine durable D144) ; le tableau de bord suit ;
  POST-SEALLAGE : verrou croisé 86/86, **proxy.exe INTACT
  (446279f3…, 65 024 o — LE MÊME binaire que LE SEPTIÈME RUN a
  couru)**, la reconstruction REFUSÉE par l'anti-rollback (constaté),
  la re-vérification sous 1.0.0 VERTE.
- LA CLÔTURE D143 (archiver_run7_m9f.py) : preuves-run-m9f-7/ créé
  (D99), les CINQ pièces DÉPLACÉES (md5 constatés après — jamais un
  jet), le VERDICT-recoup-labo-m9f-7.txt déposé AVEC les pièces,
  preuves-m9f/ ré-armé (son LISEZMOI seul), LES DEUX INDEX mis à
  jour, la racine 19 entrées en ordre (le kit RÉPARÉ 92098687…
  INCHANGÉ).
- FRONTIÈRES : le scellé 0.9.0 INTACT (l'ancre R7) ; l'artefact
  446279f3… DEMEURE L'ARTEFACT FINAL 1.0.0 (le fait de carte) ; le
  kit RÉPARÉ demeure au /test (la pièce du jalon) ; les pièces de
  cérémonie demeurées (la TROISIÈME remise 0978c117… + l'ancre
  188a7d42…) ; la clé privée jamais traversée (D87) ; les balises
  sœurs INTACTES (linux 0.7.0 / riscv 0.8.0). Consignations :
  l'Entrée 193 PAR SCRIPT, D170 PAR SCRIPT, PLAN (la rangée (f) +
  l'État — LE JALON M9 FRANCHI), la présente Task ID 111 ;
  scripts : recouper_run7_m9f.py, archiver_run7_m9f.py,
  consigner_entree193.py.
- SUITE : LA PASSATION D141 (la série 090 poursuit : le bundle à la
  pointe, l'ancien 090-96d2b8d archivé versionné) + LE PUSH GITHUB À
  LA POINTE — LES TROIS MIROIRS ALIGNÉS À LA FINALE 1.0.0.
""".replace("POST-SEALLAGE", "POST-SCELLAGE")

# ------------------------------------------------------------------------------------


def main():
    # 1. le plan : la rangée (f) + l'État (idempotent : déjà-fait = constaté)
    plan = PLAN.read_text(encoding="utf-8")
    if "LE SEPTIÈME RUN M9-(f) REÇU, RECROPÉ ET RECOPÉ VERT SUR PIÈCES" in plan:
        print("PLAN : la rangée (f) + l'État déjà consignés — constaté")
    else:
        if plan.count(ANCIEN_RANGEE) != 1:
            sys.exit(f"ÉCHEC : ancrage rangée (f) trouvé "
                     f"{plan.count(ANCIEN_RANGEE)} fois (attendu : 1)")
        if plan.count(ANCIEN_ETAT) != 1:
            sys.exit(f"ÉCHEC : ancrage État trouvé "
                     f"{plan.count(ANCIEN_ETAT)} fois (attendu : 1)")
        plan = plan.replace(ANCIEN_RANGEE, NOUVELLE_RANGEE, 1)
        plan = plan.replace(ANCIEN_ETAT, NOUVEL_ETAT, 1)
        if "LE JALON M9 FRANCHI" not in plan:
            sys.exit("ÉCHEC : la rangée (f) ne porte pas le constat du jalon "
                     "après remplacement")
        if "LA FINALE 1.0.0 SCELLÉE" not in plan:
            sys.exit("ÉCHEC : l'État ne porte pas la phrase du jalon")
        PLAN.write_text(plan, encoding="utf-8")
        print("PLAN : la rangée (f) + l'État du programme — consignés")

    # 2. le journal : l'Entrée 193 avant le marqueur m5a (idempotent)
    journal = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 193 —" in journal:
        print("JOURNAL : l'Entrée 193 déjà consignée — constaté")
    else:
        marqueur = "<!-- m5a:journal-des-builds v1"
        if journal.count(marqueur) != 1:
            sys.exit(f"ÉCHEC : le marqueur m5a trouvé "
                     f"{journal.count(marqueur)} fois (attendu : 1)")
        journal = journal.replace(marqueur, ENTREE_193 + marqueur, 1)
        if "## Entrée 193 — « preuves déposées dans le drive /test »" not in journal:
            sys.exit("ÉCHEC : l'Entrée 193 absente après remplacement")
        JOURNAL.write_text(journal, encoding="utf-8")
        print("JOURNAL : l'Entrée 193 consignée AVANT le marqueur m5a")

    # 3. le registre des décisions : la D170 à la suite de D169
    decisions = DECISIONS.read_text(encoding="utf-8")
    if "## D170 —" in decisions:
        print("DECISIONS : la D170 déjà consignée — constaté")
    else:
        if "## D169 —" not in decisions:
            sys.exit("ÉCHEC : la D169 absente (le geste précédent n'est pas "
                     "consigné)")
        decisions = decisions.rstrip("\n") + "\n" + D170.strip("\n") + "\n"
        if "## D170 — LE JALON M9 FRANCHI" not in decisions:
            sys.exit("ÉCHEC : la D170 absente après append")
        DECISIONS.write_text(decisions, encoding="utf-8")
        print("DECISIONS : la D170 consignée À LA SUITE de la D169")

    # 4. le worklog racine : la Task ID 111 à la suite
    worklog = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 111 —" in worklog:
        sys.exit("ÉCHEC : la Task ID 111 existe déjà (rejeu REFUSÉ)")
    if "## Task ID 110 —" not in worklog:
        sys.exit("ÉCHEC : l'entrée Task ID 110 absente (le geste précédent "
                 "n'est pas consigné)")
    ancre_fin = "TIENT : LA FINALE 1.0.0, LE JALON M9 — LA GRANDE ŒUVRE."
    if not worklog.rstrip().endswith(ancre_fin):
        sys.exit("ÉCHEC : le worklog ne se termine pas sur la Task 110 "
                 "attendue (ancre de suite absente)")
    worklog = worklog.rstrip("\n") + "\n" + TASK_111
    if "## Task ID 111 — LE SEPTIÈME RUN VERT SUR PIÈCES" not in worklog:
        sys.exit("ÉCHEC : la Task ID 111 absente après append")
    WORKLOG.write_text(worklog, encoding="utf-8")
    print("WORKLOG : la Task ID 111 consignée À LA SUITE de la Task 110")


if __name__ == "__main__":
    main()
