#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""scenario-loupe.py — LE TERRAIN M10-(e) : LE RUN DE LOUPE, LE GRANDEUR
NATURE (kit dev.8, l'Entrée 210).

Le kit porte UN artefact et UN scénario :
  loupe.exe   le build 0.1.0-dev.7 du jalon M10 — 127 488 o, sha256
              388d468067cbf05411a6227c5906baa27d5cbf8a6f862e4cec6a051cab4d9bbc
              (LA RETOUCHE DOUBLE DE L'ENTRÉE 210 : le run terrain du kit
              dev.7 a tenu T0 → T5 TOUT VERT — la sauvegarde de l'Entrée
              209 PROUVÉE — puis a nommé DEUX défauts D'UN MÊME TÉMOIN.
              PREMIER DÉFAUT [EAX-SANS-SIGNE] AU KIT : T6 lisait
              « 0xfffffffe != -2 ABSENT » — la pièce rendait SES codes
              d'échec par « mov eax, imm32 » — EAX seul, les 32 bits
              hauts de RAX à zéro — et le contrat publié du scénario
              [c_int64] lisait le qword ENTIER : dev.7 étend chaque
              rendu négatif au 64 bits [« push imm8 ; pop rax » — 20
              sites — et les deux passages de loupe-01 passés movsxd] ;
              SECOND DÉFAUT [D54-QUATRIÈME] À LA PIÈCE : la vitrine
              demeurait MORTE 0xC0000005 sur LES DEUX fenêtres, AUCUN
              rapport WER, alors que TOUT était propre — l'entrée, le
              WndProc, la boucle, les 63 appels couverts, la table
              d'imports PARFAITE — LE DIFFÉRENTIEL A NOMMÉ : la lignée
              prouvée [demo.exe 0.3.0, le scellé M2 dont la fenêtre
              VÉCUT au terrain] termine CHAQUE plage FirstThunk par un
              slot NULL ; le build dev.6 posait les QUATRE plages
              CONTIGUËS [kernel32@0x2400, user32@0x2450, gdi32@0x24E0,
              double@0x2818 — le chargeur du terrain (Windows 11 build
              26300, le CHEMIN FirstThunk de la leçon D97) marche chaque
              plage jusqu'au slot NULL : la marche de kernel32 déborde
              dans les noms user32, RegisterClassExW résout à NULL, et
              l'entrée APPELLE LE NUL — 0xC0000005 sans dialogue ;
              QUATRIÈME manifestation de la dérive de dépôt [D54, D68,
              D98, et celle-ci] ; LA RETOUCHE : l'IAT ENTIÈRE relogée à
              0x3100 [région née zéro], QUATRE plages SÉPARÉES PAR NULL
              et PRÉREMLIES des RVA de noms [le motif D54 au complet],
              les descripteurs dirigés, dir[12] mis à jour, les 63 sites
              d'appel repointés, les vieilles plages VIDÉES — la taille
              DEMEURE 127 488 o, AUCUNE adresse scellée ne bouge [R7 :
              le WndProc @0x5DCB, la famille sha M9, la minilibc, la
              table K[64], le CADRE — octets inchangés] ; ET LA LEÇON
              INSTITUTIONNALISÉE : le scénario dev.8 VÉRIFIE LUI-MÊME
              l'habillage [chaque plage marchée au compte exact, les
              séparateurs NULL, les slots préremplis] — l'habillage
              d'import fait partie de la surface de test, la leçon D97
              ENTRE AU SCÉNARIO ; le qword version 0x00010006 →
              0x00010007) ;
  le présent script — python SEUL (ctypes, hashlib, os, platform, struct,
              sys, tempfile — AUCUN paquet à installer).

LE GESTE DU SCÉNARIO : le scénario est LE CHARGEUR (LoadLibraryEx
DONT_RESOLVE — aucune entrée résolue, AUCUN point d'entrée exécuté : la
vitrine n'est pas lancée ici), puis il RÉSOUT LUI-MÊME les 34 feuilles de
l'IAT du plan (VirtualProtect sur les slots .rdata — le chargeur réel
fait de même à la liaison) et APPELLE LES BLOCS À LEURS ADRESSES
SCELLÉES : l'application née des blocs notés, conduite par la main du
kit. LA VITRINE se vit À CÔTÉ, ET SON TÉMOIN EST NOUVEAU AU KIT (l'Entrée
207 : la vitrine a VÉCU sa première fois au terrain et sa mort fut
sans témoin — « la fenêtre s'ouvre et se referme immédiatement ») :
lancez temoin-vitrine.bat — le run console de la vitrine, LES DEUX
façons (sans fichier puis avec un fichier), le CODE DE SORTIE capturé
(%ERRORLEVEL% : 0 la sortie propre · 1 l'explication MessageBox ·
0xC0000005 le crash — le rapport WER du système le nomme alors) — les
pièces vont au réceptacle preuves-loupe/ ; puis double-cliquez
loupe.exe — la fenêtre réelle, les octets à l'œil, le panneau
d'empreintes (le LISEZMOI du kit documente les gestes : la molette, F5
l'aller, F3 la recherche, la saisie hexa, Ctrl+S, le double Alt+F4).

LA SONDE DE L'ENTRÉE 205 (LA CASCADE DIAGNOSTIQUE — le kit porte SON
PROPRE BISSECTEUR) : après le run (ou à l'échec de la cartographie), le
scénario reconstitue UN À UN les axes par lesquels dev.2 sortait de
l'enveloppe de la lignée — LE TROU DE PAGE (.rdata 0x1000), LE BSS
MASSIF (.data RS 0x400), LE SOUS-SYSTÈME GUI (→ CUI), PUIS LA
GÉOMÉTRIE dev.2 ENTIÈRE — sur des COPIES TEMPORAIRES nées et mortes
dans %TEMP% (loupe.exe lui-même n'est JAMAIS écrit) : le VRAI
chargeur Windows NOMME l'axe fautif. Le mode d'erreur du processus
coupe les boîtes bloquantes du chargeur : le refus est nommé PAR LE
TÉMOIN, pas muré derrière un bouton OK.

CE QUE LE RUN DÉMONTRE (chaque constat tranché binaire, le verdict
POST-MORTEM — un échec nommé vaut plus qu'un vert muet) :

  T0 LE TÉMOIN      l'empreinte de l'artefact ASSERTÉE avant tout geste ;
                   l'environnement consigné (Windows, Python 64 bits) ;
                   les adresses scellées CONSTATÉES UN PAR UN dans
                   l'image (la minilibc M1 @0x1100/0x1180/0x13C0, la
                   boucle démo @0x15C0, la famille sha M9 @0xC000+, LA
                   TABLE K[64] @0x2F00 — les constantes FIPS 180-4, le
                   qword version R10 @0x2E80, le CADRE .data né LE MIROIR
                   du harnais [la poignée INVALIDE à +528, le reste né
                   zéro — la leçon de l'Entrée 206, le .data ENTIER
                   relu], l'IAT démo réservée @0x2818, LE BASERELOC
                   minimal déclaré dirs[5] (la leçon de l'Entrée 204 :
                   sans table, le VRAI chargeur refuse de reloger
                   l'image ASLR).
  T1 LA SESSION     loupe-01 à SON adresse scellée : le VRAI fichier
                   ouvert par l'application (CreateFileW par l'IAT
                   résolue), le cadre relu champ à champ (le chemin, la
                   taille EXACTE, la poignée vivante) — sur L'OMBRE
                   BYTE-À-BYTE DE LA PIÈCE (l'Entrée 208 : le scénario
                   EST LE CHARGEUR, l'image TIENT loupe.exe sans partage
                   d'écriture, le VRAI Windows refuse gle 32 et loupe-01
                   l'a NOMMÉ -7 VERROUILLÉ — LA PIÈCE ACQUITÉE, le
                   refus traduit AU NOM PRÈS : la session naît sur
                   temoin-session.bin, LA COPIE byte-à-byte née et morte
                   au run — même loi que la sonde 205 et le témoin
                   vitrine).
  T2 LA DOUBLE      LE NOYAU EMPREINTES : loupe-02 la fenêtre lue au
     LECTURE       tampon == le fichier lu par Python (les DEUX lecteurs
                   indépendants) ; loupe-07 le panneau (md5 + sha256 du
                   fichier ENTIER par fenêtres glissantes) ==
                   hashlib.md5 + hashlib.sha256 — ET LA PIÈCE DE L'ÈRE
                   JUGÉE PAR SA PROPRE APPLICATION : loupe-07 sur
                   loupe.exe LUI-MÊME rend son sha256_asserté
                   13a869a3b31b41d6….
  T3 LES LIGNES     loupe-08 la ligne : la première ligne de loupe.exe
                   == le format composé en Python pur (les DEUX
                   lecteurs encore) ; la ligne finale incomplète garde
                   le FORMAT (l'alignement des colonnes est un
                   invariant).
  T4 LA RECHERCHE   loupe-13 (le memcmp SCELLÉ M1 à l'œuvre) : le
                   motif cherché dans une fenêtre du fichier ==
                   bytes.find — l'algorithme pur sur le vrai disque.
  T5 L'ÉDITION      LA BOUCLE ENTIÈRE sur une copie : loupe-16 la
                   saisie (« 4 » puis « d » — l'attente CONSOMMÉE par
                   l'engagement), loupe-17 la sauvegarde (Ctrl+S :
                   l'écriture À L'OCTET, le contrat publié : 0 = OK, le
                   compte à la barre d'état — l'Entrée 209) ; le fichier
                   revérifié : EXACTEMENT l'octet changé, la taille
                   CONSTANTE, le journal vidé, la marque levée.
  T6 LES REJETS     L'ÉCHEC NOMMÉ : le motif absent → -1 FIN ; le
                   chemin qui ne désigne rien → -2 ABSENT ; la session
                   double → -5 (un fichier à la fois — l'offrande est
                   L'OMBRE rouvrable, jamais la pièce scellée sous le
                   chargeur : le frère du défaut T1 chassé par la
                   classe, l'Entrée 208) ; le décalage hors bornes →
                   -3 ; la ligne de longueur 0 → -5.
  T7 LA CLÔTURE     loupe-03 : le cadre re-vierge, la poignée
                   INVALIDE, idempotent ; l'artefact relu INCHANGÉ
                   (sha256 re-asserté — le run ne touche pas la pièce).
  S0 LA SONDE      LA CASCADE DIAGNOSTIQUE DE L'ENTRÉE 205 : les axes
     (205)         de dev.2 reconstitués UN À UN sur des copies %TEMP%
                   (le trou de page, le BSS, le sous-système, la
                   géométrie entière) — le VRAI chargeur NOMME l'axe
                   fautif ; loupe.exe n'est jamais écrit.

Le journal du run : preuves-loupe/temoin-loupe.txt (créé par le
scénario, à renvoyer au coffre avec les éventuelles captures de la
vitrine).

Usage (double-clic ou invite) : python scenario-loupe.py
Code de sortie : 0 = run VERT sur pièces ; 1 = échec nommé."""

import ctypes
import ctypes.wintypes as wt
import hashlib
import os
import platform
import struct
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
PREUVES = os.path.join(ICI, "preuves-loupe")
JOURNAL = []

# --- l'artefact : l'empreinte ASSERTÉE prouve CES octets (la carte demeure
#     en génération 13 — la régénération est dette au labo, l'Entrée 211) -----
SHA_EXE = ("388d468067cbf05411a6227c5906baa27d5cbf8a6f862e4c"
           "ec6a051cab4d9bbc")
TAILLE_EXE = 127488
VERSION_R10 = 0x00010007          # loupe 0.1.0-dev.7 (le qword @0x2E80 —
                                   # la retouche de l'Entrée 210 : [D54-QUATRIÈME]
                                   # chassé, l'IAT relogée séparée à 0x3100,
                                   # et [EAX-SANS-SIGNE] étendu au 64 bits)
VERSION_TXT = f"0.1.0-dev.{VERSION_R10 & 0xFFFF}"   # dynamique — le littéral périmé chassé (dev.9, l'Entrée 213)

# --- les adresses scellées (le plan, source unique — R7) -------------------------
R_LIBC01 = 0x1100      # memcpy M1 (le scellé selftest.exe)
R_LIBC02 = 0x1180      # memcmp M1 (le scellé selftest.exe)
R_LIBC07 = 0x13C0      # memset M1 (le scellé selftest.exe)
R_WIN03 = 0x15C0       # la boucle de messages (le scellé demo.exe 0.3.0)
R_MD5_S = 0x2100       # les 64 décalages RFC 1321 § 3.4
R_MD5_T = 0x2200       # les 64 sinus dérivés floor(2^32·|sin(i+1)|)
R_IAT_K32 = 0x3100     # l'IAT kernel32 (10 feuilles — l'Entrée 210 :
                       # QUATRE plages SÉPARÉES PAR NULL à 0x3100, le
                       # motif D54 complet — préremplies + terminées)
R_IAT_U32 = 0x3158     # l'IAT user32 (18 feuilles)
R_IAT_GDI = 0x31F0     # l'IAT gdi32 (6 feuilles)
R_IAT_DEMO = 0x3228    # les TROIS slots de win-03 (la double entrée)
IAT_SEPARATEURS = (0x3150, 0x31E8, 0x3220, 0x3240)  # les NULL qui
                       # terminent chaque plage — LA CLÉ DU TERRAIN
                       # (le chargeur 26300 marche au premier NULL : la
                       # leçon D97, la quatrième manifestation nommée)
R_VERSION = 0x2E80     # le qword version (la porte R10)
R_RELOC = 0x2E90       # le BASERELOC minimal (12 o, entrées ABSOLUTE —
                       # l'image PI que le chargeur PEUT reloger : la
                       # leçon de l'Entrée 204, dirs[5])
R_K = 0x2F00           # la table K[64] du scellé M9 (FIPS 180-4 § 4.2.2)
R_TLS01 = 0xC000       # sha256-init (le scellé proxy.exe 1.0.0)
R_TLS02 = 0xC080       # sha256-comprimer
R_TLS03 = 0xC240       # sha256-absorber
R_TLS04 = 0xC300       # sha256-finaliser
R_LOUPE01 = 0x4080     # ouvrir
R_LOUPE02 = 0x4240     # lire
R_LOUPE03 = 0x4380     # fermer
R_LOUPE07 = 0x4940     # le cumul (le panneau)
R_LOUPE08 = 0x49C0     # la ligne
R_LOUPE13 = 0x5740     # la recherche
R_LOUPE16 = 0x6240     # la saisie
R_LOUPE17 = 0x6500     # la sauvegarde
R_CADRE = 0xE000       # le cadre de session 960 o
DATA_VSIZE = 0x12000   # la taille .data du plan (VS == RS — l'Entrée 205 :
                       # le .data ENTIER relu contre le miroir à la naissance)
CADRE_CHEMIN = 0       # UTF-16[260] @ +0
CADRE_TAILLE = 520     # u64 @ +520
CADRE_POIGNEE = 528    # u64 @ +528 (INVALIDE hors session)
CADRE_VUE = 536        # u64 @ +536
CADRE_CURSEUR = 544    # u64 @ +544
CADRE_REMPLISSAGE = 552  # u32 @ +552
CADRE_SALE = 556       # u32 @ +556
CADRE_TAMPON = 568     # 384 o @ +568
INVALIDE = 0xFFFFFFFFFFFFFFFF

# les premières instructions des héritages scellés (relues au T0 — les
# ancres R7 constatées dans l'image, la preuve que les octets n'ont pas
# bougé d'un pouce : les PROLOGUES DES SCELLÉS relus à la source)
TETE_LIBC01 = bytes.fromhex("57564889c848")  # push rdi; push rsi; mov rax,rcx
TETE_LIBC02 = bytes.fromhex("31c04d85c074")  # xor eax,eax; test r8,r8; je …
TETE_LIBC07 = bytes.fromhex("53574889cb48")  # push rbx; push rdi; mov rbx,rcx
TETE_WIN03 = bytes.fromhex("534154415541")   # push rbx; push rsp; push r13; …
TETE_TLS01 = bytes.fromhex("c70167e6096a")   # mov dword [rcx], 0x6A09E667
                                               # — H0[0] FIPS 180-4 § 5.3.1
                                               # posé par le scellé M9

# les 64 constantes K de SHA-256 (FIPS 180-4 § 4.2.2 — la table du
# scellé M9 posée identique @0x2F00, le déplacement hérité de tls13-02
# la vise) : LES QUATRE PREMIÈRES + LES QUATRE DERNIÈRES contrôlées.
K_TETE = (0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5)
K_QUEUE = (0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2)

# l'IAT du plan : l'ORDRE FIGÉ du geste (a) — le scénario résout et pose
IAT_KERNEL32 = ("GetModuleHandleW", "GetCommandLineW", "ExitProcess",
                "CreateFileW", "GetFileSizeEx", "SetFilePointerEx",
                "ReadFile", "WriteFile", "CloseHandle", "GetLastError")
IAT_USER32 = ("RegisterClassExW", "CreateWindowExW", "ShowWindow",
              "GetMessageW", "TranslateMessage", "DispatchMessageW",
              "DefWindowProcW", "BeginPaint", "EndPaint", "InvalidateRect",
              "GetClientRect", "GetScrollInfo", "SetScrollInfo",
              "DestroyWindow", "PostQuitMessage", "LoadCursorW",
              "MessageBeep", "MessageBoxW")
IAT_GDI32 = ("GetStockObject", "SelectObject", "GetTextMetricsW",
             "TextOutW", "SetTextColor", "SetBkColor")
IAT_DEMO = ("GetMessageW", "TranslateMessage", "DispatchMessageW")
DLLS = {"kernel32": None, "user32": None, "gdi32": None}

WM_CHAR = 0x0102
CTRL_S = 0x13

LIGNE_TAILLE = 77
TAMPON_SESSION = 384
VERDICTS = {0: "OK", -1: "FIN", -2: "ABSENT", -3: "HORS-BORNES",
            -4: "SESSION", -5: "ENTRÉE", -6: "SYSTÈME", -7: "VERROUILLÉ"}


def consigne(ligne):
    print(ligne)
    JOURNAL.append(ligne)


def verdict(rax):
    return VERDICTS.get(rax if rax >= -7 and rax <= 0 else rax,
                        f"{rax:#x}" if rax > 0 else str(rax))


def echec(nom, detail):
    consigne(f"ÉCHEC NOMMÉ [{nom}] : {detail}")
    conclure(1)


# --- LA SONDE DE L'ENTRÉE 205 : LA CASCADE DIAGNOSTIQUE ----------------------------
#
# Le terrain a refusé dev.1 (l'Entrée 204 : l'oubli du BASERELOC) PUIS dev.2
# du MÊME refus 0xc000007b — la table était NÉCESSAIRE mais PAS SUFFISANTE.
# L'autopsie de labo dit l'image conforme ; la preuve par la lignée isole
# les axes par lesquels dev.2 SORTAIT de l'enveloppe des HUIT artefacts
# passés au terrain (hello M0, selftest M1, echo M2, proxy M3/M4/M5/M8/M9) :
# LE TROU DE PAGE 0x3000-0x4000, LE BSS MASSIF .data VS 0x12000 ≫ RS 0x400,
# et le sous-système GUI (le seul que la vitrise exige de garder). LA
# SONDE reconstitue ces axes UN À UN sur des COPIES TEMPORAIRES (nées et
# mortes dans %TEMP% — loupe.exe n'est JAMAIS écrit) : le VRAI chargeur
# Windows NOMME l'axe fautif. Un échec nommé vaut plus qu'un vert muet.

def sonde_entree_205(k32, donnees):
    """-> la liste des consignes de la cascade. Chaque essai : une copie de
    l'image patchée d'un SEUL axe (puis la géométrie dev.2 entière),
    LoadLibraryEx DONT_RESOLVE, le verdict VERTE/REFUS + GetLastError +
    NTSTATUS — tout est effacé à la fin."""
    lignes = []
    e_lfanew = struct.unpack_from("<I", donnees, 0x3C)[0]
    opt = e_lfanew + 4 + 20                    # l'Optional Header
    sz_opt = struct.unpack_from("<H", donnees, opt - 4)[0]
    off_sec = opt + sz_opt                     # le tableau des sections
    ntdll = ctypes.WinDLL("ntdll")
    try:
        ntdll.RtlGetLastNtStatus.restype = ctypes.c_uint32
        statut_nt = lambda: ntdll.RtlGetLastNtStatus()
    except Exception:                          # jamais vu — la chute est douce
        statut_nt = lambda: 0

    def p(off, fmt, valeur):
        return off, struct.pack(fmt, valeur)

    essais = [
        ("P0 LA PIÈCE IDENTIQUE",
         "la copie INTACTE : le contrôle du mécanisme de la sonde",
         []),
        ("P1 LE TROU RECONSTITUÉ",
         ".rdata VS/RS 0x2000 → 0x1000 : le trou de page 0x3000-0x4000 "
         "de dev.2 revient",
         [p(off_sec + 40 + 8, "<I", 0x1000),
          p(off_sec + 40 + 16, "<I", 0x1000)]),
        ("P2 LE BSS RECONSTITUÉ",
         ".data RS 0x12000 → 0x400 : le BSS massif de dev.2 revient "
         "(VS ≫ RS)",
         [p(off_sec + 3 * 40 + 16, "<I", 0x400)]),
        ("P3 LE SOUS-SYSTÈME CUI",
         "Subsystem 2 (GUI) → 3 (CUI) — l'axe fenêtré, le seul que la "
         "vitrine exige de garder",
         [p(opt + 68, "<H", 3)]),
        ("P4 LA GÉOMÉTRIE dev.2 ENTIÈRE",
         "le trou + le BSS ENSEMBLE — la géométrie exacte refusée DEUX "
         "FOIS par le terrain",
         [p(off_sec + 40 + 8, "<I", 0x1000),
          p(off_sec + 40 + 16, "<I", 0x1000),
          p(off_sec + 3 * 40 + 16, "<I", 0x400)]),
    ]
    refus = []
    p0_refus = False
    dossier = tempfile.mkdtemp(prefix="loupe-sonde-205-")
    try:
        for nom, description, patchs in essais:
            image = bytearray(donnees)
            for off, octets in patchs:
                image[off:off + len(octets)] = octets
            chemin_sonde = os.path.join(dossier, "loupe-sonde.exe")
            with open(chemin_sonde, "wb") as f:
                f.write(bytes(image))
            k32.SetLastError(0)
            base = k32.LoadLibraryExW(chemin_sonde, None, 0x00000001)
            err = ctypes.get_last_error()
            etat = statut_nt()
            if base:
                lignes.append(f"[sonde] {nom} : cartographie VERTE @ "
                              f"{base:#x} — {description}")
            else:
                refus.append(nom)
                if nom.startswith("P0"):
                    p0_refus = True
                lignes.append(f"[sonde] {nom} : REFUS DU CHARGEUR — "
                              f"GetLastError {err}, NTSTATUS {etat:#010x} "
                              f"— {description}")
            os.remove(chemin_sonde)
    finally:
        try:
            os.rmdir(dossier)
        except OSError:
            pass
    if p0_refus:
        lignes.append("[sonde] LE VERDICT : la copie IDENTIQUE elle-même "
                      "est refusée — l'axe n'est PAS dans l'image (chemin, "
                      "antivirus, stratégie de la machine) : le témoin le "
                      "consigne, le labo recoupe")
    elif refus:
        lignes.append("[sonde] LE VERDICT DE LA SONDE : le VRAI chargeur "
                      "refuse " + " · ".join(refus) + " — L'AXE EST NOMMÉ "
                      "(les copies %TEMP% sont mortes, loupe.exe INTACT)")
    else:
        lignes.append("[sonde] LE VERDICT DE LA SONDE : AUCUN axe "
                      "reconstitué n'est refusé — le refus de dev.2 était "
                      "la COMBINAISON ou hors image : le témoin le "
                      "consigne, le labo recoupe")
    return lignes


def conclure(code):
    os.makedirs(PREUVES, exist_ok=True)
    chemin = os.path.join(PREUVES, "temoin-loupe.txt")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(JOURNAL) + "\n")
    print()
    print(f"[run] le journal du run : {chemin}")
    print("[run] LA VITRINE SE VIT PAR SON TÉMOIN : double-cliquez "
          "temoin-vitrine.bat — les deux fenêtres, Alt+F4 chacune, les "
          "codes capturés ; renvoyez preuves-loupe/ ENTIER au coffre")
    sys.exit(code)


def main():
    consigne(f"=== LE TERRAIN M10-(e) : LE RUN DE LOUPE (loupe.exe {VERSION_TXT}) ===")
    if platform.system() != "Windows":
        echec("ENVIRONNEMENT", "le run exige le VRAI Windows (kernel32/"
             "user32/gdi32) — c'est le grandeur nature")
    bits = struct.calcsize("P") * 8
    consigne(f"[env] {platform.system()} {platform.release()} · Python "
             f"{bits} bits · {platform.machine()}")

    # LE MODE D'ERREUR (l'Entrée 205) : les boîtes bloquantes du chargeur
    # (python.exe — Image incorrecte) sont COUPÉES — un refus est nommé PAR
    # LE TÉMOIN (GetLastError + NTSTATUS consignés), jamais muré derrière
    # un bouton OK : le run continue et la sonde diagnostique
    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    SEM = 0x0001 | 0x8000        # FAILCRITICALERRORS | NOOPENFILEERRORBOX
    global ANCIEN_MODE_DERREUR
    ANCIEN_MODE_DERREUR = k32.SetErrorMode(SEM)

    # --- T0 LE TÉMOIN : l'empreinte ASSERTÉE + les adresses scellées ----------
    consigne("[T0] LE TÉMOIN — l'artefact relu avant tout geste")
    chemin_exe = os.path.join(ICI, "loupe.exe")
    if not os.path.exists(chemin_exe):
        echec("ARTEFACT-ABSENT", "loupe.exe introuvable auprès du scénario")
    donnees = open(chemin_exe, "rb").read()
    sha = hashlib.sha256(donnees).hexdigest()
    if len(donnees) != TAILLE_EXE or sha != SHA_EXE:
        echec("EMPREINTE-DIVERGENTE",
              f"{len(donnees)} o, sha256 {sha} != l'asserté {SHA_EXE}")
    consigne(f"[T0] loupe.exe : {TAILLE_EXE} o, sha256 {sha[:16]}… — "
             f"L'EMPREINTE ASSERTÉE (l'empreinte prouve CES octets — "
             f"la carte, génération 13, à régénérer au labo)")

    k32.LoadLibraryExW.restype = ctypes.c_void_p
    k32.LoadLibraryExW.argtypes = [wt.LPCWSTR, ctypes.c_void_p, wt.DWORD]
    k32.VirtualProtect.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                   wt.DWORD, ctypes.POINTER(wt.DWORD)]
    DONT_RESOLVE = 0x00000001
    base = k32.LoadLibraryExW(chemin_exe, None, DONT_RESOLVE)
    if not base:
        # LA CASCADE DIAGNOSTIQUE D'ABORD (l'Entrée 205) : le kit porte
        # son bissecteur — les axes de dev.2 reconstitués UN À UN, le
        # VRAI chargeur nomme le fautif AVANT le refus du run
        consigne("[sonde] LA CARTOGRAPHIE DE dev.6 A ÉTÉ REFUSÉE — LA "
                 "CASCADE DIAGNOSTIQUE DE L'ENTRÉE 205 SE JOUE (les axes "
                 "reconstitués sur des copies %TEMP%, l'artefact intact)")
        for ligne in sonde_entree_205(k32, donnees):
            consigne(ligne)
        echec("CARTOGRAPHIE", f"LoadLibraryEx a rendu {base:#x} (GetLastError "
             f"{ctypes.get_last_error()}) — LA SONDE a nommé les axes "
             f"ci-dessus : le témoin part au coffre, le labo recoupe")
    consigne(f"[T0] l'image cartographiée DONT_RESOLVE @ {base:#x} — le "
             f"scénario est LE CHARGEUR, aucun point d'entrée exécuté")

    def lire(rva, n):
        tampon = ctypes.create_string_buffer(n)
        ctypes.memmove(tampon, base + rva, n)
        return tampon.raw

    # les adresses scellées CONSTATÉES (les ancres R7 dans l'image)
    for nom, rva, attendu in (("libc-01 memcpy M1", R_LIBC01, TETE_LIBC01),
                              ("libc-02 memcmp M1", R_LIBC02, TETE_LIBC02),
                              ("libc-07 memset M1", R_LIBC07, TETE_LIBC07),
                              ("win-03 la boucle démo", R_WIN03, TETE_WIN03),
                              ("tls13-01 sha256-init M9 (H0[0] posé)",
                               R_TLS01, TETE_TLS01)):
        if lire(rva, len(attendu)) != attendu:
            echec("SCELLÉ-DIVERGENT", f"{nom} @{rva:#x} : la tête scellée "
                 f"{attendu.hex()} introuvable — l'héritage a bougé ?")
    k_image = struct.unpack("<64I", lire(R_K, 256))
    if k_image[:4] != K_TETE or k_image[-4:] != K_QUEUE:
        echec("TABLE-K", "la table K[64] @0x2F00 != les constantes FIPS "
             "180-4 § 4.2.2 (la table du scellé M9)")
    if struct.unpack("<Q", lire(R_VERSION, 8))[0] != VERSION_R10:
        echec("PORTE-R10", f"le qword version @0x2E80 != {VERSION_R10:#x} "
             f"(loupe {VERSION_TXT})")
    # LE CADRE NÉ MIROIR DU CADRE_VIERGE (LA LEÇON DE L'ENTRÉE 206 : le
    # terrain a nommé [CADRE-NÉ] sur dev.3 — l'initialiseur du build avait
    # posé le sentinel à +8 [une TAILLE prise pour un offset] au lieu de
    # +528 [la chaîne des tailles] ; dev.4 fait de l'initialiseur LE
    # MIROIR EXACT du harnais — zéros partout SAUF la poignée INVALIDE
    # à +528, et les zones .data au-delà du cadre NÉES ZÉRO) : le .data
    # ENTIER relu contre LE MÊME miroir — la porte demeure pour toujours
    cadre_vierge = bytearray(DATA_VSIZE)
    struct.pack_into("<Q", cadre_vierge, CADRE_POIGNEE, INVALIDE)
    if lire(R_CADRE, DATA_VSIZE) != bytes(cadre_vierge):
        echec("CADRE-NÉ", "le CADRE .data n'est pas né LE MIROIR du harnais "
             "(zéros partout SAUF la poignée INVALIDE à +528 — "
             "l'initialiseur du build, la leçon de l'Entrée 206)")
    # LE BASERELOC MINIMAL DÉCLARÉ (la leçon de l'Entrée 204) : le répertoire
    # dirs[5] de l'image MAPPÉE — sans lui le VRAI chargeur refuse de reloger
    # l'image ASLR : 0xc000007b, LE REFUS NOMMÉ DU TERRAIN sur dev.1
    e_lfanew = struct.unpack("<I", lire(0x3C, 4))[0]
    reloc_rva, reloc_taille = struct.unpack(
        "<II", lire(e_lfanew + 24 + 112 + 40, 8))
    if reloc_rva != R_RELOC or reloc_taille != 12:
        echec("BASERELOC", f"le répertoire dirs[5] = ({reloc_rva:#x}, "
             f"{reloc_taille}) != ({R_RELOC:#x}, 12) — sans table, le VRAI "
             f"chargeur refuse de reloger l'image ASLR (0xc000007b, le refus "
             f"nommé du terrain sur dev.1 — l'Entrée 204)")

    # L'HABILLAGE D'IMPORT VÉRIFIÉ (la leçon D97 institutionnalisée —
    # l'Entrée 210 : le chargeur du terrain [Windows 11 build 26300]
    # résout les tables par le CHEMIN FirstThunk — il MARCHE chaque
    # plage jusqu'au premier slot NULL ; des plages CONTIGUËS font
    # déborder la marche de kernel32 chez les noms user32 :
    # RegisterClassExW résout à NULL, l'entrée APPELLE LE NUL — la
    # vitrine meurt 0xC0000005 SANS dialogue, AVANT l'entrée. La
    # quatrième manifestation de la dérive D54 ne passera PLUS ici.)
    imp_rva, imp_taille = struct.unpack(
        "<II", lire(e_lfanew + 24 + 112 + 8, 8))
    plages_attendues = ((R_IAT_K32, 10, "kernel32"),
                        (R_IAT_U32, 18, "user32"),
                        (R_IAT_GDI, 6, "gdi32"),
                        (R_IAT_DEMO, 3, "user32 (double entrée)"))
    desc, vus = imp_rva, 0
    while True:
        oft, tds, fwd, nom_rva, ft = struct.unpack("<IIIII", lire(desc, 20))
        if oft == 0 and ft == 0:
            break
        if vus >= 4:
            echec("D54-DESCLIER", f"un 5e descripteur inattendu @{desc:#x}")
            break
        rva_att, n_att, dll_att = plages_attendues[vus]
        if ft != rva_att:
            echec("D54-DESCLIER", f"le descripteur #{vus} ({dll_att}) lie "
                 f"FirstThunk @{ft:#x} != {rva_att:#x} (le plan)")
        n = 0
        while struct.unpack("<Q", lire(ft + 8*n, 8))[0] != 0:
            n += 1
            if n > 40:
                echec("D54-MARCHE", f"la plage @{ft:#x} marche au-delà de 40 "
                     f"feuilles — le séparateur NULL est ABSENT (la marche "
                     f"du terrain déborderait chez la voisine)")
                break
        if n != n_att:
            echec("D54-SÉPARATEUR", f"la plage @{ft:#x} du descripteur #{vus} "
                 f"({dll_att}) marche {n} feuilles != {n_att} — les plages "
                 f"CONTIGUËS (le chargeur 26300 y lirait les noms de "
                 f"l'AUTRE dll : la vitrine mourrait avant l'entrée, "
                 f"0xC0000005 sans dialogue — la leçon D97/210)")
        for i in range(n_att):
            if struct.unpack("<Q", lire(ft + 8*i, 8))[0] == 0:
                echec("D54-PRÉREMPLI", f"le slot @{ft + 8*i:#x} est VIDE "
                     f"dans le fichier — le chemin FirstThunk du terrain y "
                     f"lirait la fin de plage avant l'heure (D97)")
        vus += 1
        desc += 20
    if vus != 4:
        echec("D54-DESCLIER", f"{vus} descripteurs d'import != 4 (le plan)")
    for sep in IAT_SEPARATEURS:
        if struct.unpack("<Q", lire(sep, 8))[0] != 0:
            echec("D54-SÉPARATEUR", f"le séparateur @{sep:#x} != NULL — la "
                 f"plage précédente déborde (la marche du terrain)")
    consigne("[T0] l'habillage d'import VÉRIFIÉ : QUATRE plages FirstThunk "
             "marchées au compte exact [10 · 18 · 6 · 3], les séparateurs "
             "NULL en place, les slots PRÉREMLIS du fichier — le motif D54 "
             "ENTIER (la leçon D97 entre au scénario — l'Entrée 210)")

    consigne("[T0] les adresses scellées CONSTATÉES : la minilibc M1 "
             "@0x1100/0x1180/0x13C0 · la boucle démo @0x15C0 · la famille "
             "sha M9 @0xC000+ (H0[0] 0x6A09E667 posé par le scellé) · LA "
             f"TABLE K[64] @0x2F00 (FIPS) · le qword version {VERSION_R10:#010x} · "
             "le CADRE né LE MIROIR DU CADRE_VIERGE (la poignée INVALIDE "
             "@+528, le .data entier relu — l'Entrée 206) · LE BASERELOC "
             "minimal déclaré dirs[5] (0x2E90, 12 o — la leçon de l'Entrée "
             "204)")

    # le scénario-chargeur : LES 34 FEUILLES RÉSOLUES + posées aux slots du
    # plan (+ les TROIS de l'IAT démo scellée) — VirtualProtect le temps de
    # la pose (.rdata est lisible seule, le chargeur réel écrit à la liaison)
    ancien = wt.DWORD(0)
    zones = (R_IAT_K32, 0x148)          # les quatre plages contiguës à 0x3100
    k32.VirtualProtect(ctypes.c_void_p(base + zones[0]), zones[1], 0x40,
                       ctypes.byref(ancien))     # PAGE_READWRITE
    poses = 0
    for rva_iat, feuilles, dll in ((R_IAT_K32, IAT_KERNEL32, "kernel32"),
                                   (R_IAT_U32, IAT_USER32, "user32"),
                                   (R_IAT_GDI, IAT_GDI32, "gdi32")):
        d = ctypes.WinDLL(dll)
        DLLS[dll] = d
        for i, feuille in enumerate(feuilles):
            adresse = ctypes.cast(getattr(d, feuille), ctypes.c_void_p).value
            ctypes.memmove(base + rva_iat + 8 * i,
                           struct.pack("<Q", adresse), 8)
            poses += 1
    for i, feuille in enumerate(IAT_DEMO):       # la double entrée scellée
        adresse = ctypes.cast(getattr(DLLS["user32"], feuille),
                              ctypes.c_void_p).value
        ctypes.memmove(base + R_IAT_DEMO + 8 * i,
                       struct.pack("<Q", adresse), 8)
        poses += 1
    k32.VirtualProtect(ctypes.c_void_p(base + zones[0]), zones[1],
                       ancien.value, ctypes.byref(ancien))
    consigne(f"[T0] l'IAT RÉSOLUE par le scénario-chargeur : {poses} "
             f"feuilles posées aux slots du plan (kernel32 10 · user32 18 · "
             f"gdi32 6 · la double entrée démo 3 — VirtualProtect le temps "
             f"de la pose)")

    # les prototypes : les blocs appelés à leurs adresses scellées
    LOUPE01 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p)
    LOUPE02 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_uint64)
    LOUPE03 = ctypes.CFUNCTYPE(ctypes.c_int64)
    LOUPE07 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p)
    LOUPE08 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p,
                               ctypes.c_uint64, ctypes.c_void_p,
                               ctypes.c_uint64)
    LOUPE13 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p,
                               ctypes.c_uint64, ctypes.c_void_p,
                               ctypes.c_uint64, ctypes.c_uint64)
    LOUPE16 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p,
                               ctypes.c_uint64, ctypes.c_uint64,
                               ctypes.c_uint64)
    LOUPE17 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p,
                               ctypes.c_uint64, ctypes.c_uint64,
                               ctypes.c_uint64)

    ouvrir = LOUPE01(base + R_LOUPE01)
    lire_fenetre = LOUPE02(base + R_LOUPE02)
    fermer = LOUPE03(base + R_LOUPE03)
    cumul = LOUPE07(base + R_LOUPE07)
    ligne = LOUPE08(base + R_LOUPE08)
    recherche = LOUPE13(base + R_LOUPE13)
    saisie = LOUPE16(base + R_LOUPE16)
    sauver = LOUPE17(base + R_LOUPE17)

    def cadre_champ(off, n=8):
        return lire(R_CADRE + off, n)

    # --- T1 LA SESSION : loupe-01 sur L'OMBRE BYTE-À-BYTE DE LA PIÈCE -----------
    # (l'Entrée 208 : le scénario EST LE CHARGEUR — l'image cartographiée
    # TIENT loupe.exe ouvert SANS partage d'écriture, et le VRAI Windows
    # refuse gle 32 : loupe-01 l'a NOMMÉ -7 VERROUILLÉ, LE REFUS AU NOM
    # PRÈS — LA PIÈCE ACQUITÉE, le geste du kit corrigé : la session naît
    # sur temoin-session.bin, LA COPIE byte-à-byte née et morte au run —
    # même loi que la sonde 205 (les copies %TEMP%) et le témoin vitrine
    # (temoin-fichier.bin) ; l'empreinte de l'ombre ASSERTÉE avant le
    # geste — un kit fauté est un refus nommé AVANT tout geste)
    consigne("[T1] LA SESSION — loupe-01 à son adresse scellée 0x4080, "
             "sur L'OMBRE byte-à-byte de la pièce (temoin-session.bin)")
    chemin_session = os.path.join(ICI, "temoin-session.bin")
    with open(chemin_exe, "rb") as src, open(chemin_session, "wb") as dst:
        dst.write(src.read())            # la copie byte-à-byte de la pièce
    with open(chemin_session, "rb") as f:
        if hashlib.sha256(f.read()).hexdigest() != SHA_EXE:
            echec("SESSION-OMBRE", "temoin-session.bin != loupe.exe (la "
                 "copie fautive — refus nommé AVANT tout geste)")
    chemin_u16 = ctypes.create_unicode_buffer(chemin_session)
    r = ouvrir(ctypes.cast(chemin_u16, ctypes.c_void_p))
    if r != 0:
        echec("SESSION", f"loupe-01 a rendu {verdict(r)} (la copie "
             f"pourtant relu à l'instant)")
    taille_lue = struct.unpack("<Q", cadre_champ(CADRE_TAILLE))[0]
    poignee = struct.unpack("<Q", cadre_champ(CADRE_POIGNEE))[0]
    if taille_lue != TAILLE_EXE or poignee == INVALIDE or poignee == 0:
        echec("CADRE", f"le cadre relu : taille {taille_lue} != "
             f"{TAILLE_EXE}, poignée {poignee:#x} (la session n'est pas née)")
    consigne(f"[T1] la session NÉE : taille {taille_lue} o == l'asserté, la "
             f"poignée vivante {poignee:#x} — le VRAI CreateFileW par "
             f"l'IAT, sur l'ombre byte-à-byte de la pièce")

    # --- T2 LA DOUBLE LECTURE : le noyau empreintes ------------------------------
    consigne("[T2] LA DOUBLE LECTURE — loupe-02 puis loupe-07, les DEUX "
             "lecteurs indépendants")
    r = lire_fenetre(0)
    remplissage = struct.unpack("<I", cadre_champ(CADRE_REMPLISSAGE, 4))[0]
    tampon = cadre_champ(CADRE_TAMPON, TAMPON_SESSION)
    if r != 0 or remplissage != TAMPON_SESSION:
        echec("FENÊTRE", f"loupe-02(0) → {verdict(r)}, remplissage "
             f"{remplissage} != 384")
    if tampon != donnees[:TAMPON_SESSION]:
        echec("DOUBLE-LECTURE", "le tampon du cadre != les 384 premiers "
             "octets lus par Python (les DEUX lecteurs divergent)")
    consigne("[T2] la fenêtre 0 : le tampon du cadre == Python — les 384 "
             "octets IDENTIQUES")
    panneau = ctypes.create_string_buffer(48)
    r = cumul(ctypes.cast(panneau, ctypes.c_void_p))
    md5_app = panneau.raw[:16].hex()
    sha_app = panneau.raw[16:].hex()
    md5_py = hashlib.md5(donnees).hexdigest()
    sha_py = hashlib.sha256(donnees).hexdigest()
    if r != 0 or md5_app != md5_py or sha_app != sha_py:
        echec("PANNEAU", f"loupe-07 → {verdict(r)} ; md5 {md5_app} != "
             f"{md5_py} ou sha256 {sha_app} != {sha_py}")
    if sha_app != SHA_EXE:
        echec("LA-PIÈCE-JUGÉE", f"loupe-07 sur loupe.exe LUI-MÊME rend "
             f"sha256 {sha_app} != l'asserté {SHA_EXE} — l'application ne "
             f"rend pas l'empreinte de sa propre pièce")
    consigne(f"[T2] LE PANNEAU : md5 {md5_app[:12]}… · sha256 "
             f"{sha_app[:12]}… == hashlib — ET LA PIÈCE DE L'ÈRE JUGÉE PAR "
             f"SA PROPRE APPLICATION SUR SON OMBRE byte-à-byte (sha256 == "
             f"l'asserté {SHA_EXE[:12]}…)")
    r = fermer()
    if r != 0:
        echec("CLÔTURE-PRÉALABLE", f"loupe-03 → {verdict(r)}")
    if struct.unpack("<Q", cadre_champ(CADRE_POIGNEE))[0] != INVALIDE:
        echec("CLÔTURE-PRÉALABLE", "la poignée n'est pas INVALIDE après fermeture")

    # --- T3 LES LIGNES : loupe-08, le format exact --------------------------------
    consigne("[T3] LES LIGNES — loupe-08 à son adresse scellée 0x49C0")

    def attendue(decalage, octets):
        s = f"{decalage:08X}  "
        groupes = [f"{b:02X}" if i < len(octets) else "  " for i, b in
                    enumerate(octets + b"\x00" * (16 - len(octets)))]
        s += " ".join(groupes[:8]) + "  " + " ".join(groupes[8:]) + "  "
        miroir = "".join(chr(b) if 0x20 <= b <= 0x7E else "."
                          for b in octets[:16])
        s += miroir + " " * (16 - len(miroir))
        return s.encode("latin-1") + b"\x00"

    sortie = ctypes.create_string_buffer(96)
    r = ligne(ctypes.cast(ctypes.create_string_buffer(donnees[:16]),
                          ctypes.c_void_p), 16,
              ctypes.cast(sortie, ctypes.c_void_p), 0)
    attendu = attendue(0, donnees[:16])
    if r != 0 or sortie.raw[:LIGNE_TAILLE] != attendu:
        echec("LIGNE", f"loupe-08 → {verdict(r)} ; rendu "
             f"{sortie.raw[:40]!r} != {attendu[:40]!r}")
    consigne(f"[T3] la ligne 0 : « {sortie.raw[:LIGNE_TAILLE-1].decode('ascii')} »"
             f" == le format composé en Python pur")
    fin = donnees[-7:]                       # la ligne finale INCOMPLÈTE
    r = ligne(ctypes.cast(ctypes.create_string_buffer(fin), ctypes.c_void_p),
              len(fin), ctypes.cast(sortie, ctypes.c_void_p),
              (TAILLE_EXE - len(fin)) & ~0xF)
    attendu = attendue((TAILLE_EXE - len(fin)) & ~0xF, fin)
    if r != 0 or sortie.raw[:LIGNE_TAILLE] != attendu:
        echec("LIGNE-FINALE", f"la ligne finale incomplète : "
             f"{sortie.raw[:LIGNE_TAILLE]!r} != {attendu!r} (l'alignement "
             f"des colonnes est un invariant)")
    consigne("[T3] la ligne finale incomplète garde LE FORMAT — les groupes "
             "absents sont deux espaces, le miroir absent un point")

    # --- T4 LA RECHERCHE : loupe-13, le memcmp scellé à l'œuvre ------------------
    consigne("[T4] LA RECHERCHE — loupe-13 à son adresse scellée 0x5740")
    motif = donnees[0x2000:0x2008]           # un motif VRAI de l'image
    fenetre = ctypes.create_string_buffer(donnees[0x1000:0x9000])
    r = recherche(ctypes.cast(fenetre, ctypes.c_void_p), len(fenetre.raw),
                  ctypes.cast(ctypes.create_string_buffer(motif),
                              ctypes.c_void_p), len(motif), 0)
    attendu_i = donnees[0x1000:0x9000].find(motif)
    if r != attendu_i:
        echec("RECHERCHE", f"loupe-13 → {verdict(r) if r < 0 else r} != "
             f"bytes.find {attendu_i} (le memcmp SCELLÉ M1 à l'œuvre)")
    consigne(f"[T4] le motif trouvé à {r} == bytes.find — l'algorithme pur "
             f"sur les octets vrais")

    # --- T5 L'ÉDITION : la boucle entière sur une copie ---------------------------
    consigne("[T5] L'ÉDITION — la boucle entière : ouvrir, saisir « 4d », "
             "sauver (Ctrl+S), vérifier, fermer")
    chemin_copie = os.path.join(ICI, "temoin-edition.bin")
    original = bytes(range(256)) * 4         # 1 024 octets, le contenu connu
    with open(chemin_copie, "wb") as f:
        f.write(original)
    chemin_u16 = ctypes.create_unicode_buffer(chemin_copie)
    r = ouvrir(ctypes.cast(chemin_u16, ctypes.c_void_p))
    if r != 0:
        echec("ÉDITION-SESSION", f"loupe-01 sur la copie → {verdict(r)}")
    r = lire_fenetre(0)
    if r != 0:
        echec("ÉDITION-FENÊTRE", f"loupe-02 → {verdict(r)}")
    hwnd = ctypes.c_void_p(0x5150)           # un hwnd factice du kit
    saisie(hwnd, WM_CHAR, ord("4"), 0)       # le premier chiffre ATTEND
    saisie(hwnd, WM_CHAR, ord("d"), 0)       # le second ENGAGE (0x4d)
    if struct.unpack("<I", cadre_champ(CADRE_SALE, 4))[0] == 0:
        echec("MARQUE-SALE", "la marque sale n'est pas posée par la saisie")
    r = sauver(hwnd, WM_CHAR, CTRL_S, 0)
    if r != 0:
        echec("SAUVEGARDE", f"loupe-17 → {verdict(r) if r <= 0 else r} "
             f"(0 = OK attendu — le compte des octets part à la barre "
             f"d'état, l'Entrée 209)")
    relu = open(chemin_copie, "rb").read()
    attendu_f = bytearray(original)
    attendu_f[0] = 0x4D
    if relu != bytes(attendu_f):
        echec("ÉCRIT-À-L'OCTET", "le fichier après sauvegarde != l'original "
             "mûté du SEUL octet 0 (0x00 → 0x4D) — l'unité est l'octet")
    if struct.unpack("<I", cadre_champ(CADRE_SALE, 4))[0] != 0:
        echec("MARQUE-LEVÉE", "la marque sale demeure après la sauvegarde")
    r = fermer()
    if r != 0:
        echec("ÉDITION-CLÔTURE", f"loupe-03 → {verdict(r)}")
    os.remove(chemin_copie)
    consigne("[T5] la boucle ENTIÈRE : l'octet 0 mûté 0x00 → 0x4D SEUL, la "
             "taille CONSTANTE, la marque levée, la session close — "
             "l'écriture À L'OCTET par le VRAI WriteFile")

    # --- T6 LES REJETS : l'échec nommé --------------------------------------------
    consigne("[T6] LES REJETS — l'échec NOMMÉ (un refus vaut plus qu'un "
             "vert muet)")
    absent = ctypes.create_unicode_buffer(
        os.path.join(ICI, "ce-fichier-nexiste-pas.bin"))
    r = ouvrir(ctypes.cast(absent, ctypes.c_void_p))
    if r != -2:
        echec("REJET-ABSENT", f"le chemin qui ne désigne rien → "
             f"{verdict(r)} != -2 ABSENT")
    consigne("[T6] le chemin qui ne désigne rien → -2 ABSENT")
    # (l'Entrée 208 — LE FRÈRE DU DÉFAUT T1 chassé par la classe : offrir
    # loupe.exe LUI-MÊME eût rendu le même -7 VERROUILLÉ — le chargeur
    # tient la pièce ; l'offrande est L'OMBRE, rouvrable, déjà prouvée)
    chemin_u16 = ctypes.create_unicode_buffer(chemin_session)
    r = ouvrir(ctypes.cast(chemin_u16, ctypes.c_void_p))
    if r != 0:
        echec("REJET-SESSION-OFFRANTE", f"loupe-01 sur l'ombre → "
             f"{verdict(r)} (la session double exige une première née)")
    r = ouvrir(ctypes.cast(chemin_u16, ctypes.c_void_p))
    if r != -5:
        echec("REJET-SESSION-DOUBLE", f"la session double → {verdict(r)} "
             f"!= -5 (un fichier à la fois, le périmètre 0.1.0)")
    consigne("[T6] la session double → -5 ENTRÉE (un fichier à la fois, "
             "l'offrande est l'ombre de la pièce — jamais la pièce scellée)")
    r = lire_fenetre(0x7FFFFFF0)
    if r != -3:
        echec("REJET-HORS-BORNES", f"le décalage hors bornes → {verdict(r)} "
             f"!= -3 HORS-BORNES")
    consigne("[T6] le décalage hors bornes → -3 HORS-BORNES (la borne nommée)")
    introuvable = ctypes.create_string_buffer(b"\xDE\xAD\xBE\xEF" * 4)
    r = recherche(ctypes.cast(fenetre, ctypes.c_void_p), len(fenetre.raw),
                  ctypes.cast(introuvable, ctypes.c_void_p), 16, 0)
    if r != -1:
        echec("REJET-FIN", f"le motif absent → {verdict(r)} != -1 FIN")
    consigne("[T6] le motif absent → -1 FIN (la fin nommée)")
    r = fermer()
    if r != 0:
        echec("REJET-CLÔTURE", f"loupe-03 final → {verdict(r)}")
    os.remove(chemin_session)           # l'ombre meurt, la pièce demeure
    consigne("[T6] l'ombre temoin-session.bin MORTE — la pièce loupe.exe "
             "demeure INTACTE, jamais offerte en écriture au run")

    # --- T7 LA CLÔTURE : l'artefact inchangé ---------------------------------------
    consigne("[T7] LA CLÔTURE — l'artefact relu inchangé")
    relu = open(chemin_exe, "rb").read()
    if relu != donnees:
        echec("ARTEFACT-TOUCHÉ", "loupe.exe a changé pendant le run — le "
             "run ne touche pas la pièce")
    consigne("[T7] loupe.exe relu INCHANGÉ (sha256 identique — le run ne "
             "touche pas la pièce)")

    # --- S0 LA SONDE DE L'ENTRÉE 205 : la cascade diagnostic ---------------------
    consigne("[S0] LA SONDE DE L'ENTRÉE 205 — les axes de dev.2 "
             "reconstitués UN À UN sur des copies %TEMP% (l'artefact "
             "n'est JAMAIS écrit, tout est effacé) : le VRAI chargeur "
             "NOMME l'axe du refus passé — la leçon consignée au témoin")
    for ligne in sonde_entree_205(k32, donnees):
        consigne(ligne)

    consigne("=== LE RUN DE LOUPE : VERT SUR PIÈCES — l'application née "
             "de TRIADE a vécu chez son utilisateur : la session, le "
             "panneau, les lignes, la recherche, l'édition à l'octet, les "
             "rejets nommés ===")
    consigne("[suite] LA VITRINE SE VIT PAR SON TÉMOIN : double-cliquez "
             "temoin-vitrine.bat — LA PREMIÈRE fenêtre (sans fichier), "
             "Alt+F4 ; LA SECONDE (avec temoin-fichier.bin), Alt+F4 — les "
             "DEUX codes de sortie capturés au témoin, la mort éventuelle "
             "NOMMÉE (l'Entrée 208 : la vitrine a vécu SANS témoin, "
             "jamais plus) ; le témoin part au coffre AVEC le présent, "
             "QUEL QUE SOIT le verdict ; les captures éventuelles de la "
             "vitrine vont au réceptacle preuves-loupe/")
    conclure(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # un échec est NOMMÉ, jamais une trace muette
        echec("EXCEPTION", repr(exc))
