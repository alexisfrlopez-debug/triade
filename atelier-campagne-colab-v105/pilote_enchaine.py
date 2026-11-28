#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE PILOTE ENCHAÎNÉ — la campagne 105 conduit en chaîne d'appels bornés.

LA LOI DU TERRAIN (mesurée au bac, 28/11) : AUCUN processus du bac ne survit
à la frontière des appels (nohup, setsid, disown — tous tués) ; ET le runtime
Colab ne survit PAS à un pilote mort (l'endpoint change, le /content est vide
— le kernel ne poursuit PAS seul). LE REDRESSAMENT : le notebook est exécuté
PAR LE RUNTIME LUI-MÊME (jupyter nbconvert --execute, détaché au bord — la
loi 0 clic INTACTE : le MÊME notebook, le MÊME ordre, AUCUNE cellule touchée)
et chaque appel du bac ne fait que RENEUVELER LE BAIL (la re-assignation au
MÊME nbh — le GET réconciliateur du patron) et OBSERVER (l'API Contents en
lecture seule). Quand la pièce vit au /test (la cellule 7 du notebook monte
SEULE par le relais embarqué), le bail est rompu proprement (unassign).

Usage (un appel à la fois, ≤ 9 min de travail chacune) :
  pilote_enchaine.py pas [nbh]     → fait ce qu'il faut selon l'état
  pilote_enchaine.py ferme [nbh]   → unassign sans condition
  pilote_enchaine.py pas|ferme --notebook <chemin> --etat <chemin>
État : work/v105-run/etat-enchaine.json (le disque du bac — la vérité)."""
import importlib.util
import json
import pathlib
import sys
import time

LABO = pathlib.Path("/home/z/my-project")
PILOTE = str(LABO / "depot" / "atelier-pilote-campagne-v105" / "pilote_campagne_v105.py")

# le paramétrage (le v1052 par défaut ; --notebook/--etat pour la campagne
# d'entraînement v106 — le MÊME conducteur, l'autre notebook)
NOTEBOOK = LABO / "work" / "Campagne-Colab-v1052-VIVANTE.ipynb"   # le terrain.9 amendé
ETAT = LABO / "work" / "v105-run" / "etat-enchaine.json"
JOURNAL = LABO / "work" / "v105-run" / "journal-enchaine.jsonl"
_args = sys.argv[1:]
if "--notebook" in _args:
    NOTEBOOK = pathlib.Path(_args[_args.index("--notebook") + 1])
if "--etat" in _args:
    ETAT = pathlib.Path(_args[_args.index("--etat") + 1])
    JOURNAL = ETAT.parent / "journal-enchaine.jsonl"
MARQUEUR_PIÈCE = "preuves-campagne-2026112"     # la 105 par défaut
if "--piece" in _args:
    MARQUEUR_PIÈCE = _args[_args.index("--piece") + 1]

spec = importlib.util.spec_from_file_location("pilote", PILOTE)
pilote = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pilote)


def journal(evenement, **champs):
    ETAT.parent.mkdir(parents=True, exist_ok=True)
    ligne = {"horodatage": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
             "evenement": evenement, **champs}
    with open(JOURNAL, "a", encoding="utf-8") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    print(f"[enchaîné {ligne['horodatage'][11:]}] {evenement}"
          + (f" — {' · '.join(str(v) for v in champs.values())}" if champs else ""))


def lit_etat():
    if ETAT.exists():
        return json.loads(ETAT.read_text(encoding="utf-8"))
    return {"phase": "neuf", "nbh": None}


def ecrit_etat(etat):
    ETAT.parent.mkdir(parents=True, exist_ok=True)
    ETAT.write_text(json.dumps(etat, ensure_ascii=False, indent=1), encoding="utf-8")


def assigne_ou_renouvelle(nbh_txt):
    import uuid
    creds = pilote.charge_jeton_colab()
    client = pilote.Client(pilote.Prod(), pilote.session_autorisee(creds))
    res = client.assign(uuid.UUID(nbh_txt), variant=pilote.Variant.GPU,
                        accelerator=pilote.Accelerator.T4)
    return client, res


LAUNCHER = r'''
import subprocess, time, pathlib
p = pathlib.Path("/content/nbconvert.log")
if p.exists():
    print("[lanceur] un nbconvert vit déjà ? — le journal :", p.read_text()[:200])
proc = subprocess.Popen(
    ["nohup", "jupyter", "nbconvert", "--to", "notebook", "--execute",
     "/content/NOM_DU_NOTEBOOK",
     "--output", "/content/Campagne-executee.ipynb",
     "--ExecutePreprocessor.timeout=14400",
     "--ExecutePreprocessor.kernel_name=python3"],
    cwd="/content", stdout=open("/content/nbconvert.log", "w"),
    stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
    start_new_session=True)
time.sleep(6)
ret = proc.poll()
print(f"[lanceur] nbconvert lancé (pid {proc.pid}) — poll après 6 s : {ret}")
'''


def lance_le_notebook(url_proxy, token, nom_notebook):
    """LE GESTE : le runtime exécute le notebook LUI-MÊME — un process détaché
    au bord (start_new_session — le kernel peut mourir, le process vit)."""
    from colab_cli.runtime import ColabRuntime
    runtime = ColabRuntime(url_proxy, token)
    try:
        source = LAUNCHER.replace("NOM_DU_NOTEBOOK", nom_notebook)
        sorties = runtime.execute_code(source, timeout=60)
        for o in sorties:
            if o.get("output_type") == "stream":
                print("".join(o.get("text", []))[:600])
            elif o.get("output_type") == "error":
                raise SystemExit(f"LANCEMENT-ROUGE : {o.get('ename')}: "
                                 f"{str(o.get('evalue'))[:300]}")
    finally:
        try:
            runtime.stop(shutdown_kernel=True)
        except Exception:
            pass


def observe(porte):
    """L'œil du labo : les pièces du bord LUES (aucune écriture)."""
    vues = {}
    for piece in ("/content/nbconvert.log", "/content/horloge-batterie.txt",
                  "/content/rapport-poste.txt", "/content/registre-entrainement-v106.json"):
        try:
            vues[piece] = porte.lit(piece).decode("utf-8", errors="replace")
        except Exception:
            vues[piece] = None
    if vues.get("/content/registre-entrainement-v106.json"):
        reg = vues["/content/registre-entrainement-v106.json"]
        print("=== le registre d'entraînement (la fin) ===")
        print(reg[-700:])
    log = vues["/content/nbconvert.log"]
    if log:
        print("=== nbconvert.log (la fin, TEL QUELLE) ===")
        print(log[-1800:])
    try:
        racine = porte.liste("/content")
        noms_racine = [f["name"] for f in racine.get("content", [])]
        print(f"=== le /content : {noms_racine}")
    except Exception as e:
        print(f"=== le /content illisible : {e.__class__.__name__}")
    horloge = vues["/content/horloge-batterie.txt"]
    if horloge and horloge.strip():
        print("=== l'horloge de la batterie ===")
        print(horloge[-800:])
    # la marche du moteur : les journaux qui croissent au /content/kit
    try:
        kit2 = porte.liste("/content/kit")
        for f in kit2.get("content", []):
            if f["name"] in ("journal-campagne.jsonl", "journal-pas.jsonl",
                              "registre-campagne.json", "garde-brut.jsonl"):
                print(f"    moteur : {f['name']} — {f.get('size', '?')} o")
    except Exception:
        pass
    try:
        kit = porte.liste("/content/kit")
        noms = [f["name"] for f in kit.get("content", []) if f["type"] == "file"]
        zips = [n for n in noms if n.startswith("preuves-campagne-")]
        print(f"=== le /content/kit : {len(noms)} fichiers — zips : {zips}")
    except Exception as e:
        print(f"=== le /content/kit illisible : {e.__class__.__name__}")
    return vues


def piece_au_test():
    sys.path.insert(0, str(LABO / "scripts"))
    from lister_test import pieces_recentes
    return [p["name"] for p in pieces_recentes(heures=3)
            if p["name"].startswith(MARQUEUR_PIÈCE)]


def cmd_pas():
    etat = lit_etat()
    # 1 · la pièce est-elle déjà au /test ? (le notebook a clos SEUL)
    pieces = piece_au_test()
    if pieces:
        journal("pièce-au-test", pièces=pieces[:3])
        if etat.get("phase") == "cours" and etat.get("nbh"):
            try:
                client, res = assigne_ou_renouvelle(etat["nbh"])
                client.unassign(res.endpoint)
                journal("bail-rompu", endpoint=res.endpoint)
            except Exception as e:
                journal("bail-rompu-manqué", erreur=e.__class__.__name__)
        ecrit_etat({"phase": "close", "nbh": etat.get("nbh"), "pièces": pieces})
        print("\n[enchaîné] LA CAMPAGNE EST CLOSE — la pièce vit au /test :", pieces[:3])
        return 0
    if etat.get("phase") == "close":
        print("[enchaîné] déjà close (l'état le dit, la pièce au /test y vivra).")
        return 0

    # 2 · le bail : assigner (neuf) ou renouveler (cours) au MÊME nbh
    nbh_txt = etat.get("nbh")
    if not nbh_txt:
        import uuid
        nbh_txt = str(uuid.uuid4())
    client, res = assigne_ou_renouvelle(nbh_txt)
    journal("bail", endpoint=res.endpoint, phase=etat.get("phase"),
            jeton_s=res.runtime_proxy_info.token_expires_in_seconds)
    porte = pilote.PorteFichiers(res.runtime_proxy_info.url, res.runtime_proxy_info.token)

    # 3 · la phase : neuf → porter le notebook + LANCER ; cours → observer
    if etat.get("phase") != "cours":
        porte.depot("/content/" + NOTEBOOK.name, NOTEBOOK.read_bytes())
        import hashlib
        journal("notebook-porté", sha256=hashlib.sha256(NOTEBOOK.read_bytes()).hexdigest()[:16] + "…")
        lance_le_notebook(res.runtime_proxy_info.url, res.runtime_proxy_info.token, NOTEBOOK.name)
        ecrit_etat({"phase": "cours", "nbh": nbh_txt, "endpoint": res.endpoint,
                    "lancé": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
        journal("notebook-lancé-au-bord")
        observe(porte)
    else:
        vues = observe(porte)
        # LE RUNTIME RECYCLÉ (le terrain de 10:04 : l'endpoint change, le
        # /content est vide) — le journal du lanceur ABSENT = la pièce est
        # neuve : la campagne REPART (l'écart nommé, jamais subi en silence)
        if vues.get("/content/nbconvert.log") is None:
            journal("runtime-recyclé", ancien_endpoint=etat.get("endpoint"),
                    nouvel_endpoint=res.endpoint)
            porte.depot("/content/" + NOTEBOOK.name, NOTEBOOK.read_bytes())
            lance_le_notebook(res.runtime_proxy_info.url, res.runtime_proxy_info.token,
                              NOTEBOOK.name)
            ecrit_etat({"phase": "cours", "nbh": nbh_txt, "endpoint": res.endpoint,
                        "lancé": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "relances": etat.get("relances", 0) + 1})
            journal("notebook-re-lancé-au-bord")
    print("\n[enchaîné] le bail est renouvelé — le prochain pas observe ; la pièce"
          "\n[enchaîné] attendue au /test (la cellule 7 du notebook y monte seule).")
    return 1


def cmd_ferme():
    etat = lit_etat()
    if not etat.get("nbh"):
        print("[enchaîné] rien à fermer.")
        return 0
    client, res = assigne_ou_renouvelle(etat["nbh"])
    client.unassign(res.endpoint)
    journal("bail-rompu", endpoint=res.endpoint, motif="fermeture manuelle")
    ecrit_etat({"phase": "fermé", "nbh": etat["nbh"]})
    print("[enchaîné] le bail est rompu (unassign).")
    return 0


if __name__ == "__main__":
    verbe = sys.argv[1] if len(sys.argv) > 1 else "pas"
    if verbe == "pas":
        raise SystemExit(cmd_pas())
    if verbe == "ferme":
        raise SystemExit(cmd_ferme())
    raise SystemExit(__doc__)
