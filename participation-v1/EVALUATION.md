# Évaluer TRIADE en six commandes

Après avoir extrait `TRIADE_complet_v0.25.0.zip` :

| # | Commande | Résultat attendu |
|---|---|---|
| 1 | `python3 scripts/vague18/linter_v250.py` | `0 RÉSIDU — les cinq classes sont vertes sur les cinq pièces` |
| 2 | `python3 scripts/vague18/linter_v250.py --controle-negatif` | `5/5` (une mutation par classe, chacune refusée) |
| 3 | `python3 scripts/vague17/provenance_tableaux.py --verifier` | `CONFORME — chaque ligne se recompose depuis sa source canonique` |
| 4 | `python3 scripts/vague17/provenance_tableaux.py --controle-negatif` | `4/4` (valeur, ratio, compte, statut refusés) |
| 5 | `python3 scripts/vague18/garde_prescriptif.py --scan` | `0 consigne(s) active(s) hors liste` |
| 6 | `python3 v06/sceau_I.py verifier` | `14 arbres VERTS` |

Puis, si vous voulez aller plus loin : `pack-v250/rapport_verification_v0.25.0.txt`
porte les preuves détaillées (linter, lecteur, provenance, scellés, sceau).

**Ce que ces commandes ne prouvent pas** : aucune exécution au métal nu, aucune ancre
TPM réelle, aucune campagne LLM — ces trois gestes sont nommés « EN ATTENTE » dans les
rapports, et le pack ne les simule pas.
