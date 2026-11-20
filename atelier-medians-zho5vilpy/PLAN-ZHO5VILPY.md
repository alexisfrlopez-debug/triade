# PLAN PRÉ-ENREGISTRÉ — LA VAGUE 11, L'INSTRUCTION zho5vilpy : LE LINTER ÉTENDU À TOUT TOKEN NUMÉRIQUE DE LA PROSE + LES CORRECTIONS SUR PIÈCES

> Pré-enregistré AVANT toute mesure (l'empreinte sha256 consignée à
> EMPREINTES-PLANS-VAGUE11.txt, commitée AVANT la première donnée).

## 1. LA QUESTION

Le linter v210 contrôle des CANONS nommés (les valeurs choisies). L'instruction
exige l'extension à TOUT token numérique de la prose des cinq pièces : chaque
nombre extrait, recalculé depuis les CSV/JSONL bruts, TOUTE divergence refusée.

## 2. LES CORRECTIONS SUR PIÈCES (diagnostiquées avant le plan, vérifiées par le linter)

(a) LA DÉCOMPOSITION MÉMOIRE DE LA PIÈCE 4 (preuves v0.21.0) : la ligne publiée
« pile 1247 · médiés 0 · constants 191 · plan-fixe 189 · plan-garde 13 ·
contrat-boucle 18 · NOMMÉS 92 » SOMME À 1750, PAS 2098. Le recompte depuis
atelier-securite-bk79jvzbm/surete_memoire_v200.csv (52 lignes, acces_mem=2098)
donne : pile 1247 · MÉDIÉS 348 (le compte réel, publié « 0 » par erreur — la
somme des medies_contrat) · constants 191 · plan-fixe 189 · plan-garde 13 ·
contrat-boucle 18 · nommés 92 · hors-cadre 0 = 2098 EXACTEMENT. La correction
porte le compte médiés réel ; la cohérence 2006 + 34 + 58 = 2098 reconduite.

(b) LES RATIOS PROSE DU MANUSCRIT §7 (sec:floor) : 833/561 = 1,4848… → 1,5×
(publié « 1.6× ») ; 16040/833 = 19,256… → 19,3× (publié « two orders below »).
Recalculés à UNE décimale, arithmétique par code, sourcés des médianes brutes.

(c) LE RATIO AU PLANCHER ÉDITER, recalculé dans le MÊME tokenizer que le
total : le total éditer est NATIF (champ usage) ; le plancher publié est 18
cl100k. Le plancher sera re-tokenisé AU NATIF (la même paire de lignes du diff
réel, mesurée au champ usage du CLI, la même méthode que la campagne) ; le
ratio rapporté natif/natif. La ligne cl100k historique demeure DATÉE au bord.

(d) TOUS LES HEADERS/VERSIONS PÉRIMÉS : running header et pdftitle v0.20.0 →
v0.22.0 ; Livre v1.3/v1.4 → v1.6 (les mentions datées demeurent datées) ;
éditions courantes v0.15.2/v0.15.5 → v0.15.7 ; Data availability v0.19.5 →
l'état courant (v0.21.0 à la rédaction, DOI 24397623, les archives nommées
v0.22.0) ; LA PLAGE DE L'ANNEXE B (D75-D228 → la plage réelle aux décisions
portées) ; « TREIZE arbres » RÉSIDUELS (les mentions d'ÉTAT courant, jamais
les mentions historiques datées — spec §… « porte désormais treize arbres » →
quatorze D177 ; le runbook « verifier : treize arbres VERTS » → quatorze ;
Livre §… « les treize arbres de lignée » → le compte courant) ; LES SECTIONS
DE VERSIONS MANQUANTES (l'historique d'édition du manuscrit porte les
programmes des éditions antérieures — la onzième vague aura sa section).

(e) LA CONCLUSION RQ2 ALIGNÉE SUR LES FORMATS ADOPTÉS : le pointeur seul (le
format adopté D222), le statut OPT-10 TRANCHÉ (la fenêtre adoptée — la
conclusion ne peut plus citer la notation complète relue comme état courant).

(f) LES VERBATIM TRONQUÉS ET LE MOJIBAKE : la cause nommée — (1) la fonction
lit() du générateur de preuves coupe à 2600 caractères (« N'ÉMET AUCUN »
devenu « n'émAUCUN » dans la pièce 1) : la limite devient la coupure À LA
LIGNE près, le verbatim INTÉGRAL des rapports d'atelier ; (2) la couverture
des preuves v0.21.0 porte « â€" »/« Ã© » — le HTML de couverture SANS déclaration
de jeu de caractères lue en Latin-1 par le moteur : la balise meta charset
posée ; (3) LA CAUSE DU « couloir B : code 1 » NOMMÉE : le sous-processus
cpuid_hisse.py mort À L'IMPORT (build_m4 → build_m3 → pefile/nacl ABSENTS du
bac à la régénération du rapport — ModuleNotFoundError, code 1) ; la mesure
elle-même VÉRIFIÉE PAR RE-EXÉCUTION (pefile+pynacl posés : v1 45 · v2 34,4 ·
scellé 26 · scellé-en-flot 34,4 — les chiffres publiés reproduits, la ligne
« code 1 » demeurée au verbatim, la cause consignée).

## 3. LE LINTER v220 (le contrôle étendu)

- L'extraction des tokens numériques : les cinq pièces (pdftotext), le regex
  des nombres (les séparateurs FR/EN normalisés), CHAQUE token confronté :
  (1) aux VALEURS CANONIQUES du manifeste des données brutes (les CSV/JSONL
  des ateliers — la table de correspondance nommée par valeur) ; (2) aux
  ARITHMÉTIQUES DÉRIVÉES (les sommes, les ratios à une décimale, les
  pourcentages) recalculés par code ; (3) aux HISTORIQUES DATÉS (la liste
  nommée des valeurs historiques autorisées, chacune à sa date).
- La règle fail-closed : TOUTE divergence non couverte par la table = ROUGE,
  le build REFUSÉ, la valeur nommée au premier écart.
- LE CONTRÔLE NÉGATIF : une valeur fausse injectée dans une copie — refusée
  au premier nom.

## 4. LA VÉRIFICATION APRÈS MODIFICATION (la lettre de l'instruction)

Le linter étendu rejoué sur les cinq pièces régénérées (zéro divergence) ; la
valeur fausse injectée refusée au premier nom ; chaque somme publiée
recalculée depuis les CSV ; les empreintes sha-256 des pièces recoupées au
manifeste du pack ; l'entrée de journal et la décision append-only.
