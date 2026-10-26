# Couche I — jalon M1 (libc)

Huit spécifications, écrites avant la notation (R2, provenance `écrite-avant-code`).
Elles instancient le gabarit § 2.2 de la spécification v0.4.0 et étendent le
registre figé du projet (m0/I/README.md, § 2.1 — domaine `libc`, réservé M1).

| Spécification | Bloc machine (carte) | Rôle | Zone |
|---|---|---|---|
| libc-01:R1 | b20001 | Copie mémoire (memcpy) | libc @ 0x1100 |
| libc-02:R1 | b20002 | Comparaison normalisée (memcmp) | libc @ 0x1180 |
| libc-03:R1 | b20003 | Longueur de chaîne (strlen) | libc @ 0x1200 |
| libc-04:R1→R2 | b20004 | Conversion décimale u32 (itoa) | libc @ 0x1280 |
| libc-05:R1 | b20005 | Allocateur par zone | libc @ 0x1300 |
| libc-06:R1 | b20006 | Réinitialisation de zone | libc @ 0x1380 |
| libc-07:R1 | b20007 | Remplissage mémoire (memset) | libc @ 0x13C0 (réserve, dev.2) |
| libc-08:R1→R2 | b20008 | Auto-test (point d'entrée selftest.exe) | app @ 0x1800 |

Blocs réutilisés de M0 (R7, octets identiques à hello.exe) :

| Spécification | Bloc machine (carte) | Rôle | Zone |
|---|---|---|---|
| hello-02:R1 | a10002 | Écriture stdout via WriteFile | io @ 0x1040 |
| hello-03:R1 | a10003 | Sortie propre via ExitProcess | io @ 0x1080 |

Le bloc a10001 (hello-01:R1, hello.exe @ 0x1000) reste indexé par la carte
projet mais n'est pas embarqué dans selftest.exe. Le profil d'instanciation est
`x86-64-win11-pe` (profil primaire, D10/D14) : ABI msx64, IAT kernel32 (D7),
granularité et padding D8, adresses stables R7, zones d'adressage D28.

Cycle de vie durant le jalon (§ 2.3) : libc-04 passe de R1 à R2 AVANT scellage
(l'oracle différentiel a démontré que « aucun octet écrit au-delà du NUL » est
irréalisable pour une génération en place — R2 borne le tampon à douze octets
et déclare l'espace au-delà du NUL non spécifié) ; libc-08 passe de R1
(18 vecteurs, dev.1) à R2 (21 vecteurs avec memset, dev.2) — la révision
s'incrémente car le contrat d'auto-test s'étend ; tous les autres identifiants
naissent et restent à R1.
