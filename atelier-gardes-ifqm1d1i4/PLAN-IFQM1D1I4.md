# PLAN PRÉ-ENREGISTRÉ — LA VAGUE 10, L'INSTRUCTION ifqm1d1i4 : LES GARDES RUNTIME DES 92 ACCÈS + LA NON-INTERFÉRENCE ÉTENDUE (x25519, md5) ET LA SOUNDNESS DU LIFTER

> Pré-enregistré AVANT toute mesure (empreinte sha256 consignée à
> EMPREINTES-PLANS-VAGUE10.txt, le commit git qui précède toute donnée).

## CHANTIER 1 — LA SÛRETÉ MÉMOIRE AU 100 % DÉCHARGÉ-OU-GARDÉ

L'ÉTAT DE DÉPART (v200, la vague 9) : 2 098 accès classés — 2 006
DÉCHARGÉS par preuve statique (95,6 %), 92 NOMMÉS à base RUNTIME (les
bornes vivent aux invariants externes : OS, appelant, layout).

LA MÉTHODE (gelée) :
 (c1) LA RE-CLASSIFICATION INTÉGRALE : les 2 098 accès re-lus de la
      base v200 (la reproduction d'abord : 2 006/92 inchangés AVANT
      toute extension — la base saine) ;
 (c2) POUR LES 92 : (a) la DÉCHARGE interprocédurale/relationnelle —
      la chaîne d'appel remontée aux scellés appelants (les appels IAT
      aux blocs scellés dont le contrat I porte la borne — la preuve
      par le contrat de l'APPELANT, le certificat SMT) LÀ OÙ la borne
      existe hors du bloc ; (b) SINON LA GARDE RUNTIME : la garde
      dérivée des invariants externes (OS/appelant/layout — la norme
      DU CONTRAT EXTERNE, jamais une hypothèse du bloc) : la garde
      posée AVANT l'accès, la borne imposée PAR CONSTRUCTION (le
      rejet nommé si l'invariant est violé), CHAQUE GARDE PROUVÉE par
      SMT : (la garde) ⇒ (la borne de l'accès) — UNSAT = la preuve, le
      certificat archivé rejouable ;
 (c3) LA CIBLE : 100 % DÉCHARGÉ-OU-GARDÉ (chaque accès : statique
      sound / borné / gardé — l'étiquette de force de preuve PAR
      ACCÈS), chaque RÉSIDU nommé avec sa cause ;
 (c4) LA FALSIFICATION PAR GARDE : CHAQUE garde a son test de
      falsification — la faute réintroduite (l'invariant violé au
      vecteur) DOIT être ATTRAPÉE par la garde (le rejet nommé au
      harnais), la divergence de comportement consignée.

## CHANTIER 2 — LA NON-INTERFÉRENCE STATIQUE ÉTENDUE

L'ÉTAT DE DÉPART : DIX familles crypto (tls13-01/02/03/05/06/07/15/16/
18/19) — 0 branche taintée, 0 adresse taintée, le contrôle négatif
attrapé.

LA MÉTHODE (gelée) :
 (n1) L'EXTENSION à x25519 (tls13-13, tls13-14) et md5 (loupe-06) —
      le secret du contrat I posé en taint à la source, la propagation
      de la vague 9 reconduite, les sites sensibles confrontés par z3 ;
 (n2) LA SOUNDNESS DU LIFTER : le round-trip IR↔notation — la notation
      assemblée (keystone) → liftée (capstone → IR) → re-générée →
      re-assemblée : ZÉRO divergence d'octets exigée sur les familles
      couvertes (le certificat de round-trip par bloc, le juge
      l'octet) ; le contrôle négatif (un octet muté) ATTRAPÉ ;
 (n3) LA REQUALIFICATION : « PROUVÉE » devient « PROUVÉE SOUS
      L'HYPOTHÈSE DE SOUNDNESS DU LIFTER » partout où la preuve
      non-interférence est rapportée (la dépendance de la preuve au
      lifter, nommée en clair — la couverture rapportée EN BLOCS et
      EN FAMILLES : chaque bloc crypto du domaine, chaque famille,
      jamais « dix familles » sans le décompte des blocs) ;
 (n4) LE CONTRÔLE NÉGATIF reconduit : la branche sur secret ATTRAPÉ
      (le bloc fautif de la vague 9, re-vérifié) ; le hash de trace
      temps-constant reconduit (l'audit fkqc7v8t re-roulé vert).

## LA VÉRIFICATION (gelée)

 la re-classification des 2 098 accès : ZÉRO hors-cadre ; chaque garde
 avec son test de falsification (la faute réintroduite → ATTRAPÉE) ;
 le round-trip du lifter : ZÉRO divergence sur les familles couvertes ;
 le contrôle négatif non-interférence (branche sur secret) ATTRAPÉ ; le
 hash de trace temps-constant reconduit ; la force de preuve par accès
 étiquetée (statique sound / borné / gardé) ; les scellés intacts (la
 garde du sceau 14/14 avant/après, AUCUNE écriture aux dossiers
 scellés — les gardes vivent en COPIES DE LABORATOIRE aux adresses de
 marge, le modèle OPT-01).
