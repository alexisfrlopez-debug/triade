# AMENDEMENT-V106 — LE TERRAIN.11 : LE T4 NE PORTE PAS LES LOGITS DU PROMPT

> L'amendement au plan gelé PLAN-ENTRAINEMENT-COLAB-V106 — le plan DEMEURE
> BYTE-BYTE (sha256 8a719580746811db0a40a9f4d4e805c4b0ac245e1ac6f67de8c0845a4a27f3d7,
> consigné à l'Entrée 458) ; la présente nomme l'écart MESURÉ au run du
> maître du 28/11 et le geste qui le soigne SANS toucher aucune loi du plan.
> Le onzième terrain de la voie Colab, à la suite des terrains 1-10.

## 1. LA MESURE (le run du maître, 28/11, le navigateur)

La cellule 5 refusa au PREMIER exemple (l'ordre du plan § 3 : les longs
d'abord — l'échec vient tôt, il vint au premier) :

    EXEMPLE-LONG-OOM : le T4 n'a pas tenu l'exemple
    ajouter-v3-i26111705-t1 (12615 jetons)
    torch.OutOfMemoryError: Tried to allocate 7.15 GiB.
    GPU 0 has a total capacity of 14.56 GiB of which 1.67 GiB is free.

LES 7,15 GiB DÉCOMPOSÉS EXACTEMENT : 12 615 × 151 936 × 4 octets — LA COPIE
FP32 DES LOGITS PLEINS (toutes les positions, le prompt y compris) que fait
`ForCausalLMLoss` (logits.float(), loss_utils.py:61). Le chemin de perte du
v106 calcule les logits de TOUS les positions puis les upcaste : le prompt
(8 293 jetons au pire — JAMAIS soumis à la perte, masqué à -100) paie le
même prix de vocabulaire que la réponse.

LE SEUIL, DÉRIVÉ DE LA MESURE : le socle au moment du refus (modèle NF4 +
bornes de checkpoint + logits bf16 pleins + réservé) ≈ 12,9 GiB ; il reste
1,67 GiB — la copie fp32 tient sous ~2 900 positions, et la marche arrière
de la perte (le log-softmax et son gradient, deux tampons de la MÊME taille)
ramène le seuil réel à ~4 500 jetons. LE CORPUS : médiane 4 527, plus court
3 351. La voie de repli du plan (l'exclusion) EÛT VIDÉ LE CORPUS : cinq ou
six exemples sur dix-sept eussent tenu — la loi des recettes du plan § 2
(LES 17 VERTS) eût péri, et le moindre reste eût couru sans marge.

## 2. LE GESTE (la même perte, calculée où elle vit)

L'amendement porte la cellule 5 à demander `logits_to_keep = len(réponse)+1` :
le découpage se fait AVANT le lm_head (`slice_logits_to_keep` —
transformers/modeling_utils.py, constaté à la source au bac sur la 5.24.1,
la famille exacte du bord) : LES LOGITS DU PROMPT NE SONT PLUS JAMAIS
ALLOUÉS. Les K = C+1 dernières positions portent les prédictions des C
jetons de la réponse (la première prédit le premier jeton de la réponse) ;
la rangée finale est jetée.

La perte — TOUJOURS SUR LA RÉPONSE SEULE (§ 3) — est conduite PAR TRONÇONS
de 1 024 rangées sous `torch.utils.checkpoint` : la somme des entropies
croisées des cibles, divisée par leur nombre — EXACTEMENT le « mean » de
ForCausalLMLoss aux non-ignorés. Le tronçon borne les tampons fp32 du pire
cas (C = 4 324 : logits bf16 1,23 Gio + trois tampons de tronçon 0,59 Gio
chacun — le sommet ≈ 12,4 Gio < 14,56, la marge nommée 2,1 Gio). La garde
`PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` (posée avant la première
allocation CUDA — le charge du modèle) rend au bassin le 1,23 Gio
réservé-non-alloué du refus : la ceinture aux bretelles.

## 3. LA PREUVE AU LABO (le bac, torch 2.15.0+cpu, transformers 5.24.1)

L'identité des deux voies est PAR POSITION — elle ne dépend ni des poids,
ni de la longueur, ni de la largeur du vocabulaire. Éprouvée en six passes
(la VOIE A = la cellule 5 du v106 TEL QUEL ; la VOIE B = l'amendement ;
la perte ET les gradients des paramètres entraînables) :

| passe | modèle | exemple (vrai texte du corpus, enveloppe du moteur) | écart perte | écart gradients |
|---|---|---|---|---|
| fp32 #0 | minuscule Qwen2, VOCAB RÉEL 151 936 | P=572 C=223 (1 tronçon) | 9,5e-07 | 6,0e-08 (rel. 2,6e-07) |
| fp32 #1 | minuscule Qwen2, vocab 16 384 | P=572 C=1111 (2 tronçons) | 9,5e-07 | 7,5e-08 (rel. 2,9e-07) |
| bf16 #0 | minuscule Qwen2, vocab réel | P=572 C=223 | 0,0 | 3,0e-08 |
| bf16 #1 | minuscule Qwen2 | P=572 C=1111 (2 tronçons) | 1,9e-06 | 2,4e-07 |
| réel #0 | Qwen2.5-0.5B-Instruct PRÉ-ENTRAÎNÉ + LoRA r16 α32 (les sept projections) | P=59 C=223 | **0,0 EXACT** | 4,4e-03 (rel. 2,4e-02) |
| réel #1 | idem | P=192 C=52 (le plus court du corpus) | **0,0 EXACT** | 6,4e-03 (rel. 2,7e-02) |

LA LECTURE : la perte est IDENTIQUE — au ulp du fp32 sur la passe décisive,
EXACTEMENT ÉGALE sur le vrai modèle. Les gradients sont identiques au ulp
du fp32 ; sur le vrai modèle en bf16, l'écart relatif ~2,5e-02 est
L'ARRONDI DU MATMUL (le lm_head à M différent bloque différemment — la
classe de bruit du dtype même, la direction du signal inchangée). LES RÉSIDUS
NOMMÉS : (a) l'ordre des sommes entre tronçons — mesuré au ulp du fp32
(9,5e-07) ; (b) l'arrondi bf16 des gradients — mesuré ci-dessus. Le run
demeure DÉTERMINISTE (la graine 20261128, l'ordre des exemples, l'ordre des
tronçons — reproductible à la lettre).

LA DÉMONSTRATION PARFAITE AU PASSAGE : la VOIE A elle-même fit sauter LE BAC
(4 Go de RAM) au-delà de ~L 1 100 au vocabulaire réel — le terrain.11 n'est
pas une particularité du T4, c'est la nature du chemin de perte du v106.

## 4. CE QUI NE CHANGE PAS (le plan demeure LA LOI)

- LE CORPUS BYTE-BYTE : les 17 VERTS, AUCUNE exclusion, AUCUNE troncature
  (train.jsonl sha256 39614077e5c6d9feb94eb528ae19d9f948d67c531a2ac26daa17229023bb3eb7) ;
- LES HYPERPARAMÈTRES DU § 3 : r16 α32 dropout 0,05 aux sept projections,
  lr 1,5e-5 cosine + échauffement 5 %, 3 époques (51 pas), batch 1 ×
  accumulation 4, clip 1,0, graine 20261128, max_len 13 000, NF4 double
  quantification fp16, l'ordre des longs d'abord, l'enveloppe VERBATIM ;
- LE POST-ENTRAÎNEMENT (§ 4 — l'adapter sauvé AVANT l'éval), L'ÉVAL (§ 5 —
  la batterie de la 105, le Q6_K --lora), LES GAPS NOMMÉS (§ 6), LES GARDES
  (§ 7 — EXEMPLE-TROP-LONG et EXEMPLE-LONG-OOM demeurent les refus nommés) ;
- LA LOI DES COPIES (§ 8) : la vive au /livrables, l'aveugle au dépôt.

## 5. LE REGISTRE (la cellule 5 le porte)

Le registre d'entraînement gagne le champ « amendement » — le terrain.11
nommé, la voie de la perte consignée — le reste des champs inchangé (la
courbe, les pertes par pas, les totaux de jetons, la durée).
