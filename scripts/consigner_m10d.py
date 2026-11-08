#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_m10d.py — LA CONSIGNATION DU CHANTIER M10-(d), PREMIÈRE MOITIÉ :
« LA FAMILLE ÉDITION LOUPE-15..18 + LA TABLE DE ROUTAGE DE LOUPE-09 ÉTENDUE
(r2, LA RÉVISION NOMMÉE DU GESTE (c) TENUE) NOTÉES-MESURÉES-PROUVÉES ; LE
DISQUE SAISISSABLE ET LA MORT DU HARNAIS (WriteFile, DestroyWindow qui
ENVOIE WM_DESTROY par LA MÊME MÉCANIQUE que le Dispatch, PostQuitMessage,
MessageBeep) ; LE RÉSEAU DE LA GARDE 16↔17↔18 PAR TOUS LES CHEMINS ; LA
VUE QUI SUIT L'AVANCE (l'invariant du domaine tenu à la saisie) ;
L'ÉCRITURE À L'OCTET (le disque APRÈS == le modèle, SEULEMENT les N octets,
la taille CONSTANTE) ; LA FALSIFICATION ATTRAPÉE (quatre mutants) » : le
plan reçoit la rangée (d) LA NOTATION RÉALISÉE (le kit attend LA CÉRÉMONIE
D'ÈRE — le 14e arbre, AVANT tout build), le journal reçoit l'Entrée 198,
DECISIONS reçoit la D175, le worklog reçoit la Task ID 116. Le garde sceau
I (13 arbres VERTS) passe AVANT toute écriture ; l'instrument VERT exigé
AVANT ; rejeu REFUSÉ ; tout ancrage absent ou compté autrement qu'UNE fois
= ÉCHEC NOMMÉ, rien n'est écrit. Les ancres État sont importées de
consigner_m10c (la chaîne des gestes tient sans retranscription)."""
import pathlib
import subprocess
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
DECISIONS = REPO / "docs" / "DECISIONS.md"
WORKLOG = REPO / "worklog.md"

sys.path.insert(0, str(REPO / "scripts"))
import consigner_m10c as _c197  # noqa: E402  # la chaîne des gestes

# --- l'État du programme : la phrase du M10-(d) remplace celle du (c) -------------

ANCIEN_ETAT = _c197.NOUVEL_ETAT   # l'État 197 (M10-(c) réalisé, la suite (d))

NOUVEL_ETAT = (
    "**LE CHANTIER M10-(d), PREMIÈRE MOITIÉ, RÉALISÉ le 08/11/2026 au soir "
    "(Entrée 198, D175, Task 116) : LA FAMILLE ÉDITION LOUPE-15..18 + LA "
    "TABLE DE ROUTAGE DE LOUPE-09 ÉTENDUE NOTÉES-MESURÉES-PROUVÉES** — la "
    "notation 391/660/521/163 o aux slots ARRÊTÉS sur les mesures (D161, "
    "la quatrième passe : 15 @0x6080 · 16 @0x6240 · 17 @0x6500 · 18 "
    "@0x6740 — fin 0x6800) et LOUPE-09 r2 CROÎT 874 → 1135 o (LA RÉVISION "
    "NOMMÉE DU GESTE (c) TENUE : WM_CLOSE/WM_DESTROY → loupe-18, les huit "
    "flèches HORS SAISIE → loupe-15, Ctrl+S 0x13 par WM_CHAR → loupe-17, "
    "VK_SUPPR et les seize chiffres hexa → loupe-16 — SANS CASCADE : les "
    "notations (c) de 08/10/11/12/13/14 INTACTES) ; L'INSTRUMENT loupe/"
    "harnais_edition.py — LE DISQUE SAISISSABLE ET LA MORT (le WriteFile à "
    "l'octet dans le fichier virtuel, l'échec armé au Nième appel ; "
    "DestroyWindow qui ENVOIE WM_DESTROY à la procédure PAR LA MÊME "
    "MÉCANIQUE que le Dispatch — la mort de la fenêtre est la mécanique "
    "EXACTE d'USER32 réduite au laboratoire ; PostQuitMessage la file "
    "quittée ; MessageBeep le coup enregistré) : 45 contrôles · 45 VERTS × "
    "3 graines (20261108, 424242, 777777) — le différentiel 10 000 touches "
    "+ 10 000 frappes + 1 000 scénarios de sauvegarde == le modèle Python "
    "indépendant (le disque APRÈS : SEULEMENT les N octets diffèrent, la "
    "taille CONSTANTE), LE TÉMOIN « N o écrits · 0x…..0x… » composé et "
    "peint, LE RÉSEAU DE LA GARDE 16↔17↔18 par tous les chemins (la perte "
    "est une volonté DEUX FOIS nommée), LA MORT COMPLÈTE au scénario (le "
    "fichier SAUVÉ re-ouvert : la persistance, les empreintes recoupées "
    "hashlib ; ET l'abandon délibéré : le disque INTACT), LA FALSIFICATION "
    "ATTRAPÉE (la vue qui suit mutée — le curseur sort de l'écran ; la "
    "garde de 16 non ré-armée — la perte d'un seul geste ; la garde de 17 "
    "non levée — l'avertissement pour rien ; l'octet de trop — la plage au "
    "lieu de l'octet). LE KIT TERRAIN ATTEND LA CÉRÉMONIE D'ÈRE (le 14e "
    "arbre, AVANT tout build — la dette D166/D171 DEMEURE, le garde à 13 "
    "arbres VERTS). SUITE : la cérémonie d'ère du TGN (le geste hors-ligne "
    "du développeur, la remise 14 arbres, le garde passant à 14) PUIS le "
    "build + le kit terrain (M10-(d) seconde moitié) et le run terrain "
    "(M10-(e))**"
)

# --- la rangée (d) du plan : la notation RÉALISÉE, le kit attend la cérémonie -----

RANGEE_ANCIENNE_D = ("| (d) L'édition + le kit terrain | curseur, saisie, "
                     "sauver, quitter ; le kit livré au /test (modèle m9f : "
                     "double-clic, témoin, réceptacle) |")
RANGEE_NOUVELLE_D = (
    "| (d) L'édition + le kit terrain — **LA NOTATION RÉALISÉE (Entrée "
    "198, D175)** : les 4 blocs notés-mesurés-prouvés (391/660/521/163 o) "
    "+ loupe-09 r2 LA TABLE ÉTENDUE (1135 o, la révision nommée tenue "
    "sans cascade), l'oracle 45 VERTS × 3 graines (le disque saisissable, "
    "la mort complète, LE RÉSEAU de la garde, la falsification) ; LE KIT "
    "ATTEND LA CÉRÉMONIE D'ÈRE (le 14e arbre, AVANT tout build) | "
    "curseur, saisie, sauver, quitter ; le kit livré au /test (modèle "
    "m9f : double-clic, témoin, réceptacle) |")

# --- la D175 (append à la suite de D174) -------------------------------------------

D175 = """
## D175 — LE CHANTIER M10-(d), PREMIÈRE MOITIÉ, RÉALISÉ : LA FAMILLE ÉDITION LOUPE-15..18 + LA TABLE DE ROUTAGE DE LOUPE-09 ÉTENDUE (r2) NOTÉES-MESURÉES-PROUVÉES (le disque saisissable et la mort du harnais ; le réseau de la garde 16↔17↔18 par tous les chemins ; l'écriture à l'octet prouvée différentielle) ; LE KIT TERRAIN ATTEND LA CÉRÉMONIE D'ÈRE (la dette D166/D171 nommée : le 14e arbre avant tout build)

**Le contexte qui fonde la décision (08/11, au soir).** La suite annoncée à l'Entrée 197 était M10-(d) : l'édition + le kit terrain. Le développeur commande la suite (« continue M10… »). LA DÉCOUPE DU PLAN EST LA LOI : la notation de l'édition est un geste de LABO (la cérémonie d'ère précède le BUILD, jamais la notation — le miroir M8/M9, Entrées 157/158 : la remise est exigée pour construire()) ; le kit terrain, lui, exige le build — LA CÉRÉMONIE D'ÈRE LE PRÉCÈDE DONC : le chantier se coupe en deux moitiés, la première réalisée ici (la famille notée-mesurée-prouvée), la seconde (le build loupe.exe + le kit livré au /test, modèle m9f) attend le geste hors-ligne du développeur. AUCUN build : la dette D166/D171 demeure, le garde reste à 13 arbres VERTS.

**Les règles.** (1) **LA TABLE DE ROUTAGE ÉTENDUE — LA RÉVISION NOMMÉE TENUE** : la promesse du geste (c) (« la table de routage s'étendra au chantier (d) sans cascade sur les autres notations ») est EXÉCUTÉE — loupe-09 croît de 874 → 1135 o (slot 0x380 → 0x480) : WM_DESTROY 0x0002 et WM_CLOSE 0x0010 → loupe-18, les HUIT flèches (VK_PRIOR/NEXT/END/HOME/LEFT/UP/RIGHT/DOWN, 0x21..0x28 d'un seul encadrement) HORS SAISIE (mode = 0) → loupe-15, Ctrl+S 0x13 PAR WM_CHAR (LE CODE DE CONTRÔLE — la voie du geste (c) pour 0x06/0x07 : aucune feuille GetKeyState au plan, l'état du clavier ne se sonde pas) → loupe-17, VK_SUPPR et les SEIZE chiffres hexa (les minuscules portées aux majuscules) → loupe-16 ; les notations (c) de 08/10/11/12/13/14 demeurent INTACTES (aucun octet bougé — la promesse tenue sur pièces), la famille édition suit À LA SUITE du slot croissant. (2) **L'ATTENTE CONSOMMÉE PAR L'ENGAGEMENT** : « le premier chiffre attend, le second ENGAGE » (la spec de loupe-16) se lit dans toute sa portée : l'engagement CONSOMME l'attente (succès OU refus — jamais un nibble zombie en attente), le premier chiffre SAUVÉ À r10d AVANT la consommation (la leçon du premier jet : la zone effacée avant la lecture, l'octet se serait composé du second chiffre seul — le journal portait 0x0D pour « 4d », l'écran attendu l'a attrapé AU PREMIER PASSAGE) ; VK_SUPPR à l'attente efface actif ET valeur (l'état NET). (3) **LA VUE SUIT L'AVANCE — L'INVARIANT DU DOMAINE** : « le curseur ne sort JAMAIS de l'écran » (le README du domaine) tient AUSSI à la saisie : le pas de loupe-16 (Q4 : le curseur AVANCE) porte LE RENVOI de loupe-15 Q3 (la même règle : les lignes visibles de la vitrine — METRIQUES.lignes − 3, capées 24, LA LECTURE STRICTE de la spec [jamais perdu hors écran, y compris la vitrine rétrécie ; à la vitrine 0.1.0 la fenêtre == le remplissage 384 : le miroir exact du commit de loupe-12] — le recadrage du plan, loupe-02 LA PREMIÈRE le refus relayé la vue inchangée) ; la relecture SEULEMENT au recadrage (le harnais compte les lectures : la vue ne bouge QUE POUR SUIVRE). (4) **L'ÉCRITURE À L'OCTET — L'UNITÉ EST L'OCTET** : loupe-17 écrit CHAQUE entrée du journal DANS SON ORDRE DE SAISIE par SetFilePointerEx + WriteFile d'UN SEUL octet (jamais une plage ; le pointeur d'écrits NUL : la poignée est synchrone) ; l'échec est FAIL-CLOSED (le journal DEMEURE, la marque demeure, les octets déjà écrits le restent — l'échec ne perd RIEN, le geste se reprend : le second Ctrl+S REPREND ET FINIT, prouvé) ; LE TÉMOIN « N o écrits · 0xAABBCCDD..0xEEFFGGHH » composé AVANT LA VIDANGE (le journal est la source du témoin : dec + chaine + hex8, LES SOUS-ROUTINES LOCALES AU CADRE RBP — le modèle loupe-10). (5) **LE RÉSEAU DE LA GARDE 16↔17↔18** : la perte d'octets non sauvés exige DEUX gestes — loupe-16 RÉ-ARME la garde à CHAQUE écriture (refus_quitter = 0 : après une nouvelle écriture, le premier Alt+F4 re-vient avertir), loupe-17 la LÈVE à chaque sauvegarde réussie, loupe-18 la POSE au premier refus (la phrase à la barre « MODIFIÉ - Alt+F4 encore pour quitter sans sauver, Ctrl+S pour sauver », MessageBeep : le refus s'entend, verdict -5) et ne tranche qu'au second (DestroyWindow) ; WM_DESTROY (envoyé par DestroyWindow) ferme la session par loupe-03 (le journal ABANDONNÉ DÉLIBÉRÉMENT — les octets non sauvés sont une VOLONTÉ), PostQuitMessage(0) rend la boucle héritée win-03, WinMain retourne, ExitProcess(0) — la sortie ne sauvegarde JAMAIS elle-même. (6) **LE DISQUE SAISISSABLE ET LA MORT — LES PIÈCES NEUVVES DU HARNAIS** : l'OS virtuel gagne un WriteFile à l'ABI msx64 (l'écriture à la position de la poignée dans le fichier virtuel SAISISSABLE — FichierEditable : le contenu matérialisé à la première écriture, TOUJOURS des bytes au lecteur [unicorn refuse les bytearray — la leçon du premier passage], l'échec armé au Nième appel, le journal des écritures) ; le GUI virtuel gagne ses trois feuilles de sortie : DestroyWindow (qui ENVOIE WM_DESTROY à la procédure PAR LA MÊME MÉCANIQUE que le Dispatch — la pile reçoit l'adresse magique, rip vise la procédure : la mort de la fenêtre est la mécanique EXACTE d'USER32 réduite au laboratoire), PostQuitMessage (la file quittée — GetMessageW rend 0, la boucle héritée rend), MessageBeep (le coup enregistré) ; les QUATRE feuilles du (d) VIVENT à l'IAT, GetModuleHandleW SEUL demeure au mort (le hInstance de l'ABI de WinMain, D174). (7) **LES REJETS NOMMÉS DE L'ÉDITION** : sans session -4 « aucun fichier ouvert » (16/17) ; LA CELLULE FANTÔME -3 « hors bornes » (le curseur forgé hors [vue, vue+remplissage) : un état forgé, le curseur visible étant l'invariant — RIEN au journal, le refus PRÉCÈDE ; le fichier VIDE y vit : aucune cellule n'existe) ; LE JOURNAL PLEIN -3 « journal plein - Ctrl+S » (256 DISTINCTS : RIEN perdu, l'octet refusé n'entre pas) ; le non-hexa IGNORÉ proprement (les seize chiffres seuls écoutent) ; « rien à sauver » (le journal vide : l'état nommé, PAS un échec, AUCUN WriteFile compté).

**Le harnais (loupe/harnais_edition.py — 45 contrôles · 45 VERTS × 3 graines [20261108, 424242, 777777]).** V0 les pièces (les TROIS scellés relus — proxy.exe 1.0.0, selftest.exe M1, demo.exe 0.3.0 : les ancres R7 ; les QUATRE specs du geste ; les slots (d) recomptés : 09 r2 @0x5C00 [0x480] → 15 @0x6080 [0x1C0] → 16 @0x6240 [0x2C0] → 17 @0x6500 [0x240] → 18 @0x6740 [0xC0], fin 0x6800 ; les 5 libellés du (d) @0x2520-0x259E ; LA TABLE ÉTENDUE déclarée dès la spec R1 du geste (a)) ; V1 le round-trip R5 × 5 + les appels directs à la liste fermée (les sous-routines locales exceptées) + LA ROUTE CONSTATÉE (VK_BAS → 15 le curseur bouge ; la touche hors table ET les flèches EN MODE SAISIE → DefWindowProcW comptées le curseur INTACT ; '4' → 16 le nibble en attente ; 'z' → le défaut ; Ctrl+S → 17 « rien à sauver » AUCUN WriteFile ; WM_CLOSE → 18 : DestroyWindow → WM_DESTROY ENVOYÉ → loupe-03 + PostQuitMessage — LA MORT COMPLÈTE, la poignée rendue) ; V2 loupe-15 (le différentiel 10 000 touches == le modèle à CHAQUE pas : le curseur ET la vue, la relecture EXACTEMENT quand la vue bouge ; LES BORDS des arrêts NOMMÉS rax = 0 quand même la vue INTACTE ; VK_DEBUT/VK_FIN à la ligne finale incomplète — la fin RÉELLE ; LA VUE SUIT à l'écran attendu octet par octet ; LA VITRINE RÉTRÉCIE la lecture stricte ; le repli sans session ; LE VIDE aucune cellule) ; V3 loupe-16 (le différentiel 10 000 frappes : le journal PAR DÉCALAGE, le remplacement, la borne 256 refusée NOMMÉMENT, l'attente consommée, le tampon, la marque, la garde, le pas, la vue — le modèle indépendant ; le scénario « 4d » L'ÉCRAN ATTENDU ; LES REJETS ; VK_SUPPR à l'attente ; LA GARDE RÉ-ARMÉE après la sauvegarde) ; V4 loupe-17 (le différentiel 1 000 scénarios : le disque APRÈS == le modèle SEULEMENT les N octets, la taille CONSTANTE, EXACTEMENT N WriteFile ; LE TÉMOIN à la barre + le panneau RE-NÉ == hashlib + l'astérisque parti — l'écran attendu ; « rien à sauver » AUCUN appel compté ; L'ÉCHEC FAIL-CLOSED : le 2e WriteFile refuse, le premier ACQUIS, le journal DEMEURE, le second Ctrl+S REPREND ET FINIT ; sans session -4) ; V5 loupe-18 (la sortie directe ; LE DOUBLE-GESTE : le refus -5, LA PHRASE, LE BEEP, la fenêtre DEMEURE, le second tranche ; LE RÉSEAU par tous les chemins ; WM_DESTROY le disque INTACT — l'abandon) ; V6 L'ORACLE À SCÉNARIOS (LA BOUCLE COMPLÈTE par la ligne de commande : ouvrir, éditer, sauver, peindre, Alt+F4 — LA MORT COMPLÈTE le disque SAUVÉ == le modèle, ExitProcess(0) ; LE CHEMIN DE L'ABANDON : le refus, le beep, le second geste, LE FICHIER INTACT ; LA RÉ-OUVERTURE : la persistance, les empreintes recoupées hashlib ; LE TÉMOIN peint à la barre) ; V7 LA FALSIFICATION (la vue qui suit MUTÉE : le curseur sort de l'écran — restauré la vue suit ; LA GARDE DE 16 non ré-armée : la perte d'un seul geste — restaurée le refus revient ; LA GARDE DE 17 non levée : l'avertissement pour rien — restaurée le quitte-après-sauvegarde ; L'OCTET DE TROP : l'écriture mutée à 2 o — restaurée UN octet exactement ; l'anti-muet du témoin).

**Alternatives rejetées.** Couper le (d) en deux chantiers du plan (rejetée : la rangée demeure UNE — la découpe se consigne DANS la rangée, la notation réalisée, le kit attend la cérémonie : le plan est la loi, la cérémonie est la porte de processus) ; loupe-16 appelant loupe-15 pour la vue (rejetée : la règle est RÉ-ÉCRITE locale — le domaine ne connaît pas de 19e bloc, le renvoi est nommé) ; garder le nibble après l'engagement (rejetée : « le second chiffre engage » — l'attente CONSOMMÉE, succès ou refus ; le premier jet laissait la zone vivante : la comparaison du harnais l'a attrapé) ; composer le témoin APRÈS la vidange (rejetée : le journal est la SOURCE du témoin — vidé d'abord, le témoin mentirait) ; l'écriture par plage (rejetée : l'unité est l'octet, I4 de loupe-17 — un hexadécimal éditeur ne crée pas d'octets ; le mutant à 2 o le prouve) ; GetKeyState pour Ctrl+S (rejetée : 0x13 par WM_CHAR, la voie des codes — aucune feuille de plus).

**Les frontières du geste.** AUCUN arbre signé touché (le garde sceau I vérifié AVANT consignation : 13 arbres VERTS, cle deposee reelle) ; le proxy 1.0.0 et la carte tls13 INTACTS ; AUCUNE clé, AUCUN coffre réel, AUCUN fragment touchés ; la dette de cérémonie D166/D171 DEMEURE (le 14e arbre et l'extension du registre figé attendent la cérémonie d'ère — AVANT tout build, la seconde moitié du (d)). Livrables : loupe/notation/brouillons/loupe-15..18.asm (les quatre brouillons) + loupe-09-ecran.asm (la table étendue), loupe/notation/loupe-15..18.asm + loupe-09-ecran.asm (les notations explicites), loupe/layout.py (l'adressage ARRÊTÉ : les slots (d), les 5 libellés @0x2520+, les constantes du journal, Ctrl_S/WM_DESTRUCTION), loupe/outils/auteur.py (les 18 blocs — la couche du domaine ENTIÈRE), loupe/harnais_edition.py (l'oracle au disque saisissable et à la mort), le présent script.
"""

# --- l'Entrée 198 (avant le marqueur m5a) -----------------------------------------

ENTREE_198 = """## Entrée 198 — « continue M10 » : LE CHANTIER M10-(d), PREMIÈRE MOITIÉ, RÉALISÉ — LA FAMILLE ÉDITION LOUPE-15..18 + LA TABLE DE ROUTAGE DE LOUPE-09 ÉTENDUE NOTÉES-MESURÉES-PROUVÉES ; LE DISQUE SAISISSABLE ET LA MORT DU HARNAIS ; LE RÉSEAU DE LA GARDE 16↔17↔18 ; L'ÉCRITURE À L'OCTET PROUVÉE DIFFÉRENTIELLE ; LE KIT TERRAIN ATTEND LA CÉRÉMONIE D'ÈRE (08/11 au soir)

**La reprise (l'état au geste).** Le M10-(c) réalisé à l'Entrée 197 (le rendu + la navigation, l'oracle à scénarios vert), le développeur commande la suite — M10, la rangée (d) : l'édition + le kit terrain. La découpe du plan est la loi : la notation est un geste de labo, le kit un geste de build — LA CÉRÉMONIE D'ÈRE PRÉCÈDE LE BUILD (le miroir M8/M9) : le chantier se coupe en deux, la première moitié réalisée ici.

**Le geste : LES QUATRE NOTATIONS DE L'ÉDITION + LA TABLE ÉTENDUE.** Les brouillons loupe-15..18 (la mesure --mesurer D'ABORD : 391/660/521/163 o, le plan ARRÊTÉ aux minimums — D161, la quatrième passe ; 15 @0x6080 [0x1C0] · 16 @0x6240 [0x2C0] · 17 @0x6500 [0x240] · 18 @0x6740 [0xC0], fin 0x6800) et loupe-09 r2 (874 → 1135 o, slot 0x480 : LA RÉVISION NOMMÉE du geste (c) tenue — la table étendue SANS CASCADE, les notations (c) voisines INTACTES). loupe-15 le curseur (le pas ±1/±16/±352, VK_DEBUT l'aligne16_inf, VK_FIN la fin de ligne RÉELLE min(aligne16+15, taille-1) ; LA BORNE les bords SONT DES ARRÊTS rax = 0 quand même ; LA VUE SUIT aux LIGNES VISIBLES de la vitrine — la lecture STRICTE, capée 24 : jamais perdu hors écran Y COMPRIS la vitrine rétrécie ; loupe-02 la première au recadrage, la relecture SEULEMENT quand la vue bouge ; le repli sans session et LE VIDE) ; loupe-16 la saisie (le premier chiffre ATTEND, le second ENGAGE — l'attente CONSOMMÉE par l'engagement, le premier chiffre SAUVÉ À r10d avant la consommation ; l'octet AU JOURNAL PAR DÉCALAGE la réécriture REMPLACE, la borne 256 -3 « journal plein - Ctrl+S » RIEN perdu ; ET À LA VUE l'octet visible IMMÉDIATEMENT ; la marque + LA GARDE RÉ-ARMÉE à chaque écriture + le pas + LA VUE SUIT L'AVANCE — l'invariant du domaine ; VK_SUPPR à l'attente ; la cellule fantôme -3 le refus PRÉCÈDE le journal ; LE DISQUE INTACT — WriteFile vit chez loupe-17 seul) ; loupe-17 la sauvegarde (« rien à sauver » sans édition AUCUN appel compté ; CHAQUE entrée à son décalage UNE PAR UNE SetFilePointerEx + WriteFile d'UN octet — l'échec -6 FAIL-CLOSED le journal demeure le geste se reprend ; le succès : journal vidé marque levée garde levée ; LE PANNEAU RE-NAÎT loupe-07 rappelé — les empreintes du DISQUE, le coût nommé ; LE TÉMOIN « N o écrits · 0x…..0x… » composé AVANT la vidange — dec + hex8 au cadre RBP, le modèle loupe-10) ; loupe-18 la sortie (LE DOUBLE-GESTE GARANTI : marque + garde → le premier WM_CLOSE REFUSÉ NOMMÉMENT -5, LA PHRASE à la barre, MessageBeep, la fenêtre DEMEURE ; le second TRANSCHE DestroyWindow ; WM_DESTROY : loupe-03 la session close — le journal ABANDONNÉ DÉLIBÉRÉMENT — PostQuitMessage(0), la boucle héritée rend, ExitProcess(0) ; la sortie ne sauvegarde JAMAIS elle-même ; AUCUNE fuite).

**L'instrument : LE DISQUE SAISISSABLE ET LA MORT (loupe/harnais_edition.py).** Le WriteFile à l'ABI msx64 dans le fichier virtuel SAISISSABLE (FichierEditable — le contenu matérialisé, TOUJOURS des bytes au lecteur ; l'échec armé au Nième appel) ; DestroyWindow qui ENVOIE WM_DESTROY à la procédure PAR LA MÊME MÉCANIQUE que le Dispatch (l'adresse magique, rip à la procédure — la mort d'USER32 réduite au laboratoire) ; PostQuitMessage (la file quittée) ; MessageBeep (le coup enregistré). LE CAHIER V0-V7 : 45 contrôles · 45 VERTS × 3 graines (20261108, 424242, 777777).

**LES LEÇONS DU PREMIER JET (consignées pour les chantiers suivants).** L'ATTENTE CONSOMMÉE : le premier jet effaçait la zone AVANT de lire le premier chiffre — l'octet se composait du second seul (le journal portait 0x0D pour « 4d »), L'ÉCRAN ATTENDU l'a attrapé au premier passage (deux octets divergents : le chiffre hexa ET le miroir ASCII) ; la règle : le SAUVÉ à r10d avant la consommation. L'ÉTAT QUI FUIT ENTRE LES VECTEURS : le premier jet ne remettait pas la zone SAISIE au vierge entre les scénarios — l'attente de V1.c survivot à V3.a (le bloc avait raison, le harnais fautait) ; la règle : reset_saisie AVANT chaque scénario qui écoute. LE BYTEARRAY : unicorn refuse les bytearray à mem_write — le disque saisissable rend TOUJOURS des bytes au lecteur. LES DÉPLACEMENTS CAPSTONE EN HEXADÉCIMAL : la cible d'une falsification se cherche « [rbx + 0x218] », jamais « [rbx + 536] » — l'outil rend hexa, la source écrit décimal.

**Détail.** FRONTIÈRES : AUCUN arbre signé touché ; le garde sceau I vérifié AVANT consignation : 13 arbres VERTS, cle deposee reelle (D87) ; le proxy 1.0.0 et la carte tls13 INTACTS ; la dette de cérémonie D166/D171 DEMEURE (le 14e arbre attend la cérémonie d'ère — AVANT tout build). Livrables : les brouillons + les notations loupe-15..18 et loupe-09 r2, loupe/layout.py, loupe/outils/auteur.py (les 18 blocs), loupe/harnais_edition.py, le présent script. Consignations : la présente Entrée PAR SCRIPT, la D175 PAR SCRIPT (docs/DECISIONS.md), le PLAN (la rangée (d) LA NOTATION RÉALISÉE + la phrase de l'État), worklog +Task ID 116. SUITE : LA CÉRÉMONIE D'ÈRE DU TGN (le geste hors-ligne du développeur : signer la remise 14 arbres à la clé du 04/11, ramener signatures + clé publique au coffre /test — le kit de cérémonie au /Cérémonie, la charge FRAÎCHE régénérée au geste) PUIS le build loupe 0.1.0-dev.1 + le kit terrain (M10-(d) seconde moitié, modèle m9f) et le run terrain (M10-(e)) ; le projet fils attend son premier geste à son message propre.

"""

# --- la Task ID 116 (append au worklog) -------------------------------------------

TASK_116 = """
## Task ID 116 — LE CHANTIER M10-(d), PREMIÈRE MOITIÉ, RÉALISÉ : LA FAMILLE ÉDITION LOUPE-15..18 + LA TABLE DE ROUTAGE DE LOUPE-09 ÉTENDUE (r2) NOTÉES-MESURÉES-PROUVÉES (LE DISQUE SAISISSABLE ET LA MORT ; LE RÉSEAU DE LA GARDE ; L'ÉCRITURE À L'OCTET PROUVÉE DIFFÉRENTIELLE) — LE KIT ATTEND LA CÉRÉMONIE (08/11 au soir)

- La suite annoncée à l'Entrée 197 ; le développeur commande (« continue
  M10 »). La notation est un geste de LABO, le kit un geste de BUILD — la
  cérémonie d'ère précède le build : le chantier coupé en deux, la
  première moitié réalisée. AUCUN build, le garde à 13 arbres.
- LOUPE-09 r2 : LA TABLE ÉTENDUE (1135 o, 874 → : WM_CLOSE/WM_DESTROY →
  18, les huit flèches HORS SAISIE → 15, Ctrl+S 0x13 par WM_CHAR → 17,
  VK_SUPPR et les seize chiffres → 16) — SANS CASCADE : les notations
  (c) de 08/10/11/12/13/14 INTACTES, la promesse du geste (c) tenue.
- LES QUATRE NOTATIONS : 15 le curseur (391 o : le pas, la borne les
  arrêts NOMMÉS, LA VUE SUIT aux lignes visibles — la lecture stricte,
  jamais perdu hors écran y compris la vitrine rétrécie ; la relecture
  SEULEMENT au recadrage) · 16 la saisie (660 o : l'attente CONSOMMÉE par
  l'engagement — le premier chiffre SAUVÉ À r10d avant la consommation ;
  le journal PAR DÉCALAGE, la borne 256, LA GARDE RÉ-ARMÉE, LA VUE SUIT
  L'AVANCE — l'invariant du domaine ; la cellule fantôme le refus
  PRÉCÈDE ; LE DISQUE INTACT) · 17 la sauvegarde (521 o : l'écriture À
  L'OCTET une par une, l'échec FAIL-CLOSED, LE PANNEAU RE-NÉ, LE TÉMOIN
  composé avant la vidange) · 18 la sortie (163 o : LE DOUBLE-GESTE
  GARANTI, la phrase + le beep au refus, loupe-03 + PostQuitMessage à la
  mort, la sortie ne sauvegarde JAMAIS elle-même).
- LE HARNAIS — LE DISQUE SAISISSABLE ET LA MORT : WriteFile à l'ABI
  msx64 (l'échec armé au Nième appel) ; DestroyWindow qui ENVOIE
  WM_DESTROY PAR LA MÊME MÉCANIQUE que le Dispatch ; PostQuitMessage ;
  MessageBeep ; les QUATRE feuilles du (d) VIVANTES à l'IAT,
  GetModuleHandleW seul au mort.
- LE VERDICT : 45 contrôles · 45 VERTS × 3 graines (20261108, 424242,
  777777) — le différentiel 10 000 touches + 10 000 frappes + 1 000
  scénarios == le modèle (le disque APRÈS : SEULEMENT les N octets, la
  taille CONSTANTE), LE TÉMOIN composé et peint, LE RÉSEAU DE LA GARDE
  par tous les chemins, LA BOUCLE COMPLÈTE au scénario (sauvé ET abandon,
  la persistance recoupée hashlib), LA FALSIFICATION (quatre mutants :
  la vue qui suit, les deux gardes, l'octet de trop).
- LES LEÇONS DU PREMIER JET : l'attente consommée (le sauvé à r10d
  AVANT l'effacement — l'écran attendu a attrapé l'octet 0x0D pour
  « 4d ») ; la zone SAISIE remise au vierge entre les scénarios (l'état
  qui fuit) ; les bytes au lecteur (unicorn refuse les bytearray) ; les
  déplacements capstone en HEXA.
- FRONTIÈRES : AUCUN arbre signé touché ; le garde sceau I : 13 arbres
  VERTS (cle deposee reelle) vérifié AVANT consignation ; le proxy 1.0.0
  et la carte tls13 INTACTS. Livrables : les brouillons + les notations
  loupe-15..18 + loupe-09 r2, loupe/layout.py (les slots (d) ARRÊTÉS,
  les 5 libellés @0x2520+, les constantes du journal), loupe/outils/
  auteur.py (les 18 blocs), loupe/harnais_edition.py,
  scripts/consigner_m10d.py.
- SUITE : LA CÉRÉMONIE D'ÈRE DU TGN (le geste hors-ligne du développeur
  — la remise 14 arbres, la clé du 04/11, les pièces au /test) PUIS le
  build + le kit terrain (M10-(d) seconde moitié) et le run terrain
  (M10-(e)) ; le projet fils attend son premier geste à son message
  propre.
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
    r = subprocess.run(["python3", str(REPO / "loupe" / "harnais_edition.py")],
                       capture_output=True, text=True)
    if "VERDICT : VERT" not in r.stdout or r.returncode != 0:
        sys.exit("ÉCHEC : l'instrument loupe/harnais_edition.py n'est pas "
                 f"VERT — consignation REFUSÉE\n{r.stdout[-600:]}")
    n_controles = r.stdout.count("[ok] ")
    print(f"INSTRUMENT : loupe/harnais_edition.py VERT ({n_controles} "
          "contrôles) — le geste se prouve avant de se consigner")

    # 1. le plan : la rangée (d) LA NOTATION RÉALISÉE + l'État (idempotent)
    plan = PLAN.read_text(encoding="utf-8")
    if "LA NOTATION RÉALISÉE (Entrée 198, D175)" in plan:
        print("PLAN : la rangée (d) LA NOTATION RÉALISÉE déjà consignée — "
              "constaté")
    else:
        if plan.count(RANGEE_ANCIENNE_D) != 1:
            sys.exit(f"ÉCHEC : la rangée (d) OUVERTE trouvée "
                     f"{plan.count(RANGEE_ANCIENNE_D)} fois (attendu : 1)")
        if plan.count(ANCIEN_ETAT) != 1:
            sys.exit(f"ÉCHEC : ancrage État trouvé "
                     f"{plan.count(ANCIEN_ETAT)} fois (attendu : 1)")
        plan = plan.replace(RANGEE_ANCIENNE_D, RANGEE_NOUVELLE_D, 1)
        plan = plan.replace(ANCIEN_ETAT, NOUVEL_ETAT, 1)
        if "LA NOTATION RÉALISÉE (Entrée 198, D175)" not in plan:
            sys.exit("ÉCHEC : la rangée (d) absente après remplacement")
        if "LE CHANTIER M10-(d), PREMIÈRE MOITIÉ, RÉALISÉ le 08/11/2026" \
                not in plan:
            sys.exit("ÉCHEC : l'État ne porte pas la phrase du M10-(d)")
        PLAN.write_text(plan, encoding="utf-8")
        print("PLAN : la rangée (d) LA NOTATION RÉALISÉE (le kit attend la "
              "cérémonie) + l'État du programme — consignés")

    # 2. le journal : l'Entrée 198 avant le marqueur m5a (idempotent)
    journal = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 198 —" in journal:
        print("JOURNAL : l'Entrée 198 déjà consignée — constaté")
    else:
        marqueur = "<!-- m5a:journal-des-builds v1"
        if journal.count(marqueur) != 1:
            sys.exit(f"ÉCHEC : le marqueur m5a trouvé "
                     f"{journal.count(marqueur)} fois (attendu : 1)")
        journal = journal.replace(marqueur, ENTREE_198 + marqueur, 1)
        if "## Entrée 198 — « continue M10 »" not in journal:
            sys.exit("ÉCHEC : l'Entrée 198 absente après remplacement")
        JOURNAL.write_text(journal, encoding="utf-8")
        print("JOURNAL : l'Entrée 198 consignée AVANT le marqueur m5a")

    # 3. le registre des décisions : la D175 à la suite de D174
    decisions = DECISIONS.read_text(encoding="utf-8")
    if "## D175 —" in decisions:
        print("DECISIONS : la D175 déjà consignée — constaté")
    else:
        if decisions.count("## D174 —") != 1:
            sys.exit("ÉCHEC : la D174 absente ou multiple (le geste "
                     "précédent n'est pas consigné)")
        decisions = decisions.rstrip("\n") + "\n" + D175.strip("\n") + "\n"
        if "## D175 — LE CHANTIER M10-(d), PREMIÈRE MOITIÉ, RÉALISÉ" \
                not in decisions:
            sys.exit("ÉCHEC : la D175 absente après append")
        DECISIONS.write_text(decisions, encoding="utf-8")
        print("DECISIONS : la D175 consignée À LA SUITE de la D174")

    # 4. le worklog racine : la Task ID 116 à la suite de la 115
    worklog = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 116 —" in worklog:
        sys.exit("ÉCHEC : la Task ID 116 existe déjà (rejeu REFUSÉ)")
    if worklog.count("## Task ID 115 —") != 1:
        sys.exit("ÉCHEC : l'entrée Task ID 115 absente ou multiple (le geste "
                 "précédent n'est pas consigné)")
    worklog = worklog.rstrip("\n") + "\n" + TASK_116
    if "## Task ID 116 — LE CHANTIER M10-(d), PREMIÈRE MOITIÉ, RÉALISÉ" \
            not in worklog:
        sys.exit("ÉCHEC : la Task ID 116 absente après append")
    WORKLOG.write_text(worklog, encoding="utf-8")
    print("WORKLOG : la Task ID 116 consignée À LA SUITE de la Task 115")


if __name__ == "__main__":
    main()
