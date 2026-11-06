#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_176.py — LA CONSIGNATION DE LA DETTE DE LA TASK 94 : le
geste « LE CHANTIER M9-(d) : LE SOCLE SOCKET sys-04..06 NOTÉS-MESURÉS-
PROUVÉS » devait porter l'Entrée 176 (la passation l'annonçait : « relu
MATCH : il porte LE SOCLE SOCKET [Entrée 176 — sys-04..06 notés-mesurés-
prouvés : …] + le worklog Task 94 » — le worklog y était, l'Entrée NON :
la passation revendiquait un MATCH jamais constaté sur cette pièce).

La reprise (Task 95) SOLDÉ LA DETTE, DEUX GESTES NOMMÉS :
  1. l'ORDRE 174<175 RESTAURÉ — le défaut de inserer_entree_175.py :
     l'insertion se faisait à l'INDEX de l'en-tête « ## Entrée 174 »
     (donc AVANT elle) au lieu d'après SA SECTION — le journal portait
     173, 175, 174 : la règle « ordre N-1<N<marqueur » violée. La
     correction est un ÉCHANGE PUR : les DEUX sections byte-identiques,
     seules leurs positions s'échangent (constaté par le script AVANT
     l'écriture) ;
  2. JOURNAL_TRAVAIL +Entrée 176 (le geste de la Task 94, consigné au
     worklog à la pointe 686b33e — la source fait foi, l'Entrée la
     suit).

Tout ancrage absent ou inattendu = ÉCHEC NOMMÉ, rien n'est écrit."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 176 — LE CHANTIER M9-(d) : LE SOCLE SOCKET sys-04..06 NOTÉS-MESURÉS-PROUVÉS (07/11)

*Note de la reprise (Task 95) : la présente Entrée fut annoncée par la passation Task 94 (« relu MATCH : il porte LE SOCLE SOCKET [Entrée 176 — sys-04..06 notés-mesurés-prouvés : 676/289/287 o ARRÊTÉS D161-rejoué, le noyau AFD STRICT du harnais 131 contrôles · 131 VERTS × 3 graines, 19 mutantes d'UN point trahies, l'erratum de notation n° 3 consigné sur pièces, l'instrument verifier_specs_m9d.py révisé en phases 1+2 : 116 VERTS] + le worklog Task 94 ») — le worklog y était, l'Entrée NON : la dette de consignation est NOMMÉE et soldée ici. L'ordre 174<175 est restauré dans le même geste (le défaut de inserer_entree_175.py : l'insertion à l'index de l'en-tête 174 au lieu d'après sa section). Le geste ci-dessous est celui de la Task 94 ; sa source fait foi (worklog, pointe 686b33e).*

**La reprise vérifiée avant le geste (« on enchaine »).** drive_sync.py --quiet EXIT 0 (rien à téléverser — le miroir DÉJÀ à la pointe 514f42b [la famille poignée + le principal, Task 93]), l'arbre propre : la reprise voit les specs sys-04..06, le README § 9-14, le plan étendu et l'instrument verifier_specs_m9d.py 93 VERTS (la phase 1 de la couche I DÉJÀ consignée par le développeur — R2 tenue : l'écrit a précédé, la notation attendait SON geste), la réserve instrumentale vivante (keystone/unicorn/capstone).

**Le geste : l'établissement, l'émission, la réception.** sys-04..06 — LA FONDATION I/O que M8 a nommée, notée sur les specs telles quelles : l'ÉTABLISSEMENT (NtCreateFile sur \\Device\\Afd\\Endpoint — le EA AfdOpenPacketXX fixture, le handle SYNCHRONE FILE_SYNCHRONOUS_IO_NONALERT — PUIS IOCTL_AFD_BIND le fixture-WILDCARD CITÉ [le noyau DÉDUIT, le domaine ne décide RIEN de la source] PUIS IOCTL_AFD_CONNECT — le sockaddr du kit COPIÉ à +24 SANS interprétation, les zéros de tête MESURÉS acceptés), l'ÉMISSION (le WSABUF de pile pointe LA CHARGE du kit, P3 traverse, AUCUNE COPIE ; TOTALE ou refus -7, le compte Information consigné — jamais une boucle silencieuse), la RÉCEPTION (bloquante sur le handle synchrone ; LE ZÉRO EST LA DEMI-FIN -7 ; le noyau ÉCRIT chez le kit, le reçu INTÈGRE) ; chaque SSN résolu AU GESTE MÊME par sys-02 — « NtDeviceIoControlFile » résolu DEUX FOIS (l'alternance résoudre-émettre × 3 dans les octets, relu par l'instrument).

**Les mesures, l'arrêt (D161 rejoué — la préfiguration s'est inclinée).** sys-04 676 o (slot 0xA240/0x300, 92 o de NOP), sys-05 289 o (0xA540/0x180, 95 o), sys-06 287 o (0xA6C0/0x180, 97 o) — les slots préfigurés TIENNENT, la réserve contiguë 0xA240 demeure la croissance du domaine ; les fixtures .text6 @ 0x10C20..0x10CE0 CITÉS par les SIX déplacements RIP de sys-04 et l'unique de chacun de 05/06 (relevés par l'instrument — le device UTF-16LE 40/42 [l'erratum n° 2 de l'instrument, corrigé sur pièces AVANT la notation], le EA déterministe 54 o, le bind WILDCARD 20 o, les noms en SPANS).

**La preuve a corrigé la notation et l'instrument — le juge est le code.** L'ERRATUM DE NOTATION n° 3 — le DesiredAccess 0xC0140000 (bit 31 posé) en `mov edx` ZÉRO-étendu, JAMAIS `mov rdx` dont le C7 SIGNERAIT l'extension (0xFFFFFFFFC0140000 : le noyau entier refusé muet) — le round-trip V1 l'a attrapé AVANT que le noyau simulé ne parle, corrigé sur pièces, la consigne citée dans le brouillon ; le noyau AFD strict du harnais a lui-même appris sur pièces : la garde commune refusait le buffer de sortie du BIND (16 o — Q2 de sys-04 : « 16 o de pile pour le BIND, NULL pour le CONNECT ») — la garde déplacée aux gestes qui exigent NULL, le BIND garde SA sortie ; et la leçon canaris : un bloc À cadre appelle des blocs à cadres (sys-02 → memcmp) qui écrivent légitimement SOUS sa trame — la couverture pleine ne juge que les blocs SANS cadre, le harnais gagne le TRACEUR SOUS-CADRE de PROVENANCE (chaque écriture doit venir d'un bloc PRUVÉ sys-02/memcmp scellé M1/sys-01 six octets ou du push taille-8 d'un appel DU bloc — tout autre scribble est une faute NOMMÉE).

**Les preuves : le noyau AFD STRICT du harnais (harnais_sys.py ÉTENDU).** Chaque geste transport VALIDE ses arguments contre le plan : les ONZE du create (DesiredAccess, l'OBJECT_ATTRIBUTES Length 0x30/Attributes 0x40/ni SD ni QoS, l'UNICODE_STRING 40/42 pointant le fixture-device octet pour octet, ShareAccess 3, Disposition 1, CreateOptions 0x20, le EaBuffer CITÉ et sa valeur re-dérivée, EaLength 54), les DIX du bind/connect/send/recv (l'IOCTL du plan, les tailles MESURÉES, le sockaddr recoupé au kit, les zéros de tête, BufferCount 1, les drapeaux : AfdFlags 0 au send — LA MESURE p.3 —, AfdFlags 0x20 au recv — L'ERRATUM DE LECTURE TENU, la littérature en TdiFlags serait REFUSÉE par le noyau même) ; V2d/e/f : la marche create→bind→connect relue aux captures (la séquence MESURÉE, jamais connect sans bind), le SSN suit DEUX modules distincts (0x55/0x56 puis 0xAA/0xBB — au geste même), la TROISIÈME résolution mise à l'épreuve par le noyau qui CORROMPT le stub au bind (le module change sous les pieds : -4 nommé, la marche s'arrête — jamais un numéro en cache), le handle en LOCALE jamais P3 (au -6 des TROIS étages : create, bind, connect — le canari de [P3] constate l'absence de possession partielle, le premier STATUS non nul arrête), l'émission 16406 o d'un geste (la borne TLS 5+2^14+17), la divergence iosb -6, les demi-fins et RESET consignés, les spans -5 AVANT tout ; V3b : 240 cas fuzzés en graine — modules aléatoires (SSN uniques — la leçon du STATUS_INVALIDE : le dispatch suit la fixture, la résolution est la SEULE source du numéro), comportements noyau aléatoires par étage, le modèle de la couche I prédit, l'émulation confrontée verdict par verdict ; V4b : 19 mutantes d'UN point (stables en taille) — le DesiredAccess+1, les IOCTL échangés ou inconnus, le EA tronqué, le MaximumLength faussé, le sockaddr décalé, la fausse source du handle, l'IOSB aveugle, la résolution sautée (js→jns), la garde span inversée, le compteur contre rax, L'ERRATUM FALSIFIÉ DANS LES DEUX SENS (0x20→0 et la littérature 0→0x20 : la MESURE est la SEULE écriture qui passe le noyau), la demi-fin masquée (jz→jnz : le zéro déguisé en succès) — CHACUNE trahit sa batterie, les trois témoins restent verts — **BILAN : 131 contrôles · 131 VERTS × 3 graines (20261105, 424242, 777777)** ; l'instrument verifier_specs_m9d.py révisé en phases 1+2 : **116 VERTS** (C7 inversé : la notation PRÉSENTE + CONCORDANTE — les constantes re-lues de la notation contre le plan re-dérivé, les citations RIP, la marche dans les octets, les brouillons). Le terrain M9-(f) confrontera le VRAI afd.sys de la machine du développeur.

**Détail.** FRONTIÈRES : aucune balise, AUCUN build (le chantier (e) attend : la cérémonie du sceau I de l'ère + le 1.0.0-dev.1 — le garde VERT, la dette de cérémonie demeure), m8/proxy.exe le scellé 0.9.0 INTACT (relu par l'instrument, sha256 1492b0bc…), les notations et specs sys-01..03 INTACTES, l'arbre tls13/I des 28 INTACT, la charte tenue de § 1 à § 14. Livrables : m8/I/ (README révisé M9-(d) + sys-04-transport.md + sys-05-emission.md + sys-06-reception.md), m8/layout.py (les slots sys-04..06 + les fixtures .text6 + les constantes AFD), m8/notation/ (3 brouillons + 3 notations), m8/harnais_sys.py (le NoyauAFD STRICT), m8/outils/auteur.py, scripts/verifier_specs_m9d.py, worklog +Task ID 94. Consignations : la présente Entrée 176 (déposée à la reprise Task 95 — la dette nommée en tête), worklog Task 94 (la pointe 686b33e). SUITE : (e) LA CÉRÉMONIE DU SCEAU I de l'ère + le build 1.0.0-dev.1 (l'oracle structurel y lira : le socket natif SANS une seule entrée d'import réseau), (f) le terrain — LA GRANDE ŒUVRE."""


def refus(nom, detail):
    print(f"[journal] REFUS {nom} : {detail}")
    return 2


def main():
    if not JOURNAL.exists():
        return refus("ANCRAGE", "journal introuvable")
    journal = JOURNAL.read_text(encoding="utf-8")

    if "## Entrée 176" in journal:
        return refus("REJEU", "Entrée 176 déjà consignée (rejeu REFUSÉ)")

    for ancrage in ("## Entrée 173", "## Entrée 174", "## Entrée 175"):
        if ancrage not in journal:
            return refus("ANCRAGE", f"{ancrage} introuvable")
    if MARQUEUR not in journal:
        return refus("ANCRAGE", "marqueur introuvable")

    i173 = journal.index("## Entrée 173")
    i175 = journal.index("## Entrée 175")
    i174 = journal.index("## Entrée 174")
    im = journal.index(MARQUEUR)

    # -- le constat AVANT l'écriture : l'ordre FAUTIF 173 < 175 < 174 < marqueur
    if not (i173 < i175 < i174 < im):
        return refus("ETAT", f"l'ordre constaté n'est pas l'état fautif attendu "
                             f"(173@{i173} 175@{i175} 174@{i174} marqueur@{im}) — "
                             "inserer_entree_176.py refuse d'écrire à l'aveugle")

    avant = journal[:i175]
    s175 = journal[i175:i174]        # la section 175 (mal placée)
    s174 = journal[i174:im]          # la section 174 (mal placée)
    apres = journal[im:]

    # l'échange PUR : sections byte-identiques, seules les positions s'échangent
    if not s175.rstrip("\n").endswith("LA GRANDE ŒUVRE."):
        return refus("CONTENU", "la section 175 ne se termine pas comme attendu")
    if not s174.rstrip("\n").startswith("## Entrée 174"):
        pass  # tautologie de découpage — le contrôle réel est ci-dessous
    if "## Entrée 175" in s174 or "## Entrée 174" in s175:
        return refus("CONTENU", "les sections extraites s'entrelacent — refus")

    nouveau = (avant + s174 + s175 + ENTREE + "\n\n" + apres)

    # -- la vérification AVANT l'écriture : l'ordre RESTAURÉ + le contenu préservé
    v173 = nouveau.index("## Entrée 173")
    v174 = nouveau.index("## Entrée 174")
    v175 = nouveau.index("## Entrée 175")
    v176 = nouveau.index("## Entrée 176")
    vm = nouveau.index(MARQUEUR)
    if not (v173 < v174 < v175 < v176 < vm):
        return refus("VERIF", "l'ordre restauré 173<174<175<176<marqueur ne tient pas")
    # les DEUX sections échangées demeurent byte-identiques (sommes de contrôle)
    import hashlib
    def condense(txt):
        return hashlib.sha256(txt.encode("utf-8")).hexdigest()[:16]
    if condense(s174) != condense(nouveau[nouveau.index("## Entrée 174"):
                                          nouveau.index("## Entrée 175")]):
        return refus("VERIF", "la section 174 a changé au passage — refus")
    if condense(s175) != condense(nouveau[nouveau.index("## Entrée 175"):
                                          nouveau.index("## Entrée 176")]):
        return refus("VERIF", "la section 175 a changé au passage — refus")

    JOURNAL.write_text(nouveau, encoding="utf-8")
    print("[journal] l'ORDRE 174<175 RESTAURÉ (l'échange pur, sections "
          "byte-identiques) + Entrée 176 (ordre 175<176<marqueur) — la dette "
          "de consignation Task 94 est SOLDÉE")
    print(f"[journal] sections échangées : 174 {condense(s174)}… · "
          f"175 {condense(s175)}… (constatées AVANT l'écriture)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
