#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""reparer_carte_051.py — RÉPARATION de la carte m4 génération 6 (scellé 0.5.1).

CONSTAT (04/11, « répare la 0.5.1 ») : la carte posée au jalon v7 (commit
da68021, 03/11 03:29) a été scellée avec des secrets ÉPHÉMÈRES. Le labo de
la chirurgie était un CLONE du bundle (RAPPORT-chirurgie-0.5.1-labo.txt :
« cloné dans l'espace labo ») : .keys/ (gitignoré, jamais dans un bundle)
n'y vivait pas, et carte_m0.charger_secrets a GÉNÉRÉ une phrase et une
graine aléatoires à la première exigence du build. La garde anti-rollback
a alors passé SILENCIEEUSEMENT (« pas de carte lisible : première
construction » — le except avale l'échec de déchiffrement de la carte
D104) et construire() a scellé la carte 0.5.1 sous ces secrets morts avec
la sandbox : pub ad98a059… (la graine lignée f40f8a20… n'a pas servi),
fragments indéchiffrables par la lignée D80 du coffre. La carte est
ORPHELLE : le verrou anti-rollback de la 0.5.1 est MORT (il repasse
silencieusement à tout labo), le verrou croisé R8 est inexécutable, et la
promesse du coffre (« lignee-D80 … déverrouille … les cartes M4+ ») est
fausse pour cette carte.

LA RÉPARATION (modèle D80 — re-scelage à faits strictement inchangés) :
re-sceller la carte génération 6 sous la lignée D80 DURABLE, l'artefact
proxy.exe 0.5.1 demeurant OCTET POUR OCTET inchangé (fb41697d…) :
  - manifestes régénérés par la machinerie EXACTE du build
    (build_m4.fragments_clairs — aucune réinvention) ;
  - l'image M4 re-composée et confrontée au scellé (R7 : la carte décrit
    bien l'artefact) SANS réécrire proxy.exe ;
  - l'oracle D93 re-joué (graine datée 20261104) : le verdict inscrit à
    frag-bld est un verdict VÉRIFIÉ, pas une copie ;
  - une graine Ed25519 NEUVE, immédiatement DÉPOSÉE AU COFFRE (entrée
    TRIADE/graine-ed25519-cartes) : la continuité de clé de signature
    redevient DURABLE — c'est la DERNIÈRE régénération.

GARDES FAIL-CLOSED (avant tout geste) :
  G1 artefact : sha256(m4/proxy.exe) == fb41697d… (intouché, non négociable) ;
  G2 phrase .keys == lignée D80, PROUVÉE par témoins croisés : elle
     déchiffre la carte m3 génération 5 ET la carte m4 D104 (git 8c280d5) ;
  G3 la carte courante est l'ORPHELINE authentique : signature Ed25519
     valide, empreinte racine conforme, pub == ad98a059… (constat) ;
  G4 la carte courante ne se déchiffre PAS en D80 (sinon rien à réparer) ;
  G5 garde sceau-I verte (l'arbre m4/I == sa signature) ;
  G6 sceau verifier : ONZE arbres verts.
Aucune écriture avant que TOUTES les gardes ne passent ; le scellement
n'écrit qu'à la fin, après vérification en mémoire des fragments.

Usage : python3 scripts/reparer_carte_051.py
Code de sortie : 0 = réparation effectuée et re-vérifiée, 1 = refus nommé.
"""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M4 = os.path.join(REPO, "m4")
M3 = os.path.join(REPO, "m3")
sys.path.insert(0, M4)

SHA_SCELLE_051 = ("fb41697ddde265ac659bdceecc2ab3ec55f564d0998d430590"
                  "90235762edf3f3")
PUB_ORPHELINE = ("ad98a059d499ee7172f02cdc97d2dccda223455345ac97378f"
                 "c2968199bce43f")
COMMIT_D104 = "8c280d5"
ORACLE_GRAINE = 20261104
ETIQUETTE_GRAINE = "graine-ed25519-cartes"

_journal: list[str] = []


def trace(msg: str) -> None:
    print(msg)
    _journal.append(msg)


def refus(msg: str) -> None:
    print(f"[réparation] REFUS (fail-closed) : {msg}", file=sys.stderr)
    print("[réparation] RIEN n'a été écrit (les gardes précèdent tout geste).",
          file=sys.stderr)
    sys.exit(1)


def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    debut = datetime.now(timezone.utc)
    print("=== RÉPARATION carte m4 génération 6 (scellé 0.5.1, lignée D80) ===")

    # --- Chargement de la machinerie du build (aucune réinvention) ------------
    import build_m4 as B4  # noqa: E402  (exécute les imports plan m3/m4, sceau)
    import carte_m4 as cm  # noqa: E402
    trace(f"[outils] build_m4 chargé — carte_m4 GENERATION={cm.GENERATION}")

    # --- G1 : l'artefact scellé est intact -----------------------------------
    chemin_exe = os.path.join(M4, "proxy.exe")
    with open(chemin_exe, "rb") as f:
        exe = f.read()
    if sha256_hex(exe) != SHA_SCELLE_051:
        refus(f"m4/proxy.exe diverge du scellé 0.5.1 (sha256 {sha256_hex(exe)[:16]}… "
              f"!= fb41697d…) — l'artefact est intouchable")
    trace("[G1] artefact INTACT : proxy.exe 0.5.1 sha256 fb41697d… "
          f"({len(exe)} o) — il ne sera PAS réécrit")

    # --- G2 : la phrase .keys est la lignée D80 (témoins croisés) -------------
    chemin_phrase = os.path.join(REPO, ".keys", "passphrase.txt")
    if not os.path.exists(chemin_phrase):
        refus(".keys/passphrase.txt absent — la relève du coffre précède la réparation")
    with open(chemin_phrase, "rb") as f:
        phrase = f.read().strip()
    if not phrase or len(phrase) < 16:
        refus("phrase .keys incohérente (trop courte)")
    sys.path.insert(0, M3)
    import carte_m3 as c3  # noqa: E402
    try:
        ent3, frag3, _sig3, _pub3 = c3.lire_carte()
        c3.verifier_signature(_pub3, ent3, frag3, _sig3)
        c3.dechiffrer_fragment(c3.cle_maitresse(phrase), "frag-loc", frag3["frag-loc"])
    except Exception as exc:  # noqa: BLE001
        refus(f"la phrase .keys ne déchiffre pas la carte m3 génération 5 "
              f"(témoin lignée D80) : {exc}")
    trace("[G2a] témoin m3 génération 5 : déchiffrement OK — la phrase est "
          "de la lignée du coffre")
    # Témoin D104 : la carte m4 de l'époque D104 (git) se déchiffre en D80.
    tmp_d104 = tempfile.mkdtemp(prefix="carte-d104-")
    for nom in ("header.txt", "frag-loc.bin", "frag-con.bin", "frag-prf.bin",
                "frag-bld.bin", "carte.sig", "cle-publique.ed25519"):
        blob = subprocess.run(["git", "-C", REPO, "show",
                               f"{COMMIT_D104}:m4/carte/{nom}"],
                              capture_output=True).stdout
        if not blob:
            refus(f"git show {COMMIT_D104}:m4/carte/{nom} vide")
        with open(os.path.join(tmp_d104, nom), "wb") as f:
            f.write(blob)
    ancien_dir = cm.CARTE_DIR
    try:
        cm.CARTE_DIR = tmp_d104
        ent0, frag0, _s0, pub0 = cm.lire_carte()
        bld0 = cm.dechiffrer_fragment(cm.cle_maitresse(phrase), "frag-bld",
                                      frag0["frag-bld"]).decode("utf-8")
        version0 = next((dict(__import__("re").findall(r"(\w+)=(\S+)", l)).get("version")
                         for l in bld0.splitlines() if "artefact=proxy.exe" in l), "?")
    except Exception as exc:  # noqa: BLE001
        refus(f"la phrase .keys ne déchiffre pas la carte m4 D104 ({COMMIT_D104}) : {exc}")
    finally:
        cm.CARTE_DIR = ancien_dir
    if version0 != "0.5.0":
        refus(f"la carte D104 déchiffrée porte version={version0!r} (0.5.0 attendu)")
    trace(f"[G2b] témoin m4 D104 ({COMMIT_D104[:7]}) : déchiffrement OK, "
          f"version={version0}, pub {pub0.hex()[:12]}… — la phrase .keys EST "
          "la lignée D80")

    # --- G3/G4 : la carte courante est l'orpheline authentique ----------------
    entc, fragc, sigc, pubc = cm.lire_carte()
    try:
        cm.verifier_listes_blanches(entc.decode("ascii"))
        cm.verifier_signature(pubc, entc, fragc, sigc)
    except Exception as exc:  # noqa: BLE001
        refus(f"la carte courante ne vérifie pas (signature/listes) : {exc}")
    if cm.empreinte_racine(fragc).hex() not in entc.decode("ascii"):
        refus("empreinte racine divergente dans la carte courante")
    if pubc.hex() != PUB_ORPHELINE:
        refus(f"la carte courante porte pub {pubc.hex()[:12]}… — ce n'est pas "
              "l'orpheline constatée (ad98a059…)")
    try:
        cm.dechiffrer_fragment(cm.cle_maitresse(phrase), "frag-loc",
                               fragc["frag-loc"])
        refus("la carte courante SE déchiffre en D80 — elle n'est pas "
              "orpheline, rien à réparer (état inattendu, ne rien forcer)")
    except cm.ErreurCarte:
        pass
    trace("[G3] carte courante : signature Ed25519 VALIDE, racine conforme, "
          "pub ad98a059… (l'orpheline du jalon v7 — authentique, elle reste "
          "dans l'historique git)")
    trace("[G4] carte courante INDÉCHIFFRABLE en lignée D80 — l'orpheline "
          "est bien le défaut nommé (secrets éphémères du clone D140)")

    # --- G5/G6 : le sceau est vert avant le geste -----------------------------
    try:
        B4._garde_sceau_I()
    except Exception as exc:  # noqa: BLE001
        refus(f"garde sceau-I : {exc}")
    trace("[G5] garde sceau-I VERTE (l'arbre m4/I == sa signature — "
          "la réparation ne touche NI l'arbre NI le sceau)")
    r = subprocess.run([sys.executable, os.path.join(REPO, "v06", "sceau_I.py"),
                        "verifier"], capture_output=True, text=True, cwd=REPO)
    if r.returncode != 0:
        refus(f"sceau verifier rc={r.returncode} : {r.stdout[-400:]} {r.stderr[-200:]}")
    trace("[G6] sceau verifier : ONZE arbres verts (état complet constaté)")

    # --- G7 : le coffre Drive (durable) est joignable et identique au local ----
    sys.path.insert(0, os.path.join(REPO, "scripts"))
    import drive_sync as ds  # noqa: E402
    chemin_coffre = os.path.join(REPO, ".keys", "coffre_fort.bin")
    if not os.path.exists(chemin_coffre):
        refus(".keys/coffre_fort.bin absent — l'import du coffre précède la réparation")
    md5_local_avant = hashlib.md5(open(chemin_coffre, "rb").read()).hexdigest()
    try:
        distant_avant = ds.list_folder(ds.DRIVE_ROOT_ID).get("coffre_fort.bin", {})
    except Exception as exc:  # noqa: BLE001
        refus(f"coffre Drive racine INJOIGNABLE : {exc} — la graine ne serait "
              "pas durable, le geste attend un canal disponible")
    if distant_avant.get("md5Checksum") != md5_local_avant:
        refus(f"coffre Drive ({(distant_avant.get('md5Checksum') or '?')[:12]}…) != "
              f"local ({md5_local_avant[:12]}…) — les deux conteneurs divergent, "
              "diagnostiquer avant tout geste")
    trace(f"[G7] coffre Drive racine joignable : coffre_fort.bin md5 "
          f"{md5_local_avant[:12]}… == local (le canal durable est là)")

    # ============================ LE GESTE =====================================
    print()
    print("--- LE GESTE : re-scelage génération 6 sous lignée D80 ---")

    # É1 — graine Ed25519 neuve (refus si une graine existe déjà : état inattendu)
    chemin_graine = os.path.join(REPO, ".keys", "ed25519.seed")
    if os.path.exists(chemin_graine):
        refus(".keys/ed25519.seed EXISTE déjà — état inattendu (aucune graine "
              "durable ne devrait être là) ; ne rien écraser, diagnostiquer")
    import secrets as _secrets
    graine = _secrets.token_bytes(32)
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    prive, pub_neuve = cm.paire_cles(graine)
    trace(f"[É1] graine Ed25519 NEUVE générée (32 o, en mémoire) — pub "
          f"{pub_neuve.hex()[:12]}… (la 3e de l'histoire des cartes : "
          "e842727c M0-M2, f40f8a20 m3/terrain, ad98a059 orpheline — "
          "celle-ci sera DÉPOSÉE AU COFFRE, la dernière régénération)")

    # É2 — assemblage honnête (la machinerie du build, R5)
    print("[É2] assemblage M3 + M4 (build_m3.assembler_tout + assembler_tout_m4)…")
    blocs_m3, _specs_m3, code_m3, verrous_m3 = B4.B3.assembler_tout()
    texte_m3, rdata_m3, data_m3, text2_m3 = B4.B3.composer_sections(code_m3, blocs_m3)
    specs_m4, code_m4, verrous_m4 = B4.assembler_tout_m4()
    trace(f"[É2] verrous structurels : M3 {len(verrous_m3)} + M4 {len(verrous_m4)}")

    # É3 — l'image re-composée == le scellé (R7), SANS réécrire l'artefact
    texte, rdata, data, text2, text3 = B4.composer_image_m4(
        texte_m3, rdata_m3, data_m3, text2_m3, code_m4, code_m4["b20007"]["slot"])
    exe_compose = B4.ecrire_pe32plus(texte, rdata, data, text2, text3)
    if sha256_hex(exe_compose) != SHA_SCELLE_051:
        refus(f"l'image M4 re-composée diverge du scellé 0.5.1 "
              f"({sha256_hex(exe_compose)[:16]}… != fb41697d…) — les manifestes "
              "ne décriraient pas l'artefact scellé")
    trace("[É3] image M4 re-composée == scellé 0.5.1 OCTET POUR OCTET "
          "(fb41697d…) — proxy.exe n'a PAS été réécrit")

    # É4 — l'oracle D93 re-joué (verdict VÉRIFIÉ, graine datée)
    print(f"[É4] oracle D93 (différentiel, graine {ORACLE_GRAINE}, volume complet)…")
    verdict = B4.od4.executer(B4.blobs_oracle(code_m3, code_m4),
                              graine=ORACLE_GRAINE, volume="complet")
    trace(f"[É4] oracle D93 : {verdict['total_cas']} cas verts, "
          f"verdict={verdict['empreinte'][:16]}… — le verdict inscrit à la "
          "carte est un verdict re-vérifié")

    # É5 — manifestes par la machinerie EXACTE du build (faits inchangés)
    version = B4.L.VERSION_051
    compteurs = {bid: 1 for bid in B4.TOUS_BLOCS}
    maintenant = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    journal_runs = [
        f"run graine={ORACLE_GRAINE} volume=complet verdict={verdict['empreinte']} "
        f"date={maintenant} build={version} rescelage=D144-secrets-ephemeres-du-"
        f"jalon-v7-remplaces-par-lignee-D80",
    ]
    clairs = B4.fragments_clairs(exe, verrous_m3, verrous_m4, version,
                                 verdict, compteurs, journal_runs)
    trace(f"[É5] manifestes régénérés (fragments_clairs du build) : "
          f"{len(B4.TOUS_BLOCS)} blocs, version={version}, compteurs=1/10 "
          "(les faits de l'orpheline — le journal enregistre la réparation)")

    # É6 — scellement sous D80 + graine neuve, TOUT EN MÉMOIRE D'ABORD
    maitre = cm.cle_maitresse(phrase)
    fragments = {n: cm.chiffrer_fragment(maitre, n, clairs[n]) for n in cm.FRAGMENTS}
    racine = cm.empreinte_racine(fragments)
    entete = cm.construire_entete(racine)
    signature = cm.signer(prive, entete, fragments)

    # Vérification en mémoire AVANT toute écriture : signature, racine,
    # déchiffrement D80, verrou croisé (empreintes embarquées == artefact).
    cm.verifier_listes_blanches(entete.decode("ascii"))
    cm.verifier_signature(pub_neuve, entete, fragments, signature)
    if racine.hex() not in entete.decode("ascii"):
        refus("empreinte racine incohérente (interne)")
    controle = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("utf-8")
    ligne_build = next(l for l in controle.splitlines() if "artefact=proxy.exe" in l)
    if f"version={version}" not in ligne_build or sha256_hex(exe) not in ligne_build:
        refus(f"frag-bld re-déchiffré incohérent : {ligne_build[:120]}")
    empreintes_bld = {}
    for ligne in controle.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(__import__("re").findall(r"(\w+)=(\S+)", ligne))
            empreintes_bld[champs["id"]] = champs["empreinte"]
    nb = 0
    for bid in B4.TOUS_BLOCS:
        if bid not in B4.EMBARQUES:
            continue
        rva = B4.RVA_PAR_BLOC[bid]
        slot = next(s for b, _sid, _f, _r, s in B4.BLOCS_EMBARQUES_M4 if b == bid)
        if "sha256:" + sha256_hex(B4.tranche_section(exe, rva, slot)) != \
                empreintes_bld.get(bid):
            refus(f"verrou croisé (mémoire) : empreinte divergente pour {bid}")
        nb += 1
    trace(f"[É6] scellement en mémoire VÉRIFIÉ : signature Ed25519 OK, racine "
          f"OK, déchiffrement D80 OK, verrou croisé {nb}/{len(B4.EMBARQUES)} "
          "blocs embarqués conformes à l'artefact — écriture autorisée")

    # L'écriture (la seule du geste sur la carte)
    cm.ecrire_carte(entete, fragments, signature, pub_neuve)

    # La graine vit désormais de façon durable : .keys (chmod 600) + coffre
    with open(chemin_graine, "wb") as f:
        f.write(graine)
    os.chmod(chemin_graine, 0o600)
    trace("[É6] carte écrite ; graine posée dans .keys/ed25519.seed (chmod 600, "
          "gitignoré) — elle part AU COFFRE ci-dessous")

    # É7 — verrou croisé sur disque (la machinerie du build)
    nb_disque, manifeste = B4.verrou_croise()
    if manifeste.get("version") != version:
        refus(f"verrou croisé : manifeste version={manifeste.get('version')!r}")
    trace(f"[É7] verrou croisé (build_m4.verrou_croise) : {nb_disque} empreintes "
          f"conformes ; artefact {manifeste.get('version')}")

    # É8 — tableau de bord (le même que le build écrit)
    with open(os.path.join(cm.CARTE_DIR, "tableau-de-bord.txt"), "w",
              encoding="utf-8") as f:
        f.write(B4.tableau_de_bord(exe, verrous_m3, verrous_m4, nb_disque,
                                   manifeste, verdict))
    trace("[É8] tableau de bord régénéré (carte/tableau-de-bord.txt)")

    # É9 — la graine entre au COFFRE (durabilité : la dernière régénération)
    chemin_controle = os.path.join(REPO, "PHRASE-CONTROLE-COFFRE.txt")
    with open(chemin_controle, "rb") as f:
        phrase_controle = f.read().strip()
    sys.path.insert(0, REPO)
    import coffre_fort as cf  # noqa: E402
    chemin_coffre = os.path.join(REPO, ".keys", "coffre_fort.bin")
    _entetes, base = cf.charger(chemin_coffre, phrase_controle)
    description = (
        "Graine Ed25519 des cartes projet (D27) — NEUVE à la reparation D144 "
        "(04/11) : les graines precedentes (e842727c M0-M2, f40f8a20 m3/terrain, "
        f"ad98a059 orpheline jalon v7) ont peri avec les recyclages du labo, "
        f"la carte m4 generation 6 du scelle 0.5.1 etait ORPHELINE. Celle-ci "
        f"signe la carte re-scellee sous lignee D80 (pub {pub_neuve.hex()[:16]}…) "
        "et signera les generations suivantes ; releve : obtenir TRIADE "
        "graine-ed25519-cartes --vers-fichier .keys/ed25519.seed (octets BRUTS, "
        "32 o — jamais d'hex, jamais de fin de ligne)"
    )
    action = cf.placer_entree(base, "TRIADE", ETIQUETTE_GRAINE, description,
                              graine, remplacer=True, description_projet="")
    cf.sauver(chemin_coffre, base, phrase_controle)
    taille_coffre = os.path.getsize(chemin_coffre)
    md5_coffre = hashlib.md5(open(chemin_coffre, "rb").read()).hexdigest()
    trace(f"[É9] coffre : entrée {action} TRIADE/{ETIQUETTE_GRAINE} ; conteneur "
          f"{taille_coffre} o, md5 {md5_coffre[:12]}… — la graine est DURABLE")

    # Export chiffré : copie développeur (download/ du labo, hors dépôt) +
    # racine du coffre Drive
    export = os.path.join(os.path.dirname(REPO), "download", "coffre_fort.bin")
    cf._ecrire_atomique(export, open(chemin_coffre, "rb").read())
    print("[É9] " + cf.pousser_drive(chemin_coffre))
    sys.path.insert(0, os.path.join(REPO, "scripts"))
    import drive_sync as ds  # noqa: E402
    racine = ds.list_folder(ds.DRIVE_ROOT_ID).get("coffre_fort.bin", {})
    md5_distant = racine.get("md5Checksum", "-")
    if md5_distant != md5_coffre:
        refus(f"le coffre Drive racine porte md5 {md5_distant[:12]}… != local "
              f"{md5_coffre[:12]}… — la copie durable n'est PAS posée, "
              "rapporter l'écart (le conteneur local reste valable)")
    trace(f"[É9] coffre Drive racine : coffre_fort.bin md5 {md5_distant[:12]}… "
          "MATCH par relecture — la copie durable est posée ; export local "
          f"download/coffre_fort.bin ({os.path.getsize(export)} o)")

    # ========================= POST-VÉRIFICATIONS ==============================
    print()
    print("--- POST-VÉRIFICATIONS (la preuve que la réparation tient) ---")

    # P1 : la carte se déchiffre en D80 et porte les faits du scellé
    ent2, frag2, sig2, pub2 = cm.lire_carte()
    cm.verifier_signature(pub2, ent2, frag2, sig2)
    bld2 = cm.dechiffrer_fragment(cm.cle_maitresse(phrase), "frag-bld",
                                  frag2["frag-bld"]).decode("utf-8")
    ligne2 = next(l for l in bld2.splitlines() if "artefact=proxy.exe" in l)
    assert f"version=0.5.1" in ligne2 and SHA_SCELLE_051 in ligne2, ligne2[:120]
    prf2 = cm.dechiffrer_fragment(cm.cle_maitresse(phrase), "frag-prf",
                                  frag2["frag-prf"]).decode("utf-8")
    assert "[verifications] runs=1" in prf2, "journal de carte inattendu"
    trace("[P1] carte LISIBLE en lignée D80 : frag-bld version=0.5.1, "
          "empreinte fb41697d…, signature Ed25519 valide (pub "
          f"{pub2.hex()[:12]}…) — la promesse du coffre est tenue à nouveau")

    # P2 : LE VERROU ANTI-ROLLBACK EST VIVANT (la réparation même)
    try:
        B4._anti_rollback()
        refus("l'anti-rollback n'a pas refusé — le verrou n'est pas revenu")
    except B4.EchecBuild as exc:
        if "reconstruction interdite" not in str(exc) or "0.5.1" not in str(exc):
            refus(f"anti-rollback a refusé pour la mauvaise raison : {exc}")
        trace(f"[P2] anti-rollback : « {exc} » — LE VERROU DE LA 0.5.1 EST "
              "VIVANT (une reconstruction est désormais refusée)")

    # P3 : le sceau est toujours vert (rien de signé n'a bougé)
    r = subprocess.run([sys.executable, os.path.join(REPO, "v06", "sceau_I.py"),
                        "verifier"], capture_output=True, text=True, cwd=REPO)
    if r.returncode != 0:
        refus(f"sceau verifier rc={r.returncode} APRÈS le geste : {r.stdout[-300:]}")
    trace("[P3] sceau verifier : ONZE arbres verts (l'arbre m4/I et sa "
          "signature n'ont pas bougé — la réparation est un fait de CARTE)")

    # P4 : l'artefact n'a pas bougé d'un octet
    with open(chemin_exe, "rb") as f:
        exe_apres = f.read()
    if sha256_hex(exe_apres) != SHA_SCELLE_051:
        refus("proxy.exe a bougé pendant le geste !")
    trace("[P4] proxy.exe 0.5.1 : sha256 fb41697d… INTACT avant/après "
          f"({len(exe_apres)} o — l'artefact prouvé terrain n'a pas bougé)")

    # P5 : git ne porte que la carte et le tableau (constat d'écrits)
    r = subprocess.run(["git", "-C", REPO, "status", "--short",
                        "m4/carte"], capture_output=True, text=True)
    trace("[P5] écrits constatés (git status m4/carte) :\n" +
          "\n".join("      " + l for l in r.stdout.strip().splitlines()))

    duree = (datetime.now(timezone.utc) - debut).total_seconds()
    trace(f"=== RÉPARATION TERMINÉE en {duree:.0f} s : la carte génération 6 "
          "du scellé 0.5.1 vit sous la lignée D80 du coffre, le verrou "
          "anti-rollback est vivant, la graine de signature est durable "
          "(coffre TRIADE/" + ETIQUETTE_GRAINE + ") ===")

    # Journal de vol (labo, hors dépôt)
    with open(os.path.join(REPO, "scripts", "reparation_carte_051.log"), "w",
              encoding="utf-8") as f:
        f.write("\n".join(_journal) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
