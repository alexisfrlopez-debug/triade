#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_m10b.py — LA CONSIGNATION DU CHANTIER M10-(b) RÉALISÉ : « LE
NOYAU NOTÉ-MESURÉ-PROUVÉ (loupe-01..07, fichier + empreintes) ; LES
HÉRITAGES VIVENT À LEURS ADRESSES SCELLÉES (la découverte du geste) ; LE
MINI-OS VIRTUEL (les six shims kernel32, le FS virtuel aux témoins réels,
les échecs paramétrables, le journal des gle) ; L'INSTRUMENT
loupe/harnais_noyau.py VERT (59 contrôles × 3 graines) ; LES RÉVISIONS
NOMMÉES DE LOUPE-01 (r2 l'erratum de la taille de la pièce, r3 LE VIDE) » :
le plan reçoit la rangée (b) RÉALISÉE + la phrase de l'État du programme,
le journal reçoit l'Entrée 196, DECISIONS reçoit la D173, le worklog
reçoit la Task ID 114. Le garde sceau I (13 arbres VERTS) passe AVANT
toute écriture ; l'instrument VERT exigé AVANT ; rejeu REFUSÉ ; tout
ancrage absent ou compté autrement qu'UNE fois = ÉCHEC NOMMÉ, rien n'est
écrit. Les ancres État sont importées de consigner_m10a (la chaîne des
gestes tient sans retranscription)."""
import pathlib
import subprocess
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
DECISIONS = REPO / "docs" / "DECISIONS.md"
WORKLOG = REPO / "worklog.md"

sys.path.insert(0, str(REPO / "scripts"))
import consigner_m10a as _c195  # noqa: E402  # la chaîne des gestes

# --- l'État du programme : la phrase du M10-(b) remplace celle du (a) -------------

ANCIEN_ETAT = _c195.NOUVEL_ETAT   # l'État 195 (M10-(a) réalisé, la suite (b))

NOUVEL_ETAT = (
    "**LE CHANTIER M10-(b) RÉALISÉ le 08/11/2026 (Entrée 196, D173, "
    "Task 114) : LE NOYAU LOUPE-01..07 NOTÉ-MESURÉ-PROUVÉ** — fichier + "
    "empreintes, la notation 47/388/296/122/312/879/102 o aux slots "
    "ARRÊTÉS sur les mesures (D161 rejoué, le mode --mesurer de l'auteur ; "
    "loupe-06 LA NOTATION NEUVE RFC 1321 : 879 o, le plus grand bloc du "
    "noyau) ; **LES HÉRITAGES VIVENT À LEURS ADRESSES SCELLÉES** (la "
    "découverte du geste : tls13-02 porte un déplacement RIP codé pour "
    "0xC080 visant K[64] @0x2F00 — l'image neuve réserve .text M1 pour la "
    "minilibc, 0xC000-0xC3C0 pour la famille sha, la table K laissée au "
    "scellé ; les octets hérités ne bougent JAMAIS d'un pouce, R7 au "
    "sens propre) ; LE MINI-OS VIRTUEL du harnais (les six shims "
    "kernel32, le FS virtuel aux témoins réels dont proxy.exe scellé, les "
    "échecs paramétrables, le journal des gle, le compteur du mort) ; "
    "l'instrument loupe/harnais_noyau.py — 59 contrôles · 59 VERTS × 3 "
    "graines (20261108, 424242, 777777) : les SEPT vecteurs RFC 1321 au "
    "fichier, 1 000 gammes md5 + 200 sha contre hashlib, LA PIÈCE DE "
    "L'ÈRE JUGÉE PAR SA PROPRE APPLICATION (loupe-05 sur proxy.exe == "
    "446279f3…), l'héritage CONSTATÉ byte-identique (la double preuve), "
    "les ONZE rejets nommés, la falsification attrapée par les vecteurs "
    "officiels ; les révisions nommées de loupe-01 (r2 : la taille de la "
    "pièce 65 024 o ; r3 : LE VIDE s'ouvre sans fenêtre, son panneau "
    "existe). SUITE : M10-(c) le rendu + la navigation (l'oracle à "
    "scénarios) ; la cérémonie d'ère du TGN attend son geste (le 14e "
    "arbre, AVANT tout build — la dette D166/D171 demeure)**"
)

# --- la rangée (b) du plan : le critère devient RÉALISÉ ---------------------------

RANGEE_ANCIENNE_B = ("| (b) Le noyau — fichier + empreintes | ouvrir/lire/"
                     "fermer + sha-256/md5 d'une gamme + le cumul du "
                     "fichier entier par fenêtres glissantes |")
RANGEE_NOUVELLE_B = (
    "| (b) Le noyau — fichier + empreintes — **RÉALISÉ (Entrée 196, "
    "D173)** : les 7 blocs notés-mesurés-prouvés (47/388/296/122/312/"
    "879/102 o, les slots ARRÊTÉS sur les mesures), les héritages posés "
    "AUX ADRESSES SCELLÉES, le harnais au mini-OS virtuel 59 VERTS × 3 "
    "graines | ouvrir/lire/fermer + sha-256/md5 d'une gamme + le cumul du "
    "fichier entier par fenêtres glissantes |")

# --- la D173 (append à la suite de D172) -------------------------------------------

D173 = """
## D173 — LE CHANTIER M10-(b) RÉALISÉ : LE NOYAU LOUPE-01..07 NOTÉ-MESURÉ-PROUVÉ (fichier + empreintes, la notation aux slots ARRÊTÉS sur les longueurs réelles — D161 rejoué) ; LES HÉRITAGES VIVENT À LEURS ADRESSES SCELLÉES (la découverte du geste : le déplacement RIP de tls13-02 est codé pour 0xC080 — une relocalisation ré-écrite serait une contrebande de R7 ET un déplacement faux) ; LE MINI-OS VIRTUEL DU HARNAIS (les six shims kernel32 aux ABI msx64, le système de fichiers virtuel aux témoins réels, les échecs paramétrables, le journal des gle)

**Le contexte qui fonde la décision (08/11).** La suite annoncée à l'Entrée 195 était M10-(b) : le noyau (ouvrir/lire/fermer + les empreintes, le harnais différentiel sur vecteurs officiels + fichiers réels, l'héritage sha constaté byte-identique — R7). Le développeur commande la suite (« ok pour la suite », puis « continue »). Le modèle M9-(b) est rejoué au domaine neuf — AUCUN build : la cérémonie d'ère précède (D168 : la remise est exigée pour le chantier construire(), jamais pour la notation), la dette D166/D171 demeure, le garde reste à 13 arbres VERTS.

**Les règles.** (1) **LA MESURE AVANT L'ARRÊT** (D161, rejoué avec un outil NEUF : le mode --mesurer de loupe/outils/auteur.py — la première passe du chantier rend les longueurs SANS écrire, le plan s'arrête aux minimums, la préfiguration s'incline) : 47/388/296/122/312/879/102 o -> slots 0x40/0x1C0/0x140/0xC0/0x180/0x380/0x80, tassés @0x4040-0x49C0, multiples de 64, padding >= 16. (2) **LES HÉRITAGES VIVENT À LEURS ADRESSES SCELLÉES** — LA DÉCOUVERTE DU GESTE : le premier jet posait les octets hérités à des slots neufs (0x1140…) ; l'émulation a CRASHÉ dans tls13-02 sur « lea rbp, [rip - 0x91a4] » : le déplacement est CODÉ POUR L'ADRESSE SCELLÉE (0xC080, visant K[64] @0x2F00) — déplacer les octets casserait le déplacement, les re-réécrire serait une contrebande de R7. L'image neuve RÉSERVE donc les plages : .text 0x1000-0x1FFF la minilibc aux adresses M1 (libc-01 @0x1100, libc-02 @0x1180 RÉSERVÉE pour le chantier navigation, libc-07 @0x13C0), .rdata 0x2000-0x2FFF (les tables MD5 @0x2100/0x2200, l'IAT @0x2400-0x2510, K[64] @0x2F00 LA TABLE DU SCELLÉ — le plan loupe RENVOIE à tls13/layout.py, jamais re-déclarée), .text2 0x4000-0xBFFF les blocs du domaine (0x4000 la réserve d'entrée pour WinMain/loupe-09), 0xC000-0xC3C0 la famille sha aux adresses M9, .data @0xE000 les zones (CUMUL @0x10000, fin 0x20000). La règle pour les chantiers suivants : tout héritage se pose à SON adresse scellée d'origine (win-03 et son IAT démo @0x2810+ au chantier rendu). (3) **LE MINI-OS VIRTUEL** — LA PIÈCE NEUVE DU GESTE : le noyau touche le monde par SIX feuilles kernel32 (CreateFileW, GetFileSizeEx, SetFilePointerEx, ReadFile, CloseHandle, GetLastError — la liste fermée des specs) ; le harnais dote l'émulation de shims à l'ABI msx64 : le système de fichiers virtuel aux témoins réels (proxy.exe scellé INCLUS — la pièce de l'ère jugée par sa propre application), les échecs PARAMÉTRABLES (le Nième ReadFile en échec : E4 de loupe-02/05/06), le journal des gle (I4 : le code consigné, jamais un code brut à la barre), le COMPTEUR DU MORT (les 28 feuilles IAT hors noyau pointent vers une adresse dont l'appel est DÉNONCÉ — la liste fermée tenue sur pièces). (4) **LE VERDICT VIT DANS EAX** (la leçon du premier passage : « mov eax, -N » zéro-étend rax — le harnais lit le verdict 32 bits SIGNÉ, la table des SEPT verdicts vit en eax, charte § 9 ; les poignées 64 bits ne transitent jamais par rax, le cadre les porte). (5) **L'ORDRE DES REGISTRES AU RÉSEAU DES APPELS** (la leçon du premier crash de loupe-01 : loupe-04 détruit rcx pour son memset — le chemin est sauvé AVANT l'appel et RECHARGÉ avant CreateFileW ; l'ABI se rejoue à CHAQUE frontière, jamais une confiance héritée). (6) **LA BORNE 2 Gio DANS LES OCTETS** : « mov eax, 0x80000000 » (le zéro-étendu : le bord exact 0x80000000 est ACCEPTÉ, le refus est strictement au-delà) + cmp/jbe — le refus de 2 Gio + 1 est PROUVÉ AU COMPORTEMENT avec la poignée REFERMÉE comptée ; l'intégrale 2 Gio vivra au terrain (le kit M10-(d) : le natif la calcule en secondes, l'émulation en heures — la découpe honnête nommée). (7) **LES RÉVISIONS NOMMÉES DE LA COUCHE I** : loupe-01 r2 (l'erratum fixtures : la taille 44 544 était celle du scellé 0.9.0 de l'ère close, la pièce 1.0.0 mesure 65 024 o — l'empreinte 446279f3… était la bonne) ; loupe-01 r3 (LE VIDE : le fichier de taille zéro est un fichier réel du quotidien que l'éditeur DOIT ouvrir — la fenêtre n'existe pas pour lui [loupe-02 P3 : tout décalage >= taille 0], le remplissage 0, LE PANNEAU DU VIDE EXISTE : d41d8cd9… + e3b0c442…) ; loupe-06 porte libc-07 en dépendance (les zéros du bourre PAR LA CARTE — l'héritage déclaré est l'héritage utilisé).

**Le harnais (loupe/harnais_noyau.py — 59 contrôles · 59 VERTS × 3 graines [20261108, 424242, 777777]).** V0 les pièces (les scellés relus, l'erratum r2 CONSTATÉ sur pièces, les slots/les zones/l'IAT recomptés) ; V1 le round-trip R5 (keystone == capstone sur les SEPT notations, les longueurs == les mesures de l'arrêt), les déplacements RIP aux symboles du plan, les appels directs à la liste fermée (le réseau des specs), les feuilles IAT par bloc, LES CONSTANTES MD5 RE-DÉRIVÉES PAR ARITHMÉTIQUE (les 64 T par sinus, les S, les abscisses), **L'HÉRITAGE R7 CONSTATÉ BYTE-IDENTIQUE — LA DOUBLE PREUVE** (les octets émulés == les EXTRAITS DES SCELLÉS [selftest.exe pour la minilibc, proxy.exe 1.0.0 pour la famille sha] ET les notations d'origine ré-assemblées == les extraits), aucun syscall ; V2 LES SEPT VECTEURS OFFICIELS RFC 1321 AU FICHIER (chaque attendu RECROISÉ à hashlib — l'instrument se contrôle avant de juger), la gamme vide, 1 000 gammes aléatoires, le témoin 3×64 Kio + 1 ENTIER par fenêtres glissantes ; V3 LE DIFFÉRENTIEL SHA : **LA PIÈCE DE L'ÈRE JUGÉE PAR SA PROPRE APPLICATION** (loupe-05(0, 65024) sur le fichier virtuel alimenté par les octets RÉELS du proxy scellé == hashlib == 446279f3…00d93d), les vecteurs FIPS au fichier, 200 gammes sha ; V4 le noyau fichier (le cadre vierge 960 o recomposé octet par octet depuis un état sale, la session née entière CHAMP À CHAMP, le panneau né, LE FICHIER VIDE [révision 3 en preuve], 1 060 fenêtres bornées, LE RECOUVREMENT du journal [l'édition survit au défilement], la fermeture idempotence-comptée, l'hygiène des zones, les zones des chantiers suivants INTACTES) ; V5 LES ONZE REJETS NOMMÉS (absent -2/verrouillé -7/accès -6 au journal des gle, la borne 2 Gio + 1 -3 LA POIGNÉE REFERMÉE COMPTÉE, la session double -5 L'ANCIEN INTACT, le chemin 260 -5, les quatre de loupe-02, les trois × deux de gammes, le -6 du shim partout avec la sortie INTACTE et le remplissage 0, le refus PROPAGÉ par loupe-01 LA SESSION CLOSE) ; V6 LA FALSIFICATION (T[1] muté d'un ulp : 7/7 vecteurs dorés échouent — ATTRAPÉS PAR LES VECTEURS OFFICIELS avec rax = 0 exigé [jamais un vert par accident de refus], la table restaurée re-passe, l'anti-muet 16 octets, le tampon de vue INTACT pendant le calcul [l'exclusion de famille], le journal INTACT, le panneau TOUJOURS celui du disque).

**Alternatives rejetées.** Relocaliser les octets hérités aux slots neufs avec re-calcul des déplacements RIP (rejetée : R7 exige le byte-identique, un octet ré-écrit — même « équivalent » — est une contrebande ; et la preuve d'équivalence serait un second harnais) ; copier les tables K/H0 au domaine loupe (rejetée : la source unique vit à tls13/layout.py, le plan loupe RENVOIE — jamais une seconde déclaration) ; refuser le fichier vide à l'ouverture (rejetée : le vide est un fichier réel du quotidien — l'éditeur du projet ouvre des fichiers vides, le panneau du vide est défini par RFC 1321 et FIPS 180-4, la session née entière SANS la fenêtre est l'arbitrage honnête, consigné en révision 3 nommée) ; l'intégrale 2 Gio au harnais (rejetée : ~33 M blocs émulés, des heures de labo pour un cas que le terrain rendra en secondes — le refus au comportement + la borne dans les octets + le cas nommé pour le kit M10-(d), la découpe honnête) ; lire le verdict en rax 64 bits (rejetée : le verdict VIT dans eax, la table des SEPT verdicts est 32 bits — le harnais lit ce que le bloc rend, la convention de la charte § 9).

**Les frontières du geste.** AUCUN arbre signé touché (le garde sceau I vérifié AVANT consignation : 13 arbres VERTS) ; le proxy 1.0.0 et la carte tls13 1.0.0 INTACTS (l'anti-rollback armé — les scellés sont LUS, jamais écrits) ; AUCUNE clé, AUCUN coffre réel, AUCUN fragment touchés ; la dette de cérémonie D166/D171 DEMEURE (le 14e arbre et l'extension du registre figé attendent la cérémonie d'ère — AVANT tout build, M10-(d)). Livrables : loupe/notation/brouillons/loupe-01..07.asm (les sept brouillons), loupe/notation/loupe-01..07.asm (les notations explicites), loupe/outils/auteur.py (l'outil d'auteur au mode --mesurer), loupe/layout.py (l'adressage ARRÊTÉ : les slots, les zones, l'IAT, les adresses scellées), loupe/harnais_noyau.py (l'instrument au mini-OS virtuel), loupe/I/loupe-01-ouvrir.md (révisions 2 et 3 nommées), loupe/I/README.md (le chantier (b) COMPLET + la règle des adresses scellées), le présent script.
"""

# --- l'Entrée 196 (avant le marqueur m5a) -----------------------------------------

ENTREE_196 = """## Entrée 196 — « continue » : LE CHANTIER M10-(b) RÉALISÉ — LE NOYAU LOUPE-01..07 NOTÉ-MESURÉ-PROUVÉ (FICHIER + EMPREINTES) ; LES HÉRITAGES VIVENT À LEURS ADRESSES SCELLÉES (LA DÉCOUVERTE DU GESTE) ; LE MINI-OS VIRTUEL DU HARNAIS ; L'INSTRUMENT 59 CONTRÔLES · 59 VERTS × 3 GRAINES ; LES RÉVISIONS NOMMÉES DE LOUPE-01 (R2 LA TAILLE DE LA PIÈCE, R3 LE VIDE) (08/11)

**La reprise (l'état au geste).** Le M10-(a) réalisé à l'Entrée 195 (les 18 spécifications, le plan d'adressage arrêté en tailles), le développeur commande la suite. La notation naît sous ses contrats — R2 tenue côté build : la cérémonie d'ère précède, la dette D166/D171 demeure, le garde à 13 arbres.

**Le geste : LES SEPT NOTATIONS DU NOYAU.** Les brouillons loupe-01..07 (la mesure --mesurer de l'auteur D'ABORD : 47/388/296/122/312/879/102 o, le plan ARRÊTÉ aux minimums — D161 rejoué, la préfiguration s'incline ; slots 0x40/0x1C0/0x140/0xC0/0x180/0x380/0x80 tassés @0x4040-0x49C0). loupe-04 le cadre (memset hérité, la poignée INVALIDE) ; loupe-01 ouvrir (l'ordre des refus : session double AVANT tout [l'ancien INTACT], loupe-04 en tête, CreateFileW traduit par gle [absent -2, verrouillé -7, le reste -6], LA BORNE 2 Gio + 1 → -3 la poignée REFERMÉE AVANT le retour, la copie du chemin par libc-01 [la mesure UTF-16 bornée 260 — jamais un débordement], la session née entière [loupe-02 si taille > 0 puis loupe-07 — sur refus : loupe-03 ferme, le verdict remonte, jamais une poignée pendante]) ; loupe-02 lire (la double borne, la position repositionnée à CHAQUE lecture, LE RECOUVREMENT du journal — l'édition survit au défilement, fail-closed remplissage 0) ; loupe-03 fermer (idempotent par construction, l'hygiène des zones, l'échec CloseHandle CONSOMMÉ — « jamais une poignée pendante » prime, rax = 0 quand même) ; loupe-05 sha256 (LA COMPOSITION HÉRITÉE tls13-01/03/04 PAR LA CARTE, le contexte 112 o SUR LA PILE, les fenêtres 64 Kio, la sortie INTACTE sur refus) ; loupe-06 md5 LA NOTATION NEUVE (RFC 1321 : les quatre abscisses, les SOIXANTE-QUATRE tours aux QUATRE rounds nommés, les tables publiques .rdata LUES PAR DÉPLACEMENT RIP [S @0x2100, T @0x2200 — la source unique du plan], le couplage par LE TAMPOHN du contexte [le miroir ah/tls13-03], le bourre 0x80/zéros/bits, l'extraction little-endian — 879 o, le plus grand bloc du noyau, la sous-routine .comprimer FEUILLE PURE) ; loupe-07 le cumul (la composition seule : loupe-05 PUIS loupe-06, DEUX passages l'un après l'autre, le panneau TOUJOURS celui du disque, le refus RELAYÉ TEL QUEL).

**LA DÉCOUVERTE DU GESTE : LES HÉRITAGES VIVENT À LEURS ADRESSES SCELLÉES.** Le premier jet posait les octets hérités à des slots neufs ; l'émulation a CRASHÉ dans tls13-02 sur « lea rbp, [rip - 0x91a4] » : le déplacement est CODÉ POUR L'ADRESSE SCELLÉE 0xC080 (visant K[64] @0x2F00). Déplacer les octets casserait le déplacement ; les re-réécrire serait une contrebande de R7. L'image loupe réserve donc : .text 0x1000-0x1FFF la minilibc AUX ADRESSES M1 (libc-01 @0x1100, libc-02 @0x1180 RÉSERVÉE au chantier navigation, libc-07 @0x13C0), .rdata 0x2000-0x2FFF (MD5_S/T @0x2100/0x2200, l'IAT 34 feuilles @0x2400-0x2510, K[64] @0x2F00 LA TABLE DU SCELLÉ — le plan RENVOIE à tls13/layout.py), .text2 0x4000-0xBFFF les blocs du domaine (0x4000 la réserve d'entrée WinMain), 0xC000-0xC3C0 la famille sha AUX ADRESSES M9, .data @0xE000 les zones (cadre @0xE000, CUMUL @0x10000, fin 0x20000). Les octets extraits des SCELLÉS posés À LEURS ADRESSES D'ORIGINE — R7 au sens propre : les MÊMES octets aux MÊMES adresses.

**L'instrument : LE MINI-OS VIRTUEL (loupe/harnais_noyau.py).** Les SIX shims kernel32 du noyau à l'ABI msx64 (le retour factice lit [rsp], rax posé, rip réglé), le système de fichiers virtuel aux témoins réels (proxy.exe scellé INCLUS), les échecs PARAMÉTRABLES (le Nième ReadFile), le journal des gle, le COMPTEUR DU MORT (les 28 feuilles hors noyau dénoncées — le contrôle FINAL constate zéro appel). LE CAHIER V0-V6 : 59 contrôles · 59 VERTS × 3 graines (20261108, 424242, 777777). V2 LES SEPT VECTEURS RFC 1321 AU FICHIER (chaque attendu recroisé à hashlib — le juge est le code), 1 000 gammes, le 3×64 Kio + 1 ENTIER ; V3 LA PIÈCE DE L'ÈRE JUGÉE PAR SA PROPRE APPLICATION (loupe-05(0, 65024) sur les octets RÉELS du proxy == 446279f3…00d93d), les FIPS au fichier, 200 gammes ; V1 l'héritage R7 CONSTATÉ — LA DOUBLE PREUVE (les extraits des scellés == les octets émulés ET les notations d'origine ré-assemblées == les extraits), les constantes re-dérivées, la borne 2 Gio dans les octets (mov eax, 0x80000000 : le bord exact accepté, le refus strictement au-delà) ; V4 le cadre vierge recomposé, la session née entière CHAMP À CHAMP, LE FICHIER VIDE (révision 3 : remplissage 0, le panneau d41d8cd9… + e3b0c442…), 1 060 fenêtres, LE RECOUVREMENT, l'idempotence COMPTÉE, les zones des chantiers suivants INTACTES ; V5 LES ONZE REJETS NOMMÉS (la poignée refermée comptée sur la borne, l'ancien fichier INTACT sur la session double, le -6 du shim avec la sortie INTACTE et le code 1117 AU JOURNAL, le refus propagé la session close) ; V6 LA FALSIFICATION (T[1] muté d'un ulp : 7/7 échouent AVEC rax = 0 exigé — jamais un vert par accident de refus ; l'anti-muet ; le tampon de vue INTACT [l'exclusion de famille] ; le journal INTACT ; le panneau du DISQUE).

**Les leçons du geste (consignées pour les chantiers suivants).** LE VERDICT VIT DANS EAX (mov eax, -N zéro-étend rax — le harnais lit le 32 bits signé, les poignées ne transitent jamais par rax) ; L'ORDRE DES REGISTRES AU RÉSEAU DES APPELS (loupe-04 détruit rcx : le chemin sauvé AVANT et RECHARGÉ — l'ABI se rejoue à chaque frontière) ; LE CADRE À L'IMAGE naît poignée INVALIDE (le zéro de la mémoire vierge serait une session fantôme) ; libc-07 appartient aux dépendances de loupe-06 (les zéros du bourre PAR LA CARTE).

**Détail.** FRONTIÈRES : AUCUN arbre signé touché ; le garde sceau I vérifié AVANT consignation : 13 arbres VERTS, cle deposee reelle (D87) ; le proxy 1.0.0 et la carte tls13 INTACTS (lus, jamais écrits) ; la dette de cérémonie D166/D171 DEMEURE (le 14e arbre attend la cérémonie d'ère — AVANT tout build). Livrables : loupe/notation/brouillons/loupe-01..07.asm, loupe/notation/loupe-01..07.asm, loupe/outils/auteur.py, loupe/layout.py (l'adressage ARRÊTÉ), loupe/harnais_noyau.py, loupe/I/loupe-01-ouvrir.md (r2/r3), loupe/I/README.md, le présent script. Consignations : la présente Entrée PAR SCRIPT, la D173 PAR SCRIPT (docs/DECISIONS.md), le PLAN (la rangée (b) RÉALISÉE + la phrase de l'État), worklog +Task ID 114. SUITE : M10-(c) LE RENDU + LA NAVIGATION (loupe-08..14 : la ligne 77 o, l'écran, la peinture, le défilement, l'aller-à, la recherche — l'oracle à scénarios, la falsification attrapée) ; la cérémonie d'ère du TGN attend son geste (le kit au /Cérémonie, la main du développeur, le garde passant à 14 arbres) ; le projet fils attend son premier geste à son message propre.

"""

# --- la Task ID 114 (append au worklog) -------------------------------------------

TASK_114 = """
## Task ID 114 — LE CHANTIER M10-(b) RÉALISÉ : LE NOYAU LOUPE-01..07 NOTÉ-MESURÉ-PROUVÉ (FICHIER + EMPREINTES — LA NOTATION AUX SLOTS ARRÊTÉS SUR LES MESURES, LES HÉRITAGES AUX ADRESSES SCELLÉES, LE HARNAIS AU MINI-OS VIRTUEL 59 VERTS × 3 GRAINES) ; LES RÉVISIONS NOMMÉES DE LOUPE-01 (R2/R3) (08/11)

- La suite annoncée à l'Entrée 195 ; le développeur commande (« continue »).
  AUCUN build : la cérémonie d'ère précède (D168), la dette D166/D171
  demeure, le garde à 13 arbres.
- LES SEPT NOTATIONS : 04 le cadre (47 o, memset hérité) · 01 ouvrir
  (388 o : l'ordre des refus, la borne 2 Gio, la copie libc-01, la
  session née entière) · 02 lire (296 o : la double borne, LE
  RECOUVREMENT du journal, fail-closed) · 03 fermer (122 o :
  idempotence, l'hygiène, l'échec CONSOMMÉ) · 05 sha256 (312 o : la
  composition tls13-01/03/04 PAR LA CARTE, les fenêtres 64 Kio) · 06
  md5 LA NOTATION NEUVE (879 o : RFC 1321, les 64 tours aux 4 rounds,
  les tables publiques .rdata par déplacement RIP, le couplage, le
  bourre, l'extraction) · 07 le cumul (102 o : la composition seule,
  le panneau du disque).
- LA DÉCOUVERTE : LES HÉRITAGES VIVENT À LEURS ADRESSES SCELLÉES — le
  tls13-02 scellé porte un déplacement RIP codé pour 0xC080 (visant
  K[64] @0x2F00) ; l'image loupe réserve .text M1, .rdata (K laissée au
  scellé), 0xC000-0xC3C0 la famille sha ; les octets extraits des
  scellés posés À LEURS ADRESSES D'ORIGINE — R7 au sens propre. La
  règle pour les chantiers suivants : tout héritage à SON adresse
  scellée (win-03 et son IAT démo au chantier rendu).
- LE MINI-OS VIRTUEL : les six shims kernel32 (la liste fermée), le FS
  virtuel aux témoins réels (proxy.exe scellé inclus), les échecs
  paramétrables, le journal des gle, le compteur du mort (28 feuilles
  dénoncées, zéro appel constaté).
- LE VERDICT : 59 contrôles · 59 VERTS × 3 graines — les SEPT
  vecteurs RFC 1321 au fichier (recroisés à hashlib), 1 000 gammes md5
  + 200 sha, LA PIÈCE DE L'ÈRE JUGÉE PAR SA PROPRE APPLICATION
  (loupe-05 sur proxy.exe == 446279f3…), l'héritage R7 CONSTATÉ (la
  double preuve), les ONZE rejets nommés, la falsification attrapée
  (T[1] d'un ulp : 7/7, rax = 0 exigé).
- LES RÉVISIONS DE LA COUCHE I : loupe-01 r2 (la taille de la pièce :
  65 024 o) ; loupe-01 r3 (LE VIDE s'ouvre sans fenêtre, son panneau
  existe). LES LEÇONS : le verdict vit dans eax ; l'ordre des registres
  au réseau des appels (rcx détruit par loupe-04 — sauvé AVANT,
  rechargé) ; le cadre à l'image naît poignée INVALIDE.
- FRONTIÈRES : AUCUN arbre signé touché ; le garde sceau I : 13 arbres
  VERTS (cle deposee reelle) vérifié AVANT consignation ; le proxy
  1.0.0 et la carte tls13 INTACTS. Livrables : les brouillons + les
  notations loupe-01..07, loupe/outils/auteur.py (--mesurer),
  loupe/layout.py, loupe/harnais_noyau.py, loupe-01-ouvrir.md (r2/r3),
  loupe/I/README.md, scripts/consigner_m10b.py.
- SUITE : M10-(c) le rendu + la navigation (l'oracle à scénarios) ; la
  cérémonie d'ère du TGN attend son geste (le 14e arbre, avant tout
  build) ; le projet fils attend son premier geste à son message propre.
"""


def main():
    # 0. le garde AVANT consignation (la discipline du projet)
    r = subprocess.run(["python3", str(REPO / "v06" / "sceau_I.py"),
                        "verifier"], capture_output=True, text=True)
    if "13 arbres VERTS" not in r.stdout:
        sys.exit("ÉCHEC : le garde sceau I ne constate pas 13 arbres VERTS "
                 f"— consignation REFUSÉE\n{r.stdout[-400:]}")
    print("GARDE : 13 arbres VERTS (cle deposee reelle) — la consignation peut suivre")

    # 0bis. l'instrument du chantier AVANT consignation (le geste se prouve)
    r = subprocess.run(["python3", str(REPO / "loupe" / "harnais_noyau.py")],
                       capture_output=True, text=True)
    if "VERDICT : VERT" not in r.stdout or r.returncode != 0:
        sys.exit("ÉCHEC : l'instrument loupe/harnais_noyau.py n'est pas VERT "
                 f"— consignation REFUSÉE\n{r.stdout[-600:]}")
    n_controles = r.stdout.count("[ok] ")
    print(f"INSTRUMENT : loupe/harnais_noyau.py VERT ({n_controles} contrôles) — "
          "le geste se prouve avant de se consigner")

    # 1. le plan : la rangée (b) RÉALISÉE + l'État (idempotent)
    plan = PLAN.read_text(encoding="utf-8")
    if "RÉALISÉ (Entrée 196, D173)" in plan:
        print("PLAN : la rangée (b) RÉALISÉE déjà consignée — constaté")
    else:
        if plan.count(RANGEE_ANCIENNE_B) != 1:
            sys.exit(f"ÉCHEC : la rangée (b) OUVERTE trouvée "
                     f"{plan.count(RANGEE_ANCIENNE_B)} fois (attendu : 1)")
        if plan.count(ANCIEN_ETAT) != 1:
            sys.exit(f"ÉCHEC : ancrage État trouvé "
                     f"{plan.count(ANCIEN_ETAT)} fois (attendu : 1)")
        plan = plan.replace(RANGEE_ANCIENNE_B, RANGEE_NOUVELLE_B, 1)
        plan = plan.replace(ANCIEN_ETAT, NOUVEL_ETAT, 1)
        if "RÉALISÉ (Entrée 196, D173)" not in plan:
            sys.exit("ÉCHEC : la rangée (b) absente après remplacement")
        if "LE CHANTIER M10-(b) RÉALISÉ le 08/11/2026" not in plan:
            sys.exit("ÉCHEC : l'État ne porte pas la phrase du M10-(b)")
        PLAN.write_text(plan, encoding="utf-8")
        print("PLAN : la rangée (b) RÉALISÉE + l'État du programme — consignés")

    # 2. le journal : l'Entrée 196 avant le marqueur m5a (idempotent)
    journal = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 196 —" in journal:
        print("JOURNAL : l'Entrée 196 déjà consignée — constaté")
    else:
        marqueur = "<!-- m5a:journal-des-builds v1"
        if journal.count(marqueur) != 1:
            sys.exit(f"ÉCHEC : le marqueur m5a trouvé "
                     f"{journal.count(marqueur)} fois (attendu : 1)")
        journal = journal.replace(marqueur, ENTREE_196 + marqueur, 1)
        if "## Entrée 196 — « continue »" not in journal:
            sys.exit("ÉCHEC : l'Entrée 196 absente après remplacement")
        JOURNAL.write_text(journal, encoding="utf-8")
        print("JOURNAL : l'Entrée 196 consignée AVANT le marqueur m5a")

    # 3. le registre des décisions : la D173 à la suite de D172
    decisions = DECISIONS.read_text(encoding="utf-8")
    if "## D173 —" in decisions:
        print("DECISIONS : la D173 déjà consignée — constaté")
    else:
        if decisions.count("## D172 —") != 1:
            sys.exit("ÉCHEC : la D172 absente ou multiple (le geste "
                     "précédent n'est pas consigné)")
        decisions = decisions.rstrip("\n") + "\n" + D173.strip("\n") + "\n"
        if "## D173 — LE CHANTIER M10-(b) RÉALISÉ" not in decisions:
            sys.exit("ÉCHEC : la D173 absente après append")
        DECISIONS.write_text(decisions, encoding="utf-8")
        print("DECISIONS : la D173 consignée À LA SUITE de la D172")

    # 4. le worklog racine : la Task ID 114 à la suite de la 113
    worklog = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 114 —" in worklog:
        sys.exit("ÉCHEC : la Task ID 114 existe déjà (rejeu REFUSÉ)")
    if worklog.count("## Task ID 113 —") != 1:
        sys.exit("ÉCHEC : l'entrée Task ID 113 absente ou multiple (le geste "
                 "précédent n'est pas consigné)")
    worklog = worklog.rstrip("\n") + "\n" + TASK_114
    if "## Task ID 114 — LE CHANTIER M10-(b) RÉALISÉ" not in worklog:
        sys.exit("ÉCHEC : la Task ID 114 absente après append")
    WORKLOG.write_text(worklog, encoding="utf-8")
    print("WORKLOG : la Task ID 114 consignée À LA SUITE de la Task 113")


if __name__ == "__main__":
    main()
