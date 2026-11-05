#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — Rapatriement + recoup de la cérémonie de l'ère M8 (D162).

Le développeur a exécuté la cérémonie hors-ligne (la re-signature des
12 arbres avec la clé du 04/11 — LISEZMOI-ceremonie-ere-M8.txt, Task 77)
et déposé signatures-I.txt dans le coffre /test du Drive.

Ce script (LECTURE SEULE sur le dépôt v06/) :
  1. sonde /test par le RELAIS COMPTE DE SERVICE (le jeton OAuth du
     relais est mort — invalid_grant, même constat que le 29/10) ;
  2. rapatrie signatures-I.txt vers download/ceremonie-ere-m8/ avec
     contrôle md5 APRÈS écriture contre les métadonnées Drive ;
  3. recoupe SUR PIÈCES avant tout dépôt :
       - format : 12 lignes « arbre balise signature(128 hex) », balises
         == la table canonique du dépôt ;
       - l'ANCRE DE CLÉ : cle-publique-I.txt locale == 173fae9c… (l'ancre
         écrite noir sur blanc au LISEZMOI de l'ère — « si cle-publique-
         I.txt diverge : ARRÊT », la règle d'or : JAMAIS « generer ») ;
       - LE RECOUP DE L'ÈRE : les DIX arbres inchangés portent les MÊMES
         signatures que celles déposées au 04/11 (Ed25519 déterministe :
         la clé du 04/11 réutilisée redonne les signatures déposées —
         une divergence nomme une clé neuve ou un arbre bougé) ;
       - m0 re-signé (l'empreinte a changé — registre étendu au M8-(a)),
         m8 arbre NEUF (aucune signature déposée au 04/11) ;
       - les empreintes vivantes des 12 arbres == a-signer.txt (la remise
         fraîche déposée au kit par le hook du commit d999103) ;
       - chaque signature de la remise VÉRIFIE Ed25519 contre la clé
         publique sur l'empreinte du manifeste VIVANT (12/12).

AUCUNE écriture dans v06/ : le dépôt canonique (sceau_I.py deposer) est
le geste suivant, explicite. Ce script prépare le verdict ; il ne signe
rien et n'installe rien (la cérémonie appartient au développeur, D87/D162).

Usage : python3 scripts/rapatrier_ceremonie_m8.py
Codes de sortie : 0 = recoup intégral VERT ; 1 = échec nommé ;
                  2 = accès Drive impossible.
"""
import importlib.util
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import relais_service_account as rsa  # noqa: E402  (l'import SURGIE le jeton)
import drive_sync as ds  # noqa: E402

# sceau_I chargé par CHEMIN ABSOLU (D158 : les lignées homonymes se chargent
# par importlib — jamais par sys.path qui écrase).
_spec = importlib.util.spec_from_file_location(
    "sceau_I", REPO / "v06" / "sceau_I.py")
sceau_I = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sceau_I)

DOSSIER_CEREMONIE = REPO / "download" / "ceremonie-ere-m8"
NOM_PIECE = "signatures-I.txt"
ANCRE_CLE_ERE = "173fae9c75229b154dcb2b6f582c8ad386a5ab14230db74694ca2dd6b57f711f"
ARBRES_INCHANGES = ["m1", "m2", "m3", "m4", "m5", "m6", "m7",
                    "demo", "terrain", "v06"]
ARBRES_NOUVEAUX = ["m0", "m8"]  # empreintes bougées à l'ère M8 (D162)


def telecharger(file_id, destination):
    url = f"{ds.API}/files/{file_id}?alt=media"
    st, body, _ = ds.api("GET", url)
    if st != 200:
        raise ds.SyncError(f"téléchargement impossible ({st}) : {body[:120]!r}")
    destination.write_bytes(body)
    return ds.md5_of(destination)


def main() -> int:
    # ---------------------------------------------------------------- sondage
    try:
        entrees = ds.list_folder(rsa.TEST_ID)
    except ds.SyncError as e:
        print(f"[ceremonie-M8] ÉCHEC D'ACCÈS au coffre /test : {e}", file=sys.stderr)
        return 2
    piece = entrees.get(NOM_PIECE)
    if piece is None:
        print(f"[ceremonie-M8] ÉCHEC : « {NOM_PIECE} » ABSENT du coffre /test "
              f"({len(entrees)} entrées vues) — le dépôt du développeur "
              f"n'est pas constaté", file=sys.stderr)
        return 1
    md5_drive = piece.get("md5Checksum")
    print(f"[ceremonie-M8] pièce trouvée dans /test : {NOM_PIECE}  "
          f"md5(annoncé Drive)={md5_drive}")

    # ----------------------------------------------------------- rapatriement
    DOSSIER_CEREMONIE.mkdir(parents=True, exist_ok=True)
    cible = DOSSIER_CEREMONIE / NOM_PIECE
    md5_local = telecharger(piece["id"], cible)
    if md5_local != md5_drive:
        print(f"[ceremonie-M8] ÉCHEC md5 : local {md5_local} != Drive {md5_drive}",
              file=sys.stderr)
        return 1
    print(f"[ceremonie-M8] rapatrié : {cible}  md5={md5_local}  "
          f"({cible.stat().st_size} o) — MATCH les métadonnées Drive")

    # ---------------------------------------------------------------- recoups
    echecs = []

    # (a) ancre de clé — la règle d'or du LISEZMOI de l'ère
    cle_txt = (REPO / "v06" / "sceau-I" / "cle-publique-I.txt").read_text().strip()
    if cle_txt != ANCRE_CLE_ERE:
        echecs.append(f"ANCRE DE CLÉ divergente : cle-publique-I.txt local "
                      f"{cle_txt[:16]}… != l'ancre de l'ère {ANCRE_CLE_ERE[:16]}… "
                      f"(« si cle-publique-I.txt diverge : ARRÊT »)")
    else:
        print(f"[ceremonie-M8] ancre de clé : cle-publique-I.txt == "
              f"{ANCRE_CLE_ERE[:16]}… (l'ancre de l'ère — la continuité "
              f"« reelle » tenue)")
    cle = bytes.fromhex(cle_txt)

    # (b) la remise fraîche a-signer.txt (12 arbres)
    a_signer = {}
    for ligne in (REPO / "v06" / "sceau-I" / "a-signer.txt").read_text().splitlines():
        if ligne.strip():
            arbre, balise, empreinte = ligne.split()
            a_signer[arbre] = (balise, empreinte)
    if len(a_signer) != 12:
        echecs.append(f"a-signer.txt : {len(a_signer)} arbres (12 attendus)")

    # (c) format de la remise déposée
    lignes = [l.strip() for l in cible.read_text().splitlines() if l.strip()]
    remise = {}
    for ligne in lignes:
        m = ligne.split()
        if len(m) != 3:
            echecs.append(f"ligne malformée dans la remise : {ligne!r}")
            continue
        arbre, balise, sig = m
        if arbre not in sceau_I.ARBRES:
            echecs.append(f"arbre inconnu dans la remise : {arbre!r}")
            continue
        if balise != sceau_I.ARBRES[arbre][1]:
            echecs.append(f"balise divergente pour {arbre} : {balise!r} != "
                          f"{sceau_I.ARBRES[arbre][1]!r}")
            continue
        if len(sig) != 128 or any(c not in "0123456789abcdef" for c in sig):
            echecs.append(f"signature malformée pour {arbre} (128 hex attendus)")
            continue
        remise[arbre] = sig
    if len(remise) != 12:
        echecs.append(f"remise INCOMPLÈTE : {len(remise)}/12 arbres")
    print(f"[ceremonie-M8] format de la remise : {len(remise)}/12 lignes "
          f"valides (arbre balise signature-128hex)")

    # (d) le recoup de l'ère + vérifications par arbre
    print()
    print(f"{'arbre':<9} {'balise':<22} {'vivant==a-signer':<17} "
          f"{'Ed25519':<8} ère")
    verts = 0
    for arbre in sceau_I.ARBRES:
        try:
            _, empreinte_vivante = sceau_I.manifeste(arbre)
        except sceau_I.EchecSceauI as e:
            echecs.append(f"{arbre} : arbre vivant illisible : {e}")
            print(f"{arbre:<9} {'—':<22} {'ÉCHEC':<17} {'—':<8} "
                  f"arbre illisible")
            continue
        sig = remise.get(arbre)
        if sig is None:
            echecs.append(f"{arbre} : absent de la remise")
            continue
        # empreinte vivante == a-signer (la remise fraîche)
        r_a_signer = (a_signer.get(arbre, ("?", ""))[1] == empreinte_vivante)
        # vérification cryptographique contre la clé de l'ère
        r_crypto = sceau_I._verifier_ed25519(
            bytes.fromhex(empreinte_vivante), bytes.fromhex(sig), cle)
        # le recoup de l'ère : comparaison à la signature déposée au 04/11
        chemin_deposee = REPO / "v06" / "sceau-I" / "signatures" / f"{arbre}.txt"
        if arbre in ARBRES_INCHANGES:
            deposee = chemin_deposee.read_text().strip() if chemin_deposee.is_file() else None
            if deposee is None:
                note_ere = "déposée 04/11 ABSENTE (inattendu)"
                echecs.append(f"{arbre} : signature du 04/11 absente du dépôt")
            elif deposee == sig:
                note_ere = "IDENTIQUE au 04/11 (clé réutilisée)"
            else:
                note_ere = "DIVERGE du 04/11 (clé neuve ou arbre bougé)"
                echecs.append(f"{arbre} : signature DIVERGENTE du 04/11 — "
                              f"la clé de l'ère n'a vraisemblablement pas été "
                              f"réutilisée (règle d'or : JAMAIS « generer »)")
        else:  # m0 / m8 : empreintes bougées à l'ère
            deposee = chemin_deposee.read_text().strip() if chemin_deposee.is_file() else None
            if arbre == "m0":
                if deposee is not None and deposee == sig:
                    note_ere = "IDENTIQUE au 04/11 (inattendu : m0 a changé !)"
                    echecs.append("m0 : signature IDENTIQUE au 04/11 alors que "
                                  "le registre a été étendu (empreinte bougée)")
                else:
                    note_ere = "re-signé (registre étendu M8-(a))"
            else:  # m8 : arbre neuf
                note_ere = "arbre NEUF (aucune déposée au 04/11)"
                if deposee is not None:
                    echecs.append("m8 : une signature du 04/11 existe "
                                  "(inattendu pour un arbre neuf)")
        if not r_a_signer:
            echecs.append(f"{arbre} : empreinte vivante {empreinte_vivante[:16]}… "
                          f"!= a-signer.txt {a_signer.get(arbre, ('?', '?'))[1][:16]}…")
        if not r_crypto:
            echecs.append(f"{arbre} : signature Ed25519 INVÉRIFIABLE contre "
                          f"la clé {cle_txt[:16]}…")
        ok = r_a_signer and r_crypto
        verts += 1 if ok else 0
        print(f"{arbre:<9} {sceau_I.ARBRES[arbre][1]:<22} "
              f"{'OUI' if r_a_signer else 'NON':<17} "
              f"{'VERT' if r_crypto else 'ÉCHEC':<8} {note_ere}")
    print()

    # ---------------------------------------------------------------- verdict
    if echecs:
        print(f"[ceremonie-M8] RECOUPE EN ÉCHEC — {len(echecs)} faute(s) nommée(s), "
              f"RIEN n'est déposé :")
        for e in echecs:
            print(f"  ✗ {e}")
        return 1
    print(f"[ceremonie-M8] RECOUPE INTÉGRAL VERT — {verts}/12 arbres : la remise "
          f"du développeur vérifie sur pièces (clé de l'ère {cle_txt[:16]}…, "
          f"les DIX inchangés == les signatures du 04/11, m0 re-signé, m8 neuf, "
          f"empreintes == a-signer.txt 12/12).")
    print("[ceremonie-M8] geste suivant (canonique) : "
          "python3 v06/sceau_I.py deposer "
          "download/ceremonie-ere-m8/signatures-I.txt "
          "--cle v06/sceau-I/cle-publique-I.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
