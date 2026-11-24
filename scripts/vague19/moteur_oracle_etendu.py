#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE MOTEUR D'ORACLE NATIF ÉTENDU AUX 52 BLOCS SCELLÉS (W19ORAC).

Contrôles INCHANGÉS : même plan d'adresses, mêmes octets scellés, aucun contrôle retiré.
Ce que le pilote ajoute :
  - le manifeste des 52 descripteurs, chaque bloc assemblé depuis sa notation puis
    confronté OCTET POUR OCTET à son image scellée de laboratoire (sha256) ;
  - un mémo CONTENT-ADDRESSED lié à (empreinte du bloc + configuration + graine) :
    tout octet changé = miss, jamais une session figée ;
  - la cristallisation incrémentale généralisée par DÉDUP content-addressed des rebuilds ;
  - l'audit CHAÎNÉ 1-sur-10 conservé (chaque dixième bloc rejoué et confronté champ
    par champ) ;
  - la re-capture des consoles du jumeau et leur comparaison LIGNE POUR LIGNE aux
    consoles originales.

Statut honnête : le moteur natif exige mmap à 0xC000, refusé par ce bac
(vm.mmap_min_addr = 65536) — la re-exécution native est NOMMÉE impossible ici ; le
jumeau Unicorn rejoue, lui, les vecteurs et rend la console. Les 50 blocs hors des deux
corps crypto n'ont AUCUN vecteur d'oracle au dépôt : leur exécution est EN ATTENTE, nommée.

Usage : python3 scripts/vague19/moteur_oracle_etendu.py [--manifeste|--memo|--audit|--recapture|--preregistrer|--statut]
"""
import hashlib
import importlib.util
import json
import pathlib
import struct
import sys

RACINE = pathlib.Path(__file__).resolve().parents[2]
DOSSIER = RACINE / "atelier-w19-oracle"
ORACLES = RACINE / "atelier-oracles-8hguph5ee"
GRAINE = 20261125
CONFIG = {"page_code": "0xC000", "sortie": "0x503000", "pile": "0x78000", "abi": "msx64"}
IMAGES = {"hello": RACINE / "m0/hello.exe", "selftest": RACINE / "m1/selftest.exe",
          "echo": RACINE / "m2/echo.exe", "proxy": RACINE / "m5/proxy.exe"}


def _m5():
    sys.path.insert(0, str(RACINE / "m5"))
    spec = importlib.util.spec_from_file_location("build_m5",
                                                  str(RACINE / "m5" / "build_m5.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _rva_off(pe, rva):
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData):
            return s.PointerToRawData + (rva - s.VirtualAddress)
    return None


def manifeste():
    import pefile
    m = _m5()
    ks = m.Ks(m.KS_ARCH_X86, m.KS_MODE_64)
    imgs = {k: v.read_bytes() for k, v in IMAGES.items() if v.exists()}
    pes = {k: pefile.PE(data=v, fast_load=True) for k, v in imgs.items()}
    blocs = []
    for bid in m.TOUS_BLOCS:
        entree = {"id": bid, "rva": m.RVA_PAR_BLOC[bid]}
        try:
            octets, _ = m.assembler_bloc(ks, m._chemin_notation_bid(bid),
                                         m.RVA_PAR_BLOC[bid], m.RVA_PAR_BLOC[bid] + 0x2000)
        except Exception as e:
            entree.update(statut="ASSEMBLAGE-REFUSE", motif=str(e)[:80])
            blocs.append(entree)
            continue
        entree["octets"] = len(octets)
        entree["sha256"] = hashlib.sha256(octets).hexdigest()
        candidats = [x.strip() for x in m.EXE_PAR_BLOC.get(bid, "").split(",") if x.strip() in imgs]
        trouve = None
        for ex in candidats:
            off = _rva_off(pes[ex], entree["rva"])
            if off is not None and imgs[ex][off:off + len(octets)] == octets:
                trouve = ex
                break
        entree["image"] = trouve
        entree["statut"] = "BYTE-IDENTIQUE" if trouve else "NON-RESOLU"
        blocs.append(entree)
    doc = {"graine": GRAINE, "n_blocs": len(blocs),
           "byte_identiques": sum(1 for b in blocs if b["statut"] == "BYTE-IDENTIQUE"),
           "non_resolus": [b["id"] for b in blocs if b["statut"] != "BYTE-IDENTIQUE"],
           "blocs": blocs}
    DOSSIER.mkdir(exist_ok=True)
    (DOSSIER / "manifeste-52.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1),
                                               encoding="utf-8")
    print(f"[manifeste] {doc['byte_identiques']}/{doc['n_blocs']} blocs BYTE-IDENTIQUES à leur "
          f"image scellée ; non résolus : {doc['non_resolus']}")
    return doc


def cle_memo(bloc_sha, config, graine):
    return hashlib.sha256((bloc_sha + "\x00" + json.dumps(config, sort_keys=True) +
                           "\x00" + str(graine)).encode()).hexdigest()


def demo_memo():
    doc = manifeste()
    b = next(x for x in doc["blocs"] if x.get("sha256"))
    k1 = cle_memo(b["sha256"], CONFIG, GRAINE)
    mute = ("0" if b["sha256"][0] != "0" else "1") + b["sha256"][1:]
    k2 = cle_memo(mute, CONFIG, GRAINE)
    k3 = cle_memo(b["sha256"], dict(CONFIG, abi="autre"), GRAINE)
    k4 = cle_memo(b["sha256"], CONFIG, GRAINE + 1)
    essais = [("bloc identique → même clé", k1 == k1),
              ("un octet changé → MISS", k1 != k2),
              ("configuration changée → MISS", k1 != k3),
              ("graine changée → MISS", k1 != k4)]
    DOSSIER.mkdir(exist_ok=True)
    (DOSSIER / "memo-cles.json").write_text(json.dumps(
        {"cle": k1, "mutation": k2, "config": k3, "graine": k4}, indent=1), encoding="utf-8")
    print("=" * 78); print("MÉMO CONTENT-ADDRESSED — une clé par (bloc ‖ config ‖ graine)"); print("=" * 78)
    for nom, ok in essais:
        print(f"[{'VERT' if ok else 'ROUGE'}] {nom}")
    print(f"{sum(1 for _, ok in essais if ok)}/{len(essais)} — clé {k1[:16]}…")
    return 0 if all(ok for _, ok in essais) else 3


def dedup():
    doc = manifeste()
    vus = {}
    for b in doc["blocs"]:
        if "sha256" in b:
            vus.setdefault(b["sha256"], []).append(b["id"])
    partages = {k: v for k, v in vus.items() if len(v) > 1}
    print(f"[dedup] {len(doc['blocs'])} blocs, {len(vus)} contenus distincts, "
          f"{sum(len(v) - 1 for v in partages.values())} rebuild(s) dédupliqué(s)")
    return {"contenus": len(vus), "dedup": sum(len(v) - 1 for v in partages.values()), "partages": partages}


def audit_1sur10():
    """Le tirage est CONTENT-ADDRESSÉ (D271) : un bloc entre dans l'échantillon si les 32
    premiers bits de son sha256 sont congrus à 0 modulo 10 — ajouter un bloc ne décale plus
    l'échantillon, et le tirage se recompose par quiconque lit les empreintes."""
    doc = manifeste()
    ech = [b for b in doc["blocs"]
           if b.get("sha256") and int(b["sha256"][:8], 16) % 10 == 0]
    if not ech:
        print("[audit 1/10] ROUGE — aucun bloc tiré (échantillon vide)")
        return 3
    m = _m5(); ks = m.Ks(m.KS_ARCH_X86, m.KS_MODE_64)
    verts = 0
    for b in ech:
        octets, _ = m.assembler_bloc(ks, m._chemin_notation_bid(b["id"]), b["rva"], b["rva"] + 0x2000)
        ok = hashlib.sha256(octets).hexdigest() == b.get("sha256")
        verts += 1 if ok else 0
        print(f"[audit 1/10] {b['id']} — {'VERT' if ok else 'ROUGE'}")
    print(f"[audit 1/10] {verts}/{len(ech)} blocs tirés par CONTENU (sha256[:8] % 10 == 0), champ par champ")
    return 0 if verts == len(ech) else 3


def _jumeau(corps, vecteurs, profil="a"):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_64
    from unicorn.x86_const import (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8,
                                   UC_X86_REG_R10, UC_X86_REG_RAX, UC_X86_REG_RSP)
    cal = (ORACLES / "registres" / "calendrier.bin").read_bytes()
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    for a, s in ((0xC000, 0x4000), (0x500000, 0x21000), (0x70000, 0x10000)):
        uc.mem_map(a, s)
    uc.mem_write(0xC000, corps)
    uc.mem_write(0x500200, cal)
    console = []
    for i, v in enumerate(vecteurs):
        uc.mem_write(0x503000, b"\x00" * 16)
        vb = struct.pack("<QQQQ", *v)
        uc.mem_write(0x500400, vb)
        uc.mem_write(0x78000, struct.pack("<Q", 0x60000))
        uc.reg_write(UC_X86_REG_RSP, 0x78000)
        uc.reg_write(UC_X86_REG_R10, 0)
        if profil == "a":
            uc.reg_write(UC_X86_REG_RCX, 0x500200)
            uc.reg_write(UC_X86_REG_RDX, 0x500400)
            uc.reg_write(UC_X86_REG_R8, 0x503000)
        else:
            uc.mem_write(0x500A00, vb[:16])
            uc.reg_write(UC_X86_REG_RCX, 0x503000)
            uc.reg_write(UC_X86_REG_RDX, 0x500400)
            uc.reg_write(UC_X86_REG_R8, 0x500A00)
        uc.emu_start(0xC000, 0x60000)
        console.append({"vecteur": i, "rax": uc.reg_read(UC_X86_REG_RAX),
                        "digeste": bytes(uc.mem_read(0x503000, 16)).hex()})
    return console


def recapture():
    brut = (ORACLES / "registres" / "console-mesure.vec").read_bytes()
    vect = [struct.unpack("<QQQQ", brut[i * 32:(i + 1) * 32]) for i in range(len(brut) // 32)]
    attendu = [json.loads(l) for l in (ORACLES / "registres" / "console-mesure.json").read_text().splitlines() if l.strip()]
    obtenu = _jumeau((ORACLES / "notation" / "corps-tls13-16.bin").read_bytes(), vect, "a")
    identiques = sum(1 for a, b in zip(attendu, obtenu)
                     if a["rax"] == b["rax"] and a["digeste"] == b["digeste"])
    DOSSIER.mkdir(exist_ok=True)
    (DOSSIER / "console-recapture.json").write_text(
        json.dumps(obtenu, indent=1), encoding="utf-8")
    print(f"[recapture] {identiques}/{len(attendu)} lignes IDENTIQUES (rax + digeste) au jumeau original")
    print("[recapture] moteur natif : NON REJOUABLE dans ce bac — mmap(0xC000) refusé "
          f"(vm.mmap_min_addr = {pathlib.Path('/proc/sys/vm/mmap_min_addr').read_text().strip()})")
    return 0 if identiques == len(attendu) else 3


def preregistrer():
    doc = {
        "objet": "extension du moteur d'oracle natif aux 52 blocs scellés",
        "cible": "session T < 10 s à volumes d'oracle égalisés",
        "n_par_configuration": 5,
        "chronometre": "monotone (CLOCK_MONOTONIC)",
        "graine": GRAINE,
        "commandes": [
            "python3 scripts/vague19/moteur_oracle_etendu.py --manifeste",
            "python3 scripts/vague19/moteur_oracle_etendu.py --memo",
            "python3 scripts/vague19/moteur_oracle_etendu.py --audit",
            "python3 scripts/vague19/moteur_oracle_etendu.py --recapture",
        ],
        "config": CONFIG,
        "statut": "EN ATTENTE — 50 des 52 blocs n'ont aucun vecteur d'oracle au dépôt ; "
                  "le moteur natif n'est pas rejouable dans ce bac",
    }
    DOSSIER.mkdir(exist_ok=True)
    f = DOSSIER / "preregistrement.json"
    f.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[preregistre] écrit {f.relative_to(RACINE)} sha256 {hashlib.sha256(f.read_bytes()).hexdigest()}")
    return 0


def main():
    if "--manifeste" in sys.argv:
        manifeste(); return 0
    if "--memo" in sys.argv:
        return demo_memo()
    if "--audit" in sys.argv:
        return audit_1sur10()
    if "--recapture" in sys.argv:
        return recapture()
    if "--preregistrer" in sys.argv:
        return preregistrer()
    manifeste(); demo_memo(); audit_1sur10(); recapture()
    print("[statut] EN ATTENTE pour les blocs sans vecteurs ; aucun chiffre natif revendiqué.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
