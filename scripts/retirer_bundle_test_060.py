#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""retirer_bundle_test_060.py — REJOUE LE GESTE 3 de la passation D141
(passe_bundle_060.py, commit 4faaf10) : la copie erronée de
triade-history-060-07d392e.bundle au dossier /test du développeur doit être
RETIRÉE (mise à la corbeille Drive — JAMAIS supprimée, D141/D143).

CONSTAT (03/11, vérification synchro demandée par le développeur) : le geste 3
consigné au commit 4faaf10 n'avait PAS pris effet — la copie /test
(id 1beZpC6I…, créée 17:38:08Z, AVANT le dépôt miroir 17:40:19Z) est restée
non corbeillée, md5 identique à la canonique (2bb725ef…), PENDANT que les
gestes 1 (dépôt miroir) et 2 (archivage versionné de l'ancien 051) étaient
effectifs. Le rejet d'assertion de passe_bundle_060.py au rejeu (état 0 :
« l'ancien courant introuvable au miroir ») prouve que les gestes 1-2 étaient
faits et que seul le geste 3 manquait.

LA VRAIE CAUSE (5e instance du piège PATCH, tranchée par preuves API du
03/11) : l'en-tête Content-Type: application/json manquait dans la fonction
api() de passe_bundle_060.py — Drive IGNORE le corps d'un PATCH sans
Content-Type et répond 200 SANS effet. Chronologie des graphies :
  (1) corps {"trashed": true} SANS Content-Type → 200, aucun effet ;
  (2) leçon du commit 4faaf10 « trashed est un paramètre de requête » →
      graphie ?trashed=true → 200, aucun effet (paramètre inconnu ignoré) ;
  (3) diagnostic capabilities : canTrash=True partout (le droit N'EST PAS
      en cause) ;
  (4) graphie qui FONCTIONNE : PATCH corps {"trashed": True} AVEC
      Content-Type: application/json → trashed=True constaté par l'API.
Règle corrigée : trashed = champ du CORPS avec Content-Type ;
addParents/removeParents = paramètres de REQUÊTE (le geste 2 a toujours
marché ainsi) ; jamais combinés (403 du run v7, entrée 128). La leçon du
commit 4faaf10 était trop large : le corps n'est pas « interdit », il doit
être DÉCLARÉ.

Protections (les mêmes que passe_bundle_060.py) :
  - la copie /test doit être md5-identique à la copie locale AVANT retrait ;
  - la canonique doit vivre au miroir (md5 recoupé) AVANT retrait ;
  - le retrait est une MISE À LA CORBEILLE (trashed=true), pas une suppression ;
  - état final recoupé PAR L'API après le geste.

Idempotent : si la copie n'est plus dans /test, ne fait rien."""

import hashlib
import importlib.util
import json
import os
import sys
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUNDLE = "triade-history-060-07d392e.bundle"
CHEMIN_LOCAL = os.path.join(REPO, "bundles-060", BUNDLE)

_spec = importlib.util.spec_from_file_location(
    "ds", os.path.join(REPO, "scripts", "drive_sync.py"))
ds = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ds)

tok = ds.get_access_token()


def api(chemin, method="GET", json_body=None):
    headers = {"Authorization": f"Bearer {tok}"}
    data = None
    if json_body is not None:
        # LE correctif : sans Content-Type, Drive ignore le corps (200 sans
        # effet) — c'est la cause des trois échecs précédents.
        headers["Content-Type"] = "application/json"
        data = json.dumps(json_body).encode()
    req = urllib.request.Request(
        "https://www.googleapis.com/" + chemin, method=method,
        headers=headers, data=data)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return {"erreur": e.code, "corps": e.read()[:150].decode("utf-8", "replace")}


def lister(parent):
    return api("drive/v3/files?q=" + urllib.request.quote(
        f"'{parent}' in parents and trashed=false") +
        "&fields=files(id,name,md5Checksum,size)&pageSize=200").get("files", [])


# -- 0. état AVANT (assertions) ------------------------------------------------
with open(CHEMIN_LOCAL, "rb") as f:
    md5_local = hashlib.md5(f.read()).hexdigest()
print(f"[0] copie locale : {BUNDLE} md5 {md5_local[:8]}…")

coffre = lister(ds.DRIVE_ROOT_ID)
miroir = next((x for x in coffre if x["name"] == ds.PROJECT_FOLDER), None)
test = next((x for x in coffre if x["name"] == "test"), None)
assert miroir, "miroir introuvable"
assert test, "dossier /test introuvable"

canonique = next((x for x in lister(miroir["id"]) if x["name"] == BUNDLE), None)
assert canonique, f"la canonique {BUNDLE} est ABSENTE du miroir — retrait refusé"
assert canonique.get("md5Checksum") == md5_local, \
    "la canonique du miroir diverge du local — retrait refusé"
print(f"[0] canonique au miroir : md5 {canonique['md5Checksum'][:8]}… MATCH "
      f"(id {canonique['id']})")

copie = next((x for x in lister(test["id"]) if x["name"] == BUNDLE), None)
if copie is None:
    print("[3] aucune copie non corbeillée dans /test — geste DÉJÀ effectif, rien à faire")
    noms_test = sorted(x["name"] for x in lister(test["id"]))
    print(f"[état] /test : {len(noms_test)} entrées — {', '.join(noms_test)}")
    sys.exit(0)
assert copie.get("md5Checksum") == md5_local, \
    "la copie /test diverge du local — retrait refusé"
print(f"[3] copie /test trouvée : id {copie['id']}, md5 {copie['md5Checksum'][:8]}… MATCH")

# -- le geste : mise à la corbeille (corps JSON DÉCLARÉ, graphie prouvée) -------
rep = api(f"drive/v3/files/{copie['id']}", "PATCH", {"trashed": True})
assert "erreur" not in rep, f"échec du retrait : {rep}"
apres = api(f"drive/v3/files/{copie['id']}?fields=trashed,parents")
assert apres.get("trashed") is True, f"le retrait n'a pas pris effet : {apres}"
print("[3] copie /test mise à la corbeille (trashed=true constaté PAR L'API)")

# -- état APRÈS (recoupement) --------------------------------------------------
final_test = lister(test["id"])
assert not any(x["name"] == BUNDLE for x in final_test), \
    "la copie figure encore dans /test"
canonique_apres = next((x for x in lister(miroir["id"]) if x["name"] == BUNDLE), None)
assert canonique_apres and canonique_apres.get("md5Checksum") == md5_local, \
    "la canonique du miroir a bougé pendant le geste"
noms_test = sorted(x["name"] for x in final_test)
print(f"[état] /test après : {len(final_test)} entrées — {', '.join(noms_test)}")
print(f"[état] canonique miroir intacte : md5 {canonique_apres['md5Checksum'][:8]}…")
print("GESTE 3 DE LA PASSATION D141 MAINTENANT EFFECTIF")
