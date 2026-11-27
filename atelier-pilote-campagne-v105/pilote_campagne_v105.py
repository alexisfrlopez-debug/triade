#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE LABO — LE PILOTE DE CAMPAGNE v105 (le patron google-colab-cli porté à
la campagne) : provisionner le runtime Colab depuis la sandbox, porter le
notebook VIVANTE au bord, exécuter ses HUIT cellules de code d'un trait
(les sorties diffusées au journal du pilote, TELLES QUELLES), rapatrier le
zip de preuves + le rapport du poste, désassigner le runtime — le geste
unique du maître réduit à SON strict minimum : le consentement OAuth au
scope colaboratory (UNE fois, copier-coller ; le jeton de rafraîchissement
vit ensuite au labo et n'expire pas).

LA VOIE (l'architecture de google-colab/google-colab-cli, lue à la source) :
  · l'assignation — GET puis POST https://colab.research.google.com/tun/m/assign
    (nbh = hash du notebook, variant=GPU, accelerator=T4) → le proxy du
    runtime + son jeton (colab_cli.client.Client, importé TEL QUEL) ;
  · l'exécution — le canal kernel Jupyter (/api/kernels, websocket /channels)
    par colab_cli.runtime.ColabRuntime, importé TEL QUEL ;
  · les fichiers — l'API Jupyter Contents (PUT base64 / GET content) au
    proxy du runtime, avec le paramètre d'auth du bord ;
  · la fermeture — le kernel tué, le runtime désassigné (unassign), même
    si le run a échoué (la hygiene d'abord).

LE BORD MUET DU PILOTE : la garde symétrique du BORD-MUET du kit — si le
bord ne rend plus un message depuis <minutes muettes>, le pilote NOMME son
refus (PILOTE-MUET) et ferme le poste — jamais un run orphelin.

Usage :
  pilote_campagne_v105.py consentement            → imprime l'URL du geste unique
  pilote_campagne_v105.py jeton <code>            → frappe le jeton colab (UNE fois)
  pilote_campagne_v105.py run [--cpu] [--muets-min N]   → LA CAMPAGNE 105
  pilote_campagne_v105.py bac                     → le bac local (mécanique prouvée
                                                      contre un serveur Jupyter
                                                      local — AUCUN Colab touché)
"""
import base64
import datetime as dt
import hashlib
import json
import pathlib
import sys
import time
import urllib.parse
import urllib.request
import uuid

LABO = pathlib.Path("/home/z/my-project")
WORK = LABO / "work"
JETON_COLAB = WORK / "jeton_colab.json"          # le coffre du labo (jamais au dépôt)
NOTEBOOK_VIVANT = WORK / "Campagne-Colab-v105-VIVANTE.ipynb"
DOS_RUN = WORK / "v105-run"
JOURNAL = DOS_RUN / "journal-pilote.jsonl"

# les pièces du patron google-colab-cli, importées TEL QUELLES
from colab_cli.client import (                      # noqa: E402
    Accelerator, Client, Prod, TooManyAssignmentsError, Variant, uuid_to_web_safe_base64)
from colab_cli.runtime import ColabRuntime          # noqa: E402

SCOPES_COLAB = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/colaboratory",
    "https://www.googleapis.com/auth/drive.file",
]
REDIRECT_COLLE = "https://sdk.cloud.google.com/applicationdefaultauthcode.html"


# ─────────────────────────── le journal à l'horloge ───────────────────────────
def horloge():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def journal(evenement, **champs):
    """Chaque geste du pilote vit au journal — TEL QUEL, jamais habillé."""
    DOS_RUN.mkdir(parents=True, exist_ok=True)
    ligne = {"horodatage": horloge(), "evenement": evenement, **champs}
    with open(JOURNAL, "a", encoding="utf-8") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    print(f"[pilote {horloge()[11:]}] {evenement}"
          + (f" — {' · '.join(str(v) for v in champs.values())}" if champs else ""))


def sha256f(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for m in iter(lambda: f.read(1 << 20), b""):
            h.update(m)
    return h.hexdigest()


# ────────────────────── le geste unique : le consentement ─────────────────────
def _flux_colab(code_verifier: str):
    """Le flux du client OAuth PUBLIC du cloud-SDK (livré avec google-colab-cli),
    au vérificateur PKCE FIXE — le même au consentement et à l'échange (sinon
    le code est rejeté : la voie du copy-paste distant)."""
    from importlib import resources
    from google_auth_oauthlib.flow import InstalledAppFlow
    config = json.loads(resources.files("colab_cli").joinpath("oauth_config.json").read_text())
    flow = InstalledAppFlow.from_client_config(config, SCOPES_COLAB,
                                               code_verifier=code_verifier,
                                               autogenerate_code_verifier=False)
    flow.redirect_uri = REDIRECT_COLLE
    return flow


def cmd_consentement():
    """L'URL du consentement — LE GESTE UNIQUE du maître (le client OAuth
    PUBLIC du cloud-SDK, livré avec google-colab-cli ; le code s'affiche sur
    la page d'atterrissage de Google, à coller au labo)."""
    import secrets
    DOS_RUN.mkdir(parents=True, exist_ok=True)
    (DOS_RUN / "code-verifier.txt").write_text(secrets.token_urlsafe(64), encoding="utf-8")
    print()
    print("LE GESTE UNIQUE DU MAÎTRE — le consentement OAuth au scope colaboratory.")
    print("Ouvre cette URL dans TON navigateur (le compte qui porte le coffre Drive) :")
    print()
    flow = _flux_colab((DOS_RUN / "code-verifier.txt").read_text())
    url, _ = flow.authorization_url(prompt="consent", access_type="offline", token_usage="remote")
    print(url)
    print()
    print("Approuve. Google affiche alors UN CODE D'AUTORISATION sur la page.")
    print("Colle-moi ce code dans le chat — je le frappe en jeton, et les campagnes")
    print("courent seules depuis la sandbox (le jeton de rafraîchissement n'expire pas).")


def cmd_jeton(code: str):
    """Le code collé devient le jeton du labo (le refresh_token sauvé, AUCUN
    secret imprimé). Le vérificateur PKCE RECHARGÉ — celui du consentement."""
    chemin_v = DOS_RUN / "code-verifier.txt"
    if not chemin_v.exists():
        raise SystemExit("VÉRIFICATEUR-ABSENT : reprends « consentement » d'abord "
                         "(le vérificateur PKCE y vit au disque du labo).")
    flow = _flux_colab(chemin_v.read_text())
    flow.fetch_token(code=code)
    creds = flow.credentials
    if not creds.refresh_token:
        raise SystemExit("JETON-SANS-RAFRAÎCHISSEMENT : Google n'a pas rendu de refresh_token "
                         "(révoque l'application dans ton compte Google puis reprends "
                         "« consentement » — le prompt=consent force la redemande).")
    WORK.mkdir(parents=True, exist_ok=True)
    JETON_COLAB.write_text(json.dumps({
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "scopes": SCOPES_COLAB,
    }, indent=2), encoding="utf-8")
    journal("jeton-colab-frappé")
    print("[pilote] le jeton colab vit au labo (work/jeton_colab.json) — "
          "la voie est ouverte : run.")


# ───────────────────────── le jeton du labo, vivant ──────────────────────────
def charge_jeton_colab():
    if not JETON_COLAB.exists():
        raise SystemExit("JETON-COLAB-ABSENT : aucun work/jeton_colab.json — cours "
                         "« consentement » puis « jeton <code> » (le geste unique du "
                         "maître, UNE fois pour toutes).")
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    creds = Credentials.from_authorized_user_info(json.loads(JETON_COLAB.read_text()), SCOPES_COLAB)
    if not creds.valid:
        creds.refresh(Request())
    return creds


def session_autorisee(creds):
    from google.auth.transport.requests import AuthorizedSession
    return AuthorizedSession(creds)


# ─────────────────── l'assignation du runtime (le patron vécu) ───────────────
def demande_runtime(creds, gpu: bool, nbh: uuid.UUID):
    """GET puis POST /tun/m/assign — le runtime T4 (ou CPU) + son proxy."""
    client = Client(Prod(), session_autorisee(creds))
    variant = Variant.GPU if gpu else Variant.DEFAULT
    accel = Accelerator.T4 if gpu else Accelerator.NONE
    try:
        res = client.assign(nbh, variant=variant, accelerator=accel)
    except TooManyAssignmentsError:
        raise SystemExit("REFUS-412 : le backend Colab refuse l'assignation (trop de "
                         "sessions actives ou quota temporaire) — attends ou ferme une "
                         "session, puis reprends le run.")
    token = res.runtime_proxy_info.token
    url = res.runtime_proxy_info.url
    journal("runtime-assigné", endpoint=res.endpoint, url=url[:48] + "…",
            expire_dans_s=res.runtime_proxy_info.token_expires_in_seconds,
            materiel=("T4" if gpu else "CPU"), nbh=str(nbh))
    return client, res


def rafraichi_jeton_proxy(client, nbh: uuid.UUID, gpu: bool):
    """Le jeton du proxy expire — le ré-assignement au MÊME nbh rend le MÊME
    runtime avec un jeton NEUF (la voie de google-colab-cli, _get_assignment
    réconciliateur)."""
    variant = Variant.GPU if gpu else Variant.DEFAULT
    accel = Accelerator.T4 if gpu else Accelerator.NONE
    res = client.assign(nbh, variant=variant, accelerator=accel)
    journal("jeton-proxy-rafraîchi",
            expire_dans_s=res.runtime_proxy_info.token_expires_in_seconds)
    return res.runtime_proxy_info.url, res.runtime_proxy_info.token


# ─────────────── l'API Contents (le patron, le paramètre du bord) ────────────
class PorteFichiers:
    """L'API Jupyter Contents au proxy du runtime — le paramètre d'auth porte
    le nom du bord : colab-runtime-proxy-token au vrai Colab, token au bac."""

    def __init__(self, url_proxy, token, nom_param="colab-runtime-proxy-token"):
        self.base = url_proxy.rstrip("/")
        self.token = token
        self.nom_param = nom_param

    def _params(self, encore=None):
        p = {self.nom_param: self.token, "authuser": "0"}
        if encore:
            p.update(encore)
        return p

    def depot(self, chemin_distant: str, octets: bytes):
        """PUT base64 — le notebook porté au bord."""
        charge = {
            "name": chemin_distant.split("/")[-1],
            "path": chemin_distant,
            "type": "file",
            "format": "base64",
            "content": base64.b64encode(octets).decode("ascii"),
            "chunk": 1,
        }
        url = (f"{self.base}/api/contents/{urllib.parse.quote(chemin_distant.strip('/'), safe='/')}"
               f"?{urllib.parse.urlencode(self._params())}")
        req = urllib.request.Request(url, data=json.dumps(charge).encode("utf-8"),
                                     method="PUT",
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            json.loads(r.read().decode())
        return True

    def lit(self, chemin_distant: str) -> bytes:
        url = (f"{self.base}/api/contents/{urllib.parse.quote(chemin_distant.strip('/'), safe='/')}"
               f"?{urllib.parse.urlencode(self._params({'content': '1'}))}")
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=300) as r:
            d = json.loads(r.read().decode())
        if d.get("format") == "base64":
            return base64.b64decode(d["content"])
        return str(d.get("content", "")).encode("utf-8")

    def liste(self, dossier: str):
        url = (f"{self.base}/api/contents/{urllib.parse.quote(dossier.strip('/'), safe='/')}"
               f"?{urllib.parse.urlencode(self._params())}")
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode())


# ────────────────── l'exécution des cellules (la pièce vivante) ───────────────
def execute_le_notebook(url_proxy, token, notebook: pathlib.Path, muets_min: float,
                        callback_sortie=None):
    """Les HUIT cellules de code du notebook VIVANT, d'un trait, dans l'ordre —
    les sorties diffusées au journal TELLES QUELLES. La garde : PILOTE-MUET si
    le bord se tait plus de <muets_min> minutes (symétrie du BORD-MUET du kit)."""
    nb = json.loads(notebook.read_text(encoding="utf-8"))
    cellules = [(i, "".join(c["source"])) for i, c in enumerate(nb["cells"])
                if c["cell_type"] == "code"]
    journal("notebook-ouvert", notebook=notebook.name, sha256=sha256f(notebook),
            cellules_code=len(cellules))
    runtime = ColabRuntime(url_proxy, token)
    try:
        kc = runtime.kernel_client
        journal("kernel-vivant", kernel_id=runtime.kernel_id)
        for i, source in cellules:
            journal("cellule-début", cellule=i, caracteres=len(source))
            t0 = time.monotonic()
            def flux(msg, _i=i):
                t = msg.get("output_type")
                if t == "stream":
                    texte = "".join(msg.get("text", []))
                    if texte.strip():
                        journal("cellule-sortie", cellule=_i, sortie=texte[-3000:])
                        if callback_sortie:
                            callback_sortie(_i, texte)
                elif t in ("error",):
                    journal("cellule-erreur", cellule=_i,
                            nom=msg.get("ename"), valeur=msg.get("evalue"))
                elif t == "execute_result":
                    texte = str(msg.get("data", {}).get("text/plain", ""))[:3000]
                    if texte.strip():
                        journal("cellule-résultat", cellule=_i, sortie=texte)
            sorties = runtime.execute_code(source, output_hook=flux, timeout=muets_min * 60)
            erreurs = [o for o in sorties if o.get("output_type") == "error"]
            journal("cellule-fin", cellule=i, duree_s=round(time.monotonic() - t0, 1),
                    erreurs=len(erreurs))
            if erreurs:
                for e in erreurs:
                    print(f"[pilote] CELLULE {i} ROUGE : {e.get('ename')} : "
                          f"{str(e.get('evalue'))[:400]}")
                raise SystemExit(f"CELLULE-{i}-ROUGE : le notebook a refusé à la cellule "
                                 f"{i} — le journal du pilote porte la trace TELLE QUELLE.")
    finally:
        try:
            runtime.stop(shutdown_kernel=True)
            journal("kernel-tu")
        except Exception as e:
            journal("kernel-tu-manqué", erreur=e.__class__.__name__)


# ─────────────────────── le run complet (le geste du labo) ───────────────────
def cmd_run(gpu: bool, muets_min: float, notebook: pathlib.Path = NOTEBOOK_VIVANT,
            bac=None):
    DOS_RUN.mkdir(parents=True, exist_ok=True)
    journal("run-début", notebook=notebook.name, materiel=("T4" if gpu else "CPU"),
            bac=bool(bac))
    nbh = uuid.uuid4()
    if bac:  # ── LE BAC : le même chemin de code, un faux bord local ──
        url_proxy, token, client = bac["demarre"]()
        try:
            porte = PorteFichiers(url_proxy, token, nom_param="token")
            porte.depot(notebook.name, notebook.read_bytes())
            journal("bac-notebook-porté", notebook=notebook.name,
                    sha256=sha256f(notebook))
            execute_le_notebook(url_proxy, token, notebook, muets_min)
            pieces = bac["rapatrie"](porte)
            journal("run-fin", bac=True, pieces=[p.name for p in pieces])
            return pieces
        finally:
            bac["ferme"]()
    # ── LE VRAI BORD ──
    creds = charge_jeton_colab()
    client, res = demande_runtime(creds, gpu, nbh)
    url_proxy, token = res.runtime_proxy_info.url, res.runtime_proxy_info.token
    try:
        porte = PorteFichiers(url_proxy, token)
        # le notebook porté au bord — la pièce d'évidence du run (lue au labo,
        # la même empreinte que la copie vivante)
        porte.depot("/content/" + notebook.name, notebook.read_bytes())
        journal("notebook-porté", chemin="/content/" + notebook.name,
                sha256=sha256f(notebook))
        t_run = time.monotonic()
        execute_le_notebook(url_proxy, token, notebook, muets_min)
        duree_min = (time.monotonic() - t_run) / 60
        # le jeton du proxy peut avoir vieilli — le ré-assignement au même nbh
        if duree_min > 30:
            url_proxy, token = rafraichi_jeton_proxy(client, nbh, gpu)
            porte = PorteFichiers(url_proxy, token)
        pieces = rapatrie_les_preuves(porte)
        journal("run-fin", duree_min=round(duree_min, 1), pieces=[p.name for p in pieces])
        return pieces
    finally:
        try:
            client.unassign(res.endpoint)
            journal("runtime-désassigné", endpoint=res.endpoint)
        except Exception as e:
            journal("runtime-désassigné-manqué", erreur=e.__class__.__name__)


def rapatrie_les_preuves(porte: PorteFichiers):
    """Le zip de preuves + le rapport du poste, tirés du bord, recoupés au
    sha256 DEUX fois (la pièce relue — la voie du relais du labo)."""
    DOS_RUN.mkdir(parents=True, exist_ok=True)
    pieces = []
    try:
        kit = porte.liste("/content/kit")
        noms_zip = [f["name"] for f in kit.get("content", []) if f["type"] == "file"
                    and f["name"].startswith("preuves-campagne-")]
    except Exception as e:
        raise SystemExit(f"KIT-ILLISIBLE : la liste du /content/kit a manqué "
                         f"({e.__class__.__name__}) — le journal porte la trace.")
    if not noms_zip:
        raise SystemExit("ZIP-ABSENT : aucun preuves-campagne-*.zip au /content/kit — "
                         "la cellule 6 (LA BATTERIE) n'a pas rendu son zip ; le journal "
                         "du pilote porte les sorties TELLES QUELLES.")
    nom_zip = sorted(noms_zip)[-1]
    blob = porte.lit(f"/content/kit/{nom_zip}")
    relu = porte.lit(f"/content/kit/{nom_zip}")
    if hashlib.sha256(blob).hexdigest() != hashlib.sha256(relu).hexdigest():
        raise SystemExit("RECOP-ROUGE : le zip relu du bord diverge — reprends le run.")
    dest_zip = DOS_RUN / nom_zip
    dest_zip.write_bytes(blob)
    pieces.append(dest_zip)
    journal("pièce-rapatriée", piece=nom_zip, octets=len(blob),
            sha256=hashlib.sha256(blob).hexdigest()[:16] + "…")
    rapport = porte.lit("/content/rapport-poste.txt")
    nom_rapport = f"rapport-poste-v105-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}.txt"
    dest_rapport = DOS_RUN / nom_rapport
    dest_rapport.write_bytes(rapport)
    pieces.append(dest_rapport)
    journal("pièce-rapatriée", piece=nom_rapport, octets=len(rapport))
    return pieces


# ───────────────────────────── le bac local ──────────────────────────────────
def cmd_bac(muets_min: float = 2.0):
    """LE BAC : la mécanique du pilote contre un serveur Jupyter LOCAL —
    l'assignation contournée (le faux bord), l'exécution, le dépôt, le
    rapatriement et la fermeture RÉELS. AUCUN Colab touché, AUCUN /test du
    Drive touché — les preuves du bac vivent au labo seul."""
    import subprocess
    dos_bac = LABO / "work" / "bac-pilote"
    racine = dos_bac / "racine"
    racine.mkdir(parents=True, exist_ok=True)
    # le mini-notebook du bac : trois cellules, les mêmes conventions de
    # pièces (preuves-campagne-*.zip au « kit », rapport-poste.txt à la racine)
    mini = {
        "nbformat": 4, "nbformat_minor": 5, "metadata": {"kernelspec": {"name": "python3"}},
        "cells": [
            {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
             "source": ["import pathlib, time\n",
                        "d = pathlib.Path('kit'); d.mkdir(exist_ok=True)\n",
                        "print('[bac] la cellule 1 vit —', time.strftime('%H:%M:%S'))\n"]},
            {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
             "source": ["contenu = 'BAC-v105 - la mecanique du pilote prouvee\\n'.encode('utf-8')\n",
                        "(d / 'preuves-campagne-BAC.zip').write_bytes(contenu)\n",
                        "print('[bac] la piece de preuves nee -', len(contenu), 'octets')\n"]},
            {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
             "source": ["pathlib.Path('rapport-poste.txt').write_text('BAC v105 — ok\\n')\n",
                        "print('[bac] le rapport du poste ne')\n"]},
        ],
    }
    chemin_mini = dos_bac / "mini-notebook-bac.ipynb"
    chemin_mini.write_text(json.dumps(mini), encoding="utf-8")

    secret = uuid.uuid4().hex
    port = 8899
    proc = subprocess.Popen(
        [sys.executable, "-m", "jupyter_server", "--ServerApp.port=" + str(port),
         "--ServerApp.root_dir=" + str(racine),
         "--IdentityProvider.token=" + secret,
         "--ServerApp.open_browser=False", "--ServerApp.log_level=ERROR"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=str(racine))
    url = f"http://127.0.0.1:{port}"
    sain = False
    for _ in range(60):
        time.sleep(1)
        try:
            req = urllib.request.Request(url + "/api/status",
                                         headers={"Authorization": f"Bearer {secret}"})
            with urllib.request.urlopen(req, timeout=5) as r:
                sain = json.loads(r.read().decode()).get("started") is not None
                break
        except Exception:
            if proc.poll() is not None:
                break
    if not sain:
        proc.kill()
        raise SystemExit("BAC-MORT : le serveur Jupyter local n'a pas rendu /api/status — "
                         "le bac ne peut pas courir (voir jupyter_server installé).")

    def demarre():
        journal("bac-serveur-vivant", url=url)
        return url, secret, None

    def rapatrie(porte: PorteFichiers):
        kit = porte.liste("kit")
        noms_zip = [f["name"] for f in kit.get("content", []) if f["name"].startswith("preuves-campagne-")]
        blob = porte.lit("kit/" + noms_zip[-1])
        relu = porte.lit("kit/" + noms_zip[-1])
        if hashlib.sha256(blob).hexdigest() != hashlib.sha256(relu).hexdigest():
            raise SystemExit("RECOP-ROUGE au bac : la pièce relue diverge.")
        dest = dos_bac / noms_zip[-1]
        dest.write_bytes(blob)
        rapport = porte.lit("rapport-poste.txt")
        (dos_bac / "rapport-poste.txt").write_bytes(rapport)
        journal("bac-pièces", zip=noms_zip[-1], rapport="rapport-poste.txt")
        return [dest, dos_bac / "rapport-poste.txt"]

    def ferme():
        proc.terminate()
        try:
            proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            proc.kill()
        journal("bac-serveur-fermé")

    try:
        return cmd_run(gpu=False, muets_min=muets_min, notebook=chemin_mini,
                       bac={"demarre": demarre, "rapatrie": rapatrie, "ferme": ferme})
    finally:
        if proc.poll() is None:
            proc.terminate()


# ─────────────────────────────── la loi du pilote ────────────────────────────
def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    cmd = args[0]
    if cmd == "consentement":
        cmd_consentement()
    elif cmd == "jeton":
        if len(args) < 2:
            raise SystemExit("jeton <code> : le code d'autorisation collé par le maître.")
        cmd_jeton(args[1].strip())
    elif cmd == "bac":
        pieces = cmd_bac()
        print("\n[bac] LA MÉCANIQUE DU PILOTE EST PROUVÉE — pièces :")
        for p in pieces:
            print("   ", p)
    elif cmd == "run":
        gpu = "--cpu" not in args
        muets = 30.0
        if "--muets-min" in args:
            muets = float(args[args.index("--muets-min") + 1])
        pieces = cmd_run(gpu=gpu, muets_min=muets)
        print("\n[pilote] LA CAMPAGNE 105 EST CLOSE — pièces au labo :")
        for p in pieces:
            print("   ", p)
    else:
        raise SystemExit(f"commande inconnue : {cmd} (consentement | jeton | run | bac)")


if __name__ == "__main__":
    main()
