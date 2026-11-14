#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compose_prompt_source_c.py — assemble le prompt de la phase source-c de
la campagne (l'unité 1, loupe-01 × bras C) : le contrat VERROUILLÉ + les
notes d'auteur (phase spec) + l'oracle (phase oracle) + LE JUGE EXACT DU
KIT (le code des vecteurs, la seule autorité observable) + LES FAITS DU
MÉCANISME (DONT_RESOLVE, les six feuilles, la table d'exports, la
discipline CRT). JAMAIS la notation scellée — la pièce mesurée naît de
cet appel seul."""
import pathlib

UNITE = pathlib.Path(__file__).resolve().parent
CONTRAT = pathlib.Path(UNITE).parent.parent.parent / "loupe" / "I" / "loupe-01-ouvrir.md"

entete = """Tu es le même auteur du domaine Loupe au laboratoire TRIADE — le bras C de
la campagne D204 (le flux CONVENTIONNEL, C + gcc). Tu as déjà lu le contrat
(tes notes de lecture et ton oracle suivent). Écris maintenant LE SOURCE C
du bloc loupe-01 · ouvrir : la pièce de campagne du bras C, compilée
gcc -O2. Le flux standard, tel qu'il se pratique — le même contrat, le
même mécanisme de kit terrain, aucune exigence de couverture imposée par
le plan : TON code, TA discipline d'ingénieur C, contre le juge.

================================================================================
LE CONTRAT (loupe/I/loupe-01-ouvrir.md, révision 3 — VERROUILLÉ)
================================================================================

"""

faits = """
================================================================================
LE MÉCANISME DE KIT TERRAIN (le même aux DEUX bras, CA2) — LES FAITS
================================================================================
- la pièce : UNE DLL PE32+ x86-64, compilée « gcc -O2 -shared -o
  loupe-01-c.dll loupe-01-c.c loupe-01-c.def » — le source ET le .def sont
  la livraison (le binaire naîtra d'eux) ;
- au terrain, la DLL est chargée par LoadLibraryEx DONT_RESOLVE : AUCUN
  import résolu, AUCUN point d'entrée exécuté — LE CRT N'EST JAMAIS
  INITIALISÉ : ton code ne peut appeler AUCUNE fonction de la CRT (pas de
  memset, memcpy, strlen, malloc, printf…) — seules les feuilles kernel32
  que tu déclares seront résolues PAR LE SCÉNARIO dans TA table d'imports
  RÉELLE : CreateFileW, GetFileSizeEx, SetFilePointerEx, ReadFile,
  CloseHandle, GetLastError (les six du kit — appelle celles dont ton
  geste a besoin) ;
- ATTENTION au piège du compilateur : sous -O2, gcc peut transformer
  certaines boucles d'initialisation en appels memset et certaines copies
  en appels memcpy (CRT jamais résolue : le run cracherait). Écris les
  boucles de sorte qu'aucune ne soit reconnue comme un memset/memcpy
  candidat (traite des mots de 8 octets par index, ou des octets un à un,
  avec des bornes que le compilateur ne peut pas réduire à un simple
  remplissage constant) — le labo AUDITERA le désassemblage : un seul
  appel CRT dans tes fonctions, l'épreuve le nommera ;
- le scénario découvre tes adresses PAR TA TABLE D'EXPORTS (le .def) :
    loupe_01_ouvrir   la fonction d'ouverture (l'ABI : un argument
                      pointeur, retour long long — le C le porte) ;
    loupe_03_fermer   la clôture de session (aucun argument, retour
                      long long) : la poignée refermée si une session
                      vit, l'état rouvert pour l'appel suivant — le juge
                      l'appelle ENTRE les vecteurs ;
    cadre             DONNÉE exportée, 960 octets — LE CADRE DU PLAN à
                      plat : chemin (+0, 520 o, UTF-16 NUL-terminé),
                      taille (+520, 8 o), poignée (+528, 8 o), vue (+536,
                      8 o), curseur (+544, 8 o), remplissage (+552, 4 o),
                      charge (+556, 4 o), tampon (+568, 384 o), marge
                      (+952, 8 o) — ACCÈDE AUX CHAMPS PAR OFFSETS SUR LE
                      TABLEAU D'OCTETS (jamais une structure C : le
                      rembourrage tuerait la disposition du plan) ;
    panneau           DONNÉE exportée, 48 octets — md5 (16 o) puis
                      sha256 (32 o) du fichier ENTIER ;
- l'état de session : des initialisations STATIQUES (.data/.bss) — la
  poignée de session vit dans une statique initialisée à INVALID
  ((HANDLE)-1 ou l'équivalent entier), AUCUN code d'initialisation ne
  court jamais ;
- LA SESSION DEMEURE OUVERTE après un loupe_01_ouvrir réussi (la poignée
  vit au cadre +528, la statique la retient) : c'est loupe_03_fermer qui
  referme — le juge éprouve la session double (E4) APRÈS un succès, et
  l'ancien cadre doit être INTACT octet par octet ;
- les refus : JAMAIS une poignée pendante — Q2 (la borne) referme AVANT
  le retour -3 ; les refus de CreateFileW n'ont rien à refermer ;
- le panneau : implémente MD5 et SHA-256 EN C PUR (aucune bibliothèque,
  les implémentations du domaine public sont ton reflexe de flux — écris
  les deux, correctes aux frontières du rembourrage : 55, 56, 63, 64, 65,
  119, 120 octets… ; le juge confronte aux hashlib du fichier ENTIER, LE
  VIDE AUSSI) ;
- la lecture : ton choix d'ingénieur (un passage nourrissant la fenêtre
  et les deux empreintes, ou les lectures séparées) — le coût nommé dans
  le LISEZMOI du kit le dira.

================================================================================
LE JUGE EXACT DU KIT (le code des vecteurs du scénario — LA SEULE
AUTORITÉ OBSERVABLE ; chaque contrôle qui jouera contre ta pièce) :
================================================================================
"""

juge = '''
    # les constantes du plan (loupe/layout.py) — le juge lit TA pièce
    # par TA table d'exports, aux offsets du plan :
    TAILLE, POIGNEE = 520, 528
    VUE, CURSEUR, REMPL, TAMPON = 536, 544, 552, 568

    def appeler_ouvrir(tampon: bytes) -> int:
        zone = ctypes.create_string_buffer(bytes(tampon), len(tampon) + 8)
        r = LOUPE01(ctypes.cast(zone, ctypes.c_void_p))
        return verdict(r)          # le bas 32 bits, signé

    # ---- V1 : LES TÉMOINS DU KIT ------------------------------------------
    for nom in ("temoin-1.bin", "temoin-384.bin", "temoin-3f.bin", "vide.bin"):
        donnees = open(os.path.join(ICI, nom), "rb").read()
        r = appeler_ouvrir(nom.encode("utf-16-le") + b"\\x00\\x00")
        rempl = min(384, len(donnees))
        attendus = (r == 0 and cadre_chemin() == nom
                    and cadre_qword(TAILLE) == len(donnees)
                    and cadre_qword(VUE) == 0 and cadre_qword(CURSEUR) == 0
                    and cadre_dword(REMPL) == rempl
                    and cadre_champ(TAMPON, rempl) == donnees[:rempl])
        controle(f"V1:{nom}-la-session-nee-entiere", attendus, ...)
        modele = hashlib.md5(donnees).digest() + hashlib.sha256(donnees).digest()
        controle(f"V1:{nom}-le-panneau-ne", panneau() == modele, ...)
        LOUPE03()

    # ---- V2 : LES REJETS D'OS ----------------------------------------------
    r = appeler_ouvrir("absent-du-terrain.bin".encode("utf-16-le")
                       + b"\\x00\\x00")
    controle("V2:E1-absent", r == -2, ...)     # attendu -2 ABSENT
    # le verrouillé : le scénario TIENT le fichier sans partage
    # (CreateFileW(..., 0x80000000, 0, None, 3, 0, None) — dwShareMode 0)
    tenue = k32.CreateFileW(os.path.join(ICI, "temoin-1.bin"), 0x80000000,
                            0, None, 3, 0, None)
    r = appeler_ouvrir("temoin-1.bin".encode("utf-16-le") + b"\\x00\\x00")
    controle("V2:E2-verrouille", r == -7, ...)  # attendu -7 VERROUILLÉ
    # (puis le scénario relâche sa tenue)
    controle("V2:E3-acces-refuse-NOMMÉ-ABSENT", True, ...)  # jamais éprouvé

    # ---- V3 : LES BORNES ----------------------------------------------------
    # la taille 2 Gio + 1 : un fichier RÉEL posé épars à cette taille
    # (SetFilePointerEx à 0x80000001, SetEndOfFile — le disque n'écrit rien)
    r = appeler_ouvrir("geant-plus.bin".encode("utf-16-le") + b"\\x00\\x00")
    controle("V3:Q2-la-borne-2-Gio", r == -3, ...)   # attendu -3
    # la session double : l'ancien cadre INTACT
    appeler_ouvrir("temoin-384.bin".encode("utf-16-le") + b"\\x00\\x00")
    avant_cadre = cadre_champ(0, 960)
    avant_panneau = panneau()
    r = appeler_ouvrir("temoin-1.bin".encode("utf-16-le") + b"\\x00\\x00")
    controle("V3:E4-la-session-double",
             r == -5 and cadre_champ(0, 960) == avant_cadre
             and panneau() == avant_panneau, ...)
    LOUPE03()
    # le chemin de 260 caractères SANS NUL (le tampon du juge porte le
    # NUL à l'octet 520 — ta fonction voit 260 caractères) : le système
    # refuse lui-même le chemin trop long
    avant_chemin = cadre_champ(0, 8)
    r = appeler_ouvrir(b"A" * 520)          # 260 caractères, AUCUN NUL
    controle("V3:P1-le-chemin-trop-long", r in (-2, -5, -6),
             f"rax={r} — un REFUS NOMMÉ ... RIEN au cadre : "
             f"{cadre_champ(0, 8) == avant_chemin}")

REMARQUES DU LABO SUR CE JUGE (les conséquences pour ton source) :
- cadre_chemin() décode le cadre +0 en UTF-16 jusqu'au premier NUL : le
  chemin copié doit être L'ENTRÉE MÊME (le nom relatif du témoin, pas un
  chemin résolu) ;
- E4 : le second appel rend -5 AVANT TOUT GESTE (la statique de session
  d'abord) et ne touche NI le cadre NI le panneau NI le système ;
- P1 : sur ton refus, RIEN n'est écrit au cadre (les 8 premiers octets
  relus identiques) ;
- le juge appelle loupe_03_fermer() après CHAQUE témoin de V1 et après
  E4 — la session doit alors se rouvrir proprement pour l'appel suivant.

'''

notes_spec = """
================================================================================
TES NOTES DE LECTURE (la phase spec — ton document de travail)
================================================================================

"""

notes_oracle = """
================================================================================
TON ORACLE (la phase oracle — l'attendu du juge, vecteur par vecteur)
================================================================================

"""

travail = """
================================================================================
TON TRAVAIL (la phase source-c du workflow, bras C)
================================================================================
Écris LES DEUX FICHIERS de la livraison — le source C et le fichier de
définition des exports — réponds UNIQUEMENT par leur contenu, délimité
exactement ainsi (aucun texte avant, aucun texte après) :

###FICHIER loupe-01-c.c
(le source C complet — il compile seul contre les en-têtes Windows,
AUCUNE inclusion au-delà de <windows.h> ; les commentaires en français
portent le contrat aux endroits qui l'honorent)
###FIN loupe-01-c.c
###FICHIER loupe-01-c.def
(LIBRARY loupe-01-c ; EXPORTS : loupe_01_ouvrir, loupe_03_fermer,
cadre DATA, panneau DATA)
###FIN loupe-01-c.def
"""

contrat = CONTRAT.read_text(encoding="utf-8")
spec = (UNITE / "spec-lue-c.txt").read_text(encoding="utf-8")
oracle = (UNITE / "oracle-depuis-I-c.txt").read_text(encoding="utf-8")

prompt = (entete + contrat + faits + juge + notes_spec + spec
          + notes_oracle + oracle + travail)
(UNITE / "prompts" / "source-c.txt").write_text(prompt, encoding="utf-8")
print(f"[composé] prompts/source-c.txt : {len(prompt.encode())} o "
      f"(contrat {len(contrat)}, spec {len(spec)}, oracle {len(oracle)})")
