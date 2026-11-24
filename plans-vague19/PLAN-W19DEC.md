# PLAN GELÉ — W19DEC (chaîne de décisions D261–D267, recompte du banc, annexe B, ancre de transparence)

> Instruction source : Prompt 2 du message du maître du 24/11/2026 12:42. Journal
> append-only, alternatives rejetées consignées, aucun coffre réel approché (D105),
> bancs sur copies de laboratoire uniquement.

## Périmètre
1. RECOMPTE DU BANC DE BASCULE depuis les cas du kit (`atelier-w17-patch-a-chaud/kit_bascule.py`,
   autotest) : le compte publié « 16/16 » se décompose-t-il en 10/10 + 5 aléas + 1 ? Nommer le
   contrôle supplémentaire (le cas NOMINAL du rendez-vous) ou corriger le compte publié.
2. PORTER AU JOURNAL ET À LA SPÉCIFICATION les décisions annoncées-absentes :
   - D261 (les cinq aléas du rendez-vous) — déjà au §7.6, à consigner au journal ;
   - D262 (liste blanche prescriptive fermée) — § nouveau ;
   - D263 (compteur NV TPM/RPMB comme ancre de fraîcheur par profil, limites nommées,
     refus fail-closed si absent ou en arrière) — § nouveau ;
   - D264 (expansion structurée, boucle de réparation bornée) — § nouveau ;
   - D265 (linter v2 porté aux résidus) — consigné au journal ;
   puis D267 : l'ancrage de transparence des témoins d'époque (Rekor/RFC 3161) au statut
   APPLIQUÉ, avec le delta au modèle de menace aux deux bords (en ligne / hors ligne).
3. Aligner la plage de l'annexe B de la spécification sur la dernière décision réelle.
4. Re-scan des consignes prescriptives par `scripts/vague17/linter_v234.py` : zéro consigne active.

## Contraintes
- Journal append-only : aucune entrée réécrite ; les nouvelles décisions sont ajoutées à la fin.
- Aucun coffre réel approché (D105) ; les bancs ne tournent que sur copies de laboratoire.
- Aucune décision n'est « mûre » par décret : D262/D263/D264 sont portées avec leurs limites
  et leurs statuts (mesuré / simulateur / EN ATTENTE) tels qu'ils sont.

## Fichiers touchés
`docs/DECISIONS.md`, `scripts/spec_v158/sec-b.tex`, `scripts/spec_v158/sec-d.tex`,
`scripts/spec_v158/main.tex`, `atelier-w19-dec/` (rapport + recompte), `edition-v0230/main.tex`
(plage de décisions et note), `scripts/vague19/recompte_banc.py`.

## Critères d'acceptation
- Linter DECISION-RANGE vert sur les cinq pièces (porté par W19LINT).
- Recompte du banc depuis les cas du kit : écart zéro avec le compte publié (ou compte corrigé).
- Autotest du banc NV rejoué sur copies : compteur absent → REFUS, retour en arrière → REFUS,
  nominal → VERT.
- MATRICE-R10 confrontée à la nouvelle ligne (D263) et au delta de transparence (D267).
- `linter_v234.py` : zéro consigne active.
