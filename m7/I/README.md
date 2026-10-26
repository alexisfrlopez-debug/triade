# m7/I — Couche I du vérificateur sceau (D34, échelon 2)

Spécifications d'intention du domaine `av` (authentification-vérifiée),
profil x86-64-linux-elf64, lignée auto-hôte. L'artefact `sceau` vérifie les
signatures Ed25519 (RFC 8032) des cartes du projet en code machine nu :
l'échelon 2 de l'échelle d'auto-hébergement — hachage (hachoir, échelon 1)
et signature vérifiés par des blocs TRIADE.

## Familles

- av-01..04 — SHA-512 (FIPS 180-4 § 4.6) : le moteur de hachage d'Ed25519.
  Contexte partagé 256 o : H[8] u64 @ +0, tampon[128] @ +64, remplissage
  u32 @ +192, total u64 @ +200.
- av-05..11 — corps f25519 (p = 2^255 − 19), radix 2^51, 5 membres u64.
  Représentation « limbs » : membres < 2^52, valeur ≡ x mod p ; les blocs
  arithmétiques (add, sub, mul) sortent une valeur RÉDUITE (< p) — l'invariant
  est maintenu par propager + freeze.
- av-12..15 — edwards25519 projective (X:Y:Z), addition unifiée complète
  (le neutre est (0:1:1) — courbe complète, Z nul impossible par
  construction : c'est l'avantage d'Edwards sur Weierstrass).
- av-16..17 — vérification RFC 8032 (v-verifier, sans E/S) et orchestration
  CLI (principal : mode `--hacher` diagnostic + mode vérification).

## Héritages m6 (octet-identiques, mêmes adresses)

ah-01-ecrire (d40001), ah-03-sortir (d40003), ah-08-hex (d40008 — son
déplacement RIP vise R_HEXCHARS @ 0x2100, intangible). ah-02-lire n'est pas
embarqué : le principal lit par read direct (I1, miroir de ah-09).

## Convention d'appel (ABI SysV, miroir hachoir)

Arguments en rdi, rsi, rdx, rcx ; retours en rax. Pile 16-alignée aux
points d'appel ; appels directs entre blocs déclarés en I1 de chaque spec ;
numéros de syscall déclarés par bloc ; données RIP déclarées par bloc.

## Phases de notation (croissance R7)

- dev.1 : av-01..04, av-17 (mode `--hacher` opérationnel, mode vérification
  en échec explicite « en chantier »), héritages. Notation de av-05..16 en
  chantier — les specs sont POSÉES (R2), la construction les audit et
  l'attend.
- dev.2+ : corps f25519, courbe, vérification (révisions des blocs touchés).
