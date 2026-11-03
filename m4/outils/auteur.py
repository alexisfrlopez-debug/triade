#!/usr/bin/env python3
"""auteur.py — Outil d'auteur du jalon M4 : résolution des étiquettes.

Même discipline qu'en M1/M2/M3 (aucun compilateur entre l'intention et les
octets : keystone assemble, rien d'autre) — cet outil fait l'arithmétique
d'adresses de l'auteur : étiquettes locales -> adresses absolues des sauts,
symboles de blocs -> cibles d'appels directes, symboles de données ->
déplacements RIP calculés une fois pour toutes depuis le plan d'adressage M4
(layout.py — arrêts D79/D81 : trois feuilles pures + tls-05 mesuré, l'extension
.rdata secur32 ARRÊTÉE D81 [IAT/INT/hints/fixture package], la suite reste
préfigurée jusqu'à la fin de l'étape b).

Entrée : notation/brouillons/*.asm. Sortie : notation/*.asm — notation
explicite WYSIWYG, seule lue par build_m4.py (round-trip R5 sur la sortie).

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

# (fichier brouillon, id bloc, spec, dépendances) — rva/slot dérivés du plan
# d'adressage (layout.py, source unique de vérité). Les trois feuilles pures
# existent (D79) ; les suivantes sont attendues au fil de l'étape b.
_FICHIERS = {
    "g70001": ("tls-01-nom-utf16", "tls-01:R1",
               "feuille pure ; propriétaire T5 de la traduction span → UTF-16 "
               "(HOTE_MAX 255, octets >= 0x80 refusés)"),
    "g70002": ("tls-02-verdicts", "tls-02:R1",
               "feuille pure ; table TOTALE des verdicts SSPI — liste blanche "
               "13 codes (layout.HRESULTS), domaine = HRESULT 32 bits "
               "sign-étendu, hors domaine = verdict 6"),
    "g70003": ("tls-03-jetons", "tls-03:R1",
               "feuille pure ; propriétaire T5 de la mise en page SecBufferDesc/"
               "SecBuffer (types 0/1/2, MAX_JETON 16384, tailles de flux en "
               "[rsp+0x28] pour le type 1 — convention cadre contigu : en-tête "
               "AVANT le clair, queue APRÈS)"),
    "g70004": ("tls-04-poignee", "tls-04:R1",
               "boucle ISC bornée 16 allers ; IAT secur32 "
               "InitializeSecurityContextW ; tls-01/02/03"),
    "g70005": ("tls-05-cles", "tls-05:R2",
               "IAT secur32 AcquireCredentialsHandleW / FreeCredentialsHandle / "
               "DeleteSecurityContext ; compensation exacte ; SCH_CREDENTIALS "
               "explicite dwVersion=5 dwFlags=0 (P3/R2, D140) ; cadre aux offsets "
               "documentés (layout.CADRE_*, arrêt D81)"),
    "g70006": ("tls-06-emission", "tls-06:R1",
               "IAT secur32 QueryContextAttributesW / EncryptMessage ; tcp-04 ; "
               "tls-03 type 1 ; tailles négociées"),
    "g70007": ("tls-07-reception", "tls-07:R2",
               "IAT secur32 DecryptMessage ; tls-03 type 2 ; tls-02 ; "
               "libc-01 normalisation ; résidu Extra à propriétaire unique "
               "(la réception tcp-03 est l'affaire de l'APPELANT tls-08)"),
    "g70008": ("tls-08-session", "tls-08:R1",
               "orchestration TLS cliente ; tls-01..07, tcp-13, tcp-03/04/05 ; "
               "compensation intégrale constatée par comptage"),
    "g70009": ("http-08-cible-r2", "http-08:R2",
               "RÉVISION (ancêtre e50008 http-08:R1 scellé 0.4.0, cité § 9) : "
               "schéma https:// BYTE-EXACT 8 octets minuscules, verdict TLS "
               "distinct, port 443 ; fixture SLASH"),
    "g70010": ("http-10-session-r2", "http-10:R2",
               "RÉVISION (ancêtre http-10 scellé 0.4.0, cité § 9) : routage "
               "https → tls-08 + table des réponses étendue (certificat "
               "invalide → 502 « certificat rejete »)"),
    "g70011": ("http-12-principal-r2", "http-12:R2",
               "RÉVISION (ancêtre e50012 http-12:R1 scellé 0.4.0, cité § 9) — "
               "LE CÂBLAGE : la boucle lance http-10:R2 (0x74C0) ; la porte R10 "
               "devient marche aux BORNES (28 entrées, l'entrée .text3 "
               "remplace le terminateur @0x2810, fail-closed sur entrée "
               "trouée) ; l'ancêtre @0x1800 reste embarqué (R7)"),
}


def blocs_m4() -> list[tuple]:
    out = []
    tous = L.BLOCS_TLS + L.BLOCS_REVISIONS
    for bid, (_f, spec, deps) in _FICHIERS.items():
        rva, slot = next((r, s) for b, _, r, s, _, _ in tous if b == bid)
        out.append((_FICHIERS[bid][0], bid, spec, rva, slot, deps))
    return out


BLOCS = blocs_m4()

SYMBOLES = {
    # blocs hérités M0/M1/M2/M3 (octets scellés — R7) : l'IAT et les données
    # M3 vivent dans le plan hérité L3 ; les révisions http les référenceront.
    "WRITE": 0x1040, "EXIT": 0x1080,
    "MEMCPY": 0x1100, "MEMCMP": 0x1180, "STRLEN": 0x1200, "ITOA": 0x1280,
    "ZONE_ALLOC": 0x1300, "ZONE_RESET": 0x1380, "MEMSET": 0x13C0,
    "TCP_INIT": 0x4000, "TCP_ACCEPT": 0x4100, "TCP_RECV": 0x4140,
    "TCP_SEND": 0x4180, "TCP_CLOSE": 0x41C0, "TCP_SPAWN": 0x4300,
    "TCP_JOURNAL": 0x4B00, "TCP_CONNEXION": 0x4400,
    "HTTP_LIGNE": 0x4C00, "HTTP_REQUETE": 0x4C80, "HTTP_ENTETE": 0x4E80,
    "HTTP_CHERCHER": 0x4F40, "HTTP_NOMBRE": 0x5080, "HTTP_TETE": 0x5140,
    "HTTP_AUTORITE": 0x5200, "HTTP_CIBLE": 0x5380, "HTTP_POMPE": 0x54C0,
    "SESSION": 0x5580, "CONSOLE": 0x5D80,
    # IAT kernel32 / ws2_32 (M3, R7 — les blocs tls-04..08 les référenceront)
    "IAT_GSH": L.IAT_SLOTS["GetStdHandle"], "IAT_WF": L.IAT_SLOTS["WriteFile"],
    "IAT_EP": L.IAT_SLOTS["ExitProcess"],
    "IAT_CREATETHREAD": L.IAT_SLOTS["CreateThread"],
    "IAT_VPROTECT": L.IAT_SLOTS["VirtualProtect"],
    "IAT_ICS": L.IAT_SLOTS["InitializeCriticalSection"],
    "IAT_ECS": L.IAT_SLOTS["EnterCriticalSection"],
    "IAT_LCS": L.IAT_SLOTS["LeaveCriticalSection"],
    "IAT_READFILE": L.IAT_SLOTS["ReadFile"], "IAT_CH": L.IAT_SLOTS["CloseHandle"],
    "IAT_WSASTARTUP": L.IAT_SLOTS["WSAStartup"], "IAT_SOCKET": L.IAT_SLOTS["socket"],
    "IAT_BIND": L.IAT_SLOTS["bind"], "IAT_LISTEN": L.IAT_SLOTS["listen"],
    "IAT_ACCEPT": L.IAT_SLOTS["accept"], "IAT_RECV": L.IAT_SLOTS["recv"],
    "IAT_SEND": L.IAT_SLOTS["send"], "IAT_CLOSESOCK": L.IAT_SLOTS["closesocket"],
    "IAT_WSAGLE": L.IAT_SLOTS["WSAGetLastError"],
    "IAT_WSACLEANUP": L.IAT_SLOTS["WSACleanup"],
    "IAT_GETADDRINFO": L.IAT_SLOTS["getaddrinfo"],
    "IAT_FREEADDRINFO": L.IAT_SLOTS["freeaddrinfo"],
    "IAT_CONNECT": L.IAT_SLOTS["connect"],
    # données .rdata M3 (révisions http)
    "TAB_METHODES": L.R_TAB_METHODES, "SLASH": L.R_SLASH,
    "TXT_400": L.R_TXT_400, "TXT_431": L.R_TXT_431, "TXT_501": L.R_TXT_501,
    "TXT_411": L.R_TXT_411, "TXT_505": L.R_TXT_505, "TXT_502": L.R_TXT_502,
    "TXT_TUNNEL": L.R_TXT_TUNNEL,
    "TAB_SUM": L.R_TAB_SUM, "TAB_TAILLE": L.R_TAB_SUM + 4,
    "TAB_SOMME": L.R_TAB_SUM + 8, "VERSION": L.R_VERSION, "ANCRE": L.R_ANCRE,
    "MSG_BANNIERE": L.R_MSG_BANNIERE, "MSG_CONNEXION": L.R_MSG_CONNEXION,
    "MSG_TUNNEL": L.R_MSG_TUNNEL, "MSG_FIN": L.R_MSG_FIN,
    "MSG_ARRET": L.R_MSG_ARRET, "MSG_INCONNU": L.R_MSG_INCONNU,
    "MSG_ERREUR": L.R_MSG_ERREUR, "MSG_KO": L.R_MSG_KO,
    "CMD_QUIT": L.R_CMD_QUIT, "NOM_HOST": L.R_NOM_HOST,
    "NOM_CL": L.R_NOM_CL, "NOM_TE": L.R_NOM_TE,
    # état .data (M3, R7)
    "STDOUT": L.R_STDOUT, "STDIN": L.R_STDIN, "LISTEN": L.R_LISTEN,
    "QUIT": L.R_QUIT, "CS": L.R_CS, "CURSEUR": L.R_CURSEUR,
    "ARENE": L.ARENA_BASE,
    # IAT secur32 + fixtures .rdata M4 : déclarés à l'ARRÊT D81 (tls-05) —
    # chaque nouveau symbole n'est déclaré qu'au moment de SA notation
    # (fail-closed historique : l'inconnu refusait ; le connu désormais
    # exigé par tls-05 est arrêté dans layout.py, source unique).
    # Blocs tls (feuilles D79 — cibles d'appel des futurs tls-04..08) :
    "TLS_UTF16": 0x6000, "TLS_VERDICTS": 0x6080, "TLS_JETONS": 0x6180,
    # Blocs tls mesurés (cibles d'appel de l'orchestrateur tls-08, D90) :
    "TLS_POIGNEE": 0x62C0, "TLS_CLES": 0x65C0, "TLS_EMISSION": 0x6740,
    "TLS_RECEPTION": 0x6A40,
    # Blocs de la révision http-10:R2 (D92 — le routage TLS) :
    "TLS_SESSION": 0x6D40,       # g70008 — la session TLS appelée par http-10:R2
    "HTTP_CIBLE_R2": 0x7340,     # g70009 — le parseur RÉVISÉ (verdict 4 = cible TLS)
    # Blocs de la révision http-12:R2 (D95 — le câblage) :
    "SESSION_R2": 0x74C0,        # g70010 — la session RÉVISÉE lancée par boucle
    # IAT secur32 (ARRÊT D81 — layout.IAT_SEC32_SLOTS, slots .rdata M4) :
    # D83 : le symbole secur32 s'appelle IAT_ISC (l'abréviation des specs
    # elles-mêmes — « boucle ISC ») — IAT_ICS désignait DÉJÀ Initialize-
    # CriticalSection (M2/M3, héritage) et le littéral de dictionnaire faisait
    # gagner cette seconde déclaration en éclipsant la première SILENCIEUSEMENT
    # (aucune notation n'a jamais résolu à travers : corrigé avant première
    # utilisation, fail-closed).
    "IAT_ACH": L.IAT_SEC32_SLOTS["AcquireCredentialsHandleW"],
    "IAT_FCH": L.IAT_SEC32_SLOTS["FreeCredentialsHandle"],
    "IAT_ISC": L.IAT_SEC32_SLOTS["InitializeSecurityContextW"],
    "IAT_DSC": L.IAT_SEC32_SLOTS["DeleteSecurityContext"],
    "IAT_QCA": L.IAT_SEC32_SLOTS["QueryContextAttributesW"],
    "IAT_EM": L.IAT_SEC32_SLOTS["EncryptMessage"],
    "IAT_DM": L.IAT_SEC32_SLOTS["DecryptMessage"],
    # Fixtures .rdata M4 (tls-05 : package Schannel, unique propriétaire) :
    "PKG": L.R_PKG_M4,
    # Fixtures .rdata M4 (tls-08 D90 : lignes console des états nommés) :
    "TXT_TLS_ETABLI": L.R_TXT_TLS_ETABLI,
    "TXT_TLS_CERT": L.R_TXT_TLS_CERT,
    # Fixtures .rdata M4 (http-10:R2 D92 : l'entrée étiquetée de la table) :
    "TXT_502_CERT": L.R_TXT_502_CERT,
}

RE_ETIQUETTE = re.compile(r"^\s*\.(\w+)\s*:\s*$")
RE_OPERANDE_ETIQUETTE = re.compile(r"^(j\w+|loop\w*|call)\s+\.(\w+)$")
RE_OPERANDE_SYMBOLE = re.compile(r"^(call)\s+(\w+)$")
RE_LEA_ETIQUETTE = re.compile(r"^(lea\s+\w+), \[\.(\w+)\]$")
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
    if m and m.group(3) in SYMBOLES:
        avant, signe, nom, apres = m.groups()
        if taille:
            return f"{avant}0x0{apres}"
    return ligne


def resoudre_rip(ligne: str, adresse: int, taille: int, etiquettes: dict) -> str:
    m = RE_LEA_ETIQUETTE.match(ligne)
    if m:
        cible = etiquettes.get(m.group(2))
        if cible is None:
            raise ErreurAuteur(f"étiquette inconnue : .{m.group(2)}")
        disp = cible - (adresse + 7)
        if disp >= 0:
            return f"{m.group(1)}, [rip + 0x{disp:x}]"
        return f"{m.group(1)}, [rip - 0x{-disp:x}]"
    m = RE_RIP_CIBLE.match(ligne)
    if not m:
        return ligne
    avant, signe, nom, apres = m.groups()
    if signe == "-":
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
        raise ErreurAuteur(f"{fichier} : pas de point fixe en 8 passes")

    lignes_sortie, adresse, calculs = [], rva, []
    for ligne, numero in instructions:
        taille = tailles[len(lignes_sortie)]
        explicite = resoudre_rip(
            substituer(ligne, adresse, etiquettes, rva), adresse, taille, etiquettes)
        lignes_sortie.append((explicite, adresse, taille, numero))
        adresse += taille
    total = adresse - rva
    if total > slot:
        raise ErreurAuteur(f"{fichier} : {total} o > slot {slot:#x} (D8) — "
                           "réarrêter le plan d'adressage sur la mesure")
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
    "tls-01-nom-utf16": "hôte span → UTF-16 (traduction unique)",
    "tls-02-verdicts": "table des verdicts SSPI (liste blanche)",
    "tls-03-jetons": "jetons SSPI (descripteurs)",
    "tls-04-poignee": "poignée de main cliente (boucle ISC)",
    "tls-05-cles": "cycle de vie des handles",
    "tls-06-emission": "émission chiffrée",
    "tls-07-reception": "réception déchiffrée",
    "tls-08-session": "session TLS cliente (orchestration)",
    "http-08-cible-r2": "cible (forme) — révision https",
    "http-10-session-r2": "session proxy — révision routage TLS",
    "http-12-principal-r2": "orchestration proxy — révision câblage + porte R10",
}


def main(verifier_seulement: bool) -> int:
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    print("=== outils/auteur.py : résolution des étiquettes (jalon M4) ===")
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
