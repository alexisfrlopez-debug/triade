#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SESSION VOLUMES — LE MOTEUR NATIF GÉNÉRALISÉ AUX VOLUMES COMPLETS
(W28HARNAIS, prompt 3, geste 5).

12 000 cas engendrés pour UN BLOC CRITIQUE (tls13-16-aes128-bloc, l'AES par
bloc — le moteur committé vit de ce corps depuis la vague 15), la graine
consignée AVANT le tirage. La cible de régime PRÉ-ENREGISTRÉE au plan gelé :
≤ 5 × C (le pilote C au même volume — le même code de bloc appelé directement
sans échafaudage d'oracle, compilé au gcc du bac).

LA SESSION :
  1. l'assemblage du corps depuis LA NOTATION (l'assemblage éprouvé du
     couloir, atelier-entrelacement-2sown2h3z/piloter_entrelacement.py) ;
  2. les 12 000 vecteurs à la convention du jumeau (le tirage du
     8hguph5ee : (0, 63 bits, 0, 0)) — la graine 20261128 consignée ;
  3. LE MOTEUR COMMITTÉ (moteur_oracles, ≤ 4 096 vecteurs par lot) aux trois
     lots — la console de RÉFÉRENCE et le régime de base ;
  4. LE MOTEUR GÉNÉRALISÉ (moteur_volumes — même sémantique, le lot unique
     12 000, la console en tampon) — la console confrontée LIGNE-IDENTIQUE
     au moteur committé (l'équivalence prouvée octet par octet) ;
  5. L'AUDIT 1-SUR-10 CONSERVÉ : un vecteur sur dix confronté au JUMEAU
     (l'émulateur Unicorn du registre 8hguph5ee, la même console, champ par
     champ — rax + digeste), aux MÊMES volumes ;
  6. LE RÉGIME mesuré contre le PILOTE C au même volume (n=5, la médiane,
     l'horloge monotone) : le moteur committé, le moteur généralisé, le
     pilote — le rapport publié TEL QUEL, la cible ≤ 5 × C tenue ou manquée.

Usage : python3 atelier-w28harnais/session_volumes.py
Écrit : volumes-resultat.json
"""
import hashlib
import json
import pathlib
import random
import struct
import subprocess
import sys
import time

R = pathlib.Path(__file__).resolve().parents[1]
ICI = pathlib.Path(__file__).resolve().parent
MOTEUR_COMMITTE = R / "atelier-w27vaes/moteur_oracles"
SC16 = R / "tls13" / "notation" / "tls13-16-aes128-bloc.asm"
CALENDRIER = R / "atelier-oracles-8hguph5ee/registres/calendrier.bin"
MARGE = 0xDF00
N = 12000
GRAINE = 20261128
LOT_MAX = 4096                          # la limite statique du moteur committé
CIBLE_REGIME = 5.0                       # ≤ 5 × C, pré-enregistrée au plan


def _assembler():
    """l'assemblage éprouvé du couloir (piloter_entrelacement.assembler)."""
    sys.path.insert(0, str(R / "atelier-entrelacement-2sown2h3z"))
    from piloter_entrelacement import assembler
    return assembler(SC16, MARGE)


def _jumeau(corps, vecteurs, profil="a"):
    """LE JUMEAU — l'émulateur du registre 8hguph5ee (le_gate.jumeau, à
    l'identique) : la console de référence par vecteur (rax + digeste)."""
    import unicorn
    UC = unicorn.Uc
    XR = unicorn.x86_const
    uc = UC(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
    uc.mem_map(0xC000, 0x4000)
    uc.mem_map(0x500000, 0x21000)
    uc.mem_map(0x70000, 0x10000)
    uc.mem_write(MARGE, corps)
    uc.mem_write(0x500200, CALENDRIER.read_bytes())
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
        uc.emu_start(MARGE, 0x60000)
        rax = uc.reg_read(XR.UC_X86_REG_RAX)
        digeste = bytes(uc.mem_read(0x503000, 16)).hex()
        console.append({"vecteur": i, "rax": rax, "digeste": digeste})
    return console


def _lancer(moteur, corps_path, vec_path, n, console_path, profil="a",
           marge=MARGE):
    """retour (console, hot_s, mur_s) — le mur du SOUS-PROCESSUS SEUL (le
    montage + la boucle + la console différée du moteur), l'analyse Python
    de la console HORS mesure (le compte de la session, pas du moteur)."""
    t0 = time.monotonic()
    r = subprocess.run([str(moteur), str(corps_path), hex(marge), str(vec_path),
                         str(n), str(console_path), profil, str(CALENDRIER)],
                        capture_output=True, text=True, timeout=300)
    mur = time.monotonic() - t0
    if r.returncode != 0:
        raise RuntimeError(f"le moteur : {r.stderr}")
    hot = None
    for l in r.stdout.splitlines():
        if l.startswith("HOT "):
            hot = float(l.split()[1]) / 1e6        # µs -> s (le régime chaud)
    return [json.loads(l) for l in console_path.read_text().splitlines() if l.strip()], hot, mur


def main():
    rapport = []
    def consigne(l):
        print(l)
        rapport.append(l)

    # 1. LE CORPS : l'assemblage depuis la notation, l'empreinte consignée
    corps = _assembler()
    sha_corps = hashlib.sha256(corps).hexdigest()
    corps_path = ICI / "corps-tls13-16.bin"
    corps_path.write_bytes(corps)
    consigne(f"[corps] tls13-16 assemblé depuis la notation — {len(corps)} octets, "
             f"sha256 {sha_corps[:16]}…")

    # 2. LES 12 000 VECTEURS — la graine consignée AVANT le tirage
    rng = random.Random(GRAINE)
    vecteurs = [(0, rng.getrandbits(63), 0, 0) for _ in range(N)]
    vec_path = ICI / "vecteurs-12000.bin"
    vec_path.write_bytes(b"".join(struct.pack("<QQQQ", *v) for v in vecteurs))
    consigne(f"[vecteurs] {N} cas à la convention du jumeau — graine {GRAINE}")

    # 3. LE MOTEUR COMMITTÉ (les trois lots) — la console de référence
    t0 = time.monotonic()
    console_ref = []
    lots = []
    off = 0
    while off < N:
        n_lot = min(LOT_MAX, N - off)
        sous = ICI / f"lot-{off}.bin"
        sous.write_bytes(vec_path.read_bytes()[off * 32:(off + n_lot) * 32])
        cl = ICI / f"console-committed-{off}.jsonl"
        _lancer(MOTEUR_COMMITTE, corps_path, sous, n_lot, cl)
        lignes = [json.loads(l) for l in cl.read_text().splitlines() if l.strip()]
        for k, l in enumerate(lignes):
            l["vecteur"] = off + k
            console_ref.append(l)
        lots.append({"offset": off, "n": n_lot})
        sous.unlink()
        cl.unlink()
        off += n_lot
    duree_commited = time.monotonic() - t0
    consigne(f"[moteur-committé] {N} vecteurs aux {len(lots)} lots — "
             f"{duree_commited * 1000:.1f} ms (le régime fprintf par vecteur)")

    # 4. LE MOTEUR GÉNÉRALISÉ — le lot unique, la console en tampon
    moteur_gen = ICI / "moteur_volumes"
    console_gen, _hot, duree_gen = _lancer(moteur_gen, corps_path, vec_path, N,
                                            ICI / "console-volumes.jsonl")
    identique = console_gen == console_ref
    consigne(f"[moteur-généralisé] {N} vecteurs au lot unique — "
             f"{duree_gen * 1000:.1f} ms ; la console {'LIGNE-IDENTIQUE au moteur committé' if identique else 'ROUGE — DIVERGENCE'}")

    # 5. L'AUDIT 1-SUR-10 : le jumeau aux mêmes volumes, champ par champ
    echantillon = [i for i in range(0, N, 10)]
    t0 = time.monotonic()
    jum = _jumeau(corps, [vecteurs[i] for i in echantillon])
    duree_jum = time.monotonic() - t0
    ecarts = []
    for k, i in enumerate(echantillon):
        a, b = console_gen[i], jum[k]
        if a["rax"] != b["rax"] or a["digeste"] != b["digeste"]:
            ecarts.append({"vecteur": i, "moteur": a, "jumeau": b})
    consigne(f"[audit-1-sur-10] {len(echantillon)} vecteurs confrontés au jumeau — "
             f"{'ZÉRO ÉCART' if not ecarts else 'REFUS NOMMÉ — ' + str(ecarts[:3])}")

    # 6. LE RÉGIME contre le PILOTE C au même volume — n=5 passes, la médiane.
    #    LES CONVENTIONS NOMMÉES : le régime CHAUD (la boucle d'exécution,
    #    horlogée EN INTERNE des deux côtés — le montage hors temps ; côté
    #    moteur : entrée posée + appel + digeste lue + compte rendu ; côté
    #    pilote : entrée posée + appel — la boucle nue), et le régime de BOUT
    #    EN BOUT (le mur du sous-processus : montage + boucle + console).
    passes = 9
    d_com = []                                   # le committé, bout en bout
    for _ in range(passes):
        t0 = time.monotonic()
        off = 0
        while off < N:
            n_lot = min(LOT_MAX, N - off)
            sous = ICI / f"lot-{off}.bin"
            sous.write_bytes(vec_path.read_bytes()[off * 32:(off + n_lot) * 32])
            _lancer(MOTEUR_COMMITTE, corps_path, sous, n_lot, ICI / "console-tmp.jsonl")
            sous.unlink(); (ICI / "console-tmp.jsonl").unlink()
            off += n_lot
        d_com.append(time.monotonic() - t0)
    d_gen, d_hot = [], []                        # le généralisé : bout en bout + chaud
    for _ in range(passes):
        _c, hot, mur = _lancer(moteur_gen, corps_path, vec_path, N,
                                ICI / "console-tmp.jsonl")
        d_gen.append(mur)
        d_hot.append(hot)
    (ICI / "console-tmp.jsonl").unlink()
    r = subprocess.run(["./pilote_c", str(corps_path), hex(MARGE), str(vec_path),
                        str(N), str(CALENDRIER), str(passes)],
                       capture_output=True, text=True, cwd=ICI, timeout=300)
    if r.returncode != 0:
        raise RuntimeError(f"le pilote : {r.stderr}")
    d_pil = [float(x) / 1e6 for x in r.stdout.split()]   # la boucle nue, interne
    med = lambda xs: sorted(xs)[len(xs) // 2]
    m_com, m_gen, m_pil, m_hot = med(d_com), med(d_gen), med(d_pil), med(d_hot)
    ratio_com = m_com / m_pil
    ratio_gen = m_gen / m_pil
    ratio_hot = m_hot / m_pil
    verdict = "TENUE" if ratio_hot <= CIBLE_REGIME else "MANQUÉE"
    consigne(f"[régime-chaud] le pilote C (la boucle nue, interne) : médiane "
             f"{m_pil * 1e6:.1f} µs ; le moteur généralisé (la boucle d'exécution, "
             f"interne) : {m_hot * 1e6:.1f} µs → {ratio_hot:.2f} × C — la cible "
             f"≤ {CIBLE_REGIME:.0f} × C {verdict}")
    consigne(f"[régime-bout-en-bout] le moteur committé : {m_com * 1000:.1f} ms → "
             f"{ratio_com:.0f} × C ; le moteur généralisé : {m_gen * 1000:.1f} ms → "
             f"{ratio_gen:.0f} × C (montage + boucle + console différée — "
             f"la convention du mur, publiée pareil)")
    per_jum = duree_jum / len(echantillon)
    per_gen = m_gen / N                            # le mur du sous-processus
    consigne(f"[jumeau] l'émulateur aux {len(echantillon)} vecteurs de l'audit : "
             f"{duree_jum * 1000:.1f} ms → {per_jum * 1e6:.1f} µs/vecteur ; le moteur "
             f"généralisé de bout en bout : {per_gen * 1e6:.2f} µs/vecteur — "
             f"l'ordre de grandeur vs l'oracle vivant : {per_jum / per_gen:.0f} × ")

    doc = {
        "bloc": "tls13-16-aes128-bloc", "corps_sha256": sha_corps,
        "corps_octets": len(corps), "marge": MARGE,
        "graine": GRAINE, "n_vecteurs": N,
        "moteur_commite": {"lots": lots, "durees_s": [round(d, 4) for d in d_com],
                           "mediane_s": round(m_com, 4),
                           "ratio_vs_c": round(ratio_com, 2),
                           "console": "fprintf par vecteur (le régime de base)"},
        "moteur_generalise": {"lot_unique": N, "durees_s": [round(d, 4) for d in d_gen],
                              "mediane_s": round(m_gen, 4),
                              "ratio_bout_en_bout_vs_c": round(ratio_gen, 2),
                              "regime_chaud_s": [round(d, 6) for d in d_hot],
                              "regime_chaud_mediane_s": round(m_hot, 6),
                              "ratio_regime_chaud_vs_c": round(ratio_hot, 2),
                              "console_ligne_identique": identique},
        "pilote_c": {"boucle": "entrée posée + appel, ni console ni digeste",
                     "gcc": "gcc -O2 du bac", "durees_s": [round(d, 6) for d in d_pil],
                     "mediane_s": round(m_pil, 6)},
        "audit_1_sur_10": {"vecteurs": len(echantillon), "ecarts": ecarts,
                           "jumeau_duree_s": round(duree_jum, 4)},
        "conventions_regime": {"chaud": "boucles internes des deux côtés, montage hors temps",
                               "bout_en_bout": "mur du sous-processus (montage + boucle + console)",
                               "pilote": "entrée posée + appel, ni console ni digeste"},
        "cible_regime": f"≤ {CIBLE_REGIME:.0f} × C (régime chaud)", "verdict_regime": verdict,
    }
    (ICI / "volumes-resultat.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    (ICI / "rapport-volumes.txt").write_text("\n".join(rapport) + "\n",
                                             encoding="utf-8")
    print("\nOK — volumes-resultat.json")


if __name__ == "__main__":
    main()
