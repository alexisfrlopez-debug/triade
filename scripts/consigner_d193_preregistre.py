#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_d193_preregistre.py — LE PRÉ-ENREGISTREMENT consigné AVANT
TOUTE MESURE (la commande v0.14.0, point 1). L'empreinte sha256 du plan
est consignée : toute modification postérieure du plan sera attrapée par
l'étape de vérification (CA5)."""
import hashlib
import pathlib

plan = pathlib.Path("/home/z/my-project/triade/scripts/preuves_v140/"
                    "PLAN_PREENREGISTRE_v140.md")
h = hashlib.sha256(plan.read_bytes()).hexdigest()

D = pathlib.Path("/home/z/my-project/triade/docs/DECISIONS.md")
D.write_text(D.read_text(encoding="utf-8") + f"""

## D193 — LE PRÉ-ENREGISTREMENT DU BRAS DE RÉFÉRENCE COMPILATEUR (la commande v0.14.0, point 1 : « rédiger et consigner un plan de comparaison avec hypothèses et critères d'acceptation AVANT toute mesure ») ; LE PLAN VIT À scripts/preuves_v140/PLAN_PREENREGISTRE_v140.md — sha256 {h} — CONSIGNÉ AVANT LE PREMIER OCTET DE MESURE (le critère CA5 : toute divergence de cette empreinte après le début des mesures est une fraude nommée)

**Le contexte qui fonde la décision (11/11).** Le cinquième fichier d'instruction (Qwen_text_20261111_ic09ydeli.txt) exige la comparaison contrôlée contre un bras de référence compilateur, le pré-enregistrement D'ABORD. Le plan pré-enregistré : SIX blocs couvrant les CINQ familles (loupe-01 ouvrir, loupe-02 lire, loupe-05 sha256, loupe-08 ligne, loupe-13 recherche, loupe-16 saisie — les mêmes contrats de couche I), la référence C consommant les MÊMES shims du mini-OS par table de pointeurs, les MÊMES vecteurs (le vide, abc, les NIST 448/896, le pseudo-aléatoire à la graine 20261113), la MÊME campagne de mutation (16 mutants/bloc, graine 20261111, les mêmes tueurs — K2 adapté à la séquence d'appels OS pour le camp C, le round-trip exclu par nature).

**Les hypothèses pré-enregistrées.** H1 la référence est saine (auto-vérification contre les vecteurs officiels AVANT toute mesure — un échec = aucun chiffre) ; H2 la notation est plus compacte que -O2 (re-testé, INVALIDABLE notamment contre -Os) ; H3 les instructions par opération sont du même ordre de grandeur (pas de facteur spectaculaire dans aucun sens) ; H4 le taux de mort par mutation est du même ordre sous les mêmes tueurs.

**Les critères d'acceptation.** CA1 l'auto-vérification d'abord ; CA2 le même harnais, les mêmes shims, les mêmes vecteurs, la même graine ; CA3 les résultats TELS QUELS, y compris défavorables au protocole ; CA4 toute adaptation d'instrument NOMMÉE ; CA5 l'empreinte du plan invariante après le début des mesures.

**Alternatives rejetées.** Mesurer d'abord et consigner le plan ensuite — rejeté : c'est précisément la fraude que le pré-enregistrement interdit. Étendre la comparaison aux 18 blocs — rejeté : six blocs couvrant les cinq familles sont l'échantillon représentatif que la commande exige (« au moins 6 blocs couvrant les cinq familles »), le coût marginal des douze autres n'apporte pas d'information de famille nouvelle. Comparer au niveau source (le C against le pseudo-code) — rejeté : la comparaison est au niveau des OCTETS vécus (instructions exécutées, tailles, mutations), la seule qui parle du contrat à l'octet.

**Frontières.** Aucun artefact scellé touché ; les kits terrain préparés et marqués « EN ATTENTE » (jamais un résultat fabriqué) ; les tokens mesurés À PART (la re-mesure RQ2, jamais confondus avec ce bras).
""", encoding="utf-8")
print(f"[D193] pré-enregistrement consigné — plan sha256 {h[:16]}…")
