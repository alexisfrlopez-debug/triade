# Couche I — jalon M0 (hello)

Trois spécifications, écrites avant la notation (R2, provenance `écrite-avant-code`).
Elles instancient le gabarit § 2.2 de la spécification v0.4.0.

Registre des domaines du projet (figé, § 2.1) — l'outil de validation TRIADE :
`hello` (M0), `libc` (M1), `tcp` (M2), `http` (M3), `tls` (M4), `outil` (M5),
`sys` (M8), `tls13` (M9), `notation`, `carte`, `crypto`, `securite`. Un
identifiant n'est jamais réutilisé.

| Spécification | Bloc machine (carte) | Rôle |
|---|---|---|
| hello-01:R1 | a10001 | Point d'entrée : orchestration |
| hello-02:R1 | a10002 | Écriture stdout via WriteFile |
| hello-03:R1 | a10003 | Sortie propre via ExitProcess |

Le profil d'instanciation est `x86-64-win11-pe` (profil primaire, D10/D14) :
ABI msx64, IAT kernel32 (D7), granularité et padding D8, adresses stables R7.
