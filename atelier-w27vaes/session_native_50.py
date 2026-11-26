#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""session_native_50.py — LA SESSION NATIVE DU MOTEUR D'ORACLE (W27VAES, prompt 6,
geste 3) : le corpus des 50 blocs (320 vecteurs, la graine 20261124 consignée)
exécuté NATIVEMENT — le refus mmap 0xC000 du bac d'alors RE-ÉPROUVÉ ici
(vm.mmap_min_addr = 4 096, l'adresse 0xC000 vit au-dessus du plancher).

La session (à volumes d'oracle égalisés — le même corpus que le jumeau) :
  1. l'assemblage de chaque bloc DEPUIS SA NOTATION (R5 : l'octet dérive de I,
     le sha256 recoupé au manifeste-52 de la vague 19) ;
  2. l'exécution native de CHAQUE vecteur par le moteur (mmap+appel), chaque
     bloc dans son sous-processus (un SIGSEGV nomme le vecteur FAULT, jamais
     la session) ;
  3. la confrontation au jumeau committé : les vecteurs OK du jumeau doivent
     être LIGNE-IDENTIQUES (rax + digeste de la page de sortie) ; les FAULT
     du jumeau sont attendus FAULT nativement (l'écart de motif nommé) ;
  4. la mesure : n=5 sessions complètes, chronomètre monotone, la médiane
     confrontée à la cible pré-enregistrée T < 10 s (CIB-ORACLE-T, D264).

Usage : python3 atelier-w27vaes/session_native_50.py [--mesure-seule]
Écrit : session-native-50.json (la confrontation) et mesure-t.json (les temps).
"""
import hashlib
import importlib.util
import json
import pathlib
import subprocess
import sys
import time

R = pathlib.Path(__file__).resolve().parents[1]          # le dépôt
ICI = pathlib.Path(__file__).resolve().parent            # atelier-w27vaes
MOTEUR = ICI / "moteur_oracles"
CALENDRIER = R / "atelier-oracles-8hguph5ee/registres/calendrier.bin"
MANIFESTE = R / "atelier-w19-oracle/manifeste-52.json"
VECTEURS = R / "atelier-w20-orac"
EXCLUS = {"c30012", "c30014"}
GRAINE = 20261124
CIBLE_T = 10.0

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


def lancer(marge_hex: str, corps: pathlib.Path, vec: pathlib.Path, n: int,
           console: pathlib.Path, delai: float = 5.0):
    """une invocation du moteur natif — retour (code, lignes)."""
    try:
        p = subprocess.run([str(MOTEUR), str(corps), marge_hex, str(vec), str(n),
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
        return f"FAULT-SIG{-p.returncode}", lignes   # SIGSEGV=-11, SIGILL=-4…
    return f"FAULT-{p.returncode}", lignes


def session_complete(tmp: pathlib.Path, trace=None):
    """UNE session : assemblage + exécution native des 50 blocs + confrontation.
    Retour (durée_s, resultats) — les resultats seulement si trace est donné."""
    debut = time.monotonic()
    blocs, corps = assembler_corpus(tmp)
    resultats = {}
    console = tmp / "console.jsonl"
    for b in blocs:
        bid = b["id"]
        vecs = json.loads((VECTEURS / f"vecteurs-{bid}.json").read_text())["vecteurs"]
        vifs = [v for v in vecs if v["type"] != "rejet"]
        vf = tmp / "vec.bin"
        with open(vf, "wb") as f:
            for v in vifs:
                f.write(int(v["entree"][0]).to_bytes(8, "little"))
                f.write(int(v["entree"][1]).to_bytes(8, "little"))
                f.write(int(v["entree"][2]).to_bytes(8, "little"))
                f.write(int(v["entree"][3]).to_bytes(8, "little"))
        # la passe du bloc entière d'abord ; si le moteur meurt, le vecteur par vecteur
        etat, lignes = lancer("c000", corps[bid], vf, len(vifs), console)
        natifs = {}
        if etat == "OK" and len(lignes) == len(vifs):
            for i, l in enumerate(lignes):
                natifs[i] = {"statut": "OK", "rax": l["rax"], "digeste": l["digeste"]}
        else:
            un = tmp / "vec-un.bin"
            for i, v in enumerate(vifs):
                with open(un, "wb") as f:
                    f.write(int(v["entree"][0]).to_bytes(8, "little"))
                    f.write(int(v["entree"][1]).to_bytes(8, "little"))
                    f.write(int(v["entree"][2]).to_bytes(8, "little"))
                    f.write(int(v["entree"][3]).to_bytes(8, "little"))
                etat_v, lignes_v = lancer("c000", corps[bid], un, 1, console)
                if etat_v == "OK" and len(lignes_v) == 1:
                    natifs[i] = {"statut": "OK", "rax": lignes_v[0]["rax"],
                                 "digeste": lignes_v[0]["digeste"]}
                else:
                    natifs[i] = {"statut": etat_v}
        if trace is not None:
            trace[bid] = natifs
    duree = time.monotonic() - debut
    return duree


def confronter():
    """la confrontation au jumeau committé + la mesure n=5 (une seule passe tracée)."""
    import tempfile
    with tempfile.TemporaryDirectory(prefix="w27vaes-") as td:
        tmp = pathlib.Path(td)
        # la passe tracée (le détail complet)
        trace = {}
        duree_tracee = session_complete(tmp, trace=trace)
        # les passes de mesure (sans trace, n=4 supplémentaires → n=5 au total)
        durees = [duree_tracee]
        for _ in range(4):
            durees.append(session_complete(tmp))
        durees.sort()
        mediane = durees[len(durees) // 2]

        # la confrontation champ par champ
        confront = {"blocs": [], "graine": GRAINE, "cible_t_s": CIBLE_T}
        tot_v = tot_ok_natif = tot_ok_identiques = tot_fault_natif = 0
        divergences = []
        for bid, natifs in sorted(trace.items()):
            vecs = json.loads((VECTEURS / f"vecteurs-{bid}.json").read_text())["vecteurs"]
            vifs = [v for v in vecs if v["type"] != "rejet"]
            b_ok_natif = b_ident = b_fault = 0
            for i, v in enumerate(vifs):
                tot_v += 1
                n = natifs.get(i, {"statut": "ABSENT"})
                if n["statut"] == "OK":
                    tot_ok_natif += 1
                    b_ok_natif += 1
                    if v.get("statut") == "OK":
                        dg = v.get("sortie", "")
                        rax = v.get("rax")
                        if n["rax"] == rax and n["digeste"] == dg:
                            tot_ok_identiques += 1
                            b_ident += 1
                        else:
                            divergences.append({"bloc": bid, "vecteur": i,
                                                "jumeau": {"rax": rax, "sortie": dg},
                                                "natif": n})
                    else:
                        divergences.append({"bloc": bid, "vecteur": i,
                                            "jumeau": {"statut": v.get("statut")},
                                            "natif": n, "motif": "OK natif, FAULT au jumeau"})
                else:
                    tot_fault_natif += 1
                    b_fault += 1
                    if v.get("statut") == "OK":
                        divergences.append({"bloc": bid, "vecteur": i,
                                            "jumeau": {"statut": "OK", "rax": v.get("rax"),
                                                       "sortie": v.get("sortie")},
                                            "natif": n,
                                            "motif": "OK au jumeau, FAULT natif — NOMMÉ"})
            confront["blocs"].append({"id": bid, "vecteurs": len(vifs),
                                      "ok_natif": b_ok_natif, "identiques": b_ident,
                                      "fault_natif": b_fault})
        confront.update({"total_vecteurs": tot_v,
                         "ok_natif": tot_ok_natif,
                         "identiques_aux_deux": tot_ok_identiques,
                         "fault_natif": tot_fault_natif,
                         "divergences": divergences,
                         "durees_sessions_s": [round(d, 4) for d in durees],
                         "mediane_s": round(mediane, 4),
                         "verdict_t": "TENUE" if mediane < CIBLE_T else "MANQUÉE"})
        (ICI / "session-native-50.json").write_text(
            json.dumps(confront, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"[session] {tot_v} vecteurs · natifs OK {tot_ok_natif} · "
              f"identiques aux deux {tot_ok_identiques} · FAULT natifs {tot_fault_natif} · "
              f"divergences {len(divergences)}")
        print(f"[mesure] sessions {['%.3f' % d for d in durees]} · médiane {mediane:.3f} s "
              f"· cible < {CIBLE_T} s → {confront['verdict_t']}")
        return confront


if __name__ == "__main__":
    confronter()
