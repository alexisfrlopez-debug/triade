#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""oracle_unite01_v180.py — L'ORACLE DU BLOC loupe-01, L'ÉDITION PARALLÈLE
(l'instruction mof9q10vq, la vague 5) — LES MÊMES VECTEURS, LE MÊME JUGE,
LE MÊME ORDRE D'IMPRESSION : seules les QUATRE sessions de V1 (les trois
témoins et le vide) courent en TRAVAILLEURS CONCURRENTS — chacune sa
propre émulation Unicorn (vivante pour sa session : le pool persistant
par travailleur). V2/V3/V4 courent séquentiellement au parent (le même
déroulé que l'original). Les textes de contrôles sont COPIÉS DE
l'original — la console est comparable ligne à ligne.
"""
from __future__ import annotations

import hashlib
import multiprocessing as mp
import os
import sys

REPO = "/tmp/triade-gh"
sys.path.insert(0, os.path.join(REPO, "loupe"))

import harnais_noyau as HN          # noqa: E402
import build_loupe as BL            # noqa: E402

L = HN.L
B4 = HN.B4

NOTATION = os.path.join(REPO, "scripts", "campagne_d204", "unite-01-T",
                        "notation", "loupe-01-ouvrir.asm")

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


def session_temoin(nom: str) -> tuple:
    """UNE session V1 (le témoin nommé) dans SA PROPRE émulation — les deux
    contrôles de l'original, retournés au parent (qui imprime en ordre)."""
    os_v, emul, temoins = preparer()
    donnees = temoins[nom]
    r = ouvrir(emul, nom)
    rempl = min(384, len(donnees))
    ok_session = (r["rax"] == 0 and emul.etat_propre(r)
                  and emul.chemin_cadre() == nom
                  and emul.u64(520) == len(donnees)
                  and emul.u64(536) == 0 and emul.u64(544) == 0
                  and emul.u32(552) == rempl
                  and emul.champ(568, rempl) == donnees[:rempl])
    panneau = emul.panneau()
    attendu = hashlib.md5(donnees).digest() + hashlib.sha256(donnees).digest()
    return (nom, ok_session, panneau == attendu, len(donnees), rempl)


def main() -> int:
    print("=== L'ORACLE DU BLOC — l'unité 1 (loupe-01 × bras T) : les "
          "vecteurs du contrat, le juge = le modèle indépendant ===")
    os_v, emul, temoins = preparer()

    # ---- V1 : LE SCÉNARIO — les sessions en parallèle ------------------------
    print("\n-- V1 : le scénario (les trois formes + le vide) --")
    with mp.Pool(3) as pool:
        resultats = pool.map(session_temoin,
                             ("temoin-1.bin", "temoin-384.bin",
                              "temoin-3f.bin"))
    for nom, ok_session, ok_panneau, taille, rempl in resultats:
        controle(f"V1:{nom}-la-session-nee-entiere", ok_session,
                 f"le cadre champ à champ : chemin {nom}, taille "
                 f"{taille}, vue 0, curseur 0, remplissage {rempl}, "
                 "le tampon == la découpe du modèle")
        controle(f"V1:{nom}-le-panneau-ne", ok_panneau,
                 "le panneau 48 o == (md5, sha256) hashlib du fichier "
                 "ENTIER")

    # LE VIDE (révision 3) : séquentiel au parent, le même contrôle
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

    # ---- V2 : LES REJETS D'OS -------------------------------------------------
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

    # ---- V3 : LES BORNES ------------------------------------------------------
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

    # ---- V4 : LA FALSIFICATION DEMANDÉE ---------------------------------------
    print("\n-- V4 : la falsification demandée --")
    r = ouvrir(emul, "temoin-384.bin")
    emul.ecrire_cadre(520, (384 + 1).to_bytes(8, "little"))
    modele_taille = 384
    cadre_taille = emul.u64(520)
    ecran_modele = f"taille={modele_taille} remplissage={min(384, modele_taille)}"
    ecran_cadre = f"taille={cadre_taille} remplissage={min(384, cadre_taille)}"
    divergence = ecran_modele != ecran_cadre
    controle("V4:la-taille-mutee-l-ecran-attendu-diverge", divergence,
             f"la taille mutée 384 → {cadre_taille} au cadre : l'écran "
             f"attendu (« {ecran_modele} ») DIVERGE de l'état lu "
             f"(« {ecran_cadre} ») — l'oracle à scénarios échoue, LA "
             "FALSIFICATION DEMANDÉE : le juge lit l'état, jamais le modèle")
    HN.fermer_session(emul)

    print(f"\n=== L'ORACLE DU BLOC : {VERTS} VERT, {ROUGES} ROUGE "
          f"{'— VERT' if ROUGES == 0 else '— ROUGE'} ===")
    return 0 if ROUGES == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
