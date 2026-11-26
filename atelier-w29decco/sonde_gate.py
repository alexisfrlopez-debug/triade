#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sonde_gate.py — LA SONDE DE GATE SUR LE NOUVEL ENDPOINT CLIENT (W29DECCO,
prompt 1 de la vague 29 — le plan gelé PLAN-W29DECCO.md, sha256 consigné à
EMPREINTES-PLANS-VAGUE29.txt AVANT toute mesure).

Le « nouvel endpoint » = LE DÉCODEUR CONTRAIT CÔTÉ CLIENT (la lettre du prompt :
xgrammar/llguidance sur modèle ouvert) : la grammaire du schéma fermé
D264/OPT-16 ÉTENDU à l'opération ajouter, compilée sur le vocabulaire du modèle
ouvert choisi (Qwen2.5-Coder-7B-Instruct — identifiant + empreintes consignés).

LA MESURE DU GATE : la violation ordonnée (l'op hors enum, l'offset hors
bornes) est-elle REFUSÉE AU DÉCODAGE — au masque de bits de tokens appliqué à
chaque pas de génération, PAS seulement au validateur ? Un décodeur qui
laisse passer la violation est refusé nommément.

Le positiv contrôle : les tokens HONNÊTES de l'op/dst/offset sont AUTORISÉS au
masque (le gate ne refuse pas tout — il refuse la violation).

Sortie : gate-verdict.json (le verdict vécu, rejouable bit-identique).
Usage : python3 atelier-w29decco/sonde_gate.py [--passe 2]
"""
import hashlib
import json
import pathlib
import sys

ICI = pathlib.Path(__file__).resolve().parent
R = ICI.parents[0]

# LES CONSIGNATIONS (le plan gelé : identifiant + empreintes)
MODELE_ID = "Qwen/Qwen2.5-Coder-7B-Instruct"
LLGUIDANCE_VERSION = "1.9.1"
LLGUIDANCE_ROUILLE_SHA256 = ("dfac6021d9c4c5ef16b3a1d336c05ca5"
                             "e8208ff30dec29d1c63ebcafbee3a346")

# LE SCHÉMA FERMÉ D264/OPT-16 ÉTENDU À L'OPÉRATION AJOUTER
# (le squelette + dictionnaire : l'op fermé du juge D264, l'offset borné,
#  l'éditer : substituer — le schéma de W28OPT16 reconduit dans l'union)
SCHEMA_ETENDU = {
    "type": "object",
    "additionalProperties": False,
    "required": ["op", "dst", "offset", "src"],
    "properties": {
        "op": {"anyOf": [
            {"const": "substituer"},
            {"enum": ["mov", "add", "sub", "xor", "and", "or",
                       "cmp", "test", "jcc", "call", "ret"]},
        ]},
        "dst": {"type": "string", "minLength": 1},
        "offset": {"type": "integer", "minimum": 0, "maximum": 65535},
        "src": {"anyOf": [{"type": "string", "minLength": 1},
                          {"type": "object"}]},
    },
}


def sha256f(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def bit_permis(bitmask: bytes, tid: int) -> bool:
    """Le bit du token tid dans le masque (1 = autorisé au décodage)."""
    octet = bitmask[tid // 8]
    return (octet >> (tid % 8)) & 1 == 1


def sonde() -> dict:
    from llguidance import JsonCompiler, LLMatcher, LLTokenizer
    from tokenizers import Tokenizer

    empreinte_tok = sha256f(ICI / "tokenizer.json")
    empreinte_cfg = sha256f(ICI / "config.json")

    enc = Tokenizer.from_file(str(ICI / "tokenizer.json"))
    ltok = LLTokenizer(enc.to_str(), eos_token=151645)

    grammar = JsonCompiler().compile(json.dumps(SCHEMA_ETENDU))
    matcher = LLMatcher(ltok, grammar)

    verdict = {
        "horodatage": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc).isoformat(timespec="seconds"),
        "modele": MODELE_ID,
        "empreinte_tokenizer_json": empreinte_tok,
        "empreinte_config_json": empreinte_cfg,
        "decodeur": f"llguidance {LLGUIDANCE_VERSION}",
        "decodeur_empreinte": LLGUIDANCE_ROUILLE_SHA256,
        "schema": "D264/OPT-16 étendu à ajouter (union éditer/ajouter)",
        "probes": [],
    }

    def ids_de(t):
        return enc.encode(t).ids

    def consomme(m, ids):
        for t in ids:
            m.consume_token(t)

    # ---- PROBE 1 : L'OP HORS ENUM REFUSÉ AU MASQUE ---------------------------------
    # le préfixe valide : {"op": "
    m1 = LLMatcher(ltok, grammar)
    consomme(m1, ids_de('{"op": "'))
    assert not m1.is_error(), "le préfixe valide ne peut pas être refusé"
    bm = m1.compute_bitmask()
    viol_ids = ids_de("SUBVERSION-HORS-ENUM")
    probe_viol = [bit_permis(bm, t) for t in viol_ids]
    honnetes = ids_de("substituer")
    probe_honnete = [bit_permis(bm, t) for t in honnetes]
    # « mov » de l'opération ajouter — la seconde voie de l'union
    probe_mov = [bit_permis(bm, t) for t in ids_de("mov")]
    verdict["probes"].append({
        "nom": "op-hors-enum",
        "prefixe": '{"op": "',
        "la_violation": "SUBVERSION-HORS-ENUM",
        "tokens_violation": viol_ids,
        "au_masque": probe_viol,
        "refusee_au_decodage": not any(probe_viol),
        "les_honnetes_au_masque": {
            "substituer": probe_honnete,
            "mov": probe_mov,
        },
        "honnets_autorises": all(probe_honnete) and all(probe_mov),
    })

    # ---- PROBE 2 : L'OFFSET HORS BORNES REFUSÉ AU MASQUE ---------------------------
    # le préfixe valide d'un objet ajouter : {"op": "mov", "dst": "CST-1", "offset":
    m2 = LLMatcher(ltok, grammar)
    consomme(m2, ids_de('{"op": "mov", "dst": "CST-1", "offset": '))
    assert not m2.is_error()
    bm2 = m2.compute_bitmask()
    # 99999 > 65535 : après « 9999 », AUCUN chiffre n'est permis (tout 5-digit ≥ 10000... 65535 borne)
    # — en fait 5 chiffres ≤ 65535 permis jusqu'à la borne ; le 6ᵉ chiffre refuse TOUT
    consomme(m2, ids_de("65535"))          # la borne exacte — permise
    bm2b = m2.compute_bitmask()
    chiffre_ids = ids_de("5")
    hors_borne = [bit_permis(bm2b, t) for t in chiffre_ids]
    # et la séquence complète « 999999 » depuis l'état vierge :
    m2c = LLMatcher(ltok, grammar)
    consomme(m2c, ids_de('{"op": "mov", "dst": "CST-1", "offset": 9999'))
    bm2c = m2c.compute_bitmask()
    suite9 = [bit_permis(bm2c, t) for t in ids_de("9")]
    verdict["probes"].append({
        "nom": "offset-hors-bornes",
        "prefixe": '{"op": "mov", "dst": "CST-1", "offset": ',
        "la_violation": "999999 (et tout 5-digit > 65535 après la borne)",
        "borne": "0..65535 (l'offset du juge D264)",
        "apres_65535_chiffre_au_masque": hors_borne,
        "apres_9999_suite_9_au_masque": suite9,
        "refusee_au_decodage": not any(hors_borne) and not any(suite9),
    })

    # ---- PROBE 3 : LA CLÉ HORS SCHÉMA REFUSÉE AU MASQUE ------------------------------
    m3 = LLMatcher(ltok, grammar)
    consomme(m3, ids_de('{"'))
    bm3 = m3.compute_bitmask()
    cle_viol = ids_de("subversion")     # la clé inconnue (additionalProperties: false)
    cle_ok = ids_de("op")
    verdict["probes"].append({
        "nom": "cle-hors-schema",
        "prefixe": '{"',
        "la_violation": "subversion (clé inconnue)",
        "au_masque": [bit_permis(bm3, t) for t in cle_viol],
        "cle_legitime_au_masque": [bit_permis(bm3, t) for t in cle_ok],
        "refusee_au_decodage": not any(bit_permis(bm3, t) for t in cle_viol),
    })

    # ---- LE CONTRÔLE POSITIF : UN OBJET HONNÊTE CONSOMMÉ JUSQU'À L'ACCEPTATION ------
    m4 = LLMatcher(ltok, grammar)
    complet = ('{"op": "mov", "dst": "CST-1", "offset": 32, '
               '"src": {"type": "reg", "valeur": "eax"}}')
    consomme(m4, ids_de(complet))
    verdict["controle_positif"] = {
        "objet": complet,
        "is_error": bool(m4.is_error()),
        "is_accepting": bool(m4.is_accepting()),
    }
    m4b = LLMatcher(ltok, grammar)
    complet_edit = ('{"op": "substituer", "dst": "b20004", "offset": 17, '
                    '"src": "je 0x4997"}')
    consomme(m4b, ids_de(complet_edit))
    verdict["controle_positif_editer"] = {
        "objet": complet_edit,
        "is_error": bool(m4b.is_error()),
        "is_accepting": bool(m4b.is_accepting()),
    }

    # ---- LE VERDICT -------------------------------------------------------------------
    refusees = all(p["refusee_au_decodage"] for p in verdict["probes"])
    positifs = (verdict["controle_positif"]["is_accepting"]
                and verdict["controle_positif_editer"]["is_accepting"]
                and verdict["controle_positif"]["is_error"] is False
                and verdict["controle_positif_editer"]["is_error"] is False)
    verdict["VERDICT"] = (
        "GATE-VERT — LE DÉCODEUR CLIENT REFUSE LA VIOLATION AU DÉCODAGE "
        "(au masque de bits, pas seulement au validateur) ; les objets honnêtes "
        "consommés jusqu'à l'acceptation."
        if refusees and positifs else
        "GATE-REFUSÉ — le décodeur laisse passer une violation : nommé.")
    return verdict


def main():
    passe = 1
    if "--passe" in sys.argv:
        passe = int(sys.argv[sys.argv.index("--passe") + 1])
    v = sonde()
    dest = ICI / ("gate-verdict.json" if passe == 1 else "gate-verdict-2.json")
    dest.write_text(json.dumps(v, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8")
    print(f"[sonde] passe {passe} → {dest.name}")
    for p in v["probes"]:
        print(f"  {p['nom']:22s} refusee_au_decodage={p['refusee_au_decodage']}")
    print(f"  contrôle positif: accepting={v['controle_positif']['is_accepting']}"
          f" / éditer accepting={v['controle_positif_editer']['is_accepting']}")
    print(f"  VERDICT: {v['VERDICT']}")


if __name__ == "__main__":
    main()
