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
    "InvalidateRect",              # loupe-10/11/12/14/15/16/17 (le repaint)
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
