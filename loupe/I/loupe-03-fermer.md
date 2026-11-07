loupe-03 · fermer : la session close, jamais une poignée pendante · révision 1
Intention : fermer proprement le fichier de session — quel que soit
l'état (ouvert, déjà fermé, en erreur) : la poignée rendue à l'OS, le
cadre re-posé vierge, les zones de session (journal, motif, empreintes,
saisie) remises à zéro. Les zones de session ne fuient JAMAIS d'un
fichier à l'autre — l'hygiène est un invariant. Idempotent par
construction : fermer deux fois ne fait rien de plus, jamais de mal.
Contrat :
  pre  : P1 AUCUNE précondition — le geste est appelable dans TOUT état
             (c'est sa raison d'être : la sortie propre de loupe-18
             n'examinerait pas l'état, elle fermerait).
  post : Q1 si la poignée du cadre est valide (≠ INVALIDE) :
             CloseHandle UNE fois — le fichier rendu à l'OS ; si
             CloseHandle échoue : le code GetLastError consigné, la
             suite AURA LIEU QUAND MÊME (jamais une poignée pendante,
             quel que soit l'état) ;
         Q2 loupe-04 appelée : le cadre re-posé VIERGE (tout à zéro,
             poignée = INVALIDE) ;
         Q3 les zones de session remises à zéro : le nombre du journal
             (loupe-16) = 0, la longueur du motif (loupe-13) = 0, les
             empreintes (loupe-07) effacées, le mode de saisie
             (loupe-12) = 0 — le prochain fichier naît dans un état
             neuf ;
         Q4 rax = 0 dans TOUS les cas de P1 (y compris session déjà
             fermée : le geste est IDEMPOTENT — rien fait, rien de
             plus).
  inv  : I1 le DISQUE n'est PAS touché : fermer ne sauvegarde RIEN
             (la sauvegarde est un geste délibéré à loupe-17 — fermer
             abandonne les écritures non sauvées, la barre de loupe-18
             les aura nommées avant) ;
         I2 le journal est OUBLIÉ, pas appliqué (Q3) — la cohérence :
             ce qui n'est pas sauvegardé n'existe pas au disque ;
         I3 l'IAT déclarée (D161) : CloseHandle, GetLastError — la
             liste fermée ; registres non volatils rendus ; NOP, 0x90.
Échecs :
  E1 : CloseHandle en échec (poignée valide) → le code GetLastError
       consigné AU JOURNAL DU HARNAIS, la suite de Q2/Q3 A LIEU, rax =
       0 QUAND MÊME (le verdict -6 serait un mensonge : la session est
       close, l'état est propre — l'échec de l'OS est constaté, pas
       propagé : « jamais une poignée pendante » prime).
Vecteurs :
  V1 : scénario — ouvrir puis fermer puis relire le cadre : tout est
       vierge (les champs à zéro, la poignée INVALIDE), l'oracle
       différentiel constate l'état neuf (couvre Q1, Q2, Q4).
  V2 : scénario d'hygiène — ouvrir le témoin, éditer (journal posé),
       saisir un motif, fermer, ouvrir le SECOND témoin : le journal
       VIDE (les octets du premier fichier n'apparaissent JAMAIS dans
       la vue du second) — l'écran attendu le prouve octet par octet
       (couvre Q3).
  V3 : idempotence — fermer sur session fermée : rax = 0, AUCUN appel
       CloseHandle (le harnais compte les appels), rien bougé (couvre
       Q4).
  V4 : rejet de l'erreur — le shim CloseHandle en échec : la suite a
       lieu, le cadre vierge, rax = 0, le code consigné (couvre E1).
Fixtures    : les deux témoins du kit (l'hygiène inter-fichiers de V2).
Provenance  : écrite-avant-code.
Décisions   : D171, D161, D7/D35 (l'IAT).
