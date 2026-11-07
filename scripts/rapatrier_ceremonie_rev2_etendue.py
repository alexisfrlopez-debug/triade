#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — Rapatriement + recoup de la SECONDE RE-CÉRÉMONIE de la
révision 2 : LA REMISE ÉTENDUE (D166 r.9, l'erratum n° 9).

Le développeur a exécuté la signature hors-ligne de la remise ÉTENDUE de
la révision 2 (l'Entrée 187 : l'erratum n° 9 — la réception sys-06 porte
le MÊME WSABUF « packé » que l'émission sys-05 ; l'arbre m8 a évolué
ENCORE : sys-06-reception.md SEUL diverge du manifeste signé, l'empreinte
m8 à signer : c444d730…, les DOUZE autres lignes byte-identiques) et
re-déposé signatures-I.txt + cle-publique-I.txt dans le coffre /test du
Drive (l'annonce du développeur : « j'ai refait les signatures et elles
sont re-déposées dans le drive /test »).

Ce script (LECTURE SEULE sur le dépôt v06/) :
  1. sonde /test par le canal OAuth du relais ;
  2. rapatrie signatures-I.txt ET cle-publique-I.txt vers
     download/ceremonie-revision2-etendue/ avec contrôle md5 APRÈS
     écriture contre les métadonnées Drive — et REFUSE la remise
     PÉRIMÉE (md5 af382476… : la première signature de la révision 2,
     contre 3e778fa0…, déjà installée — re-déposer l'ancienne n'est
     pas re-signer) ;
  3. recoupe SUR PIÈCES avant tout dépôt :
       - l'ANCRE DE CLÉ : la clé déposée par le développeur ==
         173fae9c… (l'ancre de toutes les ères — « si cle-publique-I.txt
         diverge : ARRÊT », la règle d'or : JAMAIS « generer ») ;
       - format : 13 lignes « arbre balise signature(128 hex) », balises
         == la table canonique du dépôt (la rotation couvre TOUS les
         arbres, spec § 5) ;
       - LE RECOUP D163 (rejoint une QUATRIÈME fois) : les DOUZE arbres
         inchangés portent les MÊMES signatures que celles DÉPOSÉES au
         dépôt (== les signatures du build 1.0.0 — Ed25519 déterministe :
         la clé du 04/11 réutilisée redonne les signatures déposées —
         une divergence nomme une clé neuve ou un arbre bougé) ;
       - m8 RE-SIGNÉ ENCORE (l'empreinte a changé une seconde fois :
         3e778fa0… → c444d730…, l'erratum n° 9) : la signature DOIT
         diverger de la déposée (a7a787a0…, la première signature de la
         révision 2) ET vérifier Ed25519 contre l'empreinte vivante
         c444d730… ;
       - les empreintes vivantes des 13 arbres == a-signer.txt (la remise
         fraîche régénérée à l'Entrée 187) ;
       - chaque signature de la remise VÉRIFIÉE Ed25519 contre la clé
         publique sur l'empreinte du manifeste VIVANT (13/13) ;
       - LE DIFF CONTRÔLÉ : la remise étendue vs la première remise de
         la révision 2 (download/ceremonie-revision2/signatures-I.txt) :
         UNE ligne changée, LA m8 — les DOUZE autres byte-identiques
         (le précédent M9-(d) tenu sur la remise, tenu sur les
         signatures).

AUCUNE écriture dans v06/ : le dépôt canonique (sceau_I.py deposer) est
le geste suivant, explicite. Ce script prépare le verdict ; il ne signe
rien et n'installe rien (la cérémonie appartient au développeur, D87).

Usage : python3 scripts/rapatrier_ceremonie_rev2_etendue.py
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

DOSSIER_CEREMONIE = REPO / "download" / "ceremonie-revision2-etendue"
PREMIERE_REMISE = REPO / "download" / "ceremonie-revision2" / "signatures-I.txt"
NOM_REMISE = "signatures-I.txt"
NOM_CLE = "cle-publique-I.txt"
ANCRE_CLE_ERE = "173fae9c75229b154dcb2b6f582c8ad386a5ab14230db74694ca2dd6b57f711f"
MD5_PREMIERE_REMISE = "af382476b050533b5be73c3ac0b49e9c"  # contre 3e778fa0…
ARBRES_INCHANGES = ["m0", "m1", "m2", "m3", "m4", "m5", "m6", "m7", "tls13",
                    "demo", "terrain", "v06"]
ARBRES_BOUGES = ["m8"]  # erratum n° 9 : sys-06-reception.md seul (Entrée 187)
EMPREINTE_M8_ATTENDUE = "c444d73059af33ce0d61bf48ce8ac976d1e86a566574dcb4ef63a771f7b1875a"
NB_ARBRES = 13


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
        print(f"[ceremonie-rev2b] ÉCHEC D'ACCÈS au coffre /test : {e}", file=sys.stderr)
        return 2
    manquantes = [n for n in (NOM_REMISE, NOM_CLE) if n not in entrees]
    if manquantes:
        print(f"[ceremonie-rev2b] ÉCHEC : {manquantes} ABSENT(S) du coffre /test "
              f"({len(entrees)} entrées vues) — le dépôt du développeur "
              f"n'est pas constaté", file=sys.stderr)
        return 1
    md5_remise_drive = entrees[NOM_REMISE].get("md5Checksum")
    print(f"[ceremonie-rev2b] pièces trouvées dans /test : {NOM_REMISE} "
          f"(md5 {md5_remise_drive}) + {NOM_CLE}")
    if md5_remise_drive == MD5_PREMIERE_REMISE:
        print(f"[ceremonie-rev2b] ÉCHEC : signatures-I.txt au /test porte TOUJOURS "
              f"le md5 de la PREMIÈRE remise de la révision 2 ({MD5_PREMIERE_REMISE} "
              f"— contre 3e778fa0…, DÉJÀ INSTALLÉE au geste ffcdf19) : le coffre "
              f"n'a pas reçu la re-signature de la remise étendue (l'empreinte "
              f"à signer est c444d730… — le LISEZMOI de cérémonie révisé)",
              file=sys.stderr)
        return 1

    # ----------------------------------------------------------- rapatriement
    DOSSIER_CEREMONIE.mkdir(parents=True, exist_ok=True)
    md5_drive = {}
    for nom in (NOM_REMISE, NOM_CLE):
        cible = DOSSIER_CEREMONIE / nom
        md5_drive[nom] = entrees[nom].get("md5Checksum")
        md5_local = telecharger(entrees[nom]["id"], cible)
        if md5_local != md5_drive[nom]:
            print(f"[ceremonie-rev2b] ÉCHEC md5 {nom} : local {md5_local} != "
                  f"Drive {md5_drive[nom]}", file=sys.stderr)
            return 1
        print(f"[ceremonie-rev2b] rapatrié : {cible}  md5={md5_local}  "
              f"({cible.stat().st_size} o) — MATCH les métadonnées Drive")

    # ---------------------------------------------------------------- recoups
    echecs = []

    # (a) ancre de clé — la clé DÉPOSÉE PAR LE DÉVELOPPEUR == l'ancre
    cle_deposee = (DOSSIER_CEREMONIE / NOM_CLE).read_text().strip()
    if cle_deposee != ANCRE_CLE_ERE:
        echecs.append(f"CLÉ DÉPOSÉE divergente : cle-publique-I.txt du /test "
                      f"{cle_deposee[:16]}… != l'ancre des ères "
                      f"{ANCRE_CLE_ERE[:16]}… (« si cle-publique-I.txt "
                      f"diverge : ARRÊT » — mauvaise clé, la remise ne peut "
                      f"être installée)")
    else:
        print(f"[ceremonie-rev2b] ancre de clé : la clé déposée == "
              f"{ANCRE_CLE_ERE[:16]}… (l'ancre des ères — la continuité "
              f"« reelle » tenue, la règle d'or respectée : JAMAIS generer)")
    # l'ancre locale du dépôt doit elle aussi tenir
    cle_locale = (REPO / "v06" / "sceau-I" / "cle-publique-I.txt").read_text().strip()
    if cle_locale != ANCRE_CLE_ERE:
        echecs.append(f"ANCRE LOCALE divergente : v06/sceau-I/cle-publique-I.txt "
                      f"{cle_locale[:16]}… != {ANCRE_CLE_ERE[:16]}…")
    cle = bytes.fromhex(cle_deposee)

    # (b) la remise fraîche a-signer.txt (13 arbres — la charge de l'Entrée 187)
    a_signer = {}
    for ligne in (REPO / "v06" / "sceau-I" / "a-signer.txt").read_text().splitlines():
        if ligne.strip():
            arbre, balise, empreinte = ligne.split()
            a_signer[arbre] = (balise, empreinte)
    if len(a_signer) != NB_ARBRES:
        echecs.append(f"a-signer.txt : {len(a_signer)} arbres ({NB_ARBRES} attendus)")
    if a_signer.get("m8", ("?", ""))[1] != EMPREINTE_M8_ATTENDUE:
        echecs.append(f"a-signer.txt : l'empreinte m8 "
                      f"{a_signer.get('m8', ('?', '?'))[1][:16]}… "
                      f"!= l'attendue de la révision 2 étendue "
                      f"{EMPREINTE_M8_ATTENDUE[:16]}… (la remise fraîche de "
                      f"l'Entrée 187 a-t-elle été écrasée ?)")

    # (c) format de la remise déposée
    cible = DOSSIER_CEREMONIE / NOM_REMISE
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
    if len(remise) != NB_ARBRES:
        echecs.append(f"remise INCOMPLÈTE : {len(remise)}/{NB_ARBRES} arbres")
    print(f"[ceremonie-rev2b] format de la remise : {len(remise)}/{NB_ARBRES} lignes "
          f"valides (arbre balise signature-128hex)")

    # (e) le diff contrôlé : la remise étendue vs la PREMIÈRE remise de la
    # révision 2 — UNE ligne changée, LA m8, les DOUZE autres byte-identiques
    if PREMIERE_REMISE.is_file():
        premiere = {}
        for ligne in PREMIERE_REMISE.read_text().splitlines():
            if ligne.strip():
                arbre, _, sig = ligne.split()
                premiere[arbre] = sig
        bougees = sorted(a for a in remise if premiere.get(a) != remise[a])
        manquantes_p = sorted(set(premiere) - set(remise))
        if bougees == ["m8"] and not manquantes_p:
            print(f"[ceremonie-rev2b] diff contrôlé vs la première remise de la "
                  f"révision 2 : UNE ligne changée, LA m8 — les DOUZE autres "
                  f"byte-identiques (le précédent M9-(d) tenu sur les signatures)")
        else:
            echecs.append(f"diff contrôlé vs la première remise INATTENDU : "
                          f"lignes changées {bougees}, absentes {manquantes_p} "
                          f"(UNE seule ligne changée attendue : m8)")
    else:
        print(f"[ceremonie-rev2b] (première remise absente du labo : diff contrôlé "
              f"esquivé — non bloquant, le recoup D163 prime)")

    # (d) le recoup D163 + vérifications par arbre
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
        # empreinte vivante == a-signer (la remise fraîche de l'Entrée 187)
        r_a_signer = (a_signer.get(arbre, ("?", ""))[1] == empreinte_vivante)
        # vérification cryptographique contre la clé de l'ère
        r_crypto = sceau_I._verifier_ed25519(
            bytes.fromhex(empreinte_vivante), bytes.fromhex(sig), cle)
        # le recoup D163 : comparaison à la signature DÉPOSÉE au dépôt
        chemin_deposee = REPO / "v06" / "sceau-I" / "signatures" / f"{arbre}.txt"
        deposee = chemin_deposee.read_text().strip() if chemin_deposee.is_file() else None
        if arbre in ARBRES_INCHANGES:
            if deposee is None:
                note_ere = "déposée ABSENTE (inattendu)"
                echecs.append(f"{arbre} : signature déposée absente du dépôt")
            elif deposee == sig:
                note_ere = "IDENTIQUE à la déposée (== build 1.0.0)"
            else:
                note_ere = "DIVERGE de la déposée (clé neuve ou arbre bougé)"
                echecs.append(f"{arbre} : signature DIVERGENTE de la déposée — "
                              f"la clé de l'ère n'a vraisemblablement pas été "
                              f"réutilisée (règle d'or : JAMAIS « generer »)")
        else:  # m8 : révision 2 étendue — l'empreinte a changé ENCORE
            if deposee is None:
                note_ere = "déposée ABSENTE (inattendu)"
                echecs.append("m8 : signature déposée absente du dépôt")
            elif deposee == sig:
                note_ere = "IDENTIQUE à la déposée (inattendu : m8 a changé !)"
                echecs.append("m8 : signature IDENTIQUE à la déposée (la première "
                              "signature de la révision 2, contre 3e778fa0…) "
                              "alors que l'erratum n° 9 a fait évoluer l'arbre "
                              "(empreinte bougée 3e778fa0… → c444d730…)")
            elif empreinte_vivante == EMPREINTE_M8_ATTENDUE:
                note_ere = "RE-SIGNÉ (rév. 2 étendue : sys-05 + sys-06)"
            else:
                note_ere = "diverge de la déposée (empreinte inattendue)"
                echecs.append("m8 : empreinte vivante inattendue")
        if not r_a_signer:
            echecs.append(f"{arbre} : empreinte vivante {empreinte_vivante[:16]}… "
                          f"!= a-signer.txt {a_signer.get(arbre, ('?', '?'))[1][:16]}…")
        if not r_crypto:
            echecs.append(f"{arbre} : signature Ed25519 INVÉRIFIABLE contre "
                          f"la clé {cle_deposee[:16]}…")
        ok = r_a_signer and r_crypto
        verts += 1 if ok else 0
        print(f"{arbre:<9} {sceau_I.ARBRES[arbre][1]:<22} "
              f"{'OUI' if r_a_signer else 'NON':<17} "
              f"{'VERT' if r_crypto else 'ÉCHEC':<8} {note_ere}")
    print()

    # ---------------------------------------------------------------- verdict
    if echecs:
        print(f"[ceremonie-rev2b] RECOUPE EN ÉCHEC — {len(echecs)} faute(s) nommée(s), "
              f"RIEN n'est déposé :")
        for e in echecs:
            print(f"  ✗ {e}")
        return 1
    print(f"[ceremonie-rev2b] RECOUPE INTÉGRAL VERT — {verts}/{NB_ARBRES} arbres : la "
          f"remise étendue du développeur vérifie sur pièces (clé de l'ère "
          f"{cle_deposee[:16]}…, les DOUZE inchangés == les signatures déposées "
          f"== build 1.0.0, m8 RE-SIGNÉ contre c444d730…, empreintes == "
          f"a-signer.txt {NB_ARBRES}/{NB_ARBRES}, diff vs première remise : "
          f"la ligne m8 seule).")
    print("[ceremonie-rev2b] geste suivant (canonique) : "
          "python3 v06/sceau_I.py deposer "
          "download/ceremonie-revision2-etendue/signatures-I.txt "
          "--cle download/ceremonie-revision2-etendue/cle-publique-I.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
