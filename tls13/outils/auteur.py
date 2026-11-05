#!/usr/bin/env python3
"""auteur.py — Outil d'auteur du domaine tls13 (M9, l'ère 1.0.0) : résolution
des étiquettes.

Même discipline qu'en M1..M8 (aucun compilateur entre l'intention et les
octets : keystone assemble, rien d'autre) — cet outil fait l'arithmétique
d'adresses de l'auteur : étiquettes locales -> adresses absolues des sauts,
symboles de blocs -> cibles d'appels directes (I1 des specs : l'adresse
scellée du plan), symboles de données -> déplacements RIP calculés une fois
pour toutes depuis le plan d'adressage tls13/layout.py (source unique — le
fixture K[64] vit dans la réserve .rdata héritée M8, RVA 0x2F00).

Entrée : notation/brouillons/*.asm. Sortie : notation/*.asm — notation
explicite WYSIWYG, seule lue par le futur build (chantier (e)) et par le
harnais du chantier (b) (round-trip R5 sur la sortie).

Les slots sont ARRÊTÉS au plan d'adressage sur les longueurs réelles
(D161 : la mesure auteur décide, la préfiguration s'incline) — l'outil
REFUSE tout débordement (D8 : multiple de 64, padding >= 16).

Usage : python3 outils/auteur.py [--verifier-seulement]
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import layout as L  # noqa: E402  # le plan tls13 (la source unique)

from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402

ICI = os.path.dirname(os.path.abspath(__file__))
BROUILLONS = os.path.join(ICI, "..", "notation", "brouillons")
SORTIE = os.path.join(ICI, "..", "notation")

# (fichier brouillon, id bloc, spec, dépendances) — rva/slot dérivés du plan
# d'adressage (layout.py, source unique de vérité ; l'ARRÊT DÉFINITIF des
# slots est celui du plan — la mesure auteur, D161 rejoué).
_FICHIERS = {
    "h100001": ("tls13-01-sha256-init", "tls13-01:R1",
                "bloc feuille ; aucun état, aucun appel — les H0 posés au "
                "contexte en argument (charte § 6)"),
    "h100002": ("tls13-02-sha256-comprimer", "tls13-02:R1",
                "bloc feuille ; le fixture K[64] @R_K cité par déplacement "
                "RIP (I3 de la spec) — AUCUN autre accès mémoire hors du "
                "contexte et de la pile"),
    "h100003": ("tls13-03-sha256-absorber", "tls13-03:R1",
                "tls13-02 (la compression au geste même, à l'adresse "
                "scellée — I1) ; le tampon passé en second argument"),
    "h100004": ("tls13-04-sha256-finaliser", "tls13-04:R1",
                "tls13-02 (les compressions finales, DEUX appels à "
                "l'adresse scellée — I1) ; le tampon passé en second argument"),
    "h100005": ("tls13-05-hmac-sha256", "tls13-05:R1",
                "tls13-01 (init ×2, DEUX contextes), tls13-03 (absorption), "
                "tls13-04 (finalisation) — appels directs aux adresses "
                "scellées (I1) ; K', le masque et les DEUX contextes sur la "
                "PILE (I2) — AUCUN déplacement RIP"),
    "h100006": ("tls13-06-hkdf-extract", "tls13-06:R1",
                "tls13-05 (l'HMAC appelé UNE fois — le sel devient la clé) ; "
                "les 32 zéros du sel vide sur la PILE (I1)"),
    "h100007": ("tls13-07-hkdf-expand", "tls13-07:R1",
                "tls13-05 (l'HMAC appelé à CHAQUE itération — I1) ; le tampon "
                "T(i−1) || info || i en allocation dynamique 16-alignée sur "
                "la PILE ; T(i−1) LU DEPUIS OKM (I2)"),
    "h100008": ("tls13-08-hkdf-expand-label", "tls13-08:R1",
                "tls13-07 (l'expansion appelée UNE fois — I1) ; la structure "
                "HkdfLabel sérialisée GROS-BOUTISTE dans le tampon de PILE "
                "; le préfixe « tls13 » en immédiats du plan (I2)"),
    "h100009": ("tls13-09-f25519-add", "tls13-09:R1",
                "bloc feuille de la famille x25519 ; tls13-12 (UNE passe — "
                "I1) ; les CINQ additions membres à membres IN PLACE, la "
                "sortie ÉCRASE a (Q2, miroir av-07) ; les bornes < 2^53 en "
                "registres volatils — AUCUN déplacement RIP"),
    "h100010": ("tls13-10-f25519-sub", "tls13-10:R1",
                "tls13-12 (UNE passe — I2) ; les membres de 2p en IMMÉDIATS "
                "re-dérivés du plan (I1, l'erratum consigné) ; la chaîne "
                "sub/sbb SUR LE SCRATCH, l'emprunt sortant VERROU fail-closed "
                "(Q3 : rax = -1 NOMMÉ, RIEN écrit) ; AUCUN déplacement RIP"),
    "h100011": ("tls13-11-f25519-mul", "tls13-11:R1",
                "tls13-12 (UNE passe — I3) ; l'école 5×5 déroulée, les DIX "
                "accumulateurs u128 en PILE [sous-cadre 0xC0 — I1], le repli "
                "×19 et la chaîne 51 bits (I2) ; rbx retenu (le pointeur b "
                "survit aux mul) ; AUCUN déplacement RIP"),
    "h100012": ("tls13-12-f25519-propager-geler", "tls13-12:R1",
                "bloc FEUILLE fusionné (miroirs av-06 + av-10, UNE frontière) ; "
                "la passe séquentielle 0→4 puis LE GEL SANS BRANCHE DE DONNÉES "
                "(I2 : le drapeau en registre, sar, le masque 0/-1, l'ET "
                "logique — l'amélioration nommée) ; le masque, 19 et les "
                "membres de p en IMMÉDIATS (I1/I3)"),
    "h100013": ("tls13-13-x25519-echelle", "tls13-13:R1",
                "tls13-09/10/11 (4 add + 4 sub + 10 mul PAR ITÉRATION — I5, "
                "l'erratum de compte consigné ; entre 255 et 510 pour "
                "l'inversion) ; le cswap XOR MASQUÉ (I1), les états sur la "
                "PILE (I3, le sous-cadre réel consigné), l'exposant p−2 au "
                "fixture R_EXP_INV (I4) ; le clamp et le masque bit 255 dans "
                "des COPIES LOCALES (P2/P3)"),
    "h100014": ("tls13-14-x25519-cle-publique", "tls13-14:R1",
                "tls13-13 (l'échelle au point de base — I1) ; le point 9 au "
                "fixture R_U9 (la fixture PUBLIQUE du domaine, jamais un "
                "octet de code)"),
}


def blocs_tls13() -> list[tuple]:
    out = []
    for bid, (fichier, spec, deps) in _FICHIERS.items():
        rva, slot = L.SLOTS_TLS13[bid]
        out.append((fichier, bid, spec, rva, slot, deps))
    return out


BLOCS = blocs_tls13()

SYMBOLES = {
    # les blocs du domaine (le plan, source unique — les appels directs I1)
    "TLS01": L.TLS01_VA,
    "TLS02": L.TLS02_VA,
    "TLS03": L.TLS03_VA,
    "TLS04": L.TLS04_VA,
    "TLS05": L.TLS05_VA,
    "TLS07": L.TLS07_VA,
    "TLS09": L.TLS09_VA,
    "TLS10": L.TLS10_VA,
    "TLS11": L.TLS11_VA,
    "TLS12": L.TLS12_VA,
    "TLS13": L.TLS13_VA,
    # le fixture .rdata du domaine (le plan, source unique) : K[64] dans la
    # réserve M8 exactement (RVA 0x2F00 — 256 o, vérifié vierge sur pièces)
    "K": L.R_K,
    # les fixtures .text6 du domaine (l'ARRÊT du geste x25519, miroir D95) :
    # le point de base u = 9 (tls13-14 I1) et l'exposant p−2 (tls13-13 I4)
    "U9": L.R_U9,
    "EXP_INV": L.R_EXP_INV,
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


def taille_ligne(ks: Ks, ligne: str, adresse: int, etiquettes: dict) -> int:
    enc, _ = ks.asm(substituer(ligne, adresse, etiquettes, taille=True), adresse)
    if not enc:
        raise ErreurAuteur(f"ligne inassemblable (calcul de taille) : {ligne!r}")
    return len(enc)


def substituer(ligne: str, adresse: int, etiquettes: dict, taille: int = 0) -> str:
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

    etiquettes = {nom: rva + 0x80 for nom, _ in etiquettes_lignes}
    for _ in range(8):
        tailles, adresse = [], rva
        for ligne, _ in instructions:
            t = taille_ligne(ks, ligne, adresse, etiquettes)
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
            substituer(ligne, adresse, etiquettes), adresse, taille, etiquettes)
        lignes_sortie.append((explicite, adresse, taille, numero))
        adresse += taille
    total = adresse - rva
    if total > slot:
        raise ErreurAuteur(f"{fichier} : {total} o > slot {slot:#x} (D8) — "
                           "réarrêter le plan d'adressage sur la mesure")
    if slot - total < 16:
        raise ErreurAuteur(f"{fichier} : padding {slot - total} < 16 (D8)")

    entete = [
        f"; {fichier} · bloc {NOMS_COURTS[fichier]} · spec {spec} · bloc carte {bid}",
        f"; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x{rva:x}, taille {slot} octets",
        f"; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : {deps}",
        f"; Notation explicite générée par outils/auteur.py depuis brouillons/{fichier}.asm",
        f"; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)",
        f"; Code : {total} o · padding : {slot - total} o (NOP, 0x90)",
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
    appels = [l for l, *_ in lignes_sortie if l.startswith("call ")]
    if appels:
        entete.append("; Appels directs (l'adresse scellée du plan — I1) : " +
                      ", ".join(appels))

    chemin_sortie = os.path.join(SORTIE, fichier + ".asm")
    with open(chemin_sortie, "w", encoding="utf-8") as f:
        f.write("\n".join(entete) + "\n")
        for ligne_e, *_ in lignes_sortie:
            f.write(ligne_e + "\n")
    return total, len(instructions), len(etiquettes_lignes)


NOMS_COURTS = {
    "tls13-01-sha256-init": "initialisation du contexte SHA-256 (FIPS § 5.3.1)",
    "tls13-02-sha256-comprimer": "compression d'un bloc de 64 o (FIPS § 6.2.2)",
    "tls13-03-sha256-absorber": "absorption tamponnée (invariance de découpage)",
    "tls13-04-sha256-finaliser": "finalisation bourrage-longueur-extraction",
    "tls13-05-hmac-sha256": "HMAC-SHA-256 (RFC 2104 : ipad/opad, la clé expulsée)",
    "tls13-06-hkdf-extract": "HKDF-Extract (RFC 5869 § 2.1 : le sel → le PRK)",
    "tls13-07-hkdf-expand": "HKDF-Expand (RFC 5869 § 2.3 : PRK + info → OKM)",
    "tls13-08-hkdf-expand-label": "HKDF-Expand-Label (RFC 8446 § 7.1 : le calendrier)",
    "tls13-09-f25519-add": "f25519 addition réduite (cinq membres, miroir av-07)",
    "tls13-10-f25519-sub": "f25519 soustraction réduite (a + 2p − b, miroir av-08)",
    "tls13-11-f25519-mul": "f25519 multiplication (école 5×5, repli ×19, miroir av-09)",
    "tls13-12-f25519-propager-geler": "f25519 propagation + gel sans branche (av-06+av-10 fusionnés)",
    "tls13-13-x25519-echelle": "X25519 échelle de Montgomery (RFC 7748 § 5, miroir av-11)",
    "tls13-14-x25519-cle-publique": "X25519 clé publique (le couple du ClientHello)",
}


def main(verifier_seulement: bool) -> int:
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    print("=== outils/auteur.py : résolution des étiquettes "
          "(domaine tls13, chantier M9-(b)) ===")
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
