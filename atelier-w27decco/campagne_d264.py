#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE HARNAIS DE LA CAMPAGNE D264 — PRÊT (W27DECCO, la vague 27, prompt 4).

La campagne « ajouter » à DÉCODAGE CONTRAINT, prête à courir dès qu'un serving à
structured output est disponible. Le schéma fermé {op, dst, src, offset} (11
opcodes, additionalProperties: false) est posé AU BORD ; l'expandeur déterministe
de la vague 19 est importé À EMPREINTE CONSIGNÉE (le juge intact) ; la boucle de
réparation est bornée à TROIS tours, réinjectant le refus exact et le
contre-exemple ; la graine est consignée ; n = 18 ; les médianes se calculent
sur les 18 ET sur les seules vertes (deux conventions nommées) ; la
re-tokenisation indépendante exige un écart ≤ 1 ; l'agrégateur est FAIL-CLOSED :
un appel manquant refuse le verdict. Cible pré-enregistrée ≥ 15/18 à
≤ 3 000 tokens (CIB-ADD-STRUC), JAMAIS re-tirée.

Si le serving est absent (le bord n'applique pas le schéma) : le refus nommé
SERVING-ABSENT — aucun chiffre fabriqué.

Usage :
  python3 atelier-w27decco/campagne_d264.py --sonde        # sonde le bord
  python3 atelier-w27decco/campagne_d264.py --fixtures      # 18/18 + compteurs + rejeu
  python3 atelier-w27decco/campagne_d264.py --refus         # les quatre refus nommés éprouvés
  python3 atelier-w27decco/campagne_d264.py --courir SERVING # court (SERVING = module python)
"""
import hashlib
import importlib.util
import json
import pathlib
import statistics
import subprocess
import sys

R = pathlib.Path(__file__).resolve().parents[2] if False else pathlib.Path(__file__).resolve().parents[1]
DOSSIER = pathlib.Path(__file__).resolve().parent
GRAINE = 20261124
JUGE_FICHIER = R / "scripts/vague19/expandeur_add.py"
JUGE_SHA256_ATTENDU = "9fc325e2b8eb40e7cc5c77b92ddfa92e23e6a036bd4ec68f0ec78619903389bd"
CIBLE = {"verts": 15, "tokens": 3000}
SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["op", "offset"],
    "properties": {
        "op": {"enum": ["mov", "add", "sub", "xor", "and", "or", "cmp", "test", "jcc", "call", "ret"]},
        "dst": {"type": "object"}, "src": {"type": "object"},
        "offset": {"type": "integer", "minimum": 0, "maximum": 65535},
    },
}


class RefusNomme(Exception):
    """Les refus nommés du harnais — fail-closed, aucun n'est maquillable."""
    def __init__(self, code, motif):
        super().__init__(f"{code}: {motif}")
        self.code, self.motif = code, motif


def empreinte_juge():
    return hashlib.sha256(JUGE_FICHIER.read_bytes()).hexdigest()


def _juge():
    """L'expandeur importé À EMPREINTE CONSIGNÉE — JUGE-MODIFIÉ est refusé."""
    if empreinte_juge() != JUGE_SHA256_ATTENDU:
        raise RefusNomme("JUGE-MODIFIÉ",
                         f"sha256 {empreinte_juge()[:16]}… ≠ consigné {JUGE_SHA256_ATTENDU[:16]}…")
    spec = importlib.util.spec_from_file_location("expandeur_add", str(JUGE_FICHIER))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def valider_schema_client(reponse):
    """La contre-vérification CLIENT du schéma fermé — le bord n'est pas cru sur parole."""
    try:
        p = json.loads(reponse) if isinstance(reponse, (str, bytes)) else reponse
    except Exception:
        raise RefusNomme("SCHÉMA-VIOLÉ", "la réponse n'est pas du JSON")
    if not isinstance(p, dict):
        raise RefusNomme("SCHÉMA-VIOLÉ", "la réponse n'est pas un objet")
    if set(p) - set(SCHEMA["properties"]):
        raise RefusNomme("SCHÉMA-VIOLÉ", f"champs hors schéma : {sorted(set(p) - set(SCHEMA['properties']))}")
    if p.get("op") not in SCHEMA["properties"]["op"]["enum"]:
        raise RefusNomme("SCHÉMA-VIOLÉ", f"opcode hors du domaine fermé : {p.get('op')!r}")
    if "offset" not in p or not isinstance(p["offset"], int) or not (0 <= p["offset"] <= 0xFFFF):
        raise RefusNomme("SCHÉMA-VIOLÉ", "offset entier dans [0, 0xFFFF] attendu")
    return p


def taches():
    """Les 18 tâches (les pointeurs honnêtes du juge — la graine consignée, l'ordre jamais re-tiré)."""
    m = _juge()
    honnetes, _ = m.fixtures()
    return honnetes


def courir(serving_appel, journal_chemin=None):
    """La campagne entière contre un serving donné. L'agrégateur est FAIL-CLOSED.

    serving_appel : callable(tache, tour, refus_precedent) -> (reponse_texte, usage_tokens)
    """
    m = _juge()
    ts = taches()
    resultats, journal = [], []
    for i, tache in enumerate(ts):
        refus_precedent = None
        verdict_tache = None
        for tour in range(1, m.MAX_TOURS + 1):
            try:
                reponse, usage = serving_appel(tache, tour, refus_precedent)
            except RefusNomme:
                raise
            except Exception as e:
                raise RefusNomme("APPEL-MANQUANT", f"la tâche {i + 1}/18, tour {tour} : {e}")
            if reponse is None:
                raise RefusNomme("APPEL-MANQUANT", f"la tâche {i + 1}/18 n'a pas de réponse au tour {tour}")
            p = valider_schema_client(reponse)
            try:
                r = m.boucle_reparation(p, m.DICO)
            except Exception as e:
                raise RefusNomme("APPEL-MANQUANT", f"le juge a refusé de rendre son verdict : {e}")
            journal.append({"tache": i + 1, "tour": tour, "pointeur": p, "verdict": r["verdict"],
                            "usage": usage})
            if r["verdict"] == "VERT":
                verdict_tache = {"tache": i + 1, "verdict": "VERT", "tours": tour,
                                 "texte": r["texte"], "usage": usage}
                break
            refus_precedent = {"verdict": r["verdict"], "classes": r["classes_converties"]}
        if verdict_tache is None:
            verdict_tache = {"tache": i + 1, "verdict": "REFUS", "tours": m.MAX_TOURS,
                             "texte": None, "usage": None}
        resultats.append(verdict_tache)
    # L'AGRÉGATEUR FAIL-CLOSED : les 18 résultats doivent être là, aucun trou.
    if len(resultats) != 18 or any(r is None for r in resultats):
        raise RefusNomme("APPEL-MANQUANT", f"{len(resultats)}/18 résultats — le verdict global est refusé")
    verts = [r for r in resultats if r["verdict"] == "VERT"]
    med_18 = statistics.median([r["usage"] for r in resultats if r["usage"] is not None]) if len(resultats) == 18 and all(r["usage"] is not None for r in resultats) else None
    med_vertes = statistics.median([r["usage"] for r in verts]) if verts else None
    # La re-tokenisation indépendante : écart ≤ 1 sur chaque texte vert.
    ecarts = []
    for r in verts:
        t1 = m.compter_tokens(r["texte"])
        t2 = m.compter_tokens_independant(r["texte"])
        ecarts.append(abs(t1 - t2))
    if any(e > 1 for e in ecarts):
        raise RefusNomme("COMPTEUR-DIVERGENT", f"re-tokenisation au-delà de ±1 : {ecarts}")
    verdict = {
        "cible": f"≥ {CIBLE['verts']}/18 à ≤ {CIBLE['tokens']} tokens (pré-enregistrée, jamais re-tirée)",
        "verts": f"{len(verts)}/18", "mediane_18": med_18, "mediane_vertes": med_vertes,
        "retokenisation_ecart_max": max(ecarts) if ecarts else None,
        "graine": GRAINE, "juge": {"fichier": str(JUGE_FICHIER.relative_to(R)),
                                    "sha256": empreinte_juge()},
        "tenu": (len(verts) >= CIBLE["verts"]
                 and med_vertes is not None and med_vertes <= CIBLE["tokens"]),
        "resultats": resultats,
    }
    if journal_chemin:
        pathlib.Path(journal_chemin).write_text(
            json.dumps({"verdict": verdict, "journal": journal}, ensure_ascii=False, indent=1),
            encoding="utf-8")
    return verdict


# --- la sonde du bord -------------------------------------------------------
def sonde():
    """Le bord doit APPLIQUER le schéma : la violation ordonnée ne passe pas.

    Renvoie (applied: bool, preuve: str). La preuve est consignée telle quelle."""
    script = DOSSIER / "sonde_serving.mjs"
    r = subprocess.run(["node", str(script)], capture_output=True, text=True, timeout=300)
    sortie = r.stdout + r.stderr
    applique = "LE SCHÉMA N'EST PAS APPLIQUÉ" not in sortie
    return applique, sortie.strip()


def main():
    quoi = sys.argv[1] if len(sys.argv) > 1 else "--statut"
    if quoi == "--sonde":
        applique, preuve = sonde()
        print(preuve[:1200])
        print("\n=== VERDICT DE LA SONDE ===")
        print("SCHÉMA APPLIQUÉ AU BORD" if applique
              else "SERVING-ABSENT — le bord accepte response_format mais n'applique PAS le schéma")
        return 0
    if quoi == "--fixtures":
        m = _juge()
        honnetes, mutes = m.fixtures()
        verts = sum(1 for p in honnetes if m.boucle_reparation(p, m.DICO)["verdict"] == "VERT")
        ecarts = [abs(m.compter_tokens(m.expanse(p, m.DICO)) - m.compter_tokens_independant(m.expanse(p, m.DICO)))
                  for p in honnetes]
        print(f"fixtures : {verts}/18 vertes ; re-tokenisation écart max {max(ecarts)} (≤ 1 exigé)")
        rejeu = [m.boucle_reparation(p, m.DICO)["texte"] for p in honnetes]
        rejeu2 = [m.boucle_reparation(p, m.DICO)["texte"] for p in honnetes]
        bit_identique = rejeu == rejeu2
        print(f"rejeu bit-identique : {'OUI' if bit_identique else 'NON'}")
        return 0 if (verts == 18 and max(ecarts) <= 1 and bit_identique) else 3
    if quoi == "--refus":
        return refus_eprouves()
    if quoi == "--statut":
        print(f"juge sha256 : {empreinte_juge()}")
        print(f"cible pré-enregistrée : ≥ {CIBLE['verts']}/18 à ≤ {CIBLE['tokens']} tokens — jamais re-tirée")
        print("statut : HARNAIS PRÊT — la campagne attend un serving à structured output")
        return 0
    print(__doc__)
    return 1


def refus_eprouves():
    """Les QUATRE refus nommés, éprouvés sur un serving maquetté — jamais sur des chiffres."""
    ok = 0

    def epreuve(nom, attendu, fn):
        nonlocal ok
        try:
            fn()
            print(f"[ROUGE] {nom} — le refus {attendu} n'est pas venu")
        except RefusNomme as r:
            bon = r.code == attendu
            ok += 1 if bon else 0
            print(f"[{'VERT' if bon else 'ROUGE'}] {nom} → {r.code} : {r.motif[:90]}")

    # 1. SERVING-ABSENT — vécu à la sonde : le bord n'applique pas le schéma.
    applique, preuve = sonde()
    ok += 0 if applique else 1
    print(f"[{'VERT' if not applique else 'ROUGE'}] SERVING-ABSENT (la sonde) : "
          f"{'le bord n applique pas le schéma — la violation ordonnée passe' if not applique else 'le bord applique le schéma ?!'}")

    # 2. APPEL-MANQUANT — l'agrégateur refuse le verdict quand un appel manque.
    def appel_manquant():
        vus = []
        def serving(tache, tour, refus):
            vus.append(tache["offset"])
            if len(vus) == 18:                 # la 18e tâche : le bord se tait
                raise ConnectionError("le bord ne répond plus")
            return json.dumps(tache), 100
        courir(serving)
    epreuve("APPEL-MANQUANT (la 18e tâche sans réponse)", "APPEL-MANQUANT", appel_manquant)

    # 3. SCHÉMA-VIOLÉ — une réponse hors schéma est refusée côté client (le bord n'est pas cru).
    def schema_viole():
        def serving(tache, tour, refus):
            return json.dumps({"op": "SUBVERSION-HORS-ENUM", "offset": 999999}), 50
        courir(serving)
    epreuve("SCHÉMA-VIOLÉ (la violation ordonnée)", "SCHÉMA-VIOLÉ", schema_viole)

    # 4. JUGE-MODIFIÉ — l'empreinte du juge diverge : refus.
    def juge_modifie():
        global JUGE_SHA256_ATTENDU
        garde = JUGE_SHA256_ATTENDU
        JUGE_SHA256_ATTENDU = "0" * 64          # un registre mensonger
        try:
            courir(lambda tache, tour, refus: (json.dumps(tache), 100))
        finally:
            JUGE_SHA256_ATTENDU = garde
    epreuve("JUGE-MODIFIÉ (l'empreinte consignée diverge)", "JUGE-MODIFIÉ", juge_modifie)

    # Et le chemin vert : un serving PARFAIT (maquetté) rend les 18 verts, médianes et verdict.
    def serving_parfait(tache, tour, refus):
        return json.dumps(tache), 120
    v = courir(serving_parfait, journal_chemin=DOSSIER / "rejeu-parfait.json")
    print(f"[{'VERT' if v['verts'] == '18/18' else 'ROUGE'}] LE CHEMIN VERT (serving maquetté parfait) : "
          f"{v['verts']} verts, médiane 18 = {v['mediane_18']}, médiane vertes = {v['mediane_vertes']}, "
          f"écart re-tokenisation max = {v['retokenisation_ecart_max']}")
    v2 = courir(serving_parfait, journal_chemin=DOSSIER / "rejeu-parfait-2.json")
    bit = (pathlib.Path(DOSSIER / "rejeu-parfait.json").read_bytes()
           == pathlib.Path(DOSSIER / "rejeu-parfait-2.json").read_bytes())
    print(f"[{'VERT' if bit else 'ROUGE'}] REJEU BIT-IDENTIQUE (graine {GRAINE}, l'ordre jamais re-tiré)")
    print(f"\n{ok}/4 refus nommés éprouvés" + (" + le chemin vert" if v['verts'] == '18/18' else ""))
    return 0 if (ok == 4 and v["verts"] == "18/18" and bit) else 3


if __name__ == "__main__":
    sys.exit(main())
