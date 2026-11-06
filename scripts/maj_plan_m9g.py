#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""maj_plan_m9g.py — LA CONSIGNATION DU PLAN, LA DETTE DE DEUX GESTES :

  1. la dette de la Task 93 — le worklog consignait « PLAN (chantier (b) :
     la famille poignée + le principal + État du programme) » mais
     maj_plan_m9f.py n'avait remplacé QUE la rangée (b) : la phrase
     « Entrée 175 » de l'État du programme MANQUAIT (constaté à la reprise
     Task 95 : la sonde « Entrée 175 » ne trouvait que la rangée (b)) ;
  2. la dette de la Task 94 — le geste M9-(d) (LE SOCLE SOCKET) n'avait
     consigné NI la rangée (d), NI la phrase « Entrée 176 » de l'État du
     programme (la passation revendiquait pourtant « il porte ... [Entrée
     176 — sys-04..06 notés-mesurés-prouvés ...] » — un MATCH jamais
     constaté sur cette pièce).

DEUX remplacements ASSERTÉS — tout ancrage manquant ou déjà passé = ÉCHEC
NOMMÉ, rien n'est écrit :
  - l'État du programme : les phrases Entrée 175 (poignée + principal) puis
    Entrée 176 (socle socket) insérées APRÈS la phrase Entrée 174, AVANT
    « Les chantiers M6-(a) » ;
  - la rangée M9-(d) : la complétion RÉALISÉ appendue au critère."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"

# -- remplacement 1 : l'État du programme (les deux phrases dues) --------------

ANCRE_ETAT = ("les verdicts 32 bits → le 64 bits signé].** Les chantiers M6-(a)")

PHRASE_175 = (
    " **LA FAMILLE poignée + LE PRINCIPAL NOTÉS-MESURÉS-PROUVÉS le "
    "07/11/2026 (Entrée 175)** (tls13-22..28 : le ClientHello composé "
    "[114 o FIXES, la composition par octets aux offsets constants, "
    "l'aléa @ +6, la clé @ +82, AUCUNE branche de données — charte § 1 : "
    "le message est FIXE], le ServerHello traité [la marche BORNÉE, "
    "chaque confrontation NOMMÉE dans l'ordre du corps : le type, la "
    "version, l'aléa ≠ LA VALEUR MAGIQUE HRR par OU cumulatif au fixture "
    "R_HRR, LA SUITE 0x1301 lue GROS-BOUTISTE → -5 LA NÉGOCIATION "
    "REFUSÉE, la compression, la région d'extensions qui DOIT épuiser le "
    "corps, supported_versions 0x0304 PRÉSENTE, key_share x25519 32 o "
    "PRÉSENTE, les extensions inconnues IGNORÉES, l'épuisement exact ; "
    "tls13-13 APRÈS le dernier refus : la clé privée n'est JAMAIS touchée "
    "sur un message refusé], le calendrier de clés à TROIS étages STRICTS "
    "[RFC 8446 § 7.1 : le dispatch EST l'étape, -3 sur tout saut, "
    "l'étape 4 n'existe pas : CLOS ; SEIZE étiquettes HKDF aux fixtures "
    "R_LIB_* du plan, TROIS extraits, QUATRE déploiements tls13-15, LE "
    "CONDENSÉ DU VIDE dérivé par tls13-01+04 au geste même — l'erratum "
    "n° 2 : le contexte de « derived » est Hash(vide) 32 o, JAMAIS zéro "
    "octet ; les contextes sortis COMPLETS : rk 176 + IV 12 + réserve + "
    "séquence 0 ; le hash du transcript est un ARGUMENT — le calendrier "
    "ne hache RIEN], le Finished calculé/vérifié [DEUX modes NOMMÉS sur "
    "r9, le reçu CONFRONTÉ par OU cumulatif des 32 différences, LE test "
    "À LA FIN — la discipline du verdict AEAD, le reçu JAMAIS modifié], "
    "l'épinglage [le SHA-256 du DER sur un contexte de PILE, la "
    "comparaison TEMPS CONSTANT — l'empreinte est une donnée de "
    "CONFIANCE, -6 NOMMÉ], LA MACHINE D'ÉTATS du client ENTIER "
    "[tls13-27 : QUATRE événements NOMMÉS — OUVRIR/ÉMETTRE/RECEVOIR/"
    "FERMER — sur le contexte session 17 520 o à la disposition DÉCLARÉE, "
    "LA LISTE FERMÉE des compositions [31 sites d'appel directs + "
    "tls13-28 ×10 pour TOUTE entrée/sortie], le transcript INITIALISÉ "
    "[tls13-01 — la session naît VIERGE] puis chaque message complet "
    "ABSORBÉ AVANT traitement [charte § 4], les coupes du hash sur la "
    "COPIE, le réassemblage au tampon @ +1136 borné 2^14 NOMMÉ, le "
    "certificat : l'extraction de la PREMIÈRE entrée [le u24 lu — le "
    "DÉTROIT de tls13-26], le CertificateVerify ABSORBÉ sans vérification "
    "cryptographique [le chantier futur nommé : la confiance a tranché à "
    "l'épinglage], LA DISCIPLINE D'ÉCHEC : tout verdict négatif PROPAGÉ "
    "NOMMÉ, l'état passe à 5 [MORT], un échec n'ÉMET RIEN de plus que "
    "l'offre déjà partie] et la rotule tls13-28 [le socle à DEUX rappels "
    "en argument, L'APPEL INDIRECT DÉCLARÉ — la cible est une DONNÉE du "
    "contexte : NI un import NI un syscall ; le zéro de réception est le "
    "refus -7 du KIT ; AUCUNE copie — l'adaptateur]) : la notation à la "
    "main (241/532/2130/239/285/2906/144 o, round-trip 100 %, les slots "
    "ARRÊTÉS 0x120/0x240/0x880/0x100/0x140/0xB80/0xB0 tassés depuis "
    "0xED00 — la poignée finit 0xFB20 SOUS les fixtures x25519 immobiles "
    "[miroir R7], le principal 0xFF40..0x10B30 — LA MARGE A FRANCHI "
    "0xF000 comme le plan l'avait nommé, les fixtures libellés+HRR à "
    "leur ARRÊT, D161 rejoué) ; LE HARNAIS 52 contrôles · 52 VERTS × 3 "
    "graines — **LE TRANSFERT RFC 8448 BLOC PAR BLOC** (le SH du RFC "
    "VERBATIM → LE SECRET PARTAGÉ octet pour octet ; le calendrier sur "
    "les hash CONSIGNÉS → LES SECRETS consignés, LES QUATRE CHAÎNES du "
    "TRANSFERT_8448 et les DEUX Finished [le client CALCULÉ a8ec436d…, "
    "le serveur VÉRIFIÉ 9b9b141d…, un octet muté → -4] ; l'épinglage), "
    "LA SESSION ENTIÈRE CONTRE LE SIMULATEUR (OUVRIR → l'état 3 : le "
    "journal == NOTRE CH cadré + NOTRE Finished [le SH du RFC servi "
    "verbatim, le vol re-scellé sous nos clés, le Finished serveur "
    "recalculé sur NOTRE coupe] ; la session recoupée champ par champ ; "
    "ÉMETTRE/RECEVOIR les charges du § 3 sous NOS chaînes == la "
    "référence octet pour octet ; la close_notify des deux côtés ; LA "
    "FALSIFICATION à chaque étage : le SH muté → -5, l'étiquette du vol "
    "mutée → -4, l'empreinte du kit mutée → -6, LA COUPURE DU SOCLE → "
    "-7, OUVRIR sur l'état 3 → -3, l'état 5 [MORT] ne rend PLUS RIEN), "
    "l'alignement msx64 **205 entrées à travers LA SESSION ENTIÈRE — "
    "l'imbrication COMPTÉE**, le kit INTACT ; DOUZE FAUTES nommées par "
    "le fail-closed, l'erratum n° 2 consigné sur pièces AVANT la "
    "notation — **LE DOMAINE tls13 EST COMPLET : LES 28 BLOCS "
    "notés-mesurés-prouvés, de SHA-256 à la machine d'états**"
)

PHRASE_176 = (
    " ; **LE SOCLE SOCKET sys-04..06 NOTÉ-MESURÉ-PROUVÉ le 07/11/2026 "
    "(Entrée 176, Task 94)** (l'ère 1.0.0 du transport : l'ÉTABLISSEMENT "
    "[NtCreateFile sur \\Device\\Afd\\Endpoint — le EA AfdOpenPacketXX "
    "fixture, le handle SYNCHRONE FILE_SYNCHRONOUS_IO_NONALERT — PUIS "
    "IOCTL_AFD_BIND le fixture-WILDCARD CITÉ : le noyau DÉDUIT, le "
    "domaine ne décide RIEN de la source ; PUIS IOCTL_AFD_CONNECT — le "
    "sockaddr du kit COPIÉ à +24 SANS interprétation, les zéros de tête "
    "MESURÉS acceptés], l'ÉMISSION [le WSABUF de pile pointe LA CHARGE "
    "du kit, P3 traverse, AUCUNE COPIE ; TOTALE ou refus -7, le compte "
    "Information consigné — jamais une boucle silencieuse], la RÉCEPTION "
    "[bloquante sur le handle synchrone ; LE ZÉRO EST LA DEMI-FIN -7 ; "
    "le noyau ÉCRIT chez le kit, le reçu INTÈGRE] ; chaque SSN résolu AU "
    "GESTE MÊME par sys-02 — « NtDeviceIoControlFile » résolu DEUX FOIS "
    "dans les octets, relu par l'instrument) : la notation 676/289/287 o "
    "(round-trip 100 %) aux slots ARRÊTÉS 0xA240/0x300 · 0xA540/0x180 · "
    "0xA6C0/0x180 (D161 rejoué — la réserve contiguë 0xA240 demeure la "
    "croissance du domaine), les fixtures .text6 @ 0x10C20..0x10CE0 (le "
    "device UTF-16LE 40/42 [l'erratum n° 2 de l'instrument, corrigé sur "
    "pièces AVANT la notation], le EA déterministe 54 o, le bind "
    "WILDCARD 20 o, les noms NT en SPANS) ; le harnais ÉTENDU au NOYAU "
    "AFD STRICT — **131 contrôles · 131 VERTS × 3 graines** (les ONZE du "
    "create, les DIX du bind/connect/send/recv — l'IOCTL du plan, les "
    "tailles MESURÉES, le sockaddr recoupé, les drapeaux : AfdFlags 0 au "
    "send [LA MESURE p.3], AfdFlags 0x20 au recv [L'ERRATUM DE LECTURE "
    "TENU] —, la marche create→bind→connect relue aux captures, le SSN "
    "suit DEUX modules distincts, le noyau CORROMPT le stub au bind "
    "[-4 nommé : jamais un numéro en cache], le handle en LOCALE jamais "
    "P3, l'émission 16406 o d'un geste, 240 cas fuzzés en graine, 19 "
    "mutantes d'UN point trahies — L'ERRATUM FALSIFIÉ DANS LES DEUX "
    "SENS, la demi-fin masquée) ; l'erratum de notation n° 3 consigné "
    "sur pièces (le DesiredAccess 0xC0140000 [bit 31 posé] en mov edx "
    "ZÉRO-étendu, JAMAIS mov rdx dont le C7 SIGNERAIT l'extension — le "
    "round-trip V1 l'a attrapé AVANT le noyau simulé) ; le traceur "
    "SOUS-CADRE de PROVENANCE (les cadres des blocs prouvés ne sont pas "
    "des scribbles) ; l'instrument verifier_specs_m9d.py révisé en "
    "phases 1+2 : 116 VERTS ; le VRAI afd.sys de la machine du "
    "développeur attend le chantier (f)**"
)

# -- remplacement 2 : la rangée M9-(d) -----------------------------------------

ANCRE_ROW = "la fondation I/O nommée par M8 TENUE |"

COMPLETION_ROW = (
    "la fondation I/O nommée par M8 TENUE — **RÉALISÉ le 07/11/2026 "
    "(Entrée 176, Task 94) : LE SOCLE SOCKET sys-04..06 NOTÉ-MESURÉ-"
    "PROUVÉ** — l'établissement (NtCreateFile sur \\Device\\Afd\\Endpoint, "
    "le EA AfdOpenPacketXX fixture, le handle SYNCHRONE, le bind "
    "IMPLICITE WILDCARD — le noyau DÉDUIT l'adresse, jamais le domaine — "
    "puis IOCTL_AFD_CONNECT, le sockaddr du kit COPIÉ SANS "
    "interprétation), l'émission (le WSABUF pointe LA CHARGE du kit, "
    "TOTALE ou refus -7 — jamais une boucle silencieuse), la réception "
    "(BLOQUANTE sur le handle synchrone, LE ZÉRO EST LA DEMI-FIN -7, le "
    "noyau ÉCRIT chez le kit) ; chaque SSN résolu AU GESTE MÊME par "
    "sys-02 (« NtDeviceIoControlFile » DEUX FOIS dans les octets) ; la "
    "notation 676/289/287 o aux slots ARRÊTÉS 0xA240/0x300 · 0xA540/"
    "0x180 · 0xA6C0/0x180 (D161 rejoué), les fixtures .text6 @ "
    "0x10C20..0x10CE0 ; le harnais ÉTENDU au NOYAU AFD STRICT : 131 "
    "contrôles · 131 VERTS × 3 graines (20261105, 424242, 777777), 19 "
    "mutantes d'UN point trahies ; l'erratum de notation n° 3 consigné "
    "sur pièces (le DesiredAccess en mov edx ZÉRO-étendu — le round-trip "
    "l'a attrapé AVANT le noyau simulé) ; l'instrument "
    "verifier_specs_m9d.py : 116 VERTS ; LE VRAI afd.sys de la machine "
    "du développeur attend le chantier (f) |"
)


def main():
    if not PLAN.exists():
        sys.exit("ÉCHEC : plan introuvable")
    plan = PLAN.read_text(encoding="utf-8")

    # -- remplacement 1 : l'État du programme (les phrases dues 175 + 176) -----
    debut_etat = plan.find("**État du programme.**")
    if debut_etat < 0:
        sys.exit("ÉCHEC : l'État du programme introuvable")
    fin_etat = plan.index("\n", debut_etat)
    paragraphe = plan[debut_etat:fin_etat]
    if "Entrée 175" in paragraphe or "Entrée 176" in paragraphe:
        sys.exit("ÉCHEC : une phrase Entrée 175/176 déjà présente à l'État "
                 "du programme (rejeu REFUSÉ)")
    if ANCRE_ETAT not in paragraphe:
        sys.exit("ÉCHEC : l'ancre État du programme (fin Entrée 174 → "
                 "« Les chantiers M6-(a) ») introuvable")
    plan = plan.replace(
        ANCRE_ETAT,
        "les verdicts 32 bits → le 64 bits signé].**" + PHRASE_175
        + PHRASE_176 + " Les chantiers M6-(a)",
        1)

    # -- remplacement 2 : la rangée M9-(d) --------------------------------------
    if plan.count(ANCRE_ROW) != 1:
        sys.exit(f"ÉCHEC : l'ancre rangée (d) attendue UNE fois, "
                 f"trouvée {plan.count(ANCRE_ROW)} fois")
    if "RÉALISÉ le 07/11/2026 (Entrée 176, Task 94)" in plan:
        sys.exit("ÉCHEC : la rangée (d) déjà complétée (rejeu REFUSÉ)")
    plan = plan.replace(ANCRE_ROW, COMPLETION_ROW, 1)

    # -- la vérification AVANT écriture ------------------------------------------
    d = plan.find("**État du programme.**")
    etat = plan[d:plan.index("\n", d)]
    for sonde in ("(Entrée 175)", "(Entrée 176, Task 94)",
                  "LE DOMAINE tls13 EST COMPLET", "LE SOCLE SOCKET"):
        if sonde not in etat:
            sys.exit(f"ÉCHEC : la sonde « {sonde} » absente de l'État du "
                     "programme après remplacement — rien n'est écrit")
    if plan.count("RÉALISÉ le 07/11/2026 (Entrée 176, Task 94)") != 1:
        sys.exit("ÉCHEC : la complétion (d) absente ou dupliquée")

    PLAN.write_text(plan, encoding="utf-8")
    print("[plan] État du programme : +les phrases Entrée 175 (poignée + "
          "principal — LA DETTE Task 93) et Entrée 176 (socle socket — LA "
          "DETTE Task 94), insérées après la phrase Entrée 174")
    print("[plan] rangée M9-(d) : RÉALISÉ (Entrée 176, Task 94) — LE "
          "SOCLE SOCKET noté-mesuré-prouvé, le VRAI afd.sys attend le (f)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
