#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""corriger_phrase_racine.py — corrige l'écart nommé au Task ID 60 : le
PHRASE-CONTROLE-COFFRE.txt de la racine du coffre Drive (« Triade ») porte
3 lignes (59 o) alors que la remise normée D81 est la PHRASE SEULE (33 o,
la copie du dépôt) — « l'ouverture directe par --phrase-fichier échoue ;
la copie du DÉPÔT ouvre le coffre — l'écart vit au dossier Drive racine,
à corriger à la prochaine synchro (aucune mutation de ma part) ».

La correction était PLANNÉE : ce script l'exécute en fail-closed intégral —
AVANT : constat de l'écart (taille, lignes), ligne 1 == phrase du dépôt
(par comparaison en mémoire, JAMAIS affichée), l'ouverture par le fichier
Drive ÉCHOUE, l'ouverture par la copie du dépôt RÉUSSIT ;
MUTATION : upload_update du fichier Drive avec le contenu du dépôt ;
APRÈS : re-téléchargement, identité octet pour octet avec le dépôt,
ouverture du coffre par le fichier RAPATRIÉ — VERT.

Aucun secret n'est affiché : uniquement tailles, empreintes tronquées et
verdicts. Le coffre jugé : .keys/coffre_fort.bin (md5 23a2987a… attesté
D144), jamais muté (lecture seule via lister).
"""

import hashlib
import pathlib
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

NOM_FICHIER = "PHRASE-CONTROLE-COFFRE.txt"
TAILLE_ATTENDUE_AVANT = 59          # constat Task ID 60 : 3 lignes, 59 o
TAILLE_NORME_D81 = 33               # la remise du dépôt : phrase seule
COFFRE = REPO / ".keys" / "coffre_fort.bin"
COFFRE_MD5 = "23a2987a9817c90d2439abb6f991018d"


def _md5(donnees: bytes) -> str:
    return hashlib.md5(donnees).hexdigest()


def _ouvrir_coffre(phrase_fichier: pathlib.Path) -> tuple[int, str]:
    """Exécute coffre_fort.py lister avec la phrase du fichier — rc + sortie."""
    proc = subprocess.run(
        [sys.executable, str(REPO / "coffre_fort.py"),
         "--chemin", str(COFFRE), "lister",
         "--phrase-fichier", str(phrase_fichier)],
        capture_output=True, text=True, timeout=120,
    )
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def main() -> int:
    # 0. préalables ---------------------------------------------------------
    depot = REPO / NOM_FICHIER
    if not depot.is_file():
        print(f"ERREUR : {NOM_FICHIER} absent du dépôt", file=sys.stderr)
        return 1
    ref = depot.read_bytes()
    if len(ref) != TAILLE_NORME_D81:
        print(f"ERREUR : la copie du dépôt fait {len(ref)} o "
              f"({TAILLE_NORME_D81} attendus — la remise D81 a-t-elle tourné ?)",
              file=sys.stderr)
        return 1
    if not COFFRE.is_file():
        print("ERREUR : .keys/coffre_fort.bin absent", file=sys.stderr)
        return 1
    if _md5(COFFRE.read_bytes()) != COFFRE_MD5:
        print("ERREUR : coffre .keys/coffre_fort.bin md5 divergent "
              "(23a2987a… attendu, D144)", file=sys.stderr)
        return 1

    # 1. localisation du fichier Drive racine -------------------------------
    racine = ds.list_folder(ds.DRIVE_ROOT_ID)
    meta = racine.get(NOM_FICHIER)
    if not meta or meta.get("mimeType") == ds.FOLDER_MIME:
        print(f"ERREUR : {NOM_FICHIER} absent de la racine Drive « Triade »",
              file=sys.stderr)
        return 1
    fid = meta["id"]
    print(f"[1] racine Drive : {NOM_FICHIER} id={fid[:12]}… "
          f"(taille API {meta.get('size', '?')} o)")

    # 2. téléchargement du contenu actuel ------------------------------------
    st, body, _ = ds.api("GET", f"{ds.API}/files/{fid}?alt=media")
    if st != 200:
        print(f"ERREUR : téléchargement HTTP {st}", file=sys.stderr)
        return 1
    lignes = body.decode("utf-8", errors="replace").splitlines()
    print(f"[2] contenu ACTUEL : {len(body)} o, {len(lignes)} ligne(s) — "
          f"md5 {_md5(body)[:12]}…")
    if len(body) != TAILLE_ATTENDUE_AVANT:
        print(f"ÉCART AU CONSTAT : {len(body)} o != {TAILLE_ATTENDUE_AVANT} o "
              "attendus (constat Task 60) — AUCUNE MUTATION, à examiner",
              file=sys.stderr)
        return 1
    if not lignes:
        print("ERREUR : fichier Drive vide", file=sys.stderr)
        return 1

    # 3. ligne 1 == phrase du dépôt (comparaison en mémoire, jamais affichée)
    if lignes[0].strip() != ref.decode("utf-8").strip():
        print("ERREUR FATALE : la ligne 1 du fichier Drive DIVERGE de la "
              "remise du dépôt — AUCUNE MUTATION (l'écart n'est pas celui "
              "du Task 60)", file=sys.stderr)
        return 1
    print("[3] ligne 1 du fichier Drive == phrase du dépôt (conforme au "
          "constat Task 60)")

    # 4. preuves avant : l'écart réel (échec) et la référence (succès) -------
    with tempfile.TemporaryDirectory() as td:
        tdr = pathlib.Path(td)
        f_avant = tdr / "drive_avant.txt"
        f_ref = tdr / "depot_ref.txt"
        f_avant.write_bytes(body)
        f_ref.write_bytes(ref)
        f_avant.chmod(0o600)
        f_ref.chmod(0o600)
        rc_avant, sortie_avant = _ouvrir_coffre(f_avant)
        rc_ref, _ = _ouvrir_coffre(f_ref)
        print(f"[4] ouverture par le fichier Drive ACTUEL : rc={rc_avant} "
              f"({'ÉCHEC — l\'écart D81 confirmé' if rc_avant != 0 else 'SUCCÈS inattendu'})")
        print(f"    sortie coffre (défaillance) : {sortie_avant[:120]}")
        print(f"    ouverture par la COPIE DU DÉPÔT : rc={rc_ref} "
              f"({'VERT — la référence ouvre' if rc_ref == 0 else 'ÉCHEC — référence morte, STOP'})")
        if rc_avant == 0 or rc_ref != 0:
            print("ERREUR : l'écart attendu n'est pas constaté — AUCUNE "
                  "MUTATION", file=sys.stderr)
            return 1

    # 5. LA MUTATION (prévue Task 60 : « à corriger à la prochaine synchro »)
    ds.upload_update(fid, depot)
    print("[5] MUTATION : contenu du dépôt (33 o, phrase seule, norme D81) "
          "posé sur le fichier Drive")

    # 6. vérification après : identité + ouverture VERTe ---------------------
    st2, body2, _ = ds.api("GET", f"{ds.API}/files/{fid}?alt=media")
    if st2 != 200:
        print(f"ERREUR : re-téléchargement HTTP {st2}", file=sys.stderr)
        return 1
    identique = body2 == ref
    print(f"[6] re-téléchargement : {len(body2)} o, md5 {_md5(body2)[:12]}… — "
          f"{'IDENTIQUE au dépôt octet pour octet' if identique else 'DIVERGENT'}")
    if not identique or len(body2) != TAILLE_NORME_D81:
        print("ERREUR FATALE : le fichier Drive diverge encore — REPRENDRE",
              file=sys.stderr)
        return 1
    with tempfile.TemporaryDirectory() as td:
        f_apres = pathlib.Path(td) / "drive_apres.txt"
        f_apres.write_bytes(body2)
        f_apres.chmod(0o600)
        rc_apres, _ = _ouvrir_coffre(f_apres)
        print(f"[7] ouverture par le fichier Drive CORRIGÉ (rapatrié) : "
              f"rc={rc_apres} — {'VERT' if rc_apres == 0 else 'ÉCHEC'}")
        if rc_apres != 0:
            print("ERREUR FATALE : le fichier corrigé n'ouvre pas le coffre",
                  file=sys.stderr)
            return 1

    print("BILAN : écart D81 FERMÉ — le PHRASE-CONTROLE-COFFRE.txt de la "
          "racine Drive est la phrase seule (33 o), identique à la remise "
          "du dépôt, et IL OUVRE le coffre (rc=0). Coffre INTÈGRE (md5 "
          f"{COFFRE_MD5[:8]}…, jamais muté).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
