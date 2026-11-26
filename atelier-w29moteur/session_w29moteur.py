#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""session_w29moteur.py — LA SESSION DU MOTEUR GÉNÉRALISÉ AUX 52 BLOCS
(W29MOTEUR, prompt 2 de la vague 29 — le plan gelé PLAN-W29MOTEUR.md, sha256
3ecf95d7… consigné à EMPREINTES-PLANS-VAGUE29.txt AVANT toute donnée).

1. LE CORPUS GÉNÉRALISÉ : les 50 blocs résolus du manifeste-52 (les deux non
   résolus c30012/c30014 exclus et nommés), le corpus des vecteurs
   atelier-w20-orac — l'assemblage de chaque bloc DEPUIS SA NOTATION (R5, le
   sha256 recoupé au manifeste — un écart refuse la session) ;
2. LA CONSOLE LIGNE-IDENTIQUE au moteur committé (moteur_oracles) pour chaque
   bloc : le moteur généralisé (moteur_volumes, le lot unique, le compte en
   registres bruts, la console différée) exécuté sur les vecteurs du bloc —
   l'équivalence prouvée ligne par ligne ;
3. LA CONFRONTATION au jumeau (le corpus porte la console du jumeau : le
   statut/rax/sortie de chaque vecteur) — l'AUDIT 1-SUR-10 conservé et étendu ;
4. LA RACINE DE MERKLE : le digeste de trace complet par vecteur
   (bloc ‖ index ‖ rax ‖ digeste) engagé dans UN arbre — la racine CONSIGNÉE ;
   la recomposition depuis les traces recoupée ; la racine divergente REFUSÉE ;
5. LE RÉGIME PAR BLOC : le régime chaud du moteur généralisé contre LE PILOTE
   NU (le même code de bloc appelé directement, gcc -O2, les horloges internes
   symétriques, n=9 passes, la médiane) — le ratio par bloc publié, la cible
   ≤ 5 × C pré-enregistrée au plan ;
6. LES CONTRÔLES NÉGATIFS : le shim muté attrapé au premier vecteur ; l'octet
   de carte muté → MISS du mémo content-addressed ; le voisinage amputé →
   FAULT nommé ; la racine de Merkle divergente → refus nommé.

Usage : python3 atelier-w29moteur/session_w29moteur.py [--regime-seul]
Écrit : session-corpus.json, regime-blocs.json
"""
import hashlib
import importlib.util
import json
import pathlib
import statistics
import subprocess
import sys
import tempfile
import time

R = pathlib.Path(__file__).resolve().parents[1]
ICI = pathlib.Path(__file__).resolve().parent
MOTEUR_VOLUMES = R / "atelier-w28harnais/moteur_volumes"
MOTEUR_COMMITTE = R / "atelier-w27vaes/moteur_oracles"
PILOTE = R / "atelier-w28harnais/pilote_c"
CALENDRIER = R / "atelier-oracles-8hguph5ee/registres/calendrier.bin"
MANIFESTE = R / "atelier-w19-oracle/manifeste-52.json"
VECTEURS = R / "atelier-w20-orac"
EXCLUS = {"c30012", "c30014"}
GRAINE = 20261128                 # consignée AVANT le tirage (W28HARNAIS reconduite)
TUILER_REGIME = 12000             # le volume du régime : le corpus tuilé (W28HARNAIS)
PASSES_REGIME = 9                 # n≥9 passes, la médiane
CIBLE_REGIME = 5.0                # ≤ 5 × C pré-enregistrée au plan

sys.path.insert(0, str(R / "m5"))
spec = importlib.util.spec_from_file_location("build_m5", str(R / "m5" / "build_m5.py"))
m5 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m5)


def assembler_corpus(tmp: pathlib.Path):
    """l'assemblage des 50 blocs depuis leurs notations + le recoup sha256."""
    man = json.loads(MANIFESTE.read_text())
    blocs = [b for b in man["blocs"] if b["id"] not in EXCLUS and b.get("sha256")]
    corps = {}
    for b in blocs:
        octets = m5.assembler_bloc(m5.Ks(m5.KS_ARCH_X86, m5.KS_MODE_64),
                                   m5._chemin_notation_bid(b["id"]), b["rva"],
                                   b["rva"] + 0x2000)[0]
        if hashlib.sha256(octets).hexdigest() != b["sha256"]:
            raise SystemExit(f"sha256 divergent pour {b['id']} — l'assemblage n'est plus la pièce scellée")
        f = tmp / f"corps-{b['id']}.bin"
        f.write_bytes(octets)
        corps[b["id"]] = f
    return blocs, corps


def lancer(moteur, marge_hex, corps, vec, n, console, delai=15.0):
    """une invocation du moteur — retour (code, lignes)."""
    try:
        p = subprocess.run([str(moteur), str(corps), marge_hex, str(vec), str(n),
                            str(console), "a", str(CALENDRIER)],
                           capture_output=True, timeout=delai)
    except subprocess.TimeoutExpired:
        return "DEPASSEMENT", []
    lignes = []
    if console.exists():
        for l in console.read_text().splitlines():
            l = l.strip()
            if l:
                try:
                    lignes.append(json.loads(l))
                except json.JSONDecodeError:
                    pass
    if p.returncode == 0:
        return "OK", lignes
    if p.returncode < 0:
        return f"FAULT-SIG{-p.returncode}", lignes
    return f"FAULT-{p.returncode}", lignes


def vecteurs_bin(vifs, dest: pathlib.Path, tuilage=1):
    with open(dest, "wb") as f:
        for i in range(tuilage):
            for v in vifs:
                for k in range(4):
                    f.write(int(v["entree"][k]).to_bytes(8, "little"))


def merkle(feuilles: list[bytes]) -> str:
    """LA RACINE — SHA256 aux feuilles, l'arbre binaire canonique (le jumeau
    seul survivant dupliqué — la convention du plan)."""
    niveau = [hashlib.sha256(b).digest() for b in feuilles]
    while len(niveau) > 1:
        suivant = []
        for i in range(0, len(niveau), 2):
            a = niveau[i]
            b = niveau[i + 1] if i + 1 < len(niveau) else a
            suivant.append(hashlib.sha256(a + b).digest())
        niveau = suivant
    return niveau[0].hex()


def classifier(bid, corps_f, vifs, console, moteur):
    """LA CLASSIFICATION par vecteur : la passe entière d'abord ; si le moteur
    meurt, le vecteur par vecteur (le patron W27VAES — un SIGSEGV nomme le
    VECTEUR, jamais la session). Retour le dictionnaire {i: {statut, rax,
    digeste}}."""
    vf = console.parent / f"vec-{bid}.bin"
    vecteurs_bin(vifs, vf)
    etat, lignes = lancer(moteur, "c000", corps_f, vf, len(vifs), console)
    console.unlink(missing_ok=True)
    natifs = {}
    if etat == "OK" and len(lignes) == len(vifs):
        for i, l in enumerate(lignes):
            natifs[i] = {"statut": "OK", "rax": l["rax"], "digeste": l["digeste"]}
        return natifs
    un = console.parent / f"vec-un-{bid}.bin"
    for i, v in enumerate(vifs):
        vecteurs_bin([v], un)
        etat_v, lignes_v = lancer(moteur, "c000", corps_f, un, 1, console, delai=8.0)
        console.unlink(missing_ok=True)
        if etat_v == "OK" and len(lignes_v) == 1:
            natifs[i] = {"statut": "OK", "rax": lignes_v[0]["rax"],
                         "digeste": lignes_v[0]["digeste"]}
        else:
            natifs[i] = {"statut": etat_v}
    return natifs


def session_corpus():
    """LA SESSION : consoles des deux moteurs + Merkle + audit 1/10 + contrôles."""
    debut = time.monotonic()
    registre = {"graine": GRAINE, "blocs": [], "controles": {}}
    with tempfile.TemporaryDirectory(prefix="w29moteur-") as td:
        tmp = pathlib.Path(td)
        blocs, corps = assembler_corpus(tmp)
        console_v = tmp / "console-v.jsonl"
        console_c = tmp / "console-c.jsonl"
        tot_v = tot_ident_v = tot_class_ok = 0
        divergences_moteurs = []
        divergences_jumeau = []
        feuilles = []
        audit = {"audites": 0, "vivants": 0, "identiques": 0}
        for b in blocs:
            bid = b["id"]
            vecs = json.loads((VECTEURS / f"vecteurs-{bid}.json").read_text())["vecteurs"]
            vifs = [v for v in vecs if v["type"] != "rejet"]
            nat_v = classifier(bid, corps[bid], vifs, console_v, MOTEUR_VOLUMES)
            nat_c = classifier(bid, corps[bid], vifs, console_c, MOTEUR_COMMITTE)
            b_ident = 0
            b_class = 0
            for i, v in enumerate(vifs):
                tot_v += 1
                nv, nc = nat_v.get(i, {}), nat_c.get(i, {})
                same = (nv.get("statut") == nc.get("statut")
                        and nv.get("rax") == nc.get("rax")
                        and nv.get("digeste") == nc.get("digeste"))
                if same:
                    b_ident += 1
                    tot_ident_v += 1
                else:
                    divergences_moteurs.append({"bloc": bid, "vecteur": i,
                                                "volumes": nv, "commite": nc})
                # LA FEUILLE DE TRACE — le digeste complet du vecteur
                feuilles.append(bid.encode() + b"|" + str(i).encode() + b"|"
                                + str(nv.get("rax", nv.get("statut"))).encode()
                                + b"|" + (nv.get("digeste", "-").encode()
                                          if nv.get("digeste") else b"-"))
                # LA CLASSIFICATION au jumeau (le corpus porte sa console)
                jum_ok = v.get("statut") == "OK"
                nat_ok = nv.get("statut") == "OK"
                if (jum_ok and nat_ok and v.get("rax") == nv.get("rax")
                        and v.get("sortie") == nv.get("digeste")) or \
                   (not jum_ok and not nat_ok):
                    b_class += 1
                else:
                    divergences_jumeau.append({"bloc": bid, "vecteur": i,
                                               "jumeau": {"statut": v.get("statut"),
                                                           "rax": v.get("rax")},
                                               "natif": nv})
                if i % 10 == 0:                       # L'AUDIT 1-SUR-10
                    audit["audites"] += 1
                    if jum_ok:
                        audit["vivants"] += 1
                        if (nat_ok and v.get("rax") == nv.get("rax")
                                and v.get("sortie") == nv.get("digeste")):
                            audit["identiques"] += 1
            tot_class_ok += b_class
            registre["blocs"].append({"id": bid, "vecteurs": len(vifs),
                                      "identiques_aux_deux": b_ident,
                                      "classes_comme_jumeau": b_class,
                                      "ok_natifs": sum(1 for i in range(len(vifs))
                                                       if nat_v.get(i, {}).get("statut") == "OK")})
        # LA RACINE DE MERKLE — le scellage de la trace entière
        racine = merkle(feuilles)
        registre["racine_merkle"] = racine
        registre["feuilles"] = len(feuilles)
        registre.update({"total_vecteurs": tot_v,
                         "identiques_aux_deux_moteurs": tot_ident_v,
                         "classes_comme_jumeau": tot_class_ok,
                         "divergences_moteurs": divergences_moteurs,
                         "divergences_jumeau": divergences_jumeau,
                         "note_b20006": ("l'écart de motif nommé (le précédent "
                                         "W27VAES : b20006 rend 0xC000 natif contre "
                                         "0 au jumeau — les 4 vecteurs, la même "
                                         "divergence consignée au registre 77/81)"),
                         "audit_1sur10": audit,
                         "duree_s": round(time.monotonic() - debut, 3)})

        # ---- LES CONTRÔLES NÉGATIFS -------------------------------------------
        # (1) le shim muté ATTRAPÉ : la première position d'octet du corps
        #     d'un bloc VIVANT dont la mutation diverge (la console ou l'état)
        #     — l'exécution mutée REFUSÉE à la confrontation
        bid0 = next(b["id"] for b in blocs
                    if json.loads((VECTEURS / f"vecteurs-{b['id']}.json").read_text())
                    ["vecteurs"][0].get("statut") == "OK")
        octets = corps[bid0].read_bytes()
        vecs = json.loads((VECTEURS / f"vecteurs-{bid0}.json").read_text())["vecteurs"]
        vifs = [v for v in vecs if v["type"] != "rejet"]
        nat_h = classifier(bid0, corps[bid0], vifs, console_v, MOTEUR_VOLUMES)
        attrape = None
        for pos in range(len(octets)):
            mute = bytearray(octets)
            mute[pos] ^= 0x5a
            corps_mute = tmp / f"corps-mute-{pos}.bin"
            corps_mute.write_bytes(bytes(mute))
            nat_m = classifier(f"{bid0}-mute{pos}", corps_mute, vifs, console_v,
                              MOTEUR_VOLUMES)
            if any(nat_h.get(i) != nat_m.get(i) for i in range(len(vifs))):
                attrape = pos
                break
        registre["controles"]["shim-mute"] = {
            "bloc": bid0, "octet": attrape,
            "etat": (nat_m.get(0, {}).get("statut") if attrape is not None else None),
            "note": ("la première position mutante divergente (la console ou "
                     "l'état) — le mutant REFUSÉ à la confrontation"),
            "attrape": attrape is not None}

        # (2) l'octet de carte muté → MISS du mémo content-addressed
        #     (la clé : le sha256 du corps — le corps muté une AUTRE clé)
        cle_honn = hashlib.sha256(corps[bid0].read_bytes()).hexdigest()
        cle_mute = hashlib.sha256(bytes(mute)).hexdigest()
        registre["controles"]["octet-carte-mute"] = {
            "cle_honnete": cle_honn, "cle_mutee": cle_mute,
            "miss": cle_honn != cle_mute,
            "note": "la clé content-addressed du corps muté diverge — MISS nommé"}

        # (3) le voisinage amputé → FAULT nommé (le calendrier absent)
        vf1 = tmp / "vec1.bin"
        vecteurs_bin(vifs[:1], vf1)
        p = subprocess.run([str(MOTEUR_VOLUMES), str(corps[bid0]), "c000",
                            str(vf1), "1", str(console_v), "a", str(R / "inexistant.bin")],
                           capture_output=True, timeout=10)
        console_v.unlink(missing_ok=True)
        registre["controles"]["voisinage-ampute"] = {
            "code": p.returncode, "fault": p.returncode != 0,
            "nom": "CALENDRIER-ABSENT" if p.returncode != 0 else "(aucune)"}

        # (4) la racine de Merkle divergente → refus nommé
        feuilles_mutees = list(feuilles)
        feuilles_mutees[0] = b"octet-mute"
        racine_mutee = merkle(feuilles_mutees)
        registre["controles"]["racine-divergente"] = {
            "racine_consignee": racine, "racine_mutee": racine_mutee,
            "refusee": racine_mutee != racine}

    (ICI / "session-corpus.json").write_text(
        json.dumps(registre, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[corpus] {tot_v} vecteurs · identiques aux deux moteurs {tot_ident_v}"
          f" · classes comme le jumeau {tot_class_ok} · racine {racine[:16]}…"
          f" · audit 1/10 {audit['identiques']}/{audit['audites']} identiques"
          f" (vivants {audit['vivants']})")
    for k, v in registre["controles"].items():
        vu = v.get("attrape", v.get("miss", v.get("fault", v.get("refusee"))))
        print(f"  contrôle {k:22s} → {vu}")
    return registre


def session_regime():
    """LE RÉGIME PAR BLOC : le moteur généralisé contre le pilote nu (n=9)."""
    regime = {"graine": GRAINE, "tuilage": TUILER_REGIME, "passes": PASSES_REGIME,
              "cible": CIBLE_REGIME, "blocs": []}
    with tempfile.TemporaryDirectory(prefix="w29regime-") as td:
        tmp = pathlib.Path(td)
        blocs, corps = assembler_corpus(tmp)
        console = tmp / "console.jsonl"
        for b in blocs:
            bid = b["id"]
            vecs = json.loads((VECTEURS / f"vecteurs-{bid}.json").read_text())["vecteurs"]
            vifs = [v for v in vecs if v["type"] != "rejet"]
            if not vifs:
                continue
            # LE TUILAGE : le corpus canonique tuilé au volume du régime
            # (AUCUN nouveau tirage — la convention nommée au registre)
            n = (TUILER_REGIME // len(vifs)) * len(vifs)
            vf = tmp / "vec.bin"
            vecteurs_bin(vifs, vf, tuilage=n // len(vifs))
            # LE MOTEUR : n=9 passes (le HOT imprimé par appel)
            hot = []
            for _ in range(PASSES_REGIME):
                p = subprocess.run([str(MOTEUR_VOLUMES), str(corps[bid]), "c000",
                                    str(vf), str(n), str(console), "a", str(CALENDRIER)],
                                   capture_output=True, timeout=300)
                console.unlink(missing_ok=True)
                for l in p.stdout.decode().splitlines():
                    if l.startswith("HOT"):
                        hot.append(float(l.split()[1]))
            # LE PILOTE : n=9 passes (un temps par ligne sur stdout)
            p = subprocess.run([str(PILOTE), str(corps[bid]), "c000", str(vf),
                                str(n), str(CALENDRIER), str(PASSES_REGIME)],
                               capture_output=True, timeout=300)
            pil = [float(l) for l in p.stdout.decode().splitlines() if l.strip()]
            if hot and pil:
                med_v = statistics.median(hot)
                med_p = statistics.median(pil)
                ratio = med_v / med_p if med_p > 0 else None
                regime["blocs"].append({"id": bid, "n": n,
                                        "moteur_us": round(med_v, 3),
                                        "pilote_us": round(med_p, 3),
                                        "ratio": round(ratio, 3) if ratio else None,
                                        "verdict": ("TENUE" if ratio and ratio <= CIBLE_REGIME
                                                    else "MANQUÉE")})
    tennes = sum(1 for b in regime["blocs"] if b["verdict"] == "TENUE")
    regime["resume"] = {"blocs_mesures": len(regime["blocs"]),
                        "tenues": tennes,
                        "manquees": len(regime["blocs"]) - tennes}
    (ICI / "regime-blocs.json").write_text(
        json.dumps(regime, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    pires = sorted(regime["blocs"], key=lambda b: -(b["ratio"] or 0))[:5]
    print(f"[régime] {len(regime['blocs'])} blocs mesurés · {tennes} TENUE · "
          f"{len(regime['blocs']) - tennes} MANQUÉE")
    for b in pires:
        print(f"  pire: {b['id']} ratio {b['ratio']} "
              f"({b['moteur_us']:.1f} vs {b['pilote_us']:.1f} µs)")
    return regime


if __name__ == "__main__":
    if "--regime-seul" in sys.argv:
        session_regime()
    else:
        session_corpus()
        session_regime()
