#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""oracle_unite02.py — L'ORACLE DU BLOC AU PÉRIMÈTRE LIVRÉ, l'unité 2
(loupe-02 lire × bras T, la campagne D204 — le juge = le modèle indépendant).

LES VECTEURS DEPUIS LE CONTRAT (loupe/I/loupe-02-lire.md — l'oracle régénéré
depuis I, écrit-avant-code : oracle-depuis-I.txt) : le harnais du domaine
(harnais_noyau.Emulation : le mini-OS, les shims, les sentinelles) porte la
pièce de campagne au slot loupe-02, les DIX-SEPT autres blocs demeurant les
scellés — loupe-01 scellé APPELLE la notation de campagne à chaque
naissance de session (la fenêtre à la vue 0).

  V1 (le différentiel)  : les témoins du kit + le proxy.exe scellé — le
      tampon comparé à la découpe Python à 1 000 décalages aléatoires
      valides (la graine fixe 20261114), les frontières couvertes à la
      main (la fenêtre pleine, la dernière partielle, l'avant-dernière) ;
  V2 (le recouvrement)  : les entrées aux BORDS de fenêtre (le premier, le
      dernier, l'avant, l'après) + une entrée NON ALIGNÉE + cinq entrées
      dedans — le journal INTACT après le geste (loupe-02 ne l'écrit jamais) ;
  V3 (les rejets)       : sans session (-4), non aligné (-5), à la taille
      exacte (-3), au-delà (-3) — RIEN lu : le tampon empoisonné INTACT ;
  V4 (l'échec système)  : le shim ReadFile en échec (armé au Nième appel) →
      -6, remplissage 0, le gle CONSIGNÉ au journal du harnais, la session
      SURVIT (la lecture suivante verte) ;
  V5 (la falsification) : un octet du tampon muté après lecture — l'état lu
      DIVERGE du modèle : la falsification demandée, charte § 3.

Usage : python3 scripts/campagne_d204/unite-02-T/oracle_unite02.py
Sortie : 0 = oracle VERT (falsification comprise) ; 2 = refus nommé.
"""
from __future__ import annotations

import hashlib
import os
import random
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
UNITE = os.path.join(REPO, "scripts", "campagne_d204", "unite-02-T-d210")
sys.path.insert(0, os.path.join(REPO, "loupe"))

import harnais_noyau as HN          # noqa: E402  (le harnais du domaine)
import build_loupe as BL            # noqa: E402  (B4 : le lecteur canonique)

L = HN.L
B4 = HN.B4

NOTATION = os.path.join(UNITE, "notation", "loupe-02-lire.asm")
GRAINE = 20261114                     # la graine fixe des décalages aléatoires
TAILLE_TAMPON = 384

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
    """Le harnais du domaine au slot loupe-02 PORTANT LA PIÈCE DE CAMPAGNE :
    les dix-sept autres blocs demeurent les notations scellées (loupe-01
    scellé appelera la notation de campagne à la naissance — l'intégration
    vit à chaque ouverture)."""

    def __init__(self, os_virtuel):
        super().__init__(os_virtuel)
        rva, slot = L.SLOTS_LOUPE["i110002"]
        if not os.path.exists(NOTATION):
            refus("NOTATION-ABSENTE", f"{NOTATION} — construire d'abord")
        octets, metas = B4.assembler_bloc(self.ks, NOTATION, rva, slot)
        self.uc.mem_write(rva, octets)
        self.blobs["i110002"] = (octets, metas)


def lire(emul: HN.Emulation, decalage: int):
    """L'appel de loupe-02 au décalage donné (le geste réel de la campagne)."""
    return emul.appeler(L.LOUPE02_VA, {"rcx": decalage})


def modele_fenetre(contenu: bytes, decalage: int, journal):
    """LE MODÈLE INDÉPENDANT — la sémantique du contrat, jamais les octets
    du bloc : (verdict, remplissage, tampon attendu)."""
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
    """Les décalages de l'épreuve : les frontières à la main + les aléatoires
    (1 000, la graine fixe) — tous multiples de 16, tous < taille."""
    out = []
    if taille > 0:
        out.append(0)                                  # la première fenêtre
        dernier = (taille - 1) // 16 * 16              # la dernière valide
        out.append(dernier)
        pleine = taille - TAILLE_TAMPON                # la dernière PLEINE
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


def main() -> int:
    print("=== L'ORACLE DU BLOC — l'unité 2 (loupe-02 × bras T) : les "
          "vecteurs du contrat, le juge = le modèle indépendant ===")
    os_v = HN.OSVirtuel()
    emul = EmulationCampagne(os_v)

    # LES HÉRITAGES SCELLÉS posés aux slots du plan (R7 — la même mise en
    # place que le harnais du domaine : libc-01/07 + tls13-01..04 extraits
    # des SCELLÉS M1/M9, sans eux l'appelé de loupe-01 est un désert)
    m9 = open(os.path.join(HN.TRIADE, HN.SCELLE_M9), "rb").read()
    m1 = open(os.path.join(HN.TRIADE, HN.SCELLE_M1), "rb").read()
    if hashlib.sha256(m9).hexdigest() != HN.SCELLE_M9_SHA256 \
            or hashlib.sha256(m1).hexdigest() != HN.SCELLE_M1_SHA256:
        refus("SCELLÉS-DIVERGENTS", "M1/M9 != les ancres du harnais")
    emul.poser_heritages(m9, m1)

    # LES TÉMOINS DU KIT (la génération FIXE, graine 20261107) + le scellé
    temoins = HN.composer_temoins()
    for nom, contenu in (("temoin-1.bin", temoins["temoin-1.bin"]),
                         ("temoin-384.bin", temoins["temoin-384.bin"]),
                         ("temoin-3f.bin", temoins["temoin-3f.bin"])):
        os_v.declarer(nom, HN.FichierVirtuel(contenu=contenu))
    os_v.declarer("vide.bin", HN.FichierVirtuel(contenu=b""))
    os_v.declarer("proxy.exe", HN.FichierVirtuel(contenu=m9))  # le scellé R7

    # ---- V1 : LE DIFFÉRENTIEL — la fenêtre bornée, 1 000 décalages -----------
    print("\n-- V1 : le différentiel (les témoins + le scellé) --")
    rng = random.Random(GRAINE)
    for nom in ("temoin-1.bin", "temoin-384.bin", "temoin-3f.bin", "proxy.exe"):
        contenu = {"temoin-1.bin": temoins["temoin-1.bin"],
                   "temoin-384.bin": temoins["temoin-384.bin"],
                   "temoin-3f.bin": temoins["temoin-3f.bin"],
                   "proxy.exe": m9}[nom]
        r = HN.emplacer_session(emul, os_v, nom)   # loupe-01 scellé → ma loupe-02
        assert r != 0                                # la poignée de la session
        rempl0 = min(TAILLE_TAMPON, len(contenu))
        integration = (emul.u32(552) == rempl0
                       and emul.champ(568, rempl0) == contenu[:rempl0])
        controle(f"V1:{nom}-la-fenetre-nee-a-l-ouverture", integration,
                 f"loupe-01 scellé a appelé la notation de campagne : "
                 f"remplissage {emul.u32(552)} == min(384, {len(contenu)})")
        tout_ok, appels = True, 0
        for dec in decales_valides(len(contenu), rng):
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
        controle(f"V1:{nom}-la-fenetre-bornee-a-{appels}-decalages", tout_ok,
                 f"{appels} décalages valides (les frontières + la graine "
                 f"{GRAINE}) : le tampon == la découpe, remplissage == "
                 f"min(384, taille − décalage), la vue et le curseur INTACTS")
        HN.fermer_session(emul)

    # LE VIDE : l'ouverture passe (loupe-01 saute la fenêtre), AUCUN décalage
    # n'est valide (P3 : décalage < taille = 0 — impossible)
    r = HN.emplacer_session(emul, os_v, "vide.bin")
    controle("V1:vide.bin-l-ouverture-sans-fenetre",
             r != 0 and emul.u32(552) == 0,
             "le vide s'ouvre sans fenêtre (loupe-01 saute l'appelé) — "
             "remplissage 0")
    r = lire(emul, 0)
    controle("V1:vide.bin-aucune-fenetre-valide", r["rax"] == -3,
             "sur le vide, décalage 0 ≥ taille 0 → -3 HORS-BORNES")
    HN.fermer_session(emul)

    # LA VUE PRÉ-POSÉE (Q3 renforcé) : la vue posée à un décalage non nul,
    # la lecture ne la déplace PAS (le défilement est à loupe-11)
    contenu = temoins["temoin-3f.bin"]
    HN.emplacer_session(emul, os_v, "temoin-3f.bin")
    emul.ecrire_cadre(536, (64).to_bytes(8, "little"))   # la vue à 64
    emul.ecrire_cadre(544, (65).to_bytes(8, "little"))   # le curseur à 65
    r = lire(emul, 4096)
    controle("V1:la-vue-et-le-curseur-intacts",
             r["rax"] == 0 and emul.u64(536) == 64 and emul.u64(544) == 65,
             "la lecture à 4096 ne déplace NI la vue (64) NI le curseur (65)")
    HN.fermer_session(emul)

    # ---- V2 : LE RECOUVREMENT DU JOURNAL -------------------------------------
    print("\n-- V2 : le recouvrement du journal --")
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
    controle("V2:les-bords-de-fenetre", ok_bords,
             "le premier (0xAA) et le dernier (0xBB) recouverts ; l'avant "
             "(fenêtre−16) et l'après (fenêtre+384) IGNORES — l'édition "
             "survit au défilement")
    journal_apres = bytes(emul.uc.mem_read(L.R_JOURNAL, L.ZONE_JOURNAL))
    controle("V2:le-journal-intact", journal_apres == journal_avant,
             "loupe-02 ne écrit JAMAIS au journal (I2 : la lecture ne touche "
             "que le tampon du cadre)")
    journal_multi = [(fen + 5, 0x11), (fen + 100, 0x22), (fen + 200, 0x33),
                     (fen + 300, 0x44), (fen + 383, 0x55)]
    emul.poser_journal(journal_multi)
    r = lire(emul, fen)
    v_att, rempl_att, tamp_att = modele_fenetre(contenu, fen, journal_multi)
    controle("V2:cinq-entrees-dont-une-non-alignee",
             r["rax"] == 0 and emul.champ(568, rempl_att) == tamp_att,
             "cinq entrées dedans (fen+5 NON ALIGNÉE comprise) — le tampon "
             "== le modèle")
    emul.poser_journal([])
    HN.fermer_session(emul)

    # ---- V3 : LES REJETS — rien lu, le tampon empoisonné INTACT --------------
    print("\n-- V3 : les rejets --")
    r = lire(emul, 0)
    controle("V3:E1-sans-session", r["rax"] == -4 and emul.etat_propre(r),
             "la session fermée → -4 SESSION, rien lu")
    HN.emplacer_session(emul, os_v, "temoin-384.bin")
    emul.ecrire_cadre(568, b"\xCC" * TAILLE_TAMPON)   # le poison
    emul.ecrire_cadre(552, (0xBEEF).to_bytes(4, "little"))
    poison = emul.champ(568, TAILLE_TAMPON)
    rempl_poison = emul.u32(552)
    r = lire(emul, 40)                                 # non aligné
    controle("V3:E2-le-decalage-non-aligne",
             r["rax"] == -5 and emul.etat_propre(r)
             and emul.champ(568, TAILLE_TAMPON) == poison
             and emul.u32(552) == rempl_poison,
             "40 non multiple de 16 → -5 ENTRÉE, le tampon ET le remplissage "
             "INTACTS (rien lu)")
    r = lire(emul, 384)                                # == la taille
    controle("V3:E3a-le-decalage-a-la-taille",
             r["rax"] == -3 and emul.champ(568, TAILLE_TAMPON) == poison,
             "384 == la taille → -3 HORS-BORNES, rien lu")
    r = lire(emul, 400)                                # au-delà
    controle("V3:E3b-le-decalage-au-dela",
             r["rax"] == -3 and emul.champ(568, TAILLE_TAMPON) == poison,
             "400 > la taille → -3 HORS-BORNES, rien lu")
    r = lire(emul, 1 << 40)                            # très au-delà
    controle("V3:E3c-le-decalage-immense",
             r["rax"] == -3 and emul.champ(568, TAILLE_TAMPON) == poison,
             "2^40 → -3 HORS-BORNES (u64, jamais signé), rien lu")
    HN.fermer_session(emul)

    # ---- V4 : L'ÉCHEC SYSTÈME — le shim ReadFile en échec, la session SURVIT -
    print("\n-- V4 : l'échec système --")
    HN.emplacer_session(emul, os_v, "temoin-384.bin")
    os_v.journal_gle.clear()
    os_v.armer_echec_read(1)                           # le PROCHAIN ReadFile
    r = lire(emul, 0)
    controle("V4:le-readfile-en-echec",
             r["rax"] == -6 and emul.u32(552) == 0
             and len(os_v.journal_gle) >= 1,
             f"rax={r['rax']}, remplissage {emul.u32(552)} == 0 (fail-closed), "
             f"le gle CONSIGNÉ au journal du harnais : {os_v.journal_gle}")
    os_v.armer_echec_read(None)                        # désarmé
    r = lire(emul, 0)
    controle("V4:la-session-survit",
             r["rax"] == 0 and emul.u32(552) == TAILLE_TAMPON
             and emul.champ(568, TAILLE_TAMPON) == temoins["temoin-384.bin"],
             "l'échec ne clôt PAS la session : la lecture suivante est "
             "verte, le tampon == le témoin entier")
    HN.fermer_session(emul)

    # ---- V5 : LA FALSIFICATION DEMANDÉE (charte § 3) --------------------------
    print("\n-- V5 : la falsification demandée --")
    HN.emplacer_session(emul, os_v, "temoin-384.bin")
    r = lire(emul, 0)
    modele = temoins["temoin-384.bin"][:TAILLE_TAMPON]
    ok_lecture = (r["rax"] == 0
                  and emul.champ(568, TAILLE_TAMPON) == modele)
    # l'octet muté APRÈS la lecture : le juge (qui lit l'état) constate la
    # divergence — l'oracle échoue SI la falsification était indétectable
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
