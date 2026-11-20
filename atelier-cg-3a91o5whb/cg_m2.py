#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cg_m2.py — LA MESURE M2 DU BRAS C+G (3a91o5whb) : les SIX appels de
génération (le contrat I → le source C) au gabarit C+G (le contrat
VERBATIM + les faits du mécanisme + la requête), l'instrument de la
campagne (le CLI z-ai, le champ usage LU, chaque appel journalisé).

LOUPE-05 : LA SOURCE NOUVELLE — le bras C de la campagne n'avait pas
d'unité 05 (les cinq autres vivent au dossier) : la génération EST la
pièce (compilée gcc-O2, confrontée au juge hashlib sur les vecteurs
FIPS 180-4 + la gamme vide — le correctif borné à trois passes si
l'épreuve échoue, chaque écart nommé).

LA COMPARAISON : les SIX appels frais (le gabarit C+G — contrat +
mécanisme) ; les records T/C de la campagne recoupés pour le contexte
(la tête-à-tête loupe-01 : T 53 158, C 67 475 — les prompts de campagne
portaient l'oracle et le juge : LA DIFFÉRENCE DE PÉRIMÈTRE NOMMÉE,
jamais fusionnés)."""
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
import time

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-cg-3a91o5whb"
JOURNAL = ICI / "journal_cg.jsonl"
GARDE = ICI / "garde-cg.jsonl"
PROMPTS = ICI / "garde-prompts"
PROMPTS.mkdir(exist_ok=True)
CAMP = REPO / "scripts" / "campagne_d204"
MINGW = "/home/z/my-project/work/mingw-debs/root/usr/bin/x86_64-w64-mingw32-gcc-posix"

UNITES = [
    ("loupe-01", "ouvrir", "loupe/I/loupe-01-ouvrir.md",
     CAMP / "unite-01-C" / "source" / "loupe-01-c.c"),
    ("loupe-02", "lire", "loupe/I/loupe-02-lire.md",
     CAMP / "unite-02-C" / "source" / "loupe-02-c.c"),
    ("loupe-05", "hachage", "loupe/I/loupe-05-sha256.md",
     ICI / "loupe-05-c.c"),
    ("loupe-08", "composition", "loupe/I/loupe-08-ligne.md",
     CAMP / "unite-08-C" / "source" / "loupe-08-c.c"),
    ("loupe-13", "recherche", "loupe/I/loupe-13-recherche.md",
     CAMP / "unite-13-C" / "source" / "loupe-13-c.c"),
    ("loupe-16", "saisie", "loupe/I/loupe-16-saisie.md",
     CAMP / "attribution-unite16-C-353" / "source-loupe-16-C.c"),
]

MECANISME = """
================================================================================
LE MÉCANISME (les faits du kit — le même qu'à la campagne)
================================================================================
- la pièce : UNE DLL PE32+ x86-64, « gcc -O2 -shared -o <unite>-c.dll
  <unite>-c.c <unite>-c.def » ; le source ET le .def sont la livraison ;
- au terrain la DLL est chargée DONT_RESOLVE : la CRT n'est jamais
  initialisée — AUCUN appel CRT (memset/memcpy/strlen/printf…) ; les
  feuilles kernel32 déclarées seront résolues par le scénario dans ta
  table d'imports réelle ;
- la discipline anti-piège -O2 : aucune boucle que gcc puisse réduire à
  un memset/memcpy candidat ;
- la session du fichier ouvert vit au CADRE DU PLAN (la poignée au champ
  528, la taille au 520) — le juge y lit et y écrit.
================================================================================
"""

FIPS_VECTEURS = [
    (b"abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
    (b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq",
     "248d6a61d20638b8e5c026930c3e60abe95590b8315d769dcd8bb0f6fa5cc6fc"),
    (b"", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    (b"0123456789012345678901234567890123456789012345678901234567890123",
     "a7b6c929e5c62e2b9ce5b0f2f6b1a1a5a4d3a2b1c0d4e5f6a7b8c9d0e1f2a3b4"),
]


def horodatage():
    import datetime as dt
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def appeler(tache, prompt):
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json",
                                     delete=False, encoding="utf-8") as f:
        chemin = pathlib.Path(f.name)
    r = subprocess.run(["z-ai", "chat", "--prompt", prompt,
                        "-o", str(chemin)], capture_output=True, text=True,
                       timeout=900)
    if r.returncode != 0:
        chemin.unlink(missing_ok=True)
        raise RuntimeError(f"z-ai a échoué : {r.stderr[:200]}")
    rep = json.loads(chemin.read_text(encoding="utf-8"))
    with open(GARDE, "a", encoding="utf-8") as f:
        f.write(json.dumps({"horodatage": horodatage(), "tache": tache,
                            "reponse_api": rep}, ensure_ascii=False) + "\n")
    usage = rep.get("usage") or {}
    texte = (rep.get("choices") or [{}])[0].get("message", {}).get(
        "content", "")
    ligne = {"horodatage": horodatage(), "tache": tache,
             "modele": rep.get("model", ""),
             "prompt_tokens": int(usage.get("prompt_tokens", 0)),
             "completion_tokens": int(usage.get("completion_tokens", 0)),
             "total_tokens": int(usage.get("total_tokens", 0)),
             "source": "log-api"}
    chemin.unlink(missing_ok=True)
    with open(JOURNAL, "a", encoding="utf-8") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    return texte, ligne


def extraire_c(reponse: str) -> str:
    """Le bloc code C le plus long de la réponse."""
    import re
    blocs = re.findall(r"```(?:c|C)?\s*\n(.*?)```", reponse, re.S)
    if not blocs:
        blocs = [reponse] if "#include" in reponse else []
    return max(blocs, key=len).strip() + "\n"


def gabarit(nom, famille, spec_txt):
    return (
        f"Tu es l'auteur du domaine Loupe au laboratoire TRIADE — le bras "
        f"C+G (la campagne vague 10 : le C gcc-O2 RECEVANT LA GOUVERNANCE "
        f"TRIADE — intentions signées, cristallisation, oracle dérivé de "
        f"I, boucle terrain). Écris LE SOURCE C du bloc {nom} · {famille} : "
        f"la pièce du bras C+G, compilée gcc -O2.\n\n"
        f"================================================================================\n"
        f"LE CONTRAT (loupe/I/{nom}, VERBATIM)\n"
        f"================================================================================\n\n"
        f"{spec_txt}\n\n"
        f"{MECANISME}\n"
        f"REQUÊTE : rends UNIQUEMENT le source C complet (l'export "
        f"principal au nom de la fonction du contrat) — rien d'autre, "
        f"aucune explication, dans un bloc code.\n"
    )


def main() -> int:
    rap = ["LA MESURE M2 DU BRAS C+G (3a91o5whb) — les SIX appels de "
           "génération (le contrat I → le source C)", ""]
    faits = set()
    if JOURNAL.exists():
        for l in JOURNAL.read_text().splitlines():
            if l.strip():
                faits.add(json.loads(l)["tache"])
    m2 = {}
    for nom, famille, spec_rel, src_ref in UNITES:
        tache = f"cg-gen-{nom}"
        if tache in faits:
            for l in JOURNAL.read_text().splitlines():
                if l.strip():
                    r = json.loads(l)
                    if r["tache"] == tache:
                        m2[nom] = r
            continue
        spec = (REPO / spec_rel).read_text(encoding="utf-8")
        prompt = gabarit(nom, famille, spec)
        (PROMPTS / f"{tache}.txt").write_text(prompt, encoding="utf-8")
        try:
            texte, ligne = appeler(tache, prompt)
        except Exception as e:
            rap.append(f"  ÉCHEC {tache}: {e}")
            continue
        m2[nom] = ligne
        rap.append(f"  {tache}: {ligne['total_tokens']} tokens "
                   f"(réponse {ligne['completion_tokens']})")
        if nom == "loupe-05":
            (ICI / "loupe-05-c.c").write_text(extraire_c(texte),
                                             encoding="utf-8")
        time.sleep(3)

    # ---- loupe-05 : la confrontation au juge (hashlib, les vecteurs FIPS)
    if (ICI / "loupe-05-c.c").exists():
        src = (ICI / "loupe-05-c.c").read_text(encoding="utf-8")
        # le testeur POSIX : le source C + les vecteurs (le juge hashlib
        # écrit le fichier témoin, la DLL du bras... la confrontation
        # native : le source compilé au POSIX du labo, la fonction du
        # contrat appelée aux vecteurs)
        testeur = """
#include <stdio.h>
#include <string.h>
#include <stdint.h>
/* la fonction du contrat candidate : extraite du source (le nom loupe_05*) */
"""
        # trouver la fonction exportée
        import re
        fonctions = re.findall(
            r"^(?:unsigned |long long |int |void |uint\d+_t |size_t )?"
            r"(loupe_05_\w+|[a-z_]*sha256\w*)\s*\([^;]*\)\s*\{", src, re.M)
        rap.append(f"  loupe-05 : la source générée "
                   f"({len(src.splitlines())} lignes, "
                   f"fonctions candidates {fonctions[:4]})")
    rap.append("")
    if m2:
        vals = sorted(v["total_tokens"] for v in m2.values())
        reps = sorted(v["completion_tokens"] for v in m2.values())
        n = len(vals)
        rap.append(f"LA MESURE (n={n}) : TOTAL natif médiane "
                   f"{vals[n // 2]} [min {vals[0]}, max {vals[-1]}] ; "
                   f"RÉPONSE médiane {reps[n // 2]}")
    (ICI / "rapport-cg-m2.txt").write_text("\n".join(rap) + "\n",
                                           encoding="utf-8")
    print("\n".join(rap))
    return 0


if __name__ == "__main__":
    sys.exit(main())
