#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — Rapatriement + recoup de la CÉRÉMONIE D'ÈRE DU TGN :
LA REMISE DES QUATORZE ARBRES (sceau I, le quatorzième arbre —
re-signature m0 + loupe).

Le développeur a exécuté la signature hors-ligne de la remise de l'ère du
TGN (l'Entrée 200 : la dette du QUATORZIÈME ARBRE, nommée à la naissance
de la couche I — D171, règle 8 —, est ÉCHUE AU BUILD ; les quatre
chantiers de notation accomplis (D172–D175 : les 18 blocs
NOTÉS-MESURÉS-PROUVÉS), la couche I FINALE, aucun octet de build ne naît
avant la signature. DEUX états exigent la clé hors-ligne : l'arbre m0 a
DIVERGÉ — LE REGISTRE FIGÉ ÉTENDU au domaine `loupe` (M10), empreinte à
signer 667fb5ae… — et l'arbre loupe est NEUF, jamais signé : les 19
fichiers (le README + les 18 spécifications), empreinte à signer
59e4871a…) et re-déposé signatures-I.txt + cle-publique-I.txt dans le
coffre /test du Drive (l'annonce du développeur : « signatures déposées
dans le dossier /test du drive »).

Ce script (LECTURE SEULE sur le dépôt v06/) :
  1. sonde /test par le canal OAuth du relais ;
  2. rapatrie signatures-I.txt ET cle-publique-I.txt vers
     download/ceremonie-tgn/ avec contrôle md5 APRÈS écriture contre les
     métadonnées Drive — et REFUSE les remises PÉRIMÉES nommées (md5
     62c43222… la remise du build 1.0.0 ; md5 af382476… la seconde remise
     de la révision 2 étendue ; TOUTE remise sans loupe = l'ère close,
     re-déposer l'ancienne n'est pas re-signer) ;
  3. recoupe SUR PIÈCES avant tout dépôt :
       - l'ANCRE DE CLÉ : la clé déposée par le développeur ==
         173fae9c… (l'ancre de toutes les ères — « si cle-publique-I.txt
         diverge : ARRÊT », la règle d'or : JAMAIS « generer ») ;
       - format : QUATORZE lignes « arbre balise signature(128 hex) »,
         balises == la table canonique du dépôt à QUATORZE arbres (la
         rotation couvre TOUS les arbres, spec § 5 — loupe à sa place
         d'ère après tls13.1) ;
       - LE RECOUP D163 (rejoint une SIXIÈME fois) : les DOUZE arbres
         inchangés (m1..m8, tls13, demo, terrain, v06) portent les MÊMES
         signatures que celles DÉPOSÉES au dépôt (Ed25519 déterministe :
         la clé du 04/11 réutilisée redonne les signatures déposées —
         une divergence nomme une clé neuve ou un arbre bougé) ;
       - m0 RE-SIGNÉ (le registre figé étendu au domaine `loupe` —
         l'extension promise à cette cérémonie, D171/D168) : la signature
         DOIT diverger de la déposée (c71bf747… : le registre de l'ère
         close) ET vérifier Ed25519 contre l'empreinte vivante
         667fb5ae… ;
       - loupe L'ARBRE NEUF (le quatorzième, jamais signé avant cette
         cérémonie) : AUCUNE signature déposée n'existe, l'empreinte
         vivante == 59e4871a…, la signature VÉRIFIE Ed25519 ;
       - les empreintes vivantes des QUATORZE arbres == a-signer.txt
         (la remise fraîche régénérée à l'Entrée 200, AU GESTE de la
         cérémonie — D168 rejouée) ;
       - chaque signature de la remise VÉRIFIÉE Ed25519 contre la clé
         publique sur l'empreinte du manifeste VIVANT (14/14) ;
       - LE DIFF CONTRÔLÉ vs l'ère close (les TREIZE signatures déposées
         au dépôt) : m0 changée + loupe AJOUTÉE, les DOUZE autres
         byte-identiques (le précédent M9-(d) tenu sur la remise, tenu
         sur les signatures).

AUCUNE écriture dans v06/ : le dépôt canonique (sceau_I.py deposer) est
le geste suivant, explicite. Ce script prépare le verdict ; il ne signe
rien et n'installe rien (la cérémonie appartient au développeur, D87).

Usage : python3 scripts/rapatrier_ceremonie_tgn.py
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

DOSSIER_CEREMONIE = REPO / "download" / "ceremonie-tgn"
NOM_REMISE = "signatures-I.txt"
NOM_CLE = "cle-publique-I.txt"
ANCRE_CLE_ERE = "173fae9c75229b154dcb2b6f582c8ad386a5ab14230db74694ca2dd6b57f711f"
# Remises PÉRIMÉES nommées (l'ère close — re-déposer l'ancienne n'est pas
# re-signer) :
MD5_REMISE_BUILD_100 = "62c4322263f733d6b320dcbd36d548bc"   # build 1.0.0
MD5_REMISE_REV2_ETENDUE = "af382476b050533b5be73c3ac0b49e9c"  # rév. 2 étendue
ARBRES_INCHANGES = ["m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "tls13",
                    "demo", "terrain", "v06"]
ARBRE_RESIGNE = "m0"       # le registre figé étendu au domaine loupe (D171/D168)
ARBRE_NEUF = "loupe"       # le quatorzième arbre, jamais signé avant
EMPREINTE_M0_ATTENDUE = "667fb5ae36e4ab3c5dcfd4899fc680fd5b2393d2cdc6ad32241be14b89d9f920"
EMPREINTE_LOUPE_ATTENDUE = "59e4871ab5b47623be8aad0d6633abf7a1f8b64acd6f87f4f87e2003aa5d8520"
NB_ARBRES = 14


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
        print(f"[ceremonie-tgn] ÉCHEC D'ACCÈS au coffre /test : {e}", file=sys.stderr)
        return 2
    manquantes = [n for n in (NOM_REMISE, NOM_CLE) if n not in entrees]
    if manquantes:
        print(f"[ceremonie-tgn] ÉCHEC : {manquantes} ABSENT(S) du coffre /test "
              f"({len(entrees)} entrées vues) — le dépôt du développeur "
              f"n'est pas constaté", file=sys.stderr)
        return 1
    md5_remise_drive = entrees[NOM_REMISE].get("md5Checksum")
    print(f"[ceremonie-tgn] pièces trouvées dans /test : {NOM_REMISE} "
          f"(md5 {md5_remise_drive}) + {NOM_CLE}")
    if md5_remise_drive == MD5_REMISE_BUILD_100:
        print(f"[ceremonie-tgn] ÉCHEC : signatures-I.txt au /test porte le md5 "
              f"de la remise du BUILD 1.0.0 ({MD5_REMISE_BUILD_100} — "
              f"DÉJÀ INSTALLÉE à l'ère close) : le coffre n'a pas reçu la "
              f"signature de l'ère du TGN (la remise à signer compte "
              f"QUATORZE arbres, dont m0 re-signé au registre étendu "
              f"667fb5ae… et l'arbre loupe neuf 59e4871a…)", file=sys.stderr)
        return 1
    if md5_remise_drive == MD5_REMISE_REV2_ETENDUE:
        print(f"[ceremonie-tgn] ÉCHEC : signatures-I.txt au /test porte le md5 "
              f"de la SECONDE remise de la révision 2 étendue "
              f"({MD5_REMISE_REV2_ETENDUE} — contre c444d730…, DÉJÀ "
              f"INSTALLÉE) : le coffre n'a pas reçu la signature de l'ère "
              f"du TGN (QUATORZE arbres attendus, dont m0 re-signé et "
              f"l'arbre loupe neuf)", file=sys.stderr)
        return 1

    # ----------------------------------------------------------- rapatriement
    DOSSIER_CEREMONIE.mkdir(parents=True, exist_ok=True)
    md5_drive = {}
    for nom in (NOM_REMISE, NOM_CLE):
        cible = DOSSIER_CEREMONIE / nom
        md5_drive[nom] = entrees[nom].get("md5Checksum")
        md5_local = telecharger(entrees[nom]["id"], cible)
        if md5_local != md5_drive[nom]:
            print(f"[ceremonie-tgn] ÉCHEC md5 {nom} : local {md5_local} != "
                  f"Drive {md5_drive[nom]}", file=sys.stderr)
            return 1
        print(f"[ceremonie-tgn] rapatrié : {cible}  md5={md5_local}  "
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
        print(f"[ceremonie-tgn] ancre de clé : la clé déposée == "
              f"{ANCRE_CLE_ERE[:16]}… (l'ancre des ères — la continuité "
              f"« reelle » tenue, la règle d'or respectée : JAMAIS generer)")
    # l'ancre locale du dépôt doit elle aussi tenir
    cle_locale = (REPO / "v06" / "sceau-I" / "cle-publique-I.txt").read_text().strip()
    if cle_locale != ANCRE_CLE_ERE:
        echecs.append(f"ANCRE LOCALE divergente : v06/sceau-I/cle-publique-I.txt "
                      f"{cle_locale[:16]}… != {ANCRE_CLE_ERE[:16]}…")
    cle = bytes.fromhex(cle_deposee)

    # (b) la remise fraîche a-signer.txt (QUATORZE arbres — la charge de
    # l'Entrée 200, régénérée AU GESTE de la cérémonie)
    a_signer = {}
    for ligne in (REPO / "v06" / "sceau-I" / "a-signer.txt").read_text().splitlines():
        if ligne.strip():
            arbre, balise, empreinte = ligne.split()
            a_signer[arbre] = (balise, empreinte)
    if len(a_signer) != NB_ARBRES:
        echecs.append(f"a-signer.txt : {len(a_signer)} arbres ({NB_ARBRES} attendus)")
    if a_signer.get(ARBRE_RESIGNE, ("?", ""))[1] != EMPREINTE_M0_ATTENDUE:
        echecs.append(f"a-signer.txt : l'empreinte m0 "
                      f"{a_signer.get(ARBRE_RESIGNE, ('?', '?'))[1][:16]}… "
                      f"!= l'attendue du REGISTRE ÉTENDU "
                      f"{EMPREINTE_M0_ATTENDUE[:16]}… (la remise fraîche de "
                      f"l'Entrée 200 a-t-elle été écrasée ?)")
    if a_signer.get(ARBRE_NEUF, ("?", ""))[1] != EMPREINTE_LOUPE_ATTENDUE:
        echecs.append(f"a-signer.txt : l'empreinte loupe "
                      f"{a_signer.get(ARBRE_NEUF, ('?', '?'))[1][:16]}… "
                      f"!= l'attendue de L'ARBRE NEUF "
                      f"{EMPREINTE_LOUPE_ATTENDUE[:16]}… (la remise fraîche de "
                      f"l'Entrée 200 a-t-elle été écrasée ?)")

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
    if ARBRE_NEUF not in remise and len(remise) == 13:
        echecs.append(f"remise PÉRIMÉE de l'ère close : TREIZE lignes SANS loupe "
                      f"(l'ère M9/close — re-déposer l'ancienne n'est pas "
                      f"re-signer : la remise de l'ère du TGN compte QUATORZE "
                      f"arbres, loupe à sa place d'ère après tls13.1)")
    if len(remise) != NB_ARBRES:
        echecs.append(f"remise INCOMPLÈTE : {len(remise)}/{NB_ARBRES} arbres")
    print(f"[ceremonie-tgn] format de la remise : {len(remise)}/{NB_ARBRES} lignes "
          f"valides (arbre balise signature-128hex)")

    # (d) le diff contrôlé vs l'ère close : les signatures DÉPOSÉES au dépôt
    # (TREIZE arbres) — m0 changée + loupe AJOUTÉE, les DOUZE autres
    # byte-identiques
    deposees = {}
    for chemin in (REPO / "v06" / "sceau-I" / "signatures").glob("*.txt"):
        deposees[chemin.stem] = chemin.read_text().strip()
    bougees = sorted(a for a in deposees if a in remise and deposees[a] != remise[a])
    ajoutees = sorted(set(remise) - set(deposees))
    if bougees == [ARBRE_RESIGNE] and ajoutees == [ARBRE_NEUF]:
        print(f"[ceremonie-tgn] diff contrôlé vs l'ère close (les TRÉIZE "
              f"signatures déposées) : UNE ligne changée, LA m0 (le registre "
              f"étendu) + UNE ligne AJOUTÉE, LOUPE (le quatorzième arbre) — "
              f"les DOUZE autres byte-identiques (le précédent M9-(d) tenu "
              f"sur les signatures)")
    else:
        echecs.append(f"diff contrôlé vs l'ère close INATTENDU : lignes "
                      f"changées {bougees}, ajoutées {ajoutees} (attendu : "
                      f"m0 changée seule + loupe ajoutée seule)")

    # (e) le recoup D163 + vérifications par arbre
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
        # empreinte vivante == a-signer (la remise fraîche de l'Entrée 200)
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
                note_ere = "IDENTIQUE à la déposée (== l'ère close)"
            else:
                note_ere = "DIVERGE de la déposée (clé neuve ou arbre bougé)"
                echecs.append(f"{arbre} : signature DIVERGENTE de la déposée — "
                              f"la clé de l'ère n'a vraisemblablement pas été "
                              f"réutilisée (règle d'or : JAMAIS « generer »)")
        elif arbre == ARBRE_RESIGNE:  # m0 : le registre figé ÉTENDU
            if deposee is None:
                note_ere = "déposée ABSENTE (inattendu)"
                echecs.append("m0 : signature déposée absente du dépôt")
            elif deposee == sig:
                note_ere = "IDENTIQUE à la déposée (inattendu : m0 a changé !)"
                echecs.append("m0 : signature IDENTIQUE à la déposée (celle de "
                              "l'ère close, contre l'ancien registre) alors "
                              "que le REGISTRE FIGÉ a été ÉTENDU au domaine "
                              "`loupe` (empreinte bougée → 667fb5ae…)")
            elif empreinte_vivante == EMPREINTE_M0_ATTENDUE:
                note_ere = "RE-SIGNÉ (registre étendu : loupe (M10) au registre)"
            else:
                note_ere = "diverge de la déposée (empreinte inattendue)"
                echecs.append("m0 : empreinte vivante inattendue")
        else:  # loupe : l'arbre NEUF, jamais signé avant cette cérémonie
            if deposee is not None:
                note_ere = "déposée EXISTANTE (inattendu : jamais signé !)"
                echecs.append("loupe : signature déposée existante au dépôt "
                              "(l'arbre n'a JAMAIS été signé avant cette "
                              "cérémonie — un état antérieur incohérent)")
            elif empreinte_vivante == EMPREINTE_LOUPE_ATTENDUE:
                note_ere = "L'ARBRE NEUF signé (loupe.1 — le quatorzième)"
            else:
                note_ere = "empreinte inattendue"
                echecs.append("loupe : empreinte vivante inattendue")
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
        print(f"[ceremonie-tgn] RECOUPE EN ÉCHEC — {len(echecs)} faute(s) nommée(s), "
              f"RIEN n'est déposé :")
        for e in echecs:
            print(f"  ✗ {e}")
        return 1
    print(f"[ceremonie-tgn] RECOUPE INTÉGRAL VERT — {verts}/{NB_ARBRES} arbres : la "
          f"remise de l'ère du TGN du développeur vérifie sur pièces (clé de "
          f"l'ère {cle_deposee[:16]}…, les DOUZE inchangés == les signatures "
          f"déposées == l'ère close, m0 RE-SIGNÉ contre 667fb5ae… le registre "
          f"étendu, LOUPE L'ARBRE NEUF signé contre 59e4871a…, empreintes == "
          f"a-signer.txt {NB_ARBRES}/{NB_ARBRES}, diff vs l'ère close : "
          f"la ligne m0 changée + la ligne loupe ajoutée).")
    print("[ceremonie-tgn] geste suivant (canonique) : "
          "python3 v06/sceau_I.py deposer "
          "download/ceremonie-tgn/signatures-I.txt "
          "--cle download/ceremonie-tgn/cle-publique-I.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
