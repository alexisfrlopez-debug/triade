# PLAN-ENTRAINEMENT-COLAB-V106 — LE PLAN GELÉ

> La commande du maître (28/11/2026) : « il faut relancer la campagne test 105
> sur colab et ensuite la campagne d'entrainement de modèle Qwen Code 2.5 7B
> avec Triade sur colab ». La 105 court d'abord (la ligne de base) ; la
> présente est la campagne d'ENTRAÎNEMENT — la seconde. Ce plan est GELÉ avant
> toute mesure ; son sha256 est consigné au MANIFESTE du kit et au worklog.

## 1. L'OBJECTIF

Affiner Qwen2.5-Coder-7B-Instruct sur le CORPUS TRIADE (la notation à la
main des blocs machine) par QLoRA SFT au poste Colab T4, puis mesurer LE
MODÈLE AFFINÉ par LA MÊME BATTERIE que la campagne 105 (les six étapes du
plan gelé W29DECCO/W29FAMILLE, l'instrument ÉPROUVÉ du kit poste v101) —
la comparaison pré/post conduite AU LABO, les verdicts TELS QUELS.

## 2. LES DONNÉES (le corpus tel quel, la loi des recettes)

- `dataset/train.jsonl` (78 triples) — **les verdicts VERTS SEULS** :
  17 triples (60 REFUS et 1 CANARI exclus — la recette SFT du gym
  3x9cf4e5d : « le champ reponse des verdicts VERTS, le contrat au
  contexte »).
- La longueur mesurée au bac (tokenizer Qwen2.5-Coder-7B-Instruct,
  l'enveloppe du moteur appliquée) : prompt max 8 293 jetons, exemple
  max 12 615 jetons, médiane 4 527 ; cumul 78 343 jetons de prompt +
  20 906 de réponse. **AUCUNE troncature** (max_len 13 000 ; un exemple
  plus long = EXEMPLE-TROP-LONG, refus nommé).
- L'OVERLAP NOMMÉ : 8 des 18 blocs de la batterie vivent au corpus
  (loupe-03/04/05/11/13/15/16/18) — l'overlap de BLOCS, pas de lignes :
  1 seul vert porte la ligne visée par la batterie. L'affinage apprend
  la NOTATION (le style, le gabarit, les étiquettes) ; l'éval mesure les
  ÉDITS tenus. L'interprétation sera consignée avec cette réserve.

## 3. LA MÉTHODE (QLoRA SFT, les hyperparams consignés au registre)

- Modèle : `Qwen/Qwen2.5-Coder-7B-Instruct`, chargé 4 bits NF4 double
  quantification, compute **fp16** (le T4 ne porte pas bf16).
- LoRA : r=16, α=32 (échelle 2,0), dropout 0,05, cibles q/k/v/o/gate/up/
  down_proj (les sept projections).
- Optimisation : AdamW lr 1,5e-5 (la fourchette des recettes 1e-5..2e-5),
  cosine + échauffement 5 %, 3 époques (51 pas), batch 1 × accumulation 4,
  gradient checkpointing, clip 1,0, graine 20261128.
- La perte sur LA RÉPONSE SEULE (le prompt masqué à -100) ; l'enveloppe
  VERBATIM du moteur (`<|im_start|>user\n{contrat}<|im_end|>\n
  <|im_start|>assistant\n{réponse}<|im_end|>`) — le MÊME langage que la
  batterie (l'Entrée 451 portée à l'entraînement).
- Ordre : les exemples les plus longs D'ABORD (l'échec OOM vient tôt,
  jamais à la fin) ; EXEMPLE-LONG-OOM le refus nommé si le T4 ne tient pas.

## 4. LE POST-ENTRAÎNEMENT (la pièce sauvée AVANT l'éval)

1. L'adapter sauvegardé (safetensors) PUIS converti au GGUF
   (convert_lora_to_gguf.py du dépôt llama.cpp, outtype f16, l'échelle
   α/r appliquée par le convertisseur — l'hypothèse nommée).
2. L'adapter GGUF + la courbe de perte + le registre téléversés au /test
   du coffre PAR LE RELAIS EMBARQUÉ **avant l'évaluation** — la pièce
   vit au coffre quand l'éval court (aucune perte d'œuvre si le runtime
   meurt en batterie).

## 5. L'ÉVALUATION (la batterie de la 105, l'instrument intact)

- Le serving : **le GGUF Q6_K de bartowski — byte-byte la 105** — au
  `--lora` de l'adapter (le delta appliqué au runtime sur la base
  quantisée : la SEULE différence du bord, nommée) ; llama-server
  prébâti, -ngl 99, -c 8192, la porte de santé + LA PORTE DE PAROLE
  (BORD-MUET le refus nommé).
- LA BATTERIE : les SIX étapes TELLES QUELLES (vérifier-kit · gate · la
  sonde des deux enveloppes · le canari · la campagne éditer 18 +
  ajouter 18 + la seconde famille · le zip).
- La comparaison pré/post conduite AU LABO sur les pièces du /test —
  jamais au bord.

## 6. LES GAPS NOMMÉS (l'honnêteté d'abord)

1. **17 exemples** — le corpus tel quel ; l'overfitting de style est
   attendu, la mesure seule dira.
2. **DPO différé** — le registre ne porte que 2 paires (le gym) : trop
   peu pour un pas utile ; le geste suivant, à la commande du maître.
3. **RLVR différé** — la récompense typée exige la chaîne de juges au
   bord : le geste suivant (le plan du gym demeure LA LOI).
4. **--lora au Q6_K** — le delta appliqué à la base quantisée au
   runtime ; la voie de repli (fusion bf16 puis conversion Q8_0 du
   modèle entier) est nommée si le serving refuse l'adapter.
5. **La file T4** — l'assignation peut patienter des heures (le pas
   idempotent reconduit).

## 7. LES GARDES (les refus nommés, fail-closed)

DISQUE-INSUFFISANT (< 40 Gio) · PIP-ROUGE · JETON-ROUGE · KIT-DIVERGENT ·
COMPTE-VERTS-DIVERGENT · EXEMPLE-TROP-LONG · EXEMPLE-LONG-OOM (le T4 ne
tient pas l'exemple le plus long) · ADAPTER-CONVERSION-ROUGE ·
BORD-MUET · PORT-OCCUPÉ · les refus du moteur (GATE, CANARI, campagne) ·
ZIP-ABSENT · ORDRE-ROMPU · IDENTIFIANTS-ABSENTS (la copie aveugle).

## 8. LA LOI DES COPIES

La copie AVEUGLE (dépôt git public) porte les TROIS chaînes VIDES ; la
copie VIVANTE vit au /livrables du coffre. La SEULE divergence
vivante/aveugle = les TROIS constantes de la cellule des identifiants
(l'invariant du v104, asserté au bâtisseur).
