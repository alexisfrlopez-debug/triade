#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""moteur_qemu.py — LE PILOTE DU DOUBLE MOTEUR (le plan § 3 de cq01qv1za).

L'IMAGE EST BÂTIE PAR LE VRAI HARNAIS (harnais_noyau.Emulation — les octets
de l'image QEMU sont CEUX de l'image Unicorn PAR CONSTRUCTION : notations
assemblées par la même chaîne keystone, tables .rdata, héritages EXTRAITS
DES SCELLÉS, l'IAT aux 34 slots du plan). Le lanceur C reçoit l'image, pose
ses shims aux slots IAT, exécute le programme d'opérations et imprime UNE
LIGNE JSON PAR OPÉRATION.

LA RÉFÉRENCE : le MÊME programme exécuté par le harnais Unicorn (TEL QUEL,
D185), sérialisé AU MÊME FORMAT par la présente — la comparaison octet pour
octet des deux flux EST l'échantillon d'audit (divergence=0 exigée).

LE MOTEUR N'EST JAMAIS LE JUGE : les relevés rendus, hashlib demeure le
modèle indépendant côté oracle."""
from __future__ import annotations

import json
import os
import pathlib
import random
import struct
import subprocess
import sys
import tempfile

REPO = pathlib.Path("/tmp/triade-gh")
sys.path.insert(0, str(REPO / "loupe"))
sys.path.insert(0, str(REPO / "atelier-m4-vljfs6pcj"))

import harnais_noyau as HN          # noqa: E402

L = HN.L

# les zones du plan (la source unique : le harnais même)
ZONES = [HN.ZONE_LIBC, HN.ZONE_RDATA, HN.ZONE_IMAGE, HN.ZONE_DATA,
         HN.ZONE_TESTS]
PILE = (HN.ZONE_PILE, HN.TAILLE_PILE)

NOTATION_CAMPAGNE = (REPO / "scripts" / "campagne_d204" / "unite-02-T"
                     / "notation" / "loupe-02-lire.asm")


# ---------------------------------------------------------------------------
# la sérialisation PARTAGÉE — le format exact du lanceur C (imprimer_releve)
# ---------------------------------------------------------------------------

def s_propre(emul, r) -> int:
    return 1 if emul.etat_propre(r) else 0


def ligne_releve(emul, op: str, detail: str, r: dict) -> str:
    poignee = emul.u64(528)
    pos = emul.os.poignees.get(poignee, ("", 0xFFFFFFFFFFFFFFFF))[1]
    return json.dumps({
        "op": op, "detail": detail,
        "rax": r["rax"], "propre": s_propre(emul, r),
        "poignee": poignee, "taille": emul.u64(520),
        "vue": emul.u64(536), "curseur": emul.u64(544),
        "remplissage": emul.u32(552), "pos": pos,
        "tampon": emul.champ(568, 384).hex(),
        "panneau": emul.panneau().hex(),
        "crash": r.get("crash") or "",
    }, separators=(",", ":"), ensure_ascii=False)


# ---------------------------------------------------------------------------
# LA RÉFÉRENCE UNICORN — le harnais TEL QUEL, le même programme, le même flux
# ---------------------------------------------------------------------------

class ReferenceUnicorn:
    """Le moteur de référence : UNE émulation par programme (le miroir de la
    tranche de l'oracle — l'ouverture puis les lectures, tout vivant).
    La notation de campagne (bid) paramétrable : l'oracle-01 y charge
    loupe-01 (i110001), l'oracle-02 loupe-02 (i110002) — le défaut demeure
    l'échantillon d'audit (loupe-02)."""

    def __init__(self, notation=None, bid="i110002"):
        os_v = HN.OSVirtuel()
        emul = _EmulationCampagne(os_v, notation, bid)
        m9 = open(os.path.join(HN.TRIADE, HN.SCELLE_M9), "rb").read()
        m1 = open(os.path.join(HN.TRIADE, HN.SCELLE_M1), "rb").read()
        emul.poser_heritages(m9, m1)
        self.os_v, self.emul = os_v, emul
        self.temoins: dict[str, bytes] = {}

    def declarer_temoins(self, temoins: dict[str, bytes]) -> None:
        self.temoins = temoins
        for nom, contenu in temoins.items():
            self.os_v.declarer(nom, HN.FichierVirtuel(contenu=contenu))

    def executer(self, ops: list[tuple]) -> list[str]:
        out: list[str] = []
        for op in ops:
            if op[0] == "ouvrir":
                chemin = op[1]
                self.emul.uc.mem_write(
                    HN.ADRESSE_CHEMIN,
                    chemin.encode("utf-16-le") + b"\x00\x00")
                r = self.emul.appeler(L.LOUPE01_VA, {"rcx": HN.ADRESSE_CHEMIN})
                out.append(ligne_releve(self.emul, "ouvrir", chemin, r))
            elif op[0] == "lire":
                dec = op[1]
                r = self.emul.appeler(L.LOUPE02_VA, {"rcx": dec})
                out.append(ligne_releve(self.emul, "lire", f"{dec:#x}", r))
            elif op[0] == "fermer":
                r = self.emul.appeler(L.LOUPE03_VA, {})
                out.append(ligne_releve(self.emul, "fermer", "", r))
            elif op[0] == "restaurer":
                _, poignee, pos, chemin, cadre, panneau = op
                self.emul.uc.mem_write(HN.L.R_CADRE, cadre)
                self.emul.uc.mem_write(HN.L.R_EMPREINTES, panneau)
                self.os_v.poignees[poignee] = (chemin, pos)
                out.append(json.dumps(
                    {"op": "restaurer", "poignee": poignee, "pos": pos},
                    separators=(",", ":")))
            elif op[0] == "armer_echec":
                self.os_v.armer_echec_read(op[1])
                out.append(json.dumps(
                    {"op": "armer_echec", "dans": op[1]},
                    separators=(",", ":")))
            elif op[0] == "echec_close":
                self.os_v.echec_close = bool(op[1])
            elif op[0] == "etat":
                out.append(json.dumps({
                    "op": "etat",
                    "compteurs": [self.os_v.compteurs[k]
                                  for k in HN.FEUILLES_NOYAU],
                    "gle": self.os_v.gle,
                    "journal_gle": [[f, g] for f, g in self.os_v.journal_gle],
                    "interdits": self.os_v.appels_interdits,
                }, separators=(",", ":")))
            else:
                raise ValueError(f"op inconnue : {op!r}")
        return out


# ---------------------------------------------------------------------------
# LE VOLUME QEMU — l'image bâtie par le vrai harnais, le lanceur C exécute
# ---------------------------------------------------------------------------

class _EmulationCampagne(HN.Emulation):
    """Le miroir exact de l'EmulationCampagne des oracles : LA NOTATION DE
    CAMPAGNE assemblée au slot (par-dessus la notation du noyau — la
    campagne l'a vécu ainsi) ; le défaut : loupe-02 à i110002 (l'oracle-02
    et l'échantillon d'audit) ; l'oracle-01 : loupe-01 à i110001."""

    def __init__(self, os_virtuel, notation=None, bid="i110002"):
        super().__init__(os_virtuel)
        if notation is None:
            notation = NOTATION_CAMPAGNE
        if not os.path.exists(notation):
            raise RuntimeError(f"NOTATION-ABSENTE : {notation}")
        rva, slot = L.SLOTS_LOUPE[bid]
        octets, metas = HN.B4.assembler_bloc(self.ks, str(notation),
                                             rva, slot)
        self.uc.mem_write(rva, octets)
        self.blobs[bid] = (octets, metas)


class VolumeQEMU:
    """Le moteur de volume : l'image mémoire dumpée du vrai harnais, le
    lanceur C statique (qemu-x86_64 ou natif), le programme d'opérations."""

    def __init__(self, bac: pathlib.Path, qemu: str | None = None):
        self.bac = pathlib.Path(bac)
        self.bac.mkdir(parents=True, exist_ok=True)
        self.qemu = qemu   # None : l'exécution native (le debug) ; le chemin
        # qemu-x86_64 sinon (le volume)
        ici = pathlib.Path(__file__).resolve().parent
        self.lanceur = ici / "lanceur_qemu"

    def construire_image(self, notation=None, bid="i110002") -> dict:
        """L'image bâtie PAR LE VRAI HARNAIS — les octets de l'émulation
        Unicorn dumpés zone par zone : les deux moteurs courent le MÊME
        bytecode aux MÊMES adresses (la notation de campagne au slot bid)."""
        ref = ReferenceUnicorn(notation, bid)
        infos = {"zones": [], "images": []}
        # LES BLOCS ASSEMBLÉS (les octets mêmes de l'image — la clé du mémo
        # v2 les veut : sha256(bloc) le terme premier de la clé)
        infos["blocs"] = {k: bytes(v[0]) for k, v in ref.emul.blobs.items()}
        # LA PAGE DU LANDING : RET_MAGIQUE vit à 0xDE00 — dans la réserve
        # .text que Unicorn ne mappe jamais (elle s'y ARRÊTE sans y toucher),
        # mais le lanceur y ÉCRIT le pad d'atterrissage : la page mappée
        page_landing = (HN.RET_MAGIQUE & ~0xFFF, 0x1000)
        i = 0
        for addr, taille in ZONES:                  # les zones DUMPÉES
            fimg = self.bac / f"zone{i}.bin"
            fimg.write_bytes(bytes(ref.emul.uc.mem_read(addr, taille)))
            infos["images"].append((addr, taille, fimg))
            i += 1
        for addr, taille in (page_landing, PILE):   # les zones ANONYMES
            infos["zones"].append((addr, taille))
        # l'IAT : les 34 slots du plan — 0..5 les feuilles du noyau, 6 le mort
        iat = []
        for feuille, slot in L.IAT_SLOTS.items():
            idx = HN.FEUILLES_NOYAU.index(feuille) \
                if feuille in HN.FEUILLES_NOYAU else 6
            iat.append((slot, idx))
        infos["iat"] = sorted(iat)
        infos["sentinelles"] = dict(HN.SENTINELLES_NV)
        infos["ret_magique"] = HN.RET_MAGIQUE
        infos["entree_rsp"] = HN.ENTREE_RSP
        infos["canari"] = HN.CANARI[0]
        infos["adresse_chemin"] = HN.ADRESSE_CHEMIN
        infos["cadre"] = (L.R_CADRE, L.R_EMPREINTES)
        self._image = infos
        return infos

    def _environnement(self, ops: list[tuple], temoins: dict[str, bytes],
                       fichiers_temoins: dict[str, pathlib.Path]) -> pathlib.Path:
        infos = self._image
        suffixe = os.getpid()      # chaque travailleur SON environnement —
                                   # jamais une écrasade du voisin
        lignes = []
        for addr, taille in infos["zones"]:
            lignes.append(f"zone {addr:x} {taille:x}")
        for addr, taille, fimg in infos["images"]:
            lignes.append(f"image {fimg} {addr:x} {taille:x}")
        for slot, idx in infos["iat"]:
            lignes.append(f"iat {slot:x} {idx}")
        lignes.append(f"landing {infos['ret_magique']:x}")
        lignes.append(f"ret_magique {infos['ret_magique']:x}")
        lignes.append(f"entree_rsp {infos['entree_rsp']:x}")
        lignes.append(f"canari {infos['canari']:x}")
        for nom, v in sorted(infos["sentinelles"].items()):
            lignes.append(f"sentinelle {nom} {v:x}")
        lignes.append(f"adresse_chemin {infos['adresse_chemin']:x}")
        lignes.append(f"cadre {infos['cadre'][0]:x} {infos['cadre'][1]:x}")
        for nom, chemin in sorted(fichiers_temoins.items()):
            lignes.append(f"temoin {nom} {chemin}")
        for op in ops:
            if op[0] == "ouvrir":
                lignes.append(f"op ouvrir {op[1]} {L.LOUPE01_VA:x}")
            elif op[0] == "lire":
                lignes.append(f"op lire {op[1]:x} {L.LOUPE02_VA:x}")
            elif op[0] == "fermer":
                lignes.append(f"op fermer {L.LOUPE03_VA:x}")
            elif op[0] == "restaurer":
                _, poignee, pos, chemin, cadre, panneau = op
                fc = self.bac / f"releve-cadre-{os.getpid()}.bin"
                fp = self.bac / f"releve-panneau-{os.getpid()}.bin"
                fc.write_bytes(cadre)
                fp.write_bytes(panneau)
                lignes.append(f"op restaurer {poignee:x} {pos:x} {chemin} "
                              f"{fc} {fp}")
            elif op[0] == "armer_echec":
                lignes.append(f"op armer_echec {op[1]}")
            elif op[0] == "echec_close":
                lignes.append(f"op echec_close {1 if op[1] else 0}")
            elif op[0] == "etat":
                lignes.append("etat")
            else:
                raise ValueError(f"op inconnue : {op!r}")
        lignes.append("fin")
        fenv = self.bac / f"environnement-{suffixe}.txt"
        fenv.write_text("\n".join(lignes) + "\n", encoding="utf-8")
        return fenv

    @classmethod
    def depuis_infos(cls, infos: dict, bac: pathlib.Path,
                     qemu: str | None = None) -> "VolumeQEMU":
        """Le volume SUR UNE IMAGE DÉJÀ BÂTIE (les fichiers de l'image
        vivent au bac du parent) — les travailleurs du pool n'ont PAS à
        rebâtir l'image (1,5 s par tête) : ils reçoivent les infos, ils
        écrivent leur programme d'opérations, ils exécutent."""
        vol = cls.__new__(cls)
        vol.bac = pathlib.Path(bac)
        vol.bac.mkdir(parents=True, exist_ok=True)
        vol.qemu = qemu
        ici = pathlib.Path(__file__).resolve().parent
        vol.lanceur = ici / "lanceur_qemu"
        vol._image = infos
        return vol

    def executer(self, ops: list[tuple], temoins: dict[str, bytes]) -> list[str]:
        """Écrit l'environnement, exécute le lanceur, rend les lignes JSON."""
        fichiers_temoins = {}
        for nom, contenu in temoins.items():
            f = self.bac / f"temoin-{os.getpid()}-{nom}"
            f.write_bytes(contenu)
            fichiers_temoins[nom] = f
        fenv = self._environnement(ops, temoins, fichiers_temoins)
        cmd = ([self.qemu, str(self.lanceur), str(fenv)]
               if self.qemu else [str(self.lanceur), str(fenv)])
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        if r.returncode != 0:
            raise RuntimeError(f"le lanceur a rendu {r.returncode} : "
                               f"{r.stderr[:400]}")
        return [l for l in r.stdout.splitlines() if l.strip()]


# ---------------------------------------------------------------------------
# l'échantillon consigné (le plan § 3.3)
# ---------------------------------------------------------------------------

def echantillon_ops(graine: int = 20261114) -> tuple[list[tuple], dict]:
    """LA LISTE CONSIGNÉE : les ouvertures des QUATRE fichiers du
    différentiel V1 ET les lectures à la graine de la campagne (les mêmes
    décales_valides que l'oracle-02, le même rng, le même ordre)."""
    sys.path.insert(0, str(REPO / "atelier-m4-vljfs6pcj"))
    from oracle_unite02_v181 import decales_valides   # le MÊME générateur
    m9 = open(os.path.join(HN.TRIADE, HN.SCELLE_M9), "rb").read()
    temoins = HN.composer_temoins()
    fichiers = {"temoin-1.bin": temoins["temoin-1.bin"],
                "temoin-384.bin": temoins["temoin-384.bin"],
                "temoin-3f.bin": temoins["temoin-3f.bin"],
                "proxy.exe": m9}
    rng = random.Random(graine)
    ops: list[tuple] = []
    for nom in fichiers:
        ops.append(("ouvrir", nom))
        for dec in decales_valides(len(fichiers[nom]), rng):
            ops.append(("lire", dec))
        ops.append(("fermer",))
    ops.append(("etat",))
    return ops, fichiers


if __name__ == "__main__":
    # la démonstration du double moteur : l'échantillon consigné, la
    # divergence=0 exigée, les deux moteurs, la comparaison octet pour octet
    ops, fichiers = echantillon_ops()
    print(f"[échantillon] {len(ops)} opérations consignées "
          f"(graine 20261114)")
    bac = pathlib.Path(tempfile.mkdtemp(prefix="double-moteur-"))
    ref = ReferenceUnicorn()
    ref.declarer_temoins(fichiers)
    flux_ref = ref.executer(ops)
    (bac / "flux-unicorn.jsonl").write_text("\n".join(flux_ref) + "\n")
    print(f"[référence] {len(flux_ref)} lignes Unicorn — la référence")
    vol = VolumeQEMU(bac / "qemu")
    vol.construire_image()
    flux_qemu = vol.executer(ops, fichiers)
    (bac / "flux-qemu.jsonl").write_text("\n".join(flux_qemu) + "\n")
    print(f"[volume] {len(flux_qemu)} lignes QEMU (natif pour la démo)")
    ecart = 0
    for i, (a, b) in enumerate(zip(flux_ref, flux_qemu)):
        if a != b:
            ecart += 1
            if ecart <= 3:
                print(f"DIVERGENCE à la ligne {i} :")
                print(f"  unicorn : {a[:160]}…")
                print(f"  qemu    : {b[:160]}…")
    if len(flux_ref) != len(flux_qemu):
        print(f"DIVERGENCE : {len(flux_ref)} lignes unicorn contre "
              f"{len(flux_qemu)}")
        ecart += 1
    if ecart == 0:
        verdict = "DIVERGENCE=0 — les deux moteurs s'accordent octet pour octet"
    else:
        verdict = f"{ecart} ÉCART(S) — BLOQUANT (tout écart nommé, l'exige)"
    print(f"\nVERDICT : {verdict}")
    sys.exit(0 if ecart == 0 else 2)
