#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""independance_peap6ws09.py — L'INDÉPENDANCE INTER-FAMILLES, LE PROTOCOLE
AMENDÉ (peap6ws09, l'amendement gelé avant tout run) :

  R1 LA DÉRIVATION OUTILLÉE (LE TEST D'INDÉPENDANCE) — le second modèle
     (Qwen2.5-Coder-1.5B-Instruct, la famille distincte) ÉCRIT DU CODE
     qui dérive T[64] (RFC 1321 § 3.4) et K[64] (FIPS 180-4 § 4.2.2)
     des DÉFINITIONS MATHÉMATIQUES SEULES — le plan JAMAIS au prompt ;
     le code généré est EXÉCUTÉ ; LE JUGE : la confrontation aux
     définitions exactes (les décimales) ET au plan (les tables du
     dépôt) ;
  R2 LA RÉCITATION PURE (LA SONDE DE MÉMORISATION, jamais un test
     d'indépendance) — le protocole documenté de 1c4sokpii, rapportée
     comme sonde ;
  R3 LE BRAS C À TROIS CONTRATS (loupe-13 reconduit + loupe-02 LIRE +
     loupe-16 SAISIE) — le contrat MOT POUR MOT au prompt, le modèle
     écrit le C, gcc -O2, l'épreuve POSIX (l'école, les rejets, la
     différentielle à la graine 20261115, le juge indépendant).

L'état est REPRIS (independance_etat.json) — chaque pièce vécue une
fois, jamais re-vécue. AUCUN résultat fabriqué : les sources générés
conservés verbatim, les écarts exacts consignés."""
from __future__ import annotations

import importlib.util
import json
import pathlib
import random
import re
import subprocess
import sys

ICI = pathlib.Path(__file__).resolve().parent
REPO = ICI.parent
sys.path.insert(0, str(REPO))

MODELE = pathlib.Path("/home/z/work_hf/hub/models--Qwen--Qwen2.5-Coder"
                      "-1.5B-Instruct/snapshots/"
                      "2e1fd397ee46e1388853d2af2c993145b0f1098a")
ETAT = ICI / "independance_etat.json"

# ---------------------------------------------------------- le juge : les définitions


def deriv_T_md5() -> list[int]:
    spec = importlib.util.spec_from_file_location("hn_i", REPO / "loupe"
                                                  / "harnais_noyau.py")
    hn = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hn)
    return hn.deriv_MD5_T()


def deriv_K_sha256() -> list[int]:
    """FIPS 180-4 § 4.2.2 aux décimales exactes (le juge de 1c4sokpii)."""
    from decimal import Decimal, getcontext
    getcontext().prec = 60

    def racine_cubique(x: Decimal) -> Decimal:
        r = Decimal(1)
        eps = Decimal(1).scaleb(-50)
        for _ in range(200):
            r2 = (2 * r + x / (r * r)) / 3
            if r2 == r or abs(r2 - r) < eps:
                return r2
            r = r2
        return r

    premiers = []
    n = 2
    while len(premiers) < 64:
        if all(n % p for p in premiers if p * p <= n):
            premiers.append(n)
        n += 1
    return [int((racine_cubique(Decimal(p)) % 1) * (1 << 32)) & 0xFFFFFFFF
            for p in premiers]


def plan_T_md5() -> list[int]:
    """LES TABLES DU PLAN — la source unique du dépôt (la conformité
    générative v0.14.0, la pièce scripts/independance_v140.py)."""
    spec = importlib.util.spec_from_file_location(
        "iv140", REPO / "scripts" / "independance_v140.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.T_AGENT


def plan_K_sha256() -> list[int]:
    """La table K du plan — tls13/layout.py (la chaîne sha-256 du M4)."""
    src = (REPO / "tls13" / "layout.py").read_text(encoding="utf-8")
    m = re.search(r"0x428a2f98,[^\]]*\]", src, re.S)
    return [int(h, 16) for h in re.findall(r"0x([0-9a-f]{8})", m.group(0))]


# ------------------------------------------------------------------ le modèle local
_MODELE_CACHE = None


def charger():
    global _MODELE_CACHE
    if _MODELE_CACHE is None:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        tok = AutoTokenizer.from_pretrained(str(MODELE))
        mod = AutoModelForCausalLM.from_pretrained(str(MODELE),
                                                   torch_dtype=torch.bfloat16)
        _MODELE_CACHE = (tok, mod)
    return _MODELE_CACHE


def generer(invites: list[str], max_tokens: int = 900) -> list[str]:
    import torch
    tok, mod = charger()
    msgs = [[{"role": "user", "content": i}] for i in invites]
    tok.padding_side = "left"
    enc = tok.apply_chat_template(msgs, add_generation_prompt=True,
                                  return_tensors="pt", return_dict=True,
                                  padding=True)
    with torch.no_grad():
        out = mod.generate(**enc, max_new_tokens=max_tokens, do_sample=False)
    return [tok.decode(out[i][enc["input_ids"].shape[1]:],
                       skip_special_tokens=True) for i in range(len(invites))]


def etat_lire() -> dict:
    return json.loads(ETAT.read_text(encoding="utf-8")) if ETAT.exists() else {}


def etat_ecrire(e: dict) -> None:
    ETAT.write_text(json.dumps(e, ensure_ascii=False, indent=1),
                    encoding="utf-8")


# ============================================================ R1 LA DÉRIVATION OUTILLÉE
INVITE_T = (
    "Write a complete Python function that computes the 64 MD5 constants "
    "T from the mathematical definition in RFC 1321 section 3.4: "
    "T[i] = the integer part of (4294967296 * abs(sin(i + 1))), for i from "
    "0 to 63, where sin is in radians. The function must be named table_T, "
    "take no arguments, and return the list of the 64 unsigned 32-bit "
    "integers. Derive every value from the definition with your own code "
    "(math.sin or a series is accepted) - NEVER write any literal value of "
    "the table. Output ONLY the Python code, nothing else."
)
INVITE_K = (
    "Write a complete Python function that computes the 64 SHA-256 "
    "constants K from the mathematical definition in FIPS 180-4 section "
    "4.2.2: K[i] = the first 32 bits of the fractional part of the cube "
    "root of the i-th prime number, for i from 1 to 64 (the first 64 "
    "primes: 2, 3, 5, 7, ...). The function must be named table_K, take "
    "no arguments, and return the list of the 64 unsigned 32-bit integers. "
    "Derive every value from the definition with your own code (compute "
    "the primes, the cube roots at high precision, take the fractional "
    "bits) - NEVER write any literal value of the table. Output ONLY the "
    "Python code, nothing else."
)


def extraire_code(texte: str) -> str:
    """Le code généré, conservé VERBATIM ; les clôtures ``` retirées."""
    m = re.findall(r"```[a-zA-Z]*\n(.*?)```", texte, re.S)
    return max(m, key=len).strip() if m else texte.strip()


def executer_code(code: str, nom_fonction: str) -> tuple[list | None, str]:
    """Exécute le code généré dans un sous-processus — le relevé est le
    résultat de L'EXÉCUTION, jamais une lecture de la prose."""
    fichier = ICI / f"derivation_{nom_fonction}_qwen.py"
    fichier.write_text(code, encoding="utf-8")
    # L'IMPORT SILENCIEUX : le code généré peut imprimer au niveau module
    # (la pièce verbatim demeure) — la table est lue de LA DERNIÈRE ligne
    # JSON du flux, jamais de la prose
    essai = fichier.parent / f"_essai_{nom_fonction}.py"
    essai.write_text(
        f"import io, json, contextlib, sys\n"
        f"sys.path.insert(0, {str(fichier.parent)!r})\n"
        f"with contextlib.redirect_stdout(io.StringIO()):\n"
        f"    from derivation_{nom_fonction}_qwen import {nom_fonction}\n"
        f"print(json.dumps(list({nom_fonction}())))\n", encoding="utf-8")
    r = subprocess.run(["python3", str(essai)], capture_output=True,
                       text=True, timeout=120)
    if r.returncode != 0:
        return None, f"l'exécution échoue : {r.stderr[-300:]}"
    try:
        return [int(v) & 0xFFFFFFFF
                for v in json.loads(r.stdout.strip().splitlines()[-1])], ""
    except Exception as e:
        return None, (f"la sortie n'est pas la table : {e} / "
                      f"{r.stdout.strip()[:120]}")


def ronde_derivation(nom: str, invite: str, fonction: str,
                     defs: list[int], plan: list[int]) -> dict:
    e = etat_lire()
    cle = f"derivation_{nom}"
    if cle in e:
        return e[cle]
    [texte] = generer([invite], max_tokens=1200)
    code = extraire_code(texte)
    table, err = executer_code(code, fonction)
    resultat = {"nom": nom, "code_verbatim": code[:8000], "erreur": err,
                "conforme_defs": None, "conforme_plan": None,
                "ecarts_defs": [], "ecarts_plan": []}
    if table is not None and len(table) == 64:
        resultat["conforme_defs"] = (table == defs)
        resultat["conforme_plan"] = (table == plan)
        resultat["ecarts_defs"] = [i for i in range(64) if table[i] != defs[i]][:20]
        resultat["ecarts_plan"] = [i for i in range(64) if table[i] != plan[i]][:20]
    elif table is not None:
        resultat["erreur"] = f"la table dérivée compte {len(table)} valeurs (64 attendues)"
    e[cle] = resultat
    etat_ecrire(e)
    return resultat


# ================================================== R2 LA RÉCITATION PURE (la sonde)
def sonde_recitation() -> dict:
    e = etat_lire()
    if "recitation" in e:
        return e["recitation"]
    invite_t = ("Recite the MD5 constants T[{debut}..{fin}] from memory, "
                "one per line in hex 0x........, nothing else. The first "
                "two are public anchors: T[0] = 0xd76aa478, T[1] = 0xe8c7b756.")
    invite_k = ("Recite the SHA-256 constants K[{debut}..{fin}] from memory, "
                "one per line in hex 0x........, nothing else. The first "
                "two are public anchors: K[0] = 0x428a2f98, K[1] = 0x71374491.")
    HEX = re.compile(r"0x([0-9a-fA-F]{8})")
    rapport = {"T": {}, "K": {}}
    for nom, invite, ref in [("T", invite_t, deriv_T_md5()),
                             ("K", invite_k, deriv_K_sha256())]:
        invites = [invite.format(debut=d, fin=d + 15) for d in range(0, 64, 16)]
        textes = generer(invites, max_tokens=400)
        verts = 0
        for d, texte in zip(range(0, 64, 16), textes):
            vals = [int(h, 16) for h in HEX.findall(texte)]
            bons = sum(1 for i, v in enumerate(vals[:16]) if v == ref[d + i])
            verts += bons
            rapport[nom][f"{d}-{d+15}"] = bons
        rapport[nom]["verts"] = verts
    e["recitation"] = rapport
    etat_ecrire(e)
    return rapport


# ============================================================ R3 LE BRAS C (3 contrats)
CONTRATS = {
    "loupe-13": (REPO / "loupe/I/loupe-13-recherche.md", "loupe_13_recherche"),
    "loupe-02": (REPO / "loupe/I/loupe-02-lire.md", "loupe_02_lire"),
    "loupe-16": (REPO / "loupe/I/loupe-16-saisie.md", "loupe_16_saisie"),
}

SIGNATURES = {
    "loupe-13": (
        "long loupe_13_recherche(const unsigned char *fenetre, long taille, "
        "const unsigned char *motif, long taille_motif, long depart)\n"
        "— returns the ABSOLUTE position of the FIRST occurrence of motif "
        "(1 to 32 bytes) in fenetre[depart..taille), or -1 when absent "
        "(the named end), or -5 on invalid input (empty pattern, pattern "
        "longer than 32, depart beyond taille); a pattern longer than the "
        "remaining range returns -1 immediately (the trivial constat, "
        "never a loop)."
    ),
    "loupe-02": (
        "long loupe_02_lire(const unsigned char *fichier, long taille, "
        "const long *journal_dec, const unsigned char *journal_oct, "
        "long journal_n, unsigned char *tampon, long *remplissage, "
        "long decalage)\n"
        "— reads the window of up to 384 bytes at decalage into tampon: "
        "*remplissage = min(384, taille - decalage); tampon[i] = "
        "fichier[decalage + i]; THEN the edit journal overlay: for every "
        "journal entry whose decalage d is in [decalage, decalage + "
        "*remplissage), tampon[d - decalage] = journal_oct of that entry; "
        "returns 0, or -4/-5/-3 on the contract's failures (decalage not "
        "a multiple of 16 -> -5; decalage >= taille -> -3)."
    ),
    "loupe-16": (
        "long loupe_16_saisie(long curseur, unsigned char octet, "
        "long *journal_dec, unsigned char *journal_oct, long *journal_n, "
        "unsigned char *tampon, long remplissage, long vue, long *sale)\n"
        "— writes one byte to the edit journal: if curseur's decalage is "
        "already in the journal (journal_dec[i] == curseur for some i), "
        "REPLACE its octet (journal_n unchanged); else append "
        "(journal_dec[*journal_n] = curseur, journal_oct[*journal_n] = "
        "octet, (*journal_n)++) unless the journal is FULL (256 distinct "
        "entries -> return -3, the named bound); the view overlay: if "
        "curseur - vue is in [0, remplissage), tampon[curseur - vue] = "
        "octet; *sale = 1; returns 0."
    ),
}

INVITE_C = (
    "You are implementing one block of a hex-editor in C, from its "
    "layer-I contract below. Write the EXACT function with EXACTLY this "
    "signature:\n{signature}\n\nThe contract (the source of truth for "
    "the semantics):\n{contrat}\n\nCONSTRAINTS: pure C99, no file I/O, "
    "no Windows API, no global state — every input through the arguments, "
    "every output through the return and the pointed buffers; the failure "
    "verdicts are the negative return codes exactly as stated. Output "
    "ONLY the complete C file (no main, no markdown fence, no "
    "explanation)."
)


def bras_c(nom: str, refaire=False) -> dict:
    e = etat_lire()
    cle = f"bras_c_{nom}"
    if cle in e and not refaire:
        return e[cle]
    chemin, fonction = CONTRATS[nom]
    contrat = chemin.read_text(encoding="utf-8")
    invite = INVITE_C.format(signature=SIGNATURES[nom], contrat=contrat)
    [texte] = generer([invite], max_tokens=1800)
    code = extraire_code(texte)
    fichier = ICI / f"bras_c_qwen_{nom}.c"
    fichier.write_text(code, encoding="utf-8")
    e[cle] = {"nom": nom, "code_verbatim": code[:12000],
              "fichier": fichier.name, "epreuve": None}
    etat_ecrire(e)
    return e[cle]


if __name__ == "__main__":
    quelle = sys.argv[1] if len(sys.argv) > 1 else "tout"
    if quelle in ("tout", "derivation"):
        print("== R1 LA DÉRIVATION OUTILLÉE (le test d'indépendance) ==")
        for nom, invite, fonction in [("T", INVITE_T, "table_T"),
                                      ("K", INVITE_K, "table_K")]:
            defs = deriv_T_md5() if nom == "T" else deriv_K_sha256()
            plan = plan_T_md5() if nom == "T" else plan_K_sha256()
            r = ronde_derivation(nom, invite, fonction, defs, plan)
            print(f"  {nom}: conforme_définitions={r['conforme_defs']} "
                  f"conforme_plan={r['conforme_plan']} err={r['erreur'][:80]!r}")
            if r["ecarts_defs"]:
                print(f"     écarts aux définitions (indices): {r['ecarts_defs'][:10]}")
    if quelle in ("tout", "recitation"):
        print("== R2 LA RÉCITATION PURE (la sonde de mémorisation) ==")
        r = sonde_recitation()
        print(f"  T: {r['T']['verts']}/64 ; K: {r['K']['verts']}/64")
    if quelle in ("tout", "brasc"):
        print("== R3 LE BRAS C AUX TROIS CONTRATS ==")
        for nom in CONTRATS:
            r = bras_c(nom)
            print(f"  {nom}: le source généré -> {r['fichier']}")
