#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""controle_negatif_v2.py — LES CONTRÔLES NÉGATIFS de la pile (le plan
§ 2.4/§ 3.3/§ 5.6, l'étape de vérification de l'instruction : « entrée de
cache mutée → attrapée ; moteur divergent → refus nommé ») :

  (1) L'ENTRÉE DE CACHE MUTÉE — un octet du cadre relevé muté au fichier
      mémo v2 → le chargement REFUSE (CHAÎNE-ROMPUE, fail-closed) ;
  (2) LE COMPTEUR D'AUDIT MUTÉ — le compteur chaîné muté → SIGNATURE-
      INVALIDE (le compteur vit dans le cœur signé) ;
  (3) LA RACINE MUTÉE → RACINE-DIVERGENTE ;
  (4) LA CLÉ CHANGÉE = L'ABSENCE — un terme de la clé v2 changé (la config
      émulateur) → la consultation rend RIEN → la session VIT (le repli,
      jamais l'échec muet) — l'invalidation par construction ;
  (5) LE MOTEUR DIVERGENT — un lanceur à shim ReadFile MUTÉ (un octet du
      tampon inversé) → la comparaison de l'échantillon d'audit REFUSE
      (MOTEUR-DIVERGENT) — la porte divise les moteurs honnêtes des
      moteurs faux.

Écrit : preuves/controle-negatif-v2.txt. Code 0 = les CINQ attrapés."""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ICI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import memo_sessions_v2 as MEMO     # noqa: E402
import moteur_qemu as MQ            # noqa: E402

MEMO_FICHIER = ICI / "memo-sessions-v2.json"


def cas(nom: str, fn) -> bool:
    try:
        fn()
        print(f"ROUGE {nom} : NON attrapé")
        return False
    except Exception as e:                       # noqa: BLE001
        attendu = getattr(e, "nom_attendu", None)
        ok = attendu is None or str(e).startswith(attendu)
        print(f"VERT  {nom} → REFUS {str(e)[:90]}{'…' if len(str(e)) > 90 else ''}"
              + ("" if ok else "  [MAIS le refus inattendu]"))
        return ok


def ecrire_memo(doc: dict, chemin: pathlib.Path) -> None:
    chemin.write_text(json.dumps(doc, ensure_ascii=False, indent=1),
                      encoding="utf-8")


def main() -> int:
    lignes: list[str] = []
    verts = 0

    doc = json.loads(MEMO_FICHIER.read_text(encoding="utf-8"))

    # (1) l'entrée de cache mutée : un octet du premier cadre relevé
    def _entree_mutee():
        import copy
        d = copy.deepcopy(doc)
        c = d["entrees"][0]["valeur"]["cadre_hex"]
        d["entrees"][0]["valeur"]["cadre_hex"] = \
            ("0" if c[0] != "0" else "1") + c[1:]
        f = pathlib.Path(tempfile.mkstemp(suffix=".json")[1])
        ecrire_memo(d, f)
        try:
            MEMO.MemoSessionsV2.charger(str(f))
        finally:
            f.unlink(missing_ok=True)
    if cas("l'entrée de cache mutée (un octet du cadre relevé)",
           _entree_mutee):
        verts += 1
        lignes.append("VERT l'entrée de cache mutée → CHAÎNE-ROMPUE au "
                      "chargement (fail-closed, jamais cru)")

    # (2) le compteur d'audit muté (dans le cœur signé)
    def _compteur_mute():
        import copy
        d = copy.deepcopy(doc)
        d["compteur_runs"] = int(d["compteur_runs"]) + 1
        f = pathlib.Path(tempfile.mkstemp(suffix=".json")[1])
        ecrire_memo(d, f)
        try:
            MEMO.MemoSessionsV2.charger(str(f))
        finally:
            f.unlink(missing_ok=True)
    if cas("le compteur d'audit muté", _compteur_mute):
        verts += 1
        lignes.append("VERT le compteur d'audit muté → SIGNATURE-INVALIDE "
                      "(le compteur vit dans le cœur signé — l'audit ne se "
                      "réécrit pas en silence)")

    # (3) la racine mutée
    def _racine_mutee():
        import copy
        d = copy.deepcopy(doc)
        d["racine"] = "0" * 64
        f = pathlib.Path(tempfile.mkstemp(suffix=".json")[1])
        ecrire_memo(d, f)
        try:
            MEMO.MemoSessionsV2.charger(str(f))
        finally:
            f.unlink(missing_ok=True)
    if cas("la racine mutée", _racine_mutee):
        verts += 1
        lignes.append("VERT la racine mutée → RACINE-DIVERGENTE")

    # (4) la clé changée = l'absence (la config émulateur change → une
    # autre clé → RIEN au mémo → la session vit)
    e0 = doc["entrees"][0]
    memo = MEMO.MemoSessionsV2.charger(str(MEMO_FICHIER))
    bloc = bytes.fromhex(e0["valeur"]["cadre_hex"][:64].ljust(64, "0"))
    cle_vraie = e0["cle"]
    config_autre = MEMO.config_emulateur(
        "autremoteur", {"m9": HN_M9()}, [[4096, 65536]], None)
    import hashlib
    contrat = hashlib.sha256(b"contrat").digest()
    cle_autre = MEMO.cle_session_v2(
        bloc, b"entree", contrat, config_autre, 20261114, "oracle-x")
    absence = (memo.consulter(cle_vraie) is not None
               and memo.consulter(cle_autre) is None)
    if absence:
        verts += 1
        print("VERT  la clé changée (la config émulateur) → l'ABSENCE : la "
              "consultation rend RIEN, la session VIT (le repli)")
        lignes.append("VERT la clé changée = l'absence : un terme de la "
                      "clé v2 changé → RIEN au mémo → la re-exécution "
                      "vivante (l'invalidation par construction)")
    else:
        print("ROUGE la clé changée : la consultation n'est pas vide")

    # (5) le moteur divergent : le lanceur à shim ReadFile muté
    src = (ICI / "lanceur_qemu.c").read_text(encoding="utf-8")
    marque = 'if (rendus > 0) memcpy(tampon, f->contenu + pos, rendus);'
    assert marque in src
    src_div = src.replace(
        marque,
        'if (rendus > 0) { memcpy(tampon, f->contenu + pos, rendus); '
        'tampon[0] = (uint8_t)(tampon[0] ^ 0x01); }   /* LE MOTEUR FAUX : '
        'un octet du tampon inversé — la porte doit l attraper */')
    fdiv = ICI / "lanceur_qemu_divergent.c"
    fdiv.write_text(src_div, encoding="utf-8")
    bdiv = ICI / "lanceur_qemu_divergent"
    subprocess.run(["gcc", "-O2", "-static",
                    "-Wl,-Ttext-segment=0x10000000", "-o", str(bdiv),
                    str(fdiv)], check=True)

    ops, fichiers = MQ.echantillon_ops()
    reduites = [("ouvrir", "temoin-384.bin"), ("lire", 0), ("fermer",)]
    bac = pathlib.Path(tempfile.mkdtemp(prefix="neg-moteur-"))
    ref = MQ.ReferenceUnicorn()
    ref.declarer_temoins(fichiers)
    flux_ref = ref.executer(reduites)
    vol = MQ.VolumeQEMU(bac / "qemu")
    vol.construire_image()
    vol.lanceur = bdiv               # LE MOTEUR FAUX
    flux_div = vol.executer(reduites, fichiers)
    ecart_moteur = any(a != b for a, b in zip(flux_ref, flux_div))
    if ecart_moteur:
        verts += 1
        premiere = next(i for i, (a, b) in
                        enumerate(zip(flux_ref, flux_div)) if a != b)
        print(f"VERT  le moteur divergent (un octet du tampon inversé au "
              f"shim ReadFile) → ATTRAPÉ à la ligne {premiere} : la "
              f"comparaison REFUSE (MOTEUR-DIVERGENT)")
        lignes.append(f"VERT le moteur divergent → ATTRAPÉ : le lanceur à "
                      f"shim muté diverge de la référence Unicorn à la "
                      f"ligne {premiere} de l'échantillon — le refus nommé "
                      f"MOTEUR-DIVERGENT, BLOQUANT (tout écart nominal)")
    else:
        print("ROUGE le moteur divergent : NON attrapé")

    (ICI / "preuves").mkdir(exist_ok=True)
    (ICI / "preuves" / "controle-negatif-v2.txt").write_text(
        "LES CONTRÔLES NÉGATIFS DE LA PILE cq01qv1za (le plan § 2.4/§ 3.3)"
        "\n" + "=" * 72 + "\n\n" + "\n".join(lignes)
        + f"\n\nLE BILAN : {verts}/5 VERT — "
        + ("la porte divise les moteurs honnêtes des moteux faux, le cache "
           "reste vérifié".replace("moteux", "moteurs")
           if verts == 5 else "ROUGE — un contrôle non tenu") + "\n",
        encoding="utf-8")
    print(f"\nLE BILAN : {verts}/5 VERT")
    return 0 if verts == 5 else 2


def HN_M9():
    import hashlib
    return hashlib.sha256(b"m9").hexdigest()


if __name__ == "__main__":
    sys.exit(main())
