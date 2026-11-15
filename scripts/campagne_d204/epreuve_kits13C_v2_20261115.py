#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""epreuve_kits13C_v2_20261115.py — L'ÉPREUVE DU KIT 13 C v2 : LE TEXTE
LIVRÉ, PLOMBERIE COMPRISE, LA FEUILLE EN PLUS (la leçon de la 304 : la
plomberie de la LIAISON voyage au terrain — l'épreuve la tient au fichier
livré, pas au harnais du labo qui shimmait memcmp sans que le shim
voyage).

Le kit v2 (la faute nommée à la 304) : le v1 appelait la pièce sans lier
la feuille memcmp — le premier appel sautait à la valeur SUR DISQUE du
slot IAT (0x92da, l'entrée hint/nom) : access violation, le run tombé
code 1 au premier candidat de l'école. L'épreuve du v2 :

  · py_compile du scénario v2 livré ;
  · LA FEUILLE : epreuve_feuille_memcmp.py contre le v1 (ROUGE, la faute
    nommée — l'épreuve qui aurait arrêté la faute AVANT le terrain) et
    contre le v2 livré (VERT aux trois lois) ;
  · LE BLOC DÉCOUVERTE + LE BLOC IMPORTS du v2 : le texte livré VERBATIM
    contre la pièce réelle mappée par sections — l'export unique
    loupe_13_recherche @+0x1380 ET le slot memcmp @+0x91a0, sa valeur
    sur disque 0x92da == LE JUGE INDÉPENDANT (les tables lues du fichier
    brut) — le guichet découvre, le juge confirme ;
  · LES BLOCS V1/V2/V3/V4 du v2 : le texte livré VERBATIM contre la
    pièce réelle (le trampoline SysV→msx64 à cinq arguments — le harnas
    sert la feuille par son shim, l'équivalent labo du guichet livré :
    la liaison Windows ne court pas au labo, les vecteurs si) ;
  · LA PIÈCE INTACTE : la dll du kit v2 == la gravure v1 (08610a18… —
    la faute était au kit, jamais à la pièce).
"""
import ast
import ctypes
import os
import pathlib
import pefile
import py_compile
import struct
import subprocess
import sys
import tempfile

from keystone import Ks, KS_ARCH_X86, KS_MODE_64

UNITE_C = pathlib.Path("/home/z/my-project/projet-triade/github-mirror/"
                       "scripts/campagne_d204/unite-13-C")
KIT_V1 = pathlib.Path("/home/z/my-project/projet-triade/"
                      "kit-unite-loupe-13-C-20261115-recu")
PIECE_C = UNITE_C / "source" / "loupe-13-c.dll"
SCENARIO_V2 = UNITE_C / "kit-v2" / "scenario-unite13C.py"

REUSSITES, ECARTS = [], []


def controle(nom, ok, detail=""):
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom}" + (f" — {detail}" if detail else ""))
    (REUSSITES if ok else ECARTS).append(nom)


def extraire(texte, debut, fin):
    i = texte.index(debut)
    j = texte.index(fin, i)
    return texte[i:j]


def dedent4(bloc):
    """L'indentation de la fonction ôtée d'un étage — JAMAIS le code
    touché (le bloc livré vit au corps de lier_feuille_memcmp, l'épreuve
    l'exécute au corps de sa fonction d'essai)."""
    lignes = []
    for ligne in bloc.splitlines():
        lignes.append(ligne[4:] if ligne.startswith("        ")
                      else (ligne[4:] if ligne.startswith("    ")
                            else ligne))
    return "\n".join(lignes)


def executer_bloc(bloc, ns):
    code = ("def _bloc():\n" + bloc.rstrip()
            + "\n    return {n: v for n, v in list(locals().items())"
              " if not n.startswith('_')}\n")
    exec(compile(code, "<bloc-livré>", "exec"), ns)
    return ns["_bloc"]()


# ---- 0. py_compile du scénario v2 livré ------------------------------------
py_compile.compile(str(SCENARIO_V2), doraise=True)
print("[VERT] py_compile du scénario 13 C v2 livré")

# ---- 1. LA PIÈCE RÉELLE : mappée par sections (le chargeur du labo) --------
pe = pefile.PE(str(PIECE_C))
base = pe.OPTIONAL_HEADER.ImageBase
taille = pe.OPTIONAL_HEADER.SizeOfImage
brut = PIECE_C.read_bytes()
libc = ctypes.CDLL("libc.so.6", use_errno=True)
libc.mmap.restype = ctypes.c_void_p
libc.mmap.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int,
                      ctypes.c_int, ctypes.c_int, ctypes.c_long]
libc.mmap(ctypes.c_void_p(base), ctypes.c_size_t(taille), 7, 0x32, -1, 0)
ctypes.memmove(base, brut[:pe.OPTIONAL_HEADER.SizeOfHeaders],
               pe.OPTIONAL_HEADER.SizeOfHeaders)
for s in pe.sections:
    donnees = s.get_data()
    if donnees:
        ctypes.memmove(base + s.VirtualAddress, donnees, len(donnees))
print(f"[mappage] loupe-13-c.dll : {len(pe.sections)} sections, l'image "
      f"{taille:#x} o @ {base:#x} (la base préférée — le geste de "
      f"LoadLibraryEx rejoué)")

# ---- 2. LE JUGE INDÉPENDANT : les tables lues du FICHIER BRUT --------------
e_lfanew = struct.unpack_from("<I", brut, 0x3C)[0]
n_sections = struct.unpack_from("<H", brut, e_lfanew + 6)[0]
taille_opt = struct.unpack_from("<H", brut, e_lfanew + 20)[0]
opt = e_lfanew + 4 + 20


def rva_vers_brut(rva):
    for i in range(n_sections):
        s = opt + taille_opt + 40 * i
        vtaille, vaddr, rtaille, raddr = struct.unpack_from("<IIII", brut, s + 8)
        if vaddr <= rva < vaddr + max(vtaille, rtaille):
            return raddr + (rva - vaddr)
    raise ValueError(f"rva {rva:#x} hors sections")


rva_exp = struct.unpack_from("<I", brut, opt + 112)[0]
nb_noms_j = struct.unpack_from("<I", brut, rva_vers_brut(rva_exp + 24))[0]
tab_f_j = struct.unpack_from("<I", brut, rva_vers_brut(rva_exp + 28))[0]
tab_n_j = struct.unpack_from("<I", brut, rva_vers_brut(rva_exp + 32))[0]
tab_o_j = struct.unpack_from("<I", brut, rva_vers_brut(rva_exp + 36))[0]
juge = {}
for i in range(nb_noms_j):
    nrva = struct.unpack_from("<I", brut, rva_vers_brut(tab_n_j + 4 * i))[0]
    fin = brut.index(b"\x00", rva_vers_brut(nrva))
    nom = brut[rva_vers_brut(nrva):fin].decode("ascii")
    ordinal = struct.unpack_from("<H", brut, rva_vers_brut(tab_o_j + 2 * i))[0]
    juge[nom] = struct.unpack_from("<I", brut, rva_vers_brut(tab_f_j + 4 * ordinal))[0]
assert set(juge) == {"loupe_13_recherche"}, juge

# le juge des imports : le slot memcmp (sa RVA + sa valeur sur disque) lus
# du fichier brut, par la table d'imports même
rva_imp = struct.unpack_from("<I", brut, opt + 120)[0]
juge_slot, juge_valeur = None, None
num = 0
while True:
    ilt, _, _, rva_dll, iat = struct.unpack_from(
        "<IIIII", brut, rva_vers_brut(rva_imp + 20 * num))
    if ilt == 0 and iat == 0:
        break
    fin = brut.index(b"\x00", rva_vers_brut(rva_dll))
    if brut[rva_vers_brut(rva_dll):fin].decode("ascii").lower() == "msvcrt.dll":
        k = 0
        while True:
            entree = struct.unpack_from("<Q", brut, rva_vers_brut(ilt + 8 * k))[0]
            if entree == 0:
                break
            if not entree & (1 << 63):
                fin_n = brut.index(b"\x00", rva_vers_brut(entree) + 2)
                if brut[rva_vers_brut(entree) + 2:fin_n].decode("ascii") == "memcmp":
                    juge_slot = iat + 8 * k
                    juge_valeur = struct.unpack_from(
                        "<Q", brut, rva_vers_brut(iat + 8 * k))[0]
            k += 1
    num += 1
assert juge_slot is not None, "le slot memcmp introuvable au juge"
print(f"[juge indépendant] l'export unique loupe_13_recherche @"
      f"+{juge['loupe_13_recherche']:#x} ; le slot memcmp @+{juge_slot:#x}, "
      f"sa valeur sur disque {juge_valeur:#x} (l'entrée hint/nom — "
      f"l'ADRESSE NUE du crash v1)")

# ---- 3. LA FEUILLE : l'épreuve des trois lois contre le v1 ET le v2 ---------
r1 = subprocess.run([sys.executable, str(UNITE_C / "epreuve_feuille_memcmp.py"),
                     str(KIT_V1 / "scenario-unite13C.py")],
                    capture_output=True, text=True, timeout=120)
controle("la-feuille:le-v1-ROUGE-nomme", r1.returncode == 1
         and "L'ÉPREUVE FINIE : ROUGE" in r1.stdout
         and "0x92da" in r1.stdout,
         "les trois lois ROUGES contre le v1 — la faute nommée : le saut à "
         "l'adresse nue 0x92da, L'ADRESSE EXACTE du crash terrain — "
         "L'ÉPREUVE QUI AURAIT ARRÊTÉ LA FAUTE AVANT LE TERRAIN")
r2 = subprocess.run([sys.executable, str(UNITE_C / "epreuve_feuille_memcmp.py"),
                     str(SCENARIO_V2)],
                    capture_output=True, text=True, timeout=120)
controle("la-feuille:le-v2-VERT", r2.returncode == 0
         and "L'ÉPREUVE FINIE : VERT" in r2.stdout,
         "les trois lois VERTES contre le v2 livré (la découverte par la "
         "table, la liaison avant l'appel, le guichet fail-closed)")

# ---- 4. LES BLOCS DÉCOUVERTE + IMPORTS du v2 : VERBATIM contre la pièce ----
source_v2 = SCENARIO_V2.read_text(encoding="utf-8")
bloc_dec = extraire(source_v2, "# ---- LA DÉCOUVERTE PAR LA TABLE D'EXPORTS",
                    "# ---- LA FEUILLE MEMCMP LIÉE")
ns_c = {"ctypes": ctypes, "struct": struct, "base": base, "consigne": print}
ret = executer_bloc(bloc_dec, ns_c)
r_decouvert = ret.get("R_LOUPE13") if isinstance(ret, dict) else None
controle("v2:le-bloc-decouverte-livre-execute",
         r_decouvert == juge["loupe_13_recherche"],
         f"l'export unique loupe_13_recherche découvert @+{r_decouvert:#x} "
         f"== le juge indépendant — le texte LIVRÉ exécuté, VERBATIM")

# le bloc IMPORTS du guichet livré : la découverte du slot, AVANT les
# gestes Windows (qui ne courent pas au labo)
bloc_imp = "    " + dedent4(
    extraire(source_v2, "rep_imports = lire_u32(base, opt + 120)",
                            "k32.LoadLibraryW.restype"))
ns_imp = {"ctypes": ctypes, "struct": struct, "base": base,
          "consigne": print}
ns_imp.update(ret)        # les lire_* + opt, les locaux du bloc découverte
ret_imp = executer_bloc(bloc_imp, ns_imp)
r_slot = ret_imp.get("rva_slot") if isinstance(ret_imp, dict) else None
r_disque = ret_imp.get("sur_disque") if isinstance(ret_imp, dict) else None
controle("v2:le-bloc-imports-du-guichet-execute",
         r_slot == juge_slot and r_disque == juge_valeur,
         f"le slot memcmp découvert @+{r_slot:#x} == le juge indépendant "
         f"@+{juge_slot:#x}, sa valeur sur disque {r_disque:#x} == "
         f"{juge_valeur:#x} — le guichet lit la MÊME table, le texte "
         "LIVRÉ exécuté, VERBATIM (l'indentation de la fonction ôtée d'un "
         "étage, JAMAIS le code touché)")

# LE SHIM MEMCMP (l'équivalent labo du guichet livré — la liaison Windows
# ne court pas au labo ; le harnas sert la feuille, les vecteurs si)
ks = Ks(KS_ARCH_X86, KS_MODE_64)
libc_memcmp = ctypes.cast(libc.memcmp, ctypes.c_void_p).value
SHIM, _ = ks.asm(
    "push rdi\npush rsi\nsub rsp, 8\nmov rdi, rcx\nmov rsi, rdx\n"
    f"mov rdx, r8\nmov rax, {libc_memcmp:#x}\ncall rax\nadd rsp, 8\n"
    "pop rsi\npop rdi\nret\n")
tampon_shim = ctypes.create_string_buffer(bytes(4096))
adresse_shim = ctypes.addressof(tampon_shim)
libc.mprotect(ctypes.c_void_p(adresse_shim & ~0xFFF), ctypes.c_size_t(0x1000), 7)
ctypes.memmove(adresse_shim, bytes(SHIM), len(SHIM))
entree_memcmp = [e for d in pe.DIRECTORY_ENTRY_IMPORT for e in d.imports
                 if e.name and e.name.decode() == "memcmp"][0]
slot_memcmp = entree_memcmp.address
ctypes.memmove(slot_memcmp, struct.pack("<Q", adresse_shim), 8)
print(f"[shim] memcmp servi @ {adresse_shim:#x} — le slot IAT "
      f"@{slot_memcmp - base:+#x} repointé (l'équivalent labo du guichet "
      "livré ; sa valeur sur disque lue au juge indépendant ci-dessous)")

# LE TRAMPOLINE SysV→msx64 À CINQ ARGUMENTS (le départ au slot [rsp+0x28])
TR, _ = ks.asm(
    "mov r11, r8\nmov r8, rdx\nmov rdx, rsi\nmov r9, rcx\nmov rcx, rdi\n"
    "sub rsp, 0x28\nmov qword ptr [rsp + 0x20], r11\n"
    f"mov r10, {base + 0x1380:#x}\ncall r10\nadd rsp, 0x28\nret\n")
tampon_tr = ctypes.create_string_buffer(bytes(4096))
adresse_tr = ctypes.addressof(tampon_tr)
libc.mprotect(ctypes.c_void_p(adresse_tr & ~0xFFF), ctypes.c_size_t(0x1000), 7)
ctypes.memmove(adresse_tr, bytes(TR), len(TR))
LOUPE13 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p, ctypes.c_uint64,
                           ctypes.c_void_p, ctypes.c_uint64,
                           ctypes.c_uint64)(adresse_tr)
print(f"[trampoline] SysV→msx64 à cinq arguments @ {adresse_tr:#x} "
      f"({len(TR)} o) — la pièce appelée au CPU réel")


def verdict(rax):
    v = rax & 0xFFFFFFFF
    return v - 0x100000000 if v > 0x7FFFFFFF else v


# ---- 5. LES BLOCS V1/V2/V3/V4 du v2 : VERBATIM contre la pièce -------------
RECEPTACLE_LABO = pathlib.Path(tempfile.mkdtemp(prefix="preuves-unite13C-"))
fenetre_buf = ctypes.create_string_buffer(8200)
motif_buf = ctypes.create_string_buffer(40)

# le modèle du juge (par AST — pour les blocs livrés)
arbre = ast.parse(source_v2)
gardes = [n for n in ast.walk(arbre)
          if isinstance(n, ast.FunctionDef) and n.name == "modele_recherche"]
assert len(gardes) == 1
ns_modele = {}
exec(compile(ast.Module(body=gardes, type_ignores=[]), "<modele-livré>", "exec"),
     ns_modele)
modele_recherche = ns_modele["modele_recherche"]

ns = {"ctypes": ctypes, "LOUPE13": LOUPE13, "os": os,
      "fenetre_buf": fenetre_buf, "motif_buf": motif_buf,
      "verdict": verdict, "modele_recherche": modele_recherche,
      "random": __import__("random"), "GRAINE": 20261115,
      "consigne": print, "controle": controle,
      "ICI": str(UNITE_C / "kit-v2"), "FENETRE_PROXY": 8192,
      "RECEPTACLE": str(RECEPTACLE_LABO)}

bloc_plomberie = "    " + extraire(
    source_v2, "fenetre_buf = ctypes.create_string_buffer",
    "# ---- V1 : LE DORÉ")
exec(compile("def _plomberie():\n" + bloc_plomberie.rstrip()
             + "\n    return {n: v for n, v in list(locals().items())"
               " if not n.startswith('_')}\n", "<plomberie-livrée>", "exec"), ns)
ret_plomberie = ns["_plomberie"]()
chercher = ret_plomberie["chercher"]
ns["chercher"] = chercher
# les tampons de la plomberie livrée (le bloc V2 livré y lit — I3 : les
# tampons que chercher LIVRÉ écrit, jamais ceux du harnais)
ns["fenetre_buf"] = ret_plomberie["fenetre_buf"]
ns["motif_buf"] = ret_plomberie["motif_buf"]
controle("v2:la-plomberie-livree-execute",
         callable(chercher) and chercher(b"premiere-occurrence",
                                          b"premiere", 0) == 0,
         "les buffers + chercher LIVRÉS exécutés au labo (la feuille "
         "servie par le shim du harnas) — la pièce réelle répond 0")

n_avant = len(REUSSITES)
bloc_v1 = extraire(source_v2, "# ---- V1 : LE DORÉ", "# ---- V2 : LE DIFFÉRENTIEL")
ret_v1 = executer_bloc(bloc_v1, ns)
ns["proxy8k"] = ret_v1["proxy8k"]
controle("v2:le-bloc-v1-livre-execute",
         len([n for n in REUSSITES if n.startswith("V1:")]) == 2,
         "l'école 10/10 + les marques du scellé — le texte LIVRÉ du v2 "
         "exécuté, VERBATIM")

executer_bloc(extraire(source_v2, "# ---- V2 : LE DIFFÉRENTIEL",
                       "# ---- V3 : LES REJETS"), ns)
controle("v2:le-bloc-v2-livre-execute",
         len([n for n in REUSSITES if n.startswith("V2:")]) == 2,
         "le différentiel 10 000/10 000 + la fenêtre et le motif lus "
         "seuls — le texte LIVRÉ du v2 exécuté, VERBATIM (la graine "
         "20261115, les MÊMES tirages)")

executer_bloc(extraire(source_v2, "# ---- V3 : LES REJETS",
                       "# ---- V4 : LA FALSIFICATION"), ns)
controle("v2:le-bloc-v3-livre-execute",
         len([n for n in REUSSITES if n.startswith("V3:")]) == 3,
         "les TROIS rejets -5 — le texte LIVRÉ du v2 exécuté, VERBATIM")

executer_bloc(extraire(source_v2, "# ---- V4 : LA FALSIFICATION",
                       "# ---- LE TÉMOIN"), ns)
fixture = RECEPTACLE_LABO / "falsifie-16.bin"
controle("v2:le-bloc-v4-livre-execute",
         len([n for n in REUSSITES if n.startswith("V4:")]) == 1
         and fixture.exists() and len(fixture.read_bytes()) == 16,
         f"la falsification LIVRÉE exécutée — le fixture écrit au "
         f"réceptacle du labo ({len(fixture.read_bytes())} o)")

# ---- 6. LA PIÈCE INTACTE : la dll du kit v2 == la gravure v1 ----------------
import hashlib
gravure_v1 = {}
for ligne in (KIT_V1 / "EMPREINTES-KIT-UNITE-13-C.txt").read_text(
        encoding="utf-8-sig").splitlines():
    parts = ligne.strip().split(None, 2)
    if len(parts) >= 2 and len(parts[0]) == 64:
        gravure_v1[parts[1]] = parts[0].lower()
sha_dll = hashlib.sha256(PIECE_C.read_bytes()).hexdigest()
controle("la-piece-intacte", sha_dll == gravure_v1["loupe-13-c.dll"],
         f"la dll du kit v2 == la gravure v1 ({sha_dll[:16]}…) — la faute "
         "était au kit, jamais à la pièce")

print()
print(f"=== L'ÉPREUVE DU KIT 13 C v2 : {len(REUSSITES)} VERT, "
      f"{len(ECARTS)} ROUGE ===")
for nom in ECARTS:
    print(f"  ROUGE {nom}")
sys.exit(0 if not ECARTS else 1)
