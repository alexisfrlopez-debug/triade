# AMENDEMENT-V1063 — LE TERRAIN.12 : LE CHEMIN FP32 DE PEFT ET L'ALLOCATEUR NÉ SALE

> L'amendement à la suite du terrain.11 — le plan DEMEURE BYTE-BYTE (sha256
> 8a719580746811db0a40a9f4d4e805c4b0ac245e1ac6f67de8c0845a4a27f3d7,
> consigné à l'Entrée 458) ; la présente nomme l'écart MESURÉ au second run
> du maître du 28/11 (la v1062, l'amendement terrain.11 porté) et le geste
> qui le soigne SANS toucher aucune loi du plan. Le douzième terrain de la
> voie Colab, à la suite des terrains 1-11.

## 1. LA MESURE (le second run du maître, 28/11, le navigateur)

La v1062 refusa AU PREMIER exemple encore (ajouter-v3-i26111705-t1,
12 615 jetons — l'ordre du plan § 3 : les longs d'abord) — MAIS À UN AUTRE
ENDROIT, la marque que le remède du terrain.11 a MORDU (les 7,15 GiB des
logits pleins ne furent plus jamais demandés) :

    torch.OutOfMemoryError: Tried to allocate 912.00 MiB.
    GPU 0 has a total capacity of 14.56 GiB of which 349.81 MiB is free.
    Of the allocated memory 12.45 GiB is allocated by PyTorch, and
    1.64 GiB is reserved by PyTorch but unallocated.
    [… peft/tuners/lora/bnb.py, line 549, in forward
        output = lora_B(lora_A(dropout(x))) * scaling]

LES TROIS FAITS DÉCOMPOSÉS :

1. **LE 912 MiB = LE CHEMIN FP32 DE PEFT SUR LE MLP.** La ligne fautive
   est le matmul LoRA ; sa classe est le [1 · 12 615 × 18 944] fp32 =
   911,63 Mio — la taille intermédiaire EXACTE du Qwen2.5-Coder-7B
   (config.json constaté : intermediate_size 18 944, vocab 152 064).
   La cause est à la source (peft 0.22.0, la version du bord — la ligne
   549 s'y lit mot à mot) : sans autocast, `requires_conversion = not
   torch.is_autocast_enabled()` est VRAI et peft CASTE L'ENTRÉE DE CHAQUE
   COUCHE LoRA AU FP32 DES ADAPTATEURS (bnb.py:500-503) — les adaptateurs
   naissent fp32 sur une base 4 bits (`autocast_adapter_dtype` ne fait que
   MONTER fp16/bf16 → fp32, jamais l'inverse). Sur gate/up_proj la sortie
   de lora_B est [S × 18 944] fp32 (912 Mio) et le produit par l'échelle
   un second ; sur down_proj le CAST de l'entrée et la copie du dropout
   deux encore (plus le masque booléen 228 Mio). AU PIC DE LA
   RECOMPUTATION D'UNE COUCHE : ≈ 1,8-2,7 Gio de transitoires fp32 —
   **l'écart du budget de l'Entrée 462, l'écart du labo seul, nommé** :
   le registre du terrain.11 comptait le modèle, les bornes de checkpoint,
   les logits et les tronçons — le chemin fp32 de peft n'y vivait pas.
2. **L'ALLOCATEUR ÉTÉ NÉ SANS SES SEGMENTS EXTENSIBLES.** La garde
   `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` ne se lit qu'à la
   NAISSANCE de l'allocateur — la première allocation CUDA DU PROCESSUS.
   Le run courut sur le noyau recyclé du matin (ipykernel_458 — le run du
   terrain.11 y avait déjà alloué) : la variable posée à la cellule 5 ne
   mordit JAMAIS. La signature est dans la mesure même : 1,64 Gio
   réservés-non-alloués pendant que le GPU n'avait plus que 0,34 Gio —
   des pages physiques TENUES dans des blocs fragmentés, jamais rendues.
   Le pic réel du pas (12,45 + 0,91 Gio) eût tenu sous 14,56 si le bassin
   eût été élastique ; il ne l'était pas.
3. **LA MARGE ÉTAIT MANGÉE, PAS LA MATHÉMATIQUE.** Le budget du
   terrain.11 (le sommet ≈ 13,3 Gio) est CONFIRMÉ par la mesure (12,45
   alloués + 0,91 refusés = 13,36) — ce qui tua le pas fut la
   fragmentation (1,64 Gio hors d'atteinte), pas la loi des recettes.
   L'exclusion nommée par le plan § 7 ne fut JAMAIS en jeu : le repli
   revient au labo avec la mesure, et la mesure dit UN AUTRE REMÈDE.

## 2. LE GESTE (trois prongs, aucune loi touchée)

1. **LA CANE (fail-closed, NOYAU-SALE le refus nommé).** Avant la charge
   du modèle, la cellule 5 lit `torch.cuda.memory_stats()["allocated_
   bytes.all.peak"]` : SI le processus a DÉJÀ alloué (le noyau recyclé),
   le refus AVANT la marche — « Exécution → Redémarrer la session, PUIS
   Tout exécuter » (le cache du modèle demeure au disque). Sur un
   processus vierge la cane est VERTE et l'allocateur naît sous
   expandable_segments — la variable est désormais POSÉE (plus
   `setdefault`) avant toute importation qui touche CUDA.
2. **L'AUTOCAST fp16 DU PAS — LA VOIE CONÇUE PAR PEFT.** Le pas court
   sous `torch.autocast("cuda", dtype=torch.float16)` : `requires_
   conversion` devient FAUX (bnb.py:500 — la branche ÉCRITE par peft pour
   l'autocast) — **AUCUN CAST fp32, AUCUN [S × 18 944] fp32 N'EST PLUS
   JAMAIS ALLOUÉ**, les matmuls LoRA courent au fp16 natif du T4 (la
   moitié du pied : 456 Mio la pièce). LES ADAPTATEURS DEMEURENT fp32 —
   les gradients fp32, l'optimiseur stable (le dessein même de peft :
   « typically required for stable training »). La CE demeure fp32 (le
   `.float()` explicite — inchangé) ; le chemin bnb 4 bits est hors des
   politiques d'autocast (noyaux propres — inchangé) ; le checkpoint
   non-reentrant REJOUE l'autocast à la recomputation (prouvé au bac).
3. **L'HYGIÈNE + LA MESURE VÉCUE.** `empty_cache()` après la charge du
   modèle (le charge fragmente le bassin) puis AVANT CHAQUE exemple ; le
   PIC mesuré à chaque pas (`pic_gio` porté à la courbe du registre) ;
   le message d'EXEMPLE-LONG-OOM porte le pic — le terrain se mesure
   lui-même au moment même où il refuse.

AU PASSAGE : `torch_dtype` → `dtype` à la charge (la dépréciation criée
au journal du bord par transformers 5.x — nommée et soignée).

## 3. LA PREUVE AU LABO (le bac, torch 2.15.0+cpu, transformers 5.24.1, peft 0.22.0)

Quatre passes (la VOIE A = la cellule 5 de la v1062 TELLE QUELLE ; la
VOIE B = l'amendement — l'autocast autour du pas ; la perte ET les
gradients des adaptateurs) :

| passe | modèle | la marque | écart perte | gradients |
|---|---|---|---|---|
| structure #0 | minuscule Qwen2 + LoRA ×7, adaptateurs **fp32 ASSERTÉS** | VOIE A : **28 casts au fp32** (la classe des 912 Mio) ; le checkpoint **REJOUE l'autocast** à la recomputation (le drapeau lu True/True) | — | — |
| bf16 #0 | minuscule Qwen2 bf16 + LoRA r16 α32 ×7, checkpointing, tronçons | le véritable extrait du corpus | rel. **2,3e-06** | rel. 4,1e-03 · cosinus **0,999997** |
| réel #0 | Qwen2.5-0.5B-Instruct bf16 + LoRA r16 α32 ×7 + LE MÊME pattern que la cellule 5 (logits_to_keep + tronçons de 1024) | l'extrait du monstre | **0,0 EXACT** | rel. 4,6e-03 · cosinus **0,999998** |
| réel #1 | idem | l'exemple le plus court du corpus (C=52) | **0,0 EXACT** | rel. 5,2e-03 · cosinus **0,999998** |

LA LECTURE : la perte est identique — EXACTEMENT ÉGALE sur le vrai
modèle (les adaptateurs naissent à lora_B = 0 : le chemin LoRA ne
contribue rien au forward au premier pas — les deux voies y sont
BIT-IDENTIQUES) — et le SIGNAL D'ENTRAÎNEMENT (les gradients, la chose
qui entraîne) est préservé à 5e-03 relatif, cosinus 0,999998 — UN
ORDRE DE GRANDEUR SOUS le précédent accepté de l'Entrée 462 (« rel.
~2,5e-02 — la classe de bruit du dtype même, la direction du signal
inchangée »). La composition avec le terrain.11 est intacte : la CE
chunked sous autocast demeure fp32 (le `.float()` explicite) et le
checkpoint rejoue l'autocast (la passe structure). LES RÉSIDUS NOMMÉS :
(a) l'octet exact du tampon refusé (912,00 Mio affichés contre 911,63
calculés — l'arrondi de l'allocateur, la classe clouée) ; (b) sous
autocast les normes et le softmax courent fp32 (la politique torch —
PLUS de précision, jamais moins) ; (c) au bord le fp16 du T4 tient le
rôle que le bf16 du bac joue à la preuve — la même classe de bruit.

LE NOUVEAU BUDGET (la mesure du refus pour socle) : le persistant ≈ 10,9
Gio (modèle NF4 + plongements fp16 ≈ 5,6 · bornes de checkpoint 2,53 ·
logits de la réponse 1,32 · leur gradient 1,32 · gradients LoRA 0,16) +
les transitoires de recomputation fp16 ≈ 1,5-2,0 + le contexte ≈ 0,4 →
**le sommet ≈ 12,8-13,3 Gio < 14,56 — la marge 1,3-1,8 Gio**, l'allocateur
élastique GARANTI par la cane et le bassin rendu par l'hygiène.

## 4. CE QUI NE CHANGE PAS (le plan demeure LA LOI)

- LE CORPUS BYTE-BYTE : les 17 VERTS, AUCUNE exclusion, AUCUNE
  troncature (train.jsonl sha256 39614077e5c6d9feb94eb528ae19d9f948d67c531a2ac26daa17229023bb3eb7) ;
- LES HYPERPARAMÈTRES DU § 3 : r16 α32 dropout 0,05 aux sept projections,
  lr 1,5e-5 cosine + échauffement 5 %, 3 époques (51 pas), batch 1 ×
  accumulation 4, clip 1,0, graine 20261128, max_len 13 000, NF4 double
  quantification fp16, l'ordre des longs d'abord, l'enveloppe VERBATIM ;
- LA PERTE : sur LA RÉPONSE SEULE (§ 3), la CE chunked du terrain.11
  TELLE QUELLE (logits_to_keep + tronçons de 1024 — INCHANGÉS) ;
- LE POST-ENTRAÎNEMENT (§ 4), L'ÉVAL (§ 5), LES GAPS (§ 6), LES GARDES
  (§ 7 — EXEMPLE-TROP-LONG et EXEMPLE-LONG-OOM demeurent les refus
  nommés, le second porte désormais le pic mesuré) ;
- LA LOI DES COPIES (§ 8) : la vive au /livrables, l'aveugle au dépôt.

## 5. LE REGISTRE (la cellule 5 le porte)

Le champ « amendement » s'étend (terrain.11 + terrain.12, la voie de
mémoire consignée) ; la courbe gagne « pic_gio » à chaque pas — le
terrain mesure sa propre enveloppe, le refus même portera sa mesure.
Le reste des champs inchangé.
