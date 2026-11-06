#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rapatrier_remise_ceremonie.py — rapatrie la remise de la cérémonie du
build 1.0.0 depuis /test du Drive vers download/remise-ceremonie-100/,
md5 contrôlé par pièce contre les métadonnées Drive (modèle
rapatrier_preuves_m7d.py, D99 : zéro mélange — dossier dédié à la remise ;
lecture seule, aucune écriture Drive).

Les DEUX pièces du geste du développeur (LISEZMOI-ceremonie-build-1.0.0
étape 4) :
  signatures-I.txt     — TREIZE lignes « arbre balise signature »
  cle-publique-I.txt   — la clé du 04/11, RÉUTILISÉE (173fae9c…)

Recoups AVANT dépôt (la clé privée ne traverse jamais le bac à sable —
seuls les deux fichiers publics du geste remontent) :
  1. md5 par pièce == métadonnées Drive ;
  2. la clé dépose 173fae9c… (la clé du 04/11, LA RÈGLE D'OR — toute
     autre valeur = mauvaise clé, arrêt) ;
  3. la remise porte les 13 lignes arbre+balise == a-signer.txt local
     (l'empreinte vivante sera revérifiée par sceau_I.py deposer).

Usage : python3 scripts/rapatrier_remise_ceremonie.py
Code de sortie : 0 = remise conforme, 1 = écart, 2 = erreur fatale.
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"          # /test
DEST = pathlib.Path("/home/z/my-project/download/remise-ceremonie-100")
A_SIGNER = REPO / "v06" / "sceau-I" / "a-signer.txt"

PIECES_ATTENDUES = {"signatures-I.txt", "cle-publique-I.txt"}

# LA RÈGLE D'OR (LISEZMOI § LA RÈGLE D'OR) : la clé du 04/11 RÉUTILISÉE.
CLE_0411_PREFIXE = "173fae9c"


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    try:
        entries = ds.list_folder(TEST_ID)
    except Exception as exc:  # noqa: BLE001
        print(f"[remise-100] ERREUR FATALE : listage /test impossible : {exc}",
              file=sys.stderr)
        return 2
    pieces = {n: f for n, f in entries.items()
              if f.get("mimeType") != ds.FOLDER_MIME
              and n in PIECES_ATTENDUES}
    manquantes = PIECES_ATTENDUES - set(pieces)
    if manquantes:
        print(f"[remise-100] ERREUR FATALE : pièces absentes de /test : "
              f"{sorted(manquantes)}", file=sys.stderr)
        return 2

    # 1 — téléchargement, md5 par pièce contre les métadonnées Drive
    total, ok = 0, 0
    for nom, f in sorted(pieces.items()):
        total += 1
        url = f"{ds.API}/files/{f['id']}?alt=media"
        st, body, _ = ds.api("GET", url)
        if st != 200:
            print(f"[remise-100] ÉCHEC téléchargement {nom} (HTTP {st})")
            continue
        chemin = DEST / nom
        chemin.write_bytes(body)
        local = ds.md5_of(chemin)
        attendu = (f.get("md5Checksum") or "").lower()
        if attendu and local != attendu:
            print(f"[remise-100] ÉCART md5 {nom} : local {local} != "
                  f"drive {attendu}")
            continue
        ok += 1
        print(f"[remise-100] {nom} : {len(body)} o, md5 {local[:8]}… "
              f"== drive — CONSTATÉ")
    if ok != total:
        print(f"[remise-100] ÉCHEC : {ok}/{total} pièces conformes")
        return 1

    # 2 — recoup de la clé : la clé du 04/11, RÉUTILISÉE (jamais « generer »)
    cle = (DEST / "cle-publique-I.txt").read_text(encoding="utf-8").strip()
    if not cle.startswith(CLE_0411_PREFIXE):
        print(f"[remise-100] ÉCART GRAVE : cle-publique-I.txt déposée "
              f"commence par {cle[:8]}… != {CLE_0411_PREFIXE}… (la clé du "
              f"04/11) — MAUVAISE CLÉ, arrêt (la remise ne sera pas déposée)",
              file=sys.stderr)
        return 1
    print(f"[remise-100] clé du geste : {cle[:8]}… == 173fae9c… "
          f"(la clé du 04/11, réutilisée) — CONSTATÉ")

    # 3 — recoup de la remise : 13 lignes arbre+balise == a-signer.txt local
    attendues = {}
    for ligne in A_SIGNER.read_text(encoding="utf-8").splitlines():
        if ligne.strip():
            arbre, balise, empreinte = ligne.split()
            attendues[arbre] = (balise, empreinte)
    lignes_remise = [l.strip() for l in
                     (DEST / "signatures-I.txt").read_text(
                         encoding="utf-8").splitlines() if l.strip()]
    if len(lignes_remise) != 13:
        print(f"[remise-100] ÉCART : signatures-I.txt porte "
              f"{len(lignes_remise)} lignes, 13 attendues", file=sys.stderr)
        return 1
    for ligne in lignes_remise:
        morceaux = ligne.split()
        if len(morceaux) != 3:
            print(f"[remise-100] ÉCART : ligne malformée : {ligne!r}",
                  file=sys.stderr)
            return 1
        arbre, balise, signature = morceaux
        if arbre not in attendues:
            print(f"[remise-100] ÉCART : arbre inconnu : {arbre!r}",
                  file=sys.stderr)
            return 1
        if balise != attendues[arbre][0]:
            print(f"[remise-100] ÉCART : balise {balise!r} != "
                  f"{attendues[arbre][0]!r} pour {arbre}", file=sys.stderr)
            return 1
        if len(signature) != 128 or any(
                c not in "0123456789abcdef" for c in signature):
            print(f"[remise-100] ÉCART : signature malformée pour {arbre}",
                  file=sys.stderr)
            return 1
    print(f"[remise-100] la remise : 13 lignes, arbres+balises == "
          f"a-signer.txt local — CONSTATÉ")
    print(f"[remise-100] LES DEUX PIÈCES DU GESTE SONT LÀ, md5 contrôlés "
          f"— le dépôt (sceau_I.py deposer) peut commencer")
    return 0


if __name__ == "__main__":
    sys.exit(main())
