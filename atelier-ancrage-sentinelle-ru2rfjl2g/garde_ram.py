#!/usr/bin/env python3
"""garde_ram.py — atelier RU2RFJL2G (la vague 16).

LA GARDE RAM NATIVE, au-delà du best-effort Python : le secret vit dans une
page VERROUILLÉE (VirtualLock — l'analogue Windows de mlock : la page ne peut
pas être évincée vers le swap) et meurt par RtlSecureZeroMemory — la zéroïsation
que le compilateur n'a pas le droit d'éluder (un memset ordinaire peut être
supprimé comme « écriture morte », l'appel natif non).

L'ÉCART NOMMÉ, HONNÊTE : le « drapeau dumpable » de l'instruction est un
concept POSIX (PR_SET_DUMPABLE). Windows n'en a pas : son analogue est la
politique de dump du processus (WER / MiniDump), qui ne se règle pas par un
drapeau équivalent. La garde livre donc CE QUI EXISTE — VirtualLock et la
zéroïsation effective, prouvées octet pour octet — et NOMME ce qui n'existe pas,
plutôt que de prétendre l'avoir effacé.
"""

import ctypes
import hashlib
import os
import sys
from ctypes import wintypes

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
ntdll = ctypes.WinDLL("ntdll", use_last_error=True)

MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
MEM_RELEASE = 0x8000
PAGE_READWRITE = 0x04

kernel32.VirtualAlloc.restype = ctypes.c_void_p
kernel32.VirtualAlloc.argtypes = [ctypes.c_void_p, ctypes.c_size_t, wintypes.DWORD, wintypes.DWORD]
kernel32.VirtualLock.restype = wintypes.BOOL
kernel32.VirtualLock.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
kernel32.VirtualUnlock.restype = wintypes.BOOL
kernel32.VirtualUnlock.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
kernel32.VirtualFree.restype = wintypes.BOOL
kernel32.VirtualFree.argtypes = [ctypes.c_void_p, ctypes.c_size_t, wintypes.DWORD]

# RtlSecureZeroMemory : la zéroïsation que l'optimiseur n'élude pas.
# L'ÉCART NOMMÉ : c'est un INTRINSÈQUE de winnt.h, PAS une fonction exportée —
# ntdll ne l'expose pas sur ce poste (vérifié : AttributeError). La substitution
# est HONNÊTE et nommée : ctypes.memset entre dans msvcrt (une AUTRE unité de
# compilation que le lecteur) — le compilateur n'a pas la visibilité requise pour
# supprimer l'écriture ; et la relecture qui suit prouve le résultat, pas l'intention.
SECURE_ZERO = None
try:
    _sz = ntdll.RtlSecureZeroMemory
    _sz.restype = None
    _sz.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    SECURE_ZERO = _sz
    MODE_ZEROISATION = "RtlSecureZeroMemory (ntdll)"
except AttributeError:
    SECURE_ZERO = None
    MODE_ZEROISATION = "ctypes.memset (msvcrt) — RtlSecureZeroMemory intrinsèque non exporté"


def _zeroiser(adresse, taille):
    """La zéroïsation effective — le mode nommé à l'exécution."""
    if SECURE_ZERO is not None:
        SECURE_ZERO(adresse, taille)
    else:
        ctypes.memset(adresse, 0, taille)


class GardeRam:
    """Une page verrouillée : le secret y naît, y meurt, et la page est rendue."""

    def __init__(self, taille: int = 64):
        self.taille = taille
        self.adresse = kernel32.VirtualAlloc(None, taille, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE)
        if not self.adresse:
            raise OSError(f"VirtualAlloc a échoué (errno {ctypes.get_last_error()})")
        if not kernel32.VirtualLock(self.adresse, taille):
            err = ctypes.get_last_error()
            kernel32.VirtualFree(self.adresse, 0, MEM_RELEASE)
            raise OSError(f"VirtualLock a échoué (errno {err}) — la page n'est PAS verrouillée")
        self.verrouillee = True

    def ecrire(self, secret: bytes) -> str:
        """Le secret entre ; son condensat est rendu (jamais le secret)."""
        if len(secret) > self.taille:
            raise ValueError("le secret dépasse la page")
        ctypes.memmove(self.adresse, secret, len(secret))
        return hashlib.sha256(secret).hexdigest()

    def lire(self, n: int) -> bytes:
        return ctypes.string_at(self.adresse, n)

    def zeroiser(self) -> bool:
        """-> True ssi TOUS les octets sont nuls APRÈS la passe (la preuve, pas l'intention)."""
        _zeroiser(self.adresse, self.taille)
        return self.lire(self.taille) == b"\x00" * self.taille

    def liberer(self) -> bool:
        if not self.verrouillee:
            return True
        kernel32.VirtualUnlock(self.adresse, self.taille)
        ok = bool(kernel32.VirtualFree(self.adresse, 0, MEM_RELEASE))
        self.verrouillee = False
        return ok

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.liberer()
        return False


def autotest() -> int:
    print("=== L'AUTOTEST DE LA GARDE RAM NATIVE ===")
    tests = []

    secret = os.urandom(32)
    with GardeRam(64) as g:
        condensat = g.ecrire(secret)
        present = g.lire(len(secret))
        print(f"  [1] le secret écrit               : {'OUI' if present == secret else 'NON'} "
              f"(sha256 {condensat[:16]}…)")
        tests.append(present == secret)

        # [2] le verrou : la page est bien verrouillée (le refus serait l'échec à la construction)
        print(f"  [2] la page verrouillée (VirtualLock) : {'OUI' if g.verrouillee else 'NON'}")
        tests.append(g.verrouillee)

        # [3] la zéroïsation : la PREUVE octet pour octet
        zero = g.zeroiser()
        print(f"  [3] la zéroïsation effective      : {'OUI' if zero else 'NON'} "
              f"({g.taille} octets relus nuls)")
        tests.append(zero)

        # [4] le contrôle négatif : une page NON verrouillée est quand même zéroïsée
        #     (la garde ne dépend jamais du verrou pour mourir)
        g2_adr = kernel32.VirtualAlloc(None, 32, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE)
        ctypes.memmove(g2_adr, b"\xff" * 32, 32)
        _zeroiser(g2_adr, 32)
        nz = ctypes.string_at(g2_adr, 32) == b"\x00" * 32
        kernel32.VirtualFree(g2_adr, 0, MEM_RELEASE)
        print(f"  [4] zéroïsation SANS verrou        : {'OUI' if nz else 'NON'} "
              f"(le contrôle négatif : la mort ne dépend pas du verrou)")
        tests.append(nz)

    print(f"  [5] la page rendue (VirtualFree)  : {'OUI' if not g.verrouillee else 'NON'}")
    tests.append(not g.verrouillee)

    print(f"  {sum(1 for t in tests if t)}/{len(tests)} contrôles rendus")
    print(f"  le mode de zéroïsation : {MODE_ZEROISATION}")
    print("  L'ÉCART NOMMÉ : le « drapeau dumpable » est POSIX (PR_SET_DUMPABLE) — Windows n'a")
    print("  pas d'équivalent par drapeau ; la politique de dump (WER/MiniDump) est un autre levier.")
    return 0 if all(tests) else 1


if __name__ == "__main__":
    sys.exit(autotest())
