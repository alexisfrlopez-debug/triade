# Couche I — jalon M2 (serveur TCP écho, patch à chaud)

Treize spécifications nouvelles, écrites avant la notation (R2, provenance
`écrite-avant-code`). Elles instancient le gabarit § 2.2 de la spécification
v0.4.0 et étendent le registre figé du projet (m0/I/README.md, § 2.1) dans le
domaine **`tcp`, réservé M2** — aucun domaine nouveau n'est créé ; l'extension
`libc-09` prolonge le domaine libc dans la réserve prévue à cet effet
(m1/layout.py : « réserve int3 pour libc-09+ »).

| Spécification | Bloc machine (carte) | Rôle | Zone |
|---|---|---|---|
| tcp-01:R1 | c30001 | Initialisation serveur (WSAStartup, socket, bind, listen) | net @ 0x4000 |
| tcp-02:R1 | c30002 | Acceptation d'une connexion | net @ 0x4100 |
| tcp-03:R1 | c30003 | Réception (recv) | net @ 0x4140 |
| tcp-04:R1 | c30004 | Émission (send) | net @ 0x4180 |
| tcp-05:R1 | c30005 | Fermeture de socket | net @ 0x41C0 |
| tcp-06:R1 | c30006 | Lancement de thread (CreateThread) | thr @ 0x4300 |
| tcp-07:R1 | c30007 | Moteur de patch à chaud (bascule echo, rollback) | tramp @ 0x4400 |
| tcp-08:R1 | c30008 | Écho v1 — transformation identité (CIBLE du patch) | echo @ 0x4600 |
| tcp-08:R2 | c30014 | Écho v2 — transformation majuscules (REMPLAÇANT, staging) | echo @ 0x4680 (croissance) |
| tcp-09:R1 | c30009 | Thread par connexion (boucle recv/écho/send) | srv @ 0x4800 |
| tcp-10:R1 | c30010 | Thread console (patch / rollback / quit) | srv @ 0x4980 |
| tcp-11:R1 | c30011 | Ligne de journal console (sérialisée) | srv @ 0x4B00 |
| tcp-12:R1 | c30013 | Orchestration serveur — point d'entrée echo.exe | app @ 0x1800 |
| libc-09:R1 | c30012 | Allocateur par zone thread-safe (section critique) | libc @ 0x1440 (réserve) |

Blocs réutilisés de M0/M1 dans echo.exe (R7, octets identiques aux artefacts
scellés) :

| Spécification | Bloc | Rôle | Zone |
|---|---|---|---|
| hello-02:R1 | a10002 | Écriture stdout via WriteFile | io @ 0x1040 |
| hello-03:R1 | a10003 | Sortie propre via ExitProcess | io @ 0x1080 |
| libc-01:R1 | b20001 | Copie mémoire (memcpy) | libc @ 0x1100 |
| libc-02:R1 | b20002 | Comparaison normalisée (memcmp) | libc @ 0x1180 |
| libc-03:R1 | b20003 | Longueur de chaîne (strlen) | libc @ 0x1200 |
| libc-04:R1 | b20004 | Conversion décimale u32 (itoa) | libc @ 0x1280 |

Les blocs libc-05/06/07 (zone_alloc, zone_reset, memset) et a10001 restent
indexés par la carte génération 2 mais ne sont pas embarqués dans echo.exe
(aucun appelant — la discipline M2 est la composition sur pile privée, voir
libc-09 pour l'analyse de l'arène multi-thread). Le profil d'instanciation est
`x86-64-win11-pe` : ABI msx64, IAT kernel32 + ws2_32 (D7), granularité et
padding D8, adresses stables R7, zones D28 étendues par D33 (.text2 :
net/thr/tramp/echo/srv).

Cycle de vie durant le jalon : tcp-08 naît à R1 (dev.1, transformation identité,
staging vide) puis est révisée en R2 (dev.2) par la boucle de mise à jour § 5 —
le remplaçant (majuscules) est le premier bloc de l'histoire du projet livré
en staging, activé à chaud par trampoline ; tous les autres identifiants
naissent et restent à R1.
