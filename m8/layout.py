"""layout.py — Plan d'adressage du projet TRIADE, jalon M8 (profil
x86-64-win11-pe, le domaine sys — l'ère 0.9.0 des additions mesurées, D160).

Source unique de vérité partagée par le futur build_m8.py, outils/auteur.py
et oracle du jalon (les chantiers (b)/(c)). Toute adresse, tout décalage,
toute constante du domaine dérive d'ici ; la notation référencera ces
constes et le builder vérifiera la concordance. La présente version NAÎT à
l'ouverture (couche I écrite-avant-code, modèle D77) : les RVA définitifs
des blocs seront ARRÊTÉS au chantier (b) sur les longueurs réelles des
notations (D47/D79 — la mesure auteur décide, la préfiguration n'est pas
un droit).

HÉRITAGE M0/M1/M2/M3/M4/M5 (R7 — jamais déplacé) :
  - le proxy.exe 0.6.0 SCELLÉ (m5/, sha consigné à la carte génération 7) :
    TOUT son plan d'adressage vit dans m5/layout.py — le présent module le
    CHARGE par chemin absolu (leçon D158 : les layout.py homonymes se
    chargent par importlib, jamais par sys.path) et n'ajoute QUE la
    section .text5 et les constantes du domaine sys ;
  - .text/.rdata/.data/.text2/.text3/.text4 COMPLÈTES (0x1000-0x9FFF) :
    l'extension M8 vit dans une section NOUVELLE .text5 — le corps scellé
    0.6.0 ne bouge pas d'un octet (§ 9).

LA SECTION .text5 (préfiguration D160 — arrêt définitif au chantier (b)) :
  0xA000-0xBFFF (8 Kio, modèle .text3/.text4) ; SizeOfImage 0xA000 → 0xC000
  et la table de sections 6 → 7 entrées AU BUILD du chantier (c) — deltas PE
  documentés alors (modèle D94/D136). Slots préfigurés (D8 — multiples de
  64, alignés 16, padding >= 16) :
    sys-01 @ 0xA000 (0x80)   l'émetteur — six octets utiles, int3 au reste ;
    sys-02 @ 0xA400 (0x400)  le résolveur — la marche EAT, le motif ;
    sys-03 @ 0xB000 (0x800)  la twin de hello-02 — résoudre + neuf args ;
    réserve 0xB800-0xBFFF (croissance du domaine : sys-04 et suivants).

LES CONSTANTES DU DOMAINE (charte m8/I/README.md — source unique ici) :
  - MOTIF_STUB : les quatre premiers octets du stub natif Windows 10/11
    x64 (4C 8B D1 B8 = mov r10, rcx ; mov eax, imm32) — vérifié AVANT
    toute extraction (charte § 2) ; le labo prouve sur FIXTURES, le
    terrain mesure le VRAI (la version Windows du run consignée au
    témoin) ; OFF_SSN : le décalage de l'imm32 dans le stub (4) ;
  - les décalages PE/EAT : le format PE32+ est STABLE (documenté) —
    e_lfanew @ +0x3C (fenêtre lisible [0x40, 0x400]), le motif « PE\\0\\0 »,
    le répertoire export (1re entrée du DataDirectory) @ PE+0x88
    (RVA) / +0x8C (taille), et dans le répertoire export :
    NumberOfFunctions @ +0x14, NumberOfNames @ +0x18,
    AddressOfFunctions @ +0x1C, AddressOfNames @ +0x20,
    AddressOfNameOrdinals @ +0x24 (tous RVA 32 bits relatifs à la base) ;
  - la TABLE DES VERDICTS du domaine (charte § 5) — les SEPT noms, jamais
    recopiés dans les spécifications ;
  - les versions de l'ère : 0.9.0-dev.1 (posée par le premier build M8 —
    geste de BUILD, jamais scellage, miroir M6/M7 D149) et 0.9.0 (la
    finale attendra le terrain vert du chantier (d)) ; le plancher R10
    demeure 0x00040000 (hérité — l'anti-rollback ne se relâche pas d'une
    ère à l'autre).
"""

import importlib.util
import os

# --- L'héritage m5 chargé par chemin absolu (leçon D158) ------------------------

ICI = os.path.dirname(os.path.abspath(__file__))
_CHEMIN_M5 = os.path.join(os.path.dirname(ICI), "m5", "layout.py")
_spec = importlib.util.spec_from_file_location("layout_m5", _CHEMIN_M5)
L5 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(L5)

# --- Image et sections (l'héritage réexporté — le build (c) compose depuis 0.6.0)

IMAGE_BASE = L5.IMAGE_BASE
SIZE_OF_IMAGE_M5 = L5.SIZE_OF_IMAGE          # 0xA000 — le corps scellé 0.6.0
SIZE_OF_IMAGE = 0xC000                       # 0xA000 + .text5 (AU BUILD (c))
TEXT5_VA = 0xA000                            # la section NOUVELLE du jalon
TEXT5_RAW = None                             # offset fichier arrêté au (c)
TAILLE_FICHIER_M5 = L5.TAILLE_FICHIER        # le scellé — ne bouge pas

# --- Les slots préfigurés du domaine sys (arrêt définitif au chantier (b)) ------

SYS01_VA = 0xA000        # g90001 — l'émetteur (slot 0x80)
SYS02_VA = 0xA400        # g90002 — le résolveur (slot 0x400)
SYS03_VA = 0xB000        # g90003 — la twin de hello-02 (slot 0x800)
ZONE_SYS = (0xA000, 0xBFFF)       # .text5 entière
ZONE_SYS_RESERVE = (0xB800, 0xBFFF)   # la croissance du domaine
SLOTS_SYS = {
    "g90001": (SYS01_VA, 0x80),
    "g90002": (SYS02_VA, 0x400),
    "g90003": (SYS03_VA, 0x800),
}

# --- Les constantes du domaine (charte m8/I/README.md — source unique) ----------

MOTIF_STUB = bytes.fromhex("4C8BD1B8")   # mov r10, rcx ; mov eax, imm32
OFF_SSN = 4                              # l'imm32 du SSN dans le stub
MOTIF_PE = b"PE\x00\x00"
E_LFANEW = 0x3C                          # DOS → offset du motif PE
E_LFANEW_MIN = 0x40                      # la fenêtre lisible (verdict -2 sinon)
E_LFANEW_MAX = 0x400
OFF_EXPORT_RVA = 0x88                    # DataDirectory[0] (PE32+) : RVA
OFF_EXPORT_TAILLE = 0x8C                 #                       : taille
EXP_NBFONC = 0x14                        # le répertoire export :
EXP_NBNOMS = 0x18                        #   NumberOfNames (la borne, charte § 8)
EXP_ADRFONC = 0x1C                       #   AddressOfFunctions (RVAs)
EXP_ADRNOMS = 0x20                       #   AddressOfNames (RVAs des noms)
EXP_ADRORD = 0x24                        #   AddressOfNameOrdinals (u16)

# la TABLE DES VERDICTS (charte § 5 — les SEPT noms du domaine)
V_RESOLU = 0            # succès : résolu (sys-02) / émis (sys-03)
V_NOM_ABSENT = -1       # le nom est introuvable dans l'EAT (marche complète)
V_PAS_MODULE = -2       # la base n'est pas un module PE (motif / e_lfanew fou)
V_EAT_ABSENTE = -3      # le répertoire export est absent (RVA nul)
V_STUB_DIVERGENT = -4   # le stub diverge du motif (hook ou ère inconnue)
V_SPAN_INVALIDE = -5    # le span du nom est invalide (nul / longueur nulle)
V_STATUS_NONNUL = -6    # le syscall a rendu un STATUS non nul (consigné rdx)

# --- Les versions de l'ère (geste de BUILD au premier build — jamais scellage) ---

VERSION_DEV1 = "0.9.0-dev.1"     # posée par le premier build M8 (chantier (c))
VERSION_U64_DEV1 = 0x00090001
VERSION_U64_MIN = 0x00040000     # le plancher R10 hérité (jamais relâché)
VERSION_FINALE = "0.9.0"         # la finale attend le terrain vert du (d)

# --- Les noms de blocs (la carte génération 8 — chantier (c)) -------------------

NOMS_BLOCS = dict(L5.NOMS_BLOCS) | {
    "g90001": "sys-01-emetteur",
    "g90002": "sys-02-resolveur",
    "g90003": "sys-03-ecriture",
}
