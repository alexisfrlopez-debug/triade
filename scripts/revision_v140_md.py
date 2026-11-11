#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""revision_v140_md.py — le md PROTOCOLE_TRIADE.md porté en v0.14.0 (les
ancres refusent si elles manquent) + les consignations D195/Entrée 228/
Task 135 + l'empreinte du PDF formel au registre D134."""
import hashlib
import pathlib
import subprocess

REPO = pathlib.Path("/home/z/my-project/triade")
MD = REPO / "docs" / "PROTOCOLE_TRIADE.md"
s = MD.read_text(encoding="utf-8")
FAITS = []


def remplace(ancien, nouveau, nom):
    global s
    if ancien not in s:
        raise SystemExit(f"[md v0.14.0] ANCRE INTROUVABLE — {nom}")
    s = s.replace(ancien, nouveau, 1)
    FAITS.append(nom)


remplace("# PROTOCOLE TRIADE v0.13.0 — Spécification technique",
         "# PROTOCOLE TRIADE v0.14.0 — Spécification technique",
         "le titre")
remplace("> Source de travail faisant autorité pour la v0.13.0. Les archives formelles des versions\n> précédentes demeurent :",
         "> Source de travail faisant autorité pour la v0.14.0. Les archives formelles des versions\n> précédentes demeurent : `docs/Protocole_TRIADE_v0.13.0_Specification.pdf` (v0.13.0 —\n> les corrections de l'édition),", "la source")
remplace("> La v0.13.0 consigne LES CORRECTIONS DE L'ÉDITION (D190/D191/D192, le",
         """> La v0.14.0 consigne LE PROGRAMME EMPIRIQUE (D193/D194/D195, le
> cinquième fichier d'instructions) : LE BRAS DE RÉFÉRENCE COMPILATEUR
> pré-enregistré (le plan D193 consigné AVANT toute mesure, l'empreinte
> verrouillée ; six blocs C depuis les MÊMES contrats, les mêmes shims,
> auto-vérifiés : ZÉRO DIVERGENCE aux vecteurs — la notation et le
> compilé observationnellement équivalents ; sha-256 PARITAIRE à travail
> égal [9 089 contre 9 146 instructions], les purs plus chers, la
> mutation au même degré — H4 tenue) ; LA RE-MESURE RQ2 en distributions
> (localiser 580 [496..706], éditer 2 143 [1 085..3 463], ajouter
> 3 510 [3 128..4 091], la baseline naive 300 304 — les valeurs M1
> historiques, la lecture DÉFAVORABLE au protocole consignée) ;
> L'INDÉPENDANCE par instance isolée (128 constantes, zéro divergence,
> l'écart de famille nommé) ; LE RE-JEU DES 832 MUTANTS aux
> composition-killers (93,3 % — tls13 et sys à 100 %, les 56 survivants
> loupe nommés) ; LE KIT TERRAIN en attente du geste du développeur.
> Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie
> inchangée.

> La v0.13.0 consigne LES CORRECTIONS DE L'ÉDITION (D190/D191/D192, le""",
         "le préambule v0.14.0")
remplace("- Version : v0.13.0 — la révision des CORRECTIONS DE L'ÉDITION",
         "- Version : v0.14.0 — la révision du PROGRAMME EMPIRIQUE "
         "(D193/D194/D195 : le bras de référence pré-enregistré [zéro "
         "divergence, sha-256 paritaire, H4 tenue], la re-mesure RQ2 en "
         "distributions avec la baseline naive, l'indépendance par "
         "instance isolée, le re-jeu des 832 mutants aux "
         "composition-killers [93,3 %]). Sous la v0.13.0, la révision des "
         "corrections de l'édition", "la ligne Version")
remplace("## 2. La couche I : format normalisé des spécifications",
         """### 1.15 Ce que change la v0.14.0

La révision du **programme empirique** (D193/D194/D195, le cinquième
fichier d'instructions). Aucune règle modifiée, aucun artefact scellé
touché — les affirmations du manuscrit passent aux mesures contrôlées.

**Le pré-enregistrement** (D193) : le plan de comparaison (H1-H4,
CA1-CA5, les six blocs, les vecteurs) consigné AVANT toute mesure,
empreinte verrouillée.

**Le bras de référence** (D195) : six blocs C depuis les mêmes contrats,
les mêmes shims, auto-vérifiés — ZÉRO DIVERGENCE aux vecteurs ;
sha-256 paritaire à travail égal (9 089/9 146 — l'héritage PAR LA
CARTE) ; les purs plus chers à la notation ; la mutation au même degré.

**La re-mesure RQ2** : les distributions de bout en bout (580/2 143/
3 510 de médiane, la baseline naive 300 304, le raisonnement estimé
NOMMÉ) — les valeurs M1 historiques, la lecture défavorable consignée.

**L'indépendance** : l'instance isolée (128 constantes, zéro
divergence) ; l'écart de famille nommé ; la voie entière exacte.

**Le re-jeu des survivants** : 776/832 (93,3 %) aux
composition-killers — tls13/sys à 100 %, les 56 loupe nommés.

**Le kit terrain** (`scripts/kit_terrain_bras_c/`) : EN ATTENTE.

## 2. La couche I : format normalisé des spécifications""",
         "le § 1.15")
remplace("## 20. Glossaire",
         """### 19.16 Correspondance v0.13.0 → v0.14.0

| Évolution | En v0.13.0 | En v0.14.0 | Statut |
|---|---|---|---|
| Comparaison compilateur | le facteur 15,3 retiré par l'audit (une mesure d'émulation) | le bras de référence PRÉ-ENREGISTRÉ : zéro divergence aux contrats, sha-256 paritaire à travail égal, la mutation au même degré (H4) | mesuré (D195) |
| RQ2 | les valeurs M1 historiques seules | les distributions de bout en bout (580/2 143/3 510, la baseline naive 300 304, le raisonnement estimé nommé) — M1 demeure historique | re-mesuré (D195) |
| Indépendance de l'oracle | les voies distinctes (v0.11.0) | l'instance isolée : 128 constantes, zéro divergence ; l'écart de famille nommé (une seule famille au labo) | exécuté (D195) |
| Survivants de mutation | 138 survivants nommés (83,4 %) | le re-jeu aux composition-killers : 93,3 %, tls13/sys à 100 %, 56 loupe nommés | re-jeué (D195) |
| Kits terrain | — | le kit du bras C préparé, EN ATTENTE du geste du développeur | en attente |

Modifications explicitement rejetées (v0.14.0) : mesurer sans le
pré-enregistrement — rejeté (la fraude que CA5 interdit) ; remplacer les
valeurs M1 — rejeté (les deux ères coexistent au rapport) ; extrapoler
le raisonnement à la mesure — rejeté (l'estimation est nommée).

## 20. Glossaire""", "le § 19.16")
remplace("| v0.13.0 | 11 nov. 2026 | Révision des CORRECTIONS DE L'ÉDITION",
         "| v0.14.0 | 11 nov. 2026 | Révision du PROGRAMME EMPIRIQUE (D193/D194/D195) : le bras de référence compilateur pré-enregistré (zéro divergence aux vecteurs, sha-256 paritaire à travail égal [9 089/9 146], H4 tenue) ; la re-mesure RQ2 en distributions (580/2 143/3 510, la baseline naive 300 304, les valeurs M1 historiques, la lecture défavorable consignée) ; l'indépendance par instance isolée (128 constantes, zéro divergence, l'écart de famille nommé) ; le re-jeu des 832 mutants aux composition-killers (93,3 %, tls13/sys à 100 %, 56 loupe nommés) ; le kit terrain en attente. Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |\n| v0.13.0 | 11 nov. 2026 | Révision des CORRECTIONS DE L'ÉDITION",
         "le journal des versions")
MD.write_text(s, encoding="utf-8")

# l'empreinte du PDF formel au registre D134
r = subprocess.run(["python3", "scripts/empreintes_build.py", "consigner",
                    "--artefact",
                    "docs/Protocole_TRIADE_v0.14.0_Specification.pdf",
                    "--build",
                    "chaîne spec_v140 (le programme empirique v0.14.0 — "
                    "D193/D194/D195)"], cwd=REPO, capture_output=True,
                   text=True)
print(r.stdout.strip().splitlines()[-1] if r.stdout else r.stderr[:200])
print(f"[md v0.14.0] {len(FAITS)} remplacements ancrés")
