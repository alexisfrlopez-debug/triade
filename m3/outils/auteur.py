#!/usr/bin/env python3
"""auteur.py — Outil d'auteur du jalon M3 : résolution des étiquettes.

Même discipline qu'en M1/M2 (aucun compilateur entre l'intention et les
octets : keystone assemble, rien d'autre) — cet outil fait l'arithmétique
d'adresses de l'auteur : étiquettes locales -> adresses absolues des sauts,
symboles de blocs -> cibles d'appels directes, symboles de données ->
déplacements RIP calculés une fois pour toutes depuis le plan d'adressage M3
(layout.py, D46 arrêté à l'étape b).

NOUVEAUTÉ M3 : le motif « lea reg, [.étiquette] » (adresse d'une étiquette
interne — proc de thread de la pompe du tunnel, http-10) est résolu en
lea reg, [rip + disp] — les adresses 64 bits ne sont pas atteignables par
disp32 absolu, la position-indépendance est la règle du projet (D33).

Entrée : notation/brouillons/*.asm. Sortie : notation/*.asm — notation
explicite WYSIWYG, seule lue par build_m3.py (round-trip R5 sur la sortie).

Usage : python3 outils/auteur.py [--verifier-seulement]
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import layout as L

from keystone import Ks, KS_ARCH_X86, KS_MODE_64

ICI = os.path.dirname(os.path.abspath(__file__))
BROUILLONS = os.path.join(ICI, "..", "notation", "brouillons")
SORTIE = os.path.join(ICI, "..", "notation")

# (fichier brouillon, id bloc, spec, rva, slot, dépendances) — rva/slot dérivés
# du plan d'adressage (layout.py, source unique de vérité).
_FICHIERS = {
    "e50001": ("http-01-ligne", "http-01:R1",
               "feuille pure ; aucun accès extérieur (propriétaire T5 du balayage)"),
    "e50002": ("http-02-requete", "http-02:R1",
               "table des méthodes .rdata (8 entrées + terminateur) ; feuille"),
    "e50003": ("http-03-entete", "http-03:R1",
               "feuille pure ; rognage OWS par bornes uniquement"),
    "e50004": ("http-04-chercher", "http-04:R1",
               "blocs http-01 @0x4C00, http-03 @0x4D80 ; comparaison insensible "
               "à la casse (unique du domaine)"),
    "e50005": ("http-05-nombre", "http-05:R1",
               "feuille pure ; test de borne à chaque chiffre (I2)"),
    "e50006": ("http-06-tete", "http-06:R2",
               "feuille pure ; propriétaire de MAX_TETE 8192 ; rejet LF isolé"),
    "e50007": ("http-07-autorite", "http-07:R1",
               "feuille pure ; assistant local .chiffres_port (pile équilibrée)"),
    "e50008": ("http-08-cible", "http-08:R1",
               "feuille pure ; fixture « / » .rdata (chemin par défaut)"),
    "e50009": ("http-09-pompe", "http-09:R1",
               "blocs tcp-03 @0x4140, tcp-04 @0x4180 — AUCUN autre, jamais tcp-05"),
    "e50010": ("http-10-session", "http-10:R2",
               "blocs tcp-03/04/05/06/11, tcp-13, http-01..09 ; IAT kernel32 "
               "CloseHandle (handle de la pompe détachée) ; chaînes .rdata ; "
               "R2 : corps de requête borné Content-Length INLINE (tcp-03/04), "
               "http-09 réservé au tunnel et au relais de réponse"),
    "e50011": ("http-11-console", "http-11:R1",
               "IAT kernel32 ReadFile ; blocs libc-02, tcp-05, tcp-11 ; "
               "état .data (stdin, listen, quit) ; chaînes .rdata"),
    "e50012": ("http-12-principal", "http-12:R1",
               "IAT kernel32 GSH, InitCS, CloseHandle, ExitProcess ; IAT ws2_32 "
               "WSACleanup ; blocs tcp-01/02/06/11, http-10, http-11, io-02 "
               "write ; table R10 + version .rdata ; état .data"),
    "e50013": ("tcp-13-connexion", "tcp-13:R1",
               "IAT ws2_32 : getaddrinfo, freeaddrinfo, socket, connect, "
               "closesocket ; cadre : hôte 256 o, hints 48 o, sockaddr 16 o"),
}


def blocs_m3() -> list[tuple]:
    out = []
    for bid, (_f, spec, deps) in _FICHIERS.items():
        rva, slot = next((r, s) for b, _, r, s, _, _ in L.BLOCS_M3 if b == bid)
        fichier = _FICHIERS[bid][0]
        out.append((fichier, bid, spec, rva, slot, deps))
    return out


BLOCS = blocs_m3()

SYMBOLES = {
    # blocs hérités (octets scellés M0/M1/M2)
    "WRITE": 0x1040, "EXIT": 0x1080,
    "MEMCPY": 0x1100, "MEMCMP": 0x1180, "STRLEN": 0x1200, "ITOA": 0x1280,
    "ZONE_ALLOC": 0x1300, "ZONE_RESET": 0x1380, "MEMSET": 0x13C0,
    # blocs M2 embarqués
    "TCP_INIT": 0x4000, "TCP_ACCEPT": 0x4100, "TCP_RECV": 0x4140,
    "TCP_SEND": 0x4180, "TCP_CLOSE": 0x41C0, "TCP_SPAWN": 0x4300,
    "TCP_JOURNAL": 0x4B00,
    # blocs M3
    "TCP_CONNEXION": 0x4400, "HTTP_LIGNE": 0x4C00, "HTTP_REQUETE": 0x4C80,
    "HTTP_ENTETE": 0x4E80, "HTTP_CHERCHER": 0x4F40, "HTTP_NOMBRE": 0x5080,
    "HTTP_TETE": 0x5140, "HTTP_AUTORITE": 0x5200, "HTTP_CIBLE": 0x5380,
    "HTTP_POMPE": 0x54C0, "SESSION": 0x5580, "CONSOLE": 0x5D80,
    # IAT kernel32
    "IAT_GSH": L.IAT_SLOTS["GetStdHandle"], "IAT_WF": L.IAT_SLOTS["WriteFile"],
    "IAT_EP": L.IAT_SLOTS["ExitProcess"], "IAT_CREATETHREAD": L.IAT_SLOTS["CreateThread"],
    "IAT_VPROTECT": L.IAT_SLOTS["VirtualProtect"],
    "IAT_ICS": L.IAT_SLOTS["InitializeCriticalSection"],
    "IAT_ECS": L.IAT_SLOTS["EnterCriticalSection"],
    "IAT_LCS": L.IAT_SLOTS["LeaveCriticalSection"],
    "IAT_READFILE": L.IAT_SLOTS["ReadFile"], "IAT_CH": L.IAT_SLOTS["CloseHandle"],
    # IAT ws2_32
    "IAT_WSASTARTUP": L.IAT_SLOTS["WSAStartup"], "IAT_SOCKET": L.IAT_SLOTS["socket"],
    "IAT_BIND": L.IAT_SLOTS["bind"], "IAT_LISTEN": L.IAT_SLOTS["listen"],
    "IAT_ACCEPT": L.IAT_SLOTS["accept"], "IAT_RECV": L.IAT_SLOTS["recv"],
    "IAT_SEND": L.IAT_SLOTS["send"], "IAT_CLOSESOCK": L.IAT_SLOTS["closesocket"],
    "IAT_WSAGLE": L.IAT_SLOTS["WSAGetLastError"],
    "IAT_WSACLEANUP": L.IAT_SLOTS["WSACleanup"],
    "IAT_GETADDRINFO": L.IAT_SLOTS["getaddrinfo"],
    "IAT_FREEADDRINFO": L.IAT_SLOTS["freeaddrinfo"],
    "IAT_CONNECT": L.IAT_SLOTS["connect"],
    # données .rdata (M3)
    "TAB_METHODES": L.R_TAB_METHODES, "SLASH": L.R_SLASH,
    "TXT_400": L.R_TXT_400, "TXT_431": L.R_TXT_431, "TXT_501": L.R_TXT_501,
    "TXT_411": L.R_TXT_411, "TXT_505": L.R_TXT_505, "TXT_502": L.R_TXT_502,
    "TXT_TUNNEL": L.R_TXT_TUNNEL,
    "TAB_SUM": L.R_TAB_SUM,
    "TAB_TAILLE": L.R_TAB_SUM + 4,
    "TAB_SOMME": L.R_TAB_SUM + 8,
    "VERSION": L.R_VERSION,
    "ANCRE": L.R_ANCRE,
    "MSG_BANNIERE": L.R_MSG_BANNIERE, "MSG_CONNEXION": L.R_MSG_CONNEXION,
    "MSG_TUNNEL": L.R_MSG_TUNNEL, "MSG_FIN": L.R_MSG_FIN,
    "MSG_ARRET": L.R_MSG_ARRET, "MSG_INCONNU": L.R_MSG_INCONNU,
    "MSG_ERREUR": L.R_MSG_ERREUR, "MSG_KO": L.R_MSG_KO,
    "CMD_QUIT": L.R_CMD_QUIT, "NOM_HOST": L.R_NOM_HOST,
    "NOM_CL": L.R_NOM_CL, "NOM_TE": L.R_NOM_TE,
    # état .data (M2 réutilisé)
    "STDOUT": L.R_STDOUT, "STDIN": L.R_STDIN, "LISTEN": L.R_LISTEN,
    "QUIT": L.R_QUIT, "CS": L.R_CS,
    "CURSEUR": L.R_CURSEUR, "ARENE": L.ARENE_BASE,
}

RE_ETIQUETTE = re.compile(r"^\s*\.(\w+)\s*:\s*$")
RE_OPERANDE_ETIQUETTE = re.compile(r"^(j\w+|loop\w*|call)\s+\.(\w+)$")
RE_OPERANDE_SYMBOLE = re.compile(r"^(call)\s+(\w+)$")
RE_LEA_ETIQUETTE = re.compile(r"^(lea\s+\w+), \[\.(\w+)\]$")
# RIP-relatif : symbole OU étiquette locale (préfixée d'un point — M3)
RE_RIP_CIBLE = re.compile(r"^(.*?\[rip\s*([+-])\s*)(\w+|\.\w+)(\s*\].*)$")


class ErreurAuteur(Exception):
    pass


def lire_brouillon(chemin: str):
    instructions, etiquettes_lignes = [], []
    with open(chemin, encoding="utf-8") as f:
        for numero, brut in enumerate(f.read().splitlines(), 1):
            ligne = brut.split(";")[0].strip()
            if not ligne:
                continue
            m = RE_ETIQUETTE.match(ligne)
            if m:
                etiquettes_lignes.append((m.group(1), len(instructions)))
                continue
            instructions.append((ligne, numero))
    return instructions, etiquettes_lignes


def cible_rip(nom: str, etiquettes: dict):
    """Résout un nom d'opérande RIP : étiquette locale (.nom) ou symbole."""
    if nom.startswith("."):
        if nom[1:] not in etiquettes:
            raise ErreurAuteur(f"étiquette inconnue : {nom}")
        return etiquettes[nom[1:]]
    if nom not in SYMBOLES:
        raise ErreurAuteur(f"symbole de données inconnu : {nom}")
    return SYMBOLES[nom]


def taille_ligne(ks: Ks, ligne: str, adresse: int, etiquettes: dict, base: int) -> int:
    enc, _ = ks.asm(substituer(ligne, adresse, etiquettes, base, taille=True), adresse)
    if not enc:
        raise ErreurAuteur(f"ligne inassemblable (calcul de taille) : {ligne!r}")
    return len(enc)


def substituer(ligne: str, adresse: int, etiquettes: dict, base: int, taille: int = 0) -> str:
    # lea reg, [.étiquette] -> lea reg, [rip + 0x0] (taille) / résolu plus tard
    m = RE_LEA_ETIQUETTE.match(ligne)
    if m:
        if taille:
            return f"{m.group(1)}, [rip + 0x0]"
        return ligne
    m = RE_OPERANDE_ETIQUETTE.match(ligne)
    if m:
        mnemo, nom = m.groups()
        cible = etiquettes.get(nom)
        if cible is None:
            raise ErreurAuteur(f"étiquette inconnue : .{nom}")
        return f"{mnemo} 0x{cible:x}"
    m = RE_OPERANDE_SYMBOLE.match(ligne)
    if m:
        mnemo, nom = m.groups()
        if nom not in SYMBOLES:
            raise ErreurAuteur(f"symbole de bloc inconnu : {nom}")
        return f"{mnemo} 0x{SYMBOLES[nom]:x}"
    m = RE_RIP_CIBLE.match(ligne)
    if m and m.group(3) in SYMBOLES:      # symboles uniquement (pas étiquettes)
        avant, signe, nom, apres = m.groups()
        if taille:
            # « avant » contient déjà le signe : ne pas le répéter
            return f"{avant}0x0{apres}"
    return ligne


def resoudre_rip(ligne: str, adresse: int, taille: int, etiquettes: dict) -> str:
    m = RE_LEA_ETIQUETTE.match(ligne)
    if m:
        cible = etiquettes.get(m.group(2))
        if cible is None:
            raise ErreurAuteur(f"étiquette inconnue : .{m.group(2)}")
        disp = cible - (adresse + 7)      # lea reg, [rip + disp32] = 7 octets
        if disp >= 0:
            return f"{m.group(1)}, [rip + 0x{disp:x}]"
        return f"{m.group(1)}, [rip - 0x{-disp:x}]"
    m = RE_RIP_CIBLE.match(ligne)
    if not m:
        return ligne
    avant, signe, nom, apres = m.groups()
    if signe == "-":
        # les brouillons n'emploient que la forme « [rip + SYM] » — refus
        # explicite de l'autre forme (l'auteur garde une seule convention)
        raise ErreurAuteur(f"forme [rip - symbole] non supportée : {ligne!r}")
    cible = cible_rip(nom, etiquettes)
    disp = cible - (adresse + taille)
    if disp >= 0:
        return f"{avant}0x{disp:x}{apres}"
    return f"{avant[:avant.rindex('+')]}- 0x{-disp:x}{apres}"


def resoudre_bloc(ks: Ks, fichier: str, bid: str, spec: str, rva: int, slot: int, deps: str):
    chemin = os.path.join(BROUILLONS, fichier + ".asm")
    instructions, etiquettes_lignes = lire_brouillon(chemin)
    if not instructions:
        raise ErreurAuteur(f"{fichier} : brouillon vide")

    etiquettes = {nom: rva + 0x800 for nom, _ in etiquettes_lignes}
    # 8 passes (M2 : 4) — les sauts courts keystone (choix automatique rel8
    # versus rel32) allongent la convergence des blocs denses de M3 ; un
    # éventuel cycle court/near est cassé par l'amortissement naturel des
    # positions (les tailles ne font que se rapprocher du point fixe).
    for _ in range(8):
        tailles, adresse = [], rva
        for ligne, _ in instructions:
            t = taille_ligne(ks, ligne, adresse, etiquettes, rva)
            tailles.append(t)
            adresse += t
        nouvelles = {}
        for nom, index in etiquettes_lignes:
            nouvelles[nom] = rva + sum(tailles[:index])
        if nouvelles == etiquettes:
            break
        etiquettes = nouvelles
    else:
        raise ErreurAuteur(f"{fichier} : pas de point fixe en 4 passes")

    lignes_sortie, adresse, calculs = [], rva, []
    for ligne, numero in instructions:
        taille = tailles[len(lignes_sortie)]
        explicite = resoudre_rip(
            substituer(ligne, adresse, etiquettes, rva), adresse, taille, etiquettes)
        lignes_sortie.append((explicite, adresse, taille, numero))
        adresse += taille
    total = adresse - rva
    if total > slot:
        raise ErreurAuteur(f"{fichier} : {total} o > slot {slot:#x} (D8)")
    if slot - total < 16:
        raise ErreurAuteur(f"{fichier} : padding {slot - total} < 16 (D8)")

    entete = [
        f"; {fichier} · bloc {NOMS_COURTS.get(fichier, fichier)} · spec {spec} · bloc carte {bid}",
        f"; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x{rva:x}, taille {slot} octets",
        f"; Dépendances : {deps}",
        f"; Notation explicite générée par outils/auteur.py depuis brouillons/{fichier}.asm",
        f"; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)",
        f"; Code : {total} o · padding : {slot - total} o (NOP)",
    ]
    if etiquettes_lignes:
        entete.append("; Étiquettes résolues : " + ", ".join(
            f".{nom}=0x{etiquettes[nom]:x}" for nom, _ in etiquettes_lignes))
    refs = [l for l, *_ in lignes_sortie if "[rip" in l]
    if refs:
        entete.append("; Déplacements RIP (cible = adresse + taille + disp) :")
        for ligne_e, adr, t, _ in lignes_sortie:
            m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", ligne_e)
            if m:
                cible = adr + t + (int(m.group(2), 16) if m.group(1) == "+" else -int(m.group(2), 16))
                entete.append(f";   0x{adr:x} + 0x{t:x} {m.group(1)} {m.group(2)} = 0x{cible:x}")

    chemin_sortie = os.path.join(SORTIE, fichier + ".asm")
    with open(chemin_sortie, "w", encoding="utf-8") as f:
        f.write("\n".join(entete) + "\n")
        for ligne_e, *_ in lignes_sortie:
            f.write(ligne_e + "\n")
    return total, len(instructions), len(etiquettes_lignes)


NOMS_COURTS = {
    "http-01-ligne": "itérateur de ligne CRLF",
    "http-02-requete": "ligne de requête",
    "http-03-entete": "ligne d'en-tête",
    "http-04-chercher": "recherche d'en-tête",
    "http-05-nombre": "décimal borné",
    "http-06-tete": "détection de fin de tête",
    "http-07-autorite": "autorité hôte:port",
    "http-08-cible": "cible (forme)",
    "http-09-pompe": "pompe unidirectionnelle",
    "http-10-session": "session proxy",
    "http-11-console": "console",
    "http-12-principal": "orchestration proxy (point d'entrée)",
    "tcp-13-connexion": "connexion cliente résolue",
}


def main(verifier_seulement: bool) -> int:
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    print("=== outils/auteur.py : résolution des étiquettes (jalon M3) ===")
    for fichier, bid, spec, rva, slot, deps in BLOCS:
        chemin = os.path.join(BROUILLONS, fichier + ".asm")
        if not os.path.exists(chemin):
            print(f"[absent] {fichier} : brouillon absent, ignoré (attendu selon la phase)")
            continue
        total, n, e = resoudre_bloc(ks, fichier, bid, spec, rva, slot, deps)
        print(f"[ok] {fichier} ({bid}) : {total} o, {n} instructions, "
              f"{e} étiquettes, {slot - total} o de padding")
    if not verifier_seulement:
        print("Notation explicite écrite dans notation/*.asm")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verifier-seulement" in sys.argv))
