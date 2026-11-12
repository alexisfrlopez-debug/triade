# shani · LA VARIANTE SHA-NI DE LA FAMILLE SHA · registre du domaine

> Trois blocs — la sonde, la compression, l'absorption à dispatch. NÉS DU
> PAQUET 6/6 de la vague 3 (l'instruction lfh49a1xf, D205), JAMAIS SCELLÉS :
> la cérémonie d'ère et le run terrain appartiennent au développeur ; l'arbre
> signé n'est pas touché. Les blocs vivent en COPIES DE LABORATOIRE aux
> adresses du plan (`shani/layout.py`) jusqu'au geste du développeur.

## Pourquoi cette famille existe — le dossier R11 en trois pièces

1. **LA MESURE AVANT TOUT** (R11 à la lettre) : le hachage de fichiers
   volumineux instrumenté DANS LE HARNAIS LOUPE —
   `scripts/preuves_v150/hotpath_shani/mesure_hotpath.txt`, consigné AVANT le
   premier octet de la variante : **tls13-02 (la compression d'un bloc de
   64 o) = 98,11 % des instructions exécutées** (64 Kio : 4 489 500/4 575 760 ;
   256 Kio : 17 944 860/18 289 327 — chaque condensé VÉRIFIÉ à hashlib avant
   le verdict). Le hot path est CONFIRMÉ PAR MESURE ; toute optimisation du
   hachage vise la compression, NI un autre périmètre NI un découpage partiel.
2. **LES SÉMANTIQUES ÉPINGLÉES PAR LE CODE** (le juge est le code, jamais la
   documentation lue sur parole) : `scripts/experience_semantique_shani.py`
   (les hypothèses rnds2/msg1/msg2 tranchées sur le CPU SHA-NI natif du
   laboratoire contre la référence FIPS en Python pur) et
   `scripts/epreuve_compression_shani.py` (la structure ENTIÈRE à la main :
   100/100 contre le juge Python, les QUATRE vecteurs FIPS 180-4 § 6.3.1
   verts, le corpus aux bords vert — l'épreuve VÉCUE AVANT la notation, le
   miroir de la contre-preuve AES tls13-15/16).
3. **LA MESURE APRÈS** : l'entrée OPT-01 du journal d'optimisation porte les
   mesures avant/après au laboratoire (compositions COMPLÈTES
   init+absorb+final, condensé vérifié avant comptage) ; le kit terrain
   `shani/terrain/` porte la mesure du DÉVELOPPEUR sur SA machine (avant =
   la composition scellée ; après = la variante telle que dispatchée — mêmes
   conditions, même entrée, jamais un périmètre partiel).

## La charte de la famille (trois règles, miroir des chartes M9)

- **§ 1 — LE CONTRAT EST CELUI DU SCELLÉ (R4)** : shani-02 porte EXACTEMENT le
  contrat de tls13-02, shani-03 EXACTEMENT celui de tls13-03 — mêmes
  signatures, mêmes pré/post, mêmes invariants de comportement. La variante
  est un REMPLAÇANT possible au site d'appel de la compression, jamais une
  refonte : la disposition du contexte (H[8] u32 @ +0, tampon @ +32,
  remplissage @ +96, total @ +104), la sémantique FIPS, les verdicts — tout
  ce que le scellé publie demeure.
- **§ 2 — LE REPLI VIT SUR LE SCELLÉ (R7)** : le chemin scalaire de la
  variante APPELLE tls13-02 À SON ADRESSE SCELLÉE 0xC080 (le plan loupe,
  source unique importé par chemin nominatif) — les adresses scellées sont
  intactes, la variante n'y touche pas ; la table K @0x2F00 et les blocs
  tls13-01/03/04 demeurent LES blocs de la composition : seule la
  compression est dispatchée.
- **§ 3 — AUCUN SCELLAGE AU LABORATOIRE** : les notations vivent à
  `notation/` générées par `outils/auteur.py` (keystone assemble, rien
  d'autre), les blocs ne sont PAS dans la carte, la cérémonie d'ère
  appartiendra au développeur, et l'arbre signé sceau-I n'est pas touché.

## Le registre figé

| Bloc | Spec | Rôle | État |
|---|---|---|---|
| shani-01 | `shani-01-sonde.md` | la sonde CPUID (SHA-Ni ∧ SSSE3) | notée, vérifiée au laboratoire, JAMAIS scellée |
| shani-02 | `shani-02-comprimer.md` | la compression SHA-NI d'un bloc de 64 o | notée, vérifiée au laboratoire, JAMAIS scellée |
| shani-03 | `shani-03-absorber.md` | l'absorption tamponnée à dispatch | notée, vérifiée au laboratoire, JAMAIS scellée |

La composition complète du hachage d'une gamme : tls13-01 (le scellé,
l'initialisation) → shani-03 (la variante, l'absorption dispatchée) →
tls13-04 (le scellé, la finalisation) — les opérations COMPLÈTES
init+absorb+final, jamais un périmètre partiel (l'exigence de la mesure
comme celle du kit).
