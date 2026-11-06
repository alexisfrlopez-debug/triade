#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_178.py — LA CONSIGNATION DU GESTE « LA CÉRÉMONIE DU BUILD
1.0.0 SOLDÉE, L'ERRATUM n° 4 NOMMÉ AU CHANTIER, LE BUILD 1.0.0-dev.1 NÉ » :
JOURNAL_TRAVAIL +Entrée 178 (ordre 177<178<marqueur, rejeu REFUSÉ),
worklog +Task ID 96. Tout ancrage absent = ÉCHEC NOMMÉ, rien n'est écrit.

La datation : la présente porte le 06/11 (le geste du développeur « signatures
déposées dans le drive /test » reçu le 06/11 ; les horodatages du build :
06/11 — l'heure locale du labo)."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 178 — LA CÉRÉMONIE DU BUILD 1.0.0 SOLDÉE (« signatures déposées dans le drive /test ») ; L'ERRATUM n° 4 nommé AU chantier du build : le chevauchement tls13-27/28 réparé à la source ; LE BUILD EXÉCUTÉ — tls13/proxy.exe 1.0.0-dev.1 NÉ, la carte GÉNÉRATION 9, le verrou croisé 86/86 (06/11)

**Le geste du développeur reçu, recoupé, déposé — la dette de cérémonie SOLDÉE.** La remise rapatriée du /test du Drive par scripts/rapatrier_remise_ceremonie.py (le modèle rapatrier_preuves_m7d.py, D99 : zéro mélange, lecture seule) : les DEUX pièces du geste téléchargées, md5 contrôlés PAR PIÈCE contre les métadonnées Drive (signatures-I.txt 1 847 o, md5 62c43222… ; cle-publique-I.txt 65 o, md5 188a7d42…), LA RÈGLE D'OR recoupée (la clé déposée COMMENCE par 173fae9c… == la clé du 04/11, RÉUTILISÉE — jamais « generer »), la remise recoupée (TREIZE lignes, arbres+balises == a-signer.txt local, les DEUX empreintes nouvelles présentes : m8 sys.1 72aadd38… + tls13 tls13.1 42559862…) ; LE DÉPÔT : python3 v06/sceau_I.py deposer signatures-I.txt --cle cle-publique-I.txt — L'ATOMICITÉ DE CÉRÉMONIE (toute remise vérifiée AVANT toute écriture : clé, signatures et manifestes basculent ENSEMBLE ou pas du tout) : 13 signatures installées, manifestes vivants, l'état « reelle (ceremonie hors-ligne, D87) » ; LE GARDE REPASSÉ : sceau_I.py verifier → TREIZE arbres VERTS (code 0), sceau_I.py etat → la clé 173fae9c…, les DEUX arbres re-signés SIGNE (vert) — la clé privée n'a JAMAIS traversé le bac à sable (le contrat D87 : seuls les DEUX fichiers publics du geste ont remonté du /test).

**L'erratum n° 4 — le chevauchement tls13-27/28 NOMMÉ au chantier du build (la préparation du build lit le plan d'adressage : la sonde a nommé la faute AVANT l'artefact — la méthode a tenu, le juge est le code).** LE CONSTAT sur pièces (scripts/sonde_erratum_tls13_27.py, la pièce rejouable : assemble les notations aux RVA du plan et calcule les bornes réelles du code) : tls13-27 MESURÉ 2906 o (la re-mesure après les DOUZE fautes corrigées du geste poignée — la première mesure disait 2864 o → slot 0xB40), le slot ré-arrêté 0xB80 SANS DÉPLACER tls13-28 (demeuré 0x10A80 = l'ancienne fin 0xB40) : la fin du code [0x10A80, 0x10A9A) recouvrait le socle posé à 0x10A80 — .refus_pre_taille @0x10A80 (le verdict -2) et .refus_contexte_nul @0x10A92 (le verdict -1) de la machine d'états VIVAIENT DANS tls13-28 ; LE HARNAIS N'A PAS VU (la preuve a ses limites nommées) : la pose n'écrit que le code (mem_write(rva, octets) — la dernière pose gagne) et les chemins -1/-2 n'étaient JAMAIS exercés par les 52 contrôles (verts sur des chemins sains — la faute dormait dans les refus). LA RÉPARATION À LA SOURCE (jamais un correctif local) : tls13/layout.py — TLS28_VA 0x10A80 → 0x10AC0 (la fin du slot ré-arrêté du principal ; le commentaire d'arrêt corrigé : l'erratum consigné au plan d'adressage, la source unique), outils/auteur.py RE-JOUÉ (les notations 27/28 re-générées : SEULES les cibles des DIX appels de 27 [0x10a80 → 0x10ac0] et le socle décalé +0x40 changent — les VINGT-SIX autres notations byte-identiques, git diff constaté), harnais_poignee.py RE-JOUÉ aux TROIS graines consignées (20261107/41/20261108) : 52/52 VERTS CHACUNE ; les fixtures demeurés à leur ARRÊT (R_LIB_* 0x10B80+ : tls13-28 finit 0x10B70, l'écart 0x10 tient ; U9/EXP_INV immobiles 0xFF00/0xFF20, miroir R7) ; LE CONTRÔLE PERMANENT : l'oracle structurel M9 porte désormais « slots-disjoints » (+ les fixtures hors slots, + la composition intégrale) — la faute ne peut plus dormir. NOTE D8 : l'oracle exige le padding >= 16 et l'alignement 16 (LA DÉCISION) ; la convention « multiple de 64 » est celle de l'ère M8 — tenue par les 26 autres slots tls13 et par les SIX du socle, DÉCLINÉE par l'arrêt consigné de l'Entrée 175 aux minimums alignés 16 (0x120/0xB0) : la note est consignée au layout.

**Le build 1.0.0-dev.1 NÉ (tls13/build_m9.py + tls13/carte_m9.py — le modèle build_m8/carte_m8, l'ère 1.0.0).** LA CHAÎNE : le garde sceau-I 13/13 AVANT construire() (les TREIZE arbres, le plan rangée (e) l'exigeait) ; l'héritage RE-VÉRIFIÉ : la chaîne M3+M4+M5 (oracles structurels 524/492/312 verrous) + l'ancre 0.6.0 (c1e46fb0…) PUIS la recomposition 0.9.0 (sys-01..03) CONFRONTÉE OCTET PAR OCTET au scellé m8/proxy.exe (1492b0bc… — scripts/sonde_ancre_090.py d'abord, puis le geste même du build : l'ancre R7 de l'ère M9, le corps que la 1.0.0 étend SANS le bouger) ; LE SOCLE : sys-04 (676 o)/sys-05 (289 o)/sys-06 (287 o) assemblés round-trip 100 % + l'oracle structurel socle (71 verrous : la séquence create→bind→connect, les fixtures .text6 cités, la convention M8 multiple-de-64 tenue) ; LES 28 BLOCS tls13 assemblés round-trip 100 % + l'oracle structurel tls13 (589 verrous : AUCUN IAT PAR BLOC tls13 [la preuve structurelle], AUCUN site syscall [l'unique site du domaine : sys-01 @0xA000, les nouveaux émettent PAR le trombone], les appels directs FERMÉS au plan [l'appel indirect DÉCLARÉ : la rotule tls13-28, call r10 ×2 — la cible est une DONNÉE du contexte], les déplacements RIP == les fixtures déclarés [deplacements_declares rejoué], LES SLOTS DISJOINTS, D8 [padding >= 16, aligné 16]) ; LA COMPOSITION : .text5 (le socle socket posé dans la réserve int3 VÉRIFIÉE du scellé [0xA240, 0xA840), la réserve [0xA840, 0xBFFF) demeurant int3), .rdata (K[64] @0x2F00-0x2FFF — la réserve VIERGE vérifiée du scellé 0.9.0, ÉPUISÉE par la table de SHA-256 de tls13-02, FIPS 180-4 § 4.2.2 ; la version 0x01000001 @0x2820 — LE delta R10, geste de BUILD, JAMAIS scellage), .text6 NOUVELLE (0xC000-0x10FFF, raw 0xAE00, vsize == rawsize 0x5000 — la convention .text5 : la zone réservée int3 DANS le fichier ; base int3, les 28 slots code+NOP, les fixtures aux ARRÊTS consignés : U9/EXP_INV @0xFF00/0xFF20, les HUIT libellés du calendrier + la valeur magique HRR @0x10B80..0x10BF0, le transport AFD @0x10C20..0x10CF0 [le device UTF-16LE + NUL 42 o, le EA déterministe 54 o, le bind WILDCARD 20 o, les TROIS spans de résolution NT] — les fixtures DÉRIVÉS des constantes du plan, l'EA et le bind par les fonctions du harnais M8, la seule source, jugée par verifier_specs_m9d) ; LE PE : HUIT sections (les en-têtes 648 o <= 0x400 — le décalage D94 n'est PAS rejoué), SizeOfImage 0xC000 → 0x11000, taille 0xAE00 → 0xFE00, l'entrée 0x8C80 INCHANGÉE (le principal n'est pas recâblé — la pièce rapportée, câblée au chantier (f)), AUCUN import nouveau (kernel32/ws2_32/secur32 hérités M4/M5 : le socket natif SANS une seule entrée d'import réseau PAR LES BLOCS NOUVEAUX — ws2_32 n'est JAMAIS importé par eux, l'oracle structurel le constate instruction par instruction) ; LA VALIDATION INTÉGRALE (valider_pe_m9) : chaque octet de .text6 COMPTÉ (les 28 slots == les blobs assemblés relus, les 17 fixtures == les valeurs dérivées relues, LE RESTE INT3 — la composition ne peut rien cacher), les portes R10 (28 entrées) + la porte M5 relues, la preuve R7 (.text/.text2/.text3/.text4/.data octet-identiques au scellé 0.9.0, .rdata SAUF la version + K[64] dans la zone VIERGE vérifiée, .text5 : sys-01..03 intacts + le socle dans la réserve int3 VÉRIFIÉE du scellé, .text6 NOUVELLE, les deltas PE documentés) ; LES ORACLES DIFFÉRENTIELS : M4 560 + M5 365 cas verts (l'héritage rejoué) + le harnais sys 131 contrôles VERTS (les SIX blobs : le socle socket compris, l'empreinte 9cc013dd3cc93b42, la graine 20261106) ; L'ARTEFACT : tls13/proxy.exe 1.0.0-dev.1, 65 024 o (0xFE00), sha256 9ed63f3901d044b32de8bd350ab3209303ea1c63167a4752801712a4bd45d283 — DÉTERMINISTE (re-construit byte-identique : le sha annoncé par la pièce, le re-jeu le constate) ; LA CARTE GÉNÉRATION 9 (tls13/carte_m9.py : GENERATION 9, sel Argon2id « TRIADE-M9-carte-argon2id-v1 », VERSION_DEV1 « 1.0.0-dev.1 », la lignée D80 + la graine durable D144 — LA RELÈVE AU COFFRE : coffre_fort.bin rapatrié du Drive racine [md5 contrôlé], obtenir TRIADE lignee-D80 → .keys/passphrase.txt + TRIADE graine-ed25519-cartes → .keys/ed25519.seed [octets bruts 32 o], LE TÉMOIN TENU : pub e9cd8c5494852695…]) : 86 blocs indexés sur 8 artefacts (55 de l'ère close + 3 du socle + 28 du domaine), les contrats des 31 nouveaux PARSÉS des spécifications I (R2 : la couche I est la source — sig/pre/post/inv des specs, deps des en-têtes de notation : jamais une copie d'écriture), 4 fragments chiffrés XChaCha20-Poly1305 + signature Ed25519 ; LE VERROU CROISÉ : 86/86 empreintes revérifiées + la signature + la racine (R8/R9) ; le tableau de bord écrit (tls13/carte/tableau-de-bord.txt).

**Détail.** FRONTIÈRES : le scellé 0.9.0 INTACT (m8/proxy.exe 1492b0bc… — relu par la recomposition confrontée, l'artefact de l'ère close ne bouge pas), la carte génération 8 scellée INTACTE (l'ère close), les arbres I INCHANGÉS par le geste (l'erratum n° 4 touche tls13/layout.py + tls13/notation/ — HORS du sceau : le sceau couvre <arbre>/I/, la couche I est FINALE), AUCUNE balise posée (la 1.0.0-dev.1 est un geste de BUILD ; la finale 1.0.0 attend le terrain vert du chantier (f) — le scellage sera un fait de carte, D104), la clé privée JAMAIS traversée (D87), les six harnais du domaine REJOUÉS au seul harnais poignée (l'erratum n° 4 touche 27/28 : la famille poignée + le principal — les CINQ familles précédentes relues par l'oracle structurel du build, leurs notations byte-identiques). Livrables : scripts/rapatrier_remise_ceremonie.py, download/remise-ceremonie-100/ (les deux pièces md5 contrôlés), scripts/sonde_erratum_tls13_27.py (la pièce de l'erratum n° 4, rejouable), scripts/sonde_ancre_090.py (la pièce de l'ancre R7, rejouable), tls13/layout.py (TLS28_VA 0x10AC0 + les commentaires d'arrêt + la note D8), tls13/notation/ (27/28 re-générées), tls13/carte_m9.py (la carte génération 9), tls13/build_m9.py (le build de l'ère), tls13/proxy.exe (l'artefact 1.0.0-dev.1, 65 024 o, sha256 9ed63f39…), tls13/carte/ (la carte génération 9 + le tableau de bord), .keys/ (la relève de session — JAMAIS commise). Consignations : la présente Entrée 178 PAR SCRIPT, PLAN (la rangée (e) + l'État du programme PAR maj_plan_m9i.py), worklog +Task ID 96. SUITE : le chantier (f) — LE TERRAIN, LA GRANDE ŒUVRE : le kit au coffre /test (l'artefact + le scénario : la session RÉELLE avec un serveur réel — le VRAI ntdll lu par sys-02, les sockets par les syscalls AFD directs, l'épinglage de l'empreinte attendue, la ligne applicative chiffrée échangée de bout en bout par LE CLIENT TLS 1.3 ENTIER en blocs scellés) ; si vert : la finale 1.0.0 (le scellage, fait de carte — D104) et le jalon M9 franchi."""

TASK = """## Task ID 96 — LA CÉRÉMONIE DU BUILD 1.0.0 SOLDÉE ; L'ERRATUM n° 4 (le chevauchement tls13-27/28) NOMMÉ AU CHANTIER ET RÉPARÉ À LA SOURCE ; LE BUILD EXÉCUTÉ : tls13/proxy.exe 1.0.0-dev.1 NÉ, la carte GÉNÉRATION 9, le verrou croisé 86/86 (06/11)

- LA CÉRÉMONIE SOLDÉE (« signatures déposées dans le drive /test ») :
  rapatrier_remise_ceremonie.py — les DEUX pièces md5 contrôlés par pièce
  contre le Drive, la clé du 04/11 CONSTATÉE (173fae9c…, réutilisée), la
  remise recoupée (13 lignes == a-signer local, les DEUX empreintes
  nouvelles) ; sceau_I.py deposer --cle : L'ATOMICITÉ DE CÉRÉMONIE (tout
  vérifié AVANT toute écriture) — 13 signatures installées, l'état
  « reelle » ; LE GARDE REPASSÉ : 13/13 arbres VERTS. La clé privée
  n'a JAMAIS traversé le bac à sable (D87).
- L'ERRATUM n° 4 NOMMÉ AU CHANTIER (la sonde avant l'artefact) : tls13-27
  mesuré 2906 o (après les douze fautes du geste poignée), le slot
  ré-arrêté 0xB80 SANS déplacer tls13-28 — le chevauchement de code
  [0x10A80, 0x10A9A) recouvrait le socle : .refus_pre_taille @0x10A80 et
  .refus_contexte_nul @0x10A92 de la machine d'états VIVAIENT DANS
  tls13-28 (le harnais n'a pas vu : la pose n'écrit que le code, les
  chemins -1/-2 jamais exercés). RÉPARÉ À LA SOURCE : TLS28_VA → 0x10AC0
  (layout), auteur re-joué (notations 27/28 : seules les cibles des 10
  appels + le socle décalé changent, les 26 autres byte-identiques),
  harnais poignée re-joué 52/52 × 3 graines ; LE CONTRÔLE slots-disjoints
  PERMANENT à l'oracle M9. NOTE D8 : padding >= 16 + aligné 16 (LA
  DÉCISION) ; le multiple-de-64 est la convention M8 (tenue par les 26
  autres + le socle, déclinée par l'arrêt consigné 0x120/0xB0).
- LE BUILD EXÉCUTÉ (tls13/build_m9.py + tls13/carte_m9.py) : garde 13/13
  AVANT construire() ; l'héritage re-vérifié (M3 524 + M4 492 + M5 312
  verrous, l'ancre 0.6.0, PUIS la recomposition 0.9.0 CONFRONTÉE OCTET
  PAR OCTET au scellé 1492b0bc… AVANT l'extension) ; le socle sys-04..06
  (oracle 71 verrous, la convention multiple-de-64 tenue) ; les 28 blocs
  (oracle 589 verrous : AUCUN IAT, AUCUN syscall, les appels fermés, les
  RIP == fixtures, LES SLOTS DISJOINTS) ; la composition (.text5 : le
  socle dans la réserve int3 VÉRIFIÉE ; .rdata : K[64] dans la réserve
  VIERGE vérifiée + la version 0x01000001 — LE delta R10 ; .text6
  NOUVELLE 0xC000-0x10FFF : les 28 slots + les 17 fixtures DÉRIVÉS du
  plan) ; le PE 8 sections (648 o <= 0x400), SizeOfImage 0x11000,
  l'entrée 0x8C80 inchangée, AUCUN import nouveau ; la validation
  INTÉGRALE (chaque octet de .text6 compté : slot, fixture ou int3) ; la
  preuve R7 (44 blocs embarqués octet-identiques au scellé 0.9.0, les
  deltas documentés) ; les oracles M4 560 + M5 365 + sys 131 cas verts ;
  L'ARTEFACT : tls13/proxy.exe 1.0.0-dev.1, 65 024 o, sha256
  9ed63f3901d044b32de8bd350ab3209303ea1c63167a4752801712a4bd45d283,
  DÉTERMINISTE (re-construit byte-identique) ; LA CARTE GÉNÉRATION 9 :
  86 blocs sur 8 artefacts (la relève au coffre : lignée D80 + graine
  durable, LE TÉMOIN e9cd8c549485… TENU), les contrats des 31 nouveaux
  PARSÉS des specs I (R2) ; le verrou croisé 86/86 (R8/R9) + le tableau
  de bord.
- FRONTIÈRES : le scellé 0.9.0 INTACT (relu par la confrontation), la
  carte génération 8 INTACTE, les arbres I inchangés (l'erratum touche
  layout + notation : HORS du sceau), aucune balise posée (la finale
  1.0.0 attend le terrain vert du (f) — le scellage sera un fait de
  carte, D104) ; livrables : rapatrier_remise_ceremonie.py,
  sonde_erratum_tls13_27.py, sonde_ancre_090.py, layout.py corrigé,
  notations 27/28, carte_m9.py, build_m9.py, proxy.exe 1.0.0-dev.1,
  carte/ (la génération 9) ; consignations : Entrée 178 PAR SCRIPT, PLAN
  (maj_plan_m9i.py : la rangée (e) + l'État du programme), worklog
  +Task ID 96.
- SUITE : le chantier (f) — LE TERRAIN, LA GRANDE ŒUVRE : le kit au
  coffre /test (l'artefact + le scénario : la session RÉELLE — le VRAI
  ntdll lu par sys-02, les sockets par les syscalls AFD directs,
  l'épinglage de l'empreinte attendue, la ligne applicative chiffrée
  échangée par LE CLIENT TLS 1.3 ENTIER) ; si vert : la finale 1.0.0 (le
  fait de carte) et le jalon M9 franchi.

Stage Summary:
- LE BUILD 1.0.0-dev.1 EST NÉ : tls13/proxy.exe (65 024 o, sha256
  9ed63f39…) sur le corps 0.9.0 INTACT, le socle socket dans la réserve
  .text5, les 28 blocs + les fixtures en .text6 NOUVELLE, la carte
  génération 9 (86 blocs, 8 artefacts), le verrou croisé 86/86 —
  l'artefact DÉTERMINISTE, oracles verts de bout en bout.
- LA CÉRÉMONIE DU BUILD 1.0.0 EST SOLDÉE : la remise du développeur
  rapatriée du /test (md5 contrôlés), déposée par l'atomicité de
  cérémonie, le garde repassé VERT 13/13 — l'état « reelle » tient.
- L'ERRATUM n° 4 EST LA PREUVE DE LA MÉTHODE : la sonde a nommé le
  chevauchement AVANT l'artefact, la réparation est À LA SOURCE (layout +
  re-notation + harnais re-joué), le contrôle slots-disjoints est
  PERMANENT — la faute ne peut plus dormir.
- LA GRANDE ŒUVRE ATTEND : le chantier (f), le terrain — la session
  RÉELLE avec le VRAI afd.sys, la ligne chiffrée de bout en bout ; si
  vert : la finale 1.0.0."""


def main():
    if not JOURNAL.exists():
        sys.exit("ÉCHEC : journal introuvable")
    journal = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 178" in journal:
        sys.exit("ÉCHEC : Entrée 178 déjà consignée (rejeu REFUSÉ)")
    if "## Entrée 177" not in journal:
        sys.exit("ÉCHEC : ancrage Entrée 177 introuvable")
    if MARQUEUR not in journal:
        sys.exit("ÉCHEC : marqueur introuvable")
    i177 = journal.index("## Entrée 177")
    im = journal.index(MARQUEUR)
    if not (i177 < im):
        sys.exit("ÉCHEC : l'ordre 177<marqueur est rompu")
    if "## Entrée 178" in journal[i177:im]:
        sys.exit("ÉCHEC : état inattendu entre 177 et le marqueur")
    # l'insertion APRÈS la SECTION 177 (la leçon du défaut de l'Entrée 175 :
    # TOUJOURS après la section, avant le marqueur)
    journal = journal[:im] + ENTREE + "\n\n" + journal[im:]
    JOURNAL.write_text(journal, encoding="utf-8")

    if not WORKLOG.exists():
        sys.exit("ÉCHEC : worklog introuvable")
    worklog = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 96" in worklog:
        sys.exit("ÉCHEC : Task ID 96 déjà consigné (rejeu REFUSÉ)")
    if "## Task ID 95" not in worklog:
        sys.exit("ÉCHEC : ancrage Task ID 95 introuvable")
    worklog = worklog.rstrip("\n") + "\n\n" + TASK + "\n"
    WORKLOG.write_text(worklog, encoding="utf-8")

    print("[consignation] Entrée 178 déposée au journal (ordre 177<178<marqueur)")
    print("[consignation] Task ID 96 déposé au worklog")
    print("[consignation] la relecture fait foi :")
    j = JOURNAL.read_text(encoding="utf-8")
    w = WORKLOG.read_text(encoding="utf-8")
    assert j.index("## Entrée 177") < j.index("## Entrée 178") < j.index(MARQUEUR)
    assert "## Entrée 178" in j and "erratum n° 4" in j
    assert "9ed63f3901d044b32de8bd350ab3209303ea1c63167a4752801712a4bd45d283" in j
    assert "## Task ID 96" in w and w.index("## Task ID 95") < w.index("## Task ID 96")
    print("[consignation] ORDRE et ANCRAGES constatés — rien d'autre n'a bougé")
    return 0


if __name__ == "__main__":
    sys.exit(main())
