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
    narratif = t["preuves"].split("W24AUDT —")[0].split("W25DERV —")[0].split("W23PROP —")[0]
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
            texte = texte.split("W24AUDT —")[0].split("W25DERV —")[0].split("W23PROP —")[0]
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
    for m in re.finditer(r"the (fifteenth|sixteenth|seventeenth|eighteenth|nineteenth|twentieth|twenty-first|twenty-second|twenty-third|twenty-fourth) wave", t["manuscrit"]):
        entrees.add({"fifteenth": 15, "sixteenth": 16, "seventeenth": 17, "eighteenth": 18,
                     "nineteenth": 19, "twentieth": 20, "twenty-first": 21,
                     "twenty-second": 22, "twenty-third": 23, "twenty-fourth": 24}[m.group(1)])
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
             "twenty-third": 23, "twenty-fourth": 24, "twenty-fifth": 25}
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
        txt = normalise(t[piece].split("W24AUDT —")[0].split("W25DERV —")[0].split("W23PROP —")[0])   # les rapports sont lus verbatim
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


# ==========================================================================
# C21 DOI-VERSION · C22 VERSION-PROSE-EN · C23 PROOF-STATUS · C24 RATIO-ORDER
# (la vague 25, D275) — chaque statut se recompose de son registre.
# ==========================================================================
CONCEPT_DOI = "10.5281/zenodo.24367343"


def _registres(racine):
    import json
    depots = [json.loads(l) for l in (racine / "DEPOTS.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    preuves = json.loads((racine / "PREUVES-STATUTS.json").read_text(encoding="utf-8"))
    return depots, preuves


def controles_w25(t, racine, version_edition, version_spec):
    """C21, C22, C23, C24 — les trous de couverture démontrés par l'évaluation de v0.29.0."""
    depots, preuves = _registres(racine)
    refus = []
    corps = {k: t[k] for k in ("manuscrit", "preuves", "presentation", "specification") if k in t}

    # --- C21 : tout DOI cité vient du registre, et le « courant » est le dernier publié ---
    dois = {d["doi_version"]: d for d in depots}
    dois[CONCEPT_DOI] = {"version": "concept", "statut": "concept"}
    publies = [d for d in depots if d["statut"] == "publie"]
    dernier = publies[0]
    for piece, texte in corps.items():
        for m in re.finditer(r"10\.5281/zenodo\.(\d+)", texte):
            if m.group(0) not in dois:
                refus.append(("C21", piece, f"DOI inconnu du registre : {m.group(0)}"))
        if "at this writing, version DOI" in texte:
            m = re.search(r"at this writing, version DOI\s*10\.5281/zenodo\.(\d+)", texte)
            if m and m.group(0).split()[-1] != dernier["doi_version"]:
                refus.append(("C21", piece, "DOI « courant » ≠ dernier dépôt publié"))
            if not re.search(r"v(\d+\.\d+\.\d+)", texte.split("at this writing")[0][-80:]):
                refus.append(("C21", piece, "« at this writing » sans version identifiable"))
    # la version dite « courante » doit être celle du dernier dépôt si un DOI est cité
    cur = re.search(r"archived version \(v(\d+\.\d+\.\d+) at this writing", t.get("manuscrit", ""))
    if cur and "v" + cur.group(1) != dernier["version"]:
        refus.append(("C21", "manuscrit", f"version citée v{cur.group(1)} ≠ dernier dépôt {dernier['version']}"))

    # --- C22 : la prose ANGLAISE du manuscrit, « specification vX … which this edition accompanies » ---
    for m in re.finditer(r"v(\d+\.\d+\.\d+)[^.]{0,200}?(?:this edition )?accompanies", t.get("manuscrit", ""), re.S):
        if "v" + m.group(1) != version_spec.lstrip("v") and m.group(1) != version_spec.lstrip("v"):
            refus.append(("C22", "manuscrit", f"« specification v{m.group(1)} … accompanies » ≠ {version_spec}"))

    # --- C23 : le statut de preuve publié se recompose du registre ---
    tam = preuves["tamarin"]
    _man = t.get("manuscrit", "").split("W25DERV —")[0].split("W24AUDT —")[0]
    t = dict(t)
    t["manuscrit"] = _man
    if "absent" in t.get("manuscrit", "").lower() and "Tamarin" in t.get("manuscrit", ""):
        if re.search(r"(?:Tamarin|tamarin-prover).{0,60}?(?:est|sont|is|are)\s+absent", t["manuscrit"], re.S):
            refus.append(("C23", "manuscrit", "Tamarin dit « absent » alors que le registre porte un verdict partiel"))
    if re.search(r"Tamarin.{0,160}?outils absents", t.get("presentation", ""), re.S):
        refus.append(("C23", "presentation", "statut Tamarin contradictoire avec le registre"))
    if ("1 122" not in t.get("manuscrit", "") and "1,122" not in t.get("manuscrit", "")
            and tam["verdicts"]["L3"].startswith("VERIFIED")):
        refus.append(("C23", "manuscrit", "le verdict L3 vérifié (1 122 pas / 1,122 steps) n'est pas publié"))

    # --- C24 : ordre canonique des opérandes du ratio par multiplication ---
    CANON = {63.39, 19.66}
    for piece, texte in corps.items():
        for m in re.finditer(r"\((\d{1,3},\d{2})\s*/\s*(\d{1,3},\d{2})\)", texte):
            a, b = m.group(1), m.group(2)
            va = float(a.replace(",", ".")); vb = float(b.replace(",", "."))
            avant = texte[max(0, m.start() - 60):m.start()]
            if ("«" in avant and "»" not in avant) or "remis en ordre canonique" in avant:
                continue                            # la citation d'un défaut n'est pas le défaut
            if {va, vb} == CANON and va < vb:      # seule la paire du ratio par multiplication
                refus.append(("C24", piece, f"opérandes inversés ({a}/{b}) — ordre canonique attendu"))
    return refus


# ==========================================================================
# C25 CIBLES-VERDICT (la vague 26, D276) — tout verdict de cible se recompose
# de CIBLES.md ; aucune cible re-tirée, aucun verdict maquillé.
# ==========================================================================
ANCRAGES_CIBLES = (
    ("CIB-ADD-FAISAB", "5/18", 0),
    ("CIB-ADD-COUT-4500", "4 604", 4),
    ("CIB-ADD-RATIO", "3,264", 4),
    ("CIB-HARNAIS-200", "95 exécutés", 0),
)


def controles_w26(t, racine, cibles_texte=None):
    refus = []
    texte_cibles = cibles_texte if cibles_texte is not None else \
        (racine / "CIBLES.md").read_text(encoding="utf-8")
    lignes = [l for l in texte_cibles.splitlines()
              if l.startswith("| CIB-")]
    reg = {}
    for l in lignes:
        c = [x.strip() for x in l.strip("|").split("|")]
        reg[c[0]] = c
    if len(reg) != 11:
        refus.append(("C25", "cibles", f"{len(reg)} cibles au registre, 11 attendues"))
    preuves = re.sub(r"\s+", " ", t.get("preuves", ""))
    if "REGISTRE DES CIBLES" not in preuves.upper():
        refus.append(("C25", "preuves", "le registre des cibles n'est pas publié"))
    # chaque ligne du registre est publiée UNE fois, avec sa mesure ET son verdict, tels quels
    for cid, c in reg.items():
        mes, verdict = c[4], c[5]
        n = preuves.count(cid)
        if n < 1:
            refus.append(("C25", "preuves", f"{cid} n'est pas publiée"))
            continue
        deb = preuves.index(cid)
        ln = preuves[deb:deb + 190]
        if mes and mes not in ("—", "-") and mes.split(" ")[0] not in ln:
            refus.append(("C25", "preuves", f"{cid} : mesure « {mes} » absente de sa ligne"))
        mot = verdict.split(" ")[0]
        if mot not in ln:
            refus.append(("C25", "preuves", f"{cid} : verdict « {mot} » absent de sa ligne"))
        elif mot.startswith("MANQU") and re.search(r"\bTENUE\b", preuves[deb:deb + 120]):
            refus.append(("C25", "preuves", f"{cid} : verdict retourné — « manquée » et « tenue » dans la même ligne"))
    # le couloir entrelacé n'est jamais dit « manqué » contre 1,05 ×
    if re.search(r"1,26[^.]{0,80}(manqu|missed)", preuves):
        refus.append(("C25", "preuves", "le couloir entrelacé est dit « manqué » contre 1,05 × — il est hors sujet"))

    # --- la vague 27 : la colonne périmètre est VISIBLE sur chaque ligne publiée ------------
    for cid, c in reg.items():
        perimetre = c[2]
        if perimetre in ("—", "-"):
            continue
        deb = preuves.index(cid) if cid in preuves else -1
        ln = preuves[deb:deb + 480] if deb >= 0 else ""   # la ligne publiée, entière
        if re.sub(r"\s+", " ", perimetre) not in re.sub(r"\s+", " ", ln):
            refus.append(("C25", "preuves", f"{cid} : le périmètre n'est pas publié sur sa ligne"))

    # --- la vague 27 : un verdict TENUE cite la mesure du périmètre COURANT ou l'étiquette --
    ERES_BUDGETS = {"CIB-LOC-BUDGET": "localiser", "CIB-EDIT-BUDGET": "éditer"}
    adoptes = {}
    for l in texte_cibles.splitlines():
        if l.startswith("| localiser |") or l.startswith("| éditer |") or l.startswith("| ajouter |"):
            c = [x.strip() for x in l.strip("|").split("|")]
            m = re.search(r"(\d[\d ]*)\s*\(", c[4])      # la colonne ADOPTÉ : « 627 (hiérarchique…) »
            if m:
                adoptes[c[0]] = int(m.group(1).replace(" ", ""))
    for cid, op in ERES_BUDGETS.items():
        if cid not in reg or op not in adoptes:
            continue
        c = reg[cid]
        mes, verdict = c[4], c[5]
        m = re.match(r"(\d[\d ]*)", mes)
        if not m or not verdict.startswith("TENUE"):
            continue
        mesure = int(m.group(1).replace(" ", ""))
        if mesure != adoptes[op] and "HISTORIQUE-DATÉ" not in mes and "HISTORIQUE-DATÉ" not in verdict:
            refus.append(("C25", "cibles",
                          f"{cid} : verdict TENUE sur la mesure {mesure} d'une autre ère sans étiquette HISTORIQUE-DATÉ"))
        if mesure != adoptes[op]:
            deb = preuves.index(cid) if cid in preuves else -1
            ln = preuves[deb:deb + 320] if deb >= 0 else ""
            if "HISTORIQUE-DATÉ" not in ln:
                refus.append(("C25", "preuves",
                              f"{cid} : la ligne publiée porte un verdict TENUE sur une mesure d'une autre ère sans étiquette"))
    return refus


# ==========================================================================
# C26 STATUS-INTERPIECES (la vague 27, W27RECON) — tout statut sémantique
# PARTAGÉ (ancrage, compteur NV, Tamarin/ProVerif, sentinelle Windows,
# fence.i) se recompose des REGISTRES et aucune des CINQ pièces ne peut le
# contredire. Le trou de C20 est nommé : il couvrait trois pièces, le Livre
# divergent (D267, « le déploiement n'est pas fait ») lui échappait.
# ==========================================================================
def _statuts_partages(racine, override=None):
    """Les cinq statuts partagés, recomposés de leurs registres — jamais tapés."""
    if override is not None:
        return override
    import importlib.util as _iu
    sp = _iu.spec_from_file_location("sa", str(racine / "scripts/vague24/statut_ancrage.py"))
    sa = _iu.module_from_spec(sp); sp.loader.exec_module(sa)
    reg = json.loads((racine / "PREUVES-STATUTS.json").read_text(encoding="utf-8"))
    return {
        "ancrage": sa.statut(strict=False)["statut"],
        "nv": reg["nv"]["statut"],
        "tamarin": reg["tamarin"]["statut"],
        "proverif": reg["proverif"]["statut"],
        "sentinelle_windows": reg["sentinelle_windows"]["statut"],
        "fence_i": reg["fence_i"]["statut"],
    }


def _cite_defaut(avant):
    """La citation d'un défaut n'est pas le défaut (la garde de C24, partagée)."""
    return ("«" in avant and "»" not in avant) or "traversait" in avant or "disait" in avant


def controles_w27(t, racine, override=None):
    """C26 — refuse toute pièce qui contredit un statut partagé dérivé des registres."""
    statuts = _statuts_partages(racine, override)
    refus = []
    corps = {k: re.sub(r"\s+", " ", normalise(v)).replace("\u2019", "'") for k, v in t.items()
             if k in ("manuscrit", "specification", "livre", "preuves", "presentation")}

    def cherche(piece, texte, motif, msg):
        for m in re.finditer(motif, texte):
            avant = texte[max(0, m.start() - 90):m.start()]
            apres = texte[m.end():m.end() + 70]
            if _cite_defaut(avant) or any(k in (avant + m.group(0)) for k in
                                           ("still said", "disait", "portait", "traversait")):
                continue        # la citation d'un défaut n'est pas le défaut (l'histoire datée non plus)
            if re.search(r"\(D\d{2,3}\)", apres):
                continue        # une référence de décision DATE l'énoncé : l'histoire, pas l'état courant
            if "poste réel" in avant and "configuré" in m.group(0):
                continue        # la liste des restants n'est pas un déploiement
            refus.append(("C26", piece, msg))
            return

    # --- 1. ANCRAGE (D267) : dérivé du journal append-only -------------------
    if statuts["ancrage"] == "DÉPLOYÉ":
        for piece, txt in corps.items():
            for motif in (r"déploiement n'est pas fait", r"NON\s*DÉPLOYÉ",
                          r"aucun témoin ancré n'existe", r"porte de release le dit EN ATTENTE"):
                cherche(piece, txt, motif,
                        f"statut d'ancrage contredit le journal (DÉPLOYÉ) : « {motif} »")
    else:
        for piece, txt in corps.items():
            for motif in (r"l'ancrage de transparence est[^.]{0,60}?DÉPLOYÉ",
                          r"le déploiement est APPLIQUÉ", r"déploiement est DÉPLOYÉ"):
                cherche(piece, txt, motif,
                        f"statut d'ancrage contredit le journal (EN ATTENTE) : « {motif} »")

    # --- 2. COMPTEUR NV : le registre dit le run matériel --------------------
    if "EN ATTENTE" in statuts["nv"]:
        for piece, txt in corps.items():
            for motif in (r"run matériel (?:est )?VERT", r"NV matériel (?:a été )?(?:mesuré|vérifié|exécuté)",
                          r"compteur NV (?:matériel )?(?:a été )?mesuré"):
                cherche(piece, txt, motif, f"statut NV contredit le registre ({statuts['nv']}) : « {motif} »")
    else:
        for piece, txt in corps.items():
            cherche(piece, txt, r"run matériel (?:est )?EN ATTENTE",
                    "statut NV contredit le registre (mesuré) : « run matériel EN ATTENTE »")

    # --- 3. TAMARIN/PROVERIF : les verdicts du registre ----------------------
    if "incomplets" in statuts["tamarin"] or "INCOMPLETE" in statuts["tamarin"]:
        for piece, txt in corps.items():
            for motif in (r"(?:Tamarin|tamarin-prover)[^.]{0,80}?(?:est |sont |is |are )?absents?\b",
                          r"L1/L2 (?:sont )?vérifiés", r"les trois lemmes (?:sont )?vérifiés"):
                cherche(piece, txt, motif,
                        f"statut Tamarin contredit le registre ({statuts['tamarin']}) : « {motif} »")
    else:
        for piece, txt in corps.items():
            for motif in (r"L1/L2 incomplets", r"INCOMPLETE au mur", r"L1/L2 INCOMPLETE"):
                cherche(piece, txt, motif,
                        f"statut Tamarin contredit le registre ({statuts['tamarin']}) : « {motif} »")
    if "non exécuté" in statuts["proverif"] or "NON exécuté" in statuts["proverif"]:
        for piece, txt in corps.items():
            cherche(piece, txt, r"ProVerif[^.]{0,80}?(?<!non )(?<!not )exécut\w+|ProVerif[^.]{0,80}?(?<!not )executed",
                    f"statut ProVerif contredit le registre ({statuts['proverif']})")
    else:
        for piece, txt in corps.items():
            cherche(piece, txt, r"ProVerif[^.]{0,80}?(?:non exécuté|not executed)",
                    f"statut ProVerif contredit le registre ({statuts['proverif']})")

    # --- 4. SENTINELLLE WINDOWS : au poste réel tant que le registre le dit ---
    if "poste réel" in statuts["sentinelle_windows"]:
        for piece, txt in corps.items():
            for motif in (r"sentinelle Windows[^.]{0,60}?(?:est )?(?:déployée|active|en production|en place)",
                          r"moteur SACL[^.]{0,40}?(?:est )?(?:déployé|actif|configuré)\b"):
                cherche(piece, txt, motif,
                        f"statut sentinelle contredit le registre : « {motif} »")
    else:
        for piece, txt in corps.items():
            cherche(piece, txt, r"sentinelle Windows[^.]{0,60}?(?:au poste réel|restant)",
                    "statut sentinelle contredit le registre (déployée) : « au poste réel »")

    # --- 5. FENCE.I : non prouvé sur silicium tant que le registre le dit ----
    if "non prouvé" in statuts["fence_i"]:
        for piece, txt in corps.items():
            for motif in (r"fence\.i[^.]{0,80}?(?<!NON )(?<!non )prouv(?:ée?|en) sur silicium",
                          r"fence\.i[^.]{0,80}?(?<!not )proven on (?:physical )?silicon"):
                cherche(piece, txt, motif,
                        f"statut fence.i contredit le registre : « {motif} »")
    else:
        for piece, txt in corps.items():
            for motif in (r"fence\.i[^.]{0,80}?NON prouv", r"fence\.i[^.]{0,80}?non prouv",
                          r"fence\.i[^.]{0,80}?remain unexecuted"):
                cherche(piece, txt, motif,
                        f"statut fence.i contredit le registre (prouvé) : « {motif} »")
    return refus


# ==========================================================================
# C27 COUNT-TABLECELL · C28 TITLE-UNIQUE · C29 LANG-BODY (la vague 27, W27RESID)
# — tout compte d'arbres/vecteurs se confronte au registre (le sceau-I pour
# les arbres, CIBLES.md pour les vecteurs) ; aucun titre dupliqué par pièce ;
# la langue du corps par pièce (le manuscrit anglais, les quatre françaises).
# ==========================================================================
MOTS_ARBRES = {"dix": 10, "onze": 11, "douze": 12, "treize": 13, "quatorze": 14, "quinze": 15}
DATEURS_ARBRES = re.compile(
    r"D\d{2,3}\b|\bM\d{1,2}\b|v0\.\d+\.\d+|spec_v\d+|passation|jusque-là|l'ère|d'ère|d'époque"
    r"|\d{1,2}[–-]\d{1,2}/1?0|\d{1,2}/1[0-2]|04/11|05/11|cérémonie terrain|livré \(laboratoire\)")


def _nb_arbres_sceau(racine):
    """Le compte d'arbres se DÉRIVE du sceau-I (jamais tapé)."""
    src = (racine / "v06" / "sceau_I.py").read_text(encoding="utf-8")
    m = re.search(r"ARBRES\s*=\s*\{(.*?)\n\}", src, re.S)
    return len(re.findall(r'^\s{4}"', m.group(1), re.M)) if m else 0


def _nb_vecteurs_cibles(racine):
    """Les comptes de vecteurs se dérivent du registre des cibles (CIB-HARNAIS-200)."""
    for l in (racine / "CIBLES.md").read_text(encoding="utf-8").splitlines():
        if l.startswith("| CIB-HARNAIS-200"):
            c = [x.strip() for x in l.strip("|").split("|")]
            m = re.search(r"(\d+) exécutables sur (\d+) produits", c[2])
            if m:
                return int(m.group(1)), int(m.group(2))
    return 0, 0


def _titres_pieces(racine):
    """Les titres de section/sous-section des trois pièces SOURCES (la chaîne courante)."""
    def dernier(glob):
        c = [p for p in racine.glob(glob) if re.search(r"v\d+$", p.name)]
        return max(c, key=lambda p: int(re.search(r"v(\d+)$", p.name).group(1))) if c else None

    def extraire(fichiers):
        out = []
        for f in fichiers:
            src = f.read_text(encoding="utf-8")
            out += [t.strip() for t in re.findall(r"\\(?:sub)?section\*?\{([^}]+)\}", src)]
        return out

    spec, liv = dernier("scripts/spec_v*"), dernier("scripts/livre_v*")
    return {
        "specification": extraire([*sorted(spec.glob("*.tex"))]) if spec else [],
        "livre": extraire([*sorted(liv.glob("*.tex"))]) if liv else [],
        "manuscrit": extraire([racine / "edition-v0230" / "main.tex"]),
    }


EN_SEQ = re.compile(
    r"\b(?:the|and|with|that|which|from|this|these|was|were|are|not|but|has|have|been)\b"
    r"(?:\s+[a-zà-ÿ'-]{2,15}){0,2}\s+"
    r"\b(?:the|and|with|that|which|from|this|these|was|were|are|not|but|has|have|been)\b"
    r"(?:\s+[a-zà-ÿ'-]{2,15}){0,2}\s+"
    r"\b(?:the|and|with|that|which|from|this|these|was|were|are|but|has|have|been)\b", re.I)


def controles_w27b(t, racine, titres_override=None):
    refus = []
    corps = {k: re.sub(r"\s+", " ", normalise(v)).replace("\u2019", "'") for k, v in t.items()
             if k in ("manuscrit", "specification", "livre", "preuves", "presentation")}
    nb_arbres = _nb_arbres_sceau(racine)
    nb_exec, nb_prod = _nb_vecteurs_cibles(racine)

    # --- C27 : tout compte d'arbres/vecteurs confronté au registre ------------
    for piece, txt in corps.items():
        def fen(m):
            return txt[max(0, m.start() - 200):m.end() + 200]
        for m in re.finditer(r"verifier\s*:?\s*(\d{1,2}) arbres", txt):
            # l'INVOCATION DU GARDE est toujours l'état courant : aucun dateur ne l'excuse
            if int(m.group(1)) != nb_arbres:
                refus.append(("C27", piece, f"« verifier {m.group(1)} arbres » ≠ le sceau ({nb_arbres} arbres)"))
        for m in re.finditer(r"\b(" + "|".join(MOTS_ARBRES) + r")\s+arbres?\b", txt, re.I):
            if DATEURS_ARBRES.search(fen(m)):
                continue
            if MOTS_ARBRES[m.group(1).lower()] != nb_arbres:
                refus.append(("C27", piece, f"« {m.group(0)} » ≠ le sceau ({nb_arbres} arbres)"))
        for m in re.finditer(r"\b(\d{1,2})\s+arbres\b", txt):
            if DATEURS_ARBRES.search(fen(m)):
                continue
            if int(m.group(1)) != nb_arbres:
                refus.append(("C27", piece, f"« {m.group(0)} » ≠ le sceau ({nb_arbres} arbres)"))
        for m in re.finditer(r"\b(\d{2,3})\s+produits\b", txt):
            if int(m.group(1)) != nb_prod:
                refus.append(("C27", piece, f"« {m.group(0)} » ≠ le registre ({nb_prod} produits)"))
        for m in re.finditer(r"\b(\d{2,3})\s+exécutables\b", txt):
            if int(m.group(1)) != nb_exec:
                refus.append(("C27", piece, f"« {m.group(0)} » ≠ le registre ({nb_exec} exécutables)"))

    # --- C28 : aucun titre dupliqué par pièce ----------------------------------
    titres = titres_override if titres_override is not None else _titres_pieces(racine)
    for piece, ts in titres.items():
        for titre in sorted({x for x in ts if ts.count(x) > 1}):
            refus.append(("C28", piece, f"titre dupliqué : « {titre} »"))

    # --- C29 : la langue du corps par pièce -------------------------------------
    man = corps.get("manuscrit", "")
    # les régions françaises SANCTIONNÉES du manuscrit : la ligne Mots-clés, le résumé
    man = re.sub(r"Mots-clés.*?L'étude est N ?= ?1 ?\.", " ", man)
    man = re.sub(r"«[^»]*»", "«»", man)          # les citations verbatim (refus nommés) demeurent
    man = re.sub(r"\[[A-Z0-9][A-Z0-9À-ÿ-]*\]", "[]", man)   # les refus nommés [T0-PÉRIMÉ]… demeurent
    NOMS_PROPRES = {"Entrée", "Entrées", "relevé", "éditer"}   # les noms du métier, cités tels quels
    for m in re.finditer(r"\b[\wÀ-ÿ]*[àâäéèêëîïôöùûüçÀÂÄÉÈÊËÎÏÔÖÙÛÜ][\wÀ-ÿ]*\b", man):
        if m.group(0) in NOMS_PROPRES:
            continue
        refus.append(("C29", "manuscrit", f"mot français dans le corps anglais : « {m.group(0)} »"))
        break
    for m in re.finditer(r"\b\d[\d ]* pas\b", man):
        refus.append(("C29", "manuscrit", f"compte français « {m.group(0)} » (steps attendu)"))
        break
    for piece in ("specification", "livre", "preuves", "presentation"):
        txt = re.sub(r"«[^»]*»", "«»", corps.get(piece, ""))
        txt = re.sub(r"\([A-Za-z][^()]{0,80}\)", "()", txt)   # les parenthèses anglaises des citations
        if EN_SEQ.search(txt):
            m = EN_SEQ.search(txt)
            refus.append(("C29", piece, f"séquence anglaise dans le corps français : « …{txt[m.start():m.end()][:70]}… »"))
    return refus
