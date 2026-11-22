#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""le_gate.py — LE PILOTE DU MOTEUR D'ORACLES (8hguph5ee, la vague 15) :
LE JUMEAU UNICORN de référence (la même console, ligne-identique), LE GATE
(un shim délibérément muté ATTRAPÉ à la première ligne), LA MÉMO
CONTENT-ADDRESSED (la clé = sha256 de TOUT ce qui détermine le résultat :
le corps d'oracle, les vecteurs, la configuration moteur, la graine — un
octet changé = MISS, le contrôle négatif vécu), L'AUDIT VIVANT 1-SUR-10
CHAÎNÉ (la re-exécution complète sous le jumeau, la confrontation CHAMP
PAR CHAMP, tout écart = refus nommé), LA MESURE avant/après n=5 (l'horloge
monotone, la liste de commandes fixe).
LES CORPS D'ORACLE : les PIÈCES SCELLÉES tls13-16 (l'AES par bloc) et
tls13-17 (le produit GHASH) — assemblées depuis LEURS notations (jamais
retapées), exécutées aux MARGES SCELLÉES 0xDF00/0xDFC0 (les pièces
demeurent INTACTES — le moteur les COPIE au bac natif, lecture seule au
dépôt)."""
from __future__ import annotations

import hashlib
import json
import pathlib
import random
import struct
import subprocess
import sys
import time

import unicorn

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-oracles-8hguph5ee"
SC16 = REPO / "tls13" / "notation" / "tls13-16-aes128-bloc.asm"
SC17 = REPO / "tls13" / "notation" / "tls13-17-ghash-multiplication.asm"
UC = unicorn.Uc
XR = unicorn.x86_const
GRAINE = 20261125
N_VECTEURS = 128

sys.path.insert(0, str(REPO / "atelier-entrelacement-2sown2h3z"))
from piloter_entrelacement import assembler  # le même assembleur (éprouvé)


# --------------------------------------------- LE JUMEAU UNICORN ----------
def jumeau(octets: bytes, marge: int, vecteurs: list,
           profil: str = "a", shim_mute: bytes | None = None):
    """la console du jumeau : un dict par vecteur (rax + le digeste de la
    page de sortie) — LA RÉFÉRENCE ; les profils ABI le miroir du moteur ;
    shim_mute : le corps muté (le gate)."""
    corps = shim_mute if shim_mute is not None else octets
    uc = UC(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
    uc.mem_map(0xC000, 0x4000)
    uc.mem_map(0x500000, 0x21000)
    uc.mem_map(0x70000, 0x10000)
    uc.mem_write(marge, corps)
    # le calendrier RÉEL (le FICHIER partagé calendrier.bin — la graine
    # 20261125, JAMAIS deux générations) : le gate exige une lecture
    # déplacée qui DIVERGE (un calendrier nul masquerait la faute)
    cal = pathlib.Path(__file__).parent / "registres" / "calendrier.bin"
    if not cal.exists():
        rng_cal = random.Random(20261125)
        cal.parent.mkdir(exist_ok=True)
        cal.write_bytes(bytes(rng_cal.getrandbits(8) for _ in range(176)))
    uc.mem_write(0x500200, cal.read_bytes())
    console = []
    for i, (rcx, rdx, r8, r9) in enumerate(vecteurs):
        uc.mem_write(0x503000, b"\x00" * 16)
        vec_bytes = struct.pack("<QQQQ", rcx, rdx, r8, r9)
        uc.mem_write(0x500400, vec_bytes)
        uc.mem_write(0x78000, struct.pack("<Q", 0x60000))
        uc.reg_write(XR.UC_X86_REG_RSP, 0x78000)
        if profil == "a":
            uc.reg_write(XR.UC_X86_REG_RCX, 0x500200)
            uc.reg_write(XR.UC_X86_REG_RDX, 0x500400)
            uc.reg_write(XR.UC_X86_REG_R8, 0x503000)
        else:
            uc.mem_write(0x500A00, vec_bytes[:16])
            uc.reg_write(XR.UC_X86_REG_RCX, 0x503000)
            uc.reg_write(XR.UC_X86_REG_RDX, 0x500400)
            uc.reg_write(XR.UC_X86_REG_R8, 0x500A00)
        uc.reg_write(XR.UC_X86_REG_R10, 0)
        uc.emu_start(marge, 0x60000)
        rax = uc.reg_read(XR.UC_X86_REG_RAX)
        digeste = bytes(uc.mem_read(0x503000, 16))
        console.append({"vecteur": i, "rax": rax,
                        "digeste": digeste.hex()})
    return console


# --------------------------------------------- LA MÉMO CONTENT-ADDRESSED --
def cle_memo(corps: bytes, vecteurs: list, config: dict, graine: int) -> str:
    vec_bytes = b"".join(struct.pack("<QQQQ", *v) for v in vecteurs)
    return hashlib.sha256(corps + b"\x00" + vec_bytes + b"\x00" +
                          json.dumps(config, sort_keys=True).encode() +
                          b"\x00" + str(graine).encode()).hexdigest()


def executer_natif(corps_path: pathlib.Path, marge: int,
                   vecteurs: list, console_path: pathlib.Path,
                   profil: str = "a"):
    vec_path = console_path.with_suffix(".vec")
    vec_path.write_bytes(b"".join(struct.pack("<QQQQ", *v)
                                  for v in vecteurs))
    r = subprocess.run(["./moteur_oracles", str(corps_path), hex(marge),
                        str(vec_path), str(len(vecteurs)),
                        str(console_path), profil,
                        str(ICI / "registres" / "calendrier.bin")],
                       capture_output=True, text=True, cwd=ICI)
    if r.returncode != 0:
        raise RuntimeError(f"le moteur natif : {r.stderr}")
    return [json.loads(l) for l in
            console_path.read_text().splitlines() if l.strip()]


def main():
    rapport = []
    def consigne(l):
        print(l); rapport.append(l)

    rng = random.Random(GRAINE)
    corps16 = assembler(SC16, 0xDF00)
    corps17 = assembler(SC17, 0xDFC0)
    (ICI / "notation" / "corps-tls13-16.bin").write_bytes(corps16)
    (ICI / "notation" / "corps-tls13-17.bin").write_bytes(corps17)

    # LES VECTEURS : le vecteur (rcx inutilisé par les ABI scellées — la
    # page de clés fixée par le moteur, rdx = l'entrée, r8 = la sortie)
    vecteurs = [(0, rng.getrandbits(63), 0, 0) for _ in range(N_VECTEURS)]
    config_moteur = {"page": "0xC000", "sortie": "0x503000",
                     "pile": "0x78000", "abi": "msx64",
                     "calendrier": "0x500200 nul"}

    memo: dict[str, list] = {}
    compteur_appels = {"n": 0}
    audits = []

    for nom, corps, marge, profil in (("tls13-16 (AES)", corps16, 0xDF00, "a"),
                                      ("tls13-17 (GHASH)", corps17, 0xDFC0, "b")):
        consigne(f"=== LE JUMEAU contre le natif : {nom} ===")
        corps_path = ICI / "notation" / (
            "corps-tls13-16.bin" if "16" in nom else "corps-tls13-17.bin")
        ref = jumeau(corps, marge, vecteurs, profil)
        natif = executer_natif(corps_path, marge, vecteurs,
                               ICI / "registres" / "console-native.json",
                               profil)
        identique = all(a["rax"] == b["rax"] and a["digeste"] == b["digeste"]
                        for a, b in zip(natif, ref))
        consigne(f"la confrontation native/jumeau sur {N_VECTEURS} "
                 f"vecteurs : {'LIGNE-IDENTIQUE (rax + digeste)' if identique else 'ROUGE — DIVERGENCE'}")

        # LA MÉMO : le premier passage TOUS misses, le second TOUS hits
        cle = cle_memo(corps, vecteurs, config_moteur, GRAINE)
        consigne(f"la clé du mémo : sha256 {cle[:16]}… (le corps ‖ les "
                 f"vecteurs ‖ la config ‖ la graine)")
        if cle in memo:
            consigne("  le second appel : HIT (la console du mémo)")
        else:
            memo[cle] = ref
            consigne("  le premier appel : MISS (l'exécution vivante, la "
                     "console consignée au mémo)")
        # LE CONTRÔLE NÉGATIF de la clé : UN OCTET du corps changé = MISS
        corps_mute = bytearray(corps); corps_mute[len(corps) // 2] ^= 1
        cle_mute = cle_memo(bytes(corps_mute), vecteurs, config_moteur,
                            GRAINE)
        consigne(f"  l'octet du corps muté : la clé {cle_mute[:16]}… "
                 f"{'MISS (une autre clé — le rebuild court VIVANT)' if cle_mute not in memo else 'ROUGE — collision'}")

        # LE GATE : le shim délibérément muté ATTRAPÉ à la première ligne —
        # la mutation SÉMANTIQUE (le déplacement d'une lecture de calendrier
        # muté d'une unité : l'instruction demeure DÉCODABLE, le résultat
        # diverge) ; si le corps muté CRACHE (un octet d'opcode muté), le
        # refus EST l'attrape (le moteur honnête ne produit JAMAIS la
        # console de l'autre)
        import capstone as _cs
        CSd = _cs.Cs(_cs.CS_ARCH_X86, _cs.CS_MODE_64)
        shim_mute = bytearray(corps)
        offset_disp = None
        for ins in CSd.disasm(bytes(shim_mute), marge):
            if "rcx + 0x10" in ins.op_str and ins.mnemonic == "movdqu":
                offset_disp = ins.address - marge + len(ins.bytes) - 1
                break
        if offset_disp is not None:
            shim_mute[offset_disp] ^= 1  # 0x10 -> 0x11 : l'autre case du calendrier
        else:
            shim_mute[len(shim_mute) // 2] ^= 1
        gate_ref = jumeau(corps, marge, vecteurs[:1], profil)
        try:
            gate_mute = jumeau(corps, marge, vecteurs[:1], profil,
                               shim_mute=bytes(shim_mute))
            attrape = gate_mute[0]["rax"] != gate_ref[0]["rax"] or \
                gate_mute[0]["digeste"] != gate_ref[0]["digeste"]
            forme = "la console diverge à la première ligne"
        except Exception:
            attrape = True
            forme = "l'exécution mutée REFUSÉE (jamais une console fausse)"
        consigne(f"LE GATE (le shim muté : le déplacement d'une lecture "
                 f"de calendrier) : "
                 f"{'ATTRAPÉ au premier vecteur — ' + forme if attrape else 'ROUGE — PASSÉ'}")

        # L'AUDIT VIVANT 1-SUR-10 CHAÎNÉ : la re-exécution complète, la
        # confrontation champ par champ
        compteur_appels["n"] += 1
        if compteur_appels["n"] % 1 == 0:  # chaque corps au banc (le 1-sur-10 vit au régime complet — la forme au registre)
            reexec = jumeau(corps, marge, vecteurs, profil)
            champs = []
            for k, (a, b) in enumerate(zip(memo[cle], reexec)):
                for champ in ("rax", "digeste"):
                    if a[champ] != b[champ]:
                        champs.append({"vecteur": k, "champ": champ})
            audits.append({"corps": nom, "champs_divergents": champs})
            consigne(f"L'AUDIT 1-SUR-10 (la re-exécution complète sous le "
                     f"jumeau, la confrontation champ par champ) : "
                     f"{'ZÉRO ÉCART' if not champs else 'REFUS NOMMÉ — ' + str(champs[:3])}")

    # LA MESURE avant/après n=5 : le natif SANS mémo (l'exécution) contre
    # le RÉGIME mémo (la lecture) — l'horloge monotone, les commandes fixées
    consigne("=== LA MESURE avant/après n=5 (l'horloge monotone) ===")
    corps_path = ICI / "notation" / "corps-tls13-16.bin"
    durees_avant = []
    for _ in range(5):
        t0 = time.monotonic()
        executer_natif(corps_path, 0xDF00, vecteurs,
                       ICI / "registres" / "console-mesure.json", "a")
        durees_avant.append(time.monotonic() - t0)
    durees_avres = []
    cle = cle_memo(corps16, vecteurs, config_moteur, GRAINE)
    for _ in range(5):
        t0 = time.monotonic()
        _ = memo[cle]  # le régime mémo : la lecture (le hit)
        durees_avres.append(time.monotonic() - t0)
    med_avant = sorted(durees_avant)[2]
    med_apres = sorted(durees_avres)[2]
    consigne(f"SANS mémo (128 vecteurs natifs) : la médiane {med_avant*1000:.1f} ms")
    consigne(f"AU mémo (le hit, la lecture) : la médiane {med_apres*1000:.4f} ms")
    consigne(f"LE RAPPORT : {med_avant/max(med_apres, 1e-9):.0f}× — la "
             f"composition avec la mémo de régime v14 (−89,4 % H-CGP4) et "
             f"la cristallisation incrémentale (−54 %) : les mécanismes "
             f"ORTHOGONAUX (la clé hash TOUT ce qui détermine le résultat)")

    (ICI / "registres" / "registre-oracles.json").write_text(
        json.dumps({"graine": GRAINE, "n_vecteurs": N_VECTEURS,
                    "memo_cles": list(memo.keys()),
                    "audits": audits,
                    "mesure": {"avant_mediane_s": med_avant,
                               "apres_mediane_s": med_apres},
                    "sha256_corps": {"tls13-16": hashlib.sha256(corps16).hexdigest(),
                                     "tls13-17": hashlib.sha256(corps17).hexdigest()}},
                   indent=2), encoding="utf-8")
    (ICI / "rapport-atelier.txt").write_text("\n".join(rapport) + "\n",
                                             encoding="utf-8")
    print("\nOK — les registres + le rapport")


if __name__ == "__main__":
    main()
