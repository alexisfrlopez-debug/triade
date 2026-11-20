#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""roundtrip_cache.py — LE CACHE DE ROUND-TRIP (ahult8jgd §2) : le module
réutilisable qui épargne la re-vérification des blocs INTACTS à l'ouverture.

LA CLÉ (la lettre du plan) : sha256(notation || version du moteur d'assemblage
|| configuration du profil) — TOUT écart de clé = re-vérification complète
(fail-closed) ; le hit retourne le verdict caché SANS ré-exécution.

LE FAIL-CLOSED (la discipline, jamais l'optimisme) :
  — le cache illisible, corrompu ou absent est traité comme VIDE (tout
    re-vérifié — jamais un silicium de confiance sur un JSON tordu) ;
  — un verdict caché qui manque d'un champ, ou dont le verdict n'est pas
    « VERT », est un hit REFUSÉ (re-vérification) ;
  — SEULS les verdicts VERTS sont cachés : un REFUS n'est JAMAIS caché
    (l'échec se re-constate à chaque ouverture, il ne se souvient pas) ;
  — la version du VÉRIFICATEUR vit dans la configuration du profil : le
    contrat des contrôles fait partie de l'identité du verdict.

LE CONTRÔLE NÉGATIF : la notation mutée d'UN octet DOIT invalider la clé
(ATTRAPÉ au premier nom) — le hit refusé, la re-vérification complète
exécutée ; la mutation du compteur « Code : N o » en-tête attrape le REFUS
de la re-vérification (la faute constatée, pas souvenir).

LA MESURE : le temps d'ouverture de l'échantillon tls13 (les 28 notations du
dépôt) avant (tout re-vérifié) / après (le mémo chaud) — n=10, la médiane,
la même machine. NOTE NOMMÉE : l'ouverture ici est le ROUND-TRIP R5
(keystone == capstone == keystone, le geste de round_trip_unite01.py) ; les
ouvertures UNICORN des oracles (les ~10-23 s du bras T) vivent au mémo v2 de
la pile v182 (adopté, cq01qv1za) — le cache R5 est ORTHOGONAL et compose
avec lui ; l'extension du verdict caché aux sessions Unicorn est le territoire
du mémo, nommée, non dupliquée.

Sortie : registres/roundtrip-cache.json · rapport-roundtrip-cache.txt"""
from __future__ import annotations

import hashlib
import json
import pathlib
import statistics
import sys
import time

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-porteuse-ahult8jgd"
REG = ICI / "registres"

# La version du contrat de vérification (la liste des contrôles qui fondent le
# verdict — un changement de contrat = une clé différente = tout re-vérifié).
CONTRAT_R5 = "r5-v1"

# Les champs exigés d'un verdict caché valide (le hit refusé s'il en manque).
CHAMPS_VERDICT = ("verdict", "bloc", "octets", "instructions", "sha256_octets",
                  "verificateur")


def moteur_versions() -> str:
    """La version du moteur d'assemblage (keystone ET capstone : le round-trip
    les emploie TOUS LES DEUX — les deux gravent la clé)."""
    import capstone
    import keystone
    try:
        csv = ".".join(str(x) for x in capstone.cs_version())
    except Exception:
        csv = "?"
    return (f"keystone={getattr(keystone, '__version__', '?')};"
            f"capstone={getattr(capstone, '__version__', '?')}({csv})")


class CacheRoundTrip:
    """Le cache réutilisable : un vérificateur INJECTABLE (le module ne connaît
    pas le domaine), une clé par la formule du plan, fail-closed partout."""

    def __init__(self, chemin_memo: pathlib.Path, verificateur,
                 moteur: str | None = None, contrat: str = CONTRAT_R5):
        self.chemin = pathlib.Path(chemin_memo)
        self.verificateur = verificateur      # (chemin, profil) -> dict|REFUS
        self.moteur = moteur or moteur_versions()
        self.contrat = contrat
        self.compteurs = {"hit": 0, "miss": 0, "refus": 0}
        self._memo = self._charger()

    # ---- la clé (la lettre du plan) ----------------------------------------
    @staticmethod
    def cle(notation: bytes, moteur: str, profil: str) -> str:
        h = hashlib.sha256()
        h.update(len(notation).to_bytes(8, "little"))
        h.update(notation)
        h.update(len(moteur).to_bytes(8, "little"))
        h.update(moteur.encode("utf-8"))
        h.update(len(profil).to_bytes(8, "little"))
        h.update(profil.encode("utf-8"))
        return h.hexdigest()

    def profil_config(self, domaine: str, rva: int, slot: int) -> str:
        return (f"{self.contrat};{domaine};x86-64-win11-pe;msx64;"
                f"rva={rva:#x};slot={slot:#x}")

    # ---- le mémo (fail-closed sur tout silicium tordu) ----------------------
    def _charger(self) -> dict:
        try:
            brut = json.loads(self.chemin.read_text(encoding="utf-8"))
            if isinstance(brut, dict) and all(
                    isinstance(v, dict) for v in brut.values()):
                return brut
        except Exception:
            pass
        return {}

    def _ecrire(self) -> None:
        tmp = self.chemin.with_suffix(".tmp")
        tmp.write_text(json.dumps(self._memo, ensure_ascii=False, indent=1),
                       encoding="utf-8")
        tmp.replace(self.chemin)

    # ---- le verdict ----------------------------------------------------------
    def verifier(self, chemin, domaine: str, rva: int, slot: int) -> dict:
        """L'ouverture d'UN bloc : le hit retourne le verdict caché SANS
        ré-exécution ; TOUT écart de clé (ou de forme) = la re-vérification
        complète. Le verdict porte son origine (hit/miss)."""
        notation = pathlib.Path(chemin).read_bytes()
        profil = self.profil_config(domaine, rva, slot)
        cle = self.cle(notation, self.moteur, profil)
        entree = self._memo.get(cle)
        if entree is not None and all(k in entree for k in CHAMPS_VERDICT) \
                and entree["verdict"] == "VERT" \
                and entree["verificateur"] == self.contrat:
            self.compteurs["hit"] += 1
            return {**entree, "origine": "hit", "cle": cle}
        # le miss : la re-vérification COMPLÈTE (fail-closed — jamais cru)
        self.compteurs["miss"] += 1
        verdict = self.verificateur(pathlib.Path(chemin), profil)
        if verdict.get("verdict") == "VERT":
            self._memo[cle] = {k: verdict[k] for k in CHAMPS_VERDICT}
            self._ecrire()
        else:
            self.compteurs["refus"] += 1
        return {**verdict, "origine": "miss", "cle": cle}


# ---- le vérificateur R5 (le lecteur canonique B4 du dépôt) ------------------
def fabrique_verificateur_r5():
    """Le round-trip R5 PAR LE CODE DU DÉPÔT (build_m4.assembler_bloc +
    round_trip — les mêmes fonctions que round_trip_unite01.py, la référence) :
    l'assemblage, les tailles déclarées, le slot, le padding, l'égalité
    keystone == capstone == keystone."""
    sys.path.insert(0, str(REPO / "m4"))
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "b4_rc", REPO / "m4" / "build_m4.py")
    B4 = importlib.util.module_from_spec(spec)
    sys.modules["b4_rc"] = B4
    spec.loader.exec_module(B4)
    import capstone
    import keystone
    KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
    CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

    def verificateur(chemin: pathlib.Path, profil: str) -> dict:
        bloc = chemin.stem
        try:
            rva = int(profil.split("rva=")[1].split(";")[0], 16)
            slot = int(profil.split("slot=")[1].split(";")[0], 16)
            octets, metas = B4.assembler_bloc(KS, str(chemin), rva, slot)
            insns = B4.round_trip(CS, KS, str(chemin), rva, octets, metas)
            return {"verdict": "VERT", "bloc": bloc, "octets": len(octets),
                    "instructions": len(insns),
                    "sha256_octets": hashlib.sha256(octets).hexdigest(),
                    "verificateur": CONTRAT_R5}
        except Exception as e:
            return {"verdict": "REFUS", "bloc": bloc,
                    "cause": f"{type(e).__name__}: {e}"[:400],
                    "verificateur": CONTRAT_R5}

    return verificateur


def echantillon_tls13():
    """Les 28 notations tls13 du dépôt avec leurs slots (layout.py — le plan
    d'adressage ARRÊTÉ)."""
    sys.path.insert(0, str(REPO / "tls13"))
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "lay_rc", REPO / "tls13" / "layout.py")
    lay = importlib.util.module_from_spec(spec)
    sys.modules["lay_rc"] = lay
    spec.loader.exec_module(lay)
    note = REPO / "tls13" / "notation"
    echant = []
    # (la liste réelle par glob — les noms portent leur libellé complet)
    for f in sorted(note.glob("tls13-*.asm")):
        num = int(f.name.split("-")[1])
        sid = f"h1000{num:02d}"
        rva, slot = lay.SLOTS_TLS13[sid]
        echant.append((f, "tls13", rva, slot))
    return echant


def ouverture(cache: CacheRoundTrip, echant, actif: bool) -> tuple[float, int]:
    """UNE ouverture : la vérification de l'échantillon entier — sans cache
    (actif=False : un cache VIDE à chaque ouverture, tout re-vérifié) ou avec
    (actif=True : le mémo chaud, les hits). Retour (secondes, hits)."""
    if not actif:
        cache._memo = {}
    t0 = time.monotonic()
    hits = 0
    for chemin, domaine, rva, slot in echant:
        v = cache.verifier(chemin, domaine, rva, slot)
        if v["origine"] == "hit":
            hits += 1
        elif v["verdict"] != "VERT":
            return -1.0, -1   # fail-closed : une ouverture qui refuse ÉCHOUE
    return time.monotonic() - t0, hits


def main() -> int:
    echant = echantillon_tls13()
    memo = REG / "roundtrip-cache-memo.json"
    verif = fabrique_verificateur_r5()

    rapport = ["LE CACHE DE ROUND-TRIP (ahult8jgd §2) — la clé "
               "sha256(notation || moteur || profil), le hit sans "
               "ré-exécution, TOUT écart = re-vérification complète",
               "",
               f"LA CLÉ DU JOUR : moteur « {moteur_versions()} », contrat "
               f"« {CONTRAT_R5} », l'échantillon tls13 : {len(echant)} "
               "notations (le dépôt, les slots de layout.py)",
               ""]

    # ---- la semence (le mémo posé une fois) ---------------------------------
    if memo.exists():
        memo.unlink()
    cache = CacheRoundTrip(memo, verif)
    t_semis, hits = ouverture(cache, echant, actif=True)
    assert hits == 0 and len(cache._memo) == len(echant), "la semis"
    rapport += [f"LA SEMENCE : {t_semis:.3f} s — {len(echant)} verdicts "
                "cachés (aucun hit, tout vérifié) ; sha256 du mémo "
                f"{hashlib.sha256(memo.read_bytes()).hexdigest()[:16]}…",
                ""]

    # ---- l'ouverture AVANT / APRÈS (n=10, la médiane, cette machine) --------
    avant = []
    for _ in range(10):
        cache.compteurs = {"hit": 0, "miss": 0, "refus": 0}
        dt, hits = ouverture(cache, echant, actif=False)
        if dt < 0:
            print("ROUGE : l'ouverture sans cache a refusé")
            return 2
        avant.append(dt)
    apres = []
    for _ in range(10):
        cache.compteurs = {"hit": 0, "miss": 0, "refus": 0}
        dt, hits = ouverture(cache, echant, actif=True)
        if dt < 0 or hits != len(echant):
            print(f"ROUGE : l'ouverture chaude hits={hits}/{len(echant)}")
            return 2
        apres.append(dt)
    med_avant = statistics.median(avant)
    med_apres = statistics.median(apres)
    rapport += [
        "LE TEMPS D'OUVERTURE (n=10, la médiane [min–max], cette machine) :",
        f"  AVANT (tout re-vérifié, le régime d'aujourd'hui) : "
        f"{med_avant*1000:.1f} ms [{min(avant)*1000:.1f}–"
        f"{max(avant)*1000:.1f}]",
        f"  APRÈS (le mémo chaud, {len(echant)}/{len(echant)} hits) : "
        f"{med_apres*1000:.1f} ms [{min(apres)*1000:.1f}–"
        f"{max(apres)*1000:.1f}]",
        f"  LE GAIN : {med_avant/max(med_apres,1e-9):.1f}× "
        f"(−{(1 - med_apres/med_avant)*100:.1f} %) — le hit rend le verdict "
        "SANS ré-exécution (keystone/capstone jamais invoqués)",
        ""]

    # ---- LE CONTRÔLE NÉGATIF : la notation mutée d'UN octet -----------------
    import shutil
    import tempfile
    laboratoire = pathlib.Path(tempfile.mkdtemp(prefix="rc-neg-"))
    negatif = {}
    for etiquette, mutation in [
            ("cle-invalidee", lambda t: t.replace("ptr [rcx + 0x10]",
                                                  "ptr [rcx + 0x11]")),
            ("compte-taille", lambda t: t.replace("; Code : 129 o",
                                                  "; Code : 128 o"))]:
        source = REPO / "tls13" / "notation" / "tls13-16-aes128-bloc.asm"
        cible = laboratoire / source.name
        texte = source.read_text(encoding="utf-8")
        mute = mutation(texte)
        assert mute != texte, f"la mutation {etiquette} n'a pas mordu"
        delta = sum(1 for a, b in zip(texte.encode(), mute.encode())
                    if a != b) + abs(len(texte) - len(mute))
        cible.write_text(mute, encoding="utf-8")
        # la clé du mutant DOIT différer de celle du scellé
        _, domaine, rva, slot = echant[int([e[0].name for e in echant].index(
            source.name))]
        cle_intacte = CacheRoundTrip.cle(
            source.read_bytes(), cache.moteur,
            cache.profil_config(domaine, rva, slot))
        cle_mutee = CacheRoundTrip.cle(
            cible.read_bytes(), cache.moteur,
            cache.profil_config(domaine, rva, slot))
        cache.compteurs = {"hit": 0, "miss": 0, "refus": 0}
        v = cache.verifier(cible, domaine, rva, slot)
        negatif[etiquette] = {
            "octets_mutes": delta,
            "cle_intacte": cle_intacte[:16],
            "cle_mutee": cle_mutee[:16],
            "cle_differente": cle_intacte != cle_mutee,
            "hit_refuse": v["origine"] == "miss",
            "reverification_executee": cache.compteurs["miss"] == 1,
            "verdict_reverifie": v["verdict"]}
    shutil.rmtree(laboratoire, ignore_errors=True)
    a = negatif["cle-invalidee"]
    b = negatif["compte-taille"]
    rapport += [
        "LE CONTRÔLE NÉGATIF (tls13-16, la notation du dépôt COPIÉE au "
        "laboratoire — le scellé intact) :",
        f"  (a) la mutation d'un octet du corps (le déplacement 0x10 → 0x11, "
        f"{a['octets_mutes']} octet(s) du texte) : la clé {a['cle_intacte']}… "
        f"→ {a['cle_mutee']}… — {'DIFFÉRENTE' if a['cle_differente'] else 'IDENTIQUE — ROUGE'} ; "
        f"le hit {'REFUSÉ' if a['hit_refuse'] else 'ACCEPTÉ — ROUGE'}, la "
        f"re-vérification {'EXÉCUTÉE' if a['reverification_executee'] else 'ESQUIVÉE — ROUGE'} "
        f"— le verdict re-vérifié : {a['verdict_reverifie']} (l'instruction "
        "mutée reste ASSEMBLABLE : le round-trip la valide — c'est la CLÉ qui "
        "attrape, au premier nom)",
        f"  (b) la mutation du compte d'en-tête (Code : 129 → 128 o, "
        f"{b['octets_mutes']} octet(s)) : la clé "
        f"{'DIFFÉRENTE' if b['cle_differente'] else 'IDENTIQUE — ROUGE'}, le "
        f"hit {'REFUSÉ' if b['hit_refuse'] else 'ACCEPTÉ — ROUGE'}, la "
        f"re-vérification COMPLETE ATTRAPE : verdict {b['verdict_reverifie']} "
        "(la faute CONSTATÉE — jamais un souvenir)",
        ""]

    # ---- la sensibilité de la formule (moteur, profil) ------------------------
    source = echant[0]
    cle_ref = CacheRoundTrip.cle(source[0].read_bytes(), cache.moteur,
                                 cache.profil_config(*source[1:]))
    sens = {
        "moteur": CacheRoundTrip.cle(source[0].read_bytes(),
                                     "keystone=X;capstone=X(X)",
                                     cache.profil_config(*source[1:]))
                  != cle_ref,
        "rva": CacheRoundTrip.cle(source[0].read_bytes(), cache.moteur,
                                  cache.profil_config(
                                      source[1], source[2] + 0x10,
                                      source[3])) != cle_ref,
        "slot": CacheRoundTrip.cle(source[0].read_bytes(), cache.moteur,
                                   cache.profil_config(
                                       source[1], source[2],
                                       source[3] + 0x10)) != cle_ref,
        "contrat": CacheRoundTrip.cle(
            source[0].read_bytes(), cache.moteur,
            cache.profil_config(*source[1:]).replace(CONTRAT_R5, "r5-v2"))
                   != cle_ref}
    rapport += [
        "LA SENSIBILITÉ DE LA FORMULE (tout écart = re-vérification) : "
        f"moteur {'OUI' if sens['moteur'] else 'NON — ROUGE'} ; "
        f"rva {'OUI' if sens['rva'] else 'NON — ROUGE'} ; "
        f"slot {'OUI' if sens['slot'] else 'NON — ROUGE'} ; "
        f"contrat {'OUI' if sens['contrat'] else 'NON — ROUGE'}",
        ""]

    ok = (a["cle_differente"] and a["hit_refuse"]
          and a["reverification_executee"]
          and b["cle_differente"] and b["hit_refuse"]
          and b["verdict_reverifie"] == "REFUS"
          and all(sens.values())
          and med_apres < med_avant)
    rapport += [f"LE VERDICT : {'VERT' if ok else 'ROUGE'} — le gain "
                f"{med_avant/max(med_apres,1e-9):.1f}× mesuré, le contrôle "
                "négatif attrapé au premier nom, la formule sensible à "
                "chacun de ses trois constituants"]

    (REG / "roundtrip-cache.json").write_text(json.dumps({
        "moteur": cache.moteur, "contrat": CONTRAT_R5,
        "echantillon": [str(e[0]) for e in echant],
        "semis_s": round(t_semis, 4),
        "avant_s": [round(x, 4) for x in avant],
        "apres_s": [round(x, 4) for x in apres],
        "medianes": {"avant_s": round(med_avant, 4),
                     "apres_s": round(med_apres, 4)},
        "negatif": negatif, "sensibilite": sens,
        "verdict": "VERT" if ok else "ROUGE"}, ensure_ascii=False, indent=1),
        encoding="utf-8")
    (ICI / "rapport-roundtrip-cache.txt").write_text(
        "\n".join(rapport) + "\n", encoding="utf-8")
    print("\n".join(rapport))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
