# KIT TERRAIN SHA-NI — LA MESURE AVANT/APRÈS SUR VOTRE MACHINE (D205)

> Le paquet 6/6 de la vague 3 (l'instruction `lfh49a1xf`) : la variante de
> profil sha256 par les instructions SHA-NI du processeur — **mesurée au
> laboratoire (gain 5,84×, le rapport `preuves_v150/shani/`) — le présent
> kit porte LA MESURE TERRAIN qui vous appartient**. Aucun scellage n'a eu
> lieu : la cérémonie d'ère et la décision d'embarquer la variante sont
> les vôtres ; l'arbre signé sceau-I n'a pas été touché (garde 14/14).

## Ce que le kit porte

| Pièce | Rôle |
|---|---|
| `image-shani.bin` | l'image de laboratoire (48 Kio, plage RVA 0x2000-0xE000) : la table K **du scellé**, le masque BE, la famille sha **scellée** extraite de `loupe.exe` à ses RVA d'origine (le repli, R7), et les TROIS blocs de la variante (les notations assemblées). sha256 au `manifeste-kit-shani.txt` — le scénario la recoupe AVANT toute exécution |
| `scenario-shani.py` | le scénario : il alloue la mémoire exécutable, pose l'image, vérifie les vecteurs FIPS aux deux bras, PUIS mesure — écrivant `temoin-shani.txt` |
| `manifeste-kit-shani.txt` | les empreintes et les provenances de chaque plage de l'image |

## Le geste du développeur (cinq minutes)

1. Copiez les TROIS fichiers du kit dans un répertoire vide de votre
   machine Windows 11 (ou Linux — le scénario est bifteau : sous Windows
   il appelle msx64 directement, ailleurs par trampoline).
2. `python3 scenario-shani.py` (ou `python scenario-shani.py`).
3. Le scénario écrit **`temoin-shani.txt`** — renvoyez-le au labo.

Rien d'autre. Le scénario ne touche à AUCUN fichier hors son répertoire ;
il ne modifie JAMAIS vos pièces scellées (l'image du kit est une pièce de
laboratoire autonome — la sonde « neutralisée » du repli forcé vit dans
SA copie, jamais dans un scellé).

## La discipline de la mesure (l'exigence de l'instruction, à la lettre)

- **la MÊME machine** : la vôtre, du début à la fin ;
- **la MÊME entrée** : 8 Mio de PRNG déterministe (graine 20261112) —
  bit-identiques par construction, les DEUX bras sur les MÊMES octets ;
- **le condensé VÉRIFIÉ avant comptage** : le scénario vérifie chaque
  condensé à `hashlib` AVANT la première mesure — et CHAQUE répétition
  re-vérifie (une répétition au condensé faux ABORTE : aucun chiffre
  n'est jamais compté sur un hachage faux) ;
- **les opérations COMPLÈTES** `init+absorb+final` — jamais un périmètre
  partiel : chaque bras hache le tampon ENTIER de bout en bout ;
- **les TROIS bras** : l'avant (la composition scellée tls13-01/03/04 —
  les octets que vos onze runs ont vécus), l'après (la variante telle
  que dispatchée par VOTRE processeur), et le repli forcé (la sonde
  neutralisée en copie de laboratoire — le chemin scalaire de la
  variante, mesuré pour nommer la surcharge du dispatch) ;
- **15 répétitions par bras**, médianes et IQR en cycles RDTSC
  (`lfence ; rdtsc`).

## Comment lire le témoin

- `la sonde : rax = 1` — votre processeur a SHA-NI et SSSE3 : l'après
  vivra le chemin matériel. `rax = 0` — le repli scalaire (la variante
  ne vous apportera rien : le témoin le dira, la décision d'embarquer
  n'en vaudra pas la peine — c'est une réponse honnête, pas un échec).
- `LE GAIN : N,NN×` — le rapport médian avant/après sur VOTRE machine.
  Au laboratoire (mesuré le 12/11) : **5,84×** (13,60 → 2,32 cycles/o).
- `la surcharge : +N,NN %` — ce que coûte le dispatch (sonde+branche)
  quand il retombe sur le chemin scellé : au labo **+0,15 %** — le prix
  du billet, pas celui du voyage.

## Ce que le kit n'est PAS

- Il n'est PAS un scellage : aucune carte, aucune cérémonie, aucune
  balise — embarquer la variante dans un futur build `loupe` exige la
  cérémonie d'ère (le sceau-I, la clé hors-ligne, le geste du maître).
- Il ne mesure PAS un périmètre partiel : jamais la compression seule,
  jamais « sans la finalisation » — les trois opérations, toujours.
- Il ne fabrique AUCUN chiffre : tout nombre du témoin est mesuré sur
  votre machine ou vérifié à `hashlib` avant d'être écrit.
