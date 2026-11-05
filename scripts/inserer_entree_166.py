#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_166.py — LA CONSIGNATION DU GESTE « M9-(a) COMPLET » :
JOURNAL_TRAVAIL +Entrée 166 (ordre 165<166<marqueur, rejeu REFUSÉ),
DECISIONS +D167, PLAN (le chantier M9-(a) RÉALISÉ + l'État du programme),
worklog +Task ID 84. Tout ancrage absent = ÉCHEC NOMMÉ, rien n'est écrit."""

import pathlib

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"
DECISIONS = REPO / "docs" / "DECISIONS.md"
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 166 — LE CHANTIER M9-(a) COMPLET : LES 28 SPÉCIFICATIONS POSÉES — les 24 du geste en SIX familles (hkdf, x25519, aead, enregistrement, poignée, principal), R2 tenue de bout en bout, AUCUN octet de notation ; le plan d'adressage étendu aux SIX familles (les constantes RE-DÉRIVÉES par arithmétique, l'erratum av-10 consigné AVANT la notation) ; l'instrument verifier_specs_m9a.py 117 VERTS après trois défauts nommés par le fail-closed (05/11 au soir)

**La reprise (D164 rejouée).** Les trois miroirs confrontés : le dépôt local == GitHub == 45c8970 (la pointe consignée du Task 83 — fetch, zéro avance/zéro retard, l'arbre propre), le bundle miroir 090-ab48be1 AU GESTE + sa consignation (le schéma normal de fin de session) ; les canaux OAuth Drive + GitHub 200 (check_auth.py). UN DÉFAUT D'INSTRUMENT NOMMÉ AU GESTE MÊME : le recyclage du disque labo avait posé le bit exécutable sur 179 fichiers suivis (mode 100644 → 100755, ZÉRO octet de contenu — le diff vide de contenu l'a prouvé sur pièces) : RÉPARÉ par git restore AVANT tout travail, l'arbre propre re-constaté.

**Les 24 spécifications (écrit-avant-code, R2).** La famille `hkdf` (tls13-05..08) : HMAC-SHA-256 (RFC 2104, les vecteurs RFC 4231 — l'expulsion de clé exercée dans les deux sens), HKDF-Extract (le sel vide PORTÉ par la spec : les 32 zéros du RFC 5869), HKDF-Expand (la boucle bornée par l'octet compteur, L ≤ 8160), HKDF-Expand-Label (la structure HkdfLabel du RFC 8446 § 7.1 — LE bloc du calendrier, les libellés en données publiques du plan). La famille `x25519` (tls13-09..14) : les miroirs win des contrats av-05..11 — addition/soustraction/multiplication (l'école 5×5 aux dix accumulateurs u128, les bornes CITÉES), la passe FUSIONNÉE propagation+gel (tls13-12 : une frontière d'appel au lieu des deux du M7), l'échelle de Montgomery (RFC 7748 § 5 : le clamp PAR le bloc, le cswap MASQUÉ, a24 = 121665, l'inversion finale à l'exposant public p − 2), la clé publique au point 9. La famille `aead` (tls13-15..19) : le déploiement des clés de tour et le bloc par L'ARRÊT AES-NI NOMMÉ (AESKEYGENASSIST/AESENC/AESENCLAST — le S-box matériel temps constant, JAMAIS la table logicielle indexée par la clé : charte § 3), GHASH la multiplication GF(2^128) SANS TABLE PAR DONNÉE (la marche de la § 6.3 mot pour mot, le bit en masque sar — PCLMULQDQ chantier futur nommé), GCM sceller/ouvrir (le tag VÉRIFIÉ AVANT restitution, le OU cumulatif sans court-circuit ; AUCUNE brique d'inversion AES : le GCM re-chiffre les compteurs). La famille `enregistrement` (tls13-20..21) : protéger/déprotéger (RFC 8446 § 5.2 : le nonce IV ⊕ séquence, l'AAD = l'en-tête ÉMISE/REÇUE, le texte interne charge+type, l'opaque 23, la borne 2^14, l'échec -4 SANS incrément de séquence — la rejoue attrapée par la cryptographie). La famille `poignée` (tls13-22..26) : le ClientHello FIXE de 114 o (quatre extensions, la construction re-jouée en Python par l'instrument), le ServerHello TRAITÉ (chaque divergence un refus nommé — le HRR -5, la suite -5, la valeur magique du plan), le calendrier à TROIS étages (§ 7.1 : chaque étage AVANCÉ PAR UN APPEL, la machine -3 sur tout saut, les contextes enregistrement POSÉS complets, le hash du transcript en ARGUMENT — le calendrier ne hache rien), le Finished (calculer/vérifier : l'HMAC du transcript), l'épinglage (la comparaison, jamais la croyance — l'empreinte du kit, -6 nommé). La famille `principal` (tls13-27..28) : la machine d'états du client (17 520 o de disposition DÉCLARÉE, quatre événements nommés, OUVRIR tient la poignée ENTIÈRE par la boucle bloquante du socle, le transcript absorbé à CHAQUE message dans l'ordre exact, la coupe du hash par COPIE du contexte — l'original vit), la rotule de transport (deux rappels en ARGUMENT par pointeur : NI import NI syscall, l'oracle structurel le constatera ; le simulateur au harnais, sys-04+ au terrain — jamais ws2_32).

**Le plan d'adressage étendu.** tls13/layout.py porte les constantes publiques des SIX familles : les masques ipad/opad, la borne HKDF, les membres de p et le masque M51, a24, le point de base 9, l'exposant d'inversion p − 2 (32 o little-endian), les tailles AES/GCM, R = 0xE1 || 0^15, les types d'enregistrement, la version héritage, la borne 2^14, les dispositions enregistrement (200 o) et session (17 520 o), les identifiants d'extensions, les algorithmes de signature déclaratifs, LA VALEUR MAGIQUE HRR (SHA-256 de « HelloRetryRequest »), les libellés du calendrier (données publiques). **L'ERRATUM av-10 (sur pièces, AVANT la notation — le modèle M8-(b) libc-02)** : la spec av-10 (M7) écrit « 0x7ffffffffffedc » pour le membre 0 de p — coquille d'ÉCRITURE (quatorze chiffres = 55 bits, un membre de 51 bits en a treize ; le membre 0 de p = 2^255 − 19 = 0x7ffffffffffed) ; l'oracle différentiel d'av-10 (« p → 0 ») ne pouvait passer qu'avec la valeur juste : l'écriture seule est fautive, jamais la notation prouvée — le miroir M9 RE-DÉRIVE par arithmétique, il ne copie JAMAIS l'hexadécimal d'une spec.

**L'instrument et ses trois défauts nommés.** scripts/verifier_specs_m9a.py [labo] : 117 contrôles — les 28 specs présentes et bien formées (tête, sections, la formule structurelle), la table des identifiants h100001..h100028, les constantes RE-DÉRIVÉES par arithmétique au geste même (les membres de p, p − 2, la valeur magique HRR, R, les longueurs), le ClientHello RE-CONSTRUIT (114 o == la constante), le ServerHello minimal (90 o), la session recomptée (17 520 o), les verdicts cités vivant dans la table des SEPT. Le fail-closed a nommé TROIS défauts avant le vert (l'instrument s'instruit AVANT les pièces, D165 rejouée) : les identifiants machine lus en HEXADÉCIMAL alors qu'ils sont DÉCIMAUX (les neuf premiers passaient par coïncidence — aucun chiffre a-f : la coïncidence n'est pas une preuve), l'ordre de tri de la table des verdicts attendu dans le mauvais sens, et la formule « AUCUNE entrée IAT, AUCUN site syscall » absente de tls13-27 (la constante des 27 autres — le PLUS GRAND bloc la portait le moins) : corrigés, rejoués, VERT.

**Détail.** FRONTIÈRES : aucune balise ne bouge (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 INTACTES), AUCUN build (la dette de cérémonie demeure : m0 CODE 10 + tls13 CODE 12 — la remise du développeur précède, D87/D162), m8/proxy.exe INTACT (1492b0bc…), les specs citent les RFC et normes par section et l'héritage par contrat (jamais une copie) ; la spec av-10 du M7 DEMEURE TELLE QUELLE (l'erratum vit dans la couche M9 — la pièce scellée ne se réécrit pas). Livrables : tls13/I/tls13-05..28 (les 24), tls13/layout.py, tls13/I/README.md (la clôture du chantier (a) + l'erratum), scripts/verifier_specs_m9a.py ; consignations : la présente Entrée PAR SCRIPT, D167 PAR SCRIPT (docs/DECISIONS.md), PLAN (le chantier M9-(a) RÉALISÉ + l'État du programme), worklog +Task ID 84 ; scripts suivis : inserer_entree_166.py.

- SUITE : LE KIT DE CÉRÉMONIE DE L'ÈRE M9 au dossier /Cérémonie du Drive (modèle Entrée 159 : le LISEZMOI de la cérémonie + la remise a-signer.txt [13 arbres] + les outils — la main du développeur SERVIE) ; PUIS le chantier (b) — la notation et les vecteurs officiels — APRÈS la remise (le garde le requiert).

"""

DECISION = """
## D167 — LE CHANTIER M9-(a) SE CLÔT SUR LES 28 SPÉCIFICATIONS AVANT TOUT OCTET DE NOTATION (R2 : la couche I complète — les 24 du geste en SIX familles, l'instrument 117 VERTS) ; LES CONSTANTES DU PLAN SONT DÉRIVÉES PAR ARITHMÉTIQUE, JAMAIS COPIÉES D'UNE SPEC (l'erratum av-10 : quatorze chiffres hexadécimaux pour un membre de 51 bits — l'écriture fautive, la notation prouvée demeurée juste) ; LE MIROIR NOMME SES DIVERGENCES ET SES AMÉLIORATIONS SUR L'HÉRITAGE f25519 (le gel SANS branche de données — l'amélioration sur av-10 exigée par la charte § 3 ; l'échelle EN PILE — la divergence sur av-11 exigée par la charte § 6, la réentrance par construction) ; L'ARRÊT AES-NI ET L'ABSENCE DE LA BRIQUE D'INVERSION (le S-box matériel temps constant, jamais la table indexée par la clé ; le GCM re-chiffre les compteurs — la découpe le nomme au lieu de le cacher)

**Le contexte qui fonde la décision (05/11 au soir).** La couche I du M9 était ouverte à la famille `sha` (Entrée 165, D166) ; le travail restant était nommé : « les 24 spécifications restantes (hkdf, x25519, aead, enregistrement, poignée, principal — R2) ». Le geste les pose TOUTES, la charte à HUIT règles instanciée bloc par bloc, et clôt le chantier (a) sur une preuve d'instrument (117 contrôles VERTS après trois défauts nommés par le fail-closed — l'instrument s'instruit avant les pièces, D165 rejouée). Un erratum d'HÉRITAGE est consigné au passage : la spec av-10 (M7) porte une écriture hexadécimale impossible pour le membre 0 de p — la preuve par la largeur (quatorze chiffres = 55 bits ≠ 51) et par l'oracle (le vecteur « p → 0 » ne passe qu'avec la valeur juste) ; le miroir ne réécrit pas la spec scellée du M7, il RE-DÉRIVE sa propre constante et cite.

**Les règles.** (1) **La couche I se clôt sur la preuve, pas sur l'annonce** : le chantier (a) est RÉALISÉ parce que l'instrument constate 28/28 specs présentes et bien formées, la table des identifiants h100001..h100028 (DÉCIMAUX, le miroir des g9xxxx du M8), les constantes du plan re-dérivées, les constructions re-jouées (le ClientHello 114 o, le ServerHello minimal 90 o, la session 17 520 o recomptée) et les verdicts cités vivant dans la table des SEPT. (2) **Une constante du plan est DÉRIVÉE par arithmétique ou elle n'est pas** : l'erratum av-10 devient la règle — le miroir ne copie jamais l'hexadécimal d'une spec, il re-dérive (le juge est le code) ; l'instrument RE-DÉRIVE au geste même (les membres de p, p − 2, la valeur magique HRR par SHA-256 re-calculé, R). (3) **Le miroir NOMME chaque divergence et chaque amélioration sur l'héritage** : la passe propagation+gel FUSIONNÉE en une frontière d'appel (av-06+av-10 → tls13-12) ; le gel SANS branche de données (l'amélioration sur av-10 : la sélection par masque sar — les intermédiaires de l'échelle sont des secrets, charte § 3) ; l'échelle EN PILE (la divergence sur av-11 : le M7 tenait ses zones en .bss, la charte § 6 l'interdit — le bloc est réentrant par construction) ; l'arrêt AES-NI (AESKEYGENASSIST/AESENC/AESENCLAST : le S-box matériel, jamais la table logicielle indexée par la clé) ; AUCUNE brique d'inversion AES (le GCM re-chiffre les compteurs : la découpe le NOMME) ; GHASH sans table par donnée (PCLMULQDQ chantier futur nommé — la marche binaire est la transcription exacte de la norme). (4) **Les bornes sont nommées, jamais tacites** : la charge 2^14 (RFC 8446 § 5.1), le réassemblage de poignée 2^14 (le certificat du monde réel y tient — la borne du jalon), la boucle HKDF 8160 (l'octet compteur), l'alerne autre que close_notify → l'état MORT (le couple niveau/description CONSIGNÉ au tampon — l'information n'est jamais muette). (5) **La machine d'états tient la poignée ENTIÈRE par la rotule** : OUVRIR fait CH → SH → {EE, Cert, CV, Fin} → Finished client en UNE boucle bloquante sur les rappels du socle tls13-28 (le transport est un ARGUMENT pointé — NI import NI syscall, la liste des compositions est FERMÉE) ; le hash du transcript est COPIÉ puis la copie finalisée (l'original vit — RFC 8446 § 7.1 exige le hash courant à chaque étage).

**Alternatives rejetées.** Poser les familles au fil des chantiers suivants (rejeté : R2 exige la spec AVANT la notation — la couche I entière précède, le chantier (b) n'ouvrira pas sur une spec à écrire) ; copier les constantes des specs M6/M7 (rejeté : l'erratum av-10 le prouve — une écriture fautive copiée serait une constante fausse) ; garder le gel à branches du M7 (rejeté : la charte § 3 du M9 nomme les secrets — l'amélioration est exigée, elle est nommée) ; l'échelle en .bss comme av-11 (rejeté : charte § 6 — la pile suffit, la réentrance est gratuite) ; une brique AES de déchiffrement par symétrie apparente (rejeté : le GCM n'en a JAMAIS besoin — le CTR re-chiffre ; une brique inutile serait une surface inutile) ; la table de Shoup pour GHASH (rejeté : indexée par donnée — charte § 3) ; la vérification CertificateVerify au jalon (rejeté : chantier futur nommé avec l'analyse X.509 — l'épinglage tranche la confiance, le domaine le NOMME) ; un huitième verdict « alerne » (rejeté : la table des SEPT est scellée par la charte — l'alerne fatale passe par l'état MORT et le -3, le couple consigné ; on n'étend pas une table scellée en silence).

**Frontières.** AUCUNE balise ne bouge (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 INTACTES) ; AUCUN octet de notation tls13 n'existe (R2 tenue) ; AUCUN build avant la remise du développeur (le garde m0 CODE 10 + tls13 CODE 12 — la dette de cérémonie demeure, c'est son travail) ; la spec av-10 du M7 DEMEURE TELLE QUELLE (l'erratum vit dans la couche M9, la pièce scellée ne se réécrit pas) ; m8/proxy.exe INTACT (1492b0bc…). Les pièces de l'arrêt : tls13/I/tls13-05..28, tls13/layout.py, tls13/I/README.md (la clôture + l'erratum), scripts/verifier_specs_m9a.py (117 VERTS).
"""

TASK = """
## Task ID 84 — LE CHANTIER M9-(a) COMPLET : LES 28 SPÉCIFICATIONS POSÉES — les 24 du geste (hkdf, x25519, aead, enregistrement, poignée, principal), le plan étendu aux SIX familles, l'erratum av-10 consigné, l'instrument 117 VERTS (05/11 au soir)

- LA REPRISE : les trois miroirs confrontés (local == GitHub == 45c8970 la
  pointe, le bundle 090-ab48be1 au geste), les canaux 200 ; un défaut
  d'instrument nommé au geste même (le recyclage du disque avait posé le bit
  exécutable sur 179 fichiers suivis — ZÉRO octet de contenu : réparé par git
  restore, l'arbre propre re-constaté).
- LES 24 SPÉCIFICATIONS : hkdf (HMAC RFC 2104/4231, Extract/Expand RFC
  5869, Expand-Label RFC 8446 § 7.1) ; x25519 (les miroirs av-05..11, la
  passe propagation+gel FUSIONNÉE, l'échelle SANS branche de données, l'état
  EN PILE — la divergence nommée sur av-11) ; aead (l'arrêt AES-NI, GHASH
  sans table par donnée, le tag VÉRIFIÉ avant restitution, AUCUNE brique
  d'inversion) ; enregistrement (le nonce IV ⊕ séquence, l'AAD = l'en-tête,
  l'opaque 23, la borne 2^14) ; poignée (le ClientHello FIXE 114 o, le
  ServerHello aux refus nommés [HRR -5, suite -5], le calendrier à trois
  étages, le Finished, l'épinglage -6) ; principal (la machine d'états
  17 520 o, quatre événements, OUVRIR tient la poignée entière par la
  rotule ; le socle d'appel à deux rappels en argument).
- LE PLAN ÉTENDU : les constantes des SIX familles DÉRIVÉES PAR ARITHMÉTIQUE
  (les membres de p, p − 2, la valeur magique HRR, R, les libellés, les
  dispositions 200/17 520 o) ; l'ERRATUM av-10 consigné AVANT la notation
  (quatorze chiffres hex pour un membre de 51 bits — l'écriture fautive,
  jamais la notation prouvée ; le miroir re-dérive, il ne copie pas).
- L'INSTRUMENT : verifier_specs_m9a.py — 117 contrôles VERTS (28/28 specs,
  la table h100001..h100028, les constantes re-dérivées, les constructions
  re-jouées 114/90/17 520, les verdicts dans la table des SEPT) ; TROIS
  défauts nommés par le fail-closed avant le vert (les identifiants lus en
  hex au lieu du DÉCIMAL — les neuf premiers passaient par coïncidence ;
  l'ordre de tri de la table ; la formule structurelle absente de tls13-27)
  : corrigés, rejoués.
- FRONTIÈRES : aucune balise ne bouge (0.9.0/0.7.0/0.8.0 INTACTES), AUCUN
  octet de notation (R2), AUCUN build avant la remise (la dette de
  cérémonie demeure) ; consignations : Entrée 166 PAR SCRIPT, D167 PAR
  SCRIPT, PLAN (chantier (a) RÉALISÉ + État), worklog +Task ID 84 ;
  scripts suivis : inserer_entree_166.py, verifier_specs_m9a.py [labo].
- SUITE : le kit de cérémonie de l'ère M9 au /Cérémonie du Drive (modèle
  Entrée 159) ; puis le chantier (b) — la notation et les vecteurs
  officiels — APRÈS la remise du développeur.

Stage Summary:
- LE CHANTIER M9-(a) EST RÉALISÉ : les 28 spécifications posées avant tout
  octet de notation, la charte instanciée bloc par bloc, les constantes
  re-dérivées par arithmétique — l'erratum av-10 consigné en fait la règle.
- LA COÏNCIDENCE N'EST PAS UNE PREUVE (les neuf premiers identifiants
  passaient en hex par hasard) : le fail-closed a nommé, l'instrument s'est
  instruit, le vert final est gagné.
"""

LIGNE_ETAT_OLD = ("la dette de cérémonie nommée (le garde m0 CODE 10 + "
                  "tls13 CODE 12).**")
LIGNE_ETAT_NEW = ("la dette de cérémonie nommée (le garde m0 CODE 10 + "
                  "tls13 CODE 12).** **LE CHANTIER M9-(a) RÉALISÉ le "
                  "05/11/2026 au soir (Entrée 166, D167) : LES 28 "
                  "SPÉCIFICATIONS POSÉES** (la famille sha à l'ouverture, "
                  "les 24 suivantes au geste — les constantes du plan "
                  "re-dérivées par arithmétique, l'erratum av-10 consigné "
                  "avant la notation, l'instrument 117 VERTS) : R2 tenue, "
                  "aucun octet de notation, la cérémonie de l'ère précède "
                  "tout build.**")

CELLULE_OLD = ("PRÉPARÉE ; **les 24 specs restantes se posent AVANT toute "
               "notation (R2)** |")
CELLULE_NEW = ("PRÉPARÉE ; **LES 24 SPECS RESTANTES POSÉES au geste (Entrée "
               "166, D167)** — hkdf (HMAC RFC 2104/4231, Extract/Expand RFC "
               "5869, Expand-Label § 7.1), x25519 (les miroirs av-05..11 : "
               "la passe propagation+gel FUSIONNÉE, l'échelle SANS branche "
               "de données, l'état EN PILE — les divergences et "
               "améliorations nommées), aead (l'arrêt AES-NI, GHASH sans "
               "table par donnée, le tag VÉRIFIÉ avant restitution, AUCUNE "
               "brique d'inversion), enregistrement (le nonce IV ⊕ "
               "séquence, l'AAD = l'en-tête, l'opaque 23, la borne 2^14), "
               "poignée (le ClientHello FIXE 114 o, le ServerHello aux "
               "refus nommés [HRR -5, suite -5], le calendrier à trois "
               "étages, le Finished, l'épinglage -6), principal (la machine "
               "d'états 17 520 o + la rotule de transport à rappels en "
               "argument) ; le plan d'adressage étendu aux SIX familles "
               "(les constantes DÉRIVÉES PAR ARITHMÉTIQUE — l'erratum av-10 "
               "consigné avant la notation) ; **l'instrument "
               "verifier_specs_m9a.py : 117 contrôles VERTS** (le juge est "
               "le code) ; R2 tenue — AUCUN octet de notation ; le garde "
               "constate toujours la dette de cérémonie (m0 CODE 10, tls13 "
               "CODE 12 — la remise précède tout build) |")


def main() -> int:
    journal = JOURNAL.read_text(encoding="utf-8")
    worklog = WORKLOG.read_text(encoding="utf-8")
    decisions = DECISIONS.read_text(encoding="utf-8")
    plan = PLAN.read_text(encoding="utf-8")

    ancres = {
        "l'Entrée 165 (l'ordre)": "## Entrée 165 —" in journal,
        "l'Entrée 166 absente (rejeu refusé)": "## Entrée 166 —" not in journal,
        "le marqueur du journal": MARQUEUR in journal,
        "le Task 83 au worklog": "## Task ID 83 —" in worklog,
        "le Task 84 absent (rejeu refusé)": "## Task ID 84 —" not in worklog,
        "D166 déjà consignée": "## D166 —" in decisions,
        "D167 absente (rejeu refusé)": "## D167 —" not in decisions,
        "le PLAN porte la table M9": "Chantier M9 (win, l'ère 1.0.0" in plan,
        "le PLAN porte la cellule OUVERT du (a)": CELLULE_OLD in plan,
        "le PLAN porte la ligne d'État": LIGNE_ETAT_OLD in plan,
    }
    manquantes = [n for n, ok in ancres.items() if not ok]
    if manquantes:
        print(f"[inserer-166] ÉCHEC NOMMÉ — ancres absentes : {manquantes}")
        return 2

    journal = journal.replace(MARQUEUR, ENTREE + MARQUEUR, 1)
    JOURNAL.write_text(journal, encoding="utf-8")
    with DECISIONS.open("a", encoding="utf-8") as f:
        f.write(DECISION)
    plan = plan.replace(CELLULE_OLD, CELLULE_NEW, 1)
    plan = plan.replace(LIGNE_ETAT_OLD, LIGNE_ETAT_NEW, 1)
    PLAN.write_text(plan, encoding="utf-8")
    with WORKLOG.open("a", encoding="utf-8") as f:
        f.write(TASK)
    print("[inserer-166] Entrée 166 insérée avant le marqueur ; D167 "
          "consignée ; PLAN (cellule (a) + État) mis à jour ; Task 84 "
          "ajouté")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
