# DOC-FEEDBACK — la consigne agent de `triade feedback` (witgt6qta, la vague 15)

LA CONSIGNE (l'agent adopteur, à la fin de session) :
1. LANCER à la fin de session : `triade_feedback.py generer <journal.jsonl> <version-kit>`
   (la part measured est EXTRAITE MÉCANIQUEMENT du journal déjà consigné —
   jamais retapée, le coût token marginal ≈ 0 ; les seuls tokens dépensés
   sont l'invocation ≈ 5).
2. RELIRE le rapport produit (report-<date>-<version>.json) ET le gabarit
   d'issue (issue-<date>-<version>.md) : les portes fail-closed ont couru
   (secrets, champs requis, anonymisation) — la relecture humaine reste.
3. ENVOYER SI CONSENTI (le geste humain D122 — JAMAIS d'envoi automatique ;
   l'outil est OFFLINE, aucun appel réseau, aucune dépendance réseau au
   build R10).

LES PORTES (fail-closed, chacune VÉCUE au rapport d'autotests) :
- champ requis manquant → REFUS nommé (le rapport n'est pas écrit) ;
- secret détecté (les motifs nommés : jeton github, clé privée PEM, bearer,
  refresh token OAuth, jeton générique, chemin absolu, username système ;
  ET la phrase de test marquée D105) → REFUS ;
- chemins/usernames anonymisés (le pseudonymage mécanique à la porte) ;
- le schéma TRIADE-FEEDBACK-v1 (sha256 d7e53f66077812f9… gelée par
  empreinte AVANT tout rapport) : `verifier` re-vérifiable.

LES LIMITES NOMMÉES : l'outil NE JOUE PAS le rôle d'ancre (aucune signature
du projet, la signature adopteur optionnelle n'est jamais l'ancre) ; le
commentary (≤500 tokens) est MARQUÉ NON VÉRIFIÉ au schéma ; le contrôle
négatif de la règle hex-64 RETIRÉE (un sha256 pur n'est pas un secret — les
faux positifs sur les evidence_sha256 légaux constatés au test 4 vécu,
l'écart nommé au rapport).
