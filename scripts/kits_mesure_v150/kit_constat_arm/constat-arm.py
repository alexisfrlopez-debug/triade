#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""constat-arm.py — LE CONSTAT AUTO-PORTANT DU TÉLÉPHONE ARM (kit multimachines).

La commande du développeur (12/11/2026) : « un zip avec les kits terrain
que je peux exécuter sur mes machines (téléphone ARM, PC Windows 10 et
11, QEMU ou autre si besoin sur Windows) ». Le téléphone est LE TROISIÈME
SILICIUM de la campagne — et les pièces scellées v0.15.0 sont toutes
x86-64 Windows (loupe.exe, proxy.exe, moteur-shani.bin : PE x86-64,
convention Windows x64, instructions SHA-NI x86). CE kit ne maquille
rien : il CONSTATE ce que le silicium dit de lui-même, il NOMME le refus
des pièces x86-64, et il éprouve l'EXACTITUDE du lecteur Python du
téléphone (le FIPS 180-4 « abc » — un lecteur, JAMAIS une mesure de
temps : aucun protocole pré-enregistré n'existe pour mesurer sur ce
silicium, aucun chiffre ne sera fabriqué).

L'ESPRIT D206 (le verdict auto-portant, vécu au terrain ALEKPC le
12/11 : la machine journalisée à l'ouverture, le constat CPUID au
journal ET au verdict) :
  — la machine NOMMÉE à l'ouverture (nom, système, Python, noyau) ;
  — le silicium LU par ses propres canaux (/proc/cpuinfo, getprop) ;
  — le refus des pièces x86-64 NOMMÉ (les empreintes citées) ;
  — l'échec éventuel NOMMÉ, jamais muet ;
  — le verdict AUTO-PORTANT : tout ce qu'il affirme vit dans SON journal.

Les sorties (le réceptacle ./preuves-constat-arm/) :
  constat-arm-journal.log   le run entier, ligne par ligne ;
  constat-arm-verdict.txt   le verdict auto-portant, à dater et signer.

Codes de sortie : 0 = VERT (le constat complet vécu) ;
                  3 = ÉCHEC NOMMÉ (identité illisible ou lecteur faux).

Aucun réseau. Aucun droit particulier. Python SEUL (stdlib).
Éprouvé au laboratoire (mécanique) sur un hôte Linux x86-64 — où le
script a constaté HONNÊTEMENT « ceci n'est pas un téléphone ARM » sans
faillir : le même geste sur le téléphone constatera son monde à lui.
"""

import datetime
import hashlib
import os
import platform
import shutil
import subprocess
import sys

DEST = "preuves-constat-arm"

# ---- les pièces scellées v0.15.0 (les empreintes CITÉES, jamais mesurées) ----
PIECES_X86 = [
    ("loupe.exe 0.1.1 (l'application née de TRIADE)",
     "c111510535767a40b0122d4e42261c9d8e1ec10d94d95ef666fd76ceb93e61d1"),
    ("proxy-image.bin (l'image mémoire étendue de proxy.exe 1.0.0, "
     "scellé 446279f3…)",
     "0782d7e20d0bd4a268e6ec7ed0dc1453a0f42d7e72b784c2acc9ed423a885dff"),
    ("moteur-shani.bin (le moteur SHA-NI — sha256rnds2/msg1/msg2, x86)",
     "761ab194d88d527c653111a41324b0bb3e9247b1c56ba8dc9fedeeccbe04bcec"),
]

# ---- les vecteurs FIPS 180-4 (le lecteur, pas la mesure) ----
FIPS_ABC = {
    "sha256": ("ba7816bf8f01cfea414140de5dae2223"
               "b00361a396177a9cb410ff61f20015ad"),
    "sha512": ("ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64"
               "b55d39a2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2"
               "a9ac94fa54ca49f"),
}

# ---- la carte des cœurs (le BRUT est la vérité ; le nom est une commodité) ----
IMPLEMENTERS = {
    0x41: "ARM", 0x42: "Broadcom", 0x43: "Cavium", 0x44: "DEC",
    0x46: "Fujitsu", 0x48: "HiSilicon", 0x4e: "NVIDIA", 0x50: "APM",
    0x51: "Qualcomm", 0x53: "Samsung", 0x56: "Marvell", 0x61: "Apple",
    0x66: "Faraday", 0x69: "Intel", 0x70: "Phytium", 0xc0: "Ampere",
}
CORES = {
    (0x41, 0xd03): "Cortex-A53", (0x41, 0xd04): "Cortex-A35",
    (0x41, 0xd05): "Cortex-A55", (0x41, 0xd07): "Cortex-A57",
    (0x41, 0xd08): "Cortex-A72", (0x41, 0xd09): "Cortex-A73",
    (0x41, 0xd0a): "Cortex-A75", (0x41, 0xd0b): "Cortex-A76",
    (0x41, 0xd0c): "Neoverse-N1", (0x41, 0xd0d): "Neoverse-V1",
    (0x41, 0xd40): "Neoverse-V1", (0x41, 0xd41): "Cortex-A78",
    (0x41, 0xd44): "Cortex-X1",  (0x41, 0xd46): "Cortex-A510",
    (0x41, 0xd47): "Cortex-A710", (0x41, 0xd48): "Cortex-X2",
    (0x41, 0xd4d): "Cortex-A715", (0x41, 0xd4e): "Cortex-X3",
    (0x41, 0xd80): "Cortex-A76AE", (0x41, 0xd81): "Cortex-A77",
    (0x41, 0xd82): "Cortex-A78C", (0x41, 0xd84): "Neoverse-V2",
    (0x41, 0xd85): "Cortex-X4",  (0x41, 0xd87): "Cortex-A720",
    (0x41, 0xd88): "Cortex-X925",
    (0x51, 0x800): "Kryo 2xx Gold (A73)", (0x51, 0x801): "Kryo 2xx Silver (A53)",
    (0x51, 0x802): "Kryo 3xx Gold (A75)", (0x51, 0x803): "Kryo 3xx Silver (A55)",
    (0x51, 0x804): "Kryo 4xx Gold (A76)", (0x51, 0x805): "Kryo 4xx Silver (A55)",
    (0x53, 0x001): "Mongoose M1/M2", (0x53, 0x002): "Meerkat M3",
    (0x53, 0x003): "Mongoose M4", (0x53, 0x004): "Mongoose M5",
    (0x48, 0xd01): "TaiShan-v110 (Kunpeng 920)",
    (0x4e, 0x003): "Carmel",
}

# ---- la famille cryptographique ARMv8 (les drapeaux /proc/cpuinfo) ----
CRYPTO_ARM = [
    ("aes",   "FEAT_AES (AESD/AESE — les instructions AES)"),
    ("pmull", "FEAT_PMULL (la multiplication GF(2^m), mode 64)"),
    ("sha1",  "FEAT_SHA1 (SHA1C/SAD — la famille SHA-1)"),
    ("sha2",  "FEAT_SHA256 (SHA256H/SHA256H2 — la famille SHA-256)"),
    ("sha512", "FEAT_SHA512 (SHA512H — la famille SHA-512)"),
    ("sha3",  "FEAT_SHA3 (EOR3/RAX1/XAR/BCAX)"),
    ("sm3",   "FEAT_SM3 (SM3E/SM3SS1 — le standard chinois)"),
    ("sm4",   "FEAT_SM4 (SM4E/SM4EKEY)"),
    ("crc32", "FEAT_CRC32"),
    ("atomics", "FEAT_LSE (les atomiques)"),
]

_journal = None


def journal(ligne):
    print(f"[journal] {ligne}")
    if _journal is not None:
        _journal.write(
            f"{datetime.datetime.now().isoformat(timespec='seconds')} {ligne}\n")
        _journal.flush()


def lire_getprop(nom):
    """Lit une propriété Android par getprop (absent → None, jamais muet)."""
    exe = shutil.which("getprop") or "/system/bin/getprop"
    if not os.path.exists(exe):
        return None
    try:
        r = subprocess.run([exe, nom], capture_output=True, timeout=10)
        v = r.stdout.decode("utf-8", "replace").strip()
        return v or None
    except Exception as e:                     # noqa: BLE001 — le refus nommé
        return f"<getprop refusé : {type(e).__name__}>"


def lire_cpuinfo():
    """Parse /proc/cpuinfo (ARM64 ou non). Retour (cœurs, features, ok)."""
    try:
        with open("/proc/cpuinfo", "r", encoding="utf-8", errors="replace") as f:
            texte = f.read()
    except OSError as e:
        return None, None, f"</proc/cpuinfo illisible : {type(e).__name__}>"
    coeurs, features = [], set()
    bloc_courant = {}
    for ligne in texte.splitlines():
        if not ligne.strip():
            if bloc_courant:
                coeurs.append(bloc_courant)
                bloc_courant = {}
            continue
        if ":" not in ligne:
            continue
        cle, val = (x.strip() for x in ligne.split(":", 1))
        bloc_courant[cle] = val
        if cle == "Features":
            features.update(val.lower().split())
    if bloc_courant:
        coeurs.append(bloc_courant)
    return coeurs, features, True


def hexint(s):
    try:
        return int(s, 16)
    except (ValueError, TypeError):
        return None


def main():
    global _journal
    os.makedirs(DEST, exist_ok=True)
    _journal = open(os.path.join(DEST, "constat-arm-journal.log"),
                    "w", encoding="utf-8")
    verdict_lignes = []
    echecs = []

    def verdict(l):
        verdict_lignes.append(l)

    journal("=== constat-arm.py — LE CONSTAT DU TROISIÈME SILICIUM "
            "(kit multimachines, 12/11/2026) ===")
    est_arm = platform.machine().lower() in ("aarch64", "armv8l",
                                             "armv7l", "arm")

    # ---- T0 LA MACHINE À L'OUVERTURE (le geste D206) ----
    try:
        uname = " ".join(os.uname())
    except AttributeError:
        uname = platform.platform()
    machine = platform.node() or "<sans-nom>"
    journal(f"T0.machine — {machine} · {platform.machine()} · "
            f"{sys.version.split()[0]} · {uname}")
    termux = "com.termux" in (os.environ.get("PREFIX", "") +
                              os.environ.get("PATH", ""))
    if termux:
        journal("T0.environnement — Termux constaté (le PREFIX du PATH)")
    verdict(f"machine : {machine} · {platform.machine()} · "
            f"Python {sys.version.split()[0]}")
    verdict(f"système : {uname}")
    if termux:
        verdict("environnement : Termux")

    # ---- T1 LE SILICIUM PAR SES PROPRES CANAUX ----
    journal("T1.silicium — lecture de ce que la machine dit d'elle-même")
    coeurs, features, cpuinfo_brut = lire_cpuinfo()
    ligne_silicium = None
    if coeurs is None:
        journal(f"T1.cpuinfo — REFUSÉ : {cpuinfo_brut}")
        echecs.append(f"T1.cpuinfo — {cpuinfo_brut}")
    else:
        vus = []
        for c in coeurs:
            impl = hexint(c.get("CPU implementer", ""))
            part = hexint(c.get("CPU part", ""))
            nom_impl = IMPLEMENTERS.get(impl, "?")
            nom_coeur = CORES.get((impl, part),
                                  f"part {c.get('CPU part', '?')}")
            if not vus or vus[-1] != (nom_impl, nom_coeur):
                vus.append((nom_impl, nom_coeur))
        desc = " + ".join(f"{a} {b}" for a, b in vus) or "cœurs non nommés"
        rev = coeurs[0].get("revision", "?")
        ligne_silicium = f"{desc} · révision {rev}"
        journal(f"T1.cpuinfo — {len(coeurs)} cœur(x) : {ligne_silicium}")
        if features:
            crypto = [d for d, _ in CRYPTO_ARM if d in features]
            journal("T1.crypto — extensions cryptographiques ARMv8 lues aux "
                    "Features : " + (", ".join(crypto) if crypto
                                     else "AUCUNE de la liste"))
        else:
            journal("T1.crypto — pas de ligne Features lisible "
                    "(constaté tel quel)")
        if not est_arm:
            journal("T1.isa — CECI N'EST PAS UN TÉLÉPHONE ARM : "
                    f"platform.machine() = {platform.machine()} — le constat "
                    "continue, le monde x86-64 se constate de même")

    props = ["ro.product.manufacturer", "ro.product.model", "ro.soc.model",
             "ro.board.platform", "ro.build.version.release",
             "ro.product.cpu.abilist", "ro.kernel.qemu"]
    getprop_lu = False
    for p in props:
        v = lire_getprop(p)
        if v is not None:
            getprop_lu = True
            journal(f"T1.getprop {p} = {v}")
    if not getprop_lu:
        journal("T1.getprop — absent (ce n'est pas Android, ou getprop "
                "inaccessible — constaté tel quel)")

    if ligne_silicium:
        verdict(f"silicium : {ligne_silicium}")
    identite_lue = bool(ligne_silicium) or getprop_lu
    if not identite_lue:
        echecs.append("T1 — AUCUN canal d'identité n'a vécu "
                      "(cpuinfo illisible ET getprop absent)")

    # ---- T2 LE REFUS NOMMÉ DES PIÈCES x86-64 (le cœur du kit) ----
    journal("T2.refus — les pièces scellées v0.15.0 sont x86-64 Windows :")
    for nom, empreinte in PIECES_X86:
        journal(f"T2.refus — {nom} · sha256 {empreinte[:12]}…")
    if est_arm:
        phrase = ("CE silicium ARM64 n'exécute pas l'ISA x86-64 : ni les PE "
                  "Windows 64 bits, ni la convention Windows x64, ni "
                  "sha256rnds2 — la mesure avant/après SHA-NI n'existe pas "
                  "ici, les kits x86-64 sont REFUSÉS PAR NATURE")
    else:
        phrase = ("la machine hôte n'est pas ARM64 — le constat du kit "
                  "s'éprouve ici sur un monde non-cible, sans rien maquiller")
    journal(f"T2.refus — {phrase}")
    if features and "sha2" in features:
        journal("T2.sha256-arm — l'extension ARM FEAT_SHA256 (SHA256H/"
                "SHA256H2) est PRÉSENTE aux Features : c'est UNE AUTRE "
                "famille d'instructions que la SHA-NI x86 — les deux mondes "
                "se constatent, aucun ne se déguise")
        verdict("le silicium porte FEAT_SHA256 (ARM) — une AUTRE famille "
                "d'instructions que la SHA-NI x86, aucun déguisement")
    verdict(f"le refus : {phrase}")

    # ---- T3 LE LECTEUR PYTHON (l'exactitude, jamais la vitesse) ----
    journal("T3.lecteur — le FIPS 180-4 « abc » par le Python de la machine "
            "(un lecteur, PAS une mesure de temps)")
    for algo, attendu in FIPS_ABC.items():
        rendu = hashlib.new(algo, b"abc").hexdigest()
        ok = rendu == attendu
        journal(f"T3.lecteur {algo}(abc) = {rendu[:16]}… — "
                f"{'EXACT' if ok else 'DIVERGENT'}")
        verdict(f"lecteur {algo} « abc » : {'EXACT' if ok else 'DIVERGENT'}")
        if not ok:
            echecs.append(f"T3.lecteur {algo} — DIVERGENT "
                          f"(rendu {rendu}, attendu {attendu})")

    # ---- LE VERDICT AUTO-PORTANT ----
    vert = not echecs
    entete = [
        "VERDICT CONSTAT-ARM (kit multimachines — le troisième silicium)",
        "=" * 72,
    ]
    if vert:
        entete.append("VERDICT : VERT — LE CONSTAT COMPLET VÉCU : la machine "
                      "nommée à l'ouverture, le silicium lu par ses propres "
                      "canaux, le refus des pièces x86-64 nommé avec ses "
                      "empreintes, le lecteur Python exact")
    else:
        entete.append("VERDICT : ÉCHEC NOMMÉ — " + " ; ".join(echecs))
    entete += [
        "",
        "LA PORTÉE : ce constat ne mesure RIEN (aucun protocole pré-enregistré "
        "n'existe pour ce silicium, aucun chiffre n'est fabriqué) ; il "
        "consigne CE que la machine a dit d'elle-même, CE jour, ces canaux.",
        "signature du geste : à dater et à signer de la main du développeur.",
    ]
    chemin_verdict = os.path.join(DEST, "constat-arm-verdict.txt")
    with open(chemin_verdict, "w", encoding="utf-8") as f:
        f.write("\n".join(entete + verdict_lignes) + "\n")
    _journal.close()
    print(f"\n[constat] verdict : {'VERT' if vert else 'ÉCHEC NOMMÉ'}")
    print(f"[constat] les pièces au réceptacle {DEST}/ : "
          "constat-arm-journal.log, constat-arm-verdict.txt")
    print("[constat] à renvoyer ENTIÈRES au coffre /test "
          "(dossier Drive « Triade » → « test »)")
    return 0 if vert else 3


if __name__ == "__main__":
    sys.exit(main())
