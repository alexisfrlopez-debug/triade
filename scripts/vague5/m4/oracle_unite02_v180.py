#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""oracle_unite02_v180.py — L'ORACLE DU BLOC loupe-02, L'ÉDITION PARALLÈLE
(l'instruction mof9q10vq, la vague 5 : « pool de processus Unicorn
persistant ») — LES MÊMES VECTEURS, LES MÊMES GRAINES, LE MÊME JUGE, LE
MÊME ORDRE D'IMPRESSION : seul le DIFFÉRENTIEL V1 change d'exécution.

LA MÉTHODE : les décalages de V1 sont PRÉ-GÉNÉRÉS dans le parent (le MÊME
Random(GRAINE) consommé dans le MÊME ordre de fichiers — les listes sont
IDENTIQUES à l'original), puis les tranches courent dans UN POOL DE
TRAVAILLEURS — chaque travailleur sa PROPRE émulation Unicorn (vivante
pour toute sa tranche : le pool persistant par travailleur), sa PROPRE
session ouverte sur SON fichier. Chaque contrôle est EXACTEMENT celui de
l'original (le même attendu, le même texte) — les verdicts sont
AGREGÉS puis imprimés DANS L'ORDRE ORIGINAL. V2-V5 courent séquentiellement
au parent (leur coût est nul devant le différentiel).
"""
from __future__ import annotations

import hashlib
import multiprocessing as mp
import os
import random
import sys

REPO = "/tmp/triade-gh"
sys.path.insert(0, os.path.join(REPO, "loupe"))

import harnais_noyau as HN          # noqa: E402
import build_loupe as BL            # noqa: E402

L = HN.L
B4 = HN.B4

NOTATION = os.path.join(REPO, "scripts", "campagne_d204", "unite-02-T",
                        "notation", "loupe-02-lire.asm")
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


def tranche(tache: tuple) -> tuple:
    """UNE tranche du différentiel : (nom, contenu, decalages, premiere) —
    l'ouverture, l'intégration (la première tranche seule), la boucle des
    décalages : TOUS les contrôles de l'original, retournés (jamais
    imprimés ici — le parent imprime DANS L'ORDRE)."""
    nom, contenu, decalages, premiere = tache
    os_v, emul, temoins, m9 = preparer_travailleur()
    r = HN.emplacer_session(emul, os_v, nom)
    assert r != 0
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
    return (nom, integration if premiere else None, tout_ok, appels)


def tache_vue_preposee(_) -> tuple:
    """LA VUE PRÉ-POSÉE (Q3) dans sa propre émulation — les MÊMES contrôles."""
    os_v, emul, temoins, m9 = preparer_travailleur()
    contenu = temoins["temoin-3f.bin"]
    HN.emplacer_session(emul, os_v, "temoin-3f.bin")
    emul.ecrire_cadre(536, (64).to_bytes(8, "little"))
    emul.ecrire_cadre(544, (65).to_bytes(8, "little"))
    r = lire(emul, 4096)
    ok = (r["rax"] == 0 and emul.u64(536) == 64 and emul.u64(544) == 65)
    HN.fermer_session(emul)
    return ("vue", ok)


def tache_v2_recouvrement(_) -> tuple:
    """V2 (le recouvrement du journal) dans sa propre émulation — les
    MÊMES contrôles, les MÊMES textes, retournés au parent."""
    os_v, emul, temoins, m9 = preparer_travailleur()
    contenu = temoins["temoin-3f.bin"]
    HN.emplacer_session(emul, os_v, "temoin-3f.bin")
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
    return ("v2", ok_bords, ok_journal, ok_multi)


def main() -> int:
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
    # UNE TÂCHE PAR FICHIER (le profil est sans appel : l'OUVERTURE de
    # session — le md5+sha256 du fichier ENTIERS sous émulation — domine
    # (3,2 s pour 65 Kio, ~10 s pour 196 Kio), les lectures sont quasi
    # gratuites (0,15 ms) : découper en tranches MULTIPLIERAIT les
    # ouvertures, la bonne granularité est LE FICHIER)
    taches = [(nom, contenus[nom], decalages_par_fichier[nom], True)
              for nom in fichiers]
    with mp.Pool(N_TRAVAILLEURS) as pool:
        # la vue pré-posée et V2 (les DEUX ouvertures 3f restantes)
        # démarrent immédiatement, V1 les rejoint — six tâches, un pool
        promesse_vue = pool.apply_async(tache_vue_preposee, (None,))
        promesse_v2 = pool.apply_async(tache_v2_recouvrement, (None,))
        resultats_v1 = pool.map(tranche, taches)
        res_vue = promesse_vue.get()
        res_v2 = promesse_v2.get()
    par_fichier: dict = {}
    for nom, integration, tout_ok, appels in resultats_v1:
        f = par_fichier.setdefault(nom, {"integration": None,
                                         "tout_ok": True, "appels": 0})
        if integration is not None:
            f["integration"] = integration
        f["tout_ok"] &= tout_ok
        f["appels"] += appels
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

    # LE VIDE + V3..V5 : SÉQUENTIELS au parent ; la vue pré-posée et V2
    # (les DEUX dernières ouvertures 3f coûteuses) sont les travailleurs
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

    # ---- V5 : LA FALSIFICATION DEMANDÉE ---------------------------------------
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

    print(f"\n=== L'ORACLE DU BLOC : {VERTS} VERT, {ROUGES} ROUGE "
          f"{'— VERT' if ROUGES == 0 else '— ROUGE'} ===")
    return 0 if ROUGES == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
