#!/usr/bin/env python3
"""cpuid_dispatch.py — atelier IO3UH37CJ (la vague 16).

LE DISPATCH CPUID de l'agrégation GHASH 8 blocs + VAES/VPCLMULQDQ, avec le
REPLI SCELLÉ — sans retirer aucun contrôle.

La règle du repli : un chemin accéléré QUI N'EXISTE PAS sur le silicium n'est
jamais pris. Le dispatch lit le CPUID, choisit, et TOUT chemin retombe sur la
chaîne scellée (le GHASH scellé 0xDFC0 chaîné par bloc, l'AES scellé 0xDF00).
Le contrôle 32/32 : pour les 32 combinaisons de drapeaux possibles (5 bits),
le dispatch rend TOUJOURS un chemin valide — jamais un chemin mort.

LE CPUID par un thunk natif alloué PAGE_EXECUTE_READWRITE (VirtualAlloc) :
les buffers Python ne sont pas exécutables (DEP) — la voie est NOMMÉE, pas
contournée. Si le CPUID est illisible, le repli scellé est le chemin FORCÉ et
l'écart est nommé : jamais un chemin accéléré supposé.
"""

import argparse
import ctypes
import json
import sys

# Les cinq drapeaux du dispatch (l'ordre est canonique)
DRAPEAUX = ("pclmulqdq", "aes", "vaes", "vpclmulqdq", "avx2")

# push rbx ; mov eax,ecx ; mov r10,rdx ; mov rcx,r10 ; cpuid ;
# mov [r8],rax ; mov [r8+8],rbx ; mov [r8+16],rcx ; mov [r8+24],rdx ; pop rbx ; ret
THUNK = bytes.fromhex(
    "53"          # push rbx
    "89c8"        # mov eax, ecx        (le feuille : 1er argument, RCX)
    "4c8bd2"      # mov r10, rdx        (la sous-feuille : 2e argument, RDX)
    "4c89d1"      # mov rcx, r10
    "0fa2"        # cpuid
    "498900"      # mov [r8], rax       (la sortie : 3e argument, R8)
    "49895808"    # mov [r8+8], rbx
    "49894810"    # mov [r8+16], rcx
    "49895018"    # mov [r8+24], rdx
    "5b"          # pop rbx
    "c3"          # ret
)

MEM_COMMIT, MEM_RESERVE, PAGE_EXECUTE_READWRITE, MEM_RELEASE = 0x1000, 0x2000, 0x40, 0x8000

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
kernel32.VirtualAlloc.restype = ctypes.c_void_p
kernel32.VirtualAlloc.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint32, ctypes.c_uint32]
kernel32.VirtualFree.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint32]


def cpuid(feuille: int, sous_feuille: int = 0):
    """-> (eax, ebx, ecx, edx) — ou (None,)*4 si le CPUID est illisible."""
    taille = len(THUNK) + 16
    adresse = kernel32.VirtualAlloc(None, taille, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE)
    if not adresse:
        return (None,) * 4
    try:
        ctypes.memmove(adresse, THUNK, len(THUNK))
        sortie = ctypes.create_string_buffer(32)   # 4 registres × 8 o — JAMAIS 16
        proto = ctypes.CFUNCTYPE(None, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p)
        proto(adresse)(feuille, sous_feuille, ctypes.cast(sortie, ctypes.c_void_p))
        brut = sortie.raw
        # le thunk écrit QUATRE mots de 64 bits : EAX@0 · EBX@8 · ECX@16 · EDX@24
        return (int.from_bytes(brut[0:4], "little"),
                int.from_bytes(brut[8:12], "little"),
                int.from_bytes(brut[16:20], "little"),
                int.from_bytes(brut[24:28], "little"))
    except Exception:
        return (None,) * 4
    finally:
        kernel32.VirtualFree(adresse, 0, MEM_RELEASE)


def drapeaux_reels():
    """Les drapeaux du SILICIUM — ou None si CPUID est illisible (le repli est NOMMÉ)."""
    a1, b1, c1, d1 = cpuid(1)
    a7, b7, c7, d7 = cpuid(7, 0)
    if a1 is None or a7 is None:
        return None
    return {
        "pclmulqdq": bool(c1 & (1 << 1)),
        "aes": bool(c1 & (1 << 25)),
        "vaes": bool(b7 & (1 << 9)),        # leaf 7, EBX bit 9
        "vpclmulqdq": bool(b7 & (1 << 10)),   # leaf 7, EBX bit 10
        "avx2": bool(b7 & (1 << 5)),          # leaf 7, EBX bit 5
    }


def dispatch(drapeaux):
    """Le choix du chemin — TOUT chemin retombe sur le scellé."""
    if all(drapeaux.get(d) for d in ("vaes", "vpclmulqdq", "avx2", "pclmulqdq")):
        return "GHASH-8B-VAES", "l'agrégation 8 blocs + VAES/VPCLMULQDQ"
    if drapeaux.get("pclmulqdq") and drapeaux.get("aes"):
        return "GHASH-AGREGE-4", "l'agrégation 4 blocs PCLMULQDQ (le couloir 0xF800)"
    return "REPLI-SCELLE", "la chaîne scellée par bloc (GHASH 0xDFC0, AES 0xDF00)"


def autotest():
    print("=== LE DISPATCH CPUID ET LE REPLI SCELLÉ ===")
    reels = drapeaux_reels()
    if reels is None:
        print("  le CPUID est ILLISIBLE sur ce poste (le thunk n'a pas pu s'exécuter)")
        print("  → le repli scellé est le chemin FORCÉ, et l'écart est NOMMÉ")
        chemin, note = "REPLI-SCELLE", "le CPUID illisible — jamais un chemin accéléré supposé"
    else:
        print("  les drapeaux du silicium : " + ", ".join(
            f"{d}={'OUI' if reels[d] else 'non'}" for d in DRAPEAUX))
        chemin, note = dispatch(reels)
    print(f"  le chemin retenu : {chemin} — {note}")

    # LE CONTRÔLE 32/32 : les 32 combinaisons de drapeaux rendent TOUJOURS un chemin valide
    print("  LE CONTRÔLE 32/32 (toutes les combinaisons de drapeaux) :")
    valides = {"GHASH-8B-VAES", "GHASH-AGREGE-4", "REPLI-SCELLE"}
    rendus = []
    for i in range(32):
        d = {k: bool(i & (1 << n)) for n, k in enumerate(DRAPEAUX)}
        rendus.append(dispatch(d)[0])
    tous = all(c in valides for c in rendus)
    print(f"    32 combinaisons → {'32/32 VALIDES' if tous else 'UN CHEMIN MORT'}")
    for c in sorted(set(rendus)):
        print(f"      {c:16s} {rendus.count(c)} fois")

    # LE CONTRÔLE NÉGATIF : un drapeau accéléré ABSENT force le repli
    force = dispatch({d: False for d in DRAPEAUX})
    print(f"  [negatif] tous les drapeaux absents → {force[0]} "
          f"({'OUI' if force[0] == 'REPLI-SCELLE' else 'ROUGE'})")
    return 0 if (tous and force[0] == "REPLI-SCELLE") else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--autotest", action="store_true")
    ap.add_argument("--registre", default=None)
    args = ap.parse_args()
    rc = autotest()
    if args.registre:
        reels = drapeaux_reels()
        with open(args.registre, "w", encoding="utf-8") as f:
            json.dump({"schema": "TRIADE-CPUID-DISPATCH-v1", "drapeaux": reels,
                       "chemin": dispatch(reels)[0] if reels else "REPLI-SCELLE",
                       "controle_32": "32/32" if rc == 0 else "ECART"},
                      f, ensure_ascii=False, indent=2)
    return rc


if __name__ == "__main__":
    sys.exit(main())
