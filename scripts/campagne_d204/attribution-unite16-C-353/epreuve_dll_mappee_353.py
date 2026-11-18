#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""epreuve_dll_mappee_353.py — L'ÉPREUVE DE LA DLL MAPPÉE (D122 : le bac
n'a aucun Windows). La pièce C réelle — loupe-16-d210-c.dll, le fichier livré
— est MAPPÉE par sections à la base préférée, les en-têtes mappés comme le
vrai chargeur ; LE SHIM STRLEN msx64→SysV (rdi/rsi SAUVÉS ET RENDUS — la
leçon de convention de la 304 : RDI ET RSI SONT NON-VOLATILS EN msx64) reçoit
l'appel de la feuille ; LE TRAMPOLINE SysV→msx64 À SIX ARGUMENTS (les quatre
registres réarrangés + LIGNES et le caractère aux slots [rsp+0x20]/[rsp+0x28])
conduit la pièce ; LA LIAISON VERBATIM : le bloc lier_feuille_strlen du
SCÉNARIO LIVRÉ, extrait PAR AST, exécuté au contexte neutre — le memmove à
son compte et la relecture RÉELS contre la pièce mappée (la loi L4) ; LES
VECTEURS v1-v5 du scénario livré rejoués VERBATIM (les fonctions du module
même) contre la pièce mappée. Avec --t0 : la gravure parsée (la loi L1) par
le lecteur du scénario même, contre l'EMPREINTES du staging.

Sortie : la console de l'épreuve (le bac epreuves/)."""
import ast
import ctypes
import importlib.util

import os
import struct
import subprocess
import sys
import textwrap

ICI = os.path.dirname(os.path.abspath(__file__))
STAGING = os.path.join(ICI, "kit-unite-04-C-d210-attribution-20261118")
PIECE = os.path.join(STAGING, "loupe-16-d210-c.dll")
SCENARIO = os.path.join(STAGING, "scenario-unite16C.py")
ASM = os.path.join(ICI, "asm")
BAC_EPREUVES = os.path.join(ICI, "epreuves")
BASE = 0x25BFA0000

VERTS, ROUGES = 0, 0


def controle(nom, ok, detail=""):
    global VERTS, ROUGES
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom}" + (f" — {detail}" if detail else ""))
    VERTS += ok
    ROUGES += not ok


# ============ LE PARSE PURE-FICHIER DU PE (les lois du bac) =================


def parse_pe(data):
    e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
    opt = e_lfanew + 24
    taille_image = struct.unpack_from("<I", data, opt + 56)[0]
    taille_entetes = struct.unpack_from("<I", data, opt + 60)[0]
    nb_sections = struct.unpack_from("<H", data, e_lfanew + 6)[0]
    opt_size = struct.unpack_from("<H", data, e_lfanew + 20)[0]
    rep_export = struct.unpack_from("<I", data, opt + 112)[0]
    rep_import = struct.unpack_from("<I", data, opt + 120)[0]
    secs = []
    for i in range(nb_sections):
        s = opt + opt_size + 40 * i
        nom = data[s:s + 8].rstrip(b"\x00").decode("latin1")
        vsize, va, rsize, raw = struct.unpack_from("<IIII", data, s + 8)
        secs.append((nom, va, vsize, raw, rsize))
    return {"e_lfanew": e_lfanew, "opt": opt, "taille_image": taille_image,
            "taille_entetes": taille_entetes, "secs": secs,
            "rep_export": rep_export, "rep_import": rep_import}


def rva_of(secs, rva):
    for nom, va, vsize, raw, rsize in secs:
        if va <= rva < va + max(vsize, rsize):
            return raw + (rva - va)
    return None


def main() -> int:
    print("=== L'ÉPREUVE DE LA DLL MAPPÉE — la pièce C réelle contre le "
          "scénario livré, au labo (D122) ===")
    data = open(PIECE, "rb").read()
    pe = parse_pe(data)

    # ---- la table d'exports : l'unique loupe_16_saisie ---------------------
    o = rva_of(pe["secs"], pe["rep_export"])
    nb_noms = struct.unpack_from("<I", data, o + 24)[0]
    tab_f = struct.unpack_from("<I", data, o + 28)[0]
    tab_n = struct.unpack_from("<I", data, o + 32)[0]
    tab_o = struct.unpack_from("<I", data, o + 36)[0]
    rva_par_nom = {}
    for i in range(nb_noms):
        no = rva_of(pe["secs"], struct.unpack_from("<I", data, rva_of(pe["secs"], tab_n + 4 * i))[0])
        nom = data[no:data.index(b"\x00", no)].decode("latin1")
        ordinal = struct.unpack_from("<H", data, rva_of(pe["secs"], tab_o + 2 * i))[0]
        rva_par_nom[nom] = struct.unpack_from("<I", data, rva_of(pe["secs"], tab_f + 4 * ordinal))[0]
    controle("P1:l-export-unique-decouvert-au-fichier",
             set(rva_par_nom) == {"loupe_16_saisie"},
             f"loupe_16_saisie @+{rva_par_nom.get('loupe_16_saisie', 0):#x} — "
             "la découverte par la table, la leçon de la 302")
    R_LOUPE16 = rva_par_nom["loupe_16_saisie"]

    # ---- la table d'imports : la feuille strlen au fichier (la loi L2) ------
    def chaine_f(rva):
        oo = rva_of(pe["secs"], rva)
        return data[oo:data.index(b"\x00", oo)].decode("latin1")

    rva_slot, termine = None, False
    for num_desc in range(16):
        oo = rva_of(pe["secs"], pe["rep_import"] + 20 * num_desc)
        ilt, _, _, rva_dll, iat = struct.unpack_from("<IIIII", data, oo)
        if ilt == 0 and iat == 0:
            termine = True
            break
        if chaine_f(rva_dll).lower() != "msvcrt.dll":
            continue
        marche = ilt if ilt else iat
        for k in range(4096):
            entree = struct.unpack_from(
                "<Q", data, rva_of(pe["secs"], marche + 8 * k))[0]
            if entree == 0:
                termine = True
                break
            if not entree & (1 << 63) and chaine_f(entree + 2) == "strlen":
                rva_slot = iat + 8 * k
        if rva_slot is not None:
            break
    sur_disque = struct.unpack_from(
        "<Q", data, rva_of(pe["secs"], rva_slot))[0] if rva_slot else None
    controle("P2:la-feuille-strlen-decouverte-au-fichier",
             rva_slot is not None and termine and sur_disque is not None,
             f"le descripteur aux CINQ champs, la marche des plages FT "
             f"jusqu'au NULL — le slot @+{rva_slot:#x}, la valeur sur disque "
             f"{sur_disque:#x} (l'entrée hint/nom, l'adresse nue — la 304)")

    # ---- LE MAPPAGE : la base préférée, les en-têtes, les sections ---------
    taille = (pe["taille_image"] + 0xFFF) & ~0xFFF
    libc = ctypes.CDLL("libc.so.6", use_errno=True)
    libc.mmap.restype = ctypes.c_void_p
    libc.mmap.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int,
                          ctypes.c_int, ctypes.c_int, ctypes.c_long]
    MAP_PRIVATE, MAP_ANONYMOUS, MAP_FIXED = 0x02, 0x20, 0x10
    PROT_RWX = 7
    addr = libc.mmap(BASE, taille, PROT_RWX,
                     MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED, -1, 0)
    if addr in (0, (1 << 64) - 1) or addr != BASE:
        print(f"[!] la base préférée inmappe ({addr:#x}) — REFUS (l'épreuve "
              "exige la base)")
        return 2
    # les en-têtes comme le vrai chargeur
    ctypes.memmove(addr, data[:pe["taille_entetes"]],
                   pe["taille_entetes"])
    for nom, va, vsize, raw, rsize in pe["secs"]:
        if rsize:
            ctypes.memmove(addr + va, data[raw:raw + rsize], rsize)
    # la lecture AU-DELÀ du fichier brut (bss) : déjà zéro (anonyme)

    def octets(rva, n):
        return ctypes.string_at(addr + rva, n)

    def chaine_m(rva):
        b = octets(rva, 1)
        sortie = []
        i = 0
        while b[0] != 0 and i < 256:
            sortie.append(chr(b[0]))
            i += 1
            b = octets(rva + i, 1)
        return "".join(sortie)

    e_lfanew = struct.unpack("<I", octets(0x3C, 4))[0]
    opt = e_lfanew + 4 + 20
    rva_exports = struct.unpack("<I", octets(opt + 112, 4))[0]
    nb_noms_m = struct.unpack("<I", octets(rva_exports + 24, 4))[0]
    tab_noms_m = struct.unpack("<I", octets(rva_exports + 32, 4))[0]
    noms_m = [chaine_m(struct.unpack("<I", octets(tab_noms_m + 4 * i, 4))[0])
              for i in range(nb_noms_m)]
    controle("P3:le-mappage-recoupe",
             set(noms_m) == {"loupe_16_saisie"},
             f"la base préférée {BASE:#x}, les en-têtes et les {len(pe['secs'])} "
             "sections mappées — l'export relu AU MAPPAGE : "
             f"{sorted(noms_m)}")

    # ---- LE SHIM STRLEN (msx64 → SysV : rdi/rsi SAUVÉS ET RENDUS) ----------
    def page_rwx():
        a = libc.mmap(0, 0x1000, 7, 0x02 | 0x20, -1, 0)   # RWX, PRIVATE|ANON
        if a in (0, (1 << 64) - 1):
            raise RuntimeError("la page RWX inmappe")
        return a

    shim_bin = open(os.path.join(ASM, "shim.bin"), "rb").read()
    shim_addr = page_rwx()                    # la page alignée RWX au bac
    ctypes.memmove(shim_addr, shim_bin, len(shim_bin))
    strlen_libc = ctypes.cast(libc.strlen, ctypes.c_void_p).value
    struct.pack_into("<Q", (ctypes.c_char * 64).from_address(shim_addr),
                     0x1C, strlen_libc)
    controle("P4:le-shim-strlen-ne",
             True,
             f"msx64→SysV : rcx→rdi, rdi/rsi SAUVÉS ET RENDUS (la leçon de "
             f"convention de la 304), l'alignement compté — la cible "
             f"libc strlen {strlen_libc:#x}")

    # ---- LA LIAISON VERBATIM (la loi L4) : le bloc du scénario LIVRÉ -------
    source = open(SCENARIO, encoding="utf-8").read()
    arbre = ast.parse(source)
    seg = None
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.FunctionDef) and noeud.name == "main":
            for fils in ast.walk(noeud):
                if isinstance(fils, ast.FunctionDef) \
                        and fils.name == "lier_feuille_strlen":
                    seg = ast.get_source_segment(source, fils)
        if seg:
            break
    controle("P5:le-bloc-liaison-extrait-par-ast", seg is not None,
             "lier_feuille_strlen extrait VERBATIM du scénario livré")

    class _Fn:
        """Le stub-fonction : restype/argtypes posables (la forme WinDLL),
        l'appel neutre."""

        def __init__(self, comportement):
            self.restype = None
            self.argtypes = None
            self._comportement = comportement

        def __call__(self, *args):
            return self._comportement(*args)

    class _K32:
        """Le contexte neutre : les gestes Windows neutralisés, le memmove
        et la relecture RÉELS (la méthode de la 351)."""

        def __getattr__(self, nom):
            if nom == "LoadLibraryW":
                return _Fn(lambda n: 0x1111)
            if nom == "GetProcAddress":
                return _Fn(lambda m, n: shim_addr if n == b"strlen" else 0)
            if nom == "VirtualProtect":
                def vp(a, n, p, ancien):
                    ancien._obj.value = 0x40
                    return 1
                return _Fn(vp)
            return _Fn(lambda *a: 0)

    class _WT:
        DWORD = ctypes.c_uint32
        BOOL = ctypes.c_int
        LPCWSTR = ctypes.c_wchar_p
        LPCSTR = ctypes.c_char_p

    ctx = {"struct": struct, "ctypes": ctypes, "wt": _WT, "k32": _K32(),
           "consigne": lambda s: print("    " + s),
           "base": addr, "opt": opt,
           "lire_octets": lambda rva, n: ctypes.string_at(addr + rva, n),
           "lire_u32": lambda rva: struct.unpack(
               "<I", ctypes.string_at(addr + rva, 4))[0],
           "lire_chaine": chaine_m}
    exec(textwrap.dedent(seg), ctx)
    feuille = ctx["lier_feuille_strlen"]()
    controle("P6:la-liaison-verbatim-vecue",
             feuille is not None and feuille[0] == rva_slot
             and feuille[2] == shim_addr,
             f"le memmove à SON COMPTE (8) et la relecture RÉELS contre la "
             f"pièce mappée : le slot @+{feuille[0]:#x} repointé au shim "
             f"{feuille[2]:#x}, la valeur sur disque {feuille[1]:#x} lue "
             "avant le geste — le bloc du scénario LIVRÉ, au contexte neutre")

    # ---- LE TRAMPOLINE (SysV → msx64 à six arguments) ----------------------
    tramp_bin = open(os.path.join(ASM, "tramp.bin"), "rb").read()
    tramp_addr = page_rwx()                   # la page alignée RWX au bac
    ctypes.memmove(tramp_addr, tramp_bin, len(tramp_bin))
    struct.pack_into("<Q", (ctypes.c_char * 128).from_address(tramp_addr),
                     0x31, addr + R_LOUPE16)
    controle("P7:le-trampoline-ne",
             True,
             "les quatre registres réarrangés + LIGNES et le caractère aux "
             "slots [rsp+0x20]/[rsp+0x28], l'ombre posée — la cible "
             f"{addr + R_LOUPE16:#x}")

    SAISIR = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p,
                              ctypes.c_void_p, ctypes.c_void_p,
                              ctypes.c_void_p, ctypes.c_uint,
                              ctypes.c_uint)(tramp_addr)

    # ---- LE SCÉNARIO LIVRÉ CHARGÉ (les vecteurs du module même) ------------
    spec = importlib.util.spec_from_file_location("scenario_unite16C",
                                                  SCENARIO)
    module = importlib.util.module_from_spec(spec)
    sys.modules["scenario_unite16C"] = module
    spec.loader.exec_module(module)
    controle("P8:le-module-charge",
             module.GRAINE == 20261115 and module.LIGNES == 27,
             f"la graine {module.GRAINE}, L'ÉCRAN EN ARGUMENT LIGNES="
             f"{module.LIGNES} (la loi L5 : le même 27 que le harnais et "
             "l'épreuve POSIX — l'écran annoncé, l'écran posé)")

    # T0 au besoin (la gravure parsée — la loi L1, le lecteur du scénario même)
    if "--t0" in sys.argv:
        empreintes = module.lire_empreintes()
        sha_dll = module.sha256_fichier(PIECE)
        attendu = empreintes.get("loupe-16-d210-c.dll", "")
        controle("T0:la-piece-recoupee-a-l-empreinte-gravee",
                 bool(empreintes) and sha_dll == attendu,
                 f"loupe-16-d210-c.dll sha256 {sha_dll[:16]}… == la gravure "
                 "du kit — le lecteur du scénario même, la loi L1")

    # ---- LES VECTEURS REJOUÉS VERBATIM (les fonctions du module) -----------
    os.makedirs(BAC_EPREUVES, exist_ok=True)
    module.RECEPTACLE = BAC_EPREUVES
    module.v1_le_differentiel(SAISIR)
    module.v2_le_scenario_dore(SAISIR)
    s_v3 = module.v3_les_rejets(SAISIR)
    module.v4_le_repli(SAISIR, s_v3)
    module.v5_la_falsification(SAISIR)
    n_verts = len(module.REUSSITES)
    n_rouges = len(module.ECARTS)

    print(f"\n=== L'ÉPREUVE DE LA DLL MAPPÉE : {VERTS} STRUCTURELS, "
          f"{n_verts} VECTEURS VERT, {n_rouges + ROUGES} ROUGE ===")
    return 0 if (ROUGES + n_rouges) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
