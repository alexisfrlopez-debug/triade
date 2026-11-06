#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_entree185.py — LA CONSIGNATION DU GESTE « LE RUN DE LA SONDE
SYS-05 (g) REÇU : LA MESURE RENDUE (0xC0000005, TROIS fois, déterministe),
LE COUPABLE NOMMÉ À L'INSTRUCTION PRÈS (la pose du WSABUF, spec R1-Q3
« 12 o »), LE VERDICT MANQUANT EXPLIQUÉ (l'erratum n° 8), LA RÉVISION 2
DE LA SPEC + LA RÉPARATION À LA SOURCE » : la rangée (f) du plan reçoit
le constat du run de la sonde, l'État du programme reçoit la phrase du
geste, le worklog reçoit l'Entrée 185. Rejeu REFUSÉ ; tout ancrage absent
ou compté autrement qu'UNE fois = ÉCHEC NOMMÉ, rien n'est écrit."""
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"
WORKLOG = REPO / "docs" / "JOURNAL_TRAVAIL.md"

# --- la rangée (f) : le constat du RUN DE LA SONDE, avant la colonne du
# critère -----------------------------------------------------------------------

ANCIEN_RANGEE = ("la ligne suit DANS LE MÊME RUN]** | run terrain VERT "
                 "sur pièces")

NOUVELLE_RANGEE = (
    "la ligne suit DANS LE MÊME RUN] ; **LE RUN DE LA SONDE REÇU le "
    "07/11 au soir (Entrée 185, Task 103) : LA MESURE RENDUE — LE "
    "NTSTATUS BRUT DU GESTE M9F EST 0xC0000005 (STATUS_ACCESS_VIOLATION), "
    "TROIS fois, DÉTERMINISTE [ni la taille, ni le délai, ni la session — "
    "le compas étalonné : 0xC0000008 sur le handle invalide], la "
    "contre-épreuve S4 : NON-RÉGRESSION [le chemin standard meurt PAREIL "
    ": -6 → -7, état 5] → LE COUPABLE NOMMÉ À L'INSTRUCTION PRÈS : (b) LE "
    "CONTRAT D'APPEL — LA POSE DU WSABUF [spec R1-Q3 « 12 o » : le "
    "pointeur buf posé à +4, le noyau lit le canonique à +8 — une "
    "adresse folle, relu dans l'ARTEFACT SCELLÉ à sys-05+0x46] ; le "
    "verdict manquant EXPLIQUÉ [l'erratum n° 8 : le jmp rel32 du "
    "tromphone T6, ~126 Tio ≫ 2 Gio — struct.error ; le T6 n'avait "
    "JAMAIS couru sur le terrain : les runs m9f retournaient à "
    "_verdict() dès la mort de T3] ; le recoup 31/31 [l'échelle de la "
    "SOURCE re-jouée rend la clé du témoin], le run archivé → "
    "preuves-sonde-sys05-1/ AVEC le verdict ; LA RÉPARATION SELON LA "
    "CHARTE : LA RÉVISION 2 DE LA SPEC SYS-05 [le WSABUF canonique "
    "16 o : len à +0, le padding 4 o NOMMÉ, buf à +8] + l'erratum n° 8 "
    "réparé à la source [l'adressage ABSOLU, les DEUX scénarios] — le "
    "rebuild 1.0.0-dev.3 est LE GESTE SUIVANT, puis le kit m9f réparé, "
    "le run du développeur, LA FINALE 1.0.0]** | run terrain VERT sur "
    "pièces")

# --- l'État du programme : la phrase du geste remplace l'attente ----------------

ANCIEN_ETAT = ("LE GESTE DU DÉVELOPPEUR SUR LA SONDE EST ATTENDU — puis "
               "le recoup, le coupable NOMMÉ [le contrat du bloc, l'état "
               "de l'endpoint, ou le réseau], la réparation selon la "
               "charte [l'erratum de la notation + la révision 2 de la "
               "spec sys-05 le cas échéant — jamais une dérive "
               "silencieuse] — et si la percée tient : le run m9f réparé, "
               "LA FINALE 1.0.0, LE JALON M9 — LA GRANDE ŒUVRE**")

NOUVEL_ETAT = (
    "**LE RUN DE LA SONDE SYS-05 (g) REÇU ET RECROPÉ le 07/11 au soir "
    "(Entrée 185, Task 103) : LA MESURE RENDUE, LE COUPABLE NOMMÉ À "
    "L'INSTRUCTION PRÈS** (le trampoline de capture 33 o décodé == le "
    "squelette spécifié ; le compas étalonné [le handle invalide rend -6 "
    "+ STATUS_INVALID_HANDLE : la capture lit VRAIMENT rdx] ; LA MESURE "
    "— le NTSTATUS brut du geste m9f : 0xC0000005 STATUS_ACCESS_VIOLATION, "
    "classe ERREUR, TROIS fois [la mesure, la variation taille, la "
    "variation délai : DÉTERMINISTE] ; S4 la contre-épreuve : le chemin "
    "standard meurt AU MÊME GESTE [-7, état 5 — la non-régression "
    "CONSTATÉE : le refus est AU BLOC] ; l'échelle de la source re-jouée "
    "rend la clé du témoin — le recoup 31/31 ; LE COUPABLE : (b) LE "
    "CONTRAT D'APPEL — LA POSE DU WSABUF [la spec R1-Q3 décrétait « 12 o "
    "» : len à +0, buf posé à +4 — le WSABUF canonique x64 fait 16 o, "
    "le noyau lit buf à +8 : les 4 octets hauts du vrai pointeur collés "
    "aux immondices de pile → l'adresse FOLLE → ACCESS_VIOLATION — relu "
    "dans l'ARTEFACT SCELLÉ à sys-05+0x46 : 89 74 24 60 48 89 7c 24 64] "
    "— le -6 des CINQ runs EXPLIQUÉ : le noyau n'a jamais refusé "
    "l'émission sur ses mérites, il a fait faute en lisant la structure "
    "que le bloc lui tendait ; LES CANDIDATS ÉLIMINÉS [(c) l'endpoint : "
    "INVALID_DEVICE_STATE aurait été nommé, l'endpoint était frais deux "
    "fois ; (d) le réseau : CONNECTION_* aurait été nommé, le refus est "
    "déterministe ; PENDING : le status n'est pas 0x103] ; LE VERDICT "
    "MANQUANT EXPLIQUÉ [l'erratum n° 8 : le jmp rel32 du tromphone NtClose "
    "du T6 ne peut pas coder ~126 Tio — struct.error, le run meurt dans "
    "T6 avant _verdict() ; le témoin a SURVÉCU au crash par son vidage "
    "volontaire d'après-S3 : le dessein a tenu ; la faute était invisible "
    "depuis toujours : les QUATRE runs m9f retournaient à _verdict() dès "
    "la mort de T3] ; LA RÉPARATION SELON LA CHARTE, JAMAIS UNE DÉRIVE "
    "SILENCIEUSE : LA RÉVISION 2 DE LA SPEC SYS-05 [Q3 : le WSABUF "
    "canonique 16 o, le padding d'alignement NOMMÉ ; I2 : 40 o] + la "
    "notation corrigée [mov qword ptr [rsp+0x68], rdi — le MÊME encode, "
    "le slot ne bouge pas] + l'erratum n° 8 réparé à la source [l'adressage "
    "ABSOLU mov rax,SSN ; mov rdx,sys-01 ; jmp rdx — le MÊME patron que "
    "le trampoline de capture : lui, a traversé] dans les DEUX scénarios "
    "[m9f + sonde] ; le run archivé → preuves-sonde-sys05-1/ AVEC le "
    "verdict ; la révision 2 fait évoluer v06/I/ — LE SIGNAL « signature "
    "requise » attendu, la cérémonie du build 1.0.0 l'absorbe [avec la "
    "révision M9-(d) et l'erratum tls13 n° 2 déjà en attente]) — LE GESTE "
    "SUIVANT : LE REBUILD 1.0.0-dev.3 [le bloc sys-05 réparé, les portes "
    "de l'assemblage re-passées], LE KIT M9F RÉPARÉ livré au /test — puis "
    "le run du développeur, ET SI LE VERT TIENT : LA FINALE 1.0.0, LE "
    "JALON M9 — LA GRANDE ŒUVRE**")

# --- le worklog : l'Entrée 185, AVANT la ligne m5a -------------------------------

ENTREE_185 = """## Entrée 185 — LE RUN DE LA SONDE SYS-05 (g) REÇU (« les preuves sont déposées dans le drive /test ») : LA MESURE RENDUE — LE NTSTATUS BRUT DU GESTE M9F EST 0xC0000005 (STATUS_ACCESS_VIOLATION), TROIS FOIS, DÉTERMINISTE ; LE COUPABLE NOMMÉ À L'INSTRUCTION PRÈS : (b) LE CONTRAT D'APPEL — LA POSE DU WSABUF (SPEC R1-Q3 « 12 o », LE NOYAU LIT buf À +8) ; LE VERDICT MANQUANT EXPLIQUÉ (L'ERRATUM n° 8 : LE JMP REL32 DU TROMPHONE T6) ; LA RÉVISION 2 DE LA SPEC + LA RÉPARATION À LA SOURCE (07/11 au soir)

**Le geste du développeur reçu — et la sonde a répondu à la question des cinq runs.** LE RAPATRIEMENT (scripts/ramasse_sonde1.py) : les QUATRE pièces au réceptacle /test/preuves-sonde-sys05/ (temoin-sonde-sys05.txt 3 562 o dbfce3f7…, sonde-sys05-journal.log 1 054 o a860c870…, journal-emissions.txt 119 o 42b60aa7…, LISEZMOI-preuves.txt ec84082c…), md5 aller-retour OK, les DEUX kits de la racine recoupés INTACTS (kit-sonde-sys05.zip 215c2caa… + kit-m9f.zip 90a1d022… — les acquittés), l'artefact re-haché au geste même : d8928934… INTACT, JAMAIS reconstruit ; le scénario exécuté == la source du dépôt, octet pour octet (cbc599ea…).

**LA MESURE — le cœur.** LA MÊME MACHINE QUE LE RUN 4 (Windows 10.0 build 26300, Python 3.14.3 AMD64, ntdll b072efae…). T0/T1/T2 VERT (les slot, les fixtures, l'octet 0x72 de l'erratum n° 5, SSN 85/7/15, l'endpoint AFD établi par sys-04, handle 0x210). LE TRAMPOLINE DE CAPTURE posé : 33 o consignés au témoin et DÉCODÉS AU RECOUP instruction par instruction — sub rsp,0x28 ; mov rax,0x7ff68fbba540 (== base+0xa540 : LE SLOT SYS-05) ; call rax ; shl rdx,32 ; mov ecx,eax ; or rcx,rdx ; mov rax,rcx ; add rsp,0x28 ; ret — LE SQUELETTE SPÉCIFIÉ. LE COMPAS ÉTALONNÉ : le handle invalide rend -6 + STATUS_INVALID_HANDLE (0xC0000008) — LA CAPTURE LIT VRAIMENT RDX. LA MESURE : LE CH DE RÉFÉRENCE (119 o) émis par le trampoline sur l'endpoint frais → **code -6, NTSTATUS 0xC0000005 — STATUS_ACCESS_VIOLATION, CLASSE ERREUR (sévérité 11), UN VRAI REFUS DU NOYAU** ; la variation TAILLE (un octet, session sacrifiée fraîche — sys-04 VERT, handle 0x310) : -6, 0xC0000005 ; la variation DÉLAI (le CH re-tenté après 2 s — l'horloge du journal porte le délai : 20:34:30 → 20:34:32) : -6, 0xC0000005 — DÉTERMINISTE. S4 LA CONTRE-ÉPREUVE : la poignée par LE RAPPEL STANDARD (le chemin du kit m9f, SANS trampoline, session NEUVE) meurt AU MÊME GESTE : le rappel émission rend -6, la machine propage -7, état 5 — LA MÊME MORT QUE LES QUATRE RUNS M9F : NON-RÉGRESSION CONSTATÉE, le refus est AU BLOC ; journal-emissions.txt : UN enregistrement, 119 o (16 03 03 00 72 + 114) — le CH refusé, jamais un demi-envoi déguisé.

**LE COUPABLE — nommé sur pièces, à l'instruction près.** Le WSABUF canonique x64 fait SEIZE octets : len (4 o) à +0, QUATRE OCTETS DE PADDING D'ALIGNEMENT, buf (8 o) à +8. LA SPEC sys-05:R1 Q3 AVAIT DÉCRÉTÉ « (12 o + 24 o…) » — UN WSABUF « PACKÉ ». La notation a implémenté la spec À LA LETTRE : mov dword [rsp+0x60],esi (len à +0) ; mov qword [rsp+0x64],rdi (buf à +4) — RELU DANS L'ARTEFACT SCELLÉ à sys-05+0x46 (89 74 24 60 48 89 7c 24 64). LE NOYAU, LUI, LIT LE CANONIQUE : buf à +8 — les 4 octets HAUTS du vrai pointeur collés aux 4 octets d'immondices de pile (jamais posés à rsp+0x6C) : UNE ADRESSE FOLLE → le noyau fait faute en la sondant → STATUS_ACCESS_VIOLATION. Le bloc copie le status brut dans rdx (mov rdx,rax ; mov rax,-6 — la spec Q5 l'avait NOMMÉ) : c'est LUI que le trampoline est venu lire. LE -6 DES CINQ RUNS EST EXPLIQUÉ : le noyau n'a jamais refusé l'émission sur ses mérites — il a fait faute en lisant la structure que le bloc lui tendait. LES CANDIDATS ÉLIMINÉS : (a) dès le run 4 ; (c) l'endpoint (INVALID_DEVICE_STATE aurait été nommé ; l'endpoint était frais deux fois) ; (d) le réseau (CONNECTION_* aurait été nommé ; déterministe) ; LE PENDING (le status n'est pas 0x103) ; LE TRAMPOLINE (S4 : le chemin standard meurt pareil). L'ÉCHELLE RE-JOUÉE : l'échelle de LA SOURCE (éprouvée au labo contre le vecteur officiel RFC 7748 § 6.1 Alice) sur la clé privée DU RUN (745d81a0…) rend la clé publique du témoin (d525a1c6…) — la preuve cryptographique du run est COHÉRENTE. LE RECOUP : 31/31 (scripts/recouper_sonde1.py).

**LE VERDICT MANQUANT — la mort en T6 expliquée, l'erratum n° 8.** Le journal s'arrête à la mort de S4, journal-emissions.txt est né, mais NI le VERDICT NI la ligne reçue : le run est mort DANS T6, AVANT _verdict(). LE SITE : le tromphone NtClose pose un jmp rel32 (struct.pack « <i ») de la zone VirtualAlloc vers l'artefact — la distance 0x7ff68fbb0000 − 0x1bec7ec0000 ≈ 126 Tio ≫ 2 Gio (la zone de capture DU RUN, consignée au témoin, PROUVE la région d'allocation) : struct.error, l'exception Python, le verdict jamais né. La faute était INVISIBLE depuis toujours : les QUATRE runs m9f retournaient à _verdict() dès la mort de T3 — LEUR T6 N'A JAMAIS COURU SUR LE TERRAIN. Le dessein de la sonde A TENU : le témoin écrit au fur et à mesure (« la mesure est le cœur : ses pièces survivent à tout arrêt ultérieur ») — LA MESURE A SURVÉCU À LA MORT DU RUN.

**La réparation selon la charte — jamais une dérive silencieuse.** (1) L'ERRATUM n° 8 (la série ouverte au n° 5) : le tromphone NtClose du T6 (la sonde ET le kit m9f — le même geste) passe du jmp rel32 à L'ADRESSAGE ABSOLU (mov rax,SSN ; mov rdx,sys-01 ; jmp rdx — le MÊME patron que le trampoline de capture : lui, a traversé) — réparé à la source dans les DEUX scénarios, plus AUCUN rel32 ; (2) LA RÉVISION 2 DE LA SPEC SYS-05 (m8/I/sys-05-emission.md) : Q3 réécrit — le WSABUF fait SEIZE octets (len à +0, le padding d'alignement 4 o NOMMÉ, buf à +8 : JAMAIS un « packé » de 12 o), I2 suit (40 o, non 36), la note de révision consigne la mesure ; (3) LA NOTATION corrigée (m8/notation/sys-05-emission.asm + le brouillon) : mov qword ptr [rsp+0x68], rdi — le MÊME encode (48 89 7c 24 68, 5 o), le slot ne bouge pas d'un octet, la carte demeure ; (4) LA RE-CÉRÉMONIE : la révision 2 fait évoluer v06/I/ — LE SIGNAL « signature requise » attendu, la cérémonie du build 1.0.0 l'absorbe (les arbres à signer EN GESTE, avec la révision M9-(d) et l'erratum tls13 n° 2 déjà en attente).

**Détail.** LE RUN ARCHIVÉ (scripts/archiver_sonde1.py) : preuves-sonde-sys05-1/ créé dans archives-preuves/ (D99), les TROIS pièces DU RUN DÉPLACÉES (D143 : un déplacement, jamais un jet — le LISEZMOI du réceptacle DEMEURE), le VERDICT-recoup-labo-sonde-sys05-1.txt déposé AVEC les pièces (l'archive porte le jugement : 31/31), preuves-sonde-sys05/ ré-armé, les DEUX INDEX mis à jour. FRONTIÈRES : les DEUX kits du /test INCHANGÉS (215c2caa… + 90a1d022…), l'artefact INTACT (d8928934… — le rebuild est LE GESTE SUIVANT, pas une reconstruction tacite), le scellé 0.9.0 INTACT, AUCUNE balise posée (la finale 1.0.0 attend le VERT — D104), la clé privée jamais traversée (D87). Livrables : download/preuves-sonde-sys05-1/ (les pièces + le verdict du recoup). Consignations : la présente Entrée 185 PAR SCRIPT, PLAN (maj_plan_m9r.py : la rangée (f) + l'État du programme), worklog +Task ID 103. SUITE : LE REBUILD 1.0.0-dev.3 (le bloc sys-05 réparé, les portes de l'assemblage re-passées) — puis LE KIT M9F RÉPARÉ livré au /test, le run du développeur, ET SI LE VERT TIENT : LA FINALE 1.0.0, le jalon M9 franchi — LA GRANDE ŒUVRE.

"""

def main():
    plan = PLAN.read_text(encoding="utf-8")
    if "LE RUN DE LA SONDE REÇU le 07/11" in plan:
        sys.exit("ÉCHEC : la rangée (f) est déjà à jour (rejeu REFUSÉ)")
    if plan.count(ANCIEN_RANGEE) != 1:
        sys.exit(f"ÉCHEC : ancrage rangée (f) trouvé "
                 f"{plan.count(ANCIEN_RANGEE)} fois (attendu : 1)")
    if plan.count(ANCIEN_ETAT) != 1:
        sys.exit(f"ÉCHEC : ancrage État trouvé "
                 f"{plan.count(ANCIEN_ETAT)} fois (attendu : 1)")
    plan = plan.replace(ANCIEN_RANGEE, NOUVELLE_RANGEE, 1)
    plan = plan.replace(ANCIEN_ETAT, NOUVEL_ETAT, 1)
    if "LE RUN DE LA SONDE REÇU le 07/11 au soir (Entrée 185" not in plan:
        sys.exit("ÉCHEC : la rangée (f) ne porte pas le constat du run "
                 "de la sonde après remplacement")
    if "LE COUPABLE NOMMÉ À L'INSTRUCTION PRÈS" not in plan:
        sys.exit("ÉCHEC : l'État ne porte pas la phrase du geste")
    PLAN.write_text(plan, encoding="utf-8")
    print("PLAN : la rangée (f) + l'État du programme — consignés")

    worklog = WORKLOG.read_text(encoding="utf-8")
    if "Entrée 185 —" in worklog:
        sys.exit("ÉCHEC : l'Entrée 185 existe déjà (rejeu REFUSÉ)")
    marqueur = "<!-- m5a:journal-des-builds v1"
    if worklog.count(marqueur) != 1:
        sys.exit(f"ÉCHEC : le marqueur m5a trouvé "
                 f"{worklog.count(marqueur)} fois (attendu : 1)")
    worklog = worklog.replace(marqueur, ENTREE_185 + marqueur, 1)
    if "Entrée 185 — LE RUN DE LA SONDE SYS-05 (g) REÇU" not in worklog:
        sys.exit("ÉCHEC : l'Entrée 185 absente après remplacement")
    WORKLOG.write_text(worklog, encoding="utf-8")
    print("WORKLOG : l'Entrée 185 consignée AVANT le marqueur m5a")


if __name__ == "__main__":
    main()
