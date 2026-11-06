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
    "h100015": ("tls13-15-aes128-cles-tour", "tls13-15:R1",
                "bloc feuille de la famille aead ; l'ARRÊT AES-NI — "
                "AESKEYGENASSIST le SubWord/RotWord MATÉRIEL, la disposition "
                "DÉRIVÉE DE L'OBSERVATION (le mot d'AES-128 au dword 3 → pshufd "
                "0xFF — la sonde du labo, derive_aead.py), les DIX Rcon en "
                "IMMÉDIATS, la recette préfixe-XOR ⊕ t CONTRE-PROUVÉE sur C.1 ; "
                "les dix tours DÉROULÉS — AUCUN saut, AUCUN déplacement RIP"),
    "h100016": ("tls13-16-aes128-bloc", "tls13-16:R1",
                "bloc feuille ; pxor + NEUF AESENC + AESENCLAST — LA "
                "COMPOSITION BLANCHE rend FIPS 197 C.1 sur l'émulateur (la "
                "contre-preuve du labo AVANT la notation) ; les clés chargées "
                "par movdqu NON ALIGNÉES (aucune précondition cachée), la "
                "BRIQUE D'INVERSION n'existe pas — AES en sens unique"),
    "h100017": ("tls13-17-ghash-multiplication", "tls13-17:R1",
                "bloc feuille ; la marche de l'algorithme 1 SP 800-38D § 6.3 "
                "MOT POUR MOT — SANS TABLE PAR DONNÉE (I1 : le masque 0/−1 par "
                "sbb, le repli SANS BRANCHE — I2) ; LE DOMAINE GROS-BOUTISTE "
                "PAR BSWAP (la seconde faute nommée par la sonde du geste : "
                "les DEUX voies bswapées, le premier bit de la chaîne = le bit "
                "63 de la voie haute, le sortant = le bit 0 de la voie basse, "
                "l'ordre shld/sbb/shl capture le drapeau AVANT l'écrasement) ; "
                "R = GCM_R du plan en IMMÉDIAT : l'octet 0 au SOMMET de la "
                "voie haute — 0xE1 << 56 ; le SEUL saut est la boucle sur le "
                "COMPTEUR"),
    "h100018": ("tls13-18-gcm-sceller", "tls13-18:R1",
                "tls13-16 (H = E(K,0) D'ABORD, les compteurs du CTR, E(K, J0)) "
                "+ tls13-17 (CHAQUE bloc du GHASH — I2) ; J0 FIGÉ, CB la "
                "COPIE qui mute (inc32 u32 GROS-BOUTISTE par bswap — I3) ; le "
                "cadre 0xE8 : l'ombre + J0/CB/H/Y/X/ks + les pointeurs (I5 — "
                "tout sur la PILE) ; les refus -1/-2 NOMMÉS (Q3)"),
    "h100019": ("tls13-19-gcm-ouvrir", "tls13-19:R1",
                "tls13-16 + tls13-17 (la même recette que 18 sur le chiffré "
                "REÇU) ; LA DISCIPLINE DU VERDICT — la confrontation TEMPS "
                "CONSTANT (I1 : le OU cumulatif des 16 différences en UN seul "
                "drapeau, AUCUN court-circuit, le branch sur LE drapeau), "
                "PUIS le CTR : LA RESTITUTION EST LA DERNIÈRE OPÉRATION (I2) ; "
                "l'étiquette divergente → rax = -4 NOMMÉ, la sortie INTACTE"),
    "h100020": ("tls13-20-enregistrement-proteger", "tls13-20:R1",
                "bloc ; tls13-18 (UNE composition — le scellement) ; le "
                "texte interne charge || type au DERNIER octet (bourre "
                "LONGUEUR ZÉRO), le nonce = IV ⊕ séquence GROS-BOUTISTE "
                "(I2 : le IV COPIÉ en local, le contexte jamais réécrit), "
                "l'AAD = l'en-tête LOCALE (23, 0x0303, N+17 u16 "
                "gros-boutiste — copiée à la sortie APRÈS le succès : le "
                "-3 propagé n'écrit RIEN) ; l'incrémentation SUIT le "
                "scellement (un échec n'avance JAMAIS) ; le cadre 0x4078 : "
                "le texte interne jusqu'à 2^14+1 sur la pile ; le verdict "
                "-3 = le verdict PROPAGÉ de 18 (N = 2^14 : le texte interne "
                "2^14+1 hors la brique — la fragmentation à l'appelant)"),
    "h100021": ("tls13-21-enregistrement-deproteger", "tls13-21:R1",
                "bloc ; tls13-19 (UNE composition — le déverrouillage) ; "
                "l'en-tête CONFRONTÉE AVANT TOUT (le type 23 → -1, la "
                "longueur déclarée == reçue et les bornes → -2, la version "
                "héritage IGNORÉE mais couverte par l'AAD : la mutation → "
                "-4, la cryptographie attrape ce que la logique ignore), "
                "l'AAD = l'en-tête REÇUE telle quelle, le nonce = IV ⊕ "
                "séquence, la restitution DERNIÈRE (le -4 : la sortie et "
                "le type INTACTS, la séquence ne bouge pas) ; le type = le "
                "DERNIER octet du texte interne déverrouillé dans le "
                "tampon LOCAL (la sortie P4 n'a que L−17 o) ; l'anti-rejoue "
                "par la séquence (une étiquette qui ne colle pas)"),
    "h100022": ("tls13-22-clienthello-composer", "tls13-22:R1",
                "bloc feuille de la famille poignée ; LA COMPOSITION PAR "
                "OCTETS FIXES — chaque champ à son offset constant (I1), les "
                "valeurs protocolaires du plan d'adressage en IMMÉDIATS "
                "(T5), l'aléa copié @ +6, la clé publique copiée @ +82 ; "
                "AUCUNE branche, AUCUNE construction variable — le message "
                "est FIXE (charte § 1) ; le message ne TOUCHE PAS au "
                "transcript (I2 — le principal chronique)"),
    "h100023": ("tls13-23-serverhello-traiter", "tls13-23:R1",
                "bloc ; tls13-13 (UNE composition — le secret partagé, "
                "APRÈS le dernier refus possible : la clé privée n'est "
                "JAMAIS touchée sur un message refusé — Q3) ; LA MARCHE "
                "BORNÉE (I1 : chaque lecture précédée du contrôle de "
                "reste), chaque confrontation NOMMÉE dans l'ordre du corps "
                "(le type 2, la version 0x0303, l'aléa ≠ la valeur magique "
                "HRR au fixture R_HRR par OU cumulatif — I2, l'écho "
                "session_id vide, LA SUITE 0x1301 → -5 la négociation "
                "refusée, la compression nulle, supported_versions 0x0304 "
                "PRÉSENTE, key_share x25519 32 o PRÉSENTE, les extensions "
                "inconnues IGNORÉES — la règle du protocole, l'épuisement "
                "exact) ; le message ne TOUCHE PAS au transcript (I3)"),
    "h100024": ("tls13-24-calendrier-cles", "tls13-24:R1",
                "bloc ; tls13-06 (l'extrait — UN par étage), tls13-08 "
                "(l'étiquette — TOUTES les clés : les libellés aux fixtures "
                "R_LIB_* du plan, données PUBLIQUES), tls13-15 (le "
                "déploiement des clés de tour), tls13-01 + tls13-04 (le "
                "condensé du VIDE — le contexte de « derived » : l'erratum "
                "n° 2 sur pièces, Hash du VIDE de 32 o, JAMAIS zéro octet) ; "
                "la machine à TROIS étages STRICTS (-3 sur tout saut), le "
                "contexte porte (secret courant, étape), les contextes "
                "sortis COMPLETS (rk 176 + IV 12 + réserve 4 + séquence "
                "u64) ; le hash du transcript est un ARGUMENT (I1 — le "
                "principal tient le contexte SHA) ; le calendrier ne "
                "hache RIEN"),
    "h100025": ("tls13-25-finished-calculer-verifier", "tls13-25:R1",
                "bloc ; tls13-05 (UNE composition — l'HMAC, le Finished "
                "n'est RIEN d'autre — I1) ; DEUX modes NOMMÉS sur r9 (0 "
                "calculer, 1 vérifier, toute autre valeur → -1) ; le mode "
                "VÉRIFIER : le reçu CONFRONTÉ par OU cumulatif des 32 "
                "différences (I2 : AUCUN court-circuit — la discipline du "
                "verdict AEAD), conforme → 0, divergent → -4 NOMMÉ ; le "
                "mode est une donnée PUBLIQUE de contrôle (le branch licite)"),
    "h100026": ("tls13-26-epinglage", "tls13-26:R1",
                "bloc ; tls13-01, tls13-03, tls13-04 (le hachage — un "
                "contexte de PILE local, I2) ; la décision de confiance : "
                "SHA-256(DER) CONFRONTÉ à l'empreinte par OU cumulatif des "
                "32 différences (I1 : TEMPS CONSTANT — la discipline "
                "demeure sur une donnée de confiance), conforme → 0, "
                "divergent → -6 NOMMÉ (épinglage divergent — la session "
                "MEURT sans autres formes)"),
    "h100027": ("tls13-27-principal-machine-etats", "tls13-27:R1",
                "LE PRINCIPAL — l'orchestration sur le contexte session "
                "17 520 o (la disposition DÉCLARÉE par la spec P1) ; LES "
                "COMPOSITIONS DÉCLARÉES (I1, LA LISTE FERMÉE) : tls13-14, "
                "tls13-22, tls13-23, tls13-24 (×3 étages), tls13-25 (×2 "
                "modes), tls13-26, tls13-20 (×2), tls13-21 (×2), tls13-03 "
                "(le transcript — chaque message ABSORBÉ AVANT traitement, "
                "charte § 4), tls13-04 (les coupes du hash sur la COPIE — "
                "I2), LE SOCLE tls13-28 pour TOUTE entrée/sortie ; QUATRE "
                "événements NOMMÉS (OUVRIR/ÉMETTRE/RECEVOIR/FERMER), tout "
                "événement hors de sa ligne → -3 ; LA DISCIPLINE D'ÉCHEC "
                "(Q2) : tout verdict négatif PROPAGÉ NOMMÉ, l'état passe à "
                "5 (MORT), AUCUN octet applicatif après ; le réassemblage "
                "au tampon @ +1136 (la borne 2^14 NOMMÉE), le Certificate "
                "Verify ABSORBÉ sans vérification (le chantier futur nommé), "
                "l'extraction de la PREMIÈRE entrée du Certificate (le u24 "
                "lu) le DÉTROIT de tls13-26"),
    "h100028": ("tls13-28-socle-appel", "tls13-28:R1",
                "LA ROTULE — le seul point du domaine où le calcul touche "
                "le monde : UN contexte de DEUX rappels fournis par "
                "l'appelant (émettre @ +0/+8, recevoir @ +16/+24), "
                "invoqués PAR POINTEUR DEPUIS LE CONTEXTE (I2 : l'appel "
                "indirect DÉCLARÉ sur une cible qui est une DONNÉE du "
                "contexte n'est NI un import NI un syscall) ; l'opération "
                "rdx ∈ {1 émettre, 2 recevoir}, toute autre → -1 ; le "
                "verdict du rappel négatif → -7 NOMMÉ (transport en "
                "échec) ; aucune copie, aucun tampon (Q4 — l'adaptateur), "
                "le zéro de réception est le refus -7 du KIT"),
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
    "TLS06": L.TLS06_VA,     # l'extrait — appelé par 24 (le calendrier)
    "TLS07": L.TLS07_VA,
    "TLS08": L.TLS08_VA,     # l'étiquette — appelée par 24 (LE bloc du calendrier)
    "TLS09": L.TLS09_VA,
    "TLS10": L.TLS10_VA,
    "TLS11": L.TLS11_VA,
    "TLS12": L.TLS12_VA,
    "TLS13": L.TLS13_VA,
    "TLS14": L.TLS14_VA,     # la clé publique — appelée par 27 (le couple du CH)
    "TLS15": L.TLS15_VA,     # le déploiement des clés de tour — appelé par 24
    "TLS16": L.TLS16_VA,     # le chiffrement d'un bloc — appelé par 18/19
    "TLS17": L.TLS17_VA,     # la multiplication GF(2^128) — appelée par 18/19
    "TLS18": L.TLS18_VA,     # GCM sceller — appelé par 20 (l'enregistrement)
    "TLS19": L.TLS19_VA,     # GCM ouvrir — appelé par 21 (l'enregistrement)
    "TLS20": L.TLS20_VA,     # l'enregistrement protéger — appelé par 27 (×2)
    "TLS21": L.TLS21_VA,     # l'enregistrement déprotéger — appelé par 27 (×2)
    "TLS22": L.TLS22_VA,     # le ClientHello composé — appelé par 27
    "TLS23": L.TLS23_VA,     # le ServerHello traité — appelé par 27
    "TLS24": L.TLS24_VA,     # le calendrier — appelé par 27 (trois étages)
    "TLS25": L.TLS25_VA,     # le Finished — appelé par 27 (deux modes)
    "TLS26": L.TLS26_VA,     # l'épinglage — appelé par 27
    "TLS27": L.TLS27_VA,     # la machine d'états — LE principal
    "TLS28": L.TLS28_VA,     # le socle d'appel — appelé par 27 (le transport)
    # le fixture .rdata du domaine (le plan, source unique) : K[64] dans la
    # réserve M8 exactement (RVA 0x2F00 — 256 o, vérifié vierge sur pièces)
    "K": L.R_K,
    # les fixtures .text6 du domaine (l'ARRÊT du geste x25519, miroir D95) :
    # le point de base u = 9 (tls13-14 I1) et l'exposant p−2 (tls13-13 I4)
    "U9": L.R_U9,
    "EXP_INV": L.R_EXP_INV,
    # les fixtures .text6 POIGNÉE (l'ARRÊT du geste poignée, miroir D95) :
    # les libellés du calendrier (tls13-24 — RFC 8446 § 7.1, données
    # PUBLIQUES du plan d'adressage, jamais des octets de code) et la
    # valeur magique HelloRetryRequest (tls13-23 Q1 — RFC 8446 § 4.1.3)
    "LIB_DERIVED": L.R_LIB_DERIVED,
    "LIB_C_HS": L.R_LIB_C_HS,
    "LIB_S_HS": L.R_LIB_S_HS,
    "LIB_C_AP": L.R_LIB_C_AP,
    "LIB_S_AP": L.R_LIB_S_AP,
    "LIB_KEY": L.R_LIB_KEY,
    "LIB_IV": L.R_LIB_IV,
    "LIB_FINISHED": L.R_LIB_FINISHED,
    "HRR": L.R_HRR,
}

RE_ETIQUETTE = re.compile(r"^\s*\.(\w+)\s*:\s*$")
RE_OPERANDE_ETIQUETTE = re.compile(r"^(j\w+|loop\w*|call)\s+\.(\w+)$")
RE_OPERANDE_SYMBOLE = re.compile(r"^(call)\s+(\w+)$")
RE_LEA_ETIQUETTE = re.compile(r"^(lea\s+\w+), \[\.(\w+)\]$")
RE_RIP_CIBLE = re.compile(r"^(.*?\[rip\s*([+-])\s*)(\w+|\.\w+)(\s*\].*)$")

# les registres 64 bits : « call r10 » est l'APPEL INDIRECT DÉCLARÉ de
# tls13-28 (I2 : l'appel indirect sur une cible qui est une DONNÉE du
# contexte n'est NI un import NI un syscall) — PAS un symbole de bloc
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
        if nom in REGISTRES64:
            return ligne          # l'appel indirect DÉCLARÉ (tls13-28 I2)
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
    "tls13-15-aes128-cles-tour": "AES-128 le déploiement des clés de tour (FIPS 197 § 5.2)",
    "tls13-16-aes128-bloc": "AES-128 le chiffrement d'un bloc (l'arrêt AES-NI)",
    "tls13-17-ghash-multiplication": "GHASH la multiplication GF(2^128) (SP 800-38D § 6.3)",
    "tls13-18-gcm-sceller": "GCM sceller (SP 800-38D § 7.1 — CTR + étiquette)",
    "tls13-19-gcm-ouvrir": "GCM ouvrir (le verdict AVANT la restitution, fail-closed)",
    "tls13-20-enregistrement-proteger": "l'enregistrement protéger (RFC 8446 § 5.2)",
    "tls13-21-enregistrement-deproteger": "l'enregistrement déprotéger (l'anti-rejoue par la séquence)",
    "tls13-22-clienthello-composer": "le ClientHello composé (l'offre scellée du jalon, 114 o)",
    "tls13-23-serverhello-traiter": "le ServerHello traité (les refus nommés, le secret partagé)",
    "tls13-24-calendrier-cles": "le calendrier de clés (RFC 8446 § 7.1, trois étages)",
    "tls13-25-finished-calculer-verifier": "le Finished calculé/vérifié (le HMAC du transcript, § 4.4.4)",
    "tls13-26-epinglage": "l'épinglage du certificat (la comparaison, jamais la croyance)",
    "tls13-27-principal-machine-etats": "la machine d'états du client (l'orchestration, § 2)",
    "tls13-28-socle-appel": "le socle d'appel (la rotule de transport à rappels)",
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
