# Évaluer TRIADE en six commandes

Après avoir extrait `TRIADE_complet_v0.31.0.zip` :

| # | Commande | Résultat attendu |
|---|---|---|
| 1 | `python3 scripts/vague25/porte_generation_v310.py` | `V1..V7 + L1..L25` tout VERT, zéro rouge (les cinq pièces recoupées aux empreintes) |
| 2 | `python3 scripts/vague25/porte_generation_v310.py --controle-negatif` | `18/19` (le 19e : la mutation C22 ne vit pas dans la couche texte du PDF — défaut du harnais, nommé) |
| 3 | `python3 scripts/vague17/provenance_tableaux.py --verifier` | `CONFORME — chaque ligne se recompose depuis sa source canonique` |
| 4 | `python3 scripts/vague17/provenance_tableaux.py --controle-negatif` | `4/4` (valeur, ratio, compte, statut refusés) |
| 5 | `python3 scripts/vague18/garde_prescriptif.py --scan` | `0 consigne(s) active(s) hors liste` |
| 6 | `python3 v06/sceau_I.py verifier` | `14 arbres VERTS` |

Puis, si vous voulez aller plus loin : `pack-v310/rapport_verification_v0.31.0.txt`
porte les preuves détaillées (porte, provenance, scellés, sceau, témoin RFC 3161).

**Ce que ces commandes ne prouvent pas** : aucune exécution au métal nu, aucune ancre
TPM réelle, aucune campagne LLM — ces gestes sont nommés « EN ATTENTE » dans les
rapports, et le pack ne les simule pas. La mesure au silicium se vit avec les kits de
terrain (coffre /livrables), pas dans ce pack.
