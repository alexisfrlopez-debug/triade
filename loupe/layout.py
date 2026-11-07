#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""loupe/layout.py — LE PLAN D'ADRESSAGE DU DOMAINE loupe (M10, le TGN « Loupe »).

La source unique des constantes du domaine (le modèle tls13/layout.py, D161) :
la balise de la lignée, la table des verdicts, les bornes du périmètre 0.1.0,
le cadre de session, la ligne hexadécimale, les tables publiques MD5, les
zones .data, l'héritage PAR LA CARTE et l'IAT déclaré.

LA PRÉFIGURATION N'EST PAS UN DROIT (D161, la leçon de M8-(b)) : les RVA et
tailles définitifs des blocs seront ARRÊTÉS au chantier de la notation sur
les LONGUEURS RÉELLES mesurées (auteur.py décide, la préfiguration s'incline)
; seuls les constantes immuables (les valeurs de spécification), les ZONES
.data (le cadre, l'écran, le journal — les tailles ARRÊTÉES ici) et les
bornes d'héritage (le scellé 1.0.0, R7) sont ARRÊTÉS ici. Loupe est une
APPLICATION NEUVE : son image (loupe.exe) naîtra au premier build du jalon —
la carte du domaine portera les i11xxxx dès sa première génération."""

# --- La balise de la lignée (charte § 6 : geste de BUILD, jamais scellage) ------

VERSION_DEV = 0x00010001           # loupe 0.1.0-dev.1 (au premier build — le
                                   # miroir du format 0xJJNNPPDD : 0.9.0-dev.1
                                   # == 0x00090001 [M8], 1.0.0-dev.4 ==
                                   # 0x01000004 [M9] ; 0.1.0-dev.1 == 0x00010001)
VERSION_FINALE = 0x00010000        # loupe 0.1.0 (le scellage sera un fait de
                                   # carte — le miroir D165/D170, sur le run
                                   # terrain vert recoupé)

# --- La table des SEPT verdicts du domaine (l'échec nommé, charte § 9) ---------

VERDICTS = {
    0: "OK",
    -1: "FIN (la fin nommée : la plage est épuisée, plus d'occurrence)",
    -2: "ABSENT (le chemin ne désigne rien)",
    -3: "HORS-BORNES (hors du fichier ou du périmètre 0.1.0 — la borne nommée)",
    -4: "SESSION (aucun fichier ouvert, ou déjà fermé)",
    -5: "ENTRÉE (l'ordre est refusé en l'état : argument invalide, saisie mal "
        "formée, quitter non sauvé)",
    -6: "SYSTÈME (l'OS refuse et nomme son code — GetLastError consigné)",
    -7: "VERROUILLÉ (le partage du fichier refuse l'ouverture)",
}

# --- Les bornes du périmètre 0.1.0 (charte : le périmètre tenable) --------------

BORNE_TAILLE = 1 << 31             # 2 Gio : le plus grand fichier ouvert — le
                                   # dernier décalage 0x7FFFFFFV = 8 chiffres
                                   # hex (0x7FFFFFFF), la ligne demeure droite
LIGNE_OCTETS = 16                  # la ligne hexadécimale montre 16 octets
GRILLE_LIGNES = 24                 # la borne d'affichage : 24 lignes au
                                   # maximum (l'écran montre moins si la
                                   # fenêtre est petite — jamais plus)
TAMPON_SESSION = GRILLE_LIGNES * LIGNE_OCTETS   # 384 o : la fenêtre de vue
CUMUL_FENETRE = 1 << 16            # 64 Kio : la fenêtre glissante des
                                   # empreintes et de la recherche (multiple
                                   # du bloc 64 de SHA-256 ET de MD5)
EDITS_MAX = 256                    # le journal des écritures : 256 octets
                                   # DISTINCTS en attente de sauvegarde
MOTIF_MAX = 32                     # la borne du quotidien : une suite de
                                   # 32 octets (un en-tête, une chaîne)
SAISIE_MAX = 79                    # la barre-saisie : 79 chiffres + NUL
DEFILEMENT_LIGNES = 3              # la molette : TROIS lignes par cran
                                   # (WHEEL_DELTA = 120, le cran canonique)
PAGE_LIGNES = GRILLE_LIGNES - 2    # la page : la grille − 2 lignes de repère
PAS_LIGNE = LIGNE_OCTETS           # SB_LINEUP/DOWN : ±16 o (une ligne)
PAS_PAGE = PAGE_LIGNES * LIGNE_OCTETS   # SB_PAGEUP/DOWN : ±352 o (22 lignes)

# --- La ligne hexadécimale (loupe-08) : le format ARRÊTÉ ------------------------
# « SSSSSSSS  HH HH HH HH HH HH HH HH  HH HH HH HH HH HH HH HH  AAAAAAAAAAAAAAAA »
#   8 chiffres hex du décalage · 2 espaces · 16 groupes « HH » séparés par un
#   espace (l'espace médian DOUBlé après le 8e : 32 hex + 16 espaces = 48) ·
#   2 espaces · le miroir ASCII 16 · NUL. La ligne finale (moins de 16 octets
#   valides) garde le FORMAT : les groupes absents sont deux espaces, le
#   miroir absent un espace — l'alignement des colonnes est un invariant.

LIGNE_DECALAGE = 8                 # 8 chiffres hex (BORNE_TAILLE le garantit)
LIGNE_TAILLE = (LIGNE_DECALAGE + 2 + (16 * 2 + 15 + 1) + 2 + 16 + 1)  # = 77 o
ENTETE_TEXTE = 65                  # « Décalage  00 01 … 0F  ASCII » + NUL
ENTETE_ZONE = 80                   # la zone ECRAIN de l'entête (alignée)
BARRE_LIGNES = 2                   # la barre d'état : l'état · le PANNEAU
                                   # D'EMPREINTES (md5 + sha-256)
BARRE_ZONE = 160                   # par ligne (79 utiles + NUL, la marge)

# --- Le cadre de session (loupe-04) : la structure unique, la disposition ------
# LA SOURCE UNIQUE : chaque champ cité par son offset, les dix-sept autres
# blocs y renvoient (aucune connaissance dupliquée — T5).

CADRE_CHEMIN = 260 * 2             # UTF-16[MAX_PATH] @ +0 → 520 o
CADRE_TAILLE_F = 8                 # u64 @ +520 : la taille du fichier
CADRE_POIGNEE = 8                  # u64 @ +528 : INVALID_HANDLE_VALUE (−1)
                                   # hors session
CADRE_VUE = 8                      # u64 @ +536 : le décalage du premier
                                   # octet affiché (multiple de 16 — INVARIANT)
CADRE_CURSEUR = 8                  # u64 @ +544 : le décalage de la cellule
                                   # active (borné [0, taille−1] — INVARIANT)
CADRE_REMPLISSAGE = 4              # u32 @ +552 : les octets valides du tampon
CADRE_SALE = 4                     # u32 @ +556 : la marque (0 = propre)
CADRE_REFUS_QUITTER = 4            # u32 @ +560 : la garde de loupe-18 (le
                                   # double-gestre — remise à zéro par
                                   # loupe-16 à CHAQUE écriture et par
                                   # loupe-17 à CHAQUE sauvegarde réussie)
CADRE_RESERVE = 4                  # u32 @ +564 : la réserve d'alignement
CADRE_TAMPON = TAMPON_SESSION      # 384 o @ +568 : la fenêtre de vue
CADRE_OCTETS = 568 + TAMPON_SESSION   # 952 o utiles
CADRE_TOTAL = 960                  # 952 arrondi à l'alignement 16 (8 o de
                                   # réserve finale)

# --- Les zones .data du domaine (D161 : déclarées avant la notation) ------------

ZONE_ECRAN = 2320                  # loupe-09 : l'entête 80 @ +0 · la grille
                                   # 24 × 80 @ +80 · la barre 2 × 160 @ +2000
ZONE_SAISIE = 96                   # loupe-12 : mode u32 @ +0 · actif u32
                                   # @ +4 (le nibble en attente) · nibble u32
                                   # @ +8 · tampon[80] @ +12
ZONE_MOTIF = 48                    # loupe-13/14 : motif[32] @ +0 · longueur
                                   # u32 @ +32 · la réserve @ +36
ZONE_JOURNAL = 4112                # loupe-16 : 256 entrées de 16 o @ +0
                                   # (u64 décalage · u8 octet · 7 réserve —
                                   # l'entrée PAR DÉCALAGE) · nombre u32
                                   # @ +4096 · la réserve @ +4100
ZONE_EMPREINTES = 48               # loupe-07 : md5[16] @ +0 · sha256[32]
                                   # @ +16 (le panneau d'empreintes)
ZONE_HWND = 8                      # loupe-09 : HWND_PRINCIPAL
ZONE_METRIQUES = 16                # loupe-10 : char_w u32 · ligne_h u32 ·
                                   # lignes_visibles u32 · drapeaux u32 (la
                                   # police mesurée UNE fois)
ZONE_CUMUL = CUMUL_FENETRE         # 64 Kio : LA fenêtre de lecture du domaine
                                   # (empreintes 05/06/07 + recherche 14 —
                                   # l'exclusion de famille : jamais deux flux
                                   # simultanés, l'application est monofile)

# --- La disposition des zones (ARRÊTÉE au geste (c) — la source unique) -----------
# LA BARRE-ÉTAT DU GESTE (c) : la ligne 1 de la barre porte QUATRE états nommés —
# mode MESSAGE → le texte du tampon (le refus NOMMÉ monte à la barre, I4 de
# loupe-09 : « la barre le porte au prochain WM_PAINT ») ; mode ALLER/CHERCHER →
# le libellé du mode + le tampon (la saisie vit À LA BARRE, I1 de loupe-12) ;
# mode RIEN + session → la balise ligne (D137) ; mode RIEN + vide → l'usage.
# Le tiret de la balise est le trait d'union ASCII « - » et le point médian
# « · » le byte 0xB7 : l'expansion latin-1 EXACTE (I4 de loupe-10) n'élève
# que 0x00-0xFF — U+2014 n'y vit pas, la spec l'écrit « — » à la française.

SAISIE_MODE = 0                    # u32 @ +0 : 0 RIEN · 1 ALLER · 2 CHERCHER
                                   # · 3 MESSAGE (la barre-état du geste (c))
SAISIE_ACTIF = 4                   # u32 @ +4 : le nibble en attente
                                   # (loupe-16, chantier (d) — déclaré, vivant)
SAISIE_NIBBLE = 8                  # u32 @ +8 : sa valeur
SAISIE_TAMPON = 12                 # octets @ +12 : les chiffres frappés (le
                                   # message en mode MESSAGE — 79 + NUL)
MODE_RIEN = 0
MODE_ALLER = 1
MODE_CHERCHER = 2
MODE_MESSAGE = 3
ALLER_CHIFFRES = 8                 # 8 chiffres hex max (la borne du format
                                   # 0x7FFFFFFF à 8 chiffres — Q2 de loupe-12)
CHERCHER_CHIFFRES = 64             # 64 chiffres = 32 octets (MOTIF_MAX)

MOTIF_OCTETS = 0                   # motif[32] @ +0 (la zone MOTIF)
MOTIF_LONGUEUR = 32                # u32 @ +32 (F3 reprend le dernier motif)

METRIQUES_CHAR_W = 0               # u32 @ +0 : la chasse mesurée UNE fois
METRIQUES_LIGNE_H = 4              # u32 @ +4 : la hauteur de ligne
METRIQUES_LIGNES = 8               # u32 @ +8 : les lignes visibles (WM_SIZE)
METRIQUES_DRAPEAUX = 12            # u32 @ +12 : bit 0 = la police mesurée

ECRAN_ENTETE = 0                   # 80 o @ +0 : l'entête (65 utiles + NUL)
ECRAN_GRILLE = 80                  # 24 × 80 @ +80 : une ligne par slot de 80
ECRAN_BARRE = 2000                 # 2 × 160 @ +2000 : la barre-état (2 lignes)

# --- Les messages du domaine (les WM/SB auxquels la procédure route) --------------
WM_TAILLE = 0x0005                 # WM_SIZE (lParam : cx | cy << 16)
WM_PEINTURE = 0x000F               # WM_PAINT → loupe-10 (l'unique peintre)
WM_FERMETURE = 0x0010              # WM_CLOSE → loupe-18 (chantier (d))
WM_VSCROLL = 0x0115                # WM_VSCROLL → loupe-11
WM_TOUCHE = 0x0100                 # WM_KEYDOWN : la table de commandes
WM_CARACT = 0x0102                 # WM_CHAR : la saisie active ?
WM_MOLETTE = 0x020A                # WM_MOUSEWHEEL → loupe-11
WM_QUITTE = 0x0012                 # WM_QUIT : la boucle win-03 rend
SB_VERT = 1                        # l'ascenseur vertical
UTILISATION_DEFAUT = 0x80000000    # CW_USEDEFAULT (la position de la vitrine)
COULEUR_FENETRE = 5                # COLOR_WINDOW + 1 (le pinceau de la classe)
SB_SUIVANT = 5                     # SB_THUMBTRACK (GetScrollInfo nTrackPos)

# --- Les constantes publiques de la famille sha (loupe-05) : LE RENVOI ----------
# L'HÉRITAGE PAR LA CARTE (R7, charte § 2) : la famille sha tls13 est embarquée
# BYTE-IDENTIQUE à son scellé 1.0.0 — H0, le bloc 64 et la disposition du
# contexte VIVENT À tls13-01 P1 (la source unique, jamais re-déclarés ici).

SHA_CTX = 112                      # la disposition de tls13-01 P1 (renvoi —
                                   # le contexte tenu par loupe-05 SUR LA PILE)
SHA_CONDENSE = 32                  # FIPS 180-4 (renvoi)

# --- Les constantes publiques de la famille md5 (loupe-06, RFC 1321) ------------
# La NOUVELLE notation du domaine : les tables sont PUBLIQUES en .rdata et
# DÉRIVÉES PAR ARITHMÉTIQUE au geste même (T[i] = floor(2^32 · |sin(i+1)|),
# RFC 1321 § 3.4 — le vérificateur du chantier les RE-DÉRIVE : le juge est le
# code ; md5 est L'EMPREINTE DU QUOTIDIEN du projet — jamais une preuve de
# sécurité, la spec le nomme).

MD5_ABSCISSE = (0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476)  # § 3.3
MD5_TAILLE_BLOC = 64
MD5_CONDENSE = 16
MD5_CTX = 88                       # A,B,C,D u32 @ +0 (16) · longueur u64
                                   # @ +16 (les octets absorbés cumulés) ·
                                   # tampon[64] @ +24 (la disposition miroir
                                   # ah/tls13 : les mêmes champs, le petit-
                                   # boutisme DE MD5 —RFC 1321 § 3.2 — le
                                   # condensé sérialisé little-endian)
MD5_S = (7, 12, 17, 22) * 4 + (5, 9, 14, 20) * 4 \
    + (4, 11, 16, 23) * 4 + (6, 10, 15, 21) * 4      # les 64 décalages, § 3.4
MD5_T = (
    0xD76AA478, 0xE8C7B756, 0x242070DB, 0xC1BDCEEE, 0xF57C0FAF, 0x4787C62A,
    0xA8304613, 0xFD469501, 0x698098D8, 0x8B44F7AF, 0xFFFF5BB1, 0x895CD7BE,
    0x6B901122, 0xFD987193, 0xA679438E, 0x49B40821, 0xF61E2562, 0xC040B340,
    0x265E5A51, 0xE9B6C7AA, 0xD62F105D, 0x02441453, 0xD8A1E681, 0xE7D3FBC8,
    0x21E1CDE6, 0xC33707D6, 0xF4D50D87, 0x455A14ED, 0xA9E3E905, 0xFCEFA3F8,
    0x676F02D9, 0x8D2A4C8A, 0xFFFA3942, 0x8771F681, 0x6D9D6122, 0xFDE5380C,
    0xA4BEEA44, 0x4BDECFA9, 0xF6BB4B60, 0xBEBFBC70, 0x289B7EC6, 0xEAA127FA,
    0xD4EF3085, 0x04881D05, 0xD9D4D039, 0xE6DB99E5, 0x1FA27CF8, 0xC4AC5665,
    0xF4292244, 0x432AFF97, 0xAB9423A7, 0xFC93A039, 0x655B59C3, 0x8F0CCC92,
    0xFFEFF47D, 0x85845DD1, 0x6FA87E4F, 0xFE2CE6E0, 0xA3014314, 0x4E0811A1,
    0xF7537E82, 0xBD3AF235, 0x2AD7D2BB, 0xEB86D391,
)                                   # DÉRIVÉES : floor(2^32 · |sin(i+1)|) —
                                    # T[0] = 0xD76AA478, T[63] = 0xEB86D391
                                    # (RFC 1321, recoupés au geste même)

# --- L'héritage PAR LA CARTE (charte § 2, R7 : embarqué au build, jamais copié) --

HERITAGE_SHA = ("tls13-01", "tls13-02", "tls13-03", "tls13-04")
                                   # la famille sha scellée 1.0.0 (M9) — les
                                   # QUATRE blocs byte-identiques, l'oracle du
                                   # build le constatera octet par octet
HERITAGE_LIBC = ("libc-01", "libc-02", "libc-07")
                                   # la minilibc M1 : memcpy (la copie du
                                   # chemin et des gammes), memcmp (la
                                   # recherche), memset (le cadre) — les
                                   # feuilles du quotidien CITÉES par les
                                   # specs (l'héritage déclaré est
                                   # l'héritage utilisé — libc-03 strlen
                                   # RETIRÉ au geste (a) : aucune spec ne
                                   # le cite, la contrebande de périmètre
                                   # est un défaut nommé)
HERITAGE_WIN03 = ("win-03",)       # la boucle de messages de la démo (M3) —
                                   # la respiration générique, scellée

# --- L'IAT du domaine (D7/D35 : les feuilles déclarées avant la notation) -------
# Le budget NOMMÉ : 34 entrées (kernel32 10 · user32 18 · gdi32 6). Les blocs
# SANS entrée IAT propre : loupe-04 (le memset hérité), loupe-07 (la
# composition), loupe-08 et loupe-13 (les feuilles pures — le miroir tls13
# charte § 7). Les TROIS feuilles de win-03 (héritées) vivent dans user32.

IAT_KERNEL32 = (
    "GetModuleHandleW",            # l'image PI — aucune adresse absolue (D33)
    "GetCommandLineW",             # la ligne de commande lue À LA MAIN (le
                                   # chemin cité ou non — loupe-09)
    "ExitProcess",                 # le retour propre de WinMain
    "CreateFileW",                 # loupe-01 (GENERIC_READ|GENERIC_WRITE,
                                   # FILE_SHARE_READ, OPEN_EXISTING)
    "GetFileSizeEx",               # loupe-01 (la taille, la borne nommée)
    "SetFilePointerEx",            # loupe-02/05/06/14/17 (chaque lecture
                                   # repositionne — jamais une position héritée)
    "ReadFile",                    # loupe-02/05/06/14
    "WriteFile",                   # loupe-17 (l'écriture À L'OCTET)
    "CloseHandle",                 # loupe-03
    "GetLastError",                # les refus -6/−7 NOMMÉS (le code consigné)
)
IAT_USER32 = (
    "RegisterClassExW",            # loupe-09 (la classe, l'héritage win-02)
    "CreateWindowExW",             # loupe-09 (la vitrine)
    "ShowWindow",                  # loupe-09 (SW_SHOW)
    "GetMessageW",                 # win-03 héritée
    "TranslateMessage",            # win-03 héritée
    "DispatchMessageW",            # win-03 héritée
    "DefWindowProcW",              # loupe-09 (le reste délégué)
    "BeginPaint",                  # loupe-10 (le seul peintre)
    "EndPaint",                    # loupe-10
    "InvalidateRect",              # loupe-11/12/14/15/16/17 (le repaint
                                   # demandé — JAMAIS loupe-10 : le peintre
                                   # ne s'invalide pas lui-même, I3 de
                                   # loupe-09 : l'invalidation vit chez les
                                   # APPELANTS ; retiré de 10 au geste (c))
    "GetClientRect",               # loupe-10 (le clipping par lignes visibles)
    "GetScrollInfo",               # loupe-11 (SB_THUMBTRACK/END)
    "SetScrollInfo",               # loupe-11 (l'ascenseur TOUJOURS synchrone)
    "DestroyWindow",               # loupe-18
    "PostQuitMessage",             # loupe-18 (la boucle win-03 rend)
    "LoadCursorW",                 # loupe-09 (IDC_ARROW)
    "MessageBeep",                 # loupe-18 (le refus nommé s'entend)
    "MessageBoxW",                 # loupe-09 (la vitrine impossible
                                   # s'explique puis meurt — D36 le modèle)
)
IAT_GDI32 = (
    "GetStockObject",              # loupe-10 (ANSI_FIXED_FONT — la police à
                                   # chasse fixe, l'exigence des colonnes)
    "SelectObject",                # loupe-10
    "GetTextMetricsW",             # loupe-10 (la mesure UNE fois → METRIQUES)
    "TextOutW",                    # loupe-10 (l'expansion latin-1 octet→mot)
    "SetTextColor",                # loupe-10 (la cellule active en inverse)
    "SetBkColor",                  # loupe-10
)

# --- Les constantes d'interface (publiques, arrêtées avant la notation) ---------

INVALIDE = 0xFFFFFFFFFFFFFFFF      # INVALID_HANDLE_VALUE (hors session)
GENERIC_LECTURE = 0x80000000       # GENERIC_READ
GENERIC_ECRITURE = 0x40000000      # GENERIC_WRITE
PARTAGE_LECTURE = 0x00000001       # FILE_SHARE_READ
OUVRIR_EXISTANT = 3                # OPEN_EXISTING
DEBUT_FICHIER = 0                  # FILE_BEGIN (SetFilePointerEx)
ERREUR_ABSENT = 2                  # ERROR_FILE_NOT_FOUND → verdict -2
ERREUR_CHEMIN = 3                  # ERROR_PATH_NOT_FOUND → verdict -2
ERREUR_ACCES = 5                   # ERROR_ACCESS_DENIED → verdict -6
ERREUR_PARTAGE = 32                # ERROR_SHARING_VIOLATION → verdict -7
STYLE_FENETRE = 0x00CF0000 | 0x00200000   # WS_OVERLAPPEDWINDOW | WS_VSCROLL
AFFICHER = 5                       # SW_SHOW
FENETRE_L = 640                    # la vitrine 0.1.0 (ClientWidth nominal)
FENETRE_H = 480                    # la vitrine 0.1.0
CURSEUR_FLECHE = 32512             # IDC_ARROW
ICONE_ERREUR = 0x10                # MB_ICONERROR
POLICE_FIXE = 13                   # ANSI_FIXED_FONT (GetStockObject)
MOLETTE_CRAN = 120                 # WHEEL_DELTA
SIF_RANGE = 0x1                    # SetScrollInfo : la gamme
SIF_PAGE = 0x2                     # la page
SIF_POS = 0x4                      # la position
SB_LIGNE_HAUT = 0                  # SB_LINEUP
SB_LIGNE_BAS = 1                   # SB_LINEDOWN
SB_PAGE_HAUT = 2                   # SB_PAGEUP
SB_PAGE_BAS = 3                    # SB_PAGEDOWN
SB_POIGNEE = 4                     # SB_THUMBPOSITION
SB_POIGNEE_COURSE = 5              # SB_THUMBTRACK
VK_PRECEDENT = 0x21                # VK_PRIOR (PgUp)
VK_SUIVANT = 0x22                  # VK_NEXT (PgDn)
VK_FIN = 0x23                      # VK_END
VK_DEBUT = 0x24                    # VK_HOME
VK_GAUCHE = 0x25                   # VK_LEFT
VK_HAUT = 0x26                     # VK_UP
VK_DROITE = 0x27                   # VK_RIGHT
VK_BAS = 0x28                      # VK_DOWN
VK_ECHAP = 0x1B                    # VK_ESCAPE (l'annulation de la barre-saisie)
VK_RETOUR = 0x0D                   # VK_RETURN (le commit de la barre-saisie)
VK_SUPPR = 0x08                    # VK_BACK (la correction)
VK_F3 = 0x72                       # l'occurrence suivante
VK_F5 = 0x74                       # l'aller-à
MARGE_X = 8                        # la gouttière gauche de la peinture
MARGE_Y = 8                        # la gouttière haute


def vue_max(taille):
    """La borne SUPÉRIEURE du décalage de vue (loupe-11) : la DERNIÈRE
    fenêtre VOIT le dernier octet — aligne16_sup(max(0, taille − 384)).
    La règle de spécification, EXÉCUTABLE (le vérificateur la rejoue)."""
    if taille <= TAMPON_SESSION:
        return 0
    reste = taille - TAMPON_SESSION
    return (reste + 15) & ~15      # aligne16_sup : la fin visible


def recadre(curseur):
    """La règle de recadrage (loupe-12 Q3, citée par 14/15) : la ligne
    active posée à la 12e ligne — 11 lignes au-dessus quand la place se
    trouve, le bord sinon. La règle de spécification, EXÉCUTABLE."""
    cible = curseur - 11 * LIGNE_OCTETS
    if cible < 0:
        cible = 0
    return cible & ~15             # aligne16_inf




# =================================================================================
# L'ADRESSAGE DE L'IMAGE loupe.exe — ARRÊTÉ au chantier de la notation M10-(b)
# (D161 rejoué : la mesure auteur décide, la préfiguration s'incline ; les
# ZONES .data étaient ARRÊTÉES EN TAILLES au geste (a) — le geste (b) leur
# donne l'ADRESSE, la disposition ne bouge plus).
#
# LA RÈGLE DU GESTE (b) — LES HÉRITAGES VIVENT À LEURS ADRESSES SCELLÉES :
# les octets hérités ne bougent JAMAIS d'un pouce. Le tls13-02 scellé porte
# « lea rbp, [rip - 0x91a4] » — un déplacement RIP CODÉ POUR SON ADRESSE
# SCELLÉE (0xC080, visant la table K[64] @0x2F00) ; une relocalisation
# ré-écrite serait une contrebande de R7 ET un déplacement faux. L'image
# neuve RÉSERVE donc : .text 0x1000-0x1FFF la minilibc aux adresses M1
# (libc-01 @0x1100, la réserve libc-02 @0x1180 pour le chantier navigation,
# libc-07 @0x13C0 — le reste : la réserve M1 vierge) · .rdata 0x2000-0x2FFF
# (les tables MD5 puis l'IAT, K[64] @0x2F00 LA TABLE DU SCELLÉ que le
# déplacement hérité vise — l'IAT démo @0x2810+ sera réservée au chantier
# rendu pour win-03) · .text2 0x4000-0xBFFF LES BLOCS DU DOMAINE (0x4000
# la réserve d'entrée — WinMain vivra à loupe-09) · 0xC000-0xC3C0 la
# famille sha aux adresses M9 (tls13-01..04) · .data @0xE000 les zones du
# domaine (la marge 0xC3C0-0xE000 VIERGE, la famille sha s'arrête à 0xC3C0).
# =================================================================================

# --- .text @0x1000 : LA MINILIBC AUX ADRESSES SCELLÉES M1 (R7 — les octets
# --- du selftest.exe, jamais une copie ré-écrite ; seuls les héritages REQUIS
# --- PAR LE NOYAU (b) sont posés — libc-02 memcmp vivra à SON adresse
# --- scellée au chantier navigation, win-03 la boucle au chantier rendu) ;
# --- AU GESTE (c) : libc-02 POSEE @0x1180 (loupe-13) et win-03 POSEE @0x15C0
# --- (loupe-09) — le reste de la plage demeure LA RÉSERVE M1 VIERGE

R_LIBC01 = 0x1100             # libc-01 memcpy — L'ADRESSE SCELLÉE M1 (slot
                              # 0x80 : b20001) ; feuille pure, aucun
                              # déplacement RIP ; loupe-01 Q3 (la copie du
                              # chemin)
R_LIBC02 = 0x1180             # libc-02 memcmp — L'ADRESSE SCELLÉE RÉSERVÉE
                              # (b20002) : loupe-13 l'occupera au chantier
                              # navigation, l'octet scellé ne bouge pas
R_LIBC07 = 0x13C0             # libc-07 memset — l'adresse scellée M1 (slot
                              # 0x80 : b20007) ; loupe-04 Q2 (le cadre
                              # vierge), loupe-03 Q3 (l'hygiène) et loupe-06
                              # (les zéros du bourre)
R_WIN03 = 0x15C0              # win-03 LA BOUCLE DE MESSAGES — l'adresse
                              # scellée DÉMO (d40003, slot 0x80, 75 o de
                              # code) ; loupe-09 Q4 l'appelle PAR LA CARTE
                              # (R7 : les octets de demo.exe 0.3.0, jamais
                              # une ré-écriture — ses TROIS déplacements RIP
                              # visent l'IAT démo @0x2818/0x2820/0x2828)

# --- .rdata @0x2000 : LES TABLES MD5 PUBLIQUES (I2 de loupe-06 — la source
# --- unique du plan ; T ADJACENTE à S à +0x100 : la notation de loupe-06 lit
# --- les deux tables d'UNE seule base — [base + i*4] et [base + i*4 + 0x100])

R_MD5_S = 0x2100              # MD5_S[64] u32 — les décalages (RFC 1321 § 3.4)
R_MD5_T = 0x2200              # MD5_T[64] u32 — floor(2^32·|sin(i+1)|), la
                              # table DÉRIVÉE PAR ARITHMÉTIQUE au geste (a)

# --- .rdata @0x2000-0x20FF : LES PIÈCES DU RENDU (ARRÊTÉES au geste (c)) ----------
# L'entête de la grille (65 o utiles + NUL — la chaîne que loupe-10 pose à
# ECRAN+0) et LES DEUX TABLES HEXA (I4 de loupe-08 : « la table du plan ») :
# la MAJUSCULE pour la ligne et le curseur (la convention du journal des
# builds), la minuscule pour le PANNEAU (les empreintes du quotidien du
# projet, md5sum/sha256sum à minuscules).

R_ENTETE = 0x2000             # « Décalage  00 01 … 0F  ASCII » (65 + NUL)
R_HEX = 0x2050                # « 0123456789ABCDEF » (17 o)
R_HEXL = 0x2070               # « 0123456789abcdef » (17 o)

# --- .rdata @0x2300-0x23FA : LES LIBELLÉS DE LA BARRE (latin-1, NUL-terminés) -----
# Les textes nommés des specs : l'usage, la balise, les refus nommés de 12/14,
# les préfixes des modes, les fragments de la ligne de balise. Chaque adresse
# ARRÊTÉE ici (la source unique — la notation de loupe-10/12/14 la lit PAR
# DÉPLACEMENT RIP, le « · » y est le byte 0xB7 latin-1).

L_USAGE = 0x2300              # « loupe <fichier> » (16 o) — la vitrine vide
L_BALISE = 0x2310             # « Loupe 0.1.0-dev.1 » (18 o) — la lignée (D137)
L_TIRET = 0x2322              # « - » encadré (4 o) — le séparateur de balise
L_MID = 0x2326                # « · » encadré (4 o) — le séparateur des champs
L_OCT = 0x232A                # « o · curseur 0x » (16 o) — après la taille
L_MODIF = 0x233A              # « · MODIFIÉ » (11 o) — la marque sale (barre 1)
L_MD5 = 0x2345                # « md5 » (5 o) — le panneau
L_SHA = 0x234A                # « · sha256 » (11 o)
L_AST = 0x2355                # « * » (3 o) — l'astérisque du panneau (barre 2)
L_VIDE = 0x2358               # « - » (2 o) — le panneau de la vitrine vide
L_ALLER = 0x235A              # « ALLER (hexa) : » (16 o) — le mode de loupe-12
L_CHERCHER = 0x236A           # « CHERCHER (hexa) : » (19 o) — le mode de 14
L_MALFORMEE = 0x237D          # « saisie mal formée » (18 o) — E1 de loupe-12
L_HORSBORNES = 0x238F         # « hors bornes » (12 o) — E2 de loupe-12
L_SESSION = 0x239B            # « aucun fichier ouvert » (21 o) — E3 de 12/E2 14
L_FIN = 0x23B0                # « plus d'occurrence » (18 o) — la FIN de 14
L_PAIRES = 0x23C2             # « paires hexa attendues » (22 o) — E1 de 14
L_SYSTEME = 0x23D8            # « refus système » (14 o) — le -6 générique
L_ABSENT = 0x23E6             # « fichier introuvable » (20 o) — le -2 de 01

# --- .rdata @0x2600 : LES CHAÎNES UTF-16 (pilotées AUX API, hors expansion) -------
# La classe, le titre et l'explication fatale passent AUX API UTF-16 telles
# quelles (CreateWindowExW lit l'UTF-16 DIRECTEMENT — l'ém-dash U+2014 du
# titre y vit légitimement, lui qui ne passe pas l'expansion latin-1).

R_CLASSE = 0x2600             # « LoupeHexa » (20 o)
R_TITRE = 0x2614              # « Loupe — l'éditeur hexadécimal » (60 o)
R_ERREUR = 0x2650             # « La fenêtre de Loupe ne peut pas être créée. »
                              # (88 o — l'explication fatale, E1/E2 de 09)

# --- .rdata : L'IAT DU DOMAINE (D7/D35 : les feuilles déclarées au geste (a),
# --- l'ordre des listes est FIGÉ ; chaque feuille son qword — le miroir de la
# --- lignée démo ; la marge 0x2510-0x25FF est VIERGE, les chaînes UTF-16 du
# --- rendu vivent @0x2600+, l'IAT démo scellée @0x2818+ est RÉSERVÉE au geste
# --- (c) pour win-03 — LA RÈGLE DU GESTE (b) exécutée : les trois slots que
# --- les déplacements scellés de la boucle visent, TELS QUELS)

R_IAT_K32 = 0x2400            # IAT kernel32 (10 feuilles : 0x2400-0x2450)
R_IAT_U32 = 0x2450            # IAT user32 (18 feuilles : 0x2450-0x24E0)
R_IAT_GDI = 0x24E0            # IAT gdi32 (6 feuilles : 0x24E0-0x2510)

IAT_SLOTS = {}
for _nom in IAT_KERNEL32:
    IAT_SLOTS[_nom] = R_IAT_K32 + 8 * IAT_KERNEL32.index(_nom)
for _nom in IAT_USER32:
    IAT_SLOTS[_nom] = R_IAT_U32 + 8 * IAT_USER32.index(_nom)
for _nom in IAT_GDI32:
    IAT_SLOTS[_nom] = R_IAT_GDI + 8 * IAT_GDI32.index(_nom)
del _nom

# --- .rdata : LA TABLE DU SCELLÉ — K[64] @0x2F00 (LA MÊME ADRESSE que le
# --- scellé M9 : le déplacement RIP de tls13-02 hérité la vise TELLE QUELLE ;
# --- les 64 constantes FIPS 180-4 § 4.2.2 vivent à tls13/layout.py, la
# --- source unique — le plan loupe RENVOIE, jamais re-déclare)

R_K = 0x2F00                  # K[64] u32 — la table de tls13-02 (le scellé)

# --- .rdata @0x2818-0x282F : L'IAT DÉMO SCELLÉE (les TROIS slots de win-03) -------
# LA RÈGLE DU GESTE (b) EXÉCUTÉE AU GESTE (c) : « tout héritage à SON adresse
# scellée (win-03 et son IAT démo au chantier rendu) ». La boucle scellée
# (demo.exe 0.3.0, 75 o @0x15C0) porte TROIS déplacements RIP codés pour les
# slots IAT user32 DE L'IMAGE DÉMO : 0x15dd+0x6+0x1235 = 0x2818 (GetMessageW),
# 0x15ea+0x6+0x1230 = 0x2820 (TranslateMessage), 0x15f3+0x6+0x122f = 0x2828
# (DispatchMessageW). L'image loupe RÉSERVE les TROIS qwords À LEURS ADRESSES
# D'ORIGINE : le build y posera les adresses résolues (les MÊMES feuilles que
# l'IAT loupe @0x2468/0x2470/0x2478 — la double entrée n'est pas une
# redondance, c'est le PRIX du déplacement scellé : R7 au sens propre).

R_IAT_DEMO_GMW = 0x2818       # GetMessageW (le slot que win-03 vise)
R_IAT_DEMO_TM = 0x2820        # TranslateMessage
R_IAT_DEMO_DMW = 0x2828       # DispatchMessageW

# --- .text2 @0x4000 : LES BLOCS DU DOMAINE ARRÊTÉS sur les longueurs réelles
# --- MESURÉES par outils/auteur.py au chantier (b) (D161 : multiples de 64,
# --- padding >= 16, tassés depuis 0x4040 — 0x4000-0x403F la réserve d'entrée
# --- [WinMain à loupe-09] ; le MINIMUM admissible par longueur ; les familles
# --- rendu/navigation/édition s'arrêteront au geste de LEUR notation) :
# ---   loupe-04 :  47 o notés -> slot 0x40  (padding 17 — la fondation)
# ---   loupe-01 : 388 o notés -> slot 0x1C0 (padding 60 — la session née
# ---                              entière : CreateFileW + la borne + la copie
# ---                              + les TROIS compositions 02/07/03-sur-refus)
# ---   loupe-02 : 296 o notés -> slot 0x140 (padding 24 — la double borne +
# ---                              LE RECOUVREMENT du journal)
# ---   loupe-03 : 122 o notés -> slot 0xC0  (padding 70 — l'idempotence +
# ---                              l'hygiène)
# ---   loupe-05 : 312 o notés -> slot 0x180 (padding 72 — la composition
# ---                              héritée aux fenêtres glissantes)
# ---   loupe-06 : 879 o notés -> slot 0x380 (padding 17 — LA NOTATION NEUVE :
# ---                              les 64 tours, les 4 rounds, le couplage, le
# ---                              bourre, l'extraction — le plus grand bloc du
# ---                              noyau)
# ---   loupe-07 : 102 o notés -> slot 0x80  (padding 26 — la composition seule)
# --- fin du noyau : 0x49C0 — les familles suivantes suivent à la contiguïté

LOUPE04_VA = 0x4040           # i110004 — le cadre (la fondation, posée la
                              # première : loupe-01 l'appelle À SA TÊTE)
LOUPE01_VA = 0x4080           # i110001 — ouvrir (la session née entière)
LOUPE02_VA = 0x4240           # i110002 — lire (la fenêtre bornée + le
                              # recouvrement du journal)
LOUPE03_VA = 0x4380           # i110003 — fermer (idempotent, l'hygiène)
LOUPE05_VA = 0x4440           # i110005 — sha256 (la composition héritée)
LOUPE06_VA = 0x45C0           # i110006 — md5 (la notation neuve, RFC 1321)
LOUPE07_VA = 0x4940           # i110007 — le cumul (la composition seule)

SLOTS_LOUPE = {
    "i110001": (LOUPE01_VA, 0x1C0),
    "i110002": (LOUPE02_VA, 0x140),
    "i110003": (LOUPE03_VA, 0xC0),
    "i110004": (LOUPE04_VA, 0x40),
    "i110005": (LOUPE05_VA, 0x180),
    "i110006": (LOUPE06_VA, 0x380),
    "i110007": (LOUPE07_VA, 0x80),
}

# =================================================================================
# L'ADRESSAGE DU GESTE (c) — LES FAMILLES RENDU + NAVIGATION (loupe-08..14)
# (D161 rejoué une troisième fois : les slots ci-dessous sont PRÉFIGURÉS à la
# plume pour la première passe de mesure, la MESURE de l'auteur les ARRÊTERA
# aux minimums admissibles — multiples de 64, padding >= 16, tassés à la
# contiguïté du noyau depuis 0x49C0).
#
# L'ORDRE DU TASSEMENT (arrêté au geste (c), une raison d'architecture) :
#   loupe-08 (la feuille pure, la fondation du rendu) · loupe-10 (le peintre)
#   · loupe-11 (le défilement) · loupe-12 (l'aller) · loupe-13 (la feuille
#   pure de la recherche) · loupe-14 (le suivant, qui compose 12 et 13) ·
#   LOUPE-09 DERNIER — le bloc d'entrée (WinMain + LA PROCÉDURE) : sa table
#   de routage S'ÉTENDRA au chantier (d) (les blocs 15-18 n'existent pas
#   encore : leurs messages demeurent chez DefWindowProcW à (c), révision
#   nommée à venir) ; placé DERNIER, l'extension ne bougera QUE son propre
#   slot — les notations (c) de 08/10/11/12/13/14 demeurent INTACTES, la
#   famille édition suivra à sa suite. Les appelés précèdent l'appelant.
#
# La réserve d'entrée 0x4000-0x403F (la préfiguration du geste (b), 64 o)
# S'INCLINE : l'écran mesuré ne tient pas en 64 o — WinMain vivra à SON slot
# (loupe-09, le dernier du tassement) et l'AddressOfEntryPoint du futur build
# visera LOUPE09_VA TEL QUEL (aucune fiction de trampoline : l'entrée est UNE
# adresse, celle du bloc — D33 l'image PI, D161 la mesure décide).
# =================================================================================

LOUPE08_VA = 0x49C0           # i110008 — la ligne (feuille pure, 77 o)
LOUPE10_VA = 0x4B00           # i110010 — la peinture (l'unique peintre)
LOUPE11_VA = 0x5180           # i110011 — le défilement (borné à la fin)
LOUPE12_VA = 0x5400           # i110012 — l'aller (la barre-saisie)
LOUPE13_VA = 0x5740           # i110013 — la recherche (feuille pure)
LOUPE14_VA = 0x5800           # i110014 — le suivant (le recouvrement)
LOUPE09_VA = 0x5C00           # i110009 — l'écran (WinMain + LA PROCÉDURE,
                              # DERNIER du tassement : la table s'étend à (d))
# L'ARRÊT SUR LES MESURES (D161, la troisième passe — 08/11 : 271/568/796/
# 126/983/874/1614 o notés (14 : LE PLANCHER QUI NE RECULE JAMIS —
# la correction du premier jet, attrapée par le témoin à frontières) → les slots MINIMUMS, tassés à la contiguïté du
# noyau depuis 0x49C0 : 08 @0x49C0 [0x140, padding 49] · 10 @0x4B00 [0x680,
# padding 50 — le plus grand bloc du geste] · 11 @0x5180 [0x280, padding 72]
# · 12 @0x5400 [0x340, padding 36] · 13 @0x5740 [0xC0, padding 66] · 14
# @0x5800 [0x400, padding 41] · 09 @0x5C00 [0x380, padding 22] — fin du
# geste (c) : 0x5F80, la marge jusqu'aux sha @0xC000 VIERGE)

SLOTS_LOUPE.update({
    "i110008": (LOUPE08_VA, 0x140),
    "i110009": (LOUPE09_VA, 0x380),
    "i110010": (LOUPE10_VA, 0x680),
    "i110011": (LOUPE11_VA, 0x280),
    "i110012": (LOUPE12_VA, 0x340),
    "i110013": (LOUPE13_VA, 0xC0),
    "i110014": (LOUPE14_VA, 0x400),
})

# --- 0xC000-0xC3C0 : LA FAMILLE SHA AUX ADRESSES SCELLÉES M9 (R7 — les octets
# --- du proxy.exe 1.0.0 POSÉS À LEURS ADRESSES D'ORIGINE : les déplacements
# --- RIP et l'appel absolu scellé [call 0xC080 de tls13-03/04] demeurent
# --- JUSTES TELS QUELS ; la table K @0x2F00 est la cible du déplacement
# --- scellé — posée identique en .rdata)

R_TLS01 = 0xC000              # tls13-01 sha256-init — l'adresse scellée M9
                              # (slot 0x80 : h100001) ; loupe-05 Q2
R_TLS02 = 0xC080              # tls13-02 sha256-comprimer — l'adresse scellée
                              # (slot 0x1C0 : h100002) ; vit à l'intérieur de
                              # tls13-03 (l'appel ABSOLU scellé la vise)
R_TLS03 = 0xC240              # tls13-03 sha256-absorber — l'adresse scellée
                              # (slot 0xC0 : h100003) ; loupe-05 Q2
R_TLS04 = 0xC300              # tls13-04 sha256-finaliser — l'adresse scellée
                              # (slot 0xC0 : h100004) ; loupe-05 Q2

# --- .data @0xE000 : LES ZONES DU DOMAINE (les tailles ARRÊTÉES au geste (a) —
# --- les adresses ARRÊTÉES ICI ; la disposition source unique, jamais bougée)

R_CADRE = 0xE000              # loupe-04 : le cadre de session 960 o
R_EMPREINTES = 0xE3C0         # loupe-07 : le panneau (md5[16] + sha256[32])
R_SAISIE = 0xE400             # loupe-12 : la barre-saisie 96 o
R_MOTIF = 0xE460              # loupe-13/14 : le motif 48 o
R_JOURNAL = 0xE4A0            # loupe-16 : le journal 4112 o (256 × 16 + 8)
R_ECRAN = 0xF4C0              # loupe-09 : l'écran 2320 o (fin 0xFDD0)
R_HWND = 0xFDE0               # loupe-09 : HWND_PRINCIPAL (fin 0xFDE8)
R_METRIQUES = 0xFDF0          # loupe-10 : la police mesurée une fois
R_CUMUL = 0x10000             # LA fenêtre de lecture 64 Kio (l'exclusion de
                              # famille : empreintes 05/06/07 + recherche 14)
# LE CADRE À L'IMAGE naît poignée INVALIDE : l'initialiseur .data du build
# posera 0xFFFF…FFFF à +528 (le miroir du harnais, qui pose le même état
# AVANT tout appel — le zéro de la mémoire vierge serait une session
# fantôme : loupe-02 y croirait) ; loupe-04 reste LE geste de remise au
# vierge en cours de vie (loupe-01/03 l'appellent)
