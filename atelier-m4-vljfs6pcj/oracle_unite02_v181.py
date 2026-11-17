#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""oracle_unite02_v181.py — L'ORACLE DU BLOC loupe-02, L'ÉDITION MÉMO SCELLÉ
(l'instruction vljfs6pcj, les leviers (a)/(b)/(c) du PLAN-vljfs6pcj-M4.md) —
LES MÊMES VECTEURS, LES MÊMES GRAINES (20261114), LE MÊME JUGE, LE MÊME
ORDRE D'IMPRESSION que le v180 (identique ligne à ligne à l'original,
vérifié à la vague 5).

LA CIBLE EXCLUSIVE : L'OUVERTURE DE SESSION — le loupe-01 SCELLÉ du noyau
qui calcule md5+sha256 du fichier ENTIER sous émulation (le chemin critique
mesuré : ~10 s pour 196 Kio, 3,2 s pour 65 Kio). LES QUATRE ouvertures
coûteuses (le différentiel V1 sur temoin-3f et proxy.exe, la vue pré-posée,
le recouvrement V2) passent par LE MÉMO :

  - la CLÉ (a) : l'empreinte du loupe-01 du noyau (les octets ASSEMBLÉS à
    partir de l'arbre scellé) + l'entrée + le contrat loupe-02 + l'oracle ;
  - le RELEVÉ (b) : l'état né relevé, chaîné, signé Ed25519 (clé de test
    publique) ;
  - le PRÉ-FILTRE NATIF (c) : l'attendu hashlib du panneau confronté au
    relevé — la confirmation vivante ne court qu'à la semis ou à la
    discordance ;
  - LA RECONSTRUCTION : le cadre et le panneau relevés posés à leurs
    adresses, LA POIGNÉE RENDUE À L'OS VIRTUEL — puis TOUT EST VIVANT :
    les ~1000 lectures par fichier (loupe-02, LE BLOC SOUS TEST) courent
    réellement à chaque décalage. L'UNITÉ SOUS TEST N'EST JAMAIS RELUE DU
    MÉMO — seul l'auxiliaire crypto scellé est relevé, et son relevé est
    JUGÉ (le différentiel contre le modèle indépendant demeure intégral).

Les sessions bon marché (temoin-1, temoin-384, vide, V3/V4/V5 au parent)
demeurent VIVANTES. Le mémo : chargé VÉRIFIÉ (fail-closed), re-scellé par
le parent (single-writer). Les statistiques à stderr — stdout EST la
console originale.
"""
from __future__ import annotations

import argparse
import hashlib
import multiprocessing as mp
import os
import random
import sys

REPO = "/tmp/triade-gh"
sys.path.insert(0, os.path.join(REPO, "loupe"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import harnais_noyau as HN          # noqa: E402
import build_loupe as BL            # noqa: E402
import memo_sessions as MEMO        # noqa: E402

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


def _ouvrir_session_02(emul, os_v, memo, nom: str, contenu: bytes):
    """L'ouverture AU MÉMO pour l'oracle-02 : le loupe-01 SCELLÉ du noyau
    (blobs['i110001']) — la clé l'empreinte de SES octets assemblés. Au
    relevé jugé : LA RECONSTRUCTION (cadre + panneau + poignée à l'OS) —
    puis tout est vivant. À l'absence : la session vivante (le semis)."""
    bloc = emul.blobs["i110001"][0]
    contrat = open(CONTRAT, "rb").read()
    releve, hit, depots = MEMO.ouvrir_memorise(
        emul, os_v, memo, bloc, contenu, contrat, ORACLE_ID, nom,
        _ouvrir_vivant)
    if hit:
        poignee = MEMO.reconstruire_session(emul, os_v, nom, releve)
    else:
        poignee = emul.u64(528)
    return poignee, hit, releve["secondes"], depots


def tranche(tache: tuple) -> tuple:
    """UNE tranche du différentiel : (nom, contenu, decalages, premiere,
    memo) — l'ouverture (au mémo si ≥ 64 Kio), l'intégration (la première
    tranche seule), la boucle des décalages TOUS VIVANTS : TOUS les
    contrôles de l'original, retournés (jamais imprimés ici — le parent
    imprime DANS L'ORDRE)."""
    nom, contenu, decalages, premiere, memo = tache
    os_v, emul, temoins, m9 = preparer_travailleur()
    depots: list = []
    hit = None
    s_vivante = 0.0
    if MEMO.session_memorisable(contenu):
        poignee, hit, s_vivante, depots = _ouvrir_session_02(
            emul, os_v, memo, nom, contenu)
    else:
        poignee = HN.emplacer_session(emul, os_v, nom)
    assert poignee != 0
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


def tache_vue_preposee(tache: tuple) -> tuple:
    """LA VUE PRÉ-POSÉE (Q3) dans sa propre émulation — les MÊMES contrôles.
    L'ouverture 196 Kio AU MÉMO, la lecture VIVANTE."""
    _, memo = tache
    os_v, emul, temoins, m9 = preparer_travailleur()
    contenu = temoins["temoin-3f.bin"]
    poignee, hit, s_vivante, depots = _ouvrir_session_02(
        emul, os_v, memo, "temoin-3f.bin", contenu)
    emul.ecrire_cadre(536, (64).to_bytes(8, "little"))
    emul.ecrire_cadre(544, (65).to_bytes(8, "little"))
    r = lire(emul, 4096)
    ok = (r["rax"] == 0 and emul.u64(536) == 64 and emul.u64(544) == 65)
    HN.fermer_session(emul)
    return ("vue", ok, hit, s_vivante, depots)


def tache_v2_recouvrement(tache: tuple) -> tuple:
    """V2 (le recouvrement du journal) dans sa propre émulation — les MÊMES
    contrôles, les MÊMES textes. L'ouverture 196 Kio AU MÉMO, les lectures
    et le journal VIVANTS."""
    _, memo = tache
    os_v, emul, temoins, m9 = preparer_travailleur()
    contenu = temoins["temoin-3f.bin"]
    poignee, hit, s_vivante, depots = _ouvrir_session_02(
        emul, os_v, memo, "temoin-3f.bin", contenu)
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
    return ("v2", ok_bords, ok_journal, ok_multi, hit, s_vivante, depots)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--memo", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "memo-sessions-v1.json"))
    args = ap.parse_args()

    if os.path.exists(args.memo):
        try:
            memo = MEMO.MemoSessions.charger(args.memo)
        except MEMO.MemoRefus as e:
            refus("MÉMO-REFUSÉ", str(e))
    else:
        memo = MEMO.MemoSessions()
        print("[memo] absent — la semence vivante coure (le repli EST "
              "l'émulation complète)", file=sys.stderr)

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
    taches = [(nom, contenus[nom], decalages_par_fichier[nom], True, memo)
              for nom in fichiers]
    with mp.Pool(N_TRAVAILLEURS) as pool:
        promesse_vue = pool.apply_async(tache_vue_preposee, ((None, memo),))
        promesse_v2 = pool.apply_async(tache_v2_recouvrement, ((None, memo),))
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
                  f"{'RELEVÉ jugé' if hit else f'session vivante {s_vivante:.1f} s — le semis'}",
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

    # ---- LE SCELLEMENT DU MÉMO (single-writer : le parent) --------------------
    if depots_tous:
        for cle, valeur in depots_tous:
            memo.deposer(cle, valeur)
        infos = memo.sceller(args.memo)
        print(f"[memo] scellé : {infos['n']} entrées, racine "
              f"{infos['racine'][:16]}…, {n_hits} relevé(s) jugé(s) sur "
              f"{n_sessions} sessions ≥ 64 Kio", file=sys.stderr)

    print(f"\n=== L'ORACLE DU BLOC : {VERTS} VERT, {ROUGES} ROUGE "
          f"{'— VERT' if ROUGES == 0 else '— ROUGE'} ===")
    return 0 if ROUGES == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
