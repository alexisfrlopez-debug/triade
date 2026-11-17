#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""oracle_unite01_v181.py — L'ORACLE DU BLOC loupe-01, L'ÉDITION MÉMO SCELLÉ
(l'instruction vljfs6pcj, les leviers (a)/(b)/(c) du plan
PLAN-vljfs6pcj-M4.md) — LES MÊMES VECTEURS, LE MÊME JUGE, LE MÊME ORDRE
D'IMPRESSION que le v180 (identique ligne à ligne à l'original de campagne,
vérifié à la vague 5) : seule l'OUVERTURE DES SESSIONS PUREMENT
CRYPTOGRAPHIQUES (≥ 64 Kio — le chemin critique mesuré : le témoin 196 Kio)
passe par LE MÉMO SCELLÉ :

  - la CLÉ (levier a) : sha256(empreinte du bloc assemblé ‖ empreinte de
    l'entrée ‖ empreinte du contrat ‖ oracle) — un octet changé n'importe
    où = clé différente = ABSENCE = la session vit ;
  - le RELEVÉ (levier b) : l'état né (rax, l'état propre, le cadre 960 o,
    le panneau 48 o, la position) relevé d'une session vivante, chaîné et
    SIGNÉ Ed25519 (clé de test publique, sceau-I spec § 8) ;
  - le PRÉ-FILTRE NATIF (levier c) : l'attendu (md5, sha256) hashlib —
    ~2 ms pour 196 Kio — confronté au panneau RELEVÉ ; discordance ou
    absence = L'ÉMULATION DE CONFIRMATION court en entier et tranche.

LES CONTÔLES SONT INTÉGRAUX DANS LES DEUX CHEMINS : le juge indépendant
(hashlib, les découpages) juge CHAQUE session — relevée ou vivante — les
mêmes textes, les mêmes verdicts. Les falsifications (V4) et les sessions
bon marché (< 64 Kio : temoin-1, temoin-384, vide, les rejets V2/V3)
demeurent VIVANTES — le mémo n'atteint que le chemin critique mesuré.

Le mémo (chemin par --memo) : chargé VÉRIFIÉ (chaîne + signature, tout
écart = REFUS fail-closed) ; les relevés nouveaux reviennent au parent
(single-writer) qui re-scelle. Les statistiques du mémo vont à stderr —
la console stdout EST la console originale.
"""
from __future__ import annotations

import argparse
import hashlib
import multiprocessing as mp
import os
import struct
import sys

REPO = "/tmp/triade-gh"
sys.path.insert(0, os.path.join(REPO, "loupe"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import harnais_noyau as HN          # noqa: E402
import build_loupe as BL            # noqa: E402
import memo_sessions as MEMO        # noqa: E402

L = HN.L
B4 = HN.B4

NOTATION = os.path.join(REPO, "scripts", "campagne_d204", "unite-01-T",
                        "notation", "loupe-01-ouvrir.asm")
CONTRAT = os.path.join(REPO, "loupe", "I", "loupe-01-ouvrir.md")
ORACLE_ID = "oracle-unite01"

VERTS, ROUGES = 0, 0


def controle(nom: str, ok: bool, detail: str = "") -> None:
    global VERTS, ROUGES
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom}" + (f" — {detail}" if detail else ""))
    VERTS += ok
    ROUGES += not ok


def refus(nom: str, detail: str) -> None:
    print(f"[oracle-unite01] REFUS {nom} : {detail}", file=sys.stderr)
    sys.exit(2)


class EmulationCampagne(HN.Emulation):
    def __init__(self, os_virtuel):
        super().__init__(os_virtuel)
        rva, slot = L.SLOTS_LOUPE["i110001"]
        if not os.path.exists(NOTATION):
            refus("NOTATION-ABSENTE", f"{NOTATION} — construire d'abord")
        octets, metas = B4.assembler_bloc(self.ks, NOTATION, rva, slot)
        self.uc.mem_write(rva, octets)
        self.blobs["i110001"] = (octets, metas)


def ouvrir(emul, chemin: str):
    emul.uc.mem_write(HN.ADRESSE_CHEMIN,
                      chemin.encode("utf-16-le") + b"\x00\x00")
    return emul.appeler(L.LOUPE01_VA, {"rcx": HN.ADRESSE_CHEMIN})


def preparer():
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
    return os_v, emul, temoins


# --- les lectures du cadre RELEVÉ (les miroirs exacts des helpers vivants) ------

def _chemin_releve(cadre: bytes) -> str:
    brut = cadre[0:522]
    fin = brut.find(b"\x00\x00")
    if fin > 0:
        brut = brut[:fin + 1]
    return brut.decode("utf-16-le", errors="replace").rstrip("\x00")


def _u64_releve(cadre: bytes, dec: int) -> int:
    return struct.unpack("<Q", cadre[dec:dec + 8])[0]


def _u32_releve(cadre: bytes, dec: int) -> int:
    return struct.unpack("<I", cadre[dec:dec + 4])[0]


def session_temoin(tache: tuple) -> tuple:
    """UNE session V1 (le témoin nommé) dans SA PROPRE émulation — les deux
    contrôles de l'original, retournés au parent (qui imprime en ordre).
    La session ≥ 64 Kio passe par LE MÉMO : relevé jugé si la clé vit,
    session vivante relevée sinon (le semis) — LES MÊMES CONTRÔLES."""
    nom, memo = tache
    os_v, emul, temoins = preparer()
    donnees = temoins[nom]
    rempl = min(384, len(donnees))
    depots: list = []
    if MEMO.session_memorisable(donnees):
        bloc = emul.blobs["i110001"][0]
        contrat = open(CONTRAT, "rb").read()
        releve, hit, depots = MEMO.ouvrir_memorise(
            emul, os_v, memo, bloc, donnees, contrat, ORACLE_ID, nom,
            lambda e, o, c: ouvrir(e, c))
        cadre = releve["cadre"]
        ok_session = (releve["rax"] == 0 and releve["etat_propre"]
                      and _chemin_releve(cadre) == nom
                      and _u64_releve(cadre, 520) == len(donnees)
                      and _u64_releve(cadre, 536) == 0
                      and _u64_releve(cadre, 544) == 0
                      and _u32_releve(cadre, 552) == rempl
                      and cadre[568:568 + rempl] == donnees[:rempl])
        # LE PRÉ-FILTRE NATIF (c) : l'attendu hashlib (~2 ms) confronté au
        # panneau RELEVÉ — la confirmation vivante n'a couru qu'au semis
        attendu = hashlib.md5(donnees).digest() \
            + hashlib.sha256(donnees).digest()
        ok_panneau = releve["panneau"] == attendu
        return (nom, ok_session, ok_panneau, len(donnees), rempl,
                hit, releve["secondes"], depots)
    # ---- la session bon marché : VIVANTE, l'original INTACT ----
    r = ouvrir(emul, nom)
    ok_session = (r["rax"] == 0 and emul.etat_propre(r)
                  and emul.chemin_cadre() == nom
                  and emul.u64(520) == len(donnees)
                  and emul.u64(536) == 0 and emul.u64(544) == 0
                  and emul.u32(552) == rempl
                  and emul.champ(568, rempl) == donnees[:rempl])
    panneau = emul.panneau()
    attendu = hashlib.md5(donnees).digest() + hashlib.sha256(donnees).digest()
    return (nom, ok_session, panneau == attendu, len(donnees), rempl,
            None, 0.0, [])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--memo", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "memo-sessions-v1.json"))
    args = ap.parse_args()

    # LE MÉMO : chargé VÉRIFIÉ s'il existe (tout écart = REFUS fail-closed),
    # né vide sinon (la semence viendra des sessions vivantes)
    if os.path.exists(args.memo):
        try:
            memo = MEMO.MemoSessions.charger(args.memo)
        except MEMO.MemoRefus as e:
            refus("MÉMO-REFUSÉ", str(e))
    else:
        memo = MEMO.MemoSessions()
        print("[memo] absent — la semence vivante coure (le repli EST "
              "l'émulation complète)", file=sys.stderr)

    print("=== L'ORACLE DU BLOC — l'unité 1 (loupe-01 × bras T) : les "
          "vecteurs du contrat, le juge = le modèle indépendant ===")
    os_v, emul, temoins = preparer()

    # ---- V1 : LE SCÉNARIO — les sessions en parallèle ------------------------
    print("\n-- V1 : le scénario (les trois formes + le vide) --")
    taches = [(nom, memo) for nom in ("temoin-1.bin", "temoin-384.bin",
                                      "temoin-3f.bin")]
    with mp.Pool(3) as pool:
        resultats = pool.map(session_temoin, taches)
    n_hits, depots_tous = 0, []
    for nom, ok_session, ok_panneau, taille, rempl, hit, s_vivante, depots \
            in resultats:
        controle(f"V1:{nom}-la-session-nee-entiere", ok_session,
                 f"le cadre champ à champ : chemin {nom}, taille "
                 f"{taille}, vue 0, curseur 0, remplissage {rempl}, "
                 "le tampon == la découpe du modèle")
        controle(f"V1:{nom}-le-panneau-ne", ok_panneau,
                 "le panneau 48 o == (md5, sha256) hashlib du fichier "
                 "ENTIER")
        if hit is not None:
            n_hits += int(hit)
            depots_tous += depots
            print(f"[memo] {nom} : {'RELEVÉ jugé (le mémo vivant)' if hit else f'session vivante {s_vivante:.1f} s — le semis'}",
                  file=sys.stderr)

    # LE VIDE (révision 3) : séquentiel au parent, le même contrôle — VIVANT
    r = ouvrir(emul, "vide.bin")
    attendu_vide = (hashlib.md5(b"").digest()
                    + hashlib.sha256(b"").digest())
    controle("V1:vide.bin-le-fichier-vide",
             r["rax"] == 0 and emul.etat_propre(r)
             and emul.chemin_cadre() == "vide.bin" and emul.u64(520) == 0
             and emul.u32(552) == 0 and emul.panneau() == attendu_vide,
             "le vide s'ouvre : remplissage 0, le panneau du vide == "
             "(d41d8cd9…, e3b0c442…) — les empreintes du vide")
    HN.fermer_session(emul)

    # ---- V2 : LES REJETS D'OS (VIVANTS — bon marché) -------------------------
    print("\n-- V2 : les rejets d'OS --")
    r = ouvrir(emul, "absent.bin")
    controle("V2:E1-absent", r["rax"] == -2 and emul.etat_propre(r),
             "le chemin absent → -2 ABSENT")
    os_v.declarer("verrouille.bin", HN.FichierVirtuel(contenu=b"\x00" * 16,
                                                      verrouille=True))
    r = ouvrir(emul, "verrouille.bin")
    controle("V2:E2-verrouille", r["rax"] == -7,
             "le fichier tenu par un autre détenteur → -7 VERROUILLÉ")
    os_v.declarer("acces-refuse.bin", HN.FichierVirtuel(contenu=b"\x00" * 16,
                                                        refus_acces=True))
    r = ouvrir(emul, "acces-refuse.bin")
    controle("V2:E3-acces-refuse",
             r["rax"] == -6 and any(c == 5 for _, c in os_v.journal_gle),
             "l'accès refusé → -6 SYSTÈME, gle 5 consigné au journal du "
             "harnais (I4)")
    os_v.journal_gle.clear()

    # ---- V3 : LES BORNES (VIVANTES) ------------------------------------------
    print("\n-- V3 : les bornes de l'argument --")
    os_v.declarer("geant-plus.bin", HN.FichierVirtuel(contenu=None,
                                                      taille=0x80000001))
    avant = os_v.compteurs["CloseHandle"]
    r = ouvrir(emul, "geant-plus.bin")
    controle("V3:Q2-la-borne-2-Gio",
             r["rax"] == -3 and emul.etat_propre(r)
             and os_v.compteurs["CloseHandle"] == avant + 1
             and emul.cadre() == HN.CADRE_VIERGE,
             "la taille 2 Gio + 1 → -3, la poignée REFERMÉE AVANT le "
             "retour (comptée), le cadre re-vierge — jamais une poignée "
             "pendante")
    r = ouvrir(emul, "temoin-384.bin")
    cadre_avant, panneau_avant = emul.cadre(), emul.panneau()
    r2 = ouvrir(emul, "temoin-1.bin")
    controle("V3:E4-la-session-double",
             r["rax"] == 0 and r2["rax"] == -5 and emul.etat_propre(r2)
             and emul.cadre() == cadre_avant
             and emul.panneau() == panneau_avant,
             "l'ouverture sur session ouverte → -5, le cadre ET le "
             "panneau relus identiques — l'ancien fichier INTACT")
    HN.fermer_session(emul)
    nom_long = "A" * 260
    os_v.declarer(nom_long, HN.FichierVirtuel(contenu=b"\x00" * 16))
    r = ouvrir(emul, nom_long)
    controle("V3:P1-le-chemin-trop-long",
             r["rax"] == -5 and emul.champ(0, 4) == b"\x00\x00\x00\x00",
             "260 caractères sans NUL → -5 (l'argument invalide), RIEN au "
             "cadre — jamais un débordement")

    # ---- V4 : LA FALSIFICATION DEMANDÉE (VIVANTE) ----------------------------
    print("\n-- V4 : la falsification demandée --")
    r = ouvrir(emul, "temoin-384.bin")
    emul.ecrire_cadre(520, (384 + 1).to_bytes(8, "little"))
    modele_taille = 384                    # le modèle : le témoin ouvert
    cadre_taille = emul.u64(520)           # le cadre : l'état muté
    ecran_modele = f"taille={modele_taille} remplissage={min(384, modele_taille)}"
    ecran_cadre = f"taille={cadre_taille} remplissage={min(384, cadre_taille)}"
    divergence = ecran_modele != ecran_cadre
    controle("V4:la-taille-mutee-l-ecran-attendu-diverge", divergence,
             f"la taille mutée 384 → {cadre_taille} au cadre : l'écran "
             f"attendu (« {ecran_modele} ») DIVERGE de l'état lu "
             f"(« {ecran_cadre} ») — l'oracle à scénarios échoue, LA "
             "FALSIFICATION DEMANDÉE : le juge lit l'état, jamais le modèle")
    HN.fermer_session(emul)

    # ---- LE SCELLEMENT DU MÉMO (single-writer : le parent) --------------------
    if depots_tous:
        for cle, valeur in depots_tous:
            memo.deposer(cle, valeur)
        infos = memo.sceller(args.memo)
        print(f"[memo] scellé : {infos['n']} entrées, racine "
              f"{infos['racine'][:16]}…, {n_hits} relevé(s) jugé(s) "
              "sur 1 session ≥ 64 Kio", file=sys.stderr)

    print(f"\n=== L'ORACLE DU BLOC : {VERTS} VERT, {ROUGES} ROUGE "
          f"{'— VERT' if ROUGES == 0 else '— ROUGE'} ===")
    return 0 if ROUGES == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
