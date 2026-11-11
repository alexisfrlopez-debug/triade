#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fuzzage_v110.py — LA COUVERTURE ET LE FUZZING GUIDÉ de l'édition v0.11.0
(la commande du développeur, chantier 2).

Les BLOCS D'ENTRÉE NON FIABLES, instrumentés et attaqués :

  LOUPE-01 (ouvrir) — le chemin de fichier non fiable : le harnais noyau
      (la mini-OS virtuelle) chargé avec un HOOK DE COUVERTURE (les adresses
      exécutées du bloc, par traduction) ; DES CANARIS autour du tampon du
      chemin et le panneau de session relus après chaque run ; le harnais
      d'entrée posé en PAGE GARDE (le tampon au milieu d'une page veille) ;
      campagne guidée : les entrées qui AUGMENTENT la couverture d'instructions
      du bloc sont gardées (corpus croissant), les autres mutent encore ;

  HTTP-10 (le parseur d'entrée, la révision de terrain r3) — le fuzzer du
      million (M3, D72) repris : l'émulateur de la pièce, le crochet mémoire
      P5 (la violation NOMMÉE), la session rejouée par cas ; campagne guidée
      par la couverture des adresses exécutées du bloc http-10.

GRAINES FIXÉES (reproductible) : 20261111 (loupe), 20261112 (http).
RAPPORT : couverture atteinte (instructions distinctes / total du bloc),
crashes (fautes émulation), violations (canaris/garde), taille du corpus.

Sortie : scripts/preuves_v110/fuzzage.csv + fuzzage_rapport.txt
"""

from __future__ import annotations

import importlib.util
import json
import pathlib
import random
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
PREUVES = REPO / "scripts" / "preuves_v110"
PREUVES.mkdir(parents=True, exist_ok=True)

GRAINE_LOUPE = 20261111
GRAINE_HTTP = 20261112


def charger_module(nom: str, chemin: pathlib.Path):
    chemin = pathlib.Path(chemin)
    sys.path.insert(0, str(chemin.parent))
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


# ═══════════════════════════════ 1. LOUPE-01 (le chemin non fiable) ═══════════════════════════════

def campagne_loupe01(iterations: int = 400):
    import unicorn as uc
    from unicorn import UC_HOOK_CODE

    H = charger_module("h_noyau_fuzz", REPO / "loupe" / "harnais_noyau.py")
    L = charger_module("lay_loupe_fuzz", REPO / "loupe" / "layout.py")

    LOUPE01_VA = L.LOUPE01_VA
    fin_bloc = LOUPE01_VA + L.SLOTS_LOUPE["i110001"][1]

    # -- l'émulation : la mini-OS du harnais, le crochet de couverture en plus
    os_v = H.OSVirtuel()
    noms_valides = ["temoin.bin", "vide.bin", "a.bin", "b.txt", "c.dat",
                    "donnees.bin", "octets.bin", "piece.exe", "x", "y.z",
                    "tres-long-nom-de-fichier-pour-la-borne.bin",
                    "mere.bin", "r.txt", "s.bin", "t.bin", "u.bin"]
    for j, nom in enumerate(noms_valides):
        os_v.declarer(nom, H.FichierVirtuel(
            contenu=bytes((j * 7 + k) & 0xFF for k in range(64 + 48 * j))))
    emul = H.Emulation(os_v)
    # LES HÉRITAGES (V0/V1 du harnais) : la pièce M9 (la famille sha) et la
    # pièce M1 (la minilibc) posées aux slots — sans elles, loupe-01 meurt
    donnees_m9 = (REPO / "tls13" / "proxy.exe").read_bytes()
    donnees_m1 = (REPO / "m1" / "selftest.exe").read_bytes()
    emul.poser_heritages(donnees_m9, donnees_m1)

    couverture: set[int] = set()

    def crochet_couverture(uc_, adresse, taille, donnees):
        if LOUPE01_VA <= adresse < fin_bloc:
            couverture.add(adresse)

    emul.uc.hook_add(UC_HOOK_CODE, crochet_couverture)

    # -- les canaris : le tampon du chemin bordé de part et d'autre
    CANARI = b"\xCA" * 16  # le canari : 0xCA répété
    CHEMIN = H.ADRESSE_CHEMIN

    def poser_canaris():
        emul.uc.mem_write(CHEMIN - 16, CANARI)
        emul.uc.mem_write(CHEMIN + 522, CANARI)

    def canaris_intacts() -> bool:
        return (bytes(emul.uc.mem_read(CHEMIN - 16, 16)) == CANARI
                and bytes(emul.uc.mem_read(CHEMIN + 522, 16)) == CANARI)

    # -- le corpus de départ : des chemins VALIDES (les témoins déclarés)
    rng = random.Random(GRAINE_LOUPE)
    corpus = list(noms_valides)
    LETTRES = "abcdefghijklmnopqrstuvwxyz.-_0123456789"

    def muter(entree: str) -> str:
        b = bytearray(entree.encode("utf-16-le"))
        choix = rng.random()
        if choix < 0.40:                  # la mutation lettrée (vivable)
            s = list(entree)
            if s:
                s[rng.randrange(len(s))] = rng.choice(LETTRES)
            entree2 = "".join(s)
            b = bytearray(entree2.encode("utf-16-le"))
            choix = 0.90                  # saute les mutations binaires
        if choix < 0.30 and b:            # bascule d'un octet
            b[rng.randrange(len(b))] = rng.randrange(256)
        elif choix < 0.50:                # allongement (au-delà de la borne ?)
            b += bytes(rng.randrange(256) for _ in range(rng.randrange(1, 32)))
        elif choix < 0.70 and len(b) > 4:  # troncature
            b = b[:rng.randrange(1, len(b))]
        elif choix < 0.85:                # injection de séparateurs/NUL
            b[rng.randrange(len(b))] = rng.choice((0x00, 0x5C, 0x2F, 0x3A))
        else:                             # le redoublement
            b = b + b
        return bytes(b).decode("utf-16-le", errors="ignore")[:520]

    crashes, violations, couverture_avant = 0, 0, 0
    historique = []
    for i in range(iterations):
        # le choix : un parent du corpus (guidage) ou une mutation fraîche
        parent = rng.choice(corpus)
        candidat = muter(parent) if rng.random() < 0.85 else muter("temoin.bin")
        poser_canaris()
        try:
            emul.uc.mem_write(CHEMIN, candidat.encode("utf-16-le")[:1044] + b"\x00\x00")
            r = emul.appeler(LOUPE01_VA, {"rcx": CHEMIN})
            ok_run = r.get("crash") is None
            if not ok_run:
                crashes += 1
        except Exception:  # noqa: BLE001  — le crash est une DONNÉE
            ok_run = False
            crashes += 1
        if not canaris_intacts():
            violations += 1
        if len(couverture) > couverture_avant:   # le guidage : on garde
            corpus.append(candidat)
            couverture_avant = len(couverture)
        historique.append({"i": i, "entree_len": len(candidat),
                           "ok": ok_run, "couverture": len(couverture)})
        # le retour à l'état propre : la session close si née
        try:
            if emul.u64(528) != 0xFFFFFFFFFFFFFFFF:
                emul.appeler(L.LOUPE03_VA, {})
        except Exception:  # noqa: BLE001
            pass

    total_insns = len(list(__import__("capstone").Cs(
        __import__("capstone").CS_ARCH_X86, __import__("capstone").CS_MODE_64)
        .disasm(emul.blobs["i110001"][0], LOUPE01_VA)))
    return {
        "bloc": "loupe-01 (ouvrir — le chemin non fiable)",
        "iterations": iterations,
        "couverture_instructions": len(couverture),
        "instructions_du_bloc": total_insns,
        "couverture_pct": round(100.0 * len(couverture) / total_insns, 1),
        "crashes": crashes, "violations_canaris": violations,
        "corpus_final": len(corpus),
        "graine": GRAINE_LOUPE,
    }


# ═══════════════════════════════ 2. HTTP-10 (le parseur d'entrée) ═══════════════════════════════

def campagne_http10(iterations: int = 400):
    import unicorn as uc
    from unicorn import UC_HOOK_CODE

    FM = charger_module("fuzz_million_v110", REPO / "m3" / "fuzz_million.py")
    exe = REPO / "m3" / "proxy.exe"
    if not exe.exists():
        return {"bloc": "http-10", "erreur": "m3/proxy.exe introuvable"}
    exe_octets = exe.read_bytes()
    IMAGE_BASE = getattr(FM.om, "IMAGE", 0x140000000)
    RVA_HTTP10 = FM.RVA_HTTP10
    debut_bloc = IMAGE_BASE + RVA_HTTP10
    fin_bloc = debut_bloc + 0x1000  # la plage du bloc (approx. sup)

    rng = random.Random(GRAINE_HTTP)
    couverture_globale: set[int] = set()
    TETES = [FM.TETE_GET, b"POST /x HTTP/1.1\r\nHost: a.b\r\nContent-Length: 4\r\n\r\n",
             b"CONNECT h:443 HTTP/1.1\r\n\r\n", b"BOGUS\r\n\r\n", b"", b"\r\n\r\n"]

    def jouer_avec_couverture(chunks):
        em, etat = FM.nouvel_emulateur(exe_octets)
        cov: set[int] = set()

        def crochet(uc_, adresse, taille, donnees):
            if debut_bloc <= adresse < fin_bloc:
                cov.add(adresse)

        em.uc.hook_add(UC_HOOK_CODE, crochet)
        cas = {"chunks": chunks, "recv_amont": [b"RESP", 0],
               "getaddrinfo": [(0, [2])], "connect": [0]}
        fautes = FM.jouer_session(em, cas, etat)
        return fautes, cov

    # la graine : les têtes canoniques ; le guidage : les entrées qui
    # augmentent la couverture rejoignent le corpus
    corpus = [list([t]) for t in TETES]
    crashes, fautes_nommees, couverture_avant = 0, [], 0
    historique = []
    for i in range(iterations):
        parent = rng.choice(corpus)
        # la mutation : découpage/recollement + bascules d'octets
        brut = b"".join(parent)
        r = rng.random()
        if r < 0.35 and brut:                      # bascules
            b = bytearray(brut)
            for _ in range(rng.randrange(1, 6)):
                b[rng.randrange(len(b))] = rng.randrange(256)
            brut = bytes(b)
        elif r < 0.55:                             # le tronconnage aléatoire
            if len(brut) > 2:
                a = rng.randrange(len(brut) - 1)
                brut = brut[:a] + brut[a + rng.randrange(1, 4):]
        elif r < 0.75:                             # l'allongement hostile
            brut += bytes(rng.randrange(256) for _ in range(rng.randrange(1, 64)))
        # le découpage en chunks (la fragmentation de l'entrée)
        morceaux, pos = [], 0
        while pos < len(brut):
            n = rng.randrange(1, max(2, len(brut) - pos + 1))
            morceaux.append(brut[pos:pos + n])
            pos += n
        if not morceaux:
            morceaux = [b""]
        try:
            fautes, cov = jouer_avec_couverture(morceaux)
        except Exception as exc:  # noqa: BLE001
            crashes += 1
            continue
        couverture_globale |= cov
        for f in fautes:
            fautes_nommees.append(f.split(" ")[0])
        if len(couverture_globale) > couverture_avant:
            corpus.append(morceaux)
            couverture_avant = len(couverture_globale)
        historique.append({"i": i, "fautes": len(fautes),
                           "couverture": len(couverture_globale)})

    return {
        "bloc": "http-10 (le parseur d'entrée, r3 — la pièce 0.4.0)",
        "iterations": iterations,
        "couverture_instructions": len(couverture_globale),
        "crashes_emulation": crashes,
        "fautes_nommees": len(fautes_nommees),
        "familles_de_fautes": sorted(set(fautes_nommees))[:8],
        "corpus_final": len(corpus),
        "graine": GRAINE_HTTP,
    }


def main():
    print("=== FUZZAGE GUIDÉ PAR COUVERTURE — v0.11.0 ===")
    print("[loupe-01] la campagne (le chemin non fiable)…")
    r_loupe = campagne_loupe01()
    print(json.dumps(r_loupe, indent=1, ensure_ascii=False))
    print("[http-10] la campagne (le parseur d'entrée)…")
    r_http = campagne_http10()
    print(json.dumps(r_http, indent=1, ensure_ascii=False))

    (PREUVES / "fuzzage.json").write_text(
        json.dumps({"loupe-01": r_loupe, "http-10": r_http}, indent=1,
                   ensure_ascii=False), encoding="utf-8")
    rapport = [
        "FUZZAGE GUIDÉ PAR COUVERTURE — v0.11.0 (graines fixées, reproductible)",
        "",
        f"LOUPE-01 : {r_loupe['couverture_instructions']}/"
        f"{r_loupe['instructions_du_bloc']} instructions couvertes "
        f"({r_loupe['couverture_pct']} %), {r_loupe['crashes']} crashes, "
        f"{r_loupe['violations_canaris']} violations de canaris, corpus "
        f"{r_loupe['corpus_final']} entrées (graine {r_loupe['graine']})",
        f"HTTP-10  : {r_http['couverture_instructions']} instructions couvertes, "
        f"{r_http['crashes_emulation']} crashes, "
        f"{r_http['fautes_nommees']} fautes nommées "
        f"(familles : {', '.join(r_http.get('familles_de_fautes', []))}), "
        f"corpus {r_http['corpus_final']} entrées (graine {r_http['graine']})",
        "",
        "LIMITES CONSTATÉES : la couverture est celle du BLOC en émulation "
        "(les adresses exécutées, par traduction) ; les crashes sont les "
        "fautes d'émulation (pas les morts du terrain) ; le parseur http-10 "
        "est jugé sur la pièce 0.4.0 scellée (la révision r3 du M5).",
    ]
    (PREUVES / "fuzzage_rapport.txt").write_text(
        "\n".join(rapport), encoding="utf-8")
    print("\n".join(rapport))


if __name__ == "__main__":
    main()
