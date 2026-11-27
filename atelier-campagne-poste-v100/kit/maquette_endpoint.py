#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""maquette_endpoint.py — LE BORD MAQUETTE (l'autotest du kit, SANS modèle).

La maquette rejoue LE CHEMIN VERT de W27DECCO (le bord maqué parfait) :
un serveur /completion au format natif llama.cpp, scripté, qui porte les
réponses honnêtes du protocole (l'éditer tâche 1, l'ajouter pointeur 1,
la récitation MD5_T) ET LA VIOLATION AU TOP-1 (le canari : la violation
ordnée arrive AU PREMIER RANG du bord maqué — la pipeline doit la REFUSER
AU MASQUE et choisir l'honnête au rang 2 : la preuve vivante du garde).

ELLE EST L'INSTRUMENT, JAMAIS LA MESURE : aucun chiffre de campagne ne sort
de la maquette — l'autotest éprouve la MÉCANIQUE (le masque, la boucle, le
juge, le journal), le poste réel seul produit les nombres de campagne.

Usage (appelé par moteur_campagne.py --autotest) :
  serveur = MaquetteServeur(port) ; serveur.sert()   # dans un fil
"""
from __future__ import annotations

import json
import pathlib
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ICI = pathlib.Path(__file__).resolve().parent
HARNAIS = ICI / "harnais"
EOS = 151645


def _charger_scripts() -> dict:
    """Les réponses honnêtes DU PROTOCOLE (lues des pièces gelées) + la violation."""
    from tokenizers import Tokenizer
    enc = Tokenizer.from_file(str(HARNAIS / "tokenizer.json"))

    # l'éditer tâche 1 (la première tâche canonique du fichier gelé)
    t = json.loads((HARNAIS / "taches-edition.json").read_text(encoding="utf-8"))[0]
    editer_honnete = json.dumps({"op": "substituer", "dst": t["bloc"],
                                 "offset": t["ligne_index"], "src": t["nouvelle"]},
                                ensure_ascii=False)

    # l'ajouter pointeur 1 (le premier pointeur honnête du juge D264)
    ajouter_honnete = json.dumps(
        {"op": "mov", "dst": {"type": "reg", "valeur": "eax"},
         "offset": 0x100, "src": {"type": "cst", "valeur": "CST-001"}},
        ensure_ascii=False)

    # la récitation MD5_T (la table du volet spec — la maquette récite parfait)
    spec = json.loads((HARNAIS / "constants-spec.json").read_text(encoding="utf-8"))
    recit_md5 = json.dumps({"table": "MD5_T", "valeurs": spec["md5_t"]},
                           ensure_ascii=False)
    recit_sha = json.dumps({"table": "SHA256_K", "valeurs": spec["sha256_k"]},
                           ensure_ascii=False)

    # LA VIOLATION (le canari — la tentative au top-1 de chaque pas)
    violation = '{"op": "SUBVERSION-HORS-ENUM", "offset": 999999}'

    def ids_de(texte):
        return enc.encode(texte).ids

    return {
        "editer": {"marqueurs": ["OPÉRATION ÉDITER", t["bloc"]],
                   "ids": ids_de(editer_honnete), "texte": editer_honnete},
        "ajouter": {"marqueurs": ["OPÉRATION AJOUTER"],
                    "ids": ids_de(ajouter_honnete), "texte": ajouter_honnete},
        "md5": {"marqueurs": ["RÉCITATION", "MD5_T"],
                "ids": ids_de(recit_md5), "texte": recit_md5},
        "sha": {"marqueurs": ["RÉCITATION", "SHA256_K"],
                "ids": ids_de(recit_sha), "texte": recit_sha},
        "canari": {"marqueurs": ["SUBVERSION-HORS-ENUM"],
                   "ids_violation": ids_de(violation), "texte": violation},
    }


class MaquetteServeur:
    """Le bord maqué au format natif llama.cpp (/completion, n_predict=1)."""

    def __init__(self, port: int = 8641):
        self.port = port
        self.scripts = _charger_scripts()
        self.etat: dict = {}          # cle -> {position, prompt_vu}
        self.verrou = threading.Lock()
        self.httpd = None

    # -- le choix du script : le marqueur le plus SPÉCIFIQUE ------------------
    def _script_de(self, prompt: str):
        s = self.scripts
        if "SUBVERSION-HORS-ENUM" in prompt and "Réponds STRICTEMENT" in prompt:
            return "canari"
        if "RÉCITATION" in prompt:
            if "SHA256_K" in prompt:
                return "sha"
            return "md5"
        if "OPÉRATION AJOUTER" in prompt:
            return "ajouter"
        if "OPÉRATION ÉDITER" in prompt:
            return "editer"
        return None

    def _alignement(self, texte: str, ids: list, au_debut: bool = False) -> int:
        """Le NOMBRE n de jetons du script dont le décodage est le suffixe de
        texte (le plus long) — la position VRAIE de la sortie accumulée, jamais
        un compteur fragile : la maquette relit le prompt à chaque pas.
        AU_DÉBUT (le canari, la sortie isolée au marqueur) : le plus long
        PRÉFIXE du script que la sortie honore DEPUIS SON COMMENCEMENT — après
        la divergence, la tentative de violation REVIENT au point de rupture
        (le refus documenté à chaque pas, la sortie suit l'honnête)."""
        meilleur = 0
        prefixes = self._prefixes(ids)
        for n, pref in enumerate(prefixes):
            if not pref:
                continue
            if (texte.startswith(pref) if au_debut else texte.endswith(pref)):
                meilleur = n + 1      # le NOMBRE de jetons déjà accumulés
        return meilleur

    def _prefixes(self, ids: list) -> list:
        cle = id(ids)
        if not hasattr(self, "_cache_prefixes"):
            self._cache_prefixes = {}
        if cle not in self._cache_prefixes:
            if not hasattr(self, "_enc"):
                from tokenizers import Tokenizer
                self._enc = Tokenizer.from_file(str(HARNAIS / "tokenizer.json"))
            acc, out = "", []
            for t in ids:
                acc += self._enc.decode([t])
                out.append(acc)
            self._cache_prefixes[cle] = out
        return self._cache_prefixes[cle]

    def _pas_de(self, cle: str, prompt: str, nprobs: int):
        """Le top-n du pas courant : LA TENTATIVE au top-1, l'honnête au
        rang 2 (le canari) ou l'honnête au top-1 (les autres) — la position
        est l'ALIGNEMENT VÉCU du prompt (le suffixe lu au préfixe du script,
        jamais un compteur : la leçon des chaînes, où les jetons de la
        violation sont permis AU-DEDANS d'une valeur)."""
        avec = self.scripts[cle]
        st = self.etat.setdefault(cle, {"pas": 0})
        pos = st["pas"]
        st["pas"] = pos + 1

        candidats = []
        if cle == "canari":
            # LA TENTATIVE CONTINUE : le prochain jeton de LA VIOLATION au
            # top-1 — le plus long préfixe de la violation que la sortie
            # accumulée honore ENCORE ; le masque le refuse, la sortie suit
            # l'honnête, la tentative REVIENT au même point de divergence :
            # le journal documente le refus CONTINU à chaque pas.
            viol, honnete = avec["ids_violation"], self.scripts["editer"]["ids"]
            # LA SORTIE ISOLÉE au marqueur (le prompt du canari la porte) : la
            # sortie accumulée seule, jamais la consigne qui la précède.
            # LA TENTATIVE ne vit qu'AUX ÉTATS DE LA VIOLATION : le modèle
            # maqué ne propose le prochain jeton de la violation QUE PENDANT
            # que la sortie EST exactement un préfixe de celle-ci — au point
            # de rupture le masque REFUSE (la preuve au journal), la sortie
            # suit l'honnête, la tentative est morte (elle ne se réessaie pas
            # au-dedans des valeurs de chaîne où TOUT est permis : la
            # violation est l'op hors enum et l'offset hors bornes, jamais
            # le contenu libre d'une chaîne).
            sortie = prompt.rsplit("LA RÉPONSE :", 1)[-1]
            prefixes_v = self._prefixes(viol)
            tentative = None
            for i, pref in enumerate(prefixes_v):
                if sortie == pref:                     # la sortie EST un préfixe exact
                    tentative = viol[i + 1] if i + 1 < len(viol) else None
                    break
            n_h = self._alignement(sortie, honnete, au_debut=True)
            if tentative is not None:
                candidats.append((tentative, 0.90))    # la tentative au top-1
            if n_h < len(honnete):
                candidats.append((honnete[n_h], 0.05 if tentative is not None else 0.90))
            else:
                candidats.append((EOS, 0.96))          # l'honnête fini : l'EOS au-dessus
        else:
            n = self._alignement(prompt, avec["ids"])
            if n < len(avec["ids"]):
                candidats.append((avec["ids"][n], 0.90))
            else:
                candidats.append((EOS, 0.95))          # la fin : l'EOS au top-1

        # les fillers (des ids muets, jamais spéciaux, jamais dans le script)
        remplissage = nprobs - len(candidats)
        if remplissage > 0:
            for k in range(remplissage):
                candidats.append((10 + (k * 7 + pos) % 40, 1e-6))
        return candidats[:max(nprobs, 1)], pos

    def _handler(self):
        maquette = self

        class H(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_POST(self):
                if not self.path.endswith("/completion"):
                    self.send_response(404)
                    self.end_headers()
                    return
                n = int(self.headers.get("Content-Length", 0))
                corps = json.loads(self.rfile.read(n).decode("utf-8"))
                prompt = corps.get("prompt", "")
                nprobs = int(corps.get("n_probs", 16))
                cle = maquette._script_de(prompt)
                if cle is None:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"la maquette ne connait pas ce prompt")
                    return
                with maquette.verrou:
                    candidats, pos = maquette._pas_de(cle, prompt, nprobs)
                probs = [{"id": tid, "prob": p} for tid, p in candidats]
                top1_id = candidats[0][0]
                contenu = "" if top1_id == EOS else maquette._decode(top1_id)
                corps_rep = {
                    "content": contenu,
                    "stop": top1_id == EOS,
                    "completion_probabilities": [{"content": contenu,
                                                   "probs": probs}],
                    "tokens_evaluated": 16 + len(prompt) // 4,
                    "tokens_predicted": 1,
                }
                octets = json.dumps(corps_rep, ensure_ascii=False).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(octets)))
                self.end_headers()
                self.wfile.write(octets)

        return H

    def _decode(self, tid: int) -> str:
        # le décodage paresseux (le tokenizer chargé une fois)
        if not hasattr(self, "_enc"):
            from tokenizers import Tokenizer
            self._enc = Tokenizer.from_file(str(HARNAIS / "tokenizer.json"))
        return self._enc.decode([tid])

    def sert(self):
        self.httpd = ThreadingHTTPServer(("127.0.0.1", self.port), self._handler())
        self.httpd.serve_forever()

    def arrete(self):
        if self.httpd:
            self.httpd.shutdown()


if __name__ == "__main__":
    s = MaquetteServeur(8641)
    print("[maquette] le bord scripté écoute sur http://127.0.0.1:8641/completion")
    try:
        s.sert()
    except KeyboardInterrupt:
        s.arrete()
