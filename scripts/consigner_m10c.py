#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_m10c.py — LA CONSIGNATION DU CHANTIER M10-(c) RÉALISÉ : « LES
FAMILLES RENDU + NAVIGATION LOUPE-08..14 NOTÉ-MESURÉ-PROUVÉ ; L'ORACLE À
SCÉNARIOS VERT (l'écran attendu octet par octet pour des états donnés) ;
LA FALSIFICATION ATTRAPÉE ; LE MINI-GUI VIRTUEL DU HARNAIS ; LES HÉRITAGES
libc-02 ET win-03 AUX ADRESSES SCELLÉES ; LE PLANCHER QUI NE RECULE
JAMAIS (la correction du premier jet, attrapée par le témoin à
frontières) » : le plan reçoit la rangée (c) RÉALISÉE + la phrase de
l'État du programme, le journal reçoit l'Entrée 197, DECISIONS reçoit la
D174, le worklog reçoit la Task ID 115. Le garde sceau I (13 arbres
VERTS) passe AVANT toute écriture ; l'instrument VERT exigé AVANT ;
rejeu REFUSÉ ; tout ancrage absent ou compté autrement qu'UNE fois =
ÉCHEC NOMMÉ, rien n'est écrit. Les ancres État sont importées de
consigner_m10b (la chaîne des gestes tient sans retranscription)."""
import pathlib
import subprocess
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
DECISIONS = REPO / "docs" / "DECISIONS.md"
WORKLOG = REPO / "worklog.md"

sys.path.insert(0, str(REPO / "scripts"))
import consigner_m10b as _c196  # noqa: E402  # la chaîne des gestes

# --- l'État du programme : la phrase du M10-(c) remplace celle du (b) -------------

ANCIEN_ETAT = _c196.NOUVEL_ETAT   # l'État 196 (M10-(b) réalisé, la suite (c))

NOUVEL_ETAT = (
    "**LE CHANTIER M10-(c) RÉALISÉ le 08/11/2026 (Entrée 197, D174, "
    "Task 115) : LES FAMILLES RENDU + NAVIGATION LOUPE-08..14 "
    "NOTÉ-MESURÉ-PROUVÉES** — LE CRITÈRE DU PLAN TENU : l'oracle à "
    "scénarios VERT (l'écran attendu octet par octet pour des états "
    "donnés) ; la falsification attrapée. La notation 271/1614/568/796/"
    "126/983/874 o aux slots ARRÊTÉS sur les mesures (D161, la troisième "
    "passe : tassés 0x49C0→0x5F80 — loupe-10 LE PLUS GRAND BLOC DU GESTE "
    "1614 o, loupe-09 DERNIER : la table de routage s'étendra à (d) sans "
    "cascade) ; LES HÉRITAGES AUX ADRESSES SCELLÉES (la règle du geste "
    "(b) exécutée : libc-02 @0x1180 pour loupe-13, win-03 LA BOUCLE "
    "@0x15C0 pour loupe-09 — les octets de demo.exe 0.3.0, ses TROIS "
    "déplacements RIP visant l'IAT démo réservée @0x2818/0x2820/0x2828 ; "
    "la double preuve R7 : les extraits des scellés ET les notations "
    "d'origine ré-assemblées) ; L'INSTRUMENT loupe/harnais_rendu.py — LE "
    "MINI-GUI VIRTUEL (la file scriptée, le Dispatch qui appelle LA "
    "PROCÉDURE au pointeur enregistré, le DC qui enregistre chaque "
    "goutte, les échecs paramétrables, ExitProcess qui termine) : 53 "
    "contrôles · 53 VERTS × 3 graines (20261108, 424242, 777777) — le "
    "doré proxy, 1 500 lignes + 1 500 cas différentiels contre le modèle "
    "indépendant et bytes.find, LA CHAÎNE au fichier entier + LE "
    "RECOUVREMENT PAR CONSTRUCTION (le témoin à frontières : l'occurrence "
    "n'existe QU'à cheval, TROUVÉE — **LE PLANCHER QUI NE RECULE JAMAIS**, "
    "la correction du premier jet du geste), les bornes rejouées sur "
    "10 000 tailles, LES SCÉNARIOS DE LA VITRINE (l'écran attendu octet "
    "par octet : la vitrine vide, le témoin par la ligne de commande lue "
    "À LA MAIN, la cellule INVERSÉE à l'abscisse exacte, la marque sale "
    "nommée, le refus « fichier introuvable » à la barre la vitrine VIDE "
    "VRAIE, E1/E2 l'explication fatale PUIS ExitProcess(1)), LA "
    "FALSIFICATION DANS LES DEUX SENS (le remplissage muté → l'écran "
    "diverge ; le recadrage muté → le saut diverge ; la table HEX mutée "
    "→ chaque ligne diverge ; LE RECOUVREMENT MUTÉ → l'occurrence à "
    "cheval MANQUÉE puis TROUVÉE restauré — ctl_flush_tb : le cache de "
    "traduction vidé à chaque mutation, jamais une falsification muette "
    "par le cache). SUITE : M10-(d) l'édition + le kit terrain (loupe-15 "
    "curseur, 16 saisie, 17 sauver, 18 quitter — la table de loupe-09 "
    "s'y étendra ; le kit livré au /test, modèle m9f) ; la cérémonie "
    "d'ère du TGN attend son geste (le 14e arbre, AVANT tout build — la "
    "dette D166/D171 demeure)**"
)

# --- la rangée (c) du plan : le critère devient RÉALISÉ ---------------------------

RANGEE_ANCIENNE_C = ("| (c) Le rendu + la navigation | la ligne hexa, "
                     "l'écran, la peinture, le défilement, l'aller-à, la "
                     "recherche d'octets |")
RANGEE_NOUVELLE_C = (
    "| (c) Le rendu + la navigation — **RÉALISÉ (Entrée 197, D174)** : "
    "les 7 blocs notés-mesurés-prouvés (271/1614/568/796/126/983/874 o, "
    "les slots ARRÊTÉS sur les mesures), l'oracle à scénarios 53 VERTS × "
    "3 graines (le mini-GUI virtuel : la file scriptée, le DC qui "
    "enregistre, l'écran attendu octet par octet), les héritages "
    "libc-02 + win-03 aux adresses scellées, la falsification attrapée "
    "dans les deux sens | la ligne hexa, l'écran, la peinture, le "
    "défilement, l'aller-à, la recherche d'octets |")

# --- la D174 (append à la suite de D173) -------------------------------------------

D174 = """
## D174 — LE CHANTIER M10-(c) RÉALISÉ : LES FAMILLES RENDU + NAVIGATION LOUPE-08..14 NOTÉ-MESURÉ-PROUVÉES (le critère du plan TENU : l'oracle à scénarios VERT — l'écran attendu octet par octet pour des états donnés — et la falsification attrapée) ; LE MINI-GUI VIRTUEL DU HARNAIS (la file de messages scriptée, le Dispatch qui appelle LA PROCÉDURE au pointeur enregistré, le DC qui enregistre chaque goutte, les échecs paramétrables, ExitProcess qui termine) ; LES HÉRITAGES libc-02 ET win-03 AUX ADRESSES SCELLÉES (la règle du geste (b) exécutée : l'IAT démo @0x2818+ réservée aux déplacements scellés de la boucle)

**Le contexte qui fonde la décision (08/11, au soir).** La suite annoncée à l'Entrée 196 était M10-(c) : le rendu + la navigation (l'oracle à scénarios). Le développeur commande la suite (« ok continue »). Le modèle M10-(b) est rejoué au domaine neuf — AUCUN build : la cérémonie d'ère précède (D168 : la remise est exigée pour construire(), jamais pour la notation), la dette D166/D171 demeure, le garde reste à 13 arbres VERTS.

**Les règles.** (1) **L'ORDRE DU TASSEMENT, UNE RAISON D'ARCHITECTURE** : 08 (la feuille pure) · 10 (le peintre) · 11 · 12 · 13 (la feuille pure) · 14 (qui compose 12 et 13) · **LOUPE-09 DERNIER** — le bloc d'entrée (WinMain + LA PROCÉDURE) : sa table de routage S'ÉTENDRA au chantier (d) (les blocs 15-18 n'existent pas : leurs messages demeurent chez DefWindowProcW à (c), révision nommée à venir) ; placé DERNIER, l'extension ne bougera QUE son propre slot — les notations (c) de 08/10/11/12/13/14 demeurent INTACTES, la famille édition suivra à sa suite. Les appelés précèdent l'appelant. (2) **LA RÉSERVE D'ENTRÉE S'INCLINE (D161)** : la préfiguration 64 o @0x4000 ne tient pas l'écran mesuré (874 o) — WinMain vivra à SON slot (loupe-09, le dernier) et l'AddressOfEntryPoint du futur build visera LOUPE09_VA TEL QUEL (aucune fiction de trampoline : l'entrée est UNE adresse, celle du bloc). (3) **LES HÉRITAGES AUX ADRESSES SCELLÉES — LA RÈGLE DU GESTE (b) EXÉCUTÉE** : libc-02 memcmp POSE @0x1180 (loupe-13 teste chaque candidat par le scellé M1 — JAMAIS une boucle réécrite) et win-03 LA BOUCLE POSE @0x15C0 (loupe-09 l'appelle PAR LA CARTE : les octets de demo.exe 0.3.0, dont les TROIS déplacements RIP codés visent les slots IAT user32 DE L'IMAGE DÉMO — l'image loupe RÉSERVE les TROIS qwords @0x2818/0x2820/0x2828 : la double entrée n'est pas une redondance, c'est le PRIX du déplacement scellé ; la DOUBLE PREUVE : les extraits des scellés == les octets émulés ET les notations d'origine [m1/libc-02-memcmp, demo/win-03-boucle] ré-assemblées == les extraits). (4) **LE MINI-GUI VIRTUEL — LA PIÈCE NEUVE DU GESTE** : les 15 feuilles user32 + 6 gdi32 de l'IAT du geste servies par des shims à l'ABI msx64 — la file de messages SCRIPTÉE (GetMessageW dépile, la file vide rend WM_QUIT), **le Dispatch qui APPELLE LA PROCÉDURE au pointeur enregistré par RegisterClassExW** (la pile reçoit une adresse magique, rip vise la procédure, la réponse y revient — la mécanique EXACTE d'USER32 réduite au laboratoire, une seule emu_start plate), le DC qui ENREGISTRE chaque TextOutW avec ses coordonnées et ses couleurs (l'expansion latin-1 lue MOT À MOT), la police mesurée une fois (16/8), le client rect, l'ascenseur (GetScrollInfo nTrackPos / SetScrollInfo), les échecs paramétrables (BeginPaint nul, RegisterClassExW nul, la police muette), ExitProcess qui TERMINE l'émulation (le code consigné) ; les 5 feuilles du chantier (d) + GetModuleHandleW demeurent AU MORT (le compteur dénonce). (5) **L'ORACLE À SCÉNARIOS — LE CRITÈRE DU PLAN** : le modèle PYTHON INDÉPENDANT recompose l'écran attendu (la ligne 77 o du format du plan, l'entête, la grille bornée G = min(24, ceil(remplissage/16), lignes_affichables − 3), la barre-état, le panneau) depuis les TÉMOINS et l'état — JAMAIS depuis les octets du bloc — et la comparaison est OCTET PAR OCTET sur les 2320 o de la zone ECRAN ; les scénarios : la vitrine SANS session (l'usage, « - », l'ascenseur INTACT — le repli de loupe-11), le témoin ouvert PAR LA LIGNE DE COMMANDE (la session née AVANT la vitrine, le panneau == hashlib), la cellule active INVERSÉE à l'abscisse exacte (x = MARGE_X + (10 + 3·col + médian)·char_w), la marque sale (MODIFIÉ + l'astérisque), LE ROUTAGE CONSTATÉ (chaque message chez son bloc, les appels comptés un à un, DefWindowProcW pour le reste), le refus à l'ouverture (« fichier introuvable » à la barre, la vitrine VIDE VRAIE), E1/E2 (MessageBoxW PUIS ExitProcess(1), la boucle JAMAIS lancée). (6) **LE PLANCHER QUI NE RECULE JAMAIS — LA CORRECTION DU PREMIER JET** : le premier jet de loupe-14 repartait à départ zéro à chaque fenêtre — le recouvrement RE-TROUVAIT l'occurrence courante à l'infini (F3 immobile) ; le témoin à frontières (les occurrences n'existent QU'à cheval sur chaque frontière de 64 Kio) l'a attrapé AU PREMIER PASSAGE : le plancher de recherche ne recule jamais (une fenêtre manquée y avance le premier départ non examiné ; départ_rel = plancher − bord, borné à 0 — la règle de la spec lue dans toute sa portée). (7) **LES LECTURES DU GESTE (la notation confronte la spec, chaque lecture consignée)** : LA BARRE-ÉTAT AUX QUATRE MODES (0 RIEN · 1 ALLER · 2 CHERCHER · 3 MESSAGE = aucune saisie + le refus nommé au tampon — le « mode = 0 » des E1/E2/E3 de loupe-12/14 se lit LA SAISIE FERMÉE : la barre nomme, la saisie n'écoute plus ; l'acquittement par toute frappe ramène 0) ; LA BARRE ANCRÉE AU BAS (le panneau d'empreintes TOUJOURS visible — la grille cède la place : lignes_affichables − 3, l'entête + les deux lignes du panneau réservées ; la spec nommait la formule MARGE_Y + ligne·ligne_h pour chaque ligne de l'ECRAN : la grille la tient, la barre s'ancre au bas — l'oracle la juge) ; LE TIRET ASCII ET LE POINT MÉDIAN 0xB7 (l'expansion latin-1 EXACTE de loupe-10 I4 n'élève que 0x00-0xFF : l'ém-dash U+2014 de la spec ne vit qu'aux chaînes UTF-16 pilotées AUX API — le titre — jamais à la barre) ; LES CODES DE CONTRÔLE 0x06/0x07 PAR WM_CHAR (Ctrl+F ouvre CHERCHER, Ctrl+G ouvre ALLER : aucune feuille GetKeyState au plan, l'état du clavier ne se sonde pas, le caractère ctrl EST le message) ; LE CADRE RBP DE LOUPE-10 (les six sous-routines locales partagent le cadre du bloc — chaque local à son déplacement RBP STABLE à travers les appels internes, le 5e argument des TextOutW vivant à [rsp+0x20] dans la zone LIBRE du bas : aucun local n'y vit, jamais un clobber) ; LE hInstance DE L'ABI DE WINMAIN (rcx de l'entrée — D33 tenu par l'ABI ; GetModuleHandleW attend son geste, le mort le garde) ; loupe-10 porte GetLastError (E1/E2 : le code consigné — la spec l'exige, l'IAT du plan l'accepte, retiré de l'attribution InvalidateRect : le peintre ne s'invalide pas lui-même, I3 de loupe-09). (8) **LA FALSIFICATION — ctl_flush_tb** : le cache de traduction d'unicorn ne révoque pas toujours un bloc déjà traduit après une écriture mémoire (la mutation du geste fut d'abord muette PAR LE CACHE après 1 500 exécutions) : chaque mutation et restauration VIDE LE CACHE (uc.ctl_flush_tb, la voie officielle) — jamais une falsification muette par l'outil ; la falsification exigée DANS LES DEUX SENS (le muté diverge, le restauré re-passe).

**Le harnais (loupe/harnais_rendu.py — 53 contrôles · 53 VERTS × 3 graines [20261108, 424242, 777777]).** V0 les pièces (demo.exe relu md5+sha256 — l'ancre R7 de win-03 ; les SEPT specs relues ; les slots (c) recomptés : 08@0x49C0 → 10@0x4B00 → 11@0x5180 → 12@0x5400 → 13@0x5740 → 14@0x5800 → 09@0x5C00, fin 0x5F80 ; les adresses .rdata du rendu [l'entête, les tables HEX/HEXL, les 19 libellés, l'UTF-16], l'IAT démo) ; V1 le round-trip R5 × 7 + les déplacements RIP aux symboles du plan (121 déplacements) + les appels directs à la liste fermée (le réseau des specs) + les feuilles IAT par bloc + L'HÉRITAGE R7 CONSTATÉ (la double preuve) + LA PROCÉDURE relue depuis l'étiquette de sa notation + aucun syscall ; V2 loupe-08 (le doré proxy + la ligne finale incomplète + les 16 longueurs + 1 500 lignes différentielles == le modèle + les TROIS rejets la sortie INTACTE) ; V3 loupe-13 (le corpus de l'école + 1 500 cas == bytes.find, alphabets plein et pauvre + les marques de proxy + les TROIS rejets) ; V4 loupe-14 (LA CHAÎNE au fichier entier == bytes.find + LE RECOUVREMENT PAR CONSTRUCTION [le témoin à frontières, TROUVÉES aux trois] + 12 motifs différentiels sur 70 000 o + les rejets nommés : impairs/ZZ/vide → -5 « paires hexa attendues », sans session → -4, le ReadFile en échec → -6 relayé la position intacte) ; V5 les bornes (vue_max/clamp rejoués sur 10 000 tailles == la règle du plan) + les scénarios (le pas de TROIS lignes vérifié, LA POIGNÉE AU BOUT : la dernière fenêtre voit le dernier octet, l'ascenseur synchrone max == vue_max/16 ; le petit fichier : RIEN relu, les compteurs ; WM_SIZE recalculé ; le saut exact : le curseur à 0x1000, la vue recalée à la 12e ligne, L'ÉCRAN ATTENDU OCTET PAR OCTET ; le 9e chiffre ignoré, VK_SUPPR retire, VK_ECHAP annule TOUT ; les refus NOMMÉS à la barre : -5 « saisie mal formée », -3 « hors bornes », -4 « aucun fichier ouvert ») ; V6 L'ORACLE À SCÉNARIOS (les scénarios de la règle 5 — chaque écran == le modèle octet par octet) ; V7 LA FALSIFICATION (les quatre mutations + l'anti-muet aux 332 positions + LE RECOUVREMENT MUTÉ : l'occurrence à cheval MANQUÉE puis TROUVÉE — la preuve du recouvrement exigée DANS LES DEUX SENS).

**Alternatives rejetées.** Réserver l'IAT démo entière @0x2800-0x2868 (rejetée : seuls les TROIS slots visés par les déplacements scellés sont requis — la réserve minimale, le reste demeure au plan) ; un trampoline d'entrée @0x4000 (rejetée : l'entrée est UNE adresse, celle du bloc — D33 l'image PI, D161 la mesure décide ; des octets hors notation seraient une contrebande) ; GetKeyState pour les combinaisons (rejetée : les codes de contrôle vivent par WM_CHAR — aucune feuille supplémentaire, l'état du clavier ne se sonde pas) ; loupe-16 noté à (c) pour la table complète (rejetée : la découpe du plan est la loi — l'édition vit à (d), la table s'y étendra, la révision est nommée) ; garder le recouvrement à départ zéro (rejetée : le témoin à frontières démontre la re-trouvaille à l'infini — le plancher qui ne recule jamais est la règle, la correction est consignée) ; l'expansion UTF-16 complète à la barre (rejetée : I4 de loupe-10 EXIGE l'expansion latin-1 exacte 0x00-0xFF — le tiret ASCII et le point médian 0xB7, jamais U+2014 à la barre).

**Les frontières du geste.** AUCUN arbre signé touché (le garde sceau I vérifié AVANT consignation : 13 arbres VERTS, cle deposee reelle) ; le proxy 1.0.0 et la carte tls13 1.0.0 INTACTS (l'anti-rollback armé — les scellés sont LUS, jamais écrits) ; AUCUNE clé, AUCUN coffre réel, AUCUN fragment touchés ; la dette de cérémonie D166/D171 DEMEURE (le 14e arbre et l'extension du registre figé attendent la cérémonie d'ère — AVANT tout build, M10-(e)). Livrables : loupe/notation/brouillons/loupe-08..14.asm (les sept brouillons), loupe/notation/loupe-08..14.asm (les notations explicites), loupe/layout.py (l'adressage ARRÊTÉ : les slots (c), les pièces .rdata du rendu, les libellés, l'IAT démo, les modes de la saisie), loupe/outils/auteur.py (les sept blocs + les symboles du rendu), loupe/harnais_rendu.py (l'oracle à scénarios au mini-GUI virtuel), loupe/I/README.md (le chantier (c) COMPLET + les lectures du geste), le présent script.
"""

# --- l'Entrée 197 (avant le marqueur m5a) -----------------------------------------

ENTREE_197 = """## Entrée 197 — « ok continue » : LE CHANTIER M10-(c) RÉALISÉ — LES FAMILLES RENDU + NAVIGATION LOUPE-08..14 NOTÉ-MESURÉ-PROUVÉES ; L'ORACLE À SCÉNARIOS VERT (L'ÉCRAN ATTENDU OCTET PAR OCTET) ; LE MINI-GUI VIRTUEL DU HARNAIS ; LES HÉRITAGES libc-02 ET win-03 AUX ADRESSES SCELLÉES ; LA FALSIFICATION ATTRAPÉE DANS LES DEUX SENS (08/11)

**La reprise (l'état au geste).** Le M10-(b) réalisé à l'Entrée 196 (le noyau noté-mesuré-prouvé, les héritages aux adresses scellées, le mini-OS virtuel), le développeur commande la suite. La notation naît sous ses contrats — R2 tenue côté build : la cérémonie d'ère précède, la dette D166/D171 demeure, le garde à 13 arbres.

**Le geste : LES SEPT NOTATIONS DU RENDU + NAVIGATION.** Les brouillons loupe-08..14 (la mesure --mesurer D'ABORD : 271/1614/568/796/126/967→983/874 o, le plan ARRÊTÉ aux minimums — D161, la troisième passe ; slots 0x140/0x680/0x280/0x340/0xC0/0x400/0x380 tassés 0x49C0→0x5F80, loupe-09 DERNIER : la table s'étend à (d) sans cascade). loupe-08 la ligne (la feuille pure : la table HEX du plan par déplacement RIP, les 77 o exacts, les bornes AVANT la première écriture, les groupes absents deux espaces) ; loupe-10 la peinture (l'unique peintre : BeginPaint → la police mesurée UNE fois → le client à CHAQUE peinture → la composition [l'ECRAN 2320 o remis VIERGE, l'entête du plan, la grille par loupe-08 — G = min(24, ceil(remplissage/16), lignes_aff − 3) : la barre ancrée au bas, le panneau TOUJOURS visible] → la peinture [l'expansion latin-1 octet→mot, la cellule active en inverse EXPLICITE puis restaurée] → EndPaint ; E1 le DC nul SANS EndPaint, E2 l'abort propre EndPaint quand même) ; loupe-11 le défilement (le pas de TROIS lignes par cran, la poignée par GetScrollInfo, LA BORNE : la dernière fenêtre voit le dernier octet, le clamp AVANT la lecture, loupe-02 LA PREMIÈRE le refus relayé la vue inchangée, l'ascenseur TOUJOURS synchrone, WM_SIZE la garde ligne_h nulle) ; loupe-12 l'aller (la barre-saisie : aucun contrôle enfant, le gestionnaire PARTAGÉ — le RENVOI de loupe-14, le 9e ignoré, VK_ECHAP l'annulation propre, le commit : la valeur née du tampon, LA RÈGLE DE RECADRAGE du plan, loupe-02 puis InvalidateRect, le commit CHERCHER délégué à loupe-14) ; loupe-13 la recherche (la feuille pure : chaque candidat par LE SCELLÉ M1 libc-02 @0x1180, la position ABSOLUE de la PREMIÈRE ou −1, le 5e argument lu à l'entrée) ; loupe-14 le suivant (les paires hexa posées à la zone MOTIF, les fenêtres de 64 Kio lues à TAMPON_CUMUL, LE PLANCHER QUI NE RECULE JAMAIS, LE RECOUVREMENT bord + 64 Kio − (longueur − 1), la FIN NOMMÉE le motif demeure) ; loupe-09 l'écran (WinMain : la ligne de commande lue À LA MAIN — le programme sauté, guillemets honorés, la session née AVANT la vitrine, le refus nommé monte à la barre la vitrine VIDE VRAIE ; la classe SUR LA PILE, lpfnWndProc = LA PROCÉDURE par lea, la vitrine 640×480, HWND posé, LA BOUCLE HÉRITÉE win-03 @0x15C0, ExitProcess ; LA PROCÉDURE : les quatre arguments aux non-volatils avant tout appel [D38], WM_PAINT→10, WM_SIZE/WM_VSCROLL/WM_MOUSEWHEEL→11, F5→12, F3→14, WM_CHAR la saisie active→12, 0x06→14, 0x07→12, le reste→DefWindowProcW, TOUT verdict négatif monte à la barre par .monter — jamais un refus muet).

**L'instrument : LE MINI-GUI VIRTUEL (loupe/harnais_rendu.py).** La file de messages SCRIPTÉE, LE DISPATCH QUI APPELLE LA PROCÉDURE au pointeur enregistré par RegisterClassExW (l'adresse magique rend la réponse — la mécanique d'USER32 réduite, une seule emu_start plate), le DC qui ENREGISTRE chaque goutte (les coordonnées, les couleurs, les mots), la police mesurée une fois, l'ascenseur, les échecs paramétrables, ExitProcess qui termine. LE CAHIER V0-V7 : 53 contrôles · 53 VERTS × 3 graines (20261108, 424242, 777777). V0 les pièces (demo.exe relu — l'ancre R7 de win-03 ; les specs ; les slots ; les .rdata du rendu) ; V1 le round-trip R5 × 7, les 121 déplacements RIP aux symboles, le réseau des appels, l'IAT par bloc, LA DOUBLE PREUVE R7 (libc-02 ET win-03) ; V2/V3 les différentiels (1 500 lignes == le modèle indépendant ; 1 500 cas == bytes.find ; le doré proxy) ; V4 LA CHAÎNE + LE RECOUVREMENT PAR CONSTRUCTION (le témoin à frontières : TROUVÉES aux trois) ; V5 les bornes + les scénarios (le saut exact, L'ÉCRAN ATTENDU OCTET PAR OCTET, les refus NOMMÉS à la barre) ; V6 L'ORACLE (la vitrine vide, le témoin par la ligne de commande, la cellule INVERSÉE, la marque sale, LE ROUTAGE CONSTATÉ, le refus à l'ouverture, E1/E2) ; V7 LA FALSIFICATION (les quatre mutations, LE RECOUVREMENT MUTÉ manqué puis trouvé, l'anti-muet).

**LA CORRECTION DU PREMIER JET (consignée pour les chantiers suivants).** LE PLANCHER QUI NE RECULE JAMAIS : le premier jet de loupe-14 repartait à départ zéro à chaque fenêtre — F3 re-trouvait l'occurrence courante à l'infini ; le témoin à frontières l'a attrapé au premier passage. LE CACHE DE TRADUCTION : la mutation fut d'abord muette PAR L'OUTIL (unicorn ne révoque pas toujours le bloc traduit après une écriture mémoire) — ctl_flush_tb à chaque mutation, la voie officielle. LE SUB rcx, 0xb0 : l'immédiat 32 bits vit à adresse+3 (le PREMIER octet), jamais au dernier — la cible de mutation lue sur les octets, pas devinée.

**Détail.** FRONTIÈRES : AUCUN arbre signé touché ; le garde sceau I vérifié AVANT consignation : 13 arbres VERTS, cle deposee reelle (D87) ; le proxy 1.0.0 et la carte tls13 INTACTS (lus, jamais écrits) ; la dette de cérémonie D166/D171 DEMEURE (le 14e arbre attend la cérémonie d'ère — AVANT tout build). Livrables : loupe/notation/brouillons/loupe-08..14.asm, loupe/notation/loupe-08..14.asm, loupe/layout.py, loupe/outils/auteur.py, loupe/harnais_rendu.py, loupe/I/README.md, le présent script. Consignations : la présente Entrée PAR SCRIPT, la D174 PAR SCRIPT (docs/DECISIONS.md), le PLAN (la rangée (c) RÉALISÉE + la phrase de l'État), worklog +Task ID 115. SUITE : M10-(d) L'ÉDITION + LE KIT TERRAIN (loupe-15 curseur, 16 saisie, 17 sauver, 18 quitter ; la table de loupe-09 s'étendra — révision nommée ; le kit livré au /test, modèle m9f) ; la cérémonie d'ère du TGN attend son geste (le kit au /Cérémonie, la main du développeur, le garde passant à 14 arbres) ; le projet fils attend son premier geste à son message propre.

"""

# --- la Task ID 115 (append au worklog) -------------------------------------------

TASK_115 = """
## Task ID 115 — LE CHANTIER M10-(c) RÉALISÉ : LES FAMILLES RENDU + NAVIGATION LOUPE-08..14 NOTÉ-MESURÉ-PROUVÉES (L'ORACLE À SCÉNARIOS VERT — L'ÉCRAN ATTENDU OCTET PAR OCTET ; LE MINI-GUI VIRTUEL ; LE RECOUVREMENT PAR CONSTRUCTION ; LA FALSIFICATION DANS LES DEUX SENS) (08/11)

- La suite annoncée à l'Entrée 196 ; le développeur commande (« ok
  continue »). AUCUN build : la cérémonie d'ère précède (D168), la dette
  D166/D171 demeure, le garde à 13 arbres.
- LES SEPT NOTATIONS : 08 la ligne (271 o, la feuille pure, la table HEX
  du plan) · 10 la peinture (1614 o, L'UNIQUE PEINTRE — le plus grand
  bloc du geste : la composition VIERGE, la grille par loupe-08 bornée
  lignes_aff − 3 [la barre ancrée au bas], l'expansion latin-1, la
  cellule en inverse explicite) · 11 le défilement (568 o : le pas, la
  poignée, LA BORNE, loupe-02 la première, l'ascenseur synchrone) · 12
  l'aller (796 o : la barre-saisie partagée, le saut exact, LA RÈGLE DE
  RECADRAGE, les refus nommés) · 13 la recherche (126 o, la feuille pure
  : chaque candidat par LE SCELLÉ M1) · 14 le suivant (983 o : LE
  PLANCHER QUI NE RECULE JAMAIS, LE RECOUVREMENT, la FIN nommée) · 09
  l'écran (874 o, DERNIER : WinMain + LA PROCÉDURE, la table s'étendra à
  (d) sans cascade).
- LES HÉRITAGES AUX ADRESSES SCELLÉES : libc-02 @0x1180 (loupe-13) et
  win-03 @0x15C0 (loupe-09 — les octets de demo.exe 0.3.0, l'IAT démo
  @0x2818/0x2820/0x2828 réservée : le prix du déplacement scellé) ; la
  DOUBLE PREUVE R7 (les extraits == les émulés ET les notations
  d'origine ré-assemblées == les extraits).
- LE MINI-GUI VIRTUEL : la file scriptée, le Dispatch qui appelle LA
  PROCÉDURE au pointeur enregistré, le DC qui enregistre, les échecs
  paramétrables, ExitProcess qui termine ; les 5 feuilles du (d) +
  GetModuleHandleW au mort.
- LE VERDICT : 53 contrôles · 53 VERTS × 3 graines — le doré proxy, les
  différentiels (1 500 + 1 500 == le modèle et bytes.find), LA CHAÎNE au
  fichier entier, LE RECOUVREMENT PAR CONSTRUCTION (le témoin à
  frontières), les bornes sur 10 000 tailles, LES SCÉNARIOS (l'écran
  attendu OCTET PAR OCTET : la vitrine vide, le témoin par la ligne de
  commande, la cellule inversée, la marque sale, le routage compté, le
  refus à l'ouverture, E1/E2), LA FALSIFICATION (quatre mutations + le
  recouvrement muté manqué puis trouvé + l'anti-muet ; ctl_flush_tb à
  chaque geste).
- LES LEÇONS DU GESTE : le plancher qui ne recule jamais (le premier jet
  re-trouvait l'occurrence courante — le témoin à frontières l'a
  attrapé) ; le cache de traduction vidé à chaque mutation (la voie
  officielle, jamais une falsification muette par l'outil) ; l'immédiat
  32 bits à adresse+3.
- FRONTIÈRES : AUCUN arbre signé touché ; le garde sceau I : 13 arbres
  VERTS (cle deposee reelle) vérifié AVANT consignation ; le proxy 1.0.0
  et la carte tls13 INTACTS. Livrables : les brouillons + les notations
  loupe-08..14, loupe/layout.py (l'adressage ARRÊTÉ du geste), loupe/
  outils/auteur.py, loupe/harnais_rendu.py (l'oracle), loupe/I/README.md,
  scripts/consigner_m10c.py.
- SUITE : M10-(d) l'édition + le kit terrain (15-18, la table de loupe-09
  étendue, le kit au /test modèle m9f) ; la cérémonie d'ère du TGN attend
  son geste (le 14e arbre, avant tout build) ; le projet fils attend son
  premier geste à son message propre.
"""


def main():
    # 0. le garde AVANT consignation (la discipline du projet)
    r = subprocess.run(["python3", str(REPO / "v06" / "sceau_I.py"),
                        "verifier"], capture_output=True, text=True)
    if "13 arbres VERTS" not in r.stdout:
        sys.exit("ÉCHEC : le garde sceau I ne constate pas 13 arbres VERTS "
                 f"— consignation REFUSÉE\n{r.stdout[-400:]}")
    print("GARDE : 13 arbres VERTS (cle deposee reelle) — la consignation "
          "peut suivre")

    # 0bis. l'instrument du chantier AVANT consignation (le geste se prouve)
    r = subprocess.run(["python3", str(REPO / "loupe" / "harnais_rendu.py")],
                       capture_output=True, text=True)
    if "VERDICT : VERT" not in r.stdout or r.returncode != 0:
        sys.exit("ÉCHEC : l'instrument loupe/harnais_rendu.py n'est pas VERT "
                 f"— consignation REFUSÉE\n{r.stdout[-600:]}")
    n_controles = r.stdout.count("[ok] ")
    print(f"INSTRUMENT : loupe/harnais_rendu.py VERT ({n_controles} contrôles)"
          " — le geste se prouve avant de se consigner")

    # 1. le plan : la rangée (c) RÉALISÉE + l'État (idempotent)
    plan = PLAN.read_text(encoding="utf-8")
    if "RÉALISÉ (Entrée 197, D174)" in plan:
        print("PLAN : la rangée (c) RÉALISÉE déjà consignée — constaté")
    else:
        if plan.count(RANGEE_ANCIENNE_C) != 1:
            sys.exit(f"ÉCHEC : la rangée (c) OUVERTE trouvée "
                     f"{plan.count(RANGEE_ANCIENNE_C)} fois (attendu : 1)")
        if plan.count(ANCIEN_ETAT) != 1:
            sys.exit(f"ÉCHEC : ancrage État trouvé "
                     f"{plan.count(ANCIEN_ETAT)} fois (attendu : 1)")
        plan = plan.replace(RANGEE_ANCIENNE_C, RANGEE_NOUVELLE_C, 1)
        plan = plan.replace(ANCIEN_ETAT, NOUVEL_ETAT, 1)
        if "RÉALISÉ (Entrée 197, D174)" not in plan:
            sys.exit("ÉCHEC : la rangée (c) absente après remplacement")
        if "LE CHANTIER M10-(c) RÉALISÉ le 08/11/2026" not in plan:
            sys.exit("ÉCHEC : l'État ne porte pas la phrase du M10-(c)")
        PLAN.write_text(plan, encoding="utf-8")
        print("PLAN : la rangée (c) RÉALISÉE + l'État du programme — consignés")

    # 2. le journal : l'Entrée 197 avant le marqueur m5a (idempotent)
    journal = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 197 —" in journal:
        print("JOURNAL : l'Entrée 197 déjà consignée — constaté")
    else:
        marqueur = "<!-- m5a:journal-des-builds v1"
        if journal.count(marqueur) != 1:
            sys.exit(f"ÉCHEC : le marqueur m5a trouvé "
                     f"{journal.count(marqueur)} fois (attendu : 1)")
        journal = journal.replace(marqueur, ENTREE_197 + marqueur, 1)
        if "## Entrée 197 — « ok continue »" not in journal:
            sys.exit("ÉCHEC : l'Entrée 197 absente après remplacement")
        JOURNAL.write_text(journal, encoding="utf-8")
        print("JOURNAL : l'Entrée 197 consignée AVANT le marqueur m5a")

    # 3. le registre des décisions : la D174 à la suite de D173
    decisions = DECISIONS.read_text(encoding="utf-8")
    if "## D174 —" in decisions:
        print("DECISIONS : la D174 déjà consignée — constaté")
    else:
        if decisions.count("## D173 —") != 1:
            sys.exit("ÉCHEC : la D173 absente ou multiple (le geste "
                     "précédent n'est pas consigné)")
        decisions = decisions.rstrip("\n") + "\n" + D174.strip("\n") + "\n"
        if "## D174 — LE CHANTIER M10-(c) RÉALISÉ" not in decisions:
            sys.exit("ÉCHEC : la D174 absente après append")
        DECISIONS.write_text(decisions, encoding="utf-8")
        print("DECISIONS : la D174 consignée À LA SUITE de la D173")

    # 4. le worklog racine : la Task ID 115 à la suite de la 114
    worklog = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 115 —" in worklog:
        sys.exit("ÉCHEC : la Task ID 115 existe déjà (rejeu REFUSÉ)")
    if worklog.count("## Task ID 114 —") != 1:
        sys.exit("ÉCHEC : l'entrée Task ID 114 absente ou multiple (le geste "
                 "précédent n'est pas consigné)")
    worklog = worklog.rstrip("\n") + "\n" + TASK_115
    if "## Task ID 115 — LE CHANTIER M10-(c) RÉALISÉ" not in worklog:
        sys.exit("ÉCHEC : la Task ID 115 absente après append")
    WORKLOG.write_text(worklog, encoding="utf-8")
    print("WORKLOG : la Task ID 115 consignée À LA SUITE de la Task 114")


if __name__ == "__main__":
    main()
