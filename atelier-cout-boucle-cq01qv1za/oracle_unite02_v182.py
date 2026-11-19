#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""oracle_unite02_v182.py — L'ORACLE DU BLOC loupe-02, L'ÉDITION DOUBLE
MOTEUR + MÉMO V2 (l'instruction cq01qv1za, les axes (2)/(3)) — LES MÊMES
VECTEURS, LES MÊMES GRAINES (20261114), LE MÊME JUGE, LE MÊME ORDRE
D'IMPRESSION que le v181 (identique ligne à ligne à l'original, exigé par
l'étape de vérification).

LES TROIS DIFFÉRENCES DU V182 (invisibles à la console — stdout EST la
console originale, les statistiques vivent à stderr) :
  1. LE MÉMO V2 : la clé porte la v1 entière (bloc, entrée, contrat,
     oracle) PLUS la config émulateur et la graine (l'instruction) ;
  2. LE DIFFÉRENTIEL V1 PAR LE MOTEUR DE VOLUME : les QUATRE tranches
     (l'ouverture — au mémo si ≥ 64 Kio, vivante sinon — puis les ~1000
     lectures par fichier, la fermeture) courent SOUS QEMU (le lanceur,
     l'image bâtie par le vrai harnais, DIVERGENCE=0 prouvée à
     l'échantillon consigné) — le juge Python confronte chaque ligne au
     modèle indépendant (hashlib), LES MÊMES CONTRÔLES ;
  3. L'AUDIT 1 RUN SUR 10 (--audit ou le compteur au multiple de 10) : les
     tranches RE-EXÉCUTÉES VIVANTES SOUS UNICORN, les relevés confrontés
     AU MÉMO CHAMP À CHAMP — la preuve d'identité, tout écart BLOQUANT.

LES LECTURES DU BLOC SOUS TEST : VIVANTES à chaque décalage (le plan v181
§ gelé : l'unité sous test n'est JAMAIS relue du mémo) — le mémo ne relève
que l'auxiliaire crypto scellé (loupe-01), son relevé est JUGÉ. La vue
pré-posée et le recouvrement V2 : VIVANTS sous Unicorn (bon marché — la
restauration au relevé puis UNE lecture). V3/V4/V5 : VIVANTS séquentiels
au parent (Unicorn, l'original INTACT)."""
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import os
import pathlib
import random
import struct
import sys
import time as _t

REPO = "/tmp/triade-gh"
sys.path.insert(0, os.path.join(REPO, "loupe"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import harnais_noyau as HN          # noqa: E402
import memo_sessions_v2 as MEMO     # noqa: E402
import moteur_qemu as MQ            # noqa: E402

L = HN.L
B4 = HN.B4

NOTATION = os.path.join(REPO, "scripts", "campagne_d204", "unite-02-T",
                        "notation", "loupe-02-lire.asm")
CONTRAT = os.path.join(REPO, "loupe", "I", "loupe-02-lire.md")
ORACLE_ID = "oracle-unite02"
GRAINE = 20261114
TAILLE_TAMPON = 384
N_TRAVAILLEURS = 4

VERTS, ROUGES = 0, 0
AUDIT = {"actif": False, "ecarts": []}


def controle(nom: str, ok: bool, detail: str = "") -> None:
    global VERTS, ROUGES
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom}" + (f" — {detail}" if detail else ""))
    VERTS += ok
    ROUGES += not ok


def refus(nom: str, detail: str) -> None:
    print(f"[oracle-unite02] REFUS {nom} : {detail}", file=sys.stderr)
    sys.exit(2)


class EmulationCampagne(HN.Emulation):
    def __init__(self, os_virtuel):
        super().__init__(os_virtuel)
        rva, slot = L.SLOTS_LOUPE["i110002"]
        if not os.path.exists(NOTATION):
            refus("NOTATION-ABSENTE", f"{NOTATION} — construire d'abord")
        octets, metas = B4.assembler_bloc(self.ks, NOTATION, rva, slot)
        self.uc.mem_write(rva, octets)
        self.blobs["i110002"] = (octets, metas)


def lire(emul, decalage: int):
    return emul.appeler(L.LOUPE02_VA, {"rcx": decalage})


def modele_fenetre(contenu: bytes, decalage: int, journal):
    taille = len(contenu)
    if decalage % 16 != 0:
        return (-5, None, None)
    if decalage >= taille:
        return (-3, None, None)
    remplissage = min(TAILLE_TAMPON, taille - decalage)
    tampon = bytearray(contenu[decalage:decalage + remplissage])
    for dec, octet in journal:
        if decalage <= dec < decalage + remplissage:
            tampon[dec - decalage] = octet
    return (0, remplissage, bytes(tampon))


def decales_valides(taille: int, rng: random.Random) -> list[int]:
    out = []
    if taille > 0:
        out.append(0)
        dernier = (taille - 1) // 16 * 16
        out.append(dernier)
        pleine = taille - TAILLE_TAMPON
        if pleine >= 0 and pleine % 16 == 0 and pleine not in out:
            out.append(pleine)
        elif pleine >= 0:
            pleine -= pleine % 16
            if pleine >= 0 and pleine not in out:
                out.append(pleine)
        if taille % 16 == 0 and taille - 16 not in out and taille >= 16:
            out.append(taille - 16)
        pool = list(range(0, (taille + 15) // 16 * 16, 16))
        k = min(1000, len(pool))
        out += [d for d in rng.sample(pool, k) if d not in set(out)]
    return out


def _ouvrir_vivant(emul, os_v, chemin: str):
    """Le geste d'emplacer_session, rendant le dict des registres (le
    comportement de l'original INTACT — le refus propagé pareil)."""
    emul.uc.mem_write(HN.ADRESSE_CHEMIN,
                      chemin.encode("utf-16-le") + b"\x00\x00")
    r = emul.appeler(L.LOUPE01_VA, {"rcx": HN.ADRESSE_CHEMIN})
    if r["rax"] != 0:
        raise HN.ErreurHarnais(f"l'ouverture de {chemin} a rendu {r['rax']}")
    return r


def preparer_travailleur():
    """L'émulation du travailleur : ses héritages scellés vérifiés, ses
    témoins — la MÊME mise en place que l'original (une fois par
    travailleur, VIVANTE pour toute sa tranche)."""
    os_v = HN.OSVirtuel()
    emul = EmulationCampagne(os_v)
    m9 = open(os.path.join(HN.TRIADE, HN.SCELLE_M9), "rb").read()
    m1 = open(os.path.join(HN.TRIADE, HN.SCELLE_M1), "rb").read()
    if hashlib.sha256(m9).hexdigest() != HN.SCELLE_M9_SHA256 \
            or hashlib.sha256(m1).hexdigest() != HN.SCELLE_M1_SHA256:
        refus("SCELLÉS-DIVERGENTS", "M1/M9 != les ancres du harnais")
    emul.poser_heritages(m9, m1)
    temoins = HN.composer_temoins()
    for nom, contenu in (("temoin-1.bin", temoins["temoin-1.bin"]),
                         ("temoin-384.bin", temoins["temoin-384.bin"]),
                         ("temoin-3f.bin", temoins["temoin-3f.bin"])):
        os_v.declarer(nom, HN.FichierVirtuel(contenu=contenu))
    os_v.declarer("vide.bin", HN.FichierVirtuel(contenu=b""))
    os_v.declarer("proxy.exe", HN.FichierVirtuel(contenu=m9))
    return os_v, emul, temoins, m9


def la_config(moteur: str) -> dict:
    return MEMO.config_emulateur(
        moteur,
        {"m9": HN.SCELLE_M9_SHA256, "m1": HN.SCELLE_M1_SHA256,
         "notation": hashlib.sha256(open(NOTATION, "rb").read()).hexdigest()},
        [list(z) for z in (HN.ZONE_LIBC, HN.ZONE_RDATA, HN.ZONE_IMAGE,
                           HN.ZONE_DATA, HN.ZONE_TESTS)],
        None)


def _cle_du(nom_contenu: bytes, memo, infos_image):
    """La clé v2 de l'ouverture (le loupe-01 SCELLÉ du noyau — les octets
    assemblés de l'image)."""
    bloc = infos_image["blocs"]["i110001"]
    contrat = open(CONTRAT, "rb").read()
    return MEMO.cle_session_v2(bloc, nom_contenu, contrat,
                               la_config("qemu"), GRAINE, ORACLE_ID)


def _releve_de_valeur(valeur: dict) -> dict:
    return {"rax": valeur["rax"], "etat_propre": valeur["etat_propre"],
            "cadre": bytes.fromhex(valeur["cadre_hex"]),
            "panneau": bytes.fromhex(valeur["panneau_hex"]),
            "pos": valeur["pos"], "secondes": valeur.get("secondes", 0.0)}


# ---------------------------------------------------------------------------
# LA TRANCHE AU MOTEUR DE VOLUME (le régime) : l'ouverture (au mémo si
# mémoisable, vivante sous QEMU sinon), les lectures TOUTES VIVANTES sous
# QEMU, la fermeture — le juge Python confronte chaque ligne au modèle.
# ---------------------------------------------------------------------------

def tranche_qemu(tache: tuple) -> tuple:
    (nom, contenu, decalages, premiere, memo, infos_image, bac) = tache
    depots: list = []
    hit = None
    s_vivante = 0.0
    rempl0 = min(TAILLE_TAMPON, len(contenu))
    vol = MQ.VolumeQEMU.depuis_infos(infos_image, pathlib.Path(bac))

    def _releve_de_ligne_ouvrir(d0: dict, dt: float) -> dict:
        chemin16 = nom.encode("utf-16-le") + b"\x00\x00"
        cadre = bytearray(960)
        cadre[0:len(chemin16)] = chemin16
        struct.pack_into("<Q", cadre, 520, d0["taille"])
        struct.pack_into("<Q", cadre, 528, d0["poignee"])
        struct.pack_into("<Q", cadre, 536, d0["vue"])
        struct.pack_into("<Q", cadre, 544, d0["curseur"])
        struct.pack_into("<I", cadre, 552, d0["remplissage"])
        cadre[568:568 + 384] = bytes.fromhex(d0["tampon"])
        return {"rax": d0["rax"], "etat_propre": bool(d0["propre"]),
                "cadre": bytes(cadre),
                "panneau": bytes.fromhex(d0["panneau"]),
                "pos": d0["pos"], "secondes": round(dt, 3)}

    if MEMO.session_memorisable(contenu):
        cle = _cle_du(contenu, memo, infos_image)
        valeur = memo.consulter(cle) if memo is not None else None
        if valeur is not None:
            # RELEVÉ JUGÉ : la restauration puis les lectures VIVANTES QEMU
            releve = _releve_de_valeur(valeur)
            hit = True
        else:
            # LE SEMIS : l'ouverture SEULE sous QEMU, chronométrée seule —
            # le prix déposé au mémo est le prix de l'ouverture, jamais
            # celui de la tranche
            t0 = _t.monotonic()
            d0 = json.loads(vol.executer([("ouvrir", nom)],
                                         {nom: contenu})[0])
            dt = _t.monotonic() - t0
            releve = _releve_de_ligne_ouvrir(d0, dt)
            valeur = {"rax": releve["rax"],
                      "etat_propre": releve["etat_propre"],
                      "cadre_hex": releve["cadre"].hex(),
                      "panneau_hex": releve["panneau"].hex(),
                      "pos": releve["pos"],
                      "secondes": releve["secondes"]}
            memo.deposer(cle, valeur)
            depots = [(cle, valeur)]
            hit = False
            s_vivante = releve["secondes"]
        cadre = releve["cadre"]
        poignee = struct.unpack("<Q", cadre[528:536])[0]
        ops = [("restaurer", poignee, releve["pos"], nom,
                cadre, releve["panneau"])]
        integration = (struct.unpack_from("<I", cadre, 552)[0] == rempl0
                       and cadre[568:568 + rempl0] == contenu[:rempl0])
    else:
        ops = [("ouvrir", nom)]
        integration = None

    for dec in decalages:
        ops.append(("lire", dec))
    ops.append(("fermer",))
    lignes = [json.loads(l) for l in vol.executer(ops, {nom: contenu})]

    if ops[0][0] == "ouvrir":
        d0 = lignes[0]
        integration = (d0["remplissage"] == rempl0
                       and bytes.fromhex(d0["tampon"])[:rempl0]
                       == contenu[:rempl0])

    # ---- LE JUGE (les MÊMES contrôles que l'original, ligne à ligne) ----
    if ops[0][0] == "restaurer":
        vue_avant = struct.unpack_from("<Q", cadre, 536)[0]
        cur_avant = struct.unpack_from("<Q", cadre, 544)[0]
    else:
        vue_avant, cur_avant = lignes[0]["vue"], lignes[0]["curseur"]
    tout_ok, appels = True, 0
    for d in lignes[1:-1]:
        dec = int(d["detail"], 16)
        v_att, rempl_att, tamp_att = modele_fenetre(contenu, dec, [])
        ok = (d["rax"] == v_att and d["propre"] == 1
              and d["remplissage"] == (rempl_att or 0)
              and (rempl_att is None or bytes.fromhex(d["tampon"])
                   [:rempl_att] == tamp_att)
              and d["vue"] == vue_avant and d["curseur"] == cur_avant)
        tout_ok &= ok
        appels += 1
        vue_avant, cur_avant = d["vue"], d["curseur"]
    return (nom, integration if premiere else None, tout_ok, appels,
            hit, s_vivante, depots)


# ---------------------------------------------------------------------------
# LA TRANCHE DE L'AUDIT : l'original v181 INTACT (l'ouverture vivante sous
# Unicorn, les lectures vivantes) + LA PREUVE D'IDENTITÉ CHAMP À CHAMP
# contre le relevé mémoisé.
# ---------------------------------------------------------------------------

def tranche_audit(tache: tuple) -> tuple:
    (nom, contenu, decalages, premiere, memo, infos_image, bac) = tache
    os_v, emul, temoins, m9 = preparer_travailleur()
    depots: list = []
    hit = None
    s_vivante = 0.0
    if MEMO.session_memorisable(contenu):
        bloc = emul.blobs["i110001"][0]
        contrat = open(CONTRAT, "rb").read()

        def _vivant():
            t0 = _t.monotonic()
            r = _ouvrir_vivant(emul, os_v, nom)
            dt = _t.monotonic() - t0
            cadre = emul.cadre()
            poignee = struct.unpack("<Q", cadre[528:536])[0]
            return {"rax": r["rax"], "etat_propre": emul.etat_propre(r),
                    "cadre": cadre, "panneau": emul.panneau(),
                    "pos": os_v.poignees.get(poignee, (nom, 0))[1],
                    "secondes": round(dt, 3)}

        releve, hit, depots, ecarts = MEMO.audit_memorise(
            memo, bloc, contenu, contrat, la_config("qemu"), GRAINE,
            ORACLE_ID, _vivant)
        AUDIT["ecarts"] += [f"{nom} : {e}" for e in ecarts]
        print(f"[audit] {nom} : la re-exécution vivante (Unicorn) "
              f"confrontée au mémo — {len(ecarts)} écart(s) champ à "
              f"champ", file=sys.stderr)
        if hit:
            # le relevé mémoisé RESTAURÉ dans l'émulation vivante — les
            # lectures qui suivent courent réellement
            MEMO.reconstruire_session(emul, os_v, nom, releve)
        s_vivante = releve["secondes"]
    else:
        HN.emplacer_session(emul, os_v, nom)
    rempl0 = min(TAILLE_TAMPON, len(contenu))
    integration = (emul.u32(552) == rempl0
                   and emul.champ(568, rempl0) == contenu[:rempl0])
    tout_ok, appels = True, 0
    for dec in decalages:
        avant_vue, avant_cur = emul.u64(536), emul.u64(544)
        r = lire(emul, dec)
        v_att, rempl_att, tamp_att = modele_fenetre(contenu, dec, [])
        ok = (r["rax"] == v_att and emul.etat_propre(r)
              and emul.u32(552) == rempl_att
              and emul.champ(568, rempl_att) == tamp_att
              and emul.u64(536) == avant_vue
              and emul.u64(544) == avant_cur)
        tout_ok &= ok
        appels += 1
    HN.fermer_session(emul)
    return (nom, integration if premiere else None, tout_ok, appels,
            hit, s_vivante, depots)


def _ouverture_memorisee_unicorn(emul, os_v, memo, nom, contenu,
                                 infos_image, bac):
    """L'ouverture au mémo v2 pour les tâches UNICORN (la vue pré-posée, le
    recouvrement V2) : la clé v2 (config qemu — celle du mémo), le relevé
    restauré à l'émulation vivante ; à l'absence, le SEMIS SOUS QEMU (le
    moteur de volume) puis la restauration — jamais les 10 s de l'Unicorn
    au régime."""
    cle = _cle_du(contenu, memo, infos_image)
    valeur = memo.consulter(cle) if memo is not None else None
    depots: list = []
    if valeur is not None:
        releve = _releve_de_valeur(valeur)
        poignee = MEMO.reconstruire_session(emul, os_v, nom, releve)
        return poignee, True, releve["secondes"], depots
    vol = MQ.VolumeQEMU.depuis_infos(infos_image, pathlib.Path(bac))
    t0 = _t.monotonic()
    lignes = [json.loads(l) for l in vol.executer([("ouvrir", nom)],
                                                  {nom: contenu})]
    dt = _t.monotonic() - t0
    d0 = lignes[0]
    chemin16 = nom.encode("utf-16-le") + b"\x00\x00"
    cadre = bytearray(960)
    cadre[0:len(chemin16)] = chemin16
    struct.pack_into("<Q", cadre, 520, d0["taille"])
    struct.pack_into("<Q", cadre, 528, d0["poignee"])
    struct.pack_into("<Q", cadre, 536, d0["vue"])
    struct.pack_into("<Q", cadre, 544, d0["curseur"])
    struct.pack_into("<I", cadre, 552, d0["remplissage"])
    cadre[568:568 + 384] = bytes.fromhex(d0["tampon"])
    releve = {"rax": d0["rax"], "etat_propre": bool(d0["propre"]),
              "cadre": bytes(cadre), "panneau": bytes.fromhex(d0["panneau"]),
              "pos": d0["pos"], "secondes": round(dt, 3)}
    if memo is not None:
        memo.deposer(cle, {"rax": releve["rax"],
                           "etat_propre": releve["etat_propre"],
                           "cadre_hex": releve["cadre"].hex(),
                           "panneau_hex": releve["panneau"].hex(),
                           "pos": releve["pos"],
                           "secondes": releve["secondes"]})
        depots = [(cle, {"rax": releve["rax"],
                         "etat_propre": releve["etat_propre"],
                         "cadre_hex": releve["cadre"].hex(),
                         "panneau_hex": releve["panneau"].hex(),
                         "pos": releve["pos"],
                         "secondes": releve["secondes"]})]
    poignee = MEMO.reconstruire_session(emul, os_v, nom, releve)
    return poignee, False, releve["secondes"], depots


def tache_vue_preposee(tache: tuple) -> tuple:
    """LA VUE PRÉ-POSÉE (Q3) dans sa propre émulation — les MÊMES contrôles.
    L'ouverture 196 Kio AU MÉMO V2 (restaurée à l'émulation vivante), la
    lecture VIVANTE (Unicorn — bon marché, l'original INTACT)."""
    _, memo, infos_image, bac, audit = tache
    os_v, emul, temoins, m9 = preparer_travailleur()
    contenu = temoins["temoin-3f.bin"]
    depots: list = []
    if audit:
        bloc = emul.blobs["i110001"][0]
        contrat = open(CONTRAT, "rb").read()

        def _vivant():
            t0 = _t.monotonic()
            r = _ouvrir_vivant(emul, os_v, "temoin-3f.bin")
            dt = _t.monotonic() - t0
            return {"rax": r["rax"], "etat_propre": emul.etat_propre(r),
                    "cadre": emul.cadre(), "panneau": emul.panneau(),
                    "pos": os_v.poignees.get(emul.u64(528),
                                             ("temoin-3f.bin", 0))[1],
                    "secondes": round(dt, 3)}

        releve, hit, depots, ecarts = MEMO.audit_memorise(
            memo, bloc, contenu, contrat, la_config("qemu"), GRAINE,
            ORACLE_ID, _vivant)
        AUDIT["ecarts"] += [f"vue : {e}" for e in ecarts]
        print(f"[audit] vue pré-posée : la re-exécution vivante (Unicorn) "
              f"confrontée au mémo — {len(ecarts)} écart(s)", file=sys.stderr)
        if hit:
            MEMO.reconstruire_session(emul, os_v, "temoin-3f.bin", releve)
        hit_b, s_vivante = hit, releve["secondes"]
    else:
        poignee, hit_b, s_vivante, depots = _ouverture_memorisee_unicorn(
            emul, os_v, memo, "temoin-3f.bin", contenu, infos_image, bac)
    emul.ecrire_cadre(536, (64).to_bytes(8, "little"))
    emul.ecrire_cadre(544, (65).to_bytes(8, "little"))
    r = lire(emul, 4096)
    ok = (r["rax"] == 0 and emul.u64(536) == 64 and emul.u64(544) == 65)
    HN.fermer_session(emul)
    return ("vue", ok, hit_b, s_vivante, depots)


def tache_v2_recouvrement(tache: tuple) -> tuple:
    """V2 (le recouvrement du journal) dans sa propre émulation — les MÊMES
    contrôles, les MÊMES textes. L'ouverture 196 Kio AU MÉMO V2, les
    lectures et le journal VIVANTS (Unicorn)."""
    _, memo, infos_image, bac, audit = tache
    os_v, emul, temoins, m9 = preparer_travailleur()
    contenu = temoins["temoin-3f.bin"]
    depots: list = []
    if audit:
        bloc = emul.blobs["i110001"][0]
        contrat = open(CONTRAT, "rb").read()

        def _vivant():
            t0 = _t.monotonic()
            r = _ouvrir_vivant(emul, os_v, "temoin-3f.bin")
            dt = _t.monotonic() - t0
            return {"rax": r["rax"], "etat_propre": emul.etat_propre(r),
                    "cadre": emul.cadre(), "panneau": emul.panneau(),
                    "pos": os_v.poignees.get(emul.u64(528),
                                             ("temoin-3f.bin", 0))[1],
                    "secondes": round(dt, 3)}

        releve, hit, depots, ecarts = MEMO.audit_memorise(
            memo, bloc, contenu, contrat, la_config("qemu"), GRAINE,
            ORACLE_ID, _vivant)
        AUDIT["ecarts"] += [f"V2 : {e}" for e in ecarts]
        print(f"[audit] V2 : la re-exécution vivante (Unicorn) "
              f"confrontée au mémo — {len(ecarts)} écart(s)", file=sys.stderr)
        if hit:
            MEMO.reconstruire_session(emul, os_v, "temoin-3f.bin", releve)
        hit_b, s_vivante = hit, releve["secondes"]
    else:
        poignee, hit_b, s_vivante, depots = _ouverture_memorisee_unicorn(
            emul, os_v, memo, "temoin-3f.bin", contenu, infos_image, bac)
    fen, rempl = 65536, TAILLE_TAMPON
    journal_bords = [(fen, 0xAA), (fen + rempl - 1, 0xBB),
                     (fen + rempl, 0xCC), (fen - 16, 0xDD)]
    emul.poser_journal(journal_bords)
    journal_avant = bytes(emul.uc.mem_read(L.R_JOURNAL, L.ZONE_JOURNAL))
    r = lire(emul, fen)
    v_att, rempl_att, tamp_att = modele_fenetre(contenu, fen, journal_bords)
    ok_bords = (r["rax"] == 0 and emul.u32(552) == rempl_att
                and emul.champ(568, rempl_att) == tamp_att)
    journal_apres = bytes(emul.uc.mem_read(L.R_JOURNAL, L.ZONE_JOURNAL))
    ok_journal = journal_apres == journal_avant
    journal_multi = [(fen + 5, 0x11), (fen + 100, 0x22), (fen + 200, 0x33),
                     (fen + 300, 0x44), (fen + 383, 0x55)]
    emul.poser_journal(journal_multi)
    r = lire(emul, fen)
    v_att, rempl_att, tamp_att = modele_fenetre(contenu, fen, journal_multi)
    ok_multi = (r["rax"] == 0 and emul.champ(568, rempl_att) == tamp_att)
    HN.fermer_session(emul)
    return ("v2", ok_bords, ok_journal, ok_multi, hit_b, s_vivante, depots)


def main() -> int:
    ap = argparse.ArgumentParser()
    ici = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--memo", default=os.path.join(ici,
                                                   "memo-sessions-v2.json"))
    ap.add_argument("--audit", action="store_true")
    ap.add_argument("--bac", default=os.path.join(ici, "bac-qemu-o2"))
    args = ap.parse_args()

    if os.path.exists(args.memo):
        try:
            memo = MEMO.MemoSessionsV2.charger(args.memo)
        except MEMO.MemoRefus as e:
            refus("MÉMO-REFUSÉ", str(e))
    else:
        memo = MEMO.MemoSessionsV2()
        print("[memo] absent — la semence vivante coure (le repli EST "
              "l'émulation complète)", file=sys.stderr)

    audit = args.audit or (
        (memo.compteur_runs + 1) % MEMO.PERIODE_AUDIT == 0)
    if audit:
        print(f"[audit] le run {memo.compteur_runs + 1} — les tranches "
              "re-exécutées vivantes sous Unicorn, la preuve d'identité",
              file=sys.stderr)
    AUDIT["actif"] = audit

    # L'IMAGE DU VOLUME (bâtie UNE FOIS au parent — les travailleurs la
    # partagent, jamais 1,5 s par tête)
    pathlib.Path(args.bac).mkdir(parents=True, exist_ok=True)
    vol = MQ.VolumeQEMU(os.path.join(args.bac, "image"))
    infos_image = vol.construire_image(NOTATION, "i110002")

    print("=== L'ORACLE DU BLOC — l'unité 2 (loupe-02 × bras T) : les "
          "vecteurs du contrat, le juge = le modèle indépendant ===")
    os_v = HN.OSVirtuel()
    emul = EmulationCampagne(os_v)
    m9 = open(os.path.join(HN.TRIADE, HN.SCELLE_M9), "rb").read()
    m1 = open(os.path.join(HN.TRIADE, HN.SCELLE_M1), "rb").read()
    if hashlib.sha256(m9).hexdigest() != HN.SCELLE_M9_SHA256 \
            or hashlib.sha256(m1).hexdigest() != HN.SCELLE_M1_SHA256:
        refus("SCELLÉS-DIVERGENTS", "M1/M9 != les ancres du harnais")
    emul.poser_heritages(m9, m1)
    temoins = HN.composer_temoins()
    for nom, contenu in (("temoin-1.bin", temoins["temoin-1.bin"]),
                         ("temoin-384.bin", temoins["temoin-384.bin"]),
                         ("temoin-3f.bin", temoins["temoin-3f.bin"])):
        os_v.declarer(nom, HN.FichierVirtuel(contenu=contenu))
    os_v.declarer("vide.bin", HN.FichierVirtuel(contenu=b""))
    os_v.declarer("proxy.exe", HN.FichierVirtuel(contenu=m9))

    # ---- V1 : LE DIFFÉRENTIEL — les décalages PRÉ-GÉNÉRÉS (le MÊME rng) ----
    print("\n-- V1 : le différentiel (les témoins + le scellé) --")
    rng = random.Random(GRAINE)
    fichiers = ("temoin-1.bin", "temoin-384.bin", "temoin-3f.bin",
                "proxy.exe")
    contenus = {"temoin-1.bin": temoins["temoin-1.bin"],
                "temoin-384.bin": temoins["temoin-384.bin"],
                "temoin-3f.bin": temoins["temoin-3f.bin"],
                "proxy.exe": m9}
    decalages_par_fichier = {nom: decales_valides(len(contenus[nom]), rng)
                             for nom in fichiers}
    tranche = tranche_audit if audit else tranche_qemu
    taches = [(nom, contenus[nom], decalages_par_fichier[nom], True, memo,
               infos_image, args.bac) for nom in fichiers]
    with mp.Pool(N_TRAVAILLEURS) as pool:
        promesse_vue = pool.apply_async(
            tache_vue_preposee, ((None, memo, infos_image, args.bac,
                                  audit),))
        promesse_v2 = pool.apply_async(
            tache_v2_recouvrement, ((None, memo, infos_image, args.bac,
                                     audit),))
        resultats_v1 = pool.map(tranche, taches)
        res_vue = promesse_vue.get()
        res_v2 = promesse_v2.get()
    par_fichier: dict = {}
    depots_tous: list = []
    n_hits, n_sessions = 0, 0
    for nom, integration, tout_ok, appels, hit, s_vivante, depots \
            in resultats_v1:
        f = par_fichier.setdefault(nom, {"integration": None,
                                         "tout_ok": True, "appels": 0})
        if integration is not None:
            f["integration"] = integration
        f["tout_ok"] &= tout_ok
        f["appels"] += appels
        if hit is not None:
            n_sessions += 1
            n_hits += int(hit)
            depots_tous += depots
            print(f"[memo] V1 {nom} : "
                  f"{'RELEVÉ jugé' if hit else f'session vivante {s_vivante:.1f} s — le semis QEMU'}",
                  file=sys.stderr)
    for res, etiquette in ((res_vue, "vue pré-posée"), (res_v2, "V2")):
        hit, s_vivante, depots = res[-3], res[-2], res[-1]
        n_sessions += 1
        n_hits += int(hit)
        depots_tous += depots
        print(f"[memo] {etiquette} : "
              f"{'RELEVÉ jugé' if hit else f'session vivante {s_vivante:.1f} s — le semis'}",
              file=sys.stderr)
    for nom in fichiers:
        f = par_fichier[nom]
        contenu = contenus[nom]
        controle(f"V1:{nom}-la-fenetre-nee-a-l-ouverture", f["integration"],
                 f"loupe-01 scellé a appelé la notation de campagne : "
                 f"remplissage {min(TAILLE_TAMPON, len(contenu))} == "
                 f"min(384, {len(contenu)})")
        controle(f"V1:{nom}-la-fenetre-bornee-a-{f['appels']}-decalages",
                 f["tout_ok"],
                 f"{f['appels']} décalages valides (les frontières + la "
                 f"graine {GRAINE}) : le tampon == la découpe, remplissage "
                 f"== min(384, taille − décalage), la vue et le curseur "
                 f"INTACTS")

    # LE VIDE + V3..V5 : SÉQUENTIELS au parent — VIVANTS (bon marché)
    r = HN.emplacer_session(emul, os_v, "vide.bin")
    controle("V1:vide.bin-l-ouverture-sans-fenetre",
             r != 0 and emul.u32(552) == 0,
             "le vide s'ouvre sans fenêtre (loupe-01 saute l'appelé) — "
             "remplissage 0")
    r = lire(emul, 0)
    controle("V1:vide.bin-aucune-fenetre-valide", r["rax"] == -3,
             "sur le vide, décalage 0 ≥ taille 0 → -3 HORS-BORNES")
    HN.fermer_session(emul)

    controle("V1:la-vue-et-le-curseur-intacts", res_vue[1],
             "la lecture à 4096 ne déplace NI la vue (64) NI le curseur (65)")

    # ---- V2 : LE RECOUVREMENT DU JOURNAL (les résultats du travailleur) ----
    print("\n-- V2 : le recouvrement du journal --")
    controle("V2:les-bords-de-fenetre", res_v2[1],
             "le premier (0xAA) et le dernier (0xBB) recouverts ; l'avant "
             "(fenêtre−16) et l'après (fenêtre+384) IGNORES — l'édition "
             "survit au défilement")
    controle("V2:le-journal-intact", res_v2[2],
             "loupe-02 ne écrit JAMAIS au journal (I2 : la lecture ne touche "
             "que le tampon du cadre)")
    controle("V2:cinq-entrees-dont-une-non-alignee", res_v2[3],
             "cinq entrées dedans (fen+5 NON ALIGNÉE comprise) — le tampon "
             "== le modèle")

    # ---- V3 : LES REJETS ------------------------------------------------------
    print("\n-- V3 : les rejets --")
    r = lire(emul, 0)
    controle("V3:E1-sans-session", r["rax"] == -4 and emul.etat_propre(r),
             "la session fermée → -4 SESSION, rien lu")
    HN.emplacer_session(emul, os_v, "temoin-384.bin")
    emul.ecrire_cadre(568, b"\xCC" * TAILLE_TAMPON)
    emul.ecrire_cadre(552, (0xBEEF).to_bytes(4, "little"))
    poison = emul.champ(568, TAILLE_TAMPON)
    rempl_poison = emul.u32(552)
    r = lire(emul, 40)
    controle("V3:E2-le-decalage-non-aligne",
             r["rax"] == -5 and emul.etat_propre(r)
             and emul.champ(568, TAILLE_TAMPON) == poison
             and emul.u32(552) == rempl_poison,
             "40 non multiple de 16 → -5 ENTRÉE, le tampon ET le "
             "remplissage INTACTS (rien lu)")
    r = lire(emul, 384)
    controle("V3:E3a-le-decalage-a-la-taille",
             r["rax"] == -3 and emul.champ(568, TAILLE_TAMPON) == poison,
             "384 == la taille → -3 HORS-BORNES, rien lu")
    r = lire(emul, 400)
    controle("V3:E3b-le-decalage-au-dela",
             r["rax"] == -3 and emul.champ(568, TAILLE_TAMPON) == poison,
             "400 > la taille → -3 HORS-BORNES, rien lu")
    r = lire(emul, 1 << 40)
    controle("V3:E3c-le-decalage-immense",
             r["rax"] == -3 and emul.champ(568, TAILLE_TAMPON) == poison,
             "2^40 → -3 HORS-BORNES (u64, jamais signé), rien lu")
    HN.fermer_session(emul)

    # ---- V4 : L'ÉCHEC SYSTÈME -------------------------------------------------
    print("\n-- V4 : l'échec système --")
    HN.emplacer_session(emul, os_v, "temoin-384.bin")
    os_v.journal_gle.clear()
    os_v.armer_echec_read(1)
    r = lire(emul, 0)
    controle("V4:le-readfile-en-echec",
             r["rax"] == -6 and emul.u32(552) == 0
             and len(os_v.journal_gle) >= 1,
             f"rax={r['rax']}, remplissage {emul.u32(552)} == 0 "
             f"(fail-closed), le gle CONSIGNÉ au journal du harnais : "
             f"{os_v.journal_gle}")
    os_v.armer_echec_read(None)
    r = lire(emul, 0)
    controle("V4:la-session-survit",
             r["rax"] == 0 and emul.u32(552) == TAILLE_TAMPON
             and emul.champ(568, TAILLE_TAMPON) == temoins["temoin-384.bin"],
             "l'échec ne clôt PAS la session : la lecture suivante est "
             "verte, le tampon == le témoin entier")
    HN.fermer_session(emul)

    # ---- V5 : LA FALSIFICATION DEMANDÉE (VIVANTE) ----------------------------
    print("\n-- V5 : la falsification demandée --")
    HN.emplacer_session(emul, os_v, "temoin-384.bin")
    r = lire(emul, 0)
    modele = temoins["temoin-384.bin"][:TAILLE_TAMPON]
    ok_lecture = (r["rax"] == 0
                  and emul.champ(568, TAILLE_TAMPON) == modele)
    emul.ecrire_cadre(568 + 3, b"\xFF")
    etat_lu = emul.champ(568, TAILLE_TAMPON)
    divergence = etat_lu != modele
    controle("V5:l-octet-mute-l-etat-lu-diverge",
             ok_lecture and divergence,
             "la lecture d'abord VERT (le tampon == le modèle), l'octet 3 "
             "muté 0x{:02x} → {:02x} : l'état lu DIVERGE du modèle — la "
             "falsification est DÉTECTABLE (le juge lit l'état)".format(
                 modele[3], etat_lu[3]))
    HN.fermer_session(emul)

    # ---- LE SCELLEMENT DU MÉMO V2 (single-writer : le parent) -----------------
    for cle, valeur in depots_tous:
        memo.deposer(cle, valeur)
    infos = memo.sceller(args.memo, la_config("qemu"), GRAINE)
    print(f"[memo] scellé : {infos['n']} entrées, racine "
          f"{infos['racine'][:16]}…, compteur de runs "
          f"{infos['compteur_runs']}, {n_hits} relevé(s) jugé(s) sur "
          f"{n_sessions} sessions ≥ 64 Kio", file=sys.stderr)

    if AUDIT["ecarts"]:
        for e in AUDIT["ecarts"]:
            print(f"[audit] ÉCART BLOQUANT — {e}", file=sys.stderr)
        return 3

    print(f"\n=== L'ORACLE DU BLOC : {VERTS} VERT, {ROUGES} ROUGE "
          f"{'— VERT' if ROUGES == 0 else '— ROUGE'} ===")
    return 0 if ROUGES == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
