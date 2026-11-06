#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""maj_plan_m9j.py — LE PLAN mis à jour : la rangée (f) du chantier M9
(le terrain — la session réelle) reçoit LE KIT DÉPOSÉ (l'erratum n° 5 +
le build 1.0.0-dev.2 + le kit au coffre) ; l'État du programme reçoit la
phrase du geste. Rejeu REFUSÉ ; tout ancrage absent ou compté autrement
qu'UNE fois = ÉCHEC NOMMÉ, rien n'est écrit."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"

# --- la rangée (f) : la colonne Contenu reçoit le kit déposé -------------------

ANCIEN_F = ("le kit au coffre `/test` (l'artefact + le scénario : la "
            "session TLS 1.3 avec un serveur réel — la suite arrêtée "
            "proposée, le VRAI ntdll lu par sys-02, les sockets par "
            "syscalls, l'épinglage de l'empreinte attendue, la ligne "
            "applicative chiffrée échangée) ; le run, les preuves au "
            "coffre, le recoup sur pièces (D138/D145/D148) ; si vert : la "
            "finale `1.0.0` |")

NOUVEAU_F = ("le kit au coffre `/test` (l'artefact + le scénario : la "
             "session TLS 1.3 avec un serveur réel — la suite arrêtée "
             "proposée, le VRAI ntdll lu par sys-02, les sockets par "
             "syscalls, l'épinglage de l'empreinte attendue, la ligne "
             "applicative chiffrée échangée) ; le run, les preuves au "
             "coffre, le recoup sur pièces (D138/D145/D148) ; si vert : la "
             "finale `1.0.0` ; **LE KIT DÉPOSÉ le 06/11/2026 (Entrée 179, "
             "Task 97)** : l'erratum n° 5 nommé par LA SONDE DU LABO avant "
             "le kit (l'octet de longueur du record CH `0x76`→`0x72` : le "
             "vol de dev.1 recevait le SILENCE de google/github/"
             "cloudflare/debian TOUS, preuve sur pièces ; LE CCS hérité "
             "`14 03 03 00 01 01` que les serveurs émettent TOUS entre le "
             "ServerHello et le vol — RFC 8446 § 4.1.3 : IGNORÉ désormais, "
             "un faux CCS [longueur ≠ 1] reste le refus -2 NOMMÉ ; les "
             "verdicts internes en 64 BITS — la frontière du kit) RÉPARÉ À "
             "LA SOURCE (les arbres I INTACTS : la spec scellée disait "
             "« 114 », la notation seule était fautive ; le garde 13/13 "
             "re-passé VERT ; le slot de tls13-27 ré-arrêté 0xBC0, le "
             "socle 28 déplacé 0x10D00 après les fixtures — les 26 autres "
             "blocs byte-identiques) ; le harnais 54/54 × 3 graines ; LE "
             "BUILD 1.0.0-dev.2 NÉ (65 024 o, sha256 d8928934…, "
             "DÉTERMINISTE ; la carte GÉNÉRATION 10, le verrou croisé "
             "86/86 ; l'octet 0x72 relu DANS L'IMAGE @0x10082) ; "
             "kit-m9f.zip DÉPOSÉ à la racine du /test (md5 a73fb526… "
             "MATCH relu) + LISEZMOI-m9f.txt + preuves-m9f/ NÉ (le "
             "réceptacle) ; la vague m8d CONSOMMÉE archivée → vagues-m8/ ; "
             "LA CIBLE FIGÉE : www.cloudflare.com:443 — l'empreinte "
             "épinglée 045d0758… (LE VRAI certificat CN=www.cloudflare.com "
             "[Let's Encrypt YR2, RSA-2048, valide → 2027-01-30] servi "
             "SANS SNI, 3 sessions consécutives identiques), le témoin "
             "« HTTP/1.1 200 OK » |")

# --- l'État du programme : la phrase du geste ---------------------------------

ANCIEN_ETAT = ("reste (f) le terrain — LA GRANDE ŒUVRE → la finale "
               "1.0.0** Les chantiers M6-(a)")

NOUVEL_ETAT = ("reste (f) le terrain — LA GRANDE ŒUVRE → la finale 1.0.0** "
               "**LE KIT TERRAIN (f) DÉPOSÉ AU COFFRE le 06/11/2026 "
               "(Entrée 179, Task 97) : l'erratum n° 5 [LA SONDE DU LABO "
               "AVANT LE KIT : l'octet de longueur du record CH 0x76 → "
               "0x72 — le SILENCE des serveurs réels prouvé sur pièces ; "
               "LE CCS hérité ignoré — RFC 8446 § 4.1.3, les serveurs "
               "réels l'émettent TOUS ; les verdicts internes en 64 bits "
               "— la frontière du kit] NOMMÉ ET RÉPARÉ À LA SOURCE [les "
               "arbres I INTACTS — la spec disait 114, la notation seule "
               "était fautive, le garde 13/13 re-passé VERT] ; LE BUILD "
               "1.0.0-dev.2 NÉ [65 024 o, sha256 d8928934…, DÉTERMINISTE "
               "deux builds ; la carte GÉNÉRATION 10, le verrou croisé "
               "86/86 ; le harnais poignée 54/54 × 3 graines ; les octets "
               "réparés relus dans l'image] ; LE KIT DÉPOSÉ [kit-m9f.zip "
               "34 759 o, md5 a73fb526… MATCH relu + LISEZMOI-m9f.txt ; "
               "preuves-m9f/ né ; la vague m8d archivée → vagues-m8/ ; LA "
               "CIBLE FIGÉE : www.cloudflare.com:443, l'empreinte épinglée "
               "045d0758… {le certificat Let's Encrypt servi SANS SNI, "
               "3 sessions identiques}, le témoin « HTTP/1.1 200 OK »] ; "
               "reste LE GESTE DU DÉVELOPPEUR [python scenario-m9f.py, "
               "réseau vivant, ~10 s → preuves-m9f/ au coffre → le "
               "recoup D138/D145/D148] — si vert : la finale 1.0.0, le "
               "jalon M9 franchi** Les chantiers M6-(a)")


def remplacer(texte, ancien, nouveau, nom):
    n = texte.count(ancien)
    if n != 1:
        sys.exit(f"ÉCHEC : ancrage {nom} compté {n} fois (attendu : 1) — "
                 "rien n'est écrit")
    return texte.replace(ancien, nouveau, 1)


def main():
    if not PLAN.exists():
        sys.exit("ÉCHEC : plan introuvable")
    plan = PLAN.read_text(encoding="utf-8")
    if "LE KIT DÉPOSÉ le 06/11/2026 (Entrée 179" in plan:
        sys.exit("ÉCHEC : la rangée (f) porte déjà le kit (rejeu REFUSÉ)")
    if ANCIEN_F not in plan:
        sys.exit("ÉCHEC : la rangée (f) courante introuvable")
    if ANCIEN_ETAT not in plan:
        sys.exit("ÉCHEC : l'ancre de l'État du programme introuvable")

    plan = remplacer(plan, ANCIEN_F, NOUVEAU_F, "rangée (f)")
    plan = remplacer(plan, ANCIEN_ETAT, NOUVEL_ETAT, "État du programme")
    PLAN.write_text(plan, encoding="utf-8")

    relu = PLAN.read_text(encoding="utf-8")
    assert "LE KIT DÉPOSÉ le 06/11/2026 (Entrée 179, Task 97)" in relu
    assert "d8928934…" in relu          # le sha du build dev.2 (abrégé, l'usage du plan)
    assert "045d0758…" in relu          # l'empreinte épinglée (abrégée)
    assert relu.count("kit-m9f.zip") >= 2
    print("[plan] la rangée (f) porte LE KIT DÉPOSÉ (l'erratum n° 5, le "
          "build dev.2, la cible figée)")
    print("[plan] l'État du programme porte la phrase du geste (Entrée 179)")
    print("[plan] ORDRE et ANCRAGES constatés — rien d'autre n'a bougé")
    return 0


if __name__ == "__main__":
    sys.exit(main())
