#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""client_v2.py — LE CLIENT TPL-ADD-v2 (pgodgk35l, la vague 12) : le
squelette déterministe dérivé de la couche I PLUS LE DICTIONNAIRE DE
DOMAINE VERSIONNÉ — les étiquettes et constantes admissibles du bloc
vivent comme IDs littéraux (LBL-xxx, CST-xxx) dans le matériau, l'agent
émet des IDs, LE CLIENT EXPANDE et recoupe l'empreinte sha256 du
dictionnaire.

FAIL-CLOSED (les quatre faces exigées par l'instruction) :
  ID-INCONNU          — un ID absent du dictionnaire du bloc ;
  DICT-DIVERGENT      — l'empreinte du dictionnaire divergente (le
                        dictionnaire muté d'un octet — le contrôle
                        négatif le vit) ;
  EXPANSION-DIVERGENTE — la ligne expandée ne s'assemble pas aux octets
                        du domaine (l'expansion recoupée) ;
  HORS-FORMAT         — une ligne hors les formes admises (l'instruction
                        du domaine, la définition d'étiquette locale, la
                        référence d'ID).

AUCUN CONTRÔLE RETIRÉ : la fenêtre ±12 (le gabarit TPL-EDIT), l'empreinte
sha256 de la notation, LE ROUND-TRIP keystone/capstone, LE JUGE DU CADRE
(l'ABI msx64 : le prologue/épilogue, le shadow space) demeurent — le
client v8 de la vague 11 est la base, le présent n'ajoute QUE le
dictionnaire."""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
ICI = REPO / "atelier-ajouter-v2-pgodgk35l"
V1 = REPO / "atelier-gabarits-o5apue194"
sys.path.insert(0, str(V1))
sys.path.insert(0, str(V1.parent / "atelier-fenetre-mqf258e4l"))

from client_gabarits import (generer_squelette, BALISE_DEBUT,  # noqa: E402
                             BALISE_FIN, MON_INSTRUCTION, RE_DEF_ETIQ,
                             PLAN_APPELS)
from client_gabarits import Refus, resoudre_logique, round_trip  # noqa: E402

DICT_VERSION = "DICT-DOMAINE-v1"
RE_ID = re.compile(r"^(LBL|CST)-([0-9]{3})$")
RE_LIGNE_ID = re.compile(
    r"^(j\w+|loop\w*|call)\s+(LBL|CST)-([0-9]{3})$")


# ===========================================================================
# LE DICTIONNAIRE DE DOMAINE — versionné, l'empreinte gravée au matériau
# ===========================================================================
def construire_dictionnaire(nom_bloc: str) -> dict:
    """LE DICTIONNAIRE DU BLOC : les étiquettes résolues (les cibles de
    saut du bloc — lues de l'en-tête de la notation RÉELLE du dépôt, les
    cibles absolues du plan) et les constantes admissibles (les appels
    IAT aux slots du plan, les appels directs, les bornes nommées de la
    spec). Chaque entrée : un ID littéral (LBL-xxx / CST-xxx)."""
    notation = (REPO / "loupe" / "notation" / f"{nom_bloc}.asm").read_text(
        encoding="utf-8")
    d = {"version": DICT_VERSION, "bloc": nom_bloc,
         "LBL": {}, "CST": {}, "expansion": {}}
    # (1) LES ÉTIQUETTES RÉSOLUES — la ligne « Étiquettes résolues : » de
    #     l'en-tête (les cibles absolues du plan — le dictionnaire les
    #     porte, l'agent n'a PLUS à les deviner : il émet l'ID)
    m = re.search(r"Étiquettes résolues\s*:\s*(.+)", notation)
    if m:
        for paire in m.group(1).split(","):
            mm = re.match(r"\s*\.?([A-Za-z_]\w*)=0x([0-9a-f]+)", paire)
            if mm:
                cle = f"LBL-{len(d['LBL']) + 1:03d}"
                d["LBL"][cle] = {"nom": mm.group(1),
                                 "adresse": int(mm.group(2), 16)}
                d["expansion"][mm.group(1)] = f"0x{mm.group(2)}"
    # (2) LES APPELS IAT (les déplacements RIP de l'en-tête — chaque cible
    #     = l'adresse du slot au plan ; l'agent émet « call CST-xxx », le
    #     client calcule le déplacement À L'ADRESSE de l'instruction)
    for mm in re.finditer(r"^;\s*0x([0-9a-f]+) \+ 0x([0-9a-f]+) [+-] "
                          r"0x([0-9a-f]+) = 0x([0-9a-f]+)\s*$",
                          notation, re.M):
        cible = int(mm.group(4), 16)
        if 0x3000 <= cible < 0x3200:          # la fenêtre IAT du plan loupe
            cle = f"CST-{len(d['CST']) + 1:03d}"
            if cible not in [c.get("slot") for c in d["CST"].values()]:
                d["CST"][cle] = {"type": "iat", "slot": cible}
    # (3) LES APPELS DIRECTS (le plan — les libc/tls13 de PLAN_APPELS)
    for nom, (desc, addr) in PLAN_APPELS.items():
        if re.search(rf"\b{nom}\b", notation):
            cle = f"CST-{len(d['CST']) + 1:03d}"
            d["CST"][cle] = {"type": "appel", "nom": nom, "adresse": addr,
                             "description": desc}
    # (3bis) LES CONSTANTES SÉMANTIQUES DU CORPS — les immédiats
    #     distinctifs de la notation réelle (cmp/test/mov …, immédiat
    #     ≥ 0x100 : les messages Windows, les tailles, les masques) : la
    #     couche I les nomme, le corps les porte — le dictionnaire les
    #     recueille pour que l'agent n'écrive JAMAIS un symbole en clair
    vus = set()
    for mm in re.finditer(
            r"\b(?:cmp|test)\s+(?:dword ptr \[[^]]+\]|e\w+d?|r\w+d?), "
            r"(0x[0-9a-f]{3,}|\d{3,})\b",
            notation):
        v = int(mm.group(1), 0)
        if v >= 0x100 and v not in vus:
            vus.add(v)
            cle = f"CST-{len(d['CST']) + 1:03d}"
            d["CST"][cle] = {"type": "constante", "nom":
                             f"immédiat-0x{v:x}", "valeur": v}
    # (4) LES CONSTANTES NOMMÉES de la spec (les bornes du domaine)
    spec = (REPO / "loupe" / "I" / f"{nom_bloc}.md").read_text(
        encoding="utf-8")
    for mm in re.finditer(r"\b([A-Z][A-Z_0-9]{2,})\s+octets\s*\((\d+)\)",
                          spec):
        cle = f"CST-{len(d['CST']) + 1:03d}"
        d["CST"][cle] = {"type": "constante", "nom": mm.group(1),
                         "valeur": int(mm.group(2))}
    for mm in re.finditer(r"\b(\d+)\s+à\s+(\d+)\s*(?:octets?\s*)?"
                          r"\(([A-Z][A-Z_0-9]{2,})\)", spec):
        cle = f"CST-{len(d['CST']) + 1:03d}"
        d["CST"][cle] = {"type": "constante", "nom": mm.group(3),
                         "valeur": int(mm.group(2))}
    # l'empreinte du dictionnaire (le corps canonique)
    corps = json.dumps({k: d[k] for k in ("version", "bloc", "LBL", "CST")},
                       sort_keys=True, ensure_ascii=False)
    d["sha256"] = hashlib.sha256(corps.encode()).hexdigest()
    return d


def dictionnaire_muté(d: dict) -> dict:
    """LE DICTIONNAIRE MUTÉ D'UN OCTET (le contrôle négatif DICT-DIVERGENT)
    — une borne décalée d'une unité : l'empreinte diverge, l'expansion
    DOIT être refusée."""
    m = json.loads(json.dumps(d))
    for cle, entree in m["CST"].items():
        if entree["type"] == "constante":
            entree["valeur"] += 1
            break
    corps = json.dumps({k: m[k] for k in ("version", "bloc", "LBL", "CST")},
                       sort_keys=True, ensure_ascii=False)
    m["sha256"] = hashlib.sha256(corps.encode()).hexdigest()
    return m


# ===========================================================================
# LE PROMPT v2 — le squelette + LE DICTIONNAIRE, les DEUX empreintes gravées
# ===========================================================================
def prompt_ajouter_v2(nom_bloc: str) -> tuple[str, dict]:
    squelette, infos = generer_squelette(nom_bloc)
    dico = construire_dictionnaire(nom_bloc)
    table = ["", "LE DICTIONNAIRE DU DOMAINE (versionné) — tu n'écris "
               "JAMAIS une étiquette ni une constante en clair : tu émets "
               "l'ID, le client expande :"]
    for cle, e in dico["LBL"].items():
        table.append(f"  {cle} = l'étiquette {e['nom']} (cible de saut)")
    for cle, e in dico["CST"].items():
        if e["type"] == "iat":
            table.append(f"  {cle} = l'appel IAT au slot du plan "
                         f"(« call {cle} »)")
        elif e["type"] == "appel":
            table.append(f"  {cle} = l'appel direct {e['nom']} — "
                         f"{e['description']}")
        else:
            table.append(f"  {cle} = la constante {e['nom']} "
                         f"(la borne nommée)")
    table += ["",
              f"LES EMPREINTES GRAVÉES : gabarit sha256…{infos.get('sha256', '')[:0]}"
              f" | dictionnaire {dico['sha256'][:16]}… — TOUT écart du "
              f"dictionnaire = EXPANSION REFUSÉE (fail-closed)."]
    prompt = (
        "L'OPÉRATION AJOUTER DE LA CARTE TRIADE (le mode SQUELETTE-v2 — le\n"
        "cadre ABI, les types et la signature dérivés de la couche I par le\n"
        "client ; le DICTIONNAIRE DE DOMAINE versionné porte les étiquettes\n"
        "et les constantes admissibles du bloc : tu émets des IDs, le client\n"
        "expande).\n\n"
        f"LE CONTRAT DE COUCHE I (mot pour mot) :\n{infos['spec']}\n\n"
        f"LE SQUELETTE (généré par le client — NE LE RENDS PAS) :\n"
        f"{squelette}\n"
        + "\n".join(table) + "\n\n"
        "REQUÊTE : écris UNIQUEMENT LES LIGNES DE LA LOGIQUE — le corps du\n"
        "bloc qui vivra entre les balises du squelette. LES RÈGLES : (1)\n"
        "toute étiquette de saut DU BLOC se note par SON ID (ex. « je\n"
        "LBL-005 »), jamais en clair ; (2) tout appel IAT ou direct se\n"
        "note par SON ID (ex. « call CST-002 ») ; (3) toute constante se\n"
        "note par SON ID si elle y vit, SINON par sa VALEUR NUMÉRIQUE\n"
        "littérale (ex. « cmp r13, CST-001 » ou « cmp eax, 15 ») — JAMAIS\n"
        "un nom de symbole en clair (WM_PAINT, ANSI_FIXED_FONT : la valeur\n"
        "ou l'ID, rien d'autre) ; (4) tes étiquettes LOCALES à TOI se\n"
        "définissent « nom : » (un nom court, minuscule : « boucle : »,\n"
        "« fin : ») et se référent « boucle »/« fin » — N'ÉCRIS JAMAIS\n"
        "« LBL-xxx : » : les LBL-xxx sont des cibles DÉJÀ RÉSOLUES du\n"
        "plan, elles ne se définissent pas ; (5) les instructions du\n"
        "domaine seulement. La PREMIÈRE ligne de ta réponse est la première\n"
        "instruction, la DERNIÈRE la dernière — aucune balise, aucun\n"
        "texte d'explication (les commentaires « ; » en fin de ligne sont\n"
        "admis).\n\n"
        "EXEMPLE DE FORME (l'extrait d'un bloc — LA FORME, pas ton bloc) :\n"
        "cmp qword ptr [rbx + 528], -1\n"
        "je LBL-005\n"
        "test rcx, 0xf\n"
        "jne LBL-006\n"
        "mov r12, rcx\n"
        "cmp r12, qword ptr [rbx + 520]\n"
        "jae LBL-007\n"
        "cmp r13, CST-001\n"
        "jbe boucle\n"
        "boucle:\n"
        "call CST-002\n"
        "test eax, eax\n"
        "jz LBL-008\n"
        "ret\n"
    )
    return prompt, {"infos": infos, "squelette": squelette, "dico": dico,
                    "spec": infos["spec"]}


# ===========================================================================
# L'EXPANSION + L'ASSEMBLAGE v2 — les quatre refus nommés
# ===========================================================================
def expandir_ligne(ligne: str, dico: dict, adresse_instr: int) -> str:
    """UNE ligne expandée : les IDs remplacés aux littéraux du domaine —
    l'appel IAT au déplacement calculé À L'ADRESSE de l'instruction (la
    discipline de l'auteur : disp = slot − (adresse + taille))."""
    m = RE_LIGNE_ID.match(ligne)
    if not m:
        # une référence d'ID HORS les formes d'appel/saut (opérande) :
        # la forme « instr reg, CST-xxx »
        mm = re.match(r"^(\w[\w:]*(?:\s+\w+)*)\s*,\s*(LBL|CST)-([0-9]{3})$",
                      ligne)
        if mm:
            cle = f"{mm.group(2)}-{mm.group(3)}"
            if cle not in dico[mm.group(2)]:
                raise Refus("ID-INCONNU",
                            f"l'ID {cle} n'est pas au dictionnaire du bloc")
            e = dico[mm.group(2)][cle]
            if e.get("type") == "constante":
                return f"{mm.group(1)}, {e['valeur']}"
            raise Refus("EXPANSION-DIVERGENTE",
                        f"l'ID {cle} n'est pas une opérande expandable")
        return ligne
    mnemo, sorte, num = m.group(1), m.group(2), m.group(3)
    cle = f"{sorte}-{num}"
    if sorte == "LBL":
        if cle not in dico["LBL"]:
            raise Refus("ID-INCONNU", f"l'ID {cle} n'est pas au dictionnaire")
        # L'EXPANSION AU NOM CANONIQUE : l'adresse d'une étiquette INTERNE
        # dépend de la disposition du corps réécrit — le dictionnaire porte
        # le VOCABULAIRE admissible (le nom), la RÉSOLUTION locale (la
        # discipline de l'auteur) pose l'adresse à la disposition réelle
        return f"{mnemo} {dico['LBL'][cle]['nom']}_"
    if cle not in dico["CST"]:
        raise Refus("ID-INCONNU", f"l'ID {cle} n'est pas au dictionnaire")
    e = dico["CST"][cle]
    if e["type"] == "iat":
        taille = 7 if mnemo == "call" else 6      # call [rip+d32] / jcc rel32
        disp = e["slot"] - (adresse_instr + taille)
        signe = "+" if disp >= 0 else "-"
        return f"{mnemo} qword ptr [rip {signe} {abs(disp):#x}]"
    if e["type"] == "appel":
        return f"{mnemo} 0x{e['adresse']:x}"
    raise Refus("EXPANSION-DIVERGENTE",
                f"l'ID {cle} ({e.get('type')}) n'est pas une cible "
                f"d'appel")


def assembler_v2(squelette: str, logique: str, meta: dict) -> tuple[str, str]:
    """LE CLIENT ASSEMBLE v2 : (1) le dictionnaire RECOUPÉ (l'empreinte
    sha256 du matériau — DICT-DIVERGENT sinon) ; (2) HORS-FORMAT — la
    logique ne rend QUE des instructions du domaine, des définitions
    d'étiquettes locales OU des références d'ID ; (3) L'EXPANSION aux
    littéraux (ID-INCONNU / EXPANSION-DIVERGENTE aux écarts) ; (4) la
    résolution des étiquettes locales (la discipline de l'auteur) ; (5)
    l'assemblage squelette + logique, LE CADRE INTACT, LE ROUND-TRIP
    EXACT."""
    dico = meta["dico"]
    corps = json.dumps({k: dico[k] for k in ("version", "bloc", "LBL",
                                             "CST")},
                       sort_keys=True, ensure_ascii=False)
    if hashlib.sha256(corps.encode()).hexdigest() != dico["sha256"]:
        raise Refus("DICT-DIVERGENT",
                    "l'empreinte du dictionnaire divergente — le matériau "
                    "muté, l'expansion refusée (fail-closed)")
    # LE RECOUP CANONIQUE : le client REBUILD le dictionnaire du bloc —
    # un matériau muté (une borne décalée, un ID inventé) diverge du
    # canonique DU BLOC : DICT-DIVERGENT (le contrôle négatif le vit)
    canonique = construire_dictionnaire(dico["bloc"])
    if dico["sha256"] != canonique["sha256"]:
        raise Refus("DICT-DIVERGENT",
                    f"le dictionnaire du matériau diverge du canonique du "
                    f"bloc {dico['bloc']} — l'expansion refusée")
    lignes = [l.rstrip() for l in logique.strip("\r\n").split("\n")]
    if not any(l.strip() for l in lignes):
        raise Refus("HORS-FORMAT", "la logique est vide")
    propres = []
    for k, l in enumerate(lignes):
        s = l.split(";")[0].strip()
        if not s:
            continue
        if s.startswith(("```", ">>>", "<<<")) or "```" in s:
            raise Refus("HORS-FORMAT",
                        f"la ligne {k + 1} est un artefact : {s[:56]!r}")
        mm_def = re.match(r"^(LBL)-([0-9]{3})\s*:\s*$", s)
        if mm_def:
            cle = f"{mm_def.group(1)}-{mm_def.group(2)}"
            if cle not in dico["LBL"]:
                raise Refus("ID-INCONNU",
                            f"la définition {cle} n'est pas au dictionnaire")
            propres.append(f"{dico['LBL'][cle]['nom']}_:")
            continue
        if RE_DEF_ETIQ.match(s):
            propres.append(s)
            continue
        if RE_LIGNE_ID.match(s):
            propres.append(s)
            continue
        mm = re.match(r"^[\w:]+[^,]*,\s*(LBL|CST)-[0-9]{3}$", s)
        if mm:
            propres.append(s)
            continue
        if MON_INSTRUCTION.match(s):
            propres.append(s)
            continue
        raise Refus("HORS-FORMAT",
                    f"la ligne {k + 1} n'est pas une forme admise : "
                    f"{s[:56]!r}")
    # l'ancre d'adresse : le slot du bloc + le prologue assemblé
    rva = meta["infos"].get("rva") or 0x4000
    from keystone import Ks, KS_ARCH_X86, KS_MODE_64
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    taille_prologue = 0
    try:
        octets, _ = ks.asm("\n".join(meta["infos"]["pushes"]
                                     + [meta["infos"]["sub"]]))
        taille_prologue = len(octets)
    except Exception:
        taille_prologue = 0
    # LE POINT FIXE DES TAILLES (l'expansion IAT dépend de l'adresse de
    # l'instruction — la discipline de l'auteur : assembler, mesurer,
    # ré-expander ; les tailles convergent en une passe — la boucle
    # borne le point fixe à quatre passes)
    adresse = rva + taille_prologue
    expandees = []
    for _ in range(4):
        neuves = []
        cur = adresse
        for l in propres:
            if RE_DEF_ETIQ.match(l):
                neuves.append(l)
                continue
            a_un_id = bool(re.search(r"\b(?:LBL|CST)-[0-9]{3}\b", l))
            try:
                ex = expandir_ligne(l, dico, cur)
                try:
                    octets, _ = ks.asm(ex)
                except Exception:
                    # la référence d'étiquette LOCALE (la nôtre ou le nom
                    # canonique du dictionnaire) : le placeholder de taille
                    # — la résolution vit à resoudre_logique (le point fixe
                    # des tailles de l'auteur)
                    mm = re.match(r"^(j\w+|loop\w*)\s+\.?([A-Za-z_]\w*)$",
                                  ex)
                    if mm:
                        octets, _ = ks.asm(f"{mm.group(1)} 0x{cur:x}")
                    elif a_un_id:
                        raise Refus("EXPANSION-DIVERGENTE",
                                    f"la ligne expandée ne s'assemble pas : "
                                    f"{l[:40]!r} -> {ex[:44]!r}")
                    else:
                        raise Refus("HORS-FORMAT",
                                    f"ligne inassemblable : {l[:52]!r}")
                cur += len(octets)
                neuves.append(ex)
            except Refus:
                raise
            except Exception as e:
                raise Refus("EXPANSION-DIVERGENTE",
                            f"la ligne expandée ne s'assemble pas : "
                            f"{l[:40]!r} ({type(e).__name__})")
        if neuves == expandees:
            break                     # LE POINT FIXE ATTEINT
        expandees = neuves
    # la résolution des étiquettes LOCALES (le client v8 TEL QUEL)
    explicites, reso = resoudre_logique(expandees, adresse)
    avant, apres = squelette.split(BALISE_DEBUT, 1)
    _, apres = apres.split(BALISE_FIN, 1)
    note = ""
    if reso:
        note = ("; Étiquettes résolues : " + ", ".join(
            f"{n}=0x{a:x}" for n, a in reso.items()) + "\n")
    assemble = (avant + note + BALISE_DEBUT + "\n"
                + "\n".join(explicites) + "\n" + BALISE_FIN + apres)
    # LE CADRE INTACT (le juge du cadre — AUCUN contrôle retiré)
    for l in meta["infos"]["pushes"] + [meta["infos"]["sub"]]:
        if l not in assemble:
            raise Refus("HORS-FORMAT",
                        f"le cadre ABI a perdu « {l} » — le juge du cadre")
    for l in reversed(meta["infos"]["pushes"]):
        if f"pop {l.split()[1]}" not in assemble:
            raise Refus("HORS-FORMAT",
                        f"l'épilogue a perdu « pop {l.split()[1]} »")
    # LE ROUND-TRIP EXACT (le client v8 TEL QUEL — AUCUN contrôle retiré :
    # keystone == capstone == keystone, tout écart d'instruction, d'opérande
    # ou de taille est un refus)
    try:
        ok, detail = round_trip(assemble)
        if not ok:
            raise Refus("EXPANSION-DIVERGENTE",
                        f"le round-trip a divergé : {detail[:70]}")
        return assemble, detail
    except Refus:
        raise
    except Exception as e:
        raise Refus("EXPANSION-DIVERGENTE",
                    f"le round-trip a échoué : {type(e).__name__}")
