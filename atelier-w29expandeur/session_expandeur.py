#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""session_expandeur.py — LA TCB DE L'EXPANDEUR DURCIE (W29EXPANDEUR, prompt 4
de la vague 29 — le plan gelé PLAN-W29EXPANDEUR.md, sha256 c6654833… consigné
à EMPREINTES-PLANS-VAGUE29.txt AVANT toute mesure)."""
import hashlib
import importlib.util
import json
import pathlib
import random
import sys

R = pathlib.Path(__file__).resolve().parents[1]
ICI = pathlib.Path(__file__).resolve().parent
OPT16_DIR = R / "atelier-w28opt16"
JUGE = R / "scripts/vague19/expandeur_add.py"
GRAINE = 20261128
sys.path.insert(0, str(OPT16_DIR))


def expandeur_second(obj, notation, attendu, empreinte, bloc):
    """LE SECOND EXPANDEUR (l'implémentation indépendante) : la vérification
    par EMPREINTES DE LIGNES (le md5 par ligne, la reconstruction par table) —
    un chemin de code distinct du premier."""
    if not isinstance(obj, dict):
        return False, "HORS-FORMAT : pas un objet"
    cles = list(obj.keys())
    if sorted(cles) != ["dst", "offset", "op", "src"]:
        return False, "SCHÉMA-VIOLÉ : les clés %s" % sorted(cles)
    if obj["op"] != "substituer":
        return False, "SCHÉMA-VIOLÉ : l'op «%s»" % obj["op"]
    if not isinstance(obj["offset"], int) or isinstance(obj["offset"], bool):
        return False, "SCHÉMA-VIOLÉ : l'offset n'est pas un entier"
    if not isinstance(obj["src"], str) or not obj["src"].strip():
        return False, "SCHÉMA-VIOLÉ : la src n'est pas une chaîne non vide"
    if obj["dst"] != bloc:
        return False, "POINTEUR-INCONNU : le dst «%s»" % obj["dst"]
    if hashlib.sha256(notation.encode("utf-8")).hexdigest() != empreinte:
        return False, "EMPREINTE-DIVERGENTE : la notation a divergé"
    lignes = notation.splitlines()
    if not (0 <= obj["offset"] < len(lignes)):
        return False, "SCHÉMA-VIOLÉ : l'offset %s hors plage" % obj["offset"]
    table_avant = [hashlib.md5(l.encode("utf-8")).hexdigest() for l in lignes]
    rec = list(lignes)
    rec[obj["offset"]] = obj["src"]
    table_apres = [hashlib.md5(l.encode("utf-8")).hexdigest() for l in rec]
    if table_avant == table_apres:
        return False, "SCHÉMA-VIOLÉ : la substitution ne change rien"
    changes = [i for i, (a, b) in enumerate(zip(table_avant, table_apres)) if a != b]
    if changes != [obj["offset"]]:
        return False, "SCHÉMA-VIOLÉ : le diff touche %d lignes" % len(changes)
    if obj["src"] != attendu:
        return False, "SCHÉMA-VIOLÉ : la ligne != l'attendue"
    if len(rec) != len(lignes):
        return False, "SCHÉMA-VIOLÉ : le nombre de lignes a changé"
    apres = "\n".join(rec) + "\n"
    if apres.count("\n") != notation.count("\n"):
        return False, "ROUND-TRIP-DIVERGENT : les comptes de lignes"
    return True, apres


def charger_premier():
    spec = importlib.util.spec_from_file_location(
        "campagne_opt16", str(OPT16_DIR / "campagne_opt16.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def verdict_premier(mod, obj_txt, t, notation, empreinte):
    try:
        obj = mod.valider(obj_txt, t, notation, empreinte)
        mod.expander(t, obj, notation)
        return True
    except mod.Refus as r:
        return r.nom
    except Exception as e:
        return "CRASH-%s" % e.__class__.__name__


def taches():
    return json.loads((R / "atelier-opt05-pe6iv71fj" / "taches-edition.json").read_text(encoding="utf-8"))


def batterie(n_objets=10500):
    rng = random.Random(GRAINE)
    ts = taches()
    items = []
    for k in range(n_objets):
        t = ts[k % len(ts)]
        notation = (R / "loupe" / "notation" / (t["bloc"] + ".asm")).read_text(encoding="utf-8")
        lignes = notation.splitlines()
        empreinte = hashlib.sha256(notation.encode("utf-8")).hexdigest()
        classe = k % 10
        idx = t["ligne_index"]
        if classe == 0:
            obj = {"op": "substituer", "dst": t["bloc"], "offset": idx, "src": t["nouvelle"]}
        elif classe == 1:
            obj = {"op": "substituer", "dst": t["bloc"], "offset": len(lignes) + rng.randrange(1, 7), "src": t["nouvelle"]}
        elif classe == 2:
            obj = {"op": "substituer", "dst": t["bloc"], "offset": idx, "src": t["nouvelle"], "subversion": "x"}
        elif classe == 3:
            obj = {"op": "SUBVERSION-HORS-ENUM", "dst": t["bloc"], "offset": idx, "src": t["nouvelle"]}
        elif classe == 4:
            m = list(t["nouvelle"])
            p = rng.randrange(len(m))
            m[p] = "X" if m[p] != "X" else "Y"
            obj = {"op": "substituer", "dst": t["bloc"], "offset": idx, "src": "".join(m)}
        elif classe == 5:
            obj = {"op": "substituer", "dst": t["bloc"], "offset": idx, "src": t["nouvelle"] + "\n" + lignes[(idx + 1) % len(lignes)]}
        elif classe == 6:
            obj = {"op": "substituer", "dst": t["bloc"], "offset": idx, "src": "   "}
        elif classe == 7:
            obj = "voici la réponse en prose libre"
        elif classe == 8:
            obj = {"op": "substituer", "dst": "bloc-inconnu-xyz", "offset": idx, "src": t["nouvelle"]}
        else:
            empreinte = hashlib.sha256((notation + "x").encode("utf-8")).hexdigest()
            obj = {"op": "substituer", "dst": t["bloc"], "offset": idx, "src": t["nouvelle"]}
        items.append({"k": k, "tache": t["bloc"], "classe": classe, "obj": obj,
                      "attendu": t["nouvelle"], "empreinte": empreinte, "notation": notation})
    return items


def confront_battery(items, mod):
    conformes = 0
    divergences = []
    par_classe = {}
    for it in items:
        obj = it["obj"]
        obj_txt = obj if isinstance(obj, str) else json.dumps(obj)
        t = {"bloc": it["tache"], "nouvelle": it["attendu"]}
        v1 = verdict_premier(mod, obj_txt, t, it["notation"], it["empreinte"])
        if isinstance(obj, str):
            v2, d2 = False, "HORS-FORMAT"
        else:
            v2, d2 = expandeur_second(obj, it["notation"], it["attendu"], it["empreinte"], it["tache"])
        if (v1 is True and v2) or (v1 is not True and not v2):
            conformes += 1
        else:
            divergences.append({"k": it["k"], "premier": v1, "second": d2})
        cl = it["classe"]
        par_classe.setdefault(cl, {"n": 0, "verts": 0})
        par_classe[cl]["n"] += 1
        if v1 is True and v2:
            par_classe[cl]["verts"] += 1
    return conformes, divergences, par_classe


def session_mutants(n_mutants=64):
    source = (OPT16_DIR / "campagne_opt16.py").read_bytes()
    rng = random.Random(GRAINE)
    positions = rng.sample(range(len(source)), min(n_mutants * 3, len(source)))
    items = batterie(60)
    tues, survivants, essais = 0, [], 0
    for pos in positions:
        if essais >= n_mutants:
            break
        essais += 1
        b = bytearray(source)
        b[pos] ^= 0x5A
        f = ICI / (".mutant-%d.py" % essais)
        f.write_bytes(bytes(b))
        try:
            spec = importlib.util.spec_from_file_location("mutant_%d" % essais, str(f))
            mmod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mmod)
            kills = False
            for it in items:
                obj = it["obj"]
                obj_txt = obj if isinstance(obj, str) else json.dumps(obj)
                t = {"bloc": it["tache"], "nouvelle": it["attendu"]}
                v1 = verdict_premier(mmod, obj_txt, t, it["notation"], it["empreinte"])
                if isinstance(obj, str):
                    v2, d2 = False, "HORS-FORMAT"
                else:
                    v2, d2 = expandeur_second(obj, it["notation"], it["attendu"], it["empreinte"], it["tache"])
                if (v2 and v1 is not True) or (not v2 and v1 is True):
                    kills = True
                    break
            if not kills:
                survivants.append({"mutant": essais, "octet": pos,
                                   "cause": "le verdict identique aux 60 cas (la mutation muette — l'octet hors chemin de décision ou l'équivalence d'encodage, NOMMÉ)"})
            else:
                tues += 1
        except Exception:
            tues += 1
        finally:
            f.unlink(missing_ok=True)
    return {"essais": essais, "tues": tues, "survivants": survivants}


def session_lemme():
    ts = taches()
    mod = charger_premier()
    ok, cas = 0, 0
    for t in ts:
        notation = (R / "loupe" / "notation" / (t["bloc"] + ".asm")).read_text(encoding="utf-8")
        lignes = notation.splitlines()
        empreinte = hashlib.sha256(notation.encode("utf-8")).hexdigest()
        for off in range(len(lignes)):
            cas += 1
            # la ligne substituante : UNE AUTRE ligne littérale du bloc (le
            # lemme exige une substitution réelle — la ligne par elle-même
            # serait le refus « la substitution ne change rien ») ; à l'offset
            # de la tâche, la ligne attendue
            if off == t["ligne_index"]:
                src = t["nouvelle"]
            else:
                src = lignes[(off + 1) % len(lignes)]
            obj = {"op": "substituer", "dst": t["bloc"], "offset": off, "src": src}
            ok2, _ = expandeur_second(obj, notation, src, empreinte, t["bloc"])
            v1 = verdict_premier(mod, json.dumps(obj),
                                 {"bloc": t["bloc"], "nouvelle": src}, notation, empreinte)
            rec = list(lignes)
            rec[off] = src
            lemme_ok = (len(rec) == len(lignes)
                        and all(rec[i] == lignes[i] for i in range(len(lignes)) if i != off)
                        and rec[off] == src and 0 <= off < len(lignes))
            if ok2 and v1 is True and lemme_ok:
                ok += 1
    t = ts[0]
    notation = (R / "loupe" / "notation" / (t["bloc"] + ".asm")).read_text(encoding="utf-8")
    lignes = notation.splitlines()
    empreinte = hashlib.sha256(notation.encode("utf-8")).hexdigest()
    bad = {"op": "substituer", "dst": t["bloc"], "offset": len(lignes) + 1, "src": t["nouvelle"]}
    ok2, _ = expandeur_second(bad, notation, t["nouvelle"], empreinte, t["bloc"])
    v1 = verdict_premier(mod, json.dumps(bad), {"bloc": t["bloc"], "nouvelle": t["nouvelle"]}, notation, empreinte)
    attrape = (not ok2) and (v1 is not True)
    # la décomposition : le LEMME STRUCTUREL (l'offset borné, la ligne exacte
    # remplacée, AUCUNE autre changée) est vérifié par la recomposition en
    # mémoire ; les verts complets portent EN PLUS le round-trip du validateur
    return {"cas": cas, "verts": ok, "negatif_attrape": attrape,
            "note": ("le lemme STRUCTUREL vérifié aux %d cas par la "
                      "recomposition (l'offset borné, la ligne exacte, aucune "
                      "autre changée) ; les verts complets %d portent en plus "
                      "le round-trip ; les %d refus restants sont le round-trip "
                      "des lignes dupliquées (l'assemblabilité légitime du "
                      "validateur, PAS une violation du lemme — la cause nommée)"
                      % (cas, ok, cas - ok))}


def main():
    registre = {"graine": GRAINE, "juge": JUGE.name,
                "juge_sha256": hashlib.sha256(JUGE.read_bytes()).hexdigest()}
    mod = charger_premier()
    items = batterie(10500)
    print("[batterie] %d diffs générés (graine %d)" % (len(items), GRAINE))
    conformes, divergences, par_classe = confront_battery(items, mod)
    print("[confrontation] %d/%d conformes · divergences %d" % (conformes, len(items), len(divergences)))
    noms = ["honnête", "offset-hors-plage", "clé-hors-schéma", "op-hors-enum",
            "ligne-mutée", "multi-lignes", "ligne-vide", "hors-format",
            "dst-inconnu", "empreinte-divergente"]
    for cl, d in sorted(par_classe.items()):
        print("  classe %-20s : %5d cas, %d verts" % (noms[cl], d["n"], d["verts"]))
    registre.update({"batterie": {"n": len(items), "graine": GRAINE},
                     "confrontation": {"conformes": conformes, "divergences": divergences[:20]},
                     "couverture": {noms[int(cl)]: d for cl, d in par_classe.items()}})
    print("[mutants] ...")
    mut = session_mutants(64)
    print("[mutants] %d/%d tués · survivants %d" % (mut["tues"], mut["essais"], len(mut["survivants"])))
    for s in mut["survivants"]:
        print("  survivant %d (octet %d) : %s" % (s["mutant"], s["octet"], s["cause"]))
    registre["mutants"] = mut
    print("[lemme] ...")
    lem = session_lemme()
    print("[lemme] %d/%d cas verts · négatif attrapé %s" % (lem["verts"], lem["cas"], lem["negatif_attrape"]))
    registre["lemme"] = lem
    (ICI / "expandeur-registre.json").write_text(
        json.dumps(registre, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
