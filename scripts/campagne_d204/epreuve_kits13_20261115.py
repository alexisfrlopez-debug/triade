#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""epreuve_kits13_20261115.py — L'ÉPREUVE DES KITS 13 : LE TEXTE LIVRÉ,
PLOMBERIE COMPRISE (la brèche de la 302 refermée, tenue pour toujours).

La leçon du défaut du 15/11 : les épreuves de la 286 exécutaient la
fonction PURE du scénario livré — la PLOMBERIE Windows (les buffers ctypes,
le cinquième argument à la pile, la découverte par la table d'exports)
n'avait jamais couru au labo dans un fichier livré. Les kits 08 v1 ont
planté au terrain pour cela. L'épreuve referme la brèche pour l'unité 5 :
les BLOCS LIVRÉS extraits VERBATIM des scénarios 13 sont EXÉCUTÉS au
labo —
  · les blocs V1/V3/V4 du T contre LA PIÈCE RÉELLE du bras C (loupe-13-c.dll
    mappée par sections, le trampoline SysV→msx64 à cinq arguments — le
    geste de LoadLibraryEx rejoué) : l'école, les marques du scellé, les
    TROIS rejets -5, la falsification et le fixture AU RÉCEPTACLE ;
  · le bloc DÉCOUVERTE du C contre LA PIÈCE RÉELLE mappée à une base
    factice : l'export unique loupe_13_recherche == LE JUGE INDÉPENDANT
    (la table d'exports lue du fichier brut par la table de sections du
    juge) ;
  · les épreuves de la 286/294 (le juge par AST, les constantes au plan,
    le générateur déterministe) rejouées sur les DEUX sources livrées.
"""
import ast
import ctypes
import mmap
import os
import pathlib
import pefile
import py_compile
import struct
import subprocess
import sys
import tempfile

from keystone import Ks, KS_ARCH_X86, KS_MODE_64

UNITE_T = pathlib.Path("/home/z/my-project/projet-triade/github-mirror/"
                       "scripts/campagne_d204/unite-13-T")
UNITE_C = pathlib.Path("/home/z/my-project/projet-triade/github-mirror/"
                       "scripts/campagne_d204/unite-13-C")

REUSSITES, ECARTS = [], []


def controle(nom, ok, detail=""):
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom}" + (f" — {detail}" if detail else ""))
    (REUSSITES if ok else ECARTS).append(nom)


def extraire(texte, debut, fin):
    i = texte.index(debut)
    j = texte.index(fin, i)
    return texte[i:j]


def executer_bloc(bloc, ns):
    """Le bloc livré (indenté à 4, comme au corps de main) exécuté VERBATIM
    — enveloppé d'une fonction, JAMAIS réécrit ; la queue ajoute SEULEMENT
    le ramasseur des locaux."""
    code = ("def _bloc():\n" + bloc.rstrip()
            + "\n    return {n: v for n, v in list(locals().items())"
              " if not n.startswith('_')}\n")
    exec(compile(code, "<bloc-livré>", "exec"), ns)
    return ns["_bloc"]()


# ---- 0. py_compile des DEUX sources livrées ---------------------------------
for p in (UNITE_T / "scenario-unite13.py",
          UNITE_C / "scenario-unite13C.py"):
    py_compile.compile(str(p), doraise=True)
print("[VERT] py_compile des DEUX scénarios 13 livrés")

# ---- 1. LA PIÈCE RÉELLE DU C : mappée par sections (le chargeur du labo) ----
PIECE_C = UNITE_C / "source" / "loupe-13-c.dll"
pe = pefile.PE(str(PIECE_C))
base = pe.OPTIONAL_HEADER.ImageBase
taille = pe.OPTIONAL_HEADER.SizeOfImage
brut = PIECE_C.read_bytes()
libc = ctypes.CDLL("libc.so.6", use_errno=True)
libc.mmap.restype = ctypes.c_void_p
libc.mmap.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int,
                      ctypes.c_int, ctypes.c_int, ctypes.c_long]
libc.mmap(ctypes.c_void_p(base), ctypes.c_size_t(taille), 7, 0x32, -1, 0)
# les EN-TÊTES D'ABORD (le vrai chargeur les mappe — le bloc découverte
# livré lit la table d'exports dans l'image mappée même)
ctypes.memmove(base, brut[:pe.OPTIONAL_HEADER.SizeOfHeaders],
               pe.OPTIONAL_HEADER.SizeOfHeaders)
for s in pe.sections:
    donnees = s.get_data()
    if donnees:
        ctypes.memmove(base + s.VirtualAddress, donnees, len(donnees))
print(f"[mappage] loupe-13-c.dll : {len(pe.sections)} sections, l'image "
      f"{taille:#x} o @ {base:#x} (la base préférée — le geste de "
      f"LoadLibraryEx rejoué)")

# LE SHIM MEMCMP (la feuille unique — RDI/RSI non-volatils msx64, sauvés)
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
slot_memcmp = [e.address for d in pe.DIRECTORY_ENTRY_IMPORT for e in d.imports
               if e.name and e.name.decode() == "memcmp"][0]
ctypes.memmove(slot_memcmp, struct.pack("<Q", adresse_shim), 8)
print(f"[shim] memcmp servi @ {adresse_shim:#x} — le slot IAT "
      f"@{slot_memcmp - base:+#x} repointé (la feuille unique)")

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


# LE JUGE INDÉPENDANT : la table d'exports lue du FICHIER BRUT (jamais la
# même plomberie que le bloc livré)
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
print(f"[juge indépendant] l'export unique loupe_13_recherche @+"
      f"{juge['loupe_13_recherche']:#x} (lu du fichier brut)")

# ---- 2. LE MODÈLE DU JUGE (par AST — pour les blocs livrés) ------------------
source_T = (UNITE_T / "kit" / "scenario-unite13.py").read_text(encoding="utf-8")
arbre = ast.parse(source_T)
gardes = [n for n in ast.walk(arbre)
          if isinstance(n, ast.FunctionDef) and n.name == "modele_recherche"]
assert len(gardes) == 1
module = ast.Module(body=gardes, type_ignores=[])
ns_modele = {}
exec(compile(module, "<modele-livré>", "exec"), ns_modele)
modele_recherche = ns_modele["modele_recherche"]

# ---- 3. LES BLOCS V1/V3/V4 DU T : le texte livré VERBATIM contre la pièce ----
RECEPTACLE_LABO = pathlib.Path(tempfile.mkdtemp(prefix="preuves-unite13-"))
fenetre_buf = ctypes.create_string_buffer(8200)
motif_buf = ctypes.create_string_buffer(40)
ns = {"ctypes": ctypes, "LOUPE13": LOUPE13, "os": os,
      "fenetre_buf": fenetre_buf, "motif_buf": motif_buf,
      "verdict": verdict, "modele_recherche": modele_recherche,
      "consigne": print, "controle": controle,
      "ICI": str(UNITE_T / "kit"), "FENETRE_PROXY": 8192,
      "RECEPTACLE": str(RECEPTACLE_LABO)}

# la plomberie livrée : les buffers + chercher (le 5e argument à la pile)
bloc_plomberie = "    " + extraire(
    source_T, "fenetre_buf = ctypes.create_string_buffer",
    "# ---- V1 : LE DORÉ")   # (les 4 espaces de la ligne première rendus)
exec(compile("def _plomberie():\n" + bloc_plomberie.rstrip()
             + "\n    return {n: v for n, v in list(locals().items())"
               " if not n.startswith('_')}\n", "<plomberie-livrée>", "exec"), ns)
ret_plomberie = ns["_plomberie"]()
chercher = ret_plomberie["chercher"]
ns["chercher"] = chercher        # (le bloc V1 livré la référence par son nom)
controle("T:la-plomberie-livree-execute",
         callable(chercher) and chercher(b"premiere-occurrence",
                                          b"premiere", 0) == 0,
         "les buffers + chercher LIVRÉS exécutés au labo — le 5e argument "
         "posé au slot msx64 par ctypes, la pièce réelle répond 0 (MZ de "
         "l'école)")

bloc_v1 = extraire(source_T, "# ---- V1 : LE DORÉ", "# ---- V2 : LE DIFFÉRENTIEL")
ret_v1 = executer_bloc(bloc_v1, ns)
ns["proxy8k"] = ret_v1["proxy8k"]   # (le bloc V4 livré la référence par son nom)
controle("T:le-bloc-v1-livre-execute",
         len([n for n in REUSSITES if n.startswith("V1:")]) == 2,
         "l'école 10/10 + les marques du scellé (MZ @0, PE @+0x40, les "
         "absentes → LA FIN NOMMÉE) — le texte LIVRÉ exécuté, VERBATIM")

bloc_v3 = extraire(source_T, "# ---- V3 : LES REJETS", "# ---- V4 : LA FALSIFICATION")
executer_bloc(bloc_v3, ns)
controle("T:le-bloc-v3-livre-execute",
         len([n for n in REUSSITES if n.startswith("V3:")]) == 3,
         "les TROIS rejets -5 (le motif vide, le motif de 33, le départ "
         "au-delà) — le texte LIVRÉ exécuté, VERBATIM")

bloc_v4 = extraire(source_T, "# ---- V4 : LA FALSIFICATION",
                   "# ---- LE TÉMOIN")
executer_bloc(bloc_v4, ns)
fixture = RECEPTACLE_LABO / "falsifie-16.bin"
controle("T:le-bloc-v4-livre-execute",
         len([n for n in REUSSITES if n.startswith("V4:")]) == 1
         and fixture.exists() and len(fixture.read_bytes()) == 16,
         f"la falsification LIVRÉE exécutée — le fixture falsifie-16.bin "
         f"écrit au réceptacle du labo ({len(fixture.read_bytes())} o), "
         "l'octet du « MZ » détruit : la réponse -1 LA FIN NOMMÉE == le "
         "modèle du mutant")

# ---- 4. LE BLOC DÉCOUVERTE DU C : le texte livré VERBATIM contre la pièce ----
REUSSITES.clear(), ECARTS.clear()
source_C = (UNITE_C / "kit" / "scenario-unite13C.py").read_text(encoding="utf-8")
bloc_dec = extraire(source_C, "# ---- LA DÉCOUVERTE PAR LA TABLE D'EXPORTS",
                    "# LA PIÈCE COMME FONCTION")
ns_c = {"ctypes": ctypes, "struct": struct, "base": base, "consigne": print}
ret = executer_bloc(bloc_dec, ns_c)
r_decouvert = ret.get("R_LOUPE13") if isinstance(ret, dict) else None
controle("C:le-bloc-decouverte-livre-execute",
         r_decouvert == juge["loupe_13_recherche"],
         f"l'export unique loupe_13_recherche découvert @+{r_decouvert:#x} "
         f"== le juge indépendant (la convention (base, rva) unifiée — la "
         f"leçon de la 302 tenue) — le texte LIVRÉ exécuté, VERBATIM")

# ---- 5. LES ÉPREUVES DE LA 286/294 rejouées sur les DEUX sources -----------
for epreuve, unite in (("epreuve_scenario_unite13.py", UNITE_T),
                       ("epreuve_scenario_unite13C.py", UNITE_C)):
    r = subprocess.run([sys.executable, str(unite / epreuve)],
                       capture_output=True, text=True, timeout=300)
    vert = r.returncode == 0 and "[VERT]" in r.stdout \
        and "Traceback" not in r.stderr
    controle(f"286-294:{epreuve}", vert,
             (r.stdout.strip().splitlines() or ["(vide)"])[-1][:100])

print()
print(f"=== L'ÉPREUVE DES KITS 13 : {len(REUSSITES)} VERT, "
      f"{len(ECARTS)} ROUGE ===")
for nom in ECARTS:
    print(f"  ROUGE {nom}")
sys.exit(0 if not ECARTS else 1)
