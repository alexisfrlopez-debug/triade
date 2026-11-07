loupe-17 · sauver : les octets modifiés écrits à l'octet, le témoin rendu · révision 1
Intention : enregistrer les octets modifiés — CHAQUE entrée du journal
écrite À SON DÉCALAGE, UNE PAR UNE (SetFilePointerEx + WriteFile d'UN
octet : l'écriture À L'OCTET, l'unité est l'octet, jamais une plage) —
puis la marque levée, la garde de sortie levée, le panneau
recalculé (loupe-07 : la vérité du disque re-naît — le coût du
passage est nommé) ET LE TÉMOIN RENDU à la barre : combien d'octets,
de la première à la dernière adresse — ce qui a bougé est dit, pas
suggéré.
Contrat :
  pre  : P1 la session est ouverte ; P2 appelée par la procédure
             (loupe-09 Q3) sur Ctrl+S (VK_KEYDOWN 'S' avec Ctrl) ;
             P3 le journal peut être VIDE (le repli nommé).
  post : Q1 le journal VIDE → rax = 0 SANS écriture, la barre nomme
             « rien à sauver » (le repli documenté — pas un échec,
             l'état nommé) ;
         Q2 SINON : pour CHAQUE entrée du journal DANS SON ORDRE DE
             SAISIE : SetFilePointerEx(décalage, DEBUT_FICHIER) puis
             WriteFile(1 o) — l'octet à SON décalage, un par un ;
             tout l'échec s'arrête LÀ (verdict -6, le code
             GetLastError consigné — FAIL-CLOSED : le journal DEMEURE,
             la marque demeure, les octets déjà écrits le restent —
             l'échec ne perd RIEN, le geste peut se reprendre) ;
         Q3 SUCCÈS COMPLET : journal.nombre = 0, cadre.sale = 0,
             refus_quitter = 0 (la garde de loupe-18 levée — la
             sortie ne ré-avertira plus : il n'y a plus rien à
             perdre) ;
         Q4 LE PANNEAU RE-NAÎT : loupe-07 rappelé (les empreintes du
             DISQUE — la sauvegarde a changé le fichier, le panneau
             suit : jamais un condensé d'avant) — le coût est NOMMÉ :
             un passage de plus, le prix de la vérité ;
         Q5 LE TÉMOIN à la barre : « N o écrits · 0xAABBCCDD..0xEEFF-
             GGHH » (le compte exact, la première et la dernière
             adresse écrites) — ce qui a bougé est DIT ;
         Q6 la TAILLE DEMEURE (l'écriture à l'octet ne change JAMAIS
             la taille du fichier — GetFileSizeEx après == avant,
             l'oracle le constate) ; rax = 0.
  inv  : I1 AUCUNE écriture hors des entrées du journal (le reste du
             fichier est INTACT — la différentielle avant/après le
             prouve : SEULEMENT les N octets du journal diffèrent,
             jamais un de plus) ;
         I2 l'ordre du journal est L'ORDRE DE SAISIE (loupe-16 I2) —
             la sauvegarde le suit tel quel, le témoin rend les
             adresses réelles ;
         I3 WriteFile et SetFilePointerEx vivent ICI SEULS dans le
             domaine (l'IAT fermée du plan — la contrebande
             d'écriture est un refus de build : loupe-16 l'a juré,
             le build le vérifie) ;
         I4 jamais la taille (I6 le constate : l'écriture à l'octet
             REMPLACE, elle n'étend pas — un hexadécimal éditeur ne
             crée pas d'octets) ; registres non volatils rendus ;
             NOP, 0x90.
Échecs :
  E1 : sans session ouverte (P1) → verdict -4 SESSION, rax = -4.
  E2 : SetFilePointerEx ou WriteFile en échec → verdict -6 SYSTÈME,
       le code GetLastError consigné, FAIL-CLOSED : journal et marque
       DEMEURENT (le geste se reprend — rien n'est perdu), le
       témoin ne ment pas (il ne rend que le succès complet).
Vecteurs :
  V1 : différentiel — 1 000 scénarios d'édition/sauvegarde sur les
       témoins : le fichier APRÈS == le modèle Python (les N octets
       appliqués, le reste INTACT — la comparaison octet par octet
       du fichier entier), la taille CONSTANTE (couvre Q2, Q6).
  V2 : scénario — trois octets édités puis Ctrl+S : le témoin « 3 o
       écrits · 0xA..0xC » à la barre, la marque levée, l'astérisque
       parti, le panneau RE-NAÎT (les empreintes du fichier changé —
       recoupées par hashlib) — l'écran attendu (couvre Q3, Q4, Q5).
  V3 : rejet — sans session : -4 ; le shim WriteFile en échec à la
       deuxième entrée : -6, la première écriture ACQUISE, le
       journal DEMEURE (le second Ctrl+S reprend et FINIT — la
       reprise est prouvée) (couvre E1, E2).
  V4 : scénario du repli — Ctrl+S sans édition : « rien à sauver »,
       AUCUN appel WriteFile (les appels comptés), rax = 0 (couvre
       Q1).
  V5 : falsification — un octet de trop écrit (la plage au lieu de
       l'octet) : la différentielle V1 échoue — l'écriture à l'octet
       est une exigence.
Fixtures    : les témoins du kit (édités puis sauvés puis RE-OUVERTS :
              la persistance constatée au second loupe-01 — la
              boucle complète de l'éditeur).
Provenance  : écrite-avant-code.
Décisions   : D171, D161, D7/D35 (l'IAT : WriteFile vit ici seul).
