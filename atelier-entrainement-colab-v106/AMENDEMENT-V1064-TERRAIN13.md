# AMENDEMENT-V1064 — LE TERRAIN.13 : LE MONSTRE NOMMÉ REFUSÉ À SA SECONDE VISITE, LE REPLI NOMMÉ DU PLAN § 7

> L'amendement à la suite des terrains 11/12 — le plan DEMEURE BYTE-BYTE (sha256
> 8a719580746811db0a40a9f4d4e805c4b0ac245e1ac6f67de8c0845a4a27f3d7,
> consigné à l'Entrée 458) ; la présente nomme la mesure du TROISIÈME refus
> du 28/11 (la v1063, le processus CUDA-vierge) et LE REPLI que le plan § 7
> nommait depuis l'origine — l'exclusion nommée, décidée AU LABO avec la
> mesure, jamais au bord. Le treizième terrain de la voie Colab, à la suite
> des terrains 1-12.

## 1. LA MESURE (le troisième run du maître, 28/11 — la cane verte, l'époque 1 ENTIÈRE tenue)

Le run courut sur un processus CUDA-vierge (la cane VERTE au journal —
l'allocateur NÉ sous expandable_segments, le refus NOYAU-SALE jamais levé) ;
la marche a tenu l'époque 1 ENTIÈRE — 17 pas sur 17, le monstre AU PAS 1
compris — puis refusa à LA SECONDE VISITE du monstre :

    torch.OutOfMemoryError: Tried to allocate 456.00 MiB.
    GPU 0 has a total capacity of 14.56 GiB of which 253.81 MiB is free.
    Of the allocated memory 13.02 GiB is allocated by PyTorch, and
    1.16 GiB is reserved by PyTorch but unallocated.
    EXEMPLE-LONG-OOM : le T4 n'a pas tenu l'exemple ajouter-v3-i26111705-t1
    (12615 jetons, le pic 13.58 Gio)

LE JOURNAL VÉCU (le pic mesuré à chaque pas — la mesure du terrain.12) :
pas 4 · pic 9.24 Gio (l'exemple à 6 766 jetons) · pas 8 · 8.39 · pas 12 ·
7.98 · pas 16 · 7.62 — les pics DÉCROISSANTS, l'ordre des longs d'abord
tenu ; les pas 1-3 (les trois monstres 12 615 / 12 021 / 12 019) ne se
loggent pas (le journal parle tous les 4 pas) — ILS ONT TENU : le pas 17
(le plus court, 3 351) tient sans log ; LE PAS 18 = ajouter-v3-i26111705-t1
ENCORE (l'époque 2 le remet en tête — les longs d'abord), et là le refus.

LES TROIS FAITS DÉCOMPOSÉS :

1. **LE REMÈDE DU TERRAIN.12 A MORDU, LES TROIS PRONGS.** La cane verte
   (le processus vierge, l'allocateur élastique né) ; L'AUTOCAST fp16 A
   MORDU — le tampon refusé de 456,00 MiB est LE [12 615 × 18 944] fp16
   (455,82 Mio calculés — l'arrondi de l'allocateur, la classe déjà nommée
   au terrain.12 : « 456 Mio la pièce »), LA MOITIÉ EXACTE du pied fp32 de
   912 MiB du second refus : PLUS AUCUN [S × 18 944] fp32 ne vit au chemin
   LoRA ; l'hygiène + la mesure vécue (empty_cache par exemple, le pic_gio
   à chaque pas — le refus porte SA mesure : 13.58 Gio).
2. **LE PERSISTANT DE L'OPTIMISEUR — l'écart du budget du terrain.12,
   l'écart du labo seul, NOMMÉ.** Le budget du terrain.12 comptait le
   modèle, les bornes de checkpoint, les logits, les tronçons et les
   transitoires — PAS L'ÉTAT ADAMW (2 × 40 370 176 × 4 octets ≈ 0,31 Gio,
   né au premier pas d'optimiseur, après le pas 4) NI LES GRADIENTS
   ACCUMULÉS (≈ 0,15 Gio). À la 1re visite du monstre le bassin portait
   ≈ 5,6 Gio de persistant ; à la seconde ≈ 6,1 — et le pas du monstre
   exige ≈ 8,4 Gio au-delà du persistant : LE PIC COMPLET ≈ 14,0-14,3 Gio
   contre ≈ 14,43 disponibles (14,56 moins le contexte ≈ 0,13). LA MARGE
   ~0,1-0,4 Gio — mangée par la fragmentation du bassin (1,16 Gio
   réservés-non-alloués, AUCUN bloc contigu de 456 MiB, l'expansion du
   segment impossible : 253,81 MiB libres côté device).
3. **LE MONSTRE NE TIENT QUE SUR UN BASSIN VIERGE — ET LA MARCHE LE
   REVISITE.** Au pas 1 (bassin vierge, sans état) le même pas tenait avec
   ~0,9 Gio de marge ; au pas 18 l'état de l'optimiseur — que la marche
   porte désormais pour toujours — a mangé la marge. Or le plan § 3
   (3 époques) revisite le monstre DEUX FOIS ENCORE (pas 18, pas 35) : un
   exemple qui tient à la première visite et refuse à la seconde n'est pas
   ENTRAÎNABLE à la marche du plan. LA MATHÉMATIQUE EST CONFIRMÉE : le
   budget du terrain.12 (12,8-13,3 Gio) fut tenu à l'époque 1 ; le corpus,
   la perte, l'ordre, le signal — RIEN ne divergea. Le refus est de
   CAPACITÉ PERSISTANTE, pas de loi.

## 2. LE GESTE — LE REPLI NOMMÉ DU PLAN § 7 (l'exclusion nommée, AU LABO)

1. **L'EXCLUSION DE ajouter-v3-i26111705-t1 SEUL — LE NOMMÉ.** Le plus
   long exemple (12 615 = P 8 293 + C 4 322), refusé au pas 18 avec SA
   MESURE (pic 13.58 Gio, 456,00 MiB refusés). t3/t2 (12 021 / 12 019) :
   TENUS à leur 1re visite (les pas 2-3 du run), JAMAIS nommés par la
   mesure — le labo n'exclut pas ce que la mesure n'a pas refusé (le
   principe des terrains 11/12 : l'exclusion large eût tué la loi des
   recettes quand la mesure nommait un autre remède ; aujourd'hui le
   remède a MORDU et la mesure nomme UN refus — l'exclusion est le nommé
   seul).
2. **LE REPLI VIT À LA CELLULE 5, PAR NOM, FAIL-CLOSED.** Le corpus
   FICHIER demeure BYTE-BYTE (sha256 39614077… INCHANGÉ — l'exclusion ne
   touche JAMAIS le fichier : le gate recoupe les 17 verts du corpus, la
   cellule en retient 16, le repli nommé au journal même du bord).
   EXCLUSION-NOMMÉE-DIVERGENTE le refus si le nommé manque au corpus — le
   repli ne peut pas silencieusement ne rien faire.
3. **L'ORDRE ET LA GARDE INCHANGÉS.** La clé du plan § 3 (les longs
   d'abord) court PARMI LES RETENUS — t3 en tête à 12 021, le plus court
   3 351 en queue ; la garde EXEMPLE-TROP-LONG demeure (le max retenu
   12 021 ≤ 13 000).
4. **LA MARCHE : 3 × 16 = 48 PAS, 12 PAS D'OPTIMISEUR EXACTS.** 48 % 4 = 0
   — les 3 micro-pas orphelins du 51 (les pas 49-51, accumulés jamais
   stepés) disparaissent : la marche tombe RONDE. L'HORLOGE IDENTIQUE :
   opt_pas 12 au 48-pas comme au 51-pas, l'échauffement 1 (5 % de 12), la
   cosine ÉGALE pas à pas — prouvé au bac.

## 3. LA PREUVE AU LABO (le bac, torch 2.15.0+cpu, transformers 5.24.1 — le tokenizer réel)

La passe repli-0 (preuve-terrain13-repli-0.json) :

- le corpus recoupé BYTE-BYTE (sha 39614077… : 78 triples, 17 verts) ;
- la RE-MESURE au tokenizer réel (l'enveloppe du moteur, la pièce vivante)
  recoupant le tableau consigné de l'Entrée 462 — 17/17 byte-byte ;
- LE REPLI REJOUÉ : l'exclusion retire exactement le nommé (16 retenus) ;
  le fail-closed éprouvé (un nom absent = le refus
  EXCLUSION-NOMMÉE-DIVERGENTE) ;
- L'ORDRE des 16 = l'ordre des 17 privé du premier (l'égalité des listes,
  preuve par construction : le nommé était le max strict) ;
- LA MARCHE ET L'HORLOGE construites au bac : 48 pas / 12 pas
  d'optimiseur, les 12 lr ÉGAUX pas à pas au 51-pas du plan ;
- LES TOTAUX : P 78 343 → 70 050 · C 20 906 → 16 584 (l'exclu portait
  P 8 293 + C 4 322) · le max retenu 12 021 · le min 3 351 · la médiane
  4 379,5 (4 527 aux 17).

LA PERTE D'UN PAS D'UN SURVIVANT : BIT-IDENTIQUE PAR CONSTRUCTION — le
repli ne touche NI la tokenisation, NI l'enveloppe, NI la perte, NI
l'accumulation ; les pas des 16 survivants exécutent LE MÊME code sur LES
MÊMES tenseurs (le terrain.11/12 demeure LA LOI de la cellule).

LE RISQUE NOMMÉ (l'honnêteté d'abord, à la manière du § 6) : t3/t2
(12 021 / 12 019) à leur 2e/3e visite — 594 jetons plus courts que le
nommé (−4,7 %), la pente ∝ L (les bornes de checkpoint 1,87e-4 Gio/jeton
+ les tampons MLP 3,53e-5 Gio/jeton par pièce) rend ~0,15 Gio au pic.
L'ESTIMATION NOMMÉE ESTIMATION : la mesure ne les a JAMAIS nommés. SI le
terrain les refuse, le refus nommé reviendra AU LABO avec le pic mesuré —
jamais au bord (le protocole même du § 7, tenu aux terrains 11/12/13).

## 4. CE QUI NE CHANGE PAS (le plan demeure LA LOI)

- LE CORPUS BYTE-BYTE (train.jsonl sha256
  39614077e5c6d9feb94eb528ae19d9f948d67c531a2ac26daa17229023bb3eb7) :
  AUCUNE exclusion au FICHIER, AUCUNE troncature — l'exclusion vit à la
  cellule, le repli nommé du § 7 ;
- LES HYPERPARAMÈTRES DU § 3 : r16 α32 dropout 0,05 aux sept projections,
  lr 1,5e-5 cosine + échauffement 5 %, 3 époques (48 pas, 12 pas
  d'optimiseur), batch 1 × accumulation 4, clip 1,0, graine 20261128,
  max_len 13 000, NF4 double quantification fp16, l'ordre des longs
  d'abord (parmi les retenus), l'enveloppe VERBATIM ;
- LA PERTE : sur LA RÉPONSE SEULE, logits_to_keep + les tronçons de 1024
  INCHANGÉS ; l'autocast fp16 du terrain.12 INCHANGÉ (le tampon refusé au
  pas 18 en porte la marque : 456 MiB fp16, jamais 912 fp32) ; la cane
  NOYAU-SALE et l'hygiène INCHANGÉES ;
- LE POST-ENTRAÎNEMENT (§ 4), L'ÉVAL (§ 5), LES GAPS (§ 6), LES GARDES
  (§ 7 — EXEMPLE-TROP-LONG et EXEMPLE-LONG-OOM demeurent les refus nommés,
  le second portant sa mesure ; EXCLUSION-NOMMÉE-DIVERGENTE la garde
  nouvelle du repli) ;
- LA LOI DES COPIES (§ 8) : la vive au /livrables, l'aveugle au dépôt.

## 5. LE REGISTRE (la cellule 5 le porte)

Le champ « amendement » s'étend (terrain.11 + terrain.12 + terrain.13 —
le repli consigné) ; le champ « donnees » porte les 16 retenus, les
totaux recalculés (P 70 050 · C 16 584 · exemple_max 12 021) et
l'exclusion nommée au registre même ; la courbe demeure (le pic_gio à
chaque pas). Le reste des champs inchangé.
