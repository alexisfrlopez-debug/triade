# PLAN PRÉ-ENREGISTRÉ — LA VAGUE 10, L'INSTRUCTION 3a91o5whb : LE TROISIÈME BRAS « C+G » (le C compilé gcc-O2 RECEVANT la gouvernance TRIADE complète)

> Pré-enregistré AVANT toute mesure (l'empreinte sha256 de ce plan sera
> consignée à EMPREINTES-PLANS-VAGUE10.txt et commitée AVANT la première
> donnée — la lettre de l'instruction : « Pré-enregistre (empreinte
> sha256 verrouillée AVANT toute mesure) un troisième bras C+G »).

## 1. LA QUESTION (falsifiable, pré-enregistrée)

Le protocole TRIADE applique à l'agent une gouvernance complète :
intentions signées, cristallisation, oracle dérivé de I, boucle terrain.
Les campagnes D204/D210 ont mesuré DEUX bras — T (la notation manuscrite,
gouvernée) et C (le C compilé gcc-O2, SANS gouvernance : la pièce
compilée, l'épreuve hash, aucun scellé, aucune chaîne de certificats, le
terrain nu). L'ÉCART T−C mesuré jusqu'ici CONFOND DEUX EFFETS :
l'effet de la NOTATION manuscrite et l'effet de la GOUVERNANCE.

LA QUESTION : que mesure l'effet de la notation manuscrite ISOLÉ de la
gouvernance seule ? — le bras C+G (C compilé gcc-O2 RECEVANT la
gouvernance complète) répond : effet notation = T − C+G ; effet
gouvernance = C+G − C (à travail égal, même machine, même rig).

H-CG1 (falsifiable) : à travail égal, le bras C+G rattrape l'essentiel
de l'écart M4 (la gouvernance — la chaîne de certificats, l'oracle
dérivé de I, la garde du sceau — porte le coût de vérification) ;
l'écart résiduel T−C+G est l'effet propre de la notation. AUCUN chiffre
attendu écrit avant mesure : la mesure tranche.

H-CG2 (falsifiable) : l'effet gouvernance sur M2 (les tokens du flux de
travail) est faible (la gouvernance n'ajoute pas de matériau relu au
modèle — elle contraint le client et le rig, pas le prompt) ; l'effet
notation sur M2 demeure la différence de matériau entre la notation
lisible et le C lisible.

H-CG3 (falsifiable) : l'effet gouvernance sur M1 (les échappées) est
nul ou favorable (l'oracle dérivé de I et les épreuves de contrat
attrapent les mêmes défauts des deux bras C ; les échappées propres au
C compilé — les erreurs de séquence, l'ABI — demeurent).

## 2. LE BRAS C+G (la définition, gelée)

SUR LES MÊMES CONTRATS : les SIX unités instrumentées de la campagne
D210 (loupe-01, loupe-02, loupe-05, loupe-08, loupe-13, loupe-16 — les
six blocs contrôlés aux deux bras), les sources C DE LA CAMPAGNE (les
mêmes fichiers, mot pour mot), la chaîne mingw TRIXIE aux versions
EXACTES (gcc 14.2.0-19+27+b1, binutils 2.44-3+12+b1, mingw-w64
12.0.0-5), -O2, AUCUN drapeau supplémentaire.

LA GOUVERNANCE TRIADE COMPLÈTE reçue par le bras C+G (quatre éléments,
le même niveau que T) :
 (g1) LES INTENTIONS SIGNÉES : la spécification I de l'unité signée
      Ed25519 (la signature sur le texte du contrat, la clé de session
      du labo consignée, la vérification à chaque exécution — le
      refus fail-closed si la signature diverge) ;
 (g2) LA CRISTALLISATION : le certificat de cristallisation du C+G —
      le graphe de dépendances LU des sources (les fonctions appelées,
      les symboles externes), les empreintes par unité chaînées depuis
      la genèse de la campagne, SIGNÉES Ed25519, le diff d'une unité
      re-vérifié en O(unité) contre la complète en O(tout) ;
 (g3) L'ORACLE DÉRIVÉ DE I : les oracles de campagne (oracle_uniteXX,
      le juge modèle indépendant, les vecteurs du contrat — JAMAIS les
      octets de la pièce) conduisent la DLL compilée AU MÊME RIG que T ;
 (g4) LA BOUCLE TERRAIN : le kit 1-clic de l'unité assemblé au même
      gabarit que T/C (le run au terrain attend le geste du maître —
      l'écart nommé, JAMAIS simulé).

L'ORDRE STRATIFIÉ PAR FAMILLE DE BLOCS : les six unités en ordre de
famille (ouvrir : 01 ; lire : 02 ; hachage : 05 ; composition : 08 ;
recherche : 13 ; saisie : 16) — l'ordre consigné AVANT la mesure, la
même séquence pour les trois bras.

## 3. LES MÉTRIQUES (le même rig que D210, rien d'inventé)

 M1 (les échappées) : l'oracle du bloc + l'épreuve de contrat POSIX +
      les contrôles binaires — les défauts nommés à leur classe, les
      échappées de labo comptées AVANT correctif (la même grille que T/C) ;
      les échappées de TERRAIN attendent le geste du maître (l'écart
      nommé en l'état — jamais fabriquées).
 M2 (les tokens du flux) : l'instrument de la campagne (le CLI z-ai,
      le champ usage LU, chaque appel journalisé, la même graine
      20261114) — la tâche de chaque unité (le code de la fonction
      depuis le contrat I) conduite aux TROIS bras : T (la notation),
      C+G (le C gouverné), le C de référence lu du registre D210 (la
      re-mesure n=1 par unité à titre de borne, le record de la
      campagne fait foi).
 M3 (le temps humain au geste) : NON MESURABLE en l'état au labo — le
      terrain est au geste du maître ; T et C portent leurs M3 DU
      REGISTRE D210 (datés) ; C+G M3 ATTEND le terrain — L'ÉCART NOMMÉ
      (jamais un chiffre inventé).
 M4 (le temps de vérification) : la liste fixe de la campagne étendue
      au C+G — la MÊME liste que le bras C (build gcc-O2, la suite de
      tests, l'épreuve de contrat POSIX, les contrôles binaires) PLUS
      les gestes de gouvernance (la garde de l'intention signée, la
      chaîne de cristallisation re-vérifiée, l'oracle du bloc) — n=5
      exécutions par bras, l'horloge monotone, cette machine, la
      variance inter-exécution consignée.

## 4. LA VÉRIFICATION (les exigences de l'instruction, gelées)

 (v1) L'empreinte sha256 de ce plan consignée AVANT la première donnée
      (EMPREINTES-PLANS-VAGUE10.txt, le commit git qui précède).
 (v2) LE SCRIPT DE RÉCONCILIATION : recalcule chaque total (chaque
      étape de chaque exécution M4, chaque médiane, chaque compte M1,
      chaque total M2) depuis les JSON bruts et REFUSE tout écart (la
      sortie : « réconciliation VERT » ou le premier écart nommé).
 (v3) LE CONTRÔLE NÉGATIF : une faute de rig injectée (un chronomètre
      d'étape altéré dans un JSON brut, une médiane mal reportée) DOIT
      être ATTRAPÉE et ATTRIBUÉE par le script de réconciliation.
 (v4) LE RAPPORT : l'effet notation isolé (T − C+G) et l'effet
      gouvernance (C+G − C) avec L'INTERVALLE (min–max des exécutions)
      et LE n EXPLICITE pour chaque métrique rapportée.
 (v5) AUCUN SCELLÉ TOUCHÉ : les quatorze arbres verts avant et après ;
      les pièces de campagne D204/D210 inchangées (les empreintes
      recoupées avant/après) ; le C+G vit en fichiers NOUVEAUX au
      nouvel atelier (atelier-cg-3a91o5whb/), AUCUNE écriture dans les
      dossiers scellés de campagne.

LA MACHINE DE RECORD : ce bac (2 cœurs, 4 Go, la classe des campagnes
D204/vljfs6pcj/cq01qv1za) — la machine fait partie du record, l'écart à
toute autre machine est nommé.
