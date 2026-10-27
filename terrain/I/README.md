# Couche I — jalon terrain (superviseur, lignée f6xxxx, génération 5)

Spécifications écrites-avant-code du **superviseur terrain** : un exe GUI
écrit à la main (PE32+ WINDOWS_GUI) qui exécute TOUS les tests du projet
en UN clic et téléverse le journal du run dans le dossier test du Drive,
automatiquement, par relais curl.exe (composant système). Décision
fondatrice : D48.

## La réponse à une exigence du développeur

« génère un fichier .exe afin d'effectuer tous tes tests en 1 clic via une
GUI, et je veux que cet exe envoie directement les logs des tests
automatiquement dans un dossier du drive que tu pourras examiner pour la
suite du projet ». Le superviseur EST cette phrase : bouton « TOUT
DÉMARRER » (coquille démo éprouvée), tests T1/T2/T3 enchaînés, journal
horodaté unique par run (terrain_YYYYMMDD_HHMMSS.txt), téléversement
resumable dans le dossier test (1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0) par la
MÊME voie que drive_sync.py. Le développeur n'a plus rien à copier-coller :
un clic, puis le constat attend le laboratoire dans le Drive.

## Les tests (v1)

| Test | Cible | Preuve exigée |
|---|---|---|
| T1 | demo.exe 0.3.0 (M2 scellé) | 17 lignes exactes, dernière = « boucle § 5 complète - DÉMO OK », exit 0 |
| T2 | proxy.exe 0.4.0-dev.1 (M3 étape c) | bannière + 5 événements exacts + arret + exit 0, curl http/https codes 0 |
| T3 | Drive (constat § 8.4) | 3 codes curl 0, jeton + session extraits, journal téléversé |

Un test KO n'arrête pas les suivants : le journal embarque les preuves
brutes (journal démo intégralement recopié, flux console proxy intégralement
recopié) — le § 8.4 (constat terrain normé) reçoit l'intégralité, pas un
résumé.

## Table des blocs (cible x86-64-win11-pe, generation 5, f6xxxx)

| Bloc | Spec | Slot | Taille | Rôle |
|---|---|---|---|---|
| f60001 | sup-01:R1 | 0x1400 | 0x40 | principal — horodatage puis fenêtre puis boucle |
| f60002 | sup-02:R1 | 0x1440 | 0x180 | fenêtre « TRIADE superviseur terrain » |
| d40003 | win-03:R1 | 0x15C0 | 0x80 | pompe de messages (réutilisation R7) |
| d40004 | win-04:R4 | 0x1640 | 0x380 | procédure (réutilisation R7 — clic unique) |
| d40006 | win-06:R1 | 0x1AC0 | 0x180 | porte R10 + libc (réutilisation R7) |
| f60021 | sup-21:R1 | 0x1C40 | 0x100 | horodatage (nom du run + ligne S01) |
| f60022 | sup-22:R1 | 0x1D40 | 0xC0 | balayeur étiquette->valeur (pur) |
| f60011 | sup-11:R1 | 0x1E00 | 0x200 | journal fichier horodaté (contrat win-11:R1) |
| c30006 | tcp-06:R1 | 0x4300 | 0x40 | CreateThread (réutilisation R7) |
| f60009 | sup-09:R1 | 0x4C00 | 0x200 | scénario : porte, libc, T1, T2, T3, verdict |
| f60036 | sup-36:R1 | 0x4E00 | 0x1C0 | fichiers (lire/écrire/supprimer, préfixe répertoire, cache DIR_LONG) |
| d40005 | win-05:R3 | 0x5000 | 0x200 | miroir écran + fichier (réutilisation R7) |
| f60031 | sup-31:R1 | 0x5200 | 0x1C0 | lanceur de processus (CreateProcessA + tuyaux) |
| f60033 | sup-33:R1 | 0x5400 | 0x3C0 | test T1 — démo M2 |
| f60034 | sup-34:R1 | 0x5800 | 0x5C0 | test T2 — proxy M3 |
| f60035 | sup-35:R1 | 0x5E00 | 0x4C0 | test T3 — envoi Drive |

Héritage byte-identique (R7, preuve contre les artefacts scellés) :
a10002/a10003 (io M0, hello.exe), b20001-04 (libc M1, selftest.exe),
c30006 (tcp-06, echo.exe), d40003/d40004/d40005/d40006 (lignée démo,
demo.exe 0.3.0-demo.9). Neuf blocs nouveaux.

## Chartre des contrats renforcés (liée par renvoi à la charte m3/I)

1. **Zéro gel** : toute attente est un événement borné (PeekNamedPipe,
   WaitForSingleObject, SendMessageTimeoutW, sondage de marqueur) — le
   superviseur ne peut jamais se bloquer sans rendre son verdict.
2. **Zéro fuite** : tout handle créé est fermé sur TOUT chemin, y compris
   d'échec (vérifié par l'oracle : liste des CloseHandle observés).
3. **Zéro secret au journal** : le journal embarqué ne contient pas un
   octet des champs de terrain_jetons.bin (interdit 11).
4. **Le journal est la preuve** : chaque verdict s'appuie sur un memcmp
   exact ; les contenus testés (journal démo, flux proxy) sont embarqués
   bruts — une ligne présente = une étape prouvée.
5. **Dépendance OS assumée** : curl.exe (schannel) pour HTTPS, comme
   ws2_32 pour TCP — la frontière mécanique vit dans le process/IAT, le
   superviseur ne contient NI TLS NI HTTP.
6. **Un run = un nom** : terrain_YYYYMMDD_HHMMSS.txt — les constats
   s'accumulent dans le dossier Drive sans jamais s'écraser.
7. **La porte R10 précède tout** (R10) : image invalide = arrêt avant
   tout effet, aucun test lancé.
8. **Ordre séquentiel T1->T2->T3** : le port 25000 est partagé (démo,
   proxy) et l'envoi vient en dernier (journal complet).

## Réutilisation R7 (adresses stables, octets identiques)

| Réutilisé | Depuis | À l'adresse | Condition |
|---|---|---|---|
| io write/exit | hello.exe | 0x1040/0x1080 | inchangé |
| libc memcpy/memcmp/strlen/itoa | selftest.exe | 0x1100-0x12FF | inchangé |
| tcp-06 spawn | echo.exe | 0x4300 | inchangé |
| win-03 boucle | demo.exe | 0x15C0 | inchangé |
| win-04 procédure | demo.exe | 0x1640 | TXT_BOUTON "TOUT DÉMARRER" @0x2A1E, EDIT @0x2A3A, BUTTON @0x2A44, VIDE @0x2A52, scénario @0x4C00, traces L* aux adresses démo |
| win-05 miroir | demo.exe | 0x5000 | BUF_MIROIR @0x3A50, HWND_JOURNAL @0x3868, relais queue jmp 0x1E00 (sup-11 honore le contrat) |
| win-06 autotest | demo.exe | 0x1AC0 | table R10 @0x2450 (18 entrées terrain), version @0x2628 (u64 0x00050101 >= plancher 0x30000 embarqué), ancre @0x2620, fixtures @0x2630-0x265A |

## Zones préfigurées du plan

- .text 0x1400-0x1FFF : coquille + horodatage + balayeur + journal ;
- .text2 0x4000-0x63FF : tcp-06 @0x4300, zone données sup 0x4340-0x4BFF
  (chaînes S*/URL/gabarits/étiquettes — RX, lisible, hors pages de code
  testé), scénario @0x4C00, win-05 @0x5000, lanceur 0x5200, T1/T2/T3
  0x5400/0x5800/0x5C00, zone données sup 2 0x6000-0x63FF (INT/hints
  kernel32#3/user32#2 + compléments) ;
- .data 0x3800-0x3FFF : état hérité (hwnds, drapeaux, journal) + état
  terrain (TAMPON_NOM 0x3AD0, TAMPON_AFF 0x3AF0, ETAT_SUP 0x3B10,
  TAMPON_JETON 0x3B70, TAMPON_CMD 0x3D50).

## Surface de test de l'oracle

- différentiel : sup-22 (10 000 cas contraints, référence Python) ;
- comportemental : sup-21 (horloge fixée), sup-11 (7 vecteurs win-11
  transposés), coquille GUI (entrée complète : L00/L02/L4C/L4D/L01,
  clic unique), scénario nominal COMPLET (journal d'or écran + fichier,
  spawn/pipe/findwindow scriptés), 5 scénarios d'échec (démo absente,
  journal non conforme, curl KO, jetons absents, réponse OAuth muette) ;
- falsification : octets de bloc corrompus -> porte R10 (boucle sur les
  15 blocs embarqués), 5 mutations ciblées (constante 17, longueur
  d'étiquette, ordre T1/T2/T3, nettoyage, timeout d'arrêt).
