#!/usr/bin/env python3
"""auteur.py — Outil d'auteur du domaine loupe (M10, le TGN « Loupe ») :
résolution des étiquettes.

Même discipline qu'en M1..M9 (aucun compilateur entre l'intention et les
octets : keystone assemble, rien d'autre) — cet outil fait l'arithmétique
d'adresses de l'auteur : étiquettes locales -> adresses absolues des sauts,
symboles de blocs -> cibles d'appels directes (les héritages tls13-01..04 et
libc-01/07 PAR LA CARTE à leurs slots loupe, les blocs loupe à leurs VA),
symboles de données -> déplacements RIP calculés une fois pour toutes depuis
le plan d'adressage loupe/layout.py (source unique — le cadre, les zones du
domaine, les tables MD5 publiques, l'IAT aux slots D7/D35).

Entrée : notation/brouillons/*.asm. Sortie : notation/*.asm — notation
explicite WYSIWYG, seule lue par le futur build (chantier (e)) et par le
harnais du chantier (b) (round-trip R5 sur la sortie).

Les slots sont ARRÊTÉS au plan d'adressage sur les longueurs réelles
(D161 : la mesure auteur décide, la préfiguration s'incline) — l'outil
REFUSE tout débordement (D8 : multiple de 64, padding >= 16). LE MODE
MESURE (--mesurer) rend les longueurs SANS écrire : la première passe du
chantier de notation, celle qui arrête le plan (le miroir du commentaire
« préfiguré 0xA00, mesuré 2815 o -> 0xB40 » du plan tls13).

Usage : python3 outils/auteur.py [--mesurer | --verifier-seulement]
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import layout as L  # noqa: E402  # le plan loupe (la source unique)

from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402

ICI = os.path.dirname(os.path.abspath(__file__))
BROUILLONS = os.path.join(ICI, "..", "notation", "brouillons")
SORTIE = os.path.join(ICI, "..", "notation")

# (fichier brouillon, id bloc, spec, dépendances) — rva/slot dérivés du plan
# d'adressage (layout.py, source unique de vérité ; l'ARRÊT DÉFINITIF des
# slots est celui du plan — la mesure auteur, D161 rejoué).
_FICHIERS = {
    "i110004": ("loupe-04-cadre", "loupe-04:R1",
                "libc-07 (le memset hérité PAR LA CARTE — byte-identique au "
                "scellé M1, jamais une boucle réécrite) ; le cadre posé "
                "vierge, la poignée INVALIDE ; AUCUNE entrée IAT (le miroir "
                "des feuilles pures, charte § 9)"),
    "i110001": ("loupe-01-ouvrir", "loupe-01:R1",
                "IAT kernel32 : CreateFileW, GetFileSizeEx, CloseHandle, "
                "GetLastError ; libc-01 (la copie du chemin PAR LA CARTE) ; "
                "loupe-04 (le cadre vierge en tête), loupe-02 (la fenêtre à "
                "la vue 0), loupe-03 (la clôture sur refus), loupe-07 (le "
                "panneau né) — la session née ENTIÈRE (Q4)"),
    "i110002": ("loupe-02-lire", "loupe-02:R1",
                "IAT kernel32 : SetFilePointerEx, ReadFile, GetLastError ; "
                "le recouvrement du journal (Q2 : l'édition survit au "
                "défilement) ; la lecture ne touche QUE le tampon du cadre "
                "(I2 — jamais TAMPON_CUMUL, jamais l'ECRAN)"),
    "i110003": ("loupe-03-fermer", "loupe-03:R1",
                "IAT kernel32 : CloseHandle, GetLastError ; loupe-04 (le "
                "cadre re-vierge), libc-07 (l'hygiène des empreintes) ; "
                "idempotent par construction, jamais une poignée pendante"),
    "i110005": ("loupe-05-sha256", "loupe-05:R1",
                "tls13-01 (l'init, UNE fois), tls13-03 (l'absorption à "
                "chaque fenêtre), tls13-04 (la finalisation) — LA FAMILLE "
                "SHA PAR LA CARTE (R7 : les octets du scellé 1.0.0, jamais "
                "une copie ré-écrite) ; IAT kernel32 : SetFilePointerEx, "
                "ReadFile, GetLastError ; le contexte 112 o SUR LA PILE"),
    "i110006": ("loupe-06-md5", "loupe-06:R1",
                "LA NOUVELLE NOTATION (aucun héritage : MD5 n'existe pas au "
                "projet) ; les tables MD5_S/MD5_T PUBLIQUES .rdata lues PAR "
                "DÉPLACEMENT RIP (I2 — la source unique vit au plan) ; "
                "libc-01 (le couplage du tampon PAR LA CARTE) et libc-07 (les "
                "zéros du bourre PAR LA CARTE) ; IAT "
                "kernel32 : SetFilePointerEx, ReadFile, GetLastError ; le "
                "cœur .comprimer : FEUILLE PURE en sous-routine locale, les "
                "QUATRE rounds nommés (RFC 1321 § 3.4)"),
    "i110007": ("loupe-07-cumul", "loupe-07:R1",
                "loupe-05 (le passage SHA-256) puis loupe-06 (le passage "
                "MD5) — LA COMPOSITION SEULE, DEUX passages l'un après "
                "l'autre (I2 : l'exclusion de famille) ; AUCUNE entrée IAT "
                "(le miroir des feuilles pures, charte § 9)"),
}


def blocs_loupe() -> list[tuple]:
    out = []
    for bid, (fichier, spec, deps) in _FICHIERS.items():
        rva, slot = L.SLOTS_LOUPE[bid]
        out.append((fichier, bid, spec, rva, slot, deps))
    return out


BLOCS = blocs_loupe()

SYMBOLES = {
    # les blocs du domaine (le plan, source unique — les appels directs)
    "LOUPE01": L.LOUPE01_VA,
    "LOUPE02": L.LOUPE02_VA,
    "LOUPE03": L.LOUPE03_VA,
    "LOUPE04": L.LOUPE04_VA,
    "LOUPE05": L.LOUPE05_VA,
    "LOUPE06": L.LOUPE06_VA,
    "LOUPE07": L.LOUPE07_VA,
    # les héritages PAR LA CARTE (R7 — embarqués au build byte-identiques,
    # aux slots loupe du plan ; les octets viennent des SCELLÉS, jamais de
    # la ré-écriture)
    "TLS01": L.R_TLS01,          # tls13-01 sha256-init (le scellé 1.0.0)
    "TLS03": L.R_TLS03,          # tls13-03 sha256-absorber (idem)
    "TLS04": L.R_TLS04,          # tls13-04 sha256-finaliser (idem)
    "LIBC01": L.R_LIBC01,        # libc-01 memcpy (le scellé M1)
    "LIBC07": L.R_LIBC07,        # libc-07 memset (idem)
    # les tables MD5 publiques (I2 de loupe-06 — le plan, source unique)
    "MD5_S": L.R_MD5_S,
    # les zones .data du domaine (le plan, source unique — D161)
    "CADRE": L.R_CADRE,
    "EMPREINTES": L.R_EMPREINTES,
    "SAISIE": L.R_SAISIE,
    "MOTIF": L.R_MOTIF,
    "JOURNAL": L.R_JOURNAL,
    "ECRAN": L.R_ECRAN,
    "HWND": L.R_HWND,
    "METRIQUES": L.R_METRIQUES,
    "CUMUL": L.R_CUMUL,
}
# l'IAT (le plan, source unique — chaque feuille son slot, l'ordre figé)
for _feuille, _slot in L.IAT_SLOTS.items():
    SYMBOLES["IAT_" + _feuille.upper()] = _slot
del _feuille, _slot

RE_ETIQUETTE = re.compile(r"^\s*\.(\w+)\s*:\s*$")
RE_OPERANDE_ETIQUETTE = re.compile(r"^(j\w+|loop\w*|call)\s+\.(\w+)$")
RE_OPERANDE_SYMBOLE = re.compile(r"^(call)\s+(\w+)$")
RE_LEA_ETIQUETTE = re.compile(r"^(lea\s+\w+), \[\.(\w+)\]$")
RE_RIP_CIBLE = re.compile(r"^(.*?\[rip\s*([+-])\s*)(\w+|\.\w+)(\s*\].*)$")

# les registres 64 bits : « call r10 » serait l'appel indirect DÉCLARÉ —
# PAS un symbole de bloc (le miroir tls13-28 I2)
REGISTRES64 = {"rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"} \
    | {f"r{i}" for i in range(8, 16)}


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
    try:
        enc, _ = ks.asm(substituer(ligne, adresse, etiquettes, taille=True), adresse)
    except Exception as err:
        raise ErreurAuteur(f"ligne inassemblable : {ligne!r} ({err})") from err
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
        if nom in REGISTRES64:
            return ligne          # l'appel indirect DÉCLARÉ
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


def mesurer_bloc(ks: Ks, fichier: str, rva: int) -> tuple[int, int, int, list[int]]:
    """LA MESURE (D161) : la longueur réelle du brouillon à son rva — sans
    écrire, sans juger le slot. Retourne (total, instructions, étiquettes,
    tailles)."""
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
    return (sum(tailles), len(instructions), len(etiquettes_lignes), tailles)


def slot_minimum(total: int) -> int:
    """Le MINIMUM ADMISSIBLE D8 : multiple de 64, padding >= 16."""
    slot = max(64, ((total + 16 + 63) // 64) * 64)
    while slot - total < 16:
        slot += 64
    return slot


def resoudre_bloc(ks: Ks, fichier: str, bid: str, spec: str,
                  rva: int, slot: int, deps: str):
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
        f"; Domaine : loupe (M10, le TGN « Loupe ») · Dépendances : {deps}",
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
        entete.append("; Appels directs (l'adresse du plan — I1) : " +
                      ", ".join(appels))

    chemin_sortie = os.path.join(SORTIE, fichier + ".asm")
    with open(chemin_sortie, "w", encoding="utf-8") as f:
        f.write("\n".join(entete) + "\n")
        for ligne_e, *_ in lignes_sortie:
            f.write(ligne_e + "\n")
    return total, len(instructions), len(etiquettes_lignes)


NOMS_COURTS = {
    "loupe-01-ouvrir": "ouvrir : le fichier donné à la session (la session née entière)",
    "loupe-02-lire": "lire : la fenêtre bornée au tampon + le recouvrement du journal",
    "loupe-03-fermer": "fermer : jamais une poignée pendante (idempotent)",
    "loupe-04-cadre": "le cadre de session posé vierge (la structure unique)",
    "loupe-05-sha256": "sha256 d'une gamme : l'héritage tls13 PAR LA CARTE",
    "loupe-06-md5": "md5 d'une gamme : l'empreinte du quotidien, notée neuve (RFC 1321)",
    "loupe-07-cumul": "le cumul : les empreintes du fichier entier au panneau",
}


def main(*args: str) -> int:
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    if "--mesurer" in args:
        print("=== outils/auteur.py : LA MESURE (domaine loupe, chantier "
              "M10-(b), D161 — la mesure décide, la préfiguration s'incline) ===")
        for fichier, bid, spec, rva, slot, deps in BLOCS:
            total, n, e, _ = mesurer_bloc(ks, fichier, rva)
            mini = slot_minimum(total)
            jugement = "TENU" if mini == slot else \
                (f"RÉ-ARRÊTER {slot:#x} -> {mini:#x}" if mini != slot else "")
            print(f"[mesure] {fichier} ({bid}) : {total} o notés, {n} "
                  f"instructions, {e} étiquettes — slot préfiguré {slot:#x}, "
                  f"minimum {mini:#x} (padding {mini - total}) — {jugement}")
        return 0
    print("=== outils/auteur.py : résolution des étiquettes "
          "(domaine loupe, chantier M10-(b)) ===")
    for fichier, bid, spec, rva, slot, deps in BLOCS:
        chemin = os.path.join(BROUILLONS, fichier + ".asm")
        if not os.path.exists(chemin):
            print(f"[absent] {fichier} : brouillon absent, ignoré (attendu selon la phase)")
            continue
        total, n, e = resoudre_bloc(ks, fichier, bid, spec, rva, slot, deps)
        print(f"[ok] {fichier} ({bid}) : {total} o, {n} instructions, "
              f"{e} étiquettes, {slot - total} o de padding")
    if "--verifier-seulement" not in args:
        print("Notation explicite écrite dans notation/*.asm")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
