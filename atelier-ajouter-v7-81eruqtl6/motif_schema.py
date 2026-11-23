#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""motif_schema.py — LE SCHÉMA DE CONTRAINTE CONSTRUIT DEPUIS LES CANONS
(81eruqtl6, la campagne du décodage contraint).

LA RÈGLE : les tables DEPUIS LES CANONS jamais retapées — le motif de
ligne est l'UNION DES FORMES ADMISES du juge assembler_v2, lues des
regex CANONIQUES du dépôt (client_gabarits.MON_INSTRUCTION,
client_gabarits.RE_DEF_ETIQ, client_v2.RE_LIGNE_ID, la forme
opérande-ID et la définition LBL du juge), les IDs ÉNUMÉRÉS du
dictionnaire du bloc (construire_dictionnaire — le canon du bloc).

CE QUE LA CONTRAINTE COUVRE (les classes de FORME, au décodeur) :
  HORS-FORMAT — les préfixes de chaîne (repne…), les db/dw/dd/dq, les
  artefacts ```, la prose : IMPOSSIBLES (hors l'inventaire canonnel des
  mnémoniques et des formes de ligne) ;
  ID-INCONNU — un ID hors dictionnaire : IMPOSSIBLE (l'énumération).
CE QU'ELLE NE COUVRE PAS (nommé au plan) : EXPANSION-DIVERGENTE et
FORME-INVALIDE (les quatre interdits) demeurent AU JUGE — la contrainte
ne remplace JAMAIS un juge, elle précède."""
from __future__ import annotations

import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
V2 = REPO / "atelier-ajouter-v2-pgodgk35l"
V1 = REPO / "atelier-gabarits-o5apue194"
sys.path.insert(0, str(V2))
sys.path.insert(0, str(V1))

from client_v2 import construire_dictionnaire                    # noqa: E402
from client_gabarits import MON_INSTRUCTION, RE_DEF_ETIQ        # noqa: E402


def motif_ligne(dico: dict) -> str:
    """LE MOTIF CANONNEL D'UNE LIGNE — l'union des formes admises du
    juge, les IDs énumérés du dictionnaire du bloc. Chaque alternative
    porte SA SOURCE (le canon du dépôt, la ligne du juge)."""
    alts = []
    # (a) LA DÉFINITION LBL DU DICTIONNAIRE — la forme du juge
    #     ^(LBL)-([0-9]{3})\s*:\s$ , l'ID énuméré du bloc
    lbls = sorted(dico.get("LBL") or {})
    if lbls:
        alts.append(r"(?:" + "|".join(lbls) + r")\s*:\s*")
    # (b) L'ÉTIQUETTE LOCALE — RE_DEF_ETIQ TEL QUEL (le canon gabarits)
    alts.append(RE_DEF_ETIQ.pattern.lstrip("^").rstrip("$"))
    # (c) LA FORME ID AU SAUT/APPEL — RE_LIGNE_ID TEL QUEL, les IDs
    #     énumérés (LBL ∪ CST du bloc)
    ids = sorted(list(dico.get("LBL") or {}) + list(dico.get("CST") or {}))
    if ids:
        alternance = "|".join(ids)
        alts.append(r"(?:j\w+|loop\w*|call)\s+(?:" + alternance + r")")
        # (d) LA FORME OPÉRANDE-ID — la forme du juge
        #     ^[\w:]+[^,]*,\s*(LBL|CST)-[0-9]{3}$ , l'ID énuméré
        alts.append(r"[\w:]+[^,]*,\s*(?:" + alternance + r")")
    # (e) L'INSTRUCTION DU DOMAINE — MON_INSTRUCTION TEL QUEL (le canon
    #     gabarits : l'inventaire des 18 blocs, AUCUNE directive de
    #     données) + la queue libre : LES OPÉRANDES DEMEURENT AU JUGE
    alts.append(MON_INSTRUCTION.pattern.lstrip("^") + ".*")
    return "^(?:" + "|".join(alts) + ")$"


def schema_corps(dico: dict) -> dict:
    """L'OBJET response_format PAR TÂCHE : le corps en TABLEAU de lignes
    (une chaîne par ligne), chaque ligne au motif canonnel, strict."""
    return {
        "name": "tpl_add_corps",
        "schema": {
            "type": "object",
            "properties": {
                "corps": {
                    "type": "array",
                    "items": {"type": "string",
                              "pattern": motif_ligne(dico)},
                    "minItems": 1,
                }
            },
            "required": ["corps"],
            "additionalProperties": False,
        },
        "strict": True,
    }


# ------------------------------------------------- LA CALIBRATION v6 -------
def calibrer(sortie: pathlib.Path) -> int:
    """LE MOTIF CALIBRÉ AUX CINQ VERTES v6 (le garde-brut de 7xuvsoqpuq
    — la donnée COMMISE, aucune donnée neuve) : chaque ligne canonique
    de chaque corps vert DOIT matcher le motif de son bloc — une verte
    qui échoue = le motif TROP STRICT, corrigé AVANT la campagne."""
    V6 = REPO / "atelier-ajouter-v6-7xuvsoqpuq"
    sys.path.insert(0, str(V6))
    sys.path.insert(0, str(REPO / "atelier-ajouter-v5-yfkpml1j2"))
    from campagne_v5 import normaliser                          # noqa: E402

    journ = [json.loads(l) for l in
             (V6 / "journal_v6.jsonl").read_text().splitlines() if l.strip()]
    brut = {json.loads(l)["id"]: json.loads(l) for l in
            (V6 / "garde-brut-v6.jsonl").read_text().splitlines() if l.strip()}
    verts = {}
    for l in (V6 / "resultats_v6.jsonl").read_text().splitlines():
        if l.strip():
            d = json.loads(l)
            if d["vert"]:
                verts[d["tache"]] = d
    lignes = []
    verts_ok = 0
    for tache, d in sorted(verts.items()):
        essais = [j for j in journ if j["tache"] == tache
                  and j.get("phase") == "campagne"]
        dernier = max(essais, key=lambda j: j["essai"])
        contenu = brut[dernier["id"]]["choices"][0]["message"]["content"]
        canon = normaliser(contenu)
        dico = construire_dictionnaire(d["bloc"])
        motif = re.compile(motif_ligne(dico))
        echecs = [l for l in canon.split("\n") if l.strip()
                  and not motif.match(l)]
        if echecs:
            lignes.append(f"ROUGE {tache} ({d['bloc']}) — "
                          f"{len(echecs)} ligne(s) hors motif :")
            for e in echecs[:5]:
                lignes.append(f"    {e[:90]!r}")
        else:
            verts_ok += 1
            n = sum(1 for l in canon.split("\n") if l.strip())
            lignes.append(f"VERT {tache} ({d['bloc']}) — {n} lignes "
                          f"canoniques TOUTES au motif")
    rapport = [
        "CALIBRATION DU MOTIF AUX CINQ VERTES v6 (81eruqtl6)",
        "la source : resultats/journal/garde-brut de 7xuvsoqpuq (la donnée",
        "COMMISE — aucune donnée neuve) ; la question : l'univers des",
        "formes admises au DÉCODEUR couvre-t-il tout ce que les vertes",
        "v6 ont eu besoin d'émettre ? (une verte hors motif = le motif",
        "TROP STRICT, corrigé AVANT la campagne)",
        "=" * 66,
        *lignes,
        "=" * 66,
        f"VERDICT : {verts_ok}/{len(verts)} vertes couvertes",
        ""]
    sortie.write_text("\n".join(rapport), encoding="utf-8")
    print("\n".join(rapport), end="")
    return 0 if verts_ok == len(verts) else 1


if __name__ == "__main__":
    ici = pathlib.Path(__file__).resolve().parent
    sys.exit(calibrer(ici / "registres" / "calibration-vertes-v6.txt"))
