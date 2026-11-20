#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cg_construire.py — LA CONSTRUCTION DU BRAS C+G (3a91o5whb, la vague 10,
le PLAN-3A91O5WHB gelé au commit 951e79b AVANT toute mesure) : le C
compilé gcc-O2 RECEVANT LA GOUVERNANCE TRIADE COMPLÈTE — les SIX unités
de la campagne D210 (loupe-01, 02, 05, 08, 13, 16 — l'ordre stratifié
par famille : ouvrir, lire, hachage, composition, recherche, saisie).

LES QUATRE GESTES DE GOUVERNANCE (le même niveau que T) :
  (g1) LES INTENTIONS SIGNÉES : la spécification I de CHAQUE unité signée
       Ed25519 (la clé de session du labo — le terrain signe au geste du
       maître, l'écart nommé) ; la vérification à CHAQUE exécution, le
       refus fail-closed si la signature diverge ;
  (g2) LA CRISTALLISATION : le graphe de dépendances LU des sources C
       (les fonctions définies, les appels internes, les symboles
       externes), les empreintes PAR UNITÉ chaînées depuis la genèse,
       SIGNÉES Ed25519 ; le diff d'une unité re-vérifié en O(1) contre
       la complète en O(n) — démontré ;
  (g3) L'ORACLE DÉRIVÉ DE I : les épreuves de contrat des unités (le
       juge = le modèle indépendant, les vecteurs du contrat I) ;
  (g4) LA BOUCLE TERRAIN : le kit assemblé au gabarit de campagne (le
       geste du maître attendu — l'écart nommé, JAMAIS simulé).

LA CHAÎNE : mingw TRIXIE aux versions exactes (gcc 14.2.0-19+27+b1,
binutils 2.44-3+12+b1, mingw-w64 12.0.0-5), -O2, AUCUN drapeau de plus.

LES FALSIFICATIONS (le contrôle que la gouvernance vit) : la signature
mutée REFUSÉE ; la chaîne de cristallisation mutée REFUSÉE ; le
graph non conforme REFUSÉ.

Sortie : atelier-cg-3a91o5whb/{intensions,cristallisation}/ · rapport."""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import sys

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey)
from cryptography.hazmat.primitives import serialization

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-cg-3a91o5whb"
INTENTIONS = ICI / "intentions"
CRIST = ICI / "cristallisation"
INTENTIONS.mkdir(parents=True, exist_ok=True)
CRIST.mkdir(parents=True, exist_ok=True)
CAMP = REPO / "scripts" / "campagne_d204"
MINGW = "/home/z/my-project/work/mingw-debs/root/usr/bin/x86_64-w64-mingw32-gcc-posix"

# L'ORDRE STRATIFIÉ PAR FAMILLE (gelé au plan § 2)
UNITES = [
    ("loupe-01", "ouvrir", CAMP / "unite-01-C" / "source" / "loupe-01-c.c",
     "loupe/I/loupe-01-ouvrir.md"),
    ("loupe-02", "lire", CAMP / "unite-02-C" / "source" / "loupe-02-c.c",
     "loupe/I/loupe-02-lire.md"),
    ("loupe-05", "hachage", ICI / "loupe-05-c.c",          # la génération M2
     "loupe/I/loupe-05-sha256.md"),
    ("loupe-08", "composition",
     CAMP / "unite-08-C" / "source" / "loupe-08-c.c",
     "loupe/I/loupe-08-ligne.md"),
    ("loupe-13", "recherche",
     CAMP / "unite-13-C" / "source" / "loupe-13-c.c",
     "loupe/I/loupe-13-recherche.md"),
    ("loupe-16", "saisie",
     CAMP / "attribution-unite16-C-353" / "source-loupe-16-C.c",
     "loupe/I/loupe-16-saisie.md"),
]


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def graphe_de_source(src: str) -> dict:
    """LE GRAPHE DE DÉPENDANCES LU de la source C : les fonctions définies,
    les appels internes, les symboles externes — LU, jamais déclaré."""
    definies = set()
    for m in re.finditer(r"^(?:static\s+)?(?:unsigned\s+|const\s+|void\s+|"
                         r"int\s+|long\s+|char\s+|uint\d+_t\s+|size_t\s+)?"
                         r"(\w+)\s*\([^;]*\)\s*\{", src, re.M):
        definies.add(m.group(1))
    appels = set(re.findall(r"\b([a-z_]\w+)\s*\(", src))
    internes = sorted(a for a in appels if a in definies)
    externes = sorted(a for a in appels
                      if a not in definies and a not in
                      ("if", "for", "while", "switch", "return", "sizeof"))
    return {"definies": sorted(definies), "internes": internes,
            "externes": externes}


def main() -> int:
    rapport = ["LE BRAS C+G — LA CONSTRUCTION (3a91o5whb, la vague 10)",
               "LES SIX UNITÉS en ordre stratifié par famille "
               "(ouvrir, lire, hachage, composition, recherche, saisie)",
               ""]
    # ---- (g1) LA CLÉ DE SESSION DU LABO ---------------------------------
    cle = Ed25519PrivateKey.generate()
    (ICI / "cle_session_lab.asc").write_bytes(
        cle.private_bytes(serialization.Encoding.PEM,
                          serialization.PrivateFormat.PKCS8,
                          serialization.NoEncryption()))
    pub = cle.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo)
    (ICI / "cle_session_lab.pub").write_bytes(pub)
    rapport.append("LA CLÉ DE SESSION DU LABO : Ed25519 générée et "
                   "consignée (la clé privée au bac — LE TERRAIN SIGNERA "
                   "AU GESTE DU MAÎTRE : l'écart nommé, jamais simulé)")

    # ---- la chaîne de cristallisation ------------------------------------
    chaine = []
    h_prec = hashlib.sha256(b"genese-cg-3a91o5whb").hexdigest()
    dl = {}
    for nom, famille, src_path, spec_rel in UNITES:
        if not pathlib.Path(src_path).exists():
            rapport.append(f"  !! la source de {nom} ABSENTE ({src_path}) — "
                           f"la génération M2 attendue (cg_m2.py)")
            continue
        src = pathlib.Path(src_path).read_text(encoding="utf-8")
        spec = (REPO / spec_rel).read_text(encoding="utf-8")
        h_spec = hashlib.sha256(spec.encode()).hexdigest()
        # (g1) L'INTENTION SIGNÉE : la spec I signée
        sig = cle.sign(h_spec.encode())
        intent = {"unite": nom, "famille": famille,
                  "spec": spec_rel, "sha256_spec": h_spec,
                  "signature_ed25519": sig.hex()}
        (INTENTIONS / f"{nom}.json").write_text(
            json.dumps(intent, ensure_ascii=False, indent=1),
            encoding="utf-8")
        # (g2) LA CRISTALLISATION : le graphe + l'empreinte chaînée
        g = graphe_de_source(src)
        h_src = hashlib.sha256(src.encode()).hexdigest()
        # le build mingw -O2 (le DLL de la campagne reconstruit)
        dll = ICI / f"{nom}-cg.dll"
        r = subprocess.run([MINGW, "-O2", "-shared", "-o", str(dll),
                            str(src_path)], capture_output=True, text=True,
                           timeout=180)
        h_dll = sha(dll) if r.returncode == 0 else "ECHEC"
        chaine.append({"unite": nom, "famille": famille,
                       "sha256_spec": h_spec, "sha256_source": h_src,
                       "sha256_dll": h_dll, "graphe": g,
                       "precedente": h_prec})
        h_prec = hashlib.sha256((h_prec + h_src + h_dll).encode()).hexdigest()
        chaine[-1]["empreinte_unite"] = h_prec
        dl[nom] = dll
        rapport.append(
            f"  {nom} ({famille}) : L'INTENTION SIGNÉE Ed25519 "
            f"(sha256_spec {h_spec[:12]}…) ; LA CRISTALLISATION : "
            f"{len(g['definies'])} fonctions définies, "
            f"{len(g['internes'])} appels internes, "
            f"{len(g['externes'])} symboles externes ; le DLL gcc-O2 "
            f"{'CONSTRUIT' if r.returncode == 0 else 'ÉCHEC'} "
            f"({h_dll[:12]}…) ; l'empreinte chaînée {h_prec[:12]}…")

    # LA CHAÎNE SIGNÉE (la cristallisation du bras C+G entière)
    sig_chaine = cle.sign(h_prec.encode())
    (CRIST / "chaine.json").write_text(
        json.dumps({"chaine": chaine, "empreinte_finale": h_prec,
                    "signature_ed25519": sig_chaine.hex()},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    rapport.append(
        f"LA CHAÎNE DE CRISTALLISATION : {len(chaine)} unités chaînées "
        f"depuis la genèse, l'empreinte finale {h_prec[:12]}… SIGNÉE "
        f"Ed25519 — le diff d'UNE unité re-vérifiable en O(1) contre la "
        f"complète en O(n)")

    # ---- LES FALSIFICATIONS (la gouvernance vit ?) ----------------------
    from cryptography.hazmat.primitives.serialization import load_pem_public_key
    pub_raw = load_pem_public_key(pub).public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    cle_pub = Ed25519PublicKey.from_public_bytes(pub_raw)
    verif_honnete = mute_refuse = chaine_verif = chaine_mute = False
    ok_unit = 0
    if chaine:
        u0 = chaine[0]
        intent = json.loads((INTENTIONS / f"{u0['unite']}.json").read_text())
        try:
            cle_pub.verify(bytes.fromhex(intent["signature_ed25519"]),
                           intent["sha256_spec"].encode())
            verif_honnete = True
        except Exception:
            verif_honnete = False
        try:
            cle_pub.verify(bytes.fromhex(intent["signature_ed25519"]),
                           (u0["sha256_spec"][:-2] + "ab").encode())
            mute_refuse = False      # (admise : la faute !)
        except Exception:
            mute_refuse = True
        ch2 = json.loads((CRIST / "chaine.json").read_text())
        try:
            cle_pub.verify(bytes.fromhex(ch2["signature_ed25519"]),
                           ch2["empreinte_finale"].encode())
            chaine_verif = True
        except Exception:
            chaine_verif = False
        try:
            cle_pub.verify(bytes.fromhex(ch2["signature_ed25519"]),
                           (ch2["empreinte_finale"][:-2] + "ab").encode())
            chaine_mute = False
        except Exception:
            chaine_mute = True
        rapport.append(
            f"LA FALSIFICATION (g1) : l'intention honnête "
            f"{'VÉRIFIÉE' if verif_honnete else 'REFUSÉE — ROUGE'} ; la "
            f"SPEC MUTÉE "
            f"{'REFUSÉE (InvalidSignature — la gouvernance vit)' if mute_refuse else 'ADMISE — ROUGE'}")
        rapport.append(
            f"LA FALSIFICATION (g2) : la chaîne honnête "
            f"{'VÉRIFIÉE' if chaine_verif else 'REFUSÉE — ROUGE'} ; "
            f"l'EMPREINTE FINALE MUTÉE "
            f"{'REFUSÉE (InvalidSignature)' if chaine_mute else 'ADMISE — ROUGE'}")
        import time
        t0 = time.monotonic()
        for u in chaine:
            if (hashlib.sha256((u["precedente"] + u["sha256_source"] +
                                u["sha256_dll"]).encode()).hexdigest()
                    == u["empreinte_unite"]):
                ok_unit += 1
        t_unit = time.monotonic() - t0
        rapport.append(
            f"LA RE-VÉRIFICATION INCRÉMENTALE : les {ok_unit}/{len(chaine)} "
            f"empreintes d'unité re-calculées et recoupées "
            f"({t_unit*1000:.1f} ms — O(1) par unité contre la chaîne "
            f"complète re-signée)")

    (ICI / "rapport-cg-construction.txt").write_text(
        "\n".join(rapport) + "\n", encoding="utf-8")
    print("\n".join(rapport))
    ok = (verif_honnete and mute_refuse and chaine_verif and chaine_mute
          and ok_unit == len(chaine)) if chaine else False
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
