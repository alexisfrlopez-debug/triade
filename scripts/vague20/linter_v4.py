#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE LINTER D'ÉDITION v4 — PORTÉ À LA PORTE DE GÉNÉRATION v0.26.0 (W19LINT).

Onze classes, chacune falsifiable :
  C1  PHRASES SÉMANTIQUES        — revendications interdites, étiquettes d'ère périmées ;
  C2  PLAGES DE DÉCISIONS        — la plage annoncée et les lignes des décisions récentes ;
  C3  REVENDICATIONS DE VERSION  — chaque pièce porte SA chaîne, aucune celle d'une autre ;
  C4  GALLICISMES ANGLAIS        — les calques interdits dans le texte anglais ;
  C5  NUMÉRAUX DE LA PROSE       — chaque valeur publiée se recompose de ses opérandes ;
  C6  VERSION-TABLE              — le tableau §10 de la présentation == le manifeste du pack ;
  C7  DECISION-RANGE             — tout ID cité ⊆ [D1, dernière décision réelle] ;
  C8  CHANGELOG-ORDER            — ordre chronologique strict du changelog gelé ;
  C9  NUMEROTATION               — une seule convention de renvoi (spec § x.y vs doc § n) ;
  C10 BENCH-COUNT                — tout n/n annoncé recomposé depuis les cas du kit ;
  C11 SEMANTIC-THREAT            — chaque « détecté — … » du §15.1 qualifié (classe, bord),
                                   confronté à §7.7/D254 ; plus de « toutes neutralisées ».

Usage : python3 scripts/vague19/linter_v260.py [--controle-negatif] [--pack DIR]
Sortie : 0 = 0 résidu ; 2 = résidus nommés ; 3 = un contrôle négatif non attrapé.
"""
import argparse
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys

RACINE = pathlib.Path(__file__).resolve().parents[2]
def _pack_defaut():
    def _num(d):
        m = re.search(r"pack-v(\d+)", d.name)
        return int(m.group(1)) if m else 0
    return sorted([d for d in RACINE.glob("pack-v*") if d.is_dir()], key=_num)[-1]


PACK_DEFAUT = _pack_defaut()
def _derniere_decision():
    """La borne de DECISION-RANGE est DÉRIVÉE du journal (D273), plus une constante :
    une décision ajoutée au journal relève la borne sans qu'on touche au linter."""
    j = RACINE / "docs/DECISIONS.md"
    ids = [int(x) for x in re.findall(r"^## D(\d{1,3})\b", j.read_text(encoding="utf-8"), re.M)]
    return max(ids) if ids else 0


DERNIERE_DECISION = _derniere_decision()
CLASSES_ADV = ("ADV-LOCAL", "ADV-ADMIN", "ADV-MEDIA", "ADV-DISTANT")
BORDS = ("EN-LIGNE", "HORS-LIGNE", "LES-DEUX")


def pieces(pack):
    """Les cinq pièces se lisent par MOTIF : le linter suit l'édition, il ne la code pas."""
    def _un(dossier, motif):
        c = sorted((pathlib.Path(pack) / dossier).glob(motif))
        return c[-1] if c else pathlib.Path(pack) / dossier / "absent.pdf"
    return {
        "manuscrit": _un("1-manuscrit", "TRIADE_manuscrit_v*.pdf"),
        "specification": _un("2-specification", "Protocole_TRIADE_v*_Specification.pdf"),
        "livre": _un("3-coffre-fort", "Livre_du_Coffre_*.pdf"),
        "preuves": _un("4-preuves-calculs", "TRIADE_preuves_et_calculs_v*.pdf"),
        "presentation": _un("5-presentation", "TRIADE_presentation_v*.pdf"),
    }


def normalise(t):
    """Normalisation typographique (C12/C19) : NFKC, capitales espacées, variantes « est la vX »."""
    import unicodedata
    import re as _re
    t = unicodedata.normalize("NFKC", t)
    # « V E R S I O N 1. 1 0 » -> « VERSION 1.10 »
    t = _re.sub(r"\b((?:[A-Za-zÀ-ÿ]\s){2,}[A-Za-zÀ-ÿ])\b",
                lambda m: m.group(1).replace(" ", ""), t)
    t = _re.sub(r"(\d)\s*\.\s*(\d)", r"\1.\2", t)
    return t


def texte(p):
    if not pathlib.Path(p).exists():
        return ""
    r = subprocess.run(["pdftotext", str(p), "-"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def charge(pack):
    return {k: texte(v) for k, v in pieces(pack).items()}


def charge_manifeste(pack):
    m = {}
    f = pack / "empreintes_livrables_v0.27.0.txt"
    if not f.exists():
        return m
    for ligne in f.read_text(encoding="utf-8").splitlines():
        if "  " in ligne and len(ligne.split()[0]) == 64:
            h, nom = ligne.split("  ", 1)
            m[nom.strip()] = h.strip()
    return m


def recompte_banc():
    r = subprocess.run([sys.executable, str(RACINE / "scripts/vague19/recompte_banc.py"), "--json"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None
    return json.loads(r.stdout)


def _versions(pack):
    """Les versions attendues se lisent des noms de fichiers du pack (le linter suit l'édition)."""
    noms = [f.name for f in pathlib.Path(pack).rglob("*.pdf")]
    def v(motif):
        for n in noms:
            m = re.search(motif, n)
            if m:
                return m.group(1)
        return ""
    return (v(r"TRIADE_manuscrit_(v[0-9.]+)\.pdf"),
            v(r"Protocole_TRIADE_(v[0-9.]+)_Specification"),
            v(r"CF1-CF3_(v[0-9.]+)\.pdf"))


def verifie(t, manifeste=None, recompte=None, pack=None):
    pack = pathlib.Path(pack or PACK_DEFAUT)
    refus = []
    ED, SP, BK = _versions(pack)

    # C1 — phrases sémantiques
    if re.search(r"edition \(v0\.2[0-4]\.\d+\) restates", t["manuscrit"]):
        refus.append(("C1", "manuscrit", "l'abstract porte une version d'ère périmée"))
    if "the training corpus of 109 triples" in t["manuscrit"] and "(v2, historical" not in t["manuscrit"]:
        refus.append(("C1", "manuscrit", "les 109 triples ne sont pas étiquetés historiques"))
    if "11/11 refus nommés rendus" in t["presentation"]:
        refus.append(("C1", "presentation", "« 11/11 refus » non corrigé"))

    # C2 — plages de décisions
    if not re.search(r"D75\s*[-–]+\s*D268", t["specification"]):
        refus.append(("C2", "specification", "la plage D75–D268 est absente de l'annexe B"))
    for d in ("D261", "D262", "D263", "D264", "D267", "D268"):
        if d not in t["specification"]:
            refus.append(("C2", "specification", f"la ligne {d} est absente"))
    if "D251" in t["manuscrit"]:
        refus.append(("C2", "manuscrit", "le manuscrit annonce encore D251"))

    # C3 — revendications de version
    attendu = {"manuscrit": ED, "specification": SP, "livre": BK,
               "preuves": ED, "presentation": ED}
    for piece, ver in attendu.items():
        if ver not in t[piece]:
            refus.append(("C3", piece, f"la chaîne {ver} est absente"))

    # C4 — gallicismes anglais
    for calque in ["permits to ", "allows to ", "perennisation", "dispose of the possibility",
                   "the present edition permits to", "harmonisation of the"]:
        if calque in t["manuscrit"].lower():
            refus.append(("C4", "manuscrit", f"calque interdit : {calque.strip()}"))

    # C5 — numéraux de la prose
    if "3.23×" in t["manuscrit"] or "3.23x" in t["manuscrit"]:
        refus.append(("C5", "manuscrit", "le ratio fautif 3.23 est publié comme valeur"))
    if "3.22" not in t["manuscrit"]:
        refus.append(("C5", "manuscrit", "le ratio corrigé 3.22 est absent"))
    for attendu_txt in ("712,5", "37,425", "49,12"):
        if attendu_txt not in t["preuves"]:
            refus.append(("C5", "preuves", f"le numéral {attendu_txt} est absent"))

    # C6 — VERSION-TABLE : le tableau §10 == le manifeste
    versions = {"Manuscrit": ED, "Spécification": SP, "Livre du Coffre": BK,
                "Preuves et calculs": ED, "Présentation": ED}
    pres = t["presentation"]
    for libelle, ver in versions.items():
        m = re.search(re.escape(libelle) + r"\s*\n?\s*(v?\d+\.\d+(?:\.\d+)?)", pres)
        if not m:
            refus.append(("C6", "presentation", f"ligne §10 « {libelle} » introuvable"))
        elif m.group(1).lstrip("v") != ver.lstrip("v"):
            refus.append(("C6", "presentation",
                          f"§10 {libelle} = {m.group(1)} ≠ manifeste {ver}"))
    for vieux in ("v0.25.0", "v0.15.10", "v1.9"):
        # une étiquette d'ère dans le tableau §10 est refusée ; les mentions historiques
        # du corps (append-only) restent admises hors de la section 10
        i10 = pres.find("10. L'édition")
        if i10 >= 0 and vieux in pres[i10:i10 + 1200]:
            refus.append(("C6", "presentation", f"§10 porte encore l'étiquette {vieux}"))

    # C7 — DECISION-RANGE
    for piece in ("manuscrit", "specification", "livre", "preuves", "presentation"):
        ids = set(int(x) for x in re.findall(r"\bD(\d{1,3})\b", t[piece]))
        hauts = [i for i in ids if i > DERNIERE_DECISION]
        bas = [i for i in ids if i < 1]
        if hauts:
            refus.append(("C7", piece, f"ID hors plage : D{max(hauts)} > D{DERNIERE_DECISION}"))
        if bas:
            refus.append(("C7", piece, f"ID hors plage : D{min(bas)} < D1"))
        for plage in re.findall(r"D(\d{1,3})\s*[-–]+\s*D(\d{1,3})", t[piece]):
            lo, hi = int(plage[0]), int(plage[1])
            if hi > DERNIERE_DECISION or lo > hi:
                refus.append(("C7", piece, f"plage déclarée D{lo}–D{hi} incohérente"))

    # C8 — CHANGELOG-ORDER (dates croissantes)
    entrees = re.findall(r"\\item v(\d+\.\d+(?:\.\d+)?) \((\d{1,2}) (\w+) (\d{4})\)", t["manuscrit"])
    if not entrees:
        # pdftotext perd les \\item : on relit la source si le PDF ne porte pas la forme brute
        src = (RACINE / "edition-v0230" / "main.tex").read_text(encoding="utf-8")
        entrees = re.findall(r"\\item v(\d+\.\d+(?:\.\d+)?) \((\d{1,2}) (\w+) (\d{4})\)", src)
    mois = {m: i for i, m in enumerate(
        ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}
    dates = [(int(a), mois.get(b, 0), int(c)) for _v, a, b, c in entrees]
    for i in range(1, len(dates)):
        if dates[i] < dates[i - 1]:
            refus.append(("C8", "manuscrit",
                          f"changelog hors ordre à l'entrée {i + 1} ({entrees[i][0]} après {entrees[i-1][0]})"))
            break

    # C9 — NUMEROTATION : une seule convention, sur la PARTIE NARRATIVE des preuves
    # (les rapports d'atelier sont lus verbatim : ils peuvent citer une règle du linter)
    narratif = t["preuves"].split("W24AUDT —")[0]
    fautifs = [m for m in re.finditer(r"§\s*(?!spec\b)\d+\.\d+", narratif)
               if not any(x in narratif[max(0, m.start() - 40):m.end() + 60]
                          for x in ("de la spécification", "de la spec", "Spécification",
                                    "présentation", "preuves", "section"))]
    if fautifs:
        refus.append(("C9", "preuves", "renvoi de section sans la convention « spec § x.y »"))
    if "8.6" in narratif:
        refus.append(("C9", "preuves", "renvoi §8.6 (D254 est en spec §7.7)"))
    for ref in ("spec 7.6", "spec 7.7", "spec 7.8", "spec 7.9", "spec 7.10", "spec 7.11"):
        if ref not in narratif:
            refus.append(("C9", "preuves", f"le renvoi normalisé « {ref} » est absent"))

    # C10 — BENCH-COUNT
    if recompte is not None:
        pub = f"{recompte['total']}/{recompte['total']}"
        plat = re.sub(r"\s+", " ", t["presentation"])
        if pub not in plat:
            refus.append(("C10", "presentation", f"le compte recomposé {pub} n'est pas publié"))
        attendus = [f"{recompte['cas_transaction']} cas de transaction",
                    f"{recompte['aleas_refus']} aléas",
                    f"{recompte['invariants']} invariants"]
        for a in attendus:
            if a not in plat:
                refus.append(("C10", "presentation",
                              f"la composante recomposée « {a} » n'est pas publiée"))

    # C11 — SEMANTIC-THREAT
    spec = t["specification"]
    # la DERNIÈRE occurrence de « Modèle de menace » est le corps (la première est le
    # sommaire) : une zone vide serait un faux vert, elle est refusée explicitement
    occurrences = [m.start() for m in re.finditer(r"15\.1\s+Modèle de menace", spec)]
    i151 = occurrences[-1] if occurrences else -1
    if i151 < 0:
        refus.append(("C11", "specification", "le §15.1 est introuvable"))
    else:
        zone = spec[i151:i151 + 8000]
        if zone.count("détecté") < 5:
            refus.append(("C11", "specification",
                          f"zone §15.1 inexploitable : {zone.count('détecté')} ligne(s) « détecté »"))
        lignes = zone.splitlines()
        for i, ligne in enumerate(lignes):
            if "détecté" not in ligne or "Chaque ligne" in ligne:
                continue
            # la cellule peut se poursuivre sur les lignes suivantes, mais JAMAIS au-delà
            # de la prochaine occurrence de « détecté » (une autre rangée)
            suite = []
            for j in range(i + 1, min(i + 8, len(lignes))):
                if "détecté" in lignes[j]:
                    break
                suite.append(lignes[j])
            voisin = " ".join([ligne] + suite)
            if not (any(c in voisin for c in CLASSES_ADV) and any(b in voisin for b in BORDS)):
                refus.append(("C11", "specification",
                              f"ligne « détecté » non qualifiée : {ligne.strip()[:60]}"))
        if "toutes sont neutralisées" in zone:
            refus.append(("C11", "specification", "« toutes sont neutralisées » encore revendiqué"))
        if "D254" not in zone and "D267" not in zone:
            refus.append(("C11", "specification", "le §15.1 ne renvoie ni à D254 ni à D267"))

    # C12 — VERSION-PROSE : toute mention de prose confrontée au manifeste
    prose = [(k, t[k]) for k in ("manuscrit", "specification", "livre", "preuves", "presentation")]
    for piece, texte in prose:
        # dans le Livre, « l'édition courante » désigne la SPÉCIFICATION qu'il accompagne
        attendu_ed = SP if piece == "livre" else ED
        # les rapports d'atelier sont lus verbatim : ils peuvent citer un résidu soldé
        if piece == "preuves":
            texte = texte.split("W24AUDT —")[0]
        for m in re.finditer(r"(?:édition courante|Édition courante|current edition)\s+(v\d+\.\d+(?:\.\d+)?)", texte):
            if m.group(1) != attendu_ed:
                refus.append(("C12", piece, f"« édition courante {m.group(1)} » ≠ {attendu_ed}"))
        if piece == "livre":
            for m in re.finditer(r"(?:révision|revision)\s+(v\d+\.\d+(?:\.\d+)?)", texte):
                if m.group(1) != BK:
                    refus.append(("C12", piece, f"« révision {m.group(1)} » ≠ {BK}"))
        if piece == "livre":
            for m in re.finditer(r"(?:la |the )?spécification\s+(v\d+\.\d+(?:\.\d+)?)", texte):
                if m.group(1) != SP:
                    refus.append(("C12", piece, f"« spécification {m.group(1)} » ≠ {SP}"))
    for vieux in ("v0.15.10", "v1.9"):
        if vieux in t["livre"]:
            refus.append(("C12", "livre", f"version périmée {vieux} dans le Livre"))

    # C13 — WAVE-CONTINUITY : toute « vague N » a son entrée datée
    mots = {"quinzième": 15, "seizième": 16, "dix-septième": 17, "dix-huitième": 18,
            "dix-neuvième": 19, "vingtième": 20}
    entrees = set()
    for m in re.finditer(r"the (fifteenth|sixteenth|seventeenth|eighteenth|nineteenth|twentieth|twenty-first|twenty-second) wave", t["manuscrit"]):
        entrees.add({"fifteenth": 15, "sixteenth": 16, "seventeenth": 17, "eighteenth": 18,
                     "nineteenth": 19, "twentieth": 20, "twenty-first": 21,
                     "twenty-second": 22}[m.group(1)])
    for piece, texte in [("presentation", t["presentation"])]:
        for m in re.finditer(r"vague\s+(\d{1,2})", texte):
            n = int(m.group(1))
            if n not in entrees:
                ctx = texte[max(0, m.start() - 120):m.end() + 120]
                if "sans édition" not in ctx and "hors édition" not in ctx:
                    refus.append(("C13", piece, f"« vague {n} » sans entrée au changelog"))

    # C14 — ABSTRACT-LENGTH : résumé anglais ≤ 250 mots (métadonnées exclues ; le résumé
    # français est sa traduction, la classe ne mesure pas deux fois la même prose)
    man = t["manuscrit"]
    i = man.find("Abstract")
    j = man.find("Keywords", i + 1) if i >= 0 else -1
    if i < 0 or j < 0:
        refus.append(("C14", "manuscrit", "résumé ou borne « Keywords » introuvable"))
    else:
        lignes = [l for l in man[i:j].splitlines() if not l.lstrip().startswith("*")]
        mots_resume = len(re.findall(r"[A-Za-z][A-Za-z\-']+", " ".join(lignes)))
        if mots_resume > 250:
            refus.append(("C14", "manuscrit", f"résumé {mots_resume} mots > 250"))

    # C15 — READER-TEST-COUNT : le compte se recompose de ses cas énumérés
    pre = t["preuves"]
    m = re.search(r"Test du lecteur\s*:\s*(\d+)/(\d+)", pre)
    if not m:
        refus.append(("C15", "preuves", "compte du test du lecteur introuvable"))
    else:
        annonces = int(m.group(1))
        trouves = len(re.findall(r"\((\d{1,2})\)\s", pre[m.end():m.end() + 900]))
        if annonces != trouves or m.group(1) != m.group(2):
            refus.append(("C15", "preuves",
                          f"compte {m.group(1)}/{m.group(2)} ≠ {trouves} cas énumérés"))
    # C16 — STATUS-REGISTRY : le registre unique, et le compte annoncé recomposé
    reg = RACINE / "STATUTS-EN-ATTENTE.md"
    if not reg.exists():
        refus.append(("C16", "registre", "STATUTS-EN-ATTENTE.md absent"))
    else:
        entrees = [l for l in reg.read_text(encoding="utf-8").splitlines() if l.startswith("| ATT-")]
        import unicodedata
        def _nu(x):
            return "".join(c for c in unicodedata.normalize("NFD", x) if unicodedata.category(c) != "Mn")
        vocab = {"EN ATTENTE", "MESURE", "REFUSE", "PARTIEL"}
        for l in entrees:
            cellules = [c.strip() for c in l.strip("|").split("|")]
            if len(cellules) < 5:
                refus.append(("C16", "registre", f"ligne incomplète : {cellules[0][:12]}"))
                continue
            statut = cellules[2]
            if not any(_nu(statut).upper().startswith(v) for v in vocab):
                refus.append(("C16", "registre", f"{cellules[0]} : statut hors vocabulaire « {statut} »"))
            if len(cellules) >= 6:
                try:
                    gele = int(cellules[5])
                except ValueError:
                    refus.append(("C16", "registre", f"{cellules[0]} : colonne de péremption illisible"))
                    gele = 0
                if gele > 2 and "justifi" not in l.lower():
                    refus.append(("C16", "registre",
                                  f"{cellules[0]} gelée depuis {gele} vagues sans justification"))
            else:
                refus.append(("C16", "registre", f"{cellules[0]} : colonne de péremption absente"))
            dec = re.search(r"D(\d{1,3})", cellules[4])
            if dec and int(dec.group(1)) > DERNIERE_DECISION:
                refus.append(("C16", "registre", f"{cellules[0]} : décision D{dec.group(1)} hors plage"))
        annonce = re.search(r"registre unique des chantiers en attente porte (\d+) entrées", t["presentation"])
        if not annonce:
            refus.append(("C16", "presentation", "le compte du registre n'est pas annoncé"))
        elif int(annonce.group(1)) != len(entrees):
            refus.append(("C16", "presentation",
                          f"annonce {annonce.group(1)} entrées ≠ registre {len(entrees)}"))
    # C17 — ORACLE-COUNT : le compte des vecteurs et des défauts se recompose des fichiers
    res = RACINE / "atelier-w22-audit" / "contextes-resultat.json"
    if res.exists():
        d = json.loads(res.read_text(encoding="utf-8"))
        plat = re.sub(r"\s+", " ", t["presentation"])
        attendus = {
            "exécutables": d["total_vecteurs"],
            "executes": d["executes_ok"],
            "sans_execution": sum(1 for v in d["par_bloc"].values() if v["statut"] != "MESURE"),
        }
        for libelle, valeur in (("exécutables", attendus["exécutables"]),
                                ("exécutés au contexte standard", attendus["executes"]),
                                ("blocs sans exécution", attendus["sans_execution"])):
            if f"{valeur}" not in plat:
                refus.append(("C17", "presentation", f"le compte « {libelle} » = {valeur} est absent"))
        if f"{attendus['executes']} exécutés au contexte standard" not in plat:
            refus.append(("C17", "presentation",
                          f"l'annonce ne porte pas « {attendus['executes']} exécutés au contexte standard »"))
    # C18 — LINTER-COUNT : le compte annoncé se recompose du SOURCE du linter
    src = pathlib.Path(__file__).read_text(encoding="utf-8")
    total_classes = len(set(re.findall(r'\("C(\d{1,2})"', src)))
    morceaux = re.findall(r"(\d{1,2}) classes", normalise(t["preuves"]))
    if not morceaux:
        refus.append(("C18", "preuves", "le compte de classes n'est pas annoncé"))
    for n in set(morceaux):
        if int(n) != total_classes:
            refus.append(("C18", "preuves", f"annonce {n} classes ≠ source {total_classes}"))

    # C19 — TITLE-WAVE : la vague du sous-titre == la vague de l'édition courante
    man = t["manuscrit"]
    mots = re.findall(r"the present edition, the ([a-z-]+) wave", man)
    table = {"fifteenth": 15, "sixteenth": 16, "seventeenth": 17, "eighteenth": 18,
             "nineteenth": 19, "twentieth": 20, "twenty-first": 21, "twenty-second": 22,
             "twenty-third": 23}
    courante = table.get(mots[-1], 0) if mots else 0
    for m in re.finditer(r"La vague (\d{1,2})\b", normalise(t["presentation"])):
        if int(m.group(1)) != courante:
            refus.append(("C19", "presentation",
                          f"titre « vague {m.group(1)} » ≠ édition vague {courante}"))

    # C20 — STATUS-RECOMPOSITION : le statut d'ancrage se dérive du journal
    import importlib.util as _iu
    sp = _iu.spec_from_file_location("sa", str(RACINE / "scripts/vague24/statut_ancrage.py"))
    sa = _iu.module_from_spec(sp); sp.loader.exec_module(sa)
    statut = sa.statut()["statut"]
    for piece in ("presentation", "preuves", "specification"):
        txt = normalise(t[piece].split("W24AUDT —")[0])   # les rapports sont lus verbatim
        if statut == "DÉPLOYÉ" and re.search(r"NON\s*DÉPLOYÉ", txt):
            refus.append(("C20", piece, "statut « NON DÉPLOYÉ » alors que le journal dit DÉPLOYÉ"))
        if statut == "EN ATTENTE" and re.search(r"ancrage[^.]{0,80}DÉPLOYÉ", txt, re.I):
            refus.append(("C20", piece, "statut « DÉPLOYÉ » alors que le journal est EN ATTENTE"))
    return refus


def rapport(refus):
    print("=" * 78)
    print("LE LINTER D'ÉDITION v3 — ONZE CLASSES (porte de génération v0.26.0)")
    print("=" * 78)
    if not refus:
        print("[linter-v260] 0 RÉSIDU — les onze classes sont vertes sur les cinq pièces")
        return 0
    for c, p, m in refus:
        print(f"[linter-v260] RÉSIDU {c} {p} — {m}")
    print(f"[linter-v260] {len(refus)} résidu(s)")
    return 2


def controle_negatif():
    pack = PACK_DEFAUT
    base = charge(pack)
    manifeste = charge_manifeste(pack)
    rec = recompte_banc()
    essais = []

    def essai(classe, mut):
        t = {k: v for k, v in base.items()}
        mut(t)
        r = verifie(t, manifeste, rec)
        essais.append((classe, any(c == classe for c, _, _ in r), r))

    # 1. libellé de version muté (VERSION-TABLE)
    essai("C6", lambda t: t.__setitem__(
        "presentation", t["presentation"].replace("Manuscrit\n\nv0.26.0", "Manuscrit\n\nv0.24.0")))
    # 2. ID hors plage
    essai("C7", lambda t: t.__setitem__("preuves", t["preuves"] + "\nla décision D299 tranche."))
    # 3. ligne de menace non qualifiée
    essai("C11", lambda t: t.__setitem__(
        "specification", t["specification"].replace("ADV-MEDIA", "ADVX-MEDIA")))
    # 4. compte de banc muté
    essai("C10", lambda t: t.__setitem__(
        "presentation", t["presentation"].replace("16/16", "15/15")))

    verts = 0
    print("=" * 78)
    print("CONTRÔLES NÉGATIFS — QUATRE MUTATIONS, QUATRE REFUS ATTENDUS")
    print("=" * 78)
    for classe, ok, r in essais:
        verts += 1 if ok else 0
        print(f"[{'VERT' if ok else 'ROUGE'}] {classe} → {[x for x in r if x[0] == classe]}")
    print(f"{verts}/4")
    return 0 if verts == 4 else 3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", default=str(PACK_DEFAUT))
    ap.add_argument("--controle-negatif", action="store_true")
    a = ap.parse_args()
    if a.controle_negatif:
        return controle_negatif()
    pack = pathlib.Path(a.pack)
    return rapport(verifie(charge(pack), charge_manifeste(pack), recompte_banc()))


if __name__ == "__main__":
    sys.exit(main())
