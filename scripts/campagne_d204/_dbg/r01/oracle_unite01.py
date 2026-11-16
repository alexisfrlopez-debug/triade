#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""oracle_unite01.py — L'ORACLE DU BLOC AU PÉRIMÈTRE LIVRÉ, l'unité 1
(loupe-01 × bras T, la commande M4 n° 3 du plan D204).

LES VECTEURS DEPUIS LE CONTRAT (loupe/I/loupe-01-ouvrir.md — l'oracle
régénéré depuis I, écrit-avant-code) : le juge est le MODÈLE INDÉPENDANT
Python (hashlib, les découpes), JAMAIS les octets du bloc — le harnais du
domaine (harnais_noyau.Emulation : le mini-OS, les shims, les sentinelles)
porte la pièce de campagne au slot loupe-01, les DIX-SEPT autres blocs
demeurant les scellés (la session née ENTIÈRE exige ses appelés).

  V1 (le scénario du contrat)   : les TROIS formes du remplissage (1 o,
      384 o, 3 × 64 Kio + 1) + LE VIDE — le cadre champ à champ (le chemin
      COPIÉ, la taille, la vue 0, le curseur 0, le remplissage
      min(384, taille)), le tampon == la découpe du témoin, le panneau ==
      (md5, sha256) hashlib, le vide SANS fenêtre ;
  V2 (les rejets d'OS)          : absent → -2, verrouillé → -7, accès
      refusé → -6 (gle consigné au journal du harnais) ;
  V3 (les bornes de l'argument) : la taille 2 Gio + 1 → -3 la poignée
      FERMÉE AVANT le retour (comptée), le cadre re-vierge ; la session
      double → -5 RIEN TOUCHÉ ; le chemin de 260 sans NUL → -5, RIEN au
      cadre ;
  V4 (la falsification demandée): la taille mutée d'un octet au cadre
      après l'ouverture — l'écran attendu (composé du modèle) DIVERGE,
      l'oracle échoue : LA FALSIFICATION DEMANDÉE, charte § 3 (le juge
      lit l'état, jamais le modèle).

Usage : python3 scripts/campagne_d204/unite-01-T/oracle_unite01.py
Sortie : 0 = oracle VERT (falsification comprise) ; 2 = refus nommé.
"""
from __future__ import annotations

import hashlib
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
UNITE = os.path.join(REPO, "scripts", "campagne_d204", "unite-01-T")
sys.path.insert(0, os.path.join(REPO, "loupe"))

import harnais_noyau as HN          # noqa: E402  (le harnais du domaine)
import build_loupe as BL            # noqa: E402  (B4 : le lecteur canonique)

L = HN.L
B4 = HN.B4

NOTATION = os.path.join(UNITE, "notation", "loupe-01-ouvrir.asm")

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
    """Le harnais du domaine au slot loupe-01 PORTANT LA PIÈCE DE CAMPAGNE :
    les dix-sept autres blocs demeurent les notations scellées (lues à leurs
    arbres — la session née ENTIÈRE exige ses appelés au plan)."""

    def __init__(self, os_virtuel):
        super().__init__(os_virtuel)
        rva, slot = L.SLOTS_LOUPE["i110001"]
        if not os.path.exists(NOTATION):
            refus("NOTATION-ABSENTE", f"{NOTATION} — construire d'abord")
        octets, metas = B4.assembler_bloc(self.ks, NOTATION, rva, slot)
        self.uc.mem_write(rva, octets)
        self.blobs["i110001"] = (octets, metas)


def ouvrir(emul: HN.Emulation, chemin: str):
    """L'appel de loupe-01 au chemin donné (le geste réel de la campagne)."""
    emul.uc.mem_write(HN.ADRESSE_CHEMIN,
                      chemin.encode("utf-16-le") + b"\x00\x00")
    return emul.appeler(L.LOUPE01_VA, {"rcx": HN.ADRESSE_CHEMIN})


def main() -> int:
    print("=== L'ORACLE DU BLOC — l'unité 1 (loupe-01 × bras T) : les "
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

    # LES TÉMOINS DU KIT (les trois formes du remplissage — la génération
    # FIXE du harnais, graine 20261107 : les témoins ne changent jamais)
    temoins = HN.composer_temoins()
    for nom, contenu in (("temoin-1.bin", temoins["temoin-1.bin"]),
                         ("temoin-384.bin", temoins["temoin-384.bin"]),
                         ("temoin-3f.bin", temoins["temoin-3f.bin"])):
        os_v.declarer(nom, HN.FichierVirtuel(contenu=contenu))
    os_v.declarer("vide.bin", HN.FichierVirtuel(contenu=b""))

    # ---- V1 : LE SCÉNARIO — la session née entière, champ à champ --------------
    print("\n-- V1 : le scénario (les trois formes + le vide) --")
    for nom, donnees in (("temoin-1.bin", temoins["temoin-1.bin"]),
                         ("temoin-384.bin", temoins["temoin-384.bin"]),
                         ("temoin-3f.bin", temoins["temoin-3f.bin"])):
        r = ouvrir(emul, nom)
        rempl = min(384, len(donnees))
        ok = (r["rax"] == 0 and emul.etat_propre(r)
              and emul.chemin_cadre() == nom
              and emul.u64(520) == len(donnees)
              and emul.u64(536) == 0 and emul.u64(544) == 0
              and emul.u32(552) == rempl
              and emul.champ(568, rempl) == donnees[:rempl])
        controle(f"V1:{nom}-la-session-nee-entiere", ok,
                 f"le cadre champ à champ : chemin {nom}, taille "
                 f"{len(donnees)}, vue 0, curseur 0, remplissage {rempl}, "
                 "le tampon == la découpe du modèle")
        panneau = emul.panneau()
        attendu = hashlib.md5(donnees).digest() + \
            hashlib.sha256(donnees).digest()
        controle(f"V1:{nom}-le-panneau-ne", panneau == attendu,
                 "le panneau 48 o == (md5, sha256) hashlib du fichier ENTIER")
        HN.fermer_session(emul)
    # LE VIDE (révision 3) : la session née SANS la fenêtre, le panneau défini
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

    # ---- V2 : LES REJETS D'OS (traduits par la table, jamais un code brut) -----
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

    # ---- V3 : LES BORNES (la taille, la session, le chemin) --------------------
    print("\n-- V3 : les bornes de l'argument --")
    os_v.declarer("geant-plus.bin", HN.FichierVirtuel(contenu=None,
                                                      taille=0x80000001))
    avant = os_v.compteurs["CloseHandle"]
    r = ouvrir(emul, "geant-plus.bin")
    controle("V3:Q2-la-borne-2-Gio",
             r["rax"] == -3 and emul.etat_propre(r)
             and os_v.compteurs["CloseHandle"] == avant + 1
             and emul.cadre() == HN.CADRE_VIERGE,
             "la taille 2 Gio + 1 → -3, la poignée REFERMÉE AVANT le retour "
             "(comptée), le cadre re-vierge — jamais une poignée pendante")
    r = ouvrir(emul, "temoin-384.bin")
    cadre_avant, panneau_avant = emul.cadre(), emul.panneau()
    r2 = ouvrir(emul, "temoin-1.bin")
    controle("V3:E4-la-session-double",
             r["rax"] == 0 and r2["rax"] == -5 and emul.etat_propre(r2)
             and emul.cadre() == cadre_avant
             and emul.panneau() == panneau_avant,
             "l'ouverture sur session ouverte → -5, le cadre ET le panneau "
             "relus identiques — l'ancien fichier INTACT")
    HN.fermer_session(emul)
    nom_long = "A" * 260
    os_v.declarer(nom_long, HN.FichierVirtuel(contenu=b"\x00" * 16))
    r = ouvrir(emul, nom_long)
    controle("V3:P1-le-chemin-trop-long",
             r["rax"] == -5 and emul.champ(0, 4) == b"\x00\x00\x00\x00",
             "260 caractères sans NUL → -5 (l'argument invalide), RIEN au "
             "cadre — jamais un débordement")

    # ---- V4 : LA FALSIFICATION DEMANDÉE (charte § 3) ---------------------------
    print("\n-- V4 : la falsification demandée --")
    r = ouvrir(emul, "temoin-384.bin")
    # la taille mutée d'un octet au cadre APRÈS l'ouverture
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

    # ---- LE VERDICT -------------------------------------------------------------
    print(f"\n=== L'ORACLE DU BLOC : {VERTS} VERT, {ROUGES} ROUGE "
          f"{'— VERT' if ROUGES == 0 else '— ROUGE'} ===")
    return 0 if ROUGES == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
