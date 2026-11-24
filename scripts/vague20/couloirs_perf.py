#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LES COULOIRS DE PERFORMANCE, PRÉ-ENREGISTRÉS PUIS MESURÉS (W20PERF).

Environnement consigné (modèle, fréquence, drapeaux CPUID, affinité), n ≥ 20, médiane et
IQR. Trois couloirs :
  (a) AES-GCM spécialisé VAES/VPCLMULQDQ — PRÉ-ENREGISTRÉ ; mesure du seul RÉFÉRENTIEL
      disponible ici (OpenSSL via `cryptography`), la spécialisation restant un geste machine
      réelle (aucun code VAES écrit dans ce bac) ;
  (b) recherche d'octets AVX2 à CPUID hissé contre memchr — MESURÉE (harnais C, rdtsc) ;
  (c) spécialisation des onze gardes — PRÉ-ENREGISTRÉE, EN ATTENTE (le corridor scellé n'est
      pas modifié ici).

Usage : python3 scripts/vague20/couloirs_perf.py [--preregistrer|--mesurer]
"""
import json, os, pathlib, platform, statistics, subprocess, sys, tempfile, time

R = pathlib.Path(__file__).resolve().parents[2]
DOSSIER = R / "atelier-w20-perf"
GRAINE = 20261124
N = 20
CIBLE_RECHERCHE = 561      # cycles, recherche absente de 4 096 octets (idiome memchr)


def environnement():
    cpuinfo = pathlib.Path("/proc/cpuinfo").read_text()
    modele = next((l.split(":", 1)[1].strip() for l in cpuinfo.splitlines() if l.startswith("model name")), "?")
    mhz = next((l.split(":", 1)[1].strip() for l in cpuinfo.splitlines() if l.startswith("cpu MHz")), "?")
    drapeaux = set()
    for l in cpuinfo.splitlines():
        if l.startswith("flags"):
            drapeaux = set(l.split(":", 1)[1].split())
            break
    return {"modele": modele, "mhz": mhz, "nproc": os.cpu_count(),
            "drapeaux": {k: (k in drapeaux) for k in ("aes", "avx2", "pclmulqdq", "vaes", "vpclmulqdq")},
            "noyau_epingle": sorted(os.sched_getaffinity(0))[:1]}


C_HARNAIS = (R / "scripts/vague20/harnais_recherche.c").read_text(encoding="utf-8")


def mesurer_recherche():
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="triade-perf-"))
    src = tmp / "h.c"; src.write_text(C_HARNAIS, encoding="utf-8")
    exe = tmp / "h"
    subprocess.run(["gcc", "-O2", "-mavx2", "-o", str(exe), str(src)], check=True, capture_output=True)
    essais = []
    for _ in range(N):
        out = subprocess.run([str(exe)], capture_output=True, text=True, check=True).stdout.split()
        essais.append((float(out[0]), float(out[1])))
    memchr = sorted(a for a, _ in essais); avx2 = sorted(b for _, b in essais)
    def med_iqr(x):
        m = statistics.median(x); q = statistics.quantiles(x, n=4); return m, q[2] - q[0]
    m1, i1 = med_iqr(memchr); m2, i2 = med_iqr(avx2)
    return {"n": N, "memchr_median_cycles": m1, "memchr_iqr": i1,
            "avx2_median_cycles": m2, "avx2_iqr": i2,
            "cible_cycles": CIBLE_RECHERCHE,
            "cible_tenue": m2 <= CIBLE_RECHERCHE,
            "ratio_avx2_sur_memchr": m2 / m1}


def reference_aesgcm():
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except Exception as e:
        return {"statut": "REFUS-INSTRUMENT", "motif": str(e)[:80]}
    cle = b"\x00" * 32; nonce = b"\x00" * 12; clair = b"\x41" * 4096
    a = AESGCM(cle)
    for _ in range(100):
        a.encrypt(nonce, clair, None)
    mesures = []
    for _ in range(N):
        t = time.perf_counter_ns(); a.encrypt(nonce, clair, None); mesures.append((time.perf_counter_ns() - t))
    med = statistics.median(mesures)
    mhz = 2800.0
    return {"n": N, "mediane_ns_4kio": med, "cycles_par_octet_estimes": (med * mhz / 1000.0) / 4096,
            "note": "référentiel OpenSSL mesuré ici (machine virtuelle) ; la spécialisation "
                    "VAES/VPCLMULQDQ est PRÉ-ENREGISTRÉE et reste un geste machine réelle"}


def preregistrer():
    DOSSIER.mkdir(exist_ok=True)
    doc = {"graine": GRAINE, "n": N, "environnement": environnement(),
           "couloirs": {
               "a_aesgcm_vaes": {"cible": "≤ 0,6 c/octet à 4 Kio", "statut": "PRE-ENREGISTRE — mesure du seul référentiel"},
               "b_recherche_avx2": {"cible": f"≤ {CIBLE_RECHERCHE} cycles par recherche absente de 4 096 o", "statut": "A MESURER"},
               "c_gardes_onze": {"cible": "22→7 instructions/appel sans croissance du TCB", "statut": "PRE-ENREGISTRE — EN ATTENTE (corridor scellé non modifié)"}}}
    f = DOSSIER / "preregistrement.json"
    f.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[preregistre] {f.relative_to(R)}")
    return 0


def mesurer():
    DOSSIER.mkdir(exist_ok=True)
    env = environnement()
    rec = {"environnement": env, "recherche": mesurer_recherche(), "aesgcm_reference": reference_aesgcm()}
    (DOSSIER / "mesure-couloirs.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    r = rec["recherche"]
    print(f"[couloir b] AVX2 {r['avx2_median_cycles']:.1f} c (IQR {r['avx2_iqr']:.1f}) vs memchr "
          f"{r['memchr_median_cycles']:.1f} c (IQR {r['memchr_iqr']:.1f}) · cible ≤{CIBLE_RECHERCHE} → "
          f"{'TENUE' if r['cible_tenue'] else 'MANQUÉE'} · ratio {r['ratio_avx2_sur_memchr']:.2f}×")
    a = rec["aesgcm_reference"]
    if "mediane_ns_4kio" in a:
        print(f"[couloir a] référentiel OpenSSL 4 Kio : médiane {a['mediane_ns_4kio']:.0f} ns ≈ "
              f"{a['cycles_par_octet_estimes']:.3f} c/octet (machine virtuelle) — spécialisation PRÉ-ENREGISTRÉE")
    return 0


if __name__ == "__main__":
    if "--preregistrer" in sys.argv: sys.exit(preregistrer())
    if "--mesurer" in sys.argv: sys.exit(mesurer())
    preregistrer(); mesurer()
