#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tls13/layout.py — LE PLAN D'ADRESSAGE DU DOMAINE tls13 (M9, l'ère 1.0.0).

La source unique des constantes du domaine (le modèle m8/layout.py, D161) :
la suite arrêtée, la table des verdicts, les versions de l'ère, les
constantes publiques de la famille sha et la PRÉFIGURATION .text6.

LA PRÉFIGURATION N'EST PAS UN DROIT (D161, la leçon de M8-(b)) : les RVA et
tailles définitifs des blocs seront ARRÊTÉS au chantier de la notation sur
les LONGUEURS RÉELLES mesurées (auteur.py décide, la préfiguration s'incline)
; seuls les constantes immuables (les valeurs de spécification) et les bornes
d'héritage (le scellé 0.9.0, R7) sont ARRÊTÉS ici.
"""

# --- La suite arrêtée (charte § 1 : une constante, jamais une négociation) ------

SUITE = 0x1301                     # TLS_AES_128_GCM_SHA256 (RFC 8446 §9.1)
GROUPE = 0x001D                    # x25519 (RFC 7748)
PREFIXE_ETIQUETTE = b"tls13 "      # RFC 8446 §7.1 (le NUL de terminaison

# --- Les versions de l'ère (le miroir m8 : 0x00090001 = 0.9.0-dev.1) ----------

VERSION_DEV = 0x01000001           # 1.0.0-dev.1 (geste de BUILD, jamais scellage)
VERSION_FINALE = 0x01000000        # 1.0.0 (le scellage est un fait de carte, D165)

# --- La table des SEPT verdicts du domaine (charte § 5 : l'échec nommé) --------

VERDICTS = {
    0: "OK",
    -1: "argument invalide",
    -2: "taille ou longueur invalide",
    -3: "état du domaine invalide (contexte non initialisé / calendrier divergent)",
    -4: "cryptographie divergente (étiquette AEAD, Finished) — fail-closed",
    -5: "négociation refusée (le ServerHello diverge de la suite proposée)",
    -6: "épinglage divergent (l'empreinte du certificat ≠ l'attendue)",
    -7: "transport en échec (le socle sys a rendu un NTSTATUS non nul)",
}

# --- Les constantes publiques de la famille sha (tls13-01..04) -----------------

SHA_H0 = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
          0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)   # FIPS 180-4 §5.3.1
SHA_TAILLE_BLOC = 64
SHA_TAILLE_CONDENSE = 32
SHA_CTX = 112          # H[8]u32 @+0 · tampon[64] @+32 · remplissage @+96 ·
                       # réservé @+100 · total u64 @+104 (la disposition ah)

# --- La borne d'héritage (le scellé 0.9.0 — R7, ne bouge jamais) ---------------

TEXT5_RAW_M8 = 0xAE00             # la fin du fichier m8/proxy.exe scellé
TAILLE_FICHIER_M8 = 0xAE00        # 44 544 o (l'ancre : le corps hérité)

# --- La PRÉFIGURATION .text6 (ARRÊT à la notation — D161) ----------------------

# La 8e section suit .text5 : raw 0xAE00, RVA 0xC000 (SizeOfImage 0xC000 du
# scellé 0.9.0 → la nouvelle image s'étend, la marge d'en-têtes 0x400 reçoit
# le HUITIÈME en-tête — le constat s'y refera au chantier du build, le
# décalage de packaging D94 n'est pas rejoué).
TEXT6_RAW = TEXT5_RAW_M8          # préfiguration : la mesure décidera
TEXT6_VA = 0xC000                 # préfiguration : aligné SectionAlignment

# Les slots des 28 blocs : PRÉFIGURÉS en tassé depuis TEXT6_VA (D8 : multiples
# de 64, alignés 16, padding >= 16) — ARRÊTÉS à la notation sur les longueurs
# réelles (D161 : sys-01 fut préfiguré 0x40 et le resta ; sys-02 0x140 → 0x140
# ; la préfiguration s'incline devant la mesure, TOUJOURS).
TAILLE_SLOT_PREFIGUREE = 0x200    # par bloc, préfiguration généreuse
