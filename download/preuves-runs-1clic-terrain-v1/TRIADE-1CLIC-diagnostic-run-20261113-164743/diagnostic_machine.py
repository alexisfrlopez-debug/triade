#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""diagnostic_machine.py — LE DIAGNOSTIC D'APTITUDE DE LA MACHINE (l'édition
MISE À JOUR du paquet multimachines, 12/11/2026 — la commande du développeur :
« fais un kit mis à jour avec ce qu'il reste à faire ou des corrections si
nécessaires, ou éventuellement rajouter des tests si tu trouve ça pertinent »).

UN SEUL GESTE : double-cliquez DIAGNOSTIC-MACHINE.bat (il lance ce script).

Le diagnostic CONSTATE — il ne mesure rien et ne fabrique aucun chiffre :
  — la machine nommée : l'OS, l'architecture, le processeur ;
  — le silicium lu par CPUID sur x86-64 (fabricant, famille, modèle, pas —
    la MÊME lecture que le kit-1 shani au geste A : CPUID feuille 7,
    EBX bit 29 pour SHA-NI), recoupée sur Linux par la seconde voix de
    /proc/cpuinfo (vendor_id et le flag sha_ni) ;
  — ce qui vit : Python (et ses 64 bits), les compilateurs (cl/gcc/clang),
    WSL2 (wsl.exe) ;
  — LE VERDICT : quels kits de CE paquet sont vivables SUR CETTE MACHINE,
    et le renvoi à CE-QUI-RESTE-A-FAIRE.txt (l'état du projet au 12/11
    soir — quels kits restent à vivre, le geste B, D204).

Le témoin naît dans diagnostic-machine.txt (renvoyez-le au coffre /test
avec vos preuves si vous le voulez — D206 : QUI a diagnostiqué, QUOI fut
lu). Sur une machine qui n'est pas Windows x86-64, le script vit quand
même et dit honnêtement ce qu'il peut lire (le laboratoire l'éprouve sur
son hôte Linux x86-64 ; le téléphone vit par SON kit, kit-constat-arm).

Code de sortie : 0 = le diagnostic a vécu (l'état rendu EST le résultat) ;
2 = erreur interne nommée.
"""

import ctypes
import os
import platform
import shutil
import struct
import sys

SORTIE = "diagnostic-machine.txt"
LIGNES = []


def dit(texte=""):
    print(texte)
    LIGNES.append(texte)


# --- LE SILICIUM PAR CPUID (x86-64) -----------------------------------------
# Le stub : deux conventions d'appel, un seul corps — eax/ecx reçoivent la
# feuille et la sous-feuille, cpuid s'exécute, les quatre registres rendus
# sont posés au pointeur de sortie. Jamais exécuté comme « mesure » : c'est
# une LECTURE d'identité, la même que le kit-1 vit au T0.
#   win64 : args (rcx, rdx, r8) ; sysv : args (rdi, rsi, rdx)
STUB_WIN64 = bytes([
    0x4D, 0x89, 0xC2,             # mov r10, r8        ; r10 = sortie
    0x8B, 0xC1,                   # mov eax, ecx       ; eax = feuille
    0x8B, 0xCA,                   # mov ecx, edx       ; ecx = sous-feuille
    0x0F, 0xA2,                   # cpuid
    0x41, 0x89, 0x02,             # mov [r10],    eax
    0x41, 0x89, 0x5A, 0x04,       # mov [r10+4],  ebx
    0x41, 0x89, 0x4A, 0x08,       # mov [r10+8],  ecx
    0x41, 0x89, 0x52, 0x0C,       # mov [r10+12], edx
    0xC3])                        # ret
STUB_SYSV = bytes([
    0x49, 0x89, 0xD2,             # mov r10, rdx       ; r10 = sortie
    0x8B, 0xC7,                   # mov eax, edi       ; eax = feuille
    0x8B, 0xCE,                   # mov ecx, esi       ; ecx = sous-feuille
    0x0F, 0xA2,                   # cpuid
    0x41, 0x89, 0x02,
    0x41, 0x89, 0x5A, 0x04,
    0x41, 0x89, 0x4A, 0x08,
    0x41, 0x89, 0x52, 0x0C,
    0xC3])


def _allouer_exec(len_stub):
    """Une page exécutable : VirtualAlloc sous Windows, mmap sous POSIX."""
    if sys.platform == "win32":
        k32 = ctypes.windll.kernel32
        k32.VirtualAlloc.restype = ctypes.c_void_p
        k32.VirtualAlloc.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                     ctypes.c_uint32, ctypes.c_uint32]
        p = k32.VirtualAlloc(None, max(len_stub, 4096), 0x1000, 0x40)
        if not p:
            raise OSError("VirtualAlloc a refuse")
        return ctypes.c_void_p(p)
    libc = ctypes.CDLL(None, use_errno=True)
    libc.mmap.restype = ctypes.c_void_p
    libc.mmap.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int,
                          ctypes.c_int, ctypes.c_int, ctypes.c_long]
    p = libc.mmap(None, max(len_stub, 4096), 7, 0x22, -1, 0)
    if p in (None, ctypes.c_void_p(-1).value, 2 ** 64 - 1):
        raise OSError("mmap a refuse")
    return ctypes.c_void_p(p)


def lire_cpuid():
    """Rend {fabricant, famille, modele, pas, shani} ou lève — x86-64 seul."""
    stub = STUB_WIN64 if sys.platform == "win32" else STUB_SYSV
    page = _allouer_exec(len(stub))
    ctypes.memmove(page, stub, len(stub))
    f = ctypes.CFUNCTYPE(None, ctypes.c_uint32, ctypes.c_uint32,
                         ctypes.c_void_p)(page.value)
    sortie = ctypes.create_string_buffer(16)

    def cpuid(feuille, sous=0):
        f(feuille, sous, sortie)
        e, b, c, d = struct.unpack("<4I", sortie.raw)
        return e, b, c, d

    eax0, ebx0, ecx0, edx0 = cpuid(0)
    fabricant = struct.pack("<3I", ebx0, edx0, ecx0).decode("ascii", "replace")
    eax1, _, _, _ = cpuid(1)
    pas = eax1 & 0xF
    modele = (eax1 >> 4) & 0xF
    famille = (eax1 >> 8) & 0xF
    if famille == 0xF:
        famille += (eax1 >> 20) & 0xFF
    if famille in (0x6, 0xF):
        modele += ((eax1 >> 16) & 0xF) << 4
    shani = None
    if eax0 >= 7:
        _, ebx7, _, _ = cpuid(7, 0)
        shani = bool(ebx7 & (1 << 29))
    return {"fabricant": fabricant, "famille": famille, "modele": modele,
            "pas": pas, "shani": shani}


def lire_cpuinfo_linux():
    """La seconde voix sur Linux : /proc/cpuinfo (vendor_id, model name,
    les flags sha_ni / sha2). Rend {} si absent."""
    infos = {"flags": set()}
    try:
        with open("/proc/cpuinfo", encoding="utf-8", errors="replace") as f:
            for ligne in f:
                if ":" not in ligne:
                    continue
                cle, val = ligne.split(":", 1)
                cle, val = cle.strip(), val.strip()
                if cle == "vendor_id":
                    infos["vendor_id"] = val
                elif cle == "model name":
                    infos["modele_nom"] = val
                elif cle == "Flags" or cle == "flags":
                    infos["flags"] = set(val.split())
                if "modele_nom" in infos and "flags" in infos and \
                        "vendor_id" in infos:
                    break
    except OSError:
        return {}
    return infos


def main():
    windows = sys.platform == "win32"
    arch = platform.machine() or "?"
    dit("===================================================================")
    dit(" LE DIAGNOSTIC DE LA MACHINE — le paquet multimachines MISE À JOUR")
    dit(" Il constate : la machine, le silicium, ce qui vit, quels kits y")
    dit(" sont vivables. Il ne mesure rien, ne fabrique aucun chiffre.")
    dit("===================================================================")
    dit()

    # 1. LA MACHINE NOMMÉE (D206 : QUI a diagnostiqué)
    dit("[machine] l'OS      : %s" % (
        platform.platform(terse=True) or sys.platform))
    dit("[machine] l'arche   : %s%s" % (
        arch, "  (Python %s bits)" % (struct.calcsize("P") * 8)))
    ident = os.environ.get("PROCESSOR_IDENTIFIER", "")
    cpuinfo = {} if windows else lire_cpuinfo_linux()
    if windows and ident:
        dit("[machine] le CPU   : %s (PROCESSOR_IDENTIFIER)" % ident)
    elif "modele_nom" in cpuinfo:
        dit("[machine] le CPU   : %s (/proc/cpuinfo)" % cpuinfo["modele_nom"])
    else:
        dit("[machine] le CPU   : (non lu — nommé ci-dessous par CPUID si possible)")

    # 2. LE SILICIUM PAR CPUID (la lecture du kit-1, la double voix sur Linux)
    silicium = None
    if arch in ("x86_64", "AMD64", "x86", "i686", "i386"):
        try:
            silicium = lire_cpuid()
            dit("[silicium] CPUID   : « %s » · famille %d · modèle %d · pas %d"
                % (silicium["fabricant"], silicium["famille"],
                   silicium["modele"], silicium["pas"]))
            if silicium["shani"] is None:
                dit("[silicium] SHA-NI  : INCONNU (feuille 7 absente de ce"
                    " silicium — le kit-1 le nommera au T0)")
            else:
                dit("[silicium] SHA-NI  : %s  (CPUID feuille 7, EBX bit 29)"
                    % ("PRÉSENT" if silicium["shani"] else "ABSENT"))
        except Exception as e:                      # noqa: BLE001 — nommé
            dit("[silicium] CPUID   : ILLISIBLE — %s" % e)
    else:
        dit("[silicium] l'arche n'est pas x86 : le test CPUID x86-64 ne"
            " s'applique pas — sur le téléphone, le kit-constat-arm lit le"
            " silicium par ses propres canaux.")
    if cpuinfo:
        if "vendor_id" in cpuinfo:
            dit("[silicium] 2e voix : /proc/cpuinfo vendor_id « %s »%s"
                % (cpuinfo["vendor_id"],
                   "  == CPUID (recoupées)" if silicium and
                   silicium["fabricant"] == cpuinfo["vendor_id"]
                   else "  (à recouper avec CPUID)"))
        flags = cpuinfo.get("flags", set())
        if arch in ("x86_64", "AMD64"):
            if "sha_ni" in flags:
                dit("[silicium] 2e voix : le flag sha_ni VIT dans"
                    " /proc/cpuinfo%s" % (
                        "  == CPUID (recoupées)" if silicium and
                        silicium["shani"] else ""))
            elif silicium and silicium["shani"] is False:
                dit("[silicium] 2e voix : aucun flag sha_ni dans"
                    " /proc/cpuinfo  == CPUID (recoupées)")
        if "sha2" in flags:
            dit("[silicium] 2e voix : le flag sha2 (ARM) vit dans"
                " /proc/cpuinfo")

    # 3. CE QUI VIT
    py = "Python %s" % platform.python_version()
    dit("[outils]   Python   : %s, %s bits%s" % (
        platform.python_version(), struct.calcsize("P") * 8,
        "  (exigé 64 bits par le kit-3)"
        if struct.calcsize("P") * 8 != 64 else "  (64 bits : le kit-3 y vit)"))
    compils = [c for c in ("cl", "gcc", "clang") if shutil.which(c)]
    dit("[outils]   compil.  : %s" % (" · ".join(compils) if compils
        else "AUCUN de cl/gcc/clang — les exe précompilés du kit-2 courent"))
    wsl = shutil.which("wsl.exe") if windows else None
    if windows:
        dit("[outils]   WSL2     : %s" % ("wsl.exe VU — les voies QEMU"
            " partent du menu" if wsl else
            "wsl.exe ABSENT — les voies QEMU exigent WSL2 (wsl --install)"))
    elif shutil.which("qemu-riscv64") or shutil.which("qemu-x86_64"):
        dit("[outils]   QEMU     : VU dans le PATH (machine Linux — les"
            " voies vivent en bash direct, sans WSL2)")

    # 4. LE VERDICT : quels kits vivent ICI
    dit()
    dit("===================================================================")
    dit(" LE VERDICT (les kits vivables SUR CETTE MACHINE — l'état complet")
    dit(" du projet vit dans CE-QUI-RESTE-A-FAIRE.txt)")
    dit("===================================================================")
    if windows:
        dit(" kit-1 shani     : %s" % (
            "VIVABLE — SHA-NI PRÉSENT : c'est LA machine du GESTE B"
            " (la mesure avant/après sur vrai SHA-NI)"
            if silicium and silicium["shani"] else
            "REFUS ATTENDU — SHA-NI absent : le kit refusera de lui-même au"
            " T0 (un RÉSULTAT, pas une panne — ALEKPC l'a déjà vécu deux"
            " fois, le rejeu n'est pas requis)"))
        dit(" kit-2 dudect    : VIVABLE — tout Windows x86-64 y vit (aucun"
            " Python, aucun compilateur requis : les exe précompilés"
            " courent). C'est LA MESURE JAMAIS ENCORE COURUE du paquet.")
        dit(" kit-3 loupe     : %s" % (
            "VIVABLE — Python 64 bits (déjà vécu VERT sur la machine"
            " Windows 11 : le rejeu n'est pas requis)"
            if struct.calcsize("P") * 8 == 64 else
            "Python 32 bits VU : le kit-3 exige Python 64 BITS"))
        dit(" voies QEMU      : %s" % (
            "VIVABLES par le menu (WSL2 vu)" if wsl else
            "WSL2 ABSENT — installez-le ou lisez qemu-wsl2\\LISEZMOI-qemu.txt"))
        dit(" kit-constat-arm : cette machine n'est pas le téléphone — le"
            " kit vit sur Android + Termux (telephone-arm\\kit-constat-arm\\)")
    elif sys.platform.startswith("linux"):
        dit(" cette machine est LINUX : les kits Windows du paquet n'y"
            " vivent pas (les exe livrés sont PE32+ x86-64).")
        dit(" les voies QEMU y vivent en bash DIRECT (lanceur-voie1-m7d.sh :"
            " le qemu-riscv64 STATIQUE est embarqué dans le paquet).")
        dit(" le téléphone vit par SON kit : telephone-arm/kit-constat-arm/")
        dit(" (le présent diagnostic fut éprouvé au laboratoire sur un hôte"
            " Linux x86-64 — cette voix même.)")
    else:
        dit(" cette machine n'est NI Windows NI Linux : le paquet n'y"
            " prévoit rien — chaque kit dit lui-même son refus, nommé.")
    dit()
    dit(" A VOTRE MAIN (inchangé) : la signature des témoins, l'état"
        " EFFECTIF du turbo (kit-2), le témoin vitrine (kit-3), le renvoi")
    dit(" des preuves au coffre /test (dossier Drive « Triade » → « test »).")
    dit("===================================================================")

    with open(SORTIE, "w", encoding="utf-8") as f:
        f.write("\n".join(LIGNES) + "\n")
    print()
    print("[témoin] le diagnostic est écrit : %s" % SORTIE)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as e:                          # noqa: BLE001 — nommé
        print("[ERREUR NOMMÉE] le diagnostic n'a pas pu vivre : %r" % e)
        sys.exit(2)
