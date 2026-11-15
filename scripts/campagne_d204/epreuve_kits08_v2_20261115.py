#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""epreuve_kits08_v2_20261115.py — L'ÉPREUVE DES KITS 08 v2 : LE TEXTE LIVRÉ,
PLOMBERIE COMPRISE (la leçon du défaut du 15/11 apr-midi).

Le défaut nommé : les épreuves de la 286 exécutaient la fonction PURE du
scénario livré (le juge modele_ligne, par AST) — la PLOMBERIE Windows (la
boucle V3 du bras T, la découverte par la table d'exports du bras C) courait
au labo dans AUCUN fichier livré. Les DEUX kits v1 ont planté au terrain
(ligne 232 du T : « cannot be converted to pointer » ; la découverte du C :
les arités). L'épreuve v2 referme la brèche : les BLOCS LIVRÉS extraits
VERBATIM des scénarios v2 sont EXÉCUTÉS au labo —
  · le bloc V3 du T contre UNE PIÈCE DU LABO (gcc, le même contrat : les
    rejets -5, RIEN écrit) ;
  · le bloc DÉCOUVERTE du C contre LA PIÈCE RÉELLE loupe-08-c.dll mappée
    par sections à une base factice (le geste de LoadLibraryEx rejoué) ;
  · les blocs v1 rejoués : les DEUX plantages REPRODUITS au labo (le défaut
    nommé sur pièces) ;
  · les épreuves de la 286/294 (le juge, les constantes, le générateur)
    rejouées sur les sources v2 — la fonction PURE n'a pas bougé.
"""
import ctypes
import pathlib
import py_compile
import struct
import subprocess
import sys
import tempfile

CAMP = pathlib.Path(__file__).resolve().parent
UNITE_T = CAMP / "unite-08-T"
UNITE_C = CAMP / "unite-08-C"
import tempfile
LABO = pathlib.Path(tempfile.mkdtemp(prefix="epreuve-v2-08-"))

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
    le ramasseur des locaux (les blancs de queue du fichier livré — 4
    espaces muets à la ligne 201 — ne comptent pas)."""
    code = ("def _bloc():\n" + bloc.rstrip()
            + "\n    return {n: v for n, v in list(locals().items())"
              " if not n.startswith('_')}\n")
    exec(compile(code, "<bloc-livré>", "exec"), ns)
    return ns["_bloc"]()


# ---- 0. py_compile des DEUX sources v2 --------------------------------------
for p in (UNITE_T / "scenario-unite08.py", UNITE_C / "scenario-unite08C.py"):
    py_compile.compile(str(p), doraise=True)
print("[VERT] py_compile des DEUX scénarios v2 (les sources corrigées)")

# ---- 1. LA PIÈCE DU LABO (gcc, le contrat des rejets) -----------------------
STUB_C = LABO / "piece-labo-loupe08-v2.c"
STUB_SO = LABO / "piece-labo-loupe08-v2.so"
STUB_C.write_text(
    "#include <stdint.h>\n"
    "int64_t loupe_08_ligne(const void *src, uint64_t len, void *dst,\n"
    "                      uint64_t off)\n"
    "{\n"
    "    (void)off;\n"
    "    if (len == 0 || len > 16 || src == 0 || dst == 0)\n"
    "        return -5;              /* le refus : RIEN d'ecrit, jamais */\n"
    "    return 0;\n"
    "}\n", encoding="ascii")
r = subprocess.run(["gcc", "-shared", "-fPIC", "-O2", "-o", str(STUB_SO),
                    str(STUB_C)], capture_output=True, text=True)
assert r.returncode == 0, r.stderr
print(f"[VERT] la pièce du labo compilée (gcc -O2 -shared, {STUB_SO.name})")

lib = ctypes.CDLL(str(STUB_SO))
lib.loupe_08_ligne.restype = ctypes.c_int64
LOUPE08 = ctypes.CFUNCTYPE(
    ctypes.c_int64, ctypes.c_void_p, ctypes.c_uint64,
    ctypes.c_void_p, ctypes.c_uint64)(
    ctypes.cast(lib.loupe_08_ligne, ctypes.c_void_p).value)

POISON = b"\xCC"


def verdict(rax):
    v = rax & 0xFFFFFFFF
    return v - 0x100000000 if v > 0x7FFFFFFF else v


# ---- 2. LE BLOC V3 DU BRAS T : le texte v2 VERBATIM contre la pièce du labo --
src_v2_T = (UNITE_T / "scenario-unite08.py").read_text(encoding="utf-8")
bloc_v2 = extraire(src_v2_T, "# ---- V3 : LES REJETS", "# ---- V4 : LA FALSIFICATION")
source_buf = ctypes.create_string_buffer(16)
sortie_buf = ctypes.create_string_buffer(96)
ns = {"ctypes": ctypes, "LOUPE08": LOUPE08, "source_buf": source_buf,
      "sortie_buf": sortie_buf, "POISON": POISON, "verdict": verdict,
      "consigne": print, "controle": controle, "bytes": bytes}
ret = executer_bloc(bloc_v2, ns)
controle("v2-T:le-bloc-v3-livre-execute-vert",
         isinstance(ret, dict)
         and len([n for n in REUSSITES if n.startswith("V3:")]) == 4,
         "les QUATRE rejets -5, la sortie POISON INTACTE — le texte LIVRÉ "
         "exécuté au labo, VERBATIM")

# ---- 3. LE BLOC V3 DU BRAS T : le texte v1 REPRODUIT ------------------------
REUSSITES.clear(), ECARTS.clear()
src_v1_T = (UNITE_T / "kit" / "scenario-unite08.py").read_text(encoding="utf-8")
bloc_v1 = extraire(src_v1_T, "# ---- V3 : LES REJETS", "# ---- V4 : LA FALSIFICATION")
try:
    executer_bloc(bloc_v1, dict(ns))
    controle("v1-T:le-plantage-reproduit", False, "le texte v1 n'a pas planté ?!")
except TypeError as e:
    controle("v1-T:le-plantage-reproduit",
             str(e) == "cannot be converted to pointer",
             f"TypeError: {e} — la ligne 232 du terrain rejouée au labo")

# ---- 4. LA PIÈCE RÉELLE DU C : loupe-08-c.dll mappée par sections -----------
PIECE_C = UNITE_C / "source" / "loupe-08-c.dll"
donnees = PIECE_C.read_bytes()
e_lfanew = struct.unpack_from("<I", donnees, 0x3C)[0]
n_sections = struct.unpack_from("<H", donnees, e_lfanew + 6)[0]
taille_opt = struct.unpack_from("<H", donnees, e_lfanew + 20)[0]
opt = e_lfanew + 4 + 20
taille_image = struct.unpack_from("<I", donnees, opt + 56)[0]
taille_entetes = struct.unpack_from("<I", donnees, opt + 60)[0]
image = ctypes.create_string_buffer(taille_image)     # l'image mappée, à zéro
ctypes.memmove(image, donnees[:taille_entetes], taille_entetes)
for i in range(n_sections):
    s = opt + taille_opt + 40 * i
    vtaille, vaddr, rtaille, raddr = struct.unpack_from("<IIII", donnees, s + 8)
    if rtaille:
        ctypes.memmove(ctypes.byref(image, vaddr), donnees[raddr:raddr + rtaille],
                       rtaille)
base = ctypes.addressof(image)
print(f"[cartographie] loupe-08-c.dll : {n_sections} sections, l'image "
      f"{taille_image:#x} o mappée @ {base:#x} (le geste de LoadLibraryEx "
      f"rejoué au labo)")

# LE JUGE INDÉPENDANT : la table d'exports lue du FICHIER BRUT (jamais la
# même plomberie que le bloc livré)
def rva_vers_brut(rva):
    for i in range(n_sections):
        s = opt + taille_opt + 40 * i
        vtaille, vaddr, rtaille, raddr = struct.unpack_from("<IIII", donnees, s + 8)
        if vaddr <= rva < vaddr + max(vtaille, rtaille):
            return raddr + (rva - vaddr)
    raise ValueError(f"rva {rva:#x} hors sections")


rva_exp = struct.unpack_from("<I", donnees, opt + 112)[0]
nb_noms_j = struct.unpack_from("<I", donnees, rva_vers_brut(rva_exp + 24))[0]
tab_f_j = struct.unpack_from("<I", donnees, rva_vers_brut(rva_exp + 28))[0]
tab_n_j = struct.unpack_from("<I", donnees, rva_vers_brut(rva_exp + 32))[0]
tab_o_j = struct.unpack_from("<I", donnees, rva_vers_brut(rva_exp + 36))[0]
juge = {}
for i in range(nb_noms_j):
    nrva = struct.unpack_from("<I", donnees, rva_vers_brut(tab_n_j + 4 * i))[0]
    fin = donnees.index(b"\x00", rva_vers_brut(nrva))
    nom = donnees[rva_vers_brut(nrva):fin].decode("ascii")
    ordinal = struct.unpack_from("<H", donnees, rva_vers_brut(tab_o_j + 2 * i))[0]
    juge[nom] = struct.unpack_from("<I", donnees,
                                   rva_vers_brut(tab_f_j + 4 * ordinal))[0]
assert juge == {"loupe_08_ligne": juge["loupe_08_ligne"]}, juge
print(f"[juge indépendant] l'export unique loupe_08_ligne @+"
      f"{juge['loupe_08_ligne']:#x} (lu du fichier brut, la table de "
      f"sections du juge)")

# ---- 5. LE BLOC DÉCOUVERTE DU C : le texte v2 VERBATIM contre la pièce réelle
REUSSITES.clear(), ECARTS.clear()
src_v2_C = (UNITE_C / "scenario-unite08C.py").read_text(encoding="utf-8")
bloc_dec_v2 = extraire(src_v2_C, "# ---- LA DÉCOUVERTE PAR LA TABLE D'EXPORTS",
                       "LOUPE08 = ctypes.CFUNCTYPE")
ns_c = {"ctypes": ctypes, "struct": struct, "base": base, "consigne": print}
ret = executer_bloc(bloc_dec_v2, ns_c)
r_ligne = ret.get("R_LIGNE") if isinstance(ret, dict) else None
controle("v2-C:le-bloc-decouverte-livre-execute-vert",
         r_ligne == juge["loupe_08_ligne"],
         f"l'export unique loupe_08_ligne découvert @+{r_ligne:#x} == le juge "
         f"indépendant — le texte LIVRÉ exécuté au labo, VERBATIM")

# ---- 6. LE BLOC DÉCOUVERTE DU C : le texte v1 REPRODUIT ---------------------
src_v1_C = (UNITE_C / "kit" / "scenario-unite08C.py").read_text(encoding="utf-8")
bloc_dec_v1 = extraire(src_v1_C, "# ---- LA DÉCOUVERTE PAR LA TABLE D'EXPORTS",
                       "LOUPE08 = ctypes.CFUNCTYPE")
try:
    executer_bloc(bloc_dec_v1, dict(ns_c))
    controle("v1-C:le-plantage-reproduit", False, "le texte v1 n'a pas planté ?!")
except TypeError as e:
    controle("v1-C:le-plantage-reproduit", "positional argument" in str(e),
             f"TypeError: {e} — l'arité de la découverte, la brèche du labo")

# ---- 7. LES ÉPREUVES DE LA 286/294 rejouées sur les sources v2 --------------
for epreuve in ("epreuve_scenario_unite08.py", "epreuve_scenario_unite08C.py"):
    chemin = (UNITE_T if "unite08.py" in epreuve else UNITE_C) / epreuve
    if not chemin.exists():
        print(f"[NOTE] {epreuve} introuvable — sautée")
        continue
    r = subprocess.run([sys.executable, str(chemin)], capture_output=True,
                       text=True, timeout=300)
    vert = r.returncode == 0 and "[VERT]" in r.stdout and "Traceback" not in r.stderr
    controle(f"v2:epreuve-286-{epreuve}", vert,
             (r.stdout.strip().splitlines() or ["(vide)"])[-1][:100])

print()
print(f"=== L'ÉPREUVE DES KITS 08 v2 : {len(REUSSITES)} VERT, "
      f"{len(ECARTS)} ROUGE ===")
for nom in ECARTS:
    print(f"  ROUGE {nom}")
sys.exit(0 if not ECARTS else 1)
