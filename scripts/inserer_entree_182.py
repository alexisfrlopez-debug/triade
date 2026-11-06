#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_182.py — LA CONSIGNATION DU GESTE « LA CONSOLE DU
DÉVELOPPEUR REÇUE (le paste du 07/11) : LE CRASH DU SECOND RUN NOMMÉ —
L'ERRATUM n° 7 DU KIT, TROIS FAUTES DANS LE SEGMENT PYTHON PUR, L'ACQUITTEMENT
« PAR ÉLIMINATION » DE L'ENTRÉE 181 RENVERSÉ PAR LA PIÈCE ; LE KIT RÉPARÉ À
LA SOURCE + LE CONTRÔLE PERMANENT, MIS À JOUR EN PLACE AU COFFRE — LE
TROISIÈME GESTE ATTENDU » : JOURNAL_TRAVAIL +Entrée 182 (ordre
181<182<marqueur, rejeu REFUSÉ), worklog +Task ID 100. Tout ancrage absent =
ÉCHEC NOMMÉ, rien n'est écrit.

La datation : la présente porte le 07/11 (la pièce console reçue le 07/11 —
le run mort était celui du 06/11 16:56, déjà consigné à l'Entrée 181 : la
console en est la PARTIE MANQUANTE, les temoin() ne vivent que sur la
console, jamais dans le journal)."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 182 — LA CONSOLE DU DÉVELOPPEUR REÇUE (le paste du 07/11) : LE CRASH DU SECOND RUN NOMMÉ — L'ERRATUM n° 7 DU KIT (TROIS FAUTES DANS LE SEGMENT PYTHON PUR), L'ACQUITTEMENT « PAR ÉLIMINATION » DE L'ENTRÉE 181 RENVERSÉ PAR LA PIÈCE ; LE KIT RÉPARÉ À LA SOURCE + LE CONTRÔLE PERMANENT AUX TROIS PORTES, MIS À JOUR EN PLACE AU COFFRE — LE TROISIÈME GESTE ATTENDU (07/11)

**La pièce qui manquait — la console répond, et elle condamne le kit.** LA PIÈCE : le paste intégral de la console du développeur (déposée au coffre avec le verdict : console-run-m9f.txt, md5 d6d1e931…) — le run du 06/11 16:56 REVU DEBOUT : les SEIZE T0 [ok] (l'empreinte d8928934… ASSERTÉE avant tout geste, l'octet de l'erratum n° 5 relu dans l'image, le VRAI ntdll haché 36b1a62e…), T1 aux SSN 85/7/15 (motif 4c8bd1b8 d'un stub sain — les DEUX lecteurs d'accord), T2 rax 0 handle 0x304 (LE VRAI afd.sys franchi), PUIS T3 : l'aléa du kit (a9ff3133…), la clé privée (82a24d22…), la « clé publique attendue » **000…0 — 64 ZÉROS** (LE SYMPTÔME), et le crash : **TypeError: 'bytes' object does not support item assignment, scenario-m9f.py ligne 593, `kit96.raw[:32] = alea`** — le traceback porte les lignes 832/593 == LA POINTE 35706ef OCTET POUR OCTET (relu au geste même depuis l'histoire git : le développeur a exécuté LE scénario du labo, sans modification), le prompt EST REVENU (le processus a rendu la main : ni console gelée, ni mort inexpliquée — les candidats (a)/(b) de l'Entrée 181 sont ÉLIMINÉS par la pièce, l'incident n'est PAS local, il est AU LABO).

**L'erratum n° 7 — TROIS fautes au kit, dans le MÊME segment Python pur (aucune machine en vol, cohérent avec l'horloge : la mort DANS la seconde de T2).** (1) LA POSE DU KIT PAR TRANCHES SUR `.raw` : create_string_buffer(…).raw est une COPIE bytes IMMUABLE — `kit96.raw[:32] = alea` est un TypeError DÉTERMINISTE sur TOUTE machine (LE crash du run, ligne 593) ; (2) L'ÉCHELLE RFC 7748 DU RECOUP : x_3 né à 0 (le point à l'infini tient le résultat — la « clé attendue » imprimée NULLE, le symptôme lisible AVANT le crash) ET a24 = (p+1)//4 au lieu de 121665 (la fausse courbe : a24 = (486662-2)/4, RFC 7748 § 5) — le recoup T3 aurait été IMPOSSIBLE même sans le crash ; (3) LE POINTEUR : les DEUX sites OUVRIR passaient la TAILLE (KIT96 = 96) en r9 là où tls13-27 P2 É1 exige LE POINTEUR des 96 o (aléa + clé privée + empreinte) — la machine aurait lu à l'adresse 0x60, la mort au premier geste : la faute (3) devancée de QUATRE lignes par la faute (1). LE POST-MORTEM REJOUÉ AU LABO (scripts/eprouver_fix_m9f.py, 15/15 VERT) : le TypeError EXACT reproduit (A1) ; la clé privée DU RUN — celle de la console — par l'échelle PRÉ-réparation (la pointe 35706ef extraite et rejouée) rend 000…0 (A2 : le symptôme EXPLIQUÉ sur pièces ; la VRAIE clé attendue eût été 1227429d…) ; les DEUX sites à la taille constatés PAR AST (A3).

**La réparation À LA SOURCE + LE CONTRÔLE PERMANENT — la faute ne peut plus dormir.** LA SOURCE (tls13/terrain/scenario-m9f.py) : les 96 o posés EN UN GESTE par create_string_buffer(bytes, TAILLE) aux DEUX sites (T3 session, T5 falsification) ; r9 = ctypes.addressof(kit96|kit96_2) aux DEUX appels OUVRIR ; l'échelle == le pseudocode officiel RFC 7748 § 5 == LA RÉFÉRENCE DU DÉPÔT (harnais_x25519.ref_x25519) — x_3 = u au point de base, a24 = 121665. LE CONTRÔLE PERMANENT (assembler_kit_m9f.py [2c], TROIS portes) : porte 1 — AUCUNE écriture `.raw[...]` (le TypeError ne peut plus dormir) ; porte 2 — les DEUX sites OUVRIR portent LE POINTEUR en r9 ; porte 3 — l'échelle re-jouée à l'assemblage CONTRE LES VECTEURS OFFICIELS du dépôt (RFC 7748 § 6.1 Alice 8520f009…/Bob de9edb7d…, le couple RFC 8448 § 3 99381de5…, 16 clés semées contre ref_x25519). LA PREUVE NÉGATIVE (scripts/preuve_negative_e7.py, 6/6) : les TROIS portes refusent la source PRÉ-réparation par leurs refus NOMMÉS (la porte 1 NOMME la ligne 593) et passent la source réparée — une garde qui n'a jamais refusé le coupable n'est pas une garde. LE KIT CORRIGÉ réassemblé et rééprouvé (26 constantes PAR AST == l'artefact/le plan/la sonde, les portes [2b]/[2c], py_compile, extraction vierge : kit-m9f.zip 37 134 o, md5 90a1d022…, sha256 3666b1d7…).

**Le coffre /test mis à jour en place (scripts/corriger_kit_m9f_e7.py — modèle corriger_kit_m9f.py, D143 : par DÉPLACEMENT, jamais un jet).** [1] le zip local corrigé vérifié (md5 90a1d022… MATCH) ; [2] kit-m9f.zip MIS À JOUR EN PLACE (7d5380ce… → 90a1d022…, le contenu remplacé, le fichier même conservé — l'ancien scénario vit dans l'histoire git à la pointe 35706ef) ; [3] LISEZMOI-m9f.txt MIS À JOUR (md5 d5e7a4f5… — l'erratum n° 7 consigné au document du kit, le TROISIÈME geste annoncé) ; [4] LE SECOND RUN ARCHIVÉ : preuves-run-m9f-2/ créé dans archives-preuves/ (D99 : jamais mélanger les runs), le journal DU RUN (md5 24680ac9…) DÉPLACÉ depuis le réceptacle, LA PIÈCE CONSOLE déposée AVEC lui (celle qui renverse l'acquittement) ET le VERDICT-recoup-labo-m9f-2.txt (le jugement AVEC les pièces : CRASH NOMMÉ COHÉRENT 12/12 sur pièces croisées, D138/D145/D148) ; [5] preuves-m9f/ ré-armé (il ne porte que son LISEZMOI-preuves.txt — le réceptacle du TROISIÈME geste) ; [6] LES DEUX INDEX mis à jour (archives-preuves : la section preuves-run-m9f-2 ; archives-livraisons : la note de correction du 07/11) ; [7] la racine vérifiée (13 entrées, le kit corrigé recoupé par relecture).

**Détail.** FRONTIÈRES : l'ARTEFACT N'A PAS BOUGÉ d'un octet (proxy.exe demeure le build 1.0.0-dev.2, sha256 d892893469608fd6…, 65 024 o — relu VERT au T0 du run mort LUI-MÊME : le kit fautif n'a jamais terni l'artefact), le terrain demeure LAVÉ (T0/T1/T2 VERT sur la machine réelle — l'erratum n° 6 prouvé réparé, LE VRAI afd.sys franchi pour la première fois : ces acquis de l'Entrée 181 demeurent), le scellé 0.9.0 INTACT, les arbres I inchangés, AUCUNE balise posée (le second run est INCONCLU-ARCHIVÉ : la finale 1.0.0 attend le TROISIÈME run complet vert — D104), la clé privée jamais traversée (D87), l'archive du premier run INTACTE (preuves-run-m9f/ à part — D99). Livrables : download/kit-m9f.zip (le kit corrigé, md5 90a1d022…) + download/vague-m9f/m9-kit/ (les trois pièces ré-assemblées) + download/preuves-run-m9f-2/ (console-run-m9f.txt md5 d6d1e931… + VERDICT-recoup-labo-m9f-2.txt md5 cb67b375…). Consignations : la présente Entrée 182 PAR SCRIPT, PLAN (maj_plan_m9n.py : la rangée (f) + l'État du programme), worklog +Task ID 100. SUITE : LE TROISIÈME GESTE DU DÉVELOPPEUR — dézipper kit-m9f.zip (le corrigé) dans un dossier NEUF (D99), `python scenario-m9f.py` (~10 s, réseau vivant), renvoyer preuves-m9f/ ENTIER au coffre → le recoup (D138/D145/D148) → si vert : LA FINALE 1.0.0 (fait de carte — D104) : le jalon M9 franchi — LA GRANDE ŒUVRE."""

TASK = """## Task ID 100 — LA CONSOLE DU DÉVELOPPEUR REÇUE (le paste du 07/11) : LE CRASH DU SECOND RUN NOMMÉ — L'ERRATUM n° 7 DU KIT (TROIS FAUTES DANS LE SEGMENT PYTHON PUR : la pose du kit par tranches sur `.raw`, l'échelle du recoup rendant la clé attendue NULLE, la TAILLE au lieu du POINTEUR aux sites OUVRIR), l'acquittement « par élimination » de l'Entrée 181 RENVERSÉ PAR LA PIÈCE ; LE KIT RÉPARÉ À LA SOURCE + LE CONTRÔLE PERMANENT AUX TROIS PORTES, MIS À JOUR EN PLACE AU COFFRE — LE TROISIÈME GESTE ATTENDU (07/11)

Work Log:
- LA PIÈCE : la console intégrale du développeur (console-run-m9f.txt,
  md5 d6d1e931…) — les SEIZE T0 [ok], T1 SSN 85/7/15, T2 rax 0
  handle 0x304, T3 imprimant l'aléa/la clé privée DU RUN puis la « clé
  publique attendue » 000…0 (LE SYMPTÔME), le TypeError ligne 593
  (`kit96.raw[:32] = alea`), le prompt REVENU ; les lignes 832/593 ==
  la pointe 35706ef OCTET POUR OCTET : le scénario du labo exécuté
  fidèlement ; les candidats console gelée / mort inexpliquée de
  l'Entrée 181 ÉLIMINÉS — la faute est AU LABO.
- L'ERRATUM n° 7, TROIS FAUTES AU KIT (le même segment Python pur,
  aucune machine en vol) : (1) `.raw` est une copie bytes IMMUABLE —
  la pose du kit par tranches est un TypeError DÉTERMINISTE sur toute
  machine ; (2) l'échelle RFC 7748 : x_3 né à 0 (le point à l'infini
  — la « clé attendue » NULLE imprimée) ET a24 = (p+1)//4 au lieu de
  121665 (la fausse courbe) — le recoup T3 eût été IMPOSSIBLE ; (3)
  les DEUX sites OUVRIR passaient la TAILLE (96) en r9 où tls13-27
  P2 É1 exige LE POINTEUR des 96 o — la machine eût lu à l'adresse
  0x60 (devancée de quatre lignes par la faute (1)).
- LE POST-MORTEM REJOUÉ AU LABO (eprouver_fix_m9f.py, 15/15 VERT) :
  le TypeError EXACT reproduit ; la clé privée DU RUN par l'échelle
  pré-réparation (pointe 35706ef extraite et rejouée) rend 000…0 —
  le symptôme EXPLIQUÉ sur pièces (la vraie clé attendue eût été
  1227429d…) ; la construction CH == la référence du harnais octet
  pour octet (114 o, l'aléa @ +6, la clé @ +82) ; les 96 o posés en
  un geste, exactement TAILLE octets.
- LA RÉPARATION À LA SOURCE : create_string_buffer EN UN GESTE aux
  DEUX sites, r9 = ctypes.addressof(kit96|kit96_2), l'échelle == le
  pseudocode officiel RFC 7748 § 5 == la référence du dépôt ;
  LE CONTRÔLE PERMANENT (assembler_kit_m9f.py [2c], TROIS portes :
  aucune écriture `.raw[...]`, LE POINTEUR aux OUVRIR, l'échelle
  contre les vecteurs officiels) ; LA PREUVE NÉGATIVE
  (preuve_negative_e7.py, 6/6) : les TROIS portes refusent la source
  pré-réparation (la porte 1 NOMME la ligne 593) et passent la source
  réparée.
- LE KIT CORRIGÉ réassemblé et rééprouvé (26 constantes PAR AST,
  portes [2b]/[2c], py_compile, extraction vierge — kit-m9f.zip
  37 134 o, md5 90a1d022…, sha256 3666b1d7…) ; LE COFFRE MIS À JOUR
  EN PLACE (corriger_kit_m9f_e7.py) : kit-m9f.zip 7d5380ce… →
  90a1d022…, LISEZMOI-m9f.txt à l'erratum (d5e7a4f5…), le run 2
  archivé → archives-preuves/preuves-run-m9f-2/ (le journal DU RUN
  DÉPLACÉ + la pièce console + le VERDICT-recoup-labo-m9f-2.txt
  12/12), preuves-m9f/ ré-armé, les DEUX index à jour, la racine
  vérifiée (13 entrées).
- FRONTIÈRES : l'artefact INTACT (d8928934… relu VERT au T0 du run
  mort lui-même), le terrain LAVÉ (les acquis de l'Entrée 181
  demeurent : l'erratum n° 6 prouvé réparé, LE VRAI afd.sys franchi),
  le scellé 0.9.0 INTACT, AUCUNE balise (la finale attend le
  TROISIÈME run complet vert), l'archive du premier run intacte ;
  livrables : download/kit-m9f.zip (md5 90a1d022…) +
  download/preuves-run-m9f-2/ (la console + le verdict) ;
  consignations : Entrée 182 PAR SCRIPT, PLAN (maj_plan_m9n.py :
  rangée (f) + État), worklog +Task ID 100.
- SUITE : LE TROISIÈME GESTE DU DÉVELOPPEUR — dézipper kit-m9f.zip
  dans un dossier NEUF (D99), python scenario-m9f.py, renvoyer
  preuves-m9f/ ENTIER au coffre → le recoup → si vert : LA FINALE
  1.0.0, le jalon M9 franchi — LA GRANDE ŒUVRE.

Stage Summary:
- LA PIÈCE CONSOLE RENVERSE L'ACQUITTEMENT : le second run n'était
  ni gelé ni inexpliqué — il est mort d'un crash PYTHON NOMMÉ DANS
  LE KIT (TypeError ligne 593), après l'impression d'une « clé
  attendue » NULLE, symptôme de la seconde faute ; TROIS fautes au
  kit, aucune au terrain ni à l'artefact.
- LA RÉPARATION EST À LA SOURCE ET GARANTIE : les TROIS portes du
  contrôle permanent à l'assemblage (preuve négative 6/6) ; le kit
  corrigé (md5 90a1d022…) est EN PLACE au coffre, le run 2 archivé
  avec sa pièce console et le verdict du recoup (12/12).
- LE TROISIÈME GESTE EST ATTENDU : dézipper le kit corrigé dans un
  dossier NEUF, python scenario-m9f.py, renvoyer preuves-m9f/
  ENTIER — et si le run est vert : LA FINALE 1.0.0, le jalon M9
  franchi — LA GRANDE ŒUVRE."""


def main():
    if not JOURNAL.exists():
        sys.exit("ÉCHEC : journal introuvable")
    journal = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 182" in journal:
        sys.exit("ÉCHEC : Entrée 182 déjà consignée (rejeu REFUSÉ)")
    if "## Entrée 181" not in journal:
        sys.exit("ÉCHEC : ancrage Entrée 181 introuvable")
    if MARQUEUR not in journal:
        sys.exit("ÉCHEC : marqueur introuvable")
    i181 = journal.index("## Entrée 181")
    im = journal.index(MARQUEUR)
    if not (i181 < im):
        sys.exit("ÉCHEC : l'ordre 181<marqueur est rompu")
    if "## Entrée 182" in journal[i181:im]:
        sys.exit("ÉCHEC : état inattendu entre 181 et le marqueur")
    # l'insertion APRÈS la SECTION 181 (la leçon de l'Entrée 175 :
    # TOUJOURS après la section, avant le marqueur)
    journal = journal[:im] + ENTREE + "\n\n" + journal[im:]
    JOURNAL.write_text(journal, encoding="utf-8")

    if not WORKLOG.exists():
        sys.exit("ÉCHEC : worklog introuvable")
    worklog = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 100" in worklog:
        sys.exit("ÉCHEC : Task ID 100 déjà consigné (rejeu REFUSÉ)")
    if "## Task ID 99" not in worklog:
        sys.exit("ÉCHEC : ancrage Task ID 99 introuvable")
    worklog = worklog.rstrip("\n") + "\n\n" + TASK + "\n"
    WORKLOG.write_text(worklog, encoding="utf-8")

    print("[consignation] Entrée 182 déposée au journal "
          "(ordre 181<182<marqueur)")
    print("[consignation] Task ID 100 déposé au worklog")
    print("[consignation] la relecture fait foi :")
    j = JOURNAL.read_text(encoding="utf-8")
    w = WORKLOG.read_text(encoding="utf-8")
    assert j.index("## Entrée 181") < j.index("## Entrée 182") < j.index(MARQUEUR)
    assert "## Entrée 182" in j and "90a1d022" in j and "d6d1e931" in j
    assert "kit96.raw[:32] = alea" in j and "121665" in j
    assert "RENVERSÉ" in j and "TROISIÈME GESTE" in j
    assert "## Task ID 100" in w and w.index("## Task ID 99") < w.index("## Task ID 100")
    assert "ERRATUM n° 7" in w and "12/12" in w
    print("[consignation] ORDRE et ANCRAGES constatés — rien d'autre n'a bougé")
    return 0


if __name__ == "__main__":
    sys.exit(main())
