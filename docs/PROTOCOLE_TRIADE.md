# PROTOCOLE TRIADE v0.15.0 — Spécification technique

> Source de travail faisant autorité pour la v0.15.0. Les archives formelles des versions
> précédentes demeurent : `docs/Protocole_TRIADE_v0.14.0_Specification.pdf` (v0.14.0 —
> le programme empirique), `docs/Protocole_TRIADE_v0.13.0_Specification.pdf` (v0.13.0 —
> les corrections de l'édition), `docs/Protocole_TRIADE_v0.12.0_Specification.pdf` (v0.12.0 — le
> modèle formel et la gouvernance assainie), `docs/Protocole_TRIADE_v0.11.0_Specification.pdf`
> (v0.11.0), `docs/Protocole_TRIADE_v0.10.0_Specification.pdf` (v0.10.0),
> `docs/Protocole_TRIADE_v0.9.0_Specification.pdf` (v0.9.0 — consolidation d'après M10),
> `docs/Protocole_TRIADE_v0.8.4_Specification.pdf` (v0.8.4 — dernière révision de terrain du TGN),
> `docs/Protocole_TRIADE_v0.8.0_Specification.pdf` (v0.8.0),
> `docs/Protocole_TRIADE_v0.7.0_Specification.pdf` (v0.7.0),
> `docs/Protocole_TRIADE_v0.6.1_Specification.pdf` (v0.6.1),
> `docs/Protocole_TRIADE_v0.6.0_Specification.pdf` (v0.6.0),
> `docs/Protocole_TRIADE_v0.5.2_Specification.pdf` (v0.5.2),
> `docs/Protocole_TRIADE_v0.5.0_Specification.pdf` (v0.5.0),
> `docs/Protocole_TRIADE_v0.4.0_Specification.pdf` (v0.4.0),
> `docs/Protocole_TRIADE_v0.3_Specification.pdf` (v0.3),
> `docs/Protocole_TRIADE_v0.2_Specification.pdf` (v0.2). La série documentaire compte
> également la démonstration RoomEq (`docs/Protocole_TRIADE_v0.3_Demonstration_RoomEq.pdf`)
> et l'édition académique v0.4 (`docs/Protocole_TRIADE_v0.4_Article_Recherche.pdf`, D18 —
> présentation IMRAD du noyau v0.3, sans valeur normative) ; depuis la v0.6.0, le
> **Livre du Coffre** l'accompagne (`docs/Livre_du_Coffre_TRIADE_CF1-CF3_v1.1.pdf`,
> D137 — complément opératoire : cérémonies, runbook, mode dégradé ; v1.1 : l'arbitrage
> D137 du niveau de naissance y est aligné). Depuis la décision D17,
> le PDF formel de la version courante est **régénéré systématiquement** à chaque
> modification des sources du protocole : `scripts/build_pdf.sh` compare l'empreinte des
> sources au stamp du dernier build et reconstruit avant chaque sauvegarde (`sync_backup.sh`).
> La v0.14.0 consigne LE PROGRAMME EMPIRIQUE (D193/D194/D195, le
> cinquième fichier d'instructions) : LE BRAS DE RÉFÉRENCE COMPILATEUR
> pré-enregistré (le plan D193 consigné AVANT toute mesure, l'empreinte
> verrouillée ; six blocs C depuis les MÊMES contrats, les mêmes shims,
> auto-vérifiés : ZÉRO DIVERGENCE aux vecteurs — la notation et le
> compilé observationnellement équivalents ; sha-256 PARITAIRE à travail
> égal [9 089 contre 9 146 instructions], les purs plus chers, la
> mutation au même degré — H4 tenue) ; LA RE-MESURE RQ2 en distributions
> (localiser 580 [496..706], éditer 2 143 [1 085..3 463], ajouter
> 3 510 [3 128..4 091], la baseline naive 300 304 — les valeurs M1
> historiques, la lecture DÉFAVORABLE au protocole consignée) ;
> L'INDÉPENDANCE par instance isolée (128 constantes, zéro divergence,
> l'écart de famille nommé) ; LE RE-JEU DES 832 MUTANTS aux
> composition-killers (93,3 % — tls13 et sys à 100 %, les 56 survivants
> loupe nommés) ; LE KIT TERRAIN en attente du geste du développeur.
> Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie
> inchangée.

> La v0.13.0 consigne LES CORRECTIONS DE L'ÉDITION (D190/D191/D192, le
> quatrième fichier d'instructions) : la liste exhaustive d'incohérences
> VÉRIFIÉE UNE À UNE (quatorze arbres signés, comptes exacts du journal en
> macros générées, « Fig. 5 » → « Table 5 », la Table 6 des preuves
> RÉGÉNÉRÉE intégralement en anglais par le générateur ANTI-TRONCATURE, la
> note TOTAL/brouillons du tableau des budgets, le paragraphe de
> consolidation aligné sur D181 [douze runs, loupe 0.1.1 scellée], la
> phrase du tableau de menaces, les renvois recalés) ; LES STATISTIQUES
> REFORMULÉES (P(sceller|q) = (1−q)ⁿ — les « α » de D189 étaient des
> rapports de vraisemblance mal étiquetés ; quantiles unilatéraux exacts
> 1,87σ/3,10σ ; l'IC95 % exact de 11/12 [0,615 ; 0,998] avec la réserve
> de non-indépendance ; la règle de comptage opérationnelle des défauts
> échappés) ; LE BENCHMARK AUDITÉ (le facteur « 15,3 » RETIRÉ comme
> ARTEFACT DE PÉRIMÈTRE : l'instrument lisait le compteur de la
> finalisation SEULE après le pipeline, comparé à l'opération complète de
> la référence — 4,16 instructions/ronde était le signe ; les chiffres
> corrigés : 75 983 instructions/op complète contre 69 132 [gcc -O2] et
> 77 505 [-Os], condensé vérifié avant comptage, 17 compressions
> confirmées — la notation est COMPÉTITIVE [−9 %/+2 %], jamais
> spectaculaire) ; LA NEUTRALITÉ DOCUMENTAIRE (l'anti-debug léger
> documenté honnêtement dans les deux documents — la dissuasion, jamais la
> résistance ; la conséquence D81 au modèle de menace : la phrase au dépôt
> + S_serrure en en-tête clair = deux éléments trivialement disponibles,
> la confidentialité effective repose sur le seul média piège ; la
> frontière D105/D81 du clone du laboratoire ; le terrain M7 requalifié :
> qemu-riscv64 TCG au noyau réel, la sémantique matérielle I-cache de
> fence.i NON prouvée sur silicium) ; LE KIT DE LA CÉRÉMONIE D183 PRÉPARÉ
> SANS L'APPLIQUER (`scripts/kit_ceremonie_d183/` : l'outil au partage
> CF2 D120 tel quel, l'autotest VERT sur phrase de test publique, le
> LISEZMOI pas à pas — le geste appartient au développeur) ; L'ÉTAT DE
> L'ART ÉTENDU (huit références vérifiées DOI/arXiv : LLM Compiler,
> CompCert, Kitsune, POLUS, SWE-agent, Jakobi, Peng, Bacic ; la
> revendication « first quantified account » scopée ; RQ3 recadrée en
> GARANTIES SILENCIEUSES DU COMPILATEUR). Aucune règle modifiée, aucune
> couche d'exécution ajoutée, hiérarchie inchangée.

> La v0.12.0 consigne LE MODÈLE FORMEL ET LA GOUVERNANCE ASSAINIE
> (D187/D188/D189, le troisième fichier d'instructions) : CF3 modélisé en
> machine à états et vérifié par exploration exhaustive — les QUATRE
> propriétés PROUVÉES DANS LE MODÈLE (le secret sous seuil, le refus du
> roll-back, l'absence de destruction sur phrase erronée, le rayon borné à
> une époque), les hypothèses d'adversaire EXPLICITES (A1-A5, le hors
> modèle nommé), le vérificateur nommé (l'explorateur d'états —
> Tamarin/ProVerif absents du labo) ; le modèle de menace RESTRUCTURÉ EN
> DEUX PLANS (IP contre sûreté d'exécution) avec l'ordre intra-sécurité
> EXPLICITE (le plan sûreté gagne) et la tension D81↔D183 consignée avec
> l'analyse chiffrée ; la cristallisation ÉVALUÉE (le seuil 10 justifié —
> l'étiquetage « α » des rapports de vraisemblance de D189 est CORRIGÉ
> par D190 : voir les caractéristiques opérationnelles ci-dessus ; le
> seuil demeure, la politique jamais changée en silence) et le protocole
> de réplication PROPOSÉ (trois axes, grille T/X, κ de Cohen ≥ 0,61) ;
> les manifestes de kit à sha256 (la suite de D184). Aucune règle
> modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée.

> La v0.11.0 consigne LES PREUVES RENFORCÉES (D185/D186, le deuxième
> fichier d'instructions du coffre) : SIX instruments au laboratoire
> (graines consignées, reproductibles) — le mutation testing (832 mutants,
> 83,4 % tués, les familles crypto à 100 %, les survivants nommés), le
> fuzzage guidé par couverture (loupe-01 60,5 %, zéro crash ; http-10 zéro
> faute), la sûreté mémoire statique bornée (2 098 accès classés, ZÉRO
> hors-cadre, 463 non résolus nommés), le temps constant d'émulation
> (STRUCTUREL : traces indépendantes du secret ; le temps réel NON MESURÉ —
> la limite explicite), les benchmarks comparatifs (sha256 : l'opération complète 75 983
> instructions/op contre 69 132 à la référence gcc -O2 et 77 505 à -Os,
> au MÊME émulateur — le « facteur 15,3 » publié par la v0.11.0 était
> un ARTEFACT DE PÉRIMÈTRE retiré par l'audit D191 ; md5/aes écartés
> par l'auto-vérification de l'instrument), l'indépendance de l'oracle (zéro divergence par voies
> distinctes) ; la spécification CSPRNG manquante COMBLÉE en brouillon
> (tls13-29, l'entrée à l'arbre signé attend la cérémonie d'ère du
> développeur — D186) ; les vecteurs RFC 8446 au corpus de fixtures
> partagées ; le manuscrit v0.11.0 (Results étendu § 4.5, limites mises à
> jour, ce qui reste ouvert précisément mesuré). AUCUNE règle modifiée,
> AUCUNE couche d'exécution ajoutée, hiérarchie inchangée — les
> instruments vivent au laboratoire, les artefacts scellés et les arbres
> signés INTACTS.

> La v0.10.0 consigne L'ÉDITION ACADÉMIQUE (D182, la commande du développeur du
> 11/11 : trois fichiers d'instructions au dossier `/instructions` du coffre) :
> le manuscrit IMRAD en anglais (résumé français inclus) — quatre questions de
> recherche (défauts échappés, coût en tokens par changement validé, classes
> invisibles à l'émulation, sûreté du patch à chaud), les données réelles du
> journal EXTRAITES PAR SCRIPT, la formulation corrigée (aucune chaîne de
> traduction optimisante ni opaque — assemblage WYSIWYG vérifié par round-trip ;
> l'évolution du code volé est bloquée, son exécution ne l'est pas ; les termes
> standards de l'ingénierie ; D19 requalifiée politique de projet explicite),
> l'auteur humain unique (l'agent IA en méthodes et remerciements, jamais
> co-auteur), les déclarations Ethics/dual-use, Data Availability, Limitations ;
> la proposition D183 (le séquestre chiffré de la phrase de contrôle —
> documentée, NON appliquée au coffre réel) ; l'annexe A portée à sha-256
> (D184 — md5 demeure une fonctionnalité d'affichage de Loupe, aucun octet de
> la pièce ne change) ; les livrables `TRIADE_soumission_v0.10.0.zip` (cinq
> fichiers au plus, readme inclus, le manuscrit en pdf) et
> `TRIADE_complet_v0.10.0.zip` (l'intégralité). Aucune règle modifiée, aucune
> couche d'exécution ajoutée, hiérarchie inchangée — l'édition consigne, elle
> ne légifère pas.

> La v0.9.0 consolide le programme d'après M10 (D178/D179) : LE JALON M10 — le test
> grandeur nature, l'application « Loupe » (l'éditeur hexadécimal au panneau
> d'empreintes, le domaine `loupe`) — est FRANCHI : l'application est NÉE ENTIÈREMENT
> DE LA MÉTHODE (la cérémonie d'ère passée sur pièces — le garde à QUATORZE arbres,
> les 18 blocs NOTÉS-MESURÉS-PROUVÉS, le kit déployé au coffre /test), ONZE RUNS
> TERRAIN l'ont VÉCUE — onze défauts nommés, onze retouches documentées (chaque
> défaut du kit ou de la pièce NOMMÉ sur pièces, jamais un vert muet) — ET LA
> VITRINE A VÉCU CHEZ SON UTILISATEUR (les deux codes à 0, deux runs de suite) :
> LE ONZIÈME RUN recoupé 39/39, LA BALISE `loupe 0.1.0` SCELLÉE PAR FAIT DE
> CARTE (D178 — l'artefact INTACT, la dette de la carte soldée par la
> régénération des notations, la cristallisation 26 × 10/10, l'anti-rollback
> ARMÉ) : LA MÉTHODE TRIADE ENTIÈRE PROUVÉE PAR LA CRÉATION. LE PROGRAMME
> D'APRÈS M10 est ouvert à la commande du développeur (D179) : la version
> `0.1.1-dev.1` est NÉE DE LA RECOMPOSITION — la dette [R10-PÉRIMÉE] (les 17
> sommes de l'ère dev.5) SOLDÉE À LA NAISSANCE, le code BYTE-IDENTIQUE au vécu
> des onze runs (R4/R7), le DOUZIÈME RUN attendu : la balise `loupe 0.1.1` se
> scellera sur le vert recoupé (le miroir D165/D170) ; la
> v0.6.1 consigne l'arbitrage du niveau de naissance d'un coffre neuf (D137) ; la
> v0.6.0 avait consigné la passation du programme de souveraineté cryptographique (D133) :
> axes 2-3-4 accomplis et prouvés sur terrain — la chaîne réelle du coffre a migré
> CF1 → CF2 → CF3 les 30–31 octobre 2026 ; la v0.5.2 avait consigné la garde durable de
> la phrase de contrôle (D81) ; la v0.5.1 avait ajouté le coffre-fort (D75) et consigné
> M3 franchi ; la v0.5.0 demeure la révision du retour du terrain (validation normée,
> taxonomie X1–X8, jalons M0–M2).

- Version : v0.15.0 — la révision des PREUVES NON BORNÉES ET DU RAFFINEMENT (D197/D198 : le croisement d'attribution des instructions recoupé et corrigé, la règle du contenu cité, la règle d'archivage des versions ; l'invariant inductif [P1-P4 PROUVÉES NON BORNÉES, la fidélité D187 reproduite 154/1 152, les bornes étendues zéro hors I], le raffinement modèle↔implémentation [34 pas, zéro écart, les chemins d'échec inclus], les trois kits de mesure matérielle EN ATTENTE, la réplication outillée [grille finalisée, κ autotesté], les statuts systématiques). Sous la v0.14.0, la révision du programme empirique (D193/D194/D195 : le bras de référence pré-enregistré [zéro divergence, sha-256 paritaire, H4 tenue], la re-mesure RQ2 en distributions avec la baseline naive, l'indépendance par instance isolée, le re-jeu des 832 mutants aux composition-killers [93,3 %]). Sous la v0.13.0, la révision des corrections de l'édition (D190/D191/D192) : les incohérences vérifiées une à une (le rapport de conformité joint), les statistiques reformulées (P(sceller|q) = (1−q)ⁿ, l'IC95 exact de 11/12), le facteur 15,3 RETIRÉ par l'audit D191 (les chiffres corrigés : 75 983 contre 69 132/-Os 77 505), la neutralité documentaire (l'anti-debug arbitré, la conséquence D81 au modèle de menace, le M7 requalifié), le kit de cérémonie D183 préparé sans l'appliquer, l'état de l'art étendu (huit références vérifiées, RQ3 recadrée). Sous la v0.12.0, la révision du modèle formel et de la gouvernance assainie (D187/D188/D189) : CF3 vérifié par exploration exhaustive (quatre propriétés prouvées dans le modèle, hypothèses A1-A5 explicites) ; le modèle de menace en deux plans avec l'ordre intra-sécurité explicite ; la cristallisation justifiée (le seuil 10 demeure) ; le protocole de réplication proposé (grille T/X, κ de Cohen) ; les manifestes de kit à sha256 ; le manuscrit v0.12.0 § 4.1. Sous la v0.11.0, les preuves renforcées (D185/D186) : les six instruments de laboratoire (mutation 83,4 %, fuzzage guidé, sûreté mémoire bornée zéro hors-cadre, temps constant structurel, benchmarks [le facteur 15,3 retiré par l'audit D191], indépendance zéro divergence), la spec CSPRNG en brouillon (tls13-29 — la cérémonie d'ère attend le geste du développeur), les vecteurs RFC 8446 au corpus, le manuscrit v0.11.0 (§ 4.5 les preuves renforcées). Sous la v0.10.0, l'édition académique (D182 : le manuscrit IMRAD né du dépôt, la formulation corrigée ; D183 : la proposition de séquestre chiffré, non appliquée ; D184 : l'annexe A à sha-256) le manuscrit IMRAD en anglais (résumé français) né du dépôt — quatre questions de recherche, les données du journal extraites par script (`extraire_donnees_v100.py`, le manuscrit n'affirme rien qui ne soit vérifié), la formulation corrigée dans les termes standards de l'ingénierie, l'auteur humain unique, les déclarations Ethics/Data/Limitations ; la proposition D183 (séquestre chiffré de la phrase de contrôle — alternative documentée à la garde durable D81, NON appliquée au coffre réel) ; l'annexe A de gouvernance portée à sha-256 (D184 — md5 demeure une fonctionnalité d'affichage de Loupe) ; les livrables soumission (cinq fichiers au plus) et complet. Sous la v0.9.0, la consolidation du programme d'après M10 (D178/D179/D180/D181 : la balise `loupe 0.1.1` scellée sur le douzième run recoupé 39/39) **LE JALON M10 FRANCHI le 11/11/2026** — l'application « Loupe » NÉE ENTIÈREMENT DE LA MÉTHODE (la couche I de 18 spécifications écrites-avant-code, les QUATRE chantiers de notation — 159 contrôles verts aux trois graines —, la cérémonie d'ère PASSÉE : le garde 14/14, le kit déployé au coffre /test), ONZE RUNS TERRAIN (Entrées 202–219 : ONZE DÉFAUTS NOMMÉS, ONZE RETOUCHES DOCUMENTÉES — les refus du chargeur 0xc000007b [l'enveloppe de la lignée NORME DE FAIT], [CADRE-NÉ] [l'initialiseur .data MIROIR EXACT du CADRE_VIERGE — LE GARDE GUÉRI : le contrôle dérive du plan, jamais de la pièce qu'il contrôle], la classe des arguments pile [l'audit d'ABI msx64 NÉ AU BUILD], [SESSION] -7 [L'OMBRE au kit, l'artefact acquitté], [HINSTANCE-PEB] [r12 = GetModuleHandleW(NULL) LE VRAI MODULE], [D54-QUATRIÈME] + [EAX-SANS-SIGNE] [l'IAT relogée 0x3100 en QUATRE plages séparées par NULL, les 20 rendus étendus au 64 bits], [OFT-QWORD] [les QUATRE OFT au pas DWORD — la sixième mort NOMMÉE par le journal d'événements [4/4]], [FREE-SANS-TYPE] [le HMODULE en POINTEUR, l'essai isolé pour TOUTE classe], [RET-NU] [mov eax, 1 ; ret — le verdict ATTACH VRAI PAR CONSTRUCTION], [SONDE-EXE] [le faux négatif structurel : le chargeur de bibliothèque ne résout JAMAIS les imports d'un EXE — LA LIAISON PROUVÉE PAR LE VIVANT]) — ET LA VITRINE A VÉCU (0 et 0 aux dixième et onzième runs : L'APPLICATION NÉE DE TRIADE A VÉCU CHEZ SON UTILISATEUR) ; LE ONZIÈME RUN recoupé 39/39 : **LA BALISE `loupe 0.1.0` SCELLÉE PAR FAIT DE CARTE** (D178 — la dette de la carte soldée par la RÉGÉNÉRATION DES NOTATIONS [18/18 == la pièce OCTET POUR OCTET, l'écart 587 → 0], la cristallisation 26 × 10/10, la re-signature à la graine durable [LE TÉMOIN NE BOUGE PAS], l'anti-rollback ARMÉ, loupe.exe INTACT 054de960…) — LA MÉTHODE TRIADE ENTIÈRE PROUVÉE PAR LA CRÉATION ; LE PROGRAMME D'APRÈS M10 (D179, la commande du développeur) : la version `0.1.1-dev.1` NÉE DE LA RECOMPOSITION — LA DETTE [R10-PÉRIMÉE] SOLDÉE À LA NAISSANCE (les 17 sommes rafraîchies à la VÉRITÉ des blocs, le qword porté 0x00010008 → 0x00010101, 0 OCTET AILLEURS — le code byte-identique au vécu des onze runs, R4/R7), la carte GÉNÉRATION 17, le kit 0.1.1-dev.1 DÉPOSÉ au coffre /test (loupe-kit-13, le réceptacle ARMÉ) — LE DOUZIÈME RUN ATTENDU : si le vert tient, LA BALISE `loupe 0.1.1` SCELLÉE sur run recoupé (le miroir D165/D170). Sous les révisions de terrain v0.8.1 à v0.8.4, les enseignements des runs un à un ; sous la v0.8.0, la consolidation du programme d'après M9 (D170/D171)
- Date : 11 novembre 2026 (modèle formel)
- Couches : I/B/C · Profil primaire : x86-64 / Windows 11 / PE32+
- Hiérarchie de la fonction objectif : **Sécurité > Performance > Optimisation > Coût en tokens** — inchangée et verrouillée (D19)

---

## 1. Vision et objectifs

Le développement logiciel est entré dans l'ère agent-first : une part croissante du code est
écrite, relue et modifiée par des modèles de langage plutôt que par des humains. Cette
bascule remet en question une hypothèse centrale de nos outils — que le code source est
optimisé pour la lecture humaine. Compilateurs, systèmes de build et langages ont été conçus
autour de cette hypothèse ; si le lecteur principal devient une machine, l'empilement
complet mérite un réexamen systématique plutôt qu'une révision marginale.

TRIADE est la réponse disciplinée à ce réexamen. Plutôt que de supprimer les langages — une
impossibilité de principe, puisqu'un modèle de langage manipule des symboles textuels et que
tout format binaire rendu lisible par un agent constitue de facto un langage —, TRIADE
déplace le langage vers une fine couche de spécification maintenue par l'agent, tandis que
l'artefact livré est du code machine natif pur. Le compilateur disparaît du pipeline de
livraison : ce que l'agent écrit est ce qui s'exécute — et rien d'autre.

Le nom encode l'architecture : trois couches indissociables — Intention (I), Binaire (B),
Carte (C) — unies par un verrou croisé cryptographique. La couche I contient le quoi et le
pourquoi : contrats typés, pré et post-conditions, invariants, cas d'échec, vecteurs de
vérification. La couche B contient le comment : des octets scellés, versionnés, à adresses
stables. La couche C est l'index naviguable qui lie les deux et sert d'unique interface de
développement à l'agent.

La v0.4.0 tire les enseignements de la première validation à l'échelle — le recodage complet
de RoomEq (démonstration v0.3) — et les convertit en normes : ce que la démonstration a
pratiqué (reverse-specs, pré-versions, partage de fixtures, mesure avant optimisation)
devient exigence ; ce que son analyse des défauts a révélé devient taxonomie ; ce que son
étude de cas a établi et ne prouve pas reste explicitement hors périmètre de preuve.

La v0.5.0 est la révision du retour du terrain. Les jalons M0 (chaîne artefact), M1
(mini-libc scellée) et M2 (patch à chaud en production, avec retour arrière) sont franchis
— chacun sur validation terrain Windows 11, chacun scellé par une balise finale immuable
(0.2.0, 0.3.0). La campagne M2 a coûté huit classes de défauts invisibles à l'émulation
(§ 8.5) — le prix d'une leçon : un oracle valide un artefact contre un modèle
d'environnement, et la complétude du modèle ne se démontre qu'en exécutant le binaire sur
le système réel. Ce que le terrain a appris devient norme : la boucle d'évidence (§ 8.4),
la taxonomie X, l'instrumentation contractualisée — et l'ouverture du jalon M3, contrats
renforcés sur entrées non fiables.

### 1.1 Fonction objectif hiérarchisée — invariant de révision

**Sécurité > Performance > Optimisation > Coût en tokens** — arbitrage lexicographique : un
objectif n'est jamais sacrifié au profit d'un objectif de rang inférieur. La v0.4.0 consigne
cette hiérarchie comme **invariant de révision** (D19) : aucune révision future du
protocole ne peut la modifier sans invalider explicitement le protocole entier — pas
l'ordre, pas les rangs, pas la non-compensation.

| Objectif | Signification concrète | Métrique de validation |
|---|---|---|
| Sécurité | Sûreté mémoire validée par oracle, intégrité carte ↔ binaire, durcissement au chargement | 0 corruption détectée par l'oracle ; tout échec de verrou bloque la session ; échec de vérification au lancement = arrêt propre |
| Performance | 100 % code machine natif, zéro abstraction intermédiaire entre l'écriture et l'exécution | Comparaison par bloc scellé face à une référence compilée (clang -O2 ou équivalent du profil) |
| Optimisation | Descente à l'ISA sur les hot paths identifiés par profilage — jamais sans mesure (R11) | Gain mesuré et journalisé pour chaque bloc optimisé |
| Coût en tokens | Édition ciblée via la carte, jamais de lecture intégrale du binaire | Budgets par type d'édition (§ 14) |

### 1.2 Périmètre et non-objectifs

Cinq non-objectifs posés d'emblée. Premièrement, TRIADE ne prétend pas remplacer les
langages dans l'industrie : c'est une architecture de laboratoire, conçue pour être validée
sur une application réelle complète. Deuxièmement, la furtivité face aux EDR n'est pas
recherchée : l'outil cible est un utilitaire de pentest destiné à des tests autorisés en
environnement de laboratoire, et les API du système sont appelées via les interfaces
standards du profil. Troisièmement, l'universalité revendiquée est structurelle mais
progressive : chaque profil de cible doit être instancié et validé (jalons M6 et M7) avant
d'être déclaré supporté — le protocole ne promet pas la portabilité, il la vérifie.
Quatrièmement, aucune couche d'abstraction à l'exécution — bytecode portable, machine
virtuelle, traduction à la volée — n'est introduite par la présente révision ni ne le sera :
elle trahirait la fonction objectif Performance (rejet consigné, D14). Cinquièmement, la
couche de gouvernance validée par la démonstration RoomEq (spécifications avant code,
vérifie-puis-écrit, cristallisation) et le cœur natif du protocole (notation, verrou
cryptographique sur octets, patch à chaud) restent des niveaux de preuve distincts : les
jalons M0 à M10 demeurent la charge de validation du cœur natif — le TGN
l'exige tout entier : de l'intention (la couche I) à l'octet livré (le kit terrain),
chaque geste d'une application réelle NEUVE est prouvé sur pièces.

### 1.3 Ce que change la v0.4.0

Dix-sept évolutions, toutes tracées dans la correspondance du § 19 et dans le journal des
versions (§ 21), toutes rattachées aux décisions D19 à D24 : normalisation de la couche I
(§ 2), taxonomie des défauts de contrat non écrit (§ 3), traçabilité I ↔ C ↔ B ↔ tests
(§ 4.2), norme de fragmentation et localisation par intention (§ 7, § 14), R10 renforcée
et R11 nouvelle (§ 6), suite de conformité par profil et parité inter-profils (§ 8),
pré-versions de cristallisation (§ 9), reverse-specs (§ 10), journal d'optimisation
(§ 11), modèle de menace étendu (§ 15), journal des décisions normalisé et tableau de bord
de conformité (§ 17). Aucune règle existante n'est affaiblie ; aucune couche n'est ajoutée
à l'exécution ; la hiérarchie de la fonction objectif est inchangée.

### 1.4 Ce que change la v0.5.0

Huit évolutions, toutes tracées dans la correspondance (§ 19.3) et le journal des versions
(§ 21), toutes rattachées aux décisions D26 à D45 : la validation terrain devient une
couche de vérification normée — boucle d'évidence, journal d'exécution, instrumentation
contractualisée, diff chirurgical (§ 8.4) ; la taxonomie des défauts s'étend des classes T
(contrat non écrit) aux classes X — défauts invisibles à l'émulation, huit classes nommées
par la campagne M2 (§ 8.5) ; l'état des jalons est constaté — M0, M1 et M2 franchis sur
validations terrain Windows 11, balises finales 0.2.0 et 0.3.0 posées (§ 18) ; le budget
de localisation est corrigé à 64 tokens (D31) et les budgets affichent leurs valeurs
mesurées (§ 14, § 17.2) ; les volumes d'oracle effectifs sont consignés ; les preuves
terrain sont archivées brutes avec leurs empreintes ; le corpus de démonstration (huit
itérations instrumentées) devient l'occurrence de référence de la méthode ; le jalon M3
est ouvert — contrats renforcés sur entrées non fiables et fuzzing à propriétés (D45).
Aucune règle n'est modifiée ; aucune couche n'est ajoutée à l'exécution ; la hiérarchie de
la fonction objectif est inchangée.

### 1.5 Ce que change la v0.5.1

Un composant nouveau et deux constats, tous tracés dans la correspondance (§ 19.5) et le
journal des versions (§ 21), rattachés à la décision D75 : le **coffre-fort des phrases
maîtresses** — conteneur chiffré TRIADE-CF1 centralisant toutes les phrases maîtresses
par projet, sur la pile cryptographique de la carte au repos (Argon2id aux planchers,
HKDF à contexte dédié, XChaCha20-Poly1305), doté d'un autotest de falsification et de
règles d'export/import (§ 17.3, FORMAT_CARTE § 11) ; l'état des jalons est constaté —
M3 franchi le 28 octobre 2026 sur la campagne million (D72), la conformité permanente
(D73) et le scellage de la balise finale 0.4.0 (D74) ; le modèle de menace gagne la ligne
du vol du coffre-fort (§ 15.1). Aucune règle n'est modifiée ; aucune couche n'est ajoutée
à l'exécution ; la hiérarchie de la fonction objectif est inchangée.

### 1.6 Ce que change la v0.5.2

Une évolution de discipline, tracée dans la correspondance (§ 19.6) et le journal des
versions (§ 21), rattachée à la décision D81 puis AMENDÉE par D223 : **la phrase de
contrôle vit sous séquestre à seuil depuis le 19 novembre 2026** — répartie en CINQ
parts à seuil TROIS, AUCUNE phrase en clair au dépôt git ni au coffre Drive, la
cérémonie de reconstitution à froid de trois parts l'unique voie de survie (le refus
nommé D223 garde la ligne) ; l'affichage unique de cérémonie (D27/D30) n'est jamais
le canal de survie. (L'histoire D81 — la phrase au fichier-remise
`PHRASE-CONTROLE-COFFRE.txt` au dépôt et au coffre Drive, sauvegardée avant toute
autre action — est DATÉE : du 4 au 19 novembre 2026, amendée par D223, jamais un
geste courant.) Le constat fondateur : la rotation D80 avait produit une
phrase neuve dont la remise prévue en fin de tour n'a jamais eu lieu — la session
d'exécution est morte avant (pannes d'infrastructure récurrentes, quatre réinitialisations
et une interruption de session déjà consignées) — et la phrase ne vivait plus que dans le
bac à sable éphémère : un décès d'infra de plus et le coffre entier devenait
indéchiffrable à jamais. L'arbitrage est consigné : le risque de PERTE (vécu, répété) est
jugé supérieur au risque d'EXPOSITION (URL non devinable) ; le modèle de menace (§ 15.1)
en tire la conséquence honnête — la confidentialité des phrases au repos repose désormais
sur le contrôle d'accès au dossier du coffre Drive, la mitigation première devient la
restriction du partage par lien, et une phrase entrée dans l'historique git y demeure à
vie : on ne compte plus sur sa confidentialité, la rotation reste le remède. Aucune règle
n'est modifiée ; aucune couche n'est ajoutée à l'exécution ; la hiérarchie de la fonction
objectif est inchangée.

### 1.7 Ce que change la v0.6.0

La révision de génération attendue par le plan : le **programme de souveraineté
cryptographique est accompli et prouvé sur terrain** — décision de passation D133,
arbitrage du développeur. Trois axes livrés (§ 12) : l'**axe 2** (D86) — le coffre CF2 à
clé maîtresse répartie par Shamir, cinq gardes seuil trois, sentinelle à double seuil
puis PORTE D120 ; l'**axe 3** (D87) — le sceau de l'Intention : dix arbres de couche I
signés par la clé Ed25519 hors-ligne du développeur, gardes de build et de patch ;
l'**axe 4** (D121, né du terrain) — le coffre CF3 : la serrure à triple scellement, le
piège sur média séparé, la sentinelle instantanée *par invocation* et le cycle en deux
actes. L'**axe 1** (D85, attestation TEE) demeure une exigence consignée :
l'infrastructure sans racine de confiance matérielle ne peut pas la satisfaire et le
dit. La **chaîne réelle du coffre** a migré sur le terrain du développeur les 30–31
octobre 2026 — CF1 vérifié INTÈGRE, phrase de contrôle changée (D110), CF2 migré (cinq
gardes, seuil 3, trois copies hors-ligne), CF3 migré (époque 1, checksum `0cc89a96`),
verdict à froid VERT deux fois — les cérémonies étant conduites par le maître de
cérémonie graphique (D107–D118) avec le kit Drive tenu identique au miroir par
construction (D130) : le détail vit au § 13. Un **coffre neuf naissait CF3** :
`init` direct à l'époque 1 — la chaîne de migration est l'histoire du coffre réel, pas
un rite obligé (la v0.6.1 remet ce choix au développeur — § 1.8, § 12.5). Un document complémentaire, le *Livre du Coffre* (même date, même
dépôt), porte la posture opératoire du maître : cérémonies pas à pas, runbook, mode
dégradé. Aucune règle du cœur n'est modifiée ; aucune couche n'est ajoutée à
l'exécution ; la hiérarchie de la fonction objectif est inchangée.

### 1.8 Ce que change la v0.6.1

Une seule règle, explicitement invalidée et remplacée (§ 19.8) : le niveau de
sécurité d'un coffre neuf. La v0.6.0 (D133) l'avait fixé — un coffre neuf naît CF3,
`init` direct à l'époque 1 ; la v0.6.1 (D137) en fait **l'arbitrage du développeur au
moment de créer son projet de développement** : CF1, CF2 ou CF3, chacun avec son acte
de naissance, ses obligations et son guide (§ 12.5) — imposer CF3 par défaut risque
d'être trop contraignant selon le projet : média du piège à produire dès le premier
jour, cycle en deux actes à chaque session, sachet physique à tenir — la contrainte se
justifie quand le secret la mérite. La chaîne de migration CF1 → CF2 → CF3 demeure
disponible à tout moment pour un coffre dont les besoins grandissent ; le coffre réel
de TRIADE reste CF3 (époque 1, checksum `0cc89a96`). Aucune autre règle n'est
modifiée ; aucune couche n'est ajoutée à l'exécution ; la hiérarchie de la fonction
objectif est inchangée.

### 1.9 Ce que change la v0.7.0

La révision de consolidation du programme d'après M7 (D160) : ce que la clôture de la
v0.6.1 tenait « hors périmètre courant » entre dans la spécification, sur résultats
mesurés — la clause est levée NOMMÉMENT pour les deux premières familles, les profils
additionnels demeurent hors périmètre. Le **jalon M8** (le bloc optionnel de
syscalls directs — le domaine `sys`) est franchi : la charte à huit règles (le SSN
est une donnée, jamais un octet de code ; le motif du stub vérifié avant toute
extraction ; un stub divergent est un refus nommé — le résolveur ne devine jamais,
il ne s'adapte jamais en silence), les spécifications sys-01…03 écrites-avant-code,
le harnais différentiel 61 contrôles verts sur fixtures ntdll synthétiques (le
laboratoire ne connaît jamais le SSN du terrain), la cérémonie de l'ère passée avant
le build (12 arbres, D162/D163), le run terrain sur le VRAI ntdll — la twin de la
ligne hello-02 par les DEUX chemins (l'IAT kernel32 et le syscall direct
NtWriteFile), le refus -4 nommé du stub crocheté — recoupé 30/30 sur pièces
croisées, la finale `0.9.0` scellée (Entrée 164, D165 : le scellage exige le verdict
du recoup comme pièce ; le scellage est un fait de carte, l'artefact ne bouge
jamais). Le **jalon M9** (TLS 1.3 pur en blocs scellés — le domaine `tls13`, l'ère
1.0.0) est ouvert (D166) : la couche I complète — 28 spécifications en six familles
(sha, hkdf, x25519, aead, enregistrement, poignée, principal), l'instrument
`verifier_specs_m9a.py` 117 contrôles verts (D167) — et la cérémonie de l'ère passée
le 05/11 : la remise du développeur, TREIZE arbres signés hors ligne à la clé du
04/11 (la continuité prouvée par le déterminisme Ed25519, D163 : les onze arbres
inchangés rendent les signatures de l'ère M8), le garde repassé VERT 13/13 — la
dette D166 soldée sur pièces. Le **sceau de l'Intention** porte désormais treize
arbres (§ 12.4) et les cérémonies d'ère entrent au protocole (§ 13.5) : la dette se
nomme à la naissance, jamais après coup (D166, règle 8) ; la charge se prépare au
geste qui sert la main du développeur (D168). Aucune règle du cœur n'est modifiée ;
aucune couche n'est ajoutée à l'exécution ; la hiérarchie de la fonction objectif
est inchangée.

### 1.10 Ce que change la v0.9.0

La révision de consolidation du programme d'après M10 (D178/D179). Le **jalon M10**
(le test grandeur nature — le domaine `loupe`) est **franchi** : l'application
« Loupe », l'éditeur hexadécimal au panneau d'empreintes, est NÉE ENTIÈREMENT DE
LA MÉTHODE — la cérémonie d'ère passée sur pièces (le garde à QUATORZE arbres,
la dette D166/D171 soldée), la couche I de 18 spécifications écrites-avant-code
(D172), les QUATRE chantiers de notation (D173–D175 : les 18 blocs
NOTÉS-MESURÉS-PROUVÉS, 159 contrôles verts aux trois graines), le kit déployé au
coffre `/test` (M10-(d)) — ET ONZE RUNS TERRAIN (M10-(e), Entrées 202–219) :
ONZE DÉFAUTS NOMMÉS, ONZE RETOUCHES DOCUMENTÉES — les refus du chargeur
(l'enveloppe prouvée de la lignée NORME DE FAIT), [CADRE-NÉ] (l'initialiseur
`.data` MIROIR EXACT du `CADRE_VIERGE` du harnais — LE GARDE GUÉRI : le contrôle
dérive du plan, jamais de la pièce qu'il contrôle), la classe des arguments pile
(l'audit d'ABI msx64 NÉ AU BUILD), [SESSION] -7 VERROUILLÉ (L'OMBRE au kit,
l'artefact acquitté), [HINSTANCE-PEB] (l'entrée réécrite : r12 =
GetModuleHandleW(NULL) LE VRAI MODULE), [D54-QUATRIÈME] + [EAX-SANS-SIGNE]
(l'IAT relogée à 0x3100 en QUATRE plages séparées par NULL, les 20 rendus
négatifs étendus au 64 bits), [OFT-QWORD] (les QUATRE OFT au pas DWORD du
chargeur — la sixième mort NOMMÉE par le journal d'événements [4/4]),
[FREE-SANS-TYPE] (le HMODULE en POINTEUR, l'essai isolé pour TOUTE classe
d'exception), [RET-NU] (`mov eax, 1 ; ret` — le verdict ATTACH VRAI PAR
CONSTRUCTION), [SONDE-EXE] (le faux négatif STRUCTUREL de la sonde de liaison :
le chargeur de bibliothèque ne résout JAMAIS les imports d'un module exécutable —
LA LIAISON PROUVÉE PAR LE VIVANT) — ET LA VITRINE A VÉCU (0 et 0 aux dixième et
onzième runs : L'APPLICATION NÉE DE TRIADE A VÉCU CHEZ SON UTILISATEUR). LE
ONZIÈME RUN recoupé 39/39 : **LA BALISE `loupe 0.1.0` SCELLÉE PAR FAIT DE
CARTE** (D178 : la dette de la carte soldée par la RÉGÉNÉRATION DES NOTATIONS —
18/18 notations == la pièce OCTET POUR OCTET, l'écart de l'audit 587 → 0 ; la
cristallisation 26 × 10/10 ; la re-signature à la graine durable D144 — LE
TÉMOIN NE BOUGE PAS ; l'anti-rollback ARMÉ ; loupe.exe INTACT 054de960… — LE
MÊME binaire que le run a couru) : **LA MÉTHODE TRIADE ENTIÈRE PROUVÉE PAR LA
CRÉATION — de l'intention (la couche I) à l'octet vécu chez son utilisateur**.
LE PROGRAMME D'APRÈS M10 APPARTIENT AU DÉVELOPPEUR : la version `0.1.1-dev.1`
est COMMANDÉE (D179) — la dette [R10-PÉRIMÉE] (les 17 sommes de l'ère dev.5 que
les retouches des Entrées 210/214 changèrent sans rafraîchir la table) SOLDÉE À
LA NAISSANCE : la pièce naît de LA RECOMPOSITION même (chaque somme == son bloc
relu, par construction), le qword version porté 0x00010101, 0 OCTET AILLEURS —
le code BYTE-IDENTIQUE au vécu des onze runs (R4 : le contrat stable ; R7 : les
adresses intactes), la carte GÉNÉRATION 17 ; le kit 0.1.1-dev.1 DÉPOSÉ au
coffre `/test` (loupe-kit-13, le réceptacle ARMÉ) — LE DOUZIÈME RUN ATTENDU :
si le vert tient (le scénario ENTIER T0 → S0 → LA LIAISON ET la vitrine
vivante), LA BALISE `loupe 0.1.1` SCELLÉE sur run terrain recoupé (le miroir
D165/D170 : la porte est de processus). Le projet fils COFFRE-FORT demeure
dégelable au rythme du développeur (D135 amendée par D171) : la frontière
fondatrice demeure INTACTE. Aucune règle du cœur n'est modifiée ; aucune couche
n'est ajoutée à l'exécution ; la hiérarchie de la fonction objectif est
inchangée.


### 1.11 Ce que change la v0.10.0

La révision de **l'édition académique** (D182, la commande du développeur du 11/11).
La présente révision **consigne** ; elle ne modifie AUCUNE règle, n'ajoute AUCUNE
couche d'exécution, laisse la hiérarchie de la fonction objectif inchangée — le
modèle D180 : le protocole consigne, il ne légifère pas.

**Le manuscrit académique** (`docs/TRIADE_manuscrit_v0.10.0.pdf`, la chaîne
`scripts/manuscrit_v100/`) : une édition IMRAD en anglais (résumé français inclus),
structurée autour de quatre questions de recherche — le taux de défauts échappés
(onze classes nommées sur douze runs terrain du TGN « Loupe »), le coût en tokens
par changement validé (51 / 719 / 1 088 mesurés M1, D31/D34), les classes de
défauts invisibles à l'émulation (cinq familles : chargeur/image, ABI/SSE,
sémantique du chargeur de bibliothèque, conventions de codes d'erreur, hypothèses
du harnais), la sûreté du patch à chaud (zéro régression post-patch, monotonie
signée, anti-rollback armé). L'auteur humain est unique ; l'agent IA est décrit en
méthodes et remerciements, jamais co-auteur. Les déclarations Ethics/dual-use
(outil de pentest autorisé — le projet ne porte AUCUN mécanisme de furtivité),
Data Availability (dépôt + DOI Zenodo à créer au dépôt), Limitations (N=1,
circularité de l'oracle, absence de baseline, sécurité mémoire non prouvée, temps
constant non analysé) sont explicites. Chaque donnée du manuscrit est GÉNÉRÉE
depuis le journal par `scripts/extraire_donnees_v100.py` — le manuscrit n'affirme
rien qui ne soit extrait et vérifié.

**La formulation corrigée** : « le compilateur disparaît » devient « aucune chaîne
de traduction optimisante ni opaque ; assemblage WYSIWYG vérifié par round-trip » ;
« code volé inexploitable » devient « l'évolution du code volé est bloquée, son
exécution ne l'est pas » ; les majuscules emphatiques et le vocabulaire
sacralisant cèdent aux termes standards (key ceremony, signed manifest, sealed
build) ; l'invariant D19 (Sécurité > Performance > Optimisation > Coût en tokens)
est requalifié **politique de projet explicite** — la hiérarchie demeure la règle
du projet, dite dans les termes de l'ingénierie.

**La proposition D183** (documentée, NON appliquée au coffre réel) : le séquestre
chiffré de la phrase de contrôle — l'alternative à la garde durable D81 (la phrase
en clair au dépôt et au coffre Drive, l'arbitrage PERTE > EXPOSITION). La
proposition : la phrase chiffrée vers une clé hors-ligne, ou partagée en parts
Shamir à seuil, la phrase en clair retirée du dépôt. L'analyse comparative
chiffrée des risques perte/exposition vit dans la décision D183. Le coffre réel
du développeur DEMEURE à la garde D81 — aucune clé touchée, aucun conteneur
réécrit : la proposition attend le geste du développeur.

**L'annexe A portée à sha-256** (D184) : les empreintes de gouvernance de l'annexe
A (les modules du coffre) passent de md5 à sha-256 — la même méthode au contenu
canonique LF, l'empreinte longue. md5 demeure UNIQUEMENT une fonctionnalité
d'affichage de Loupe (le panneau d'empreintes, loupe-06) : AUCUN octet de la
pièce ne change, et les empreintes md5 des preuves historiques (le journal, les
archives) demeurent ce qu'elles sont — les preuves ne se réécrivent jamais.

**Les livrables** : `TRIADE_soumission_v0.10.0.zip` (cinq fichiers au plus,
readme inclus, le manuscrit en pdf — prêt pour un comité de révision) et
`TRIADE_complet_v0.10.0.zip` (l'intégralité : sources LaTeX, bibliographie,
tableaux de données, script d'extraction, extraits de journal, empreintes). La
v0.9.0 demeure : ses sources et son PDF archivés à `docs/`, la chaîne
`spec_v090` intacte — chaque édition vit à sa chaîne.


### 1.12 Ce que change la v0.11.0

La révision des **preuves renforcées** (D185/D186). AUCUNE règle modifiée,
aucune couche d'exécution ajoutée, hiérarchie inchangée — les instruments
nouveaux vivent AU LABORATOIRE uniquement (l'exigence de la commande), aucun
artefact scellé ne bouge, aucun arbre signé ne bouge.

**Les six instruments** (`scripts/preuves_v110/`, graines consignées,
reproductibles) : (1) LE MUTATION TESTING — 832 mutants d'un octet, tués
par les instruments existants dans l'ordre du coût : 694/832 (83,4 %), les
familles crypto à 100 %, les 138 survivants des blocs d'orchestration
NOMMÉS ; (2) LE FUZZING GUIDÉ PAR COUVERTURE — loupe-01 (le chemin non
fiable, l'OS virtuel, les canaris) : 60,5 % de couverture, zéro crash,
zéro violation ; http-10 : 358 instructions, zéro faute ; (3) LA SÛRETÉ
MÉMOIRE STATIQUE BORNÉE — 2 098 accès classés, 1 181 vérifiés au cadre
(zéro hors-cadre : la classe du stack-smash absente), 463 non résolus
nommés, les limites consignées ; (4) LE TEMPS CONSTANT — le dudect
d'émulation : les familles crypto CONSTANTES (traces indépendantes du
secret), le temps réel NON MESURÉ (la limite explicite) ; (5) LES
BENCHMARKS — la référence C à contrat équivalent (gcc -O2/-Os, clang
absent : l'écart nommé), le même émulateur : sha256 4 524 instructions/op
contre 69 132 (facteur 15,3) pour 765 o contre 5 436 ; md5/aes ÉCARTÉS par
l'auto-vérification de l'instrument (le C fautif refusé : jamais un
chiffre faux) ; (6) L'INDÉPENDANCE DE L'ORACLE — les voies distinctes
(dérivation décimale, os.urandom, tripartite spec ↔ harnais ↔ hashlib) :
zéro divergence.

**La spécification CSPRNG (D186)** : la couche I manquante comblée au
laboratoire — le brouillon `tls13/notation/brouillons/tls13-29-source-csprng.md`
(le générateur = le CSPRNG de l'OS hôte via le kit, le reseed = la
politique du noyau, l'échec fail-closed, le KIT96 seule interface) ;
l'entrée à l'arbre signé EXIGE la cérémonie d'ère du développeur (le
quinzième arbre, le modèle D177).

**Les vecteurs RFC 8446** (`tls13/fixtures/rfc8446.py`) : les constantes
normatives natives (sentinelles DOWNGRD, valeur magique HRR, types
d'enregistrement, suite, groupe) au corpus de fixtures partagées — le plan
recroisé (SUITE, GROUPE, HRR conformes).

**Le manuscrit v0.11.0** : la section Results étendue (§ 4.5 — les six
instruments, la table générée depuis les preuves), les limites mises à
jour (la sûreté mémoire BORNÉE pas prouvée, le temps constant STRUCTUREL
pas réel, la réplication par second agent à venir).


### 1.13 Ce que change la v0.12.0

La révision du **modèle formel et de la gouvernance assainie** (D187/D188/D189,
le troisième fichier d'instruction). Aucune règle modifiée, aucune couche
d'exécution ajoutée, hiérarchie inchangée.

**Le modèle formel de CF3** (`scripts/modele_formel_v120.py`, le script EST le
modèle — reproductible) : la chaîne du coffre scellé en machine à états
explicite, l'exploration EXHAUSTIVE (154 états, 1 152 transitions, époques ≤ 3,
adversaire à seuil ≤ 2 éléments avec rejeu d'époques passées) — P1 le secret
sous seuil, P2 le refus du roll-back (la monotonie structurelle constatée
mécaniquement), P3 l'absence de destruction sur phrase erronée, P4 le rayon
borné à une époque : **les quatre PROUVÉES DANS LE MODÈLE** ; les hypothèses
A1-A5 explicites (le modèle symbolique, le seuil, le média, les anciens
couples, le HORS MODÈLE : canaux auxiliaires, implémentation, trois éléments,
quantique) ; le vérificateur NOMMÉ (Tamarin/ProVerif absents — l'explorateur
d'états tient la place).

**Le modèle de menace en deux plans** (D188) : le plan IP (la propriété
intellectuelle — la confidentialité d'abord, les pertes REMÉDIABLES) et le plan
sûreté d'exécution (la corruption, le rollback, l'environnement — l'intégrité
et la disponibilité d'abord, les pertes IRRÉMÉDIABLES) ; **l'ordre
intra-sécurité explicite** (la politique de projet : quand les deux plans se
rencontrent, le plan sûreté GAGNE — un coffre cassé ne protège rien) ; la
tension D81 ↔ D183 consignée avec l'analyse chiffrée (facteur ≈ 40 en faveur
du séquestre Shamir — D81 DEMEURE, le geste appartient au développeur).

**La cristallisation évaluée** (D189) : le seuil de 10 rebuilds analysé comme
test séquentiel (SPRT : 5 rebuilds identiques atteignent α = 5 %, le seuil 10
atteint α = 1,08 × 10⁻³ — 46× plus strict) ; **le seuil demeure 10** (la
politique de projet, jamais changée en silence) ; le protocole de réplication
proposé (`scripts/preuves_v120/protocole_replication.md` : les trois axes —
second développeur, second domaine, second profil — la grille T/X à double
annotation, le κ de Cohen ≥ 0,61, les critères pré-enregistrés) — proposé,
jamais exécuté.

**Les manifestes de kit à sha256** (D187) : le manifeste du kit de cérémonie
consigne désormais sha256 (la suite de la migration D184) ; les kits déjà
livrés demeurent (leurs manifestes md5 sont des preuves) ; md5 demeure à
l'idempotence Drive et à l'affichage Loupe.

### 1.14 Ce que change la v0.13.0

La révision des **corrections de l'édition** (D190/D191/D192, le quatrième
fichier d'instructions). Aucune règle modifiée, aucune couche d'exécution
ajoutée, aucun artefact scellé touché — l'édition CORRIGE les documents,
elle ne légifère pas (le modèle D180/D182).

**Les incohérences corrigées** (la liste de la commande, vérifiée une à une,
le rapport de conformité joint aux livrables) : les quatorze arbres signés
(cohérence avec le garde 14/14) ; la référence au manuscrit accompagnant
portée v0.13.0 ; le compte de lignes du journal UNIFIÉ en valeur exacte
extraite (macros générées — jamais un arrondi) ; « Fig. 5 » devient
« Table 5 » ; la Data Availability portée aux archives v0.13.0 ; la Table 6
des preuves RÉGÉNÉRÉE intégralement en anglais par le générateur
**anti-troncature** (aucune cellule jamais coupée, chaque ligne PARSÉE
depuis les sorties brutes) ; la note TOTAL/brouillons au tableau des
budgets (8 774 + 5 099 = 13 873, les brouillons exclus) ; le paragraphe de
consolidation du § 1.10 aligné sur D181 (douze runs, la balise
`loupe 0.1.1` scellée) ; le tableau de menaces (« le code volé est
inexploitable » devient « l'évolution du code volé est bloquée, son
exécution ne l'est pas ») ; les renvois au manuscrit recalés (§ 3.5 les
preuves renforcées, § 4.1 le modèle formel).

**Les statistiques reformulées** (D190) : la cristallisation — les
caractéristiques opérationnelles P(sceller|q) = (1−q)ⁿ (à q = 50 % :
3,1 % à n=5, 0,098 % à n=10, soit 32× plus strict ; les quantiles
unilatéraux exacts 1,87σ/3,10σ) remplacent les « α = 3,29·10⁻² /
1,08·10⁻³ » de D189 (des rapports de vraisemblance (0,5/0,99)ⁿ mal
étiquetés) ; l'IC95 % EXACT de 11/12 (Clopper-Pearson [0,615 ; 0,998],
la réserve de non-indépendance des itérations séquentielles) ; la règle
de comptage opérationnelle des défauts échappés DÉFINIE en méthodes du
manuscrit (les runs 6/7 à deux défauts comptés une fois chacun ; le
résidu [T0-PÉRIMÉ] du run 12 divulgué, non compté — et pourquoi).

**La neutralité documentaire** (D190) : l'anti-debug léger par mesure de
temps documenté honnêtement dans les deux documents (la portée : la
dissuasion, jamais la résistance) ; la conséquence D81 ajoutée au modèle
de menace (deux éléments trivialement disponibles, le média piège seul
rempart de confidentialité) ; la frontière D105/D81 du clone du
laboratoire (clones temporaires à phrases de test) ; le kit de la
cérémonie D183 préparé sans l'appliquer.

**Le benchmark audité** (D191) : le facteur 15,3 retiré — l'artefact de
périmètre nommé et rejoué sur pièces ; les chiffres corrigés (75 983
contre 69 132 / 77 505), la parité d'extensions ISA au baseline constatée,
le terrain M7 requalifié (qemu TCG, fence.i non prouvé sur silicium).

**L'état de l'art étendu** (D192) : huit références vérifiées DOI/arXiv ;
la revendication « first quantified account » scopée ; RQ3 recadrée en
garanties silencieuses du compilateur.

### 1.15 Ce que change la v0.14.0

La révision du **programme empirique** (D193/D194/D195, le cinquième
fichier d'instructions). Aucune règle modifiée, aucun artefact scellé
touché — les affirmations du manuscrit passent aux mesures contrôlées.

**Le pré-enregistrement** (D193) : le plan de comparaison (H1-H4,
CA1-CA5, les six blocs, les vecteurs) consigné AVANT toute mesure,
empreinte verrouillée.

**Le bras de référence** (D195) : six blocs C depuis les mêmes contrats,
les mêmes shims, auto-vérifiés — ZÉRO DIVERGENCE aux vecteurs ;
sha-256 paritaire à travail égal (9 089/9 146 — l'héritage PAR LA
CARTE) ; les purs plus chers à la notation ; la mutation au même degré.

**La re-mesure RQ2** : les distributions de bout en bout (580/2 143/
3 510 de médiane, la baseline naive 300 304, le raisonnement estimé
NOMMÉ) — les valeurs M1 historiques, la lecture défavorable consignée.

**L'indépendance** : l'instance isolée (128 constantes, zéro
divergence) ; l'écart de famille nommé ; la voie entière exacte.

**Le re-jeu des survivants** : 776/832 (93,3 %) aux
composition-killers — tls13/sys à 100 %, les 56 loupe nommés.

**Le kit terrain** (`scripts/kit_terrain_bras_c/`) : EN ATTENTE.

### 1.16 Ce que change la v0.15.0

LES PREUVES NON BORNÉES ET LE RAFFINEMENT (le sixième fichier
d'instructions, ic09ydeli sous son vrai nom — le croisement
d'attribution d'hier RECROUPÉ et CORRIGÉ, D197). AUCUNE règle du cœur
modifiée, AUCUNE couche d'exécution ajoutée, AUCUN artefact scellé
touché.

**La déviation constatée** : Tamarin ET ProVerif demeurent ABSENTS du
laboratoire (constat re-vérifié au geste) — la route consignée à D196
est suivie : la preuve par INVARIANT INDUCTIF dans l'explorateur.

**L'invariant inductif** (`scripts/preuves_v150/modele_invariant_v150.py`) :
le plafond d'époque de l'explorateur v0.12.0 (un artefact d'exploration,
jamais du design — l'implémentation fait e ← e+1 sans borne) est RETIRÉ ;
l'invariant I (I1 secret ⟹ seuil = 3 ; I2 aucune destruction injuste ;
I3 média du piège et fragments CF2 intacts ; I4 époque ≥ 1) est
initialisé, PRÉSERVÉ par chacune des 13 règles sur l'ensemble FINI des
formes d'état (288 formes, les deux classes d'époque {1} et {≥ 2}),
l'uniformité témoignée par translations δ ∈ {7, 50, 1000} aux verdicts
IDENTIQUES ; la monotonie vérifiée INCONDITIONNELLEMENT (4 096 formes,
zéro décroissance) ; le rejeu retourne l'état inchangé. **P1-P4 SONT
PROUVÉES NON BORNÉES** (toute époque, toute profondeur, sous A1-A4 ;
A5 hors modèle nommé). La FIDÉLITÉ : D187 reproduit EXACTEMENT (154
états / 1 152 transitions) ; les bornes étendues (époques ≤ 5 prof 8 :
228/1 902 ; époques ≤ 7 prof 12 : 372/3 342) trouvent ZÉRO état hors
de I — la preuve bornée CONFIRME la preuve non bornée.

**Le raffinement** (`scripts/preuves_v150/raffinement_v150.py`) :
chaque règle abstraite REJOUÉE contre l'implémentation Python (coffre
de TEST à phrase publique marquée, D192) : le cycle honnête sur CINQ
époques VÉCUES aux deux niveaux, la phrase erronée aux deux actes
(quinze essais, zéro destruction), la falsification du conteneur (une
destruction LOCALE, un PV, le média intact), la falsification du piège
(refus nommé, rien détruit), le rejeu d'époque passée en TROIS
variantes, le piège absent (IMPOSSIBLE, pas refusé), le piège d'un
autre coffre, l'adversaire sous le seuil (32 moitiés forgées, zéro
passage) : **34 pas, ZÉRO ÉCART** — les chemins d'échec inclus ; trois
gestes hors modèle consignés comme tels.

**Les trois kits de mesure matérielle** (`scripts/kits_mesure_v150/`) :
le dudect temps réel (quatre cibles extraites de la pièce scellée,
l'appel natif VALIDÉ au vecteur FIPS « abc », le mesureur C double
backend dont l'autotest POSIX n'éprouve que le mécanisme), le fence.i
sur silicium (le scénario M7, la cible changée), le terrain tiers Loupe
(T0→T7+S0 intégral) — TOUS **EN ATTENTE DE RUN MATÉRIEL** : aucun
chiffre n'existe, aucun n'est fabriqué.

**La réplication** (`scripts/replication_v150/`) : la grille T/X
FINALISÉE (définitions opérationnelles, exemples vécus), le
calculateur κ de Cohen AUTOTESTÉ (trois cas synthétiques au κ
calculable à la main), les critères pré-enregistrés D189 INCHANGÉS ;
le second annotateur À RECRUTER, le second domaine EN ATTENTE d'une
vraie commande — les statuts consignés.

**Les statuts systématiques** (la commande, point 4) : chaque
affiliation de preuve porte son statut — *prouvé non borné* / *prouvé
borné* / *en attente de run matériel* — la table générée depuis les
pièces (`scripts/statuts_preuves_v150.py`), AUCUNE revendication
matérielle tant que le run n'est pas recoupé.

**La dette documentaire guérie** : la table des preuves du manuscrit
(29 lignes en v0.13.0/v0.14.0) n'était JAMAIS RENDUE — le flot
dépassait la page et LaTeX le rejetait silencieusement : la table
devient LONGTABLE, les 34 lignes sont rendues.

**La gouvernance** (D197) : le croisement d'attribution des
instructions n°5/n°6 recoupé aux métadonnées Drive et corrigé aux
gestes (ysddxpk0o archivé, ic09ydeli rappelé vers /instructions) ; LA
RÈGLE DU CONTENU CITÉ (à l'ouverture de toute instruction : lecture
intégrale, empreinte confrontée, le contenu cité à l'entrée
d'ouverture) ; LA RÈGLE DU DÉVELOPPEUR (12/11) : à chaque livraison
d'une nouvelle version d'un document, les anciennes versions sont
archivées (racine → /ARCHIVE, déplacement vérifié).

## 2. La couche I : format normalisé des spécifications

La v0.3 décrivait la couche I comme « contrats légers : signatures typées, pré et
post-conditions, invariants » (D3), sans en fixer le gabarit — la légèreté demeure, la
structure devient normative (D19). Une spécification I n'est pas un document libre :
c'est un artefact diffable dont la structure conditionne la vérification. La démonstration
RoomEq en a fixé la pratique (44 spécifications, une par module, écrites avant le code) ;
la v0.4.0 en fait la règle.

### 2.1 Identifiants stables

Chaque spécification reçoit à sa création un identifiant `<DOM>-<NN>` : un domaine parmi
une liste figée par projet (dsp, eq, calibration, audio, io, app, installateur, securite,
outils…) et un numéro séquentiel à deux chiffres. L'identifiant est immuable et jamais
réutilisé ; un module supprimé laisse son identifiant vacant à jamais. C'est l'équivalent
exact, côté intention, de l'adresse stable côté binaire (R7) : les références croisées —
dépendances, carte, tests — ne cassent jamais. Le couple (identifiant, révision) est la
clé de traçabilité du § 4.2.

### 2.2 Gabarit obligatoire

```
<DOM>-<NN> · <nom court> · révision <R>
Intention : <une phrase — le pourquoi>
Contrat :
  pre  : P1…Pn    (préconditions numérotées, une phrase chacune)
  post : Q1…Qn    (postconditions numérotées)
  inv  : I1…In    (invariants)
Échecs :
  E1 : <condition> → <sanction nommée : exception | arrêt propre | repli documenté>
Vecteurs :
  V1 : <vecteur doré | propriété différentielle | test de rejet>
Fixtures    : <références aux fixtures contractuelles partagées, le cas échéant>
Provenance  : écrite-avant-code | reverse-spec de <binaire scellé @ tag>
Décisions   : <Dxx…>
```

Sept blocs, tous obligatoires — les échecs et vecteurs ne peuvent être vides que pour un
module sans effet observable, situation rare à justifier dans le champ Intention. Trois
règles de rédaction conditionnent la diffabilité exigée par R2 : **une exigence par phrase
numérotée** (le diff montre exactement quelle exigence change) ; **aucune connaissance
dupliquée** (ce qui est écrit dans une spécification n'est pas réécrit dans une autre —
renvoi par identifiant, sinon défaut T5) ; **chaque pre/post/invariant relie au moins un
vecteur** (une exigence invérifiable est une exigence mal formulée).

La provenance distingue les spécifications écrites avant le code — le cas normal, exigé par
R2 — des reverse-specs (§ 10), extraites de binaires scellés hérités.

### 2.3 Révision et cycle de vie

La révision R s'incrémente à chaque changement du contrat : postcondition modifiée, cas
d'échec ajouté, vecteur étendu. Une évolution qui rompt un contrat existant ne modifie pas
la spécification — elle en crée une nouvelle, l'ancienne étant dépréciée avec renvoi :
miroir exact du cycle de vie des blocs (FORMAT_CARTE § 6). Les appelants dépendent du
couple (identifiant, révision) ; la carte porte ce couple dans chaque entrée.

### 2.4 Fixtures contractuelles partagées

Quand plusieurs consommateurs se lient au même contrat externe — sortie d'un outil système,
format de fichier, API distante — les échantillons qui définissent ce contrat (fixtures)
appartiennent à la spécification, pas aux consommateurs. Le champ Fixtures référence un
jeu unique ; toute copie privée est un défaut de classe T5 (duplication). Le mécanisme est
né dans la démonstration RoomEq : l'installateur scellé et l'application recodée
partagent les fixtures de parsing de pnputil — le défaut historique qui a survécu à trois
versions vivait précisément de la duplication (trois copies divergentes du même contrat
implicite). Le partage élimine par construction la divergence des exemplaires.

## 3. Taxonomie des défauts de contrat non écrit

La classe de défauts que le protocole existe pour éliminer a un nom : **contrat non
écrit**. La v0.4.0 en fixe la taxonomie (D19), née de l'analyse des défauts historiques de
la démonstration RoomEq — défauts d'application et défauts d'installateur confondus.

| Classe | Définition | Détecteur typique | Verrou |
|---|---|---|---|
| T1 — valeur-seuil enfouie | Constante critique sans nom, sans justification, dupliquée ou non | revue ; oracle (comportement absurde sur entrée limite) | constante nommée + rationale dans la spec I |
| T2 — convention d'interface implicite | Structure ou ABI déclarée de mémoire, hors contrat | échec système nommé à l'exécution | contrat typé + invariant de taille testé |
| T3 — dépendance à l'hôte | Comportement dépendant de l'OS ou des paramètres d'exécution | tests multi-plateformes | contrat indépendant de l'hôte, union fixée |
| T4 — parsing de surface fragile | Analyse de libellés localisés ou volatils | fixtures multi-langues | fragments indépendants des libellés + fixtures partagées |
| T5 — contrat dupliqué | Même connaissance codée en N exemplaires qui divergent | diff des exemplaires | source unique : spec I + fixtures |
| T6 — garantie non testée | Comportement critique sans vecteur de rejet | revue de couverture des vecteurs | cas d'échec nommé + test de rejet |

Deux règles d'usage. D'abord, tout défaut corrigé est **classé dans cette taxonomie** au
journal des décisions du projet — la métrique « défauts ouverts par classe » du tableau de
bord (§ 17.2) en dérive. Ensuite, la taxonomie sert de liste de contrôle de rédaction :
chaque bloc du gabarit § 2.2 verrouille au moins une classe (Échecs verrouille T6, Fixtures
verrouille T4/T5, le contrat typé verrouille T1/T2/T3).

La démonstration fournit les occurrences de référence : le seuil de détection 8 non justifié
est T1 + T6 (le bruit seul passait) ; la structure `SP_DEVINFO_DATA` de 424 octets au lieu
de 32 est T2 (échec 0x6F8, deux copies) ; la sanitisation de noms de fichiers dépendante de
l'OS hôte est T3 ; le parsing de pnputil sur libellés français est T4 + T5 (trois copies) ;
le seuil dupliqué dans le message d'erreur est T5. Chacun est devenu un contrat nommé, un
cas d'échec et un test — la conversion est documentée dans la démonstration et sa méthode
est désormais la règle.

## 4. Architecture : les trois couches

L'architecture repose sur une séparation stricte entre ce que l'artefact contient, ce que
l'agent manipule et ce que le destinataire reçoit. Le diff d'intention descend de I vers C,
le verrou croisé relie C et B dans les deux sens, et la couche B seule quitte le
laboratoire. **Aucune couche n'est optionnelle** — la v0.4.0 le consigne comme propriété
normative, pas comme constat : privé de I, le système perd son ancrage sémantique ; privé
de C, l'agent devient aveugle ; privé de B, il n'y a plus rien à exécuter. Toute
implémentation qui livrerait B sans I et C à jour viole R1 ; toute évolution qui
contournerait C pour éditer B directement viole R3 et la boucle (§ 7).

### 4.1 Les trois couches

| Couche | Contenu | Visibilité | Rôle |
|---|---|---|---|
| I | Spécifications normalisées (§ 2) : contrats typés pré/post, invariants, cas d'échec, vecteurs de vérification | Privée | Compression de l'intention — le quoi et le pourquoi |
| C | Index des blocs, adresses, signatures, preuves, manifestes de build, traçabilité | Privée, signée, chiffrée | Unique interface de développement de l'agent |
| B | Code machine scellé, padding inter-blocs, checksums runtime | Livrée | Le comment — exécution pure, sémantiquement muette |

Depuis la v0.3, la séparation des couches croise une seconde dimension : la cible. La
couche I est **indépendante de la cible** — un contrat s'écrit une fois, ses types abstraits
(`usize`, alignements) étant paramétrés par le profil. La couche B est **par profil** :
chaque plateforme visée possède son jeu d'octets scellés. La couche C indexe l'ensemble :
chaque entrée porte son profil, et frag-bld organise les empreintes par profil. Un même
contrat I est ainsi instancié par autant de blocs machine que de profils supportés — c'est
la condition de possibilité de la portabilité sans duplication de l'intention.

Quatre invariants structurels, vérifiés à chaque cycle de build — leur violation est un
refus de build : B n'est jamais nu (R1) ; les adresses exposées sont stables (R7, par
profil) ; la signature couvre la carte entière (R9) ; B est auto-vérifiant au chargement
(R10, renforcée en v0.4.0).

### 4.2 Traçabilité I ↔ C ↔ B ↔ tests

La v0.4.0 rend obligatoire une chaîne de traçabilité complète (D24). Chaque entrée de la
carte référence quatre maillons :

| Maillon | Contenu | Porté par |
|---|---|---|
| I | spécification (identifiant + révision) | couche I |
| C | entrée de localisation + contrat embarqué | frag-loc, frag-con |
| B | bloc(s) instancié(s) + empreinte(s) par profil | frag-bld, binaire |
| tests | vecteurs exécutés + verdict du dernier cycle | frag-prf, suites |

Trois propriétés, contrôlées mécaniquement par la **commande d'audit de traçabilité** :
aucune spécification sans entrée de carte (l'exception visible étant la reverse-spec en
statut « prête », § 10) ; aucun bloc scellé sans spécification référencée ; aucun
vecteur orphelin (rattaché à une exigence numérotée du gabarit § 2.2). Une chaîne
incomplète est un refus de build — au même titre qu'un binaire nu. La traçabilité est la
condition de l'audit par des tiers : elle permet de répondre à « quelle exigence ce bloc
implémente-t-il, et quel test la défend ? » sans lecture du binaire.

## 5. La carte (couche C)

La carte est le cœur opérationnel du protocole : c'est elle qui rend le binaire navigable
pour l'agent, qui porte les preuves et qui concentre la valeur intellectuelle du projet.
Elle est compacte (coût en tokens, § 14), intègre (verrou croisé) et résiliente face à la
compromission (sharding et chiffrement). Sa spécification détaillée — en-tête normalisé,
quatre fragments, format d'entrée, procédure du verrou, cycle de vie, budgets, export de
continuité, re-cryptage — fait l'objet de `docs/FORMAT_CARTE.md`, mis à jour avec la
présente révision : l'en-tête porte `version=0.4.0`, chaque entrée de bloc porte le champ
de traçabilité `spec=<DOM>-<NN>:R` exigé par le § 4.2.

La carte est **autodescriptive** : un en-tête normalisé consigne la version du protocole,
la suite cryptographique retenue — `algo_hachage` (SHA-256 par défaut), `algo_signature`
(Ed25519 par défaut), `algo_chiffrement` (XChaCha20-Poly1305 par défaut), chacun modifiable
par le développeur dans les limites d'une liste blanche (D15) — et la liste des profils de
cible actifs. Les empreintes portées par frag-bld sont préfixées par leur algorithme
(`sha256:ab12…`) : n'importe quel agent, présent ou futur, sait vérifier le verrou croisé
sans connaissance extérieure à la carte.

## 6. Règles du protocole v0.4.0

R1 à R7 proviennent de la v0.1 ; R8 à R10 de la v0.2 ; **R10 est renforcée et R11 ajoutée
par la v0.4.0**. Les règles sont peu nombreuses, vérifiables mécaniquement et sanctionnées
par des effets concrets — refus de build, refus de commit ou blocage de session — plutôt
que par des recommandations. Aucune règle existante n'est affaiblie : les énoncés de R1 à
R9 sont repris à l'identique, celui de R10 est un sur-ensemble strict de la version v0.3.

| # | Règle | Énoncé | Violation et sanction |
|---|---|---|---|
| R1 | Jamais de binaire nu | Tout artefact B est accompagné de I et C à jour | Build refusé |
| R2 | Intention d'abord | Toute modification commence par un diff sur I | Édition rejetée par la boucle |
| R3 | Balisage obligatoire | Chaque bloc est décrit dans C | Build refusé |
| R4 | Patch à contrat stable | Le remplacement préserve signature et contrats ; les appelants ne sont jamais invalidés | Échec de vérification |
| R5 | Vérifie-puis-écrit | Aucun commit sans oracle, vecteurs dorés et round-trip | Commit impossible |
| R6 | Cristallisation | Dix vérifications réussies rendent le bloc immuable ; le modifier exige la procédure lourde | Nouvelle version du bloc |
| R7 | Adresses stables | Les points d'entrée sont garantis par padding ; patcher ne déplace rien | Re-liage forcé — interdit |
| R8 | Verrou croisé | Empreintes des blocs et signature de la carte vérifiés avant chaque édition | Session bloquée |
| R9 | Carte signée obligatoire | L'agent refuse toute carte non signée | Refus de démarrage |
| R10 | Échec contrôlé intégré (renforcée) | Au lancement — avant toute entrée dans le chemin d'exécution — l'artefact vérifie (a) les checksums de ses blocs scellés, (b) la signature du manifeste de build couvrant le code et les données embarquées, (c) la monotonie de version (anti-rollback : tout état antérieur à la version minimale acceptée est refusé), (d) la conformité minimale de l'environnement au profil. Tout écart = arrêt propre immédiat ; aucun chemin d'exécution dégradé n'existe (fail-closed explicite) | Arrêt avant tout effet |
| R11 | Optimisation mesurée (nouvelle) | Toute optimisation exige un hot path identifié par mesure, une mesure avant/après consignée au journal d'optimisation (§ 11) et un contrat stable (R4). L'optimisation prématurée — sans hot path identifié ni mesure — est interdite : la demande est refusée et consignée | Refus de commit |

Quatre précisions. R4 signifie qu'un bloc remplaçant honore les contrats publiés de son
prédécesseur — mêmes signatures, mêmes pré et post-conditions, mêmes invariants visibles —
condition de possibilité du patch à chaud. R7 s'entend **par profil** : les adresses sont
stables au sein du binaire de chaque profil ; rien n'impose qu'elles coïncident entre
profils. R1, précisée par D16, interdit de livrer la carte **avec l'artefact** ou à des
tiers — elle n'interdit pas au développeur de détenir, sauvegarder et transférer son propre
état de développement : c'est précisément l'objet de l'export de continuité (FORMAT_CARTE
§ 8). R10 renforcée (D20) étend le fail-closed de la v0.3 — checksums au lancement — en
un contrôle intégré à quatre volets ; la vérification est strictement **locale** (aucune
dépendance réseau au chargement : l'outil doit échouer proprement hors ligne), et la
politique anti-rollback précise (registre des versions acceptées, stockage du plancher)
appartient au profil de cible.

## 7. Boucle de mise à jour

La boucle de mise à jour est la seule voie par laquelle le logiciel évolue. Elle se déroule
en sept étapes réparties en deux phases — l'édition, puis la validation et le commit —
séparées par un point de non-retour : rien n'est écrit dans le binaire avant que l'oracle
n'ait rendu son verdict.

| N | Étape | Entrées | Sorties | Règles |
|---|---|---|---|---|
| 1 | Diff d'intention | Requête de changement, couche I | Diff minimal sur I | R2 |
| 2 | Localisation par intention | frag-loc, diff I | Liste des blocs impactés | R3 |
| 3 | Verrou croisé | frag-bld, binaire | Verdict go / no-go | R8, R9 |
| 4 | Régénération ciblée | frag-con, notation du bloc | Octets candidats | R4, R7, R11 |
| 5 | Vérification | Candidats, oracle, vecteurs dorés | Verdict, journal | R5 |
| 6 | Commit atomique | Verdict favorable | Patch B, carte à jour, scellage | R1 |
| 7 | Cristallisation | Compteur de vérifications | Bloc immuable | R6 |

**Localisation par intention (norme v0.4.0).** L'étape 2 porte désormais son nom entier :
la localisation est **dérivée du diff d'intention** par l'index de la carte — jamais par
balayage du binaire, jamais par recherche de motif dans les octets. Un diff qui ne localise
aucun bloc est une erreur de spécification à corriger dans I, pas une licence de scan ;
un balayage serait d'ailleurs une violation du budget (§ 14) et de R3. C'est la
formalisation du principe « l'agent ne lit jamais le binaire en entier », appliqué à
l'étape la plus fréquente de la boucle. La précision de localisation — bon bloc identifié
du premier coup — reste l'indicateur de santé mesuré dès M0 (cible 95 %).

### 7.1 Patch à chaud — exemple du profil primaire

Le patch à chaud — modifier un logiciel en cours d'exécution — est l'un des deux objectifs
fondateurs du projet avec la performance. Le mécanisme exact est **spécifié par chaque
profil de cible** (taille minimale de bascule atomique, procédure d'invalidation du cache
d'instructions) ; ce paragraphe décrit l'instanciation du profil primaire x86-64. La
méthode contourne la cohérence du cache d'instructions et l'atomicité de la bascule en
n'écrivant jamais un bloc pendant qu'il s'exécute : le nouveau bloc est d'abord écrit dans
une zone de croissance libre ; ensuite, et seulement ensuite, un trampoline est installé à
l'ancien point d'entrée et PUBLIÉ ATOMIQUEMENT — au sens borné que fixe le § 7.1.1 : une
seule écriture alignée de HUIT octets au plus, ou un unique `LOCK CMPXCHG16B` là où le
processeur l'expose. La formulation antérieure (« trampoline de 12 à 16 octets, écriture
alignée unique atomique pour le processeur ») est CORRIGÉE : aucune écriture simple de 12
ni de 16 octets n'est atomique au sens de l'architecture (§ 7.1.1, D253).

```
; trampoline de bascule atomique (aligné sur 16 octets)
; forme courte : saut relatif 32 bits
  E9 xx xx xx xx                ; jmp rel32 -> nouveau bloc
; forme longue : saut absolu 64 bits
  48 B8 xx xx xx xx xx xx xx xx ; mov rax, addr_new
  FF E0                         ; jmp rax
```

L'ancien trampoline est conservé : le rollback copy-on-write de l'étape 5 consiste à
rebasculer vers lui, et la carte référence les deux versions tant que la nouvelle n'a pas
atteint son seuil de cristallisation. Les adresses stables garantissent qu'aucun appelant
ne référence l'intérieur d'un bloc : seuls les points d'entrée — promis par R7 — sont
susceptibles d'être trampolinés, et la table de ces points est close et vérifiée par le
verrou croisé. Le critère de sortie du jalon M2 est précisément ce scénario : remplacer le
bloc d'écho d'un serveur TCP pendant qu'il traite des connexions, sans interruption de
service et avec rollback démontré.

### 7.1.1 Ce que garantit réellement la primitive de publication (D253)

**La distinction qui fonde tout le mécanisme.** Quatre propriétés sont distinctes et ne
s'impliquent pas l'une l'autre : l'**alignement** (l'adresse est un multiple de la taille),
l'**atomicité de l'accès mémoire** (aucun observateur ne voit un état intermédiaire),
la **cohérence des instructions** (le cœur qui exécute voit les octets neufs) et l'**état
des threads** (un thread peut avoir RIP dans la zone remplacée).

**Ce que l'architecture garantit (x86-64, sources primaires).** Une écriture simple n'est
atomique que si elle est naturelle et d'au plus HUIT octets (Intel SDM vol. 3 § 8.1.1) ;
au-delà, aucune garantie d'atomicité n'existe, quand bien même l'adresse serait alignée sur
16. Les seules publications de 16 octets atomiques sont les opérations verrouillées
`LOCK CMPXCHG16B`, disponibles sous CPUID.CMPXCHG16B (absent de certains profils anciens) ;
elles sont des lectures-modifications-écritures verrouillées, pas des magasins. Les magasins
SSE/AVX de 16 octets ne sont PAS architecturalement atomiques. **Conséquence : la
publication doit se faire par un mot de HUIT octets aligné, ou par un `LOCK CMPXCHG16B`
quand il est présent — jamais par l'écriture d'un trampoline de 12 octets « d'un seul
coup ».**

**Le mécanisme retenu, par profil.**

| Profil | Forme publiée | Primitive | Exigences |
|---|---|---|---|
| x86-64 (Windows PE, Linux ELF) | `E9 rel32` + trois `NOP` = un mot de 8 octets aligné sur 8 ; la cible absolue (`48 B8 … FF E0`, 12 octets) n'est écrite QUE dans un emplacement 16 octets aligné publié par `LOCK CMPXCHG16B` | magasin 8 octets naturel, ou `LOCK CMPXCHG16B` | pages en écriture puis exécution (jamais RWX simultané) ; `FlushInstructionCache` (Windows) ou `__builtin___clear_cache` (Linux) après l'écriture ; cible enregistrée au CFG, et IBT/shadow-stack de CET vérifiés avant de trampoliner un prologue |
| RISC-V 64 | instruction de 4 octets alignée sur 4 (ou 2 octets compressé aligné) | magasin 4 octets naturel | `fence.i` sur le hart modifiant ; synchronisation explicite des autres harts (IPI) — aucune cohérence I/D implicite |
| Tout profil | — | — | **quiescence** : aucun thread ne doit avoir RIP dans la plage remplacée au moment de la publication (voir ci-dessous) |

**L'état des threads n'est pas couvert par l'atomicité.** Un thread dont RIP tombe dans
les octets remplacés peut décoder un mélange de l'ancien et du nouveau flux : l'atomicité
du magasin ne le protège pas. La publication est donc conditionnée à un **rendez-vous** :
sur Windows, suspension des threads du processus et lecture de `RIP` par `GetThreadContext`
(refus si l'un tombe dans la plage) ; sur Linux, arrêt par signal et lecture de `RIP` dans
`ucontext` (ou `ptrace` sur un processus fils), avec la même condition de refus. Un thread
immobilisé DANS la plage n'est jamais relancé sur des octets mixtes : il est soit avancé
au-delà (single-step hors de la plage), soit la publication est refusée.

**Les états de la transaction** (aucun état partiellement publié n'est exécutable) :
`0 préparé` (nouveau bloc écrit dans la zone de croissance, hors ligne d'exécution) →
`1 armé` (page de la zone passée en exécution, contenu vérifié par relecture) →
`2 rendez-vous` (threads immobilisés, aucun RIP dans la plage, sinon refus et retour à 0) →
`3 publication` (mot de 8 octets ou `LOCK CMPXCHG16B` unique) →
`4 invalidation` (flush du cache d'instructions, barrière) →
`5 vérification` (relecture des octets publiés, comparaison à l'attendu) →
`6 reprise` (threads relancés) ; `R rollback` depuis 3, 4 ou 5 : republication de l'ancien
trampoline par la même primitive, puis retour à 1. Un échec en 4 ou 5 est un état
**publié-mais-non-vérifié** : il est rollbacké, jamais toléré.

**Cas de refus explicites.** Taille de bascule supérieure au mot atomique disponible sur le
profil ; adresse non alignée sur la taille du mot ; absence de CPUID.CMPXCHG16B quand la
forme longue est demandée ; RIP d'un thread dans la plage et avance impossible ; page non
inscriptible (protection refusée par l'OS) ; cible non enregistrée au CFG sur un processus
protégé ; cache d'instructions non invalidable.

**Statut des preuves.** Les états, les refus et les bornes sont **prouvés au banc**
(`atelier-w17-patch-a-chaud/kit_bascule.py`, autotest incluant les contrôles négatifs) et en
émulation pour la logique d'états — l'émulation NE VALIDE PAS la cohérence du cache
d'instructions, qui n'existe pas dans un émulateur. La bascule concurrente sur matériel réel
(multi-threads, mises à jour concurrentes, rollback, interruption à chaque étape) est
**EN ATTENTE DE RUN MATÉRIEL** (≥ 2 machines) : aucun résultat n'est annoncé.

## 8. Stratégie de vérification

Supprimer le compilateur, c'est perdre les filets de sécurité qu'il tendait gratuitement :
vérification de types, initialisation, analyse de flot. La stratégie de vérification
reconstruit une confiance équivalente — voire supérieure — sans réintroduire de couche de
traduction dans l'artefact. Elle repose sur trois piliers, complétés en v0.4.0 par la
couverture des vecteurs, la suite de conformité par profil et la parité inter-profils
(§ 8.1 à § 8.3), puis en v0.5.0 par la validation terrain normée (§ 8.4) et la taxonomie
des défauts invisibles à l'émulation (§ 8.5).

**L'oracle éphémère** : implémentation de référence de chaque bloc — triviale,
volontairement lente, écrite dans un langage sûr et dérivant directement de la couche I. Il
est généré au début de chaque session, utilisé pour des tests différentiels par propriétés,
puis détruit : jamais livré, jamais archivé dans la carte ; seuls ses vecteurs de test
dorés — hachés — y survivent. Le protocole de test est différentiel : l'oracle et le bloc
machine reçoivent des entrées aléatoires contraintes par les pré-conditions du contrat, et
leurs sorties sont comparées octet par octet. Volume de référence : douze mille cas par
bloc critique. Trois propriétés rendent l'oracle fiable : il dérive de I et non de B (il ne
peut pas hériter d'un bug du code machine) ; il est régénéré à chaque session (jamais en
désaccord avec les contrats courants) ; sa régénération coûte moins que le diagnostic d'une
corruption découverte après scellage. L'oracle étant dérivé de I — couche indépendante de
la cible — le **même** oracle valide les blocs de tous les profils : la portabilité ne
divise pas le coût de vérification, elle le mutualise.

**Le round-trip de notation** : chaque bloc assemblé par le moteur de notation du profil
est désassemblé par le vérificateur correspondant, et les instructions obtenues sont
comparées à la notation d'origine. Tout désaccord — une instruction, un opérande, une
taille d'encodage — est un échec de build. Ce contrôle à coût quasi nul attrape la classe
d'erreurs la plus insidieuse : l'écart silencieux entre ce que l'agent croit avoir écrit et
les octets réellement produits. La nuance capitale est que la notation n'est pas un
compilateur — aucune optimisation, aucune réécriture ne s'intercale entre l'écriture et les
octets (principe WYSIWYG).

**La cristallisation** ferme la boucle économique : plus un bloc fait ses preuves, moins il
coûte à vérifier, ce qui libère le budget pour les blocs jeunes et les zones actives. La
chaîne de confiance du scellage résume le parcours d'une preuve : verdict de l'oracle →
vecteurs dorés hachés dans frag-prf → empreinte du bloc dans frag-bld → signature de la
carte entière → immuabilité à dix vérifications.

### 8.1 Vecteurs de vérification

Les vecteurs exigés par le gabarit § 2.2 sont de trois espèces : **vecteurs dorés**
(entrées/sorties de référence, conservés hachés dans frag-prf) ; **propriétés
différentielles** (invariants testés par l'oracle sur entrées aléatoires contraintes) ;
**tests de rejet** (les cas d'échec E1…En du contrat, chacun matérialisé par un test qui
exige la sanction nommée). Exigence de couverture : chaque exigence numérotée du contrat
(pre, post, inv) et chaque cas d'échec relie au moins un vecteur — la commande d'audit de
traçabilité (§ 4.2) vérifie ce maillon.

### 8.2 Suite de conformité par profil

Chaque profil embarque une **suite de conformité** vérifiant ses sept éléments
constitutifs (D22) :

| # | Élément du profil | Contrôle de la suite |
|---|---|---|
| 1 | ISA et types | tailles, alignements, boutisme constatés = déclarés |
| 2 | ABI d'appel | appels et retours conformes ; volatilité ; shadow space ou zone rouge |
| 3 | Format d'exécutable | en-têtes valides ; protections actives constatées (DEP/NX, ASLR/PIE, CFI/CFG) |
| 4 | Interface système | résolution des imports ou syscalls ; contrat d'erreurs |
| 5 | Patch à chaud | bascule atomique et invalidation du cache d'instructions démontrées |
| 6 | Notation | round-trip 100 % sur le corpus d'instructions du profil |
| 7 | Granularité et padding | adresses stables après patch (R7) |

Un profil sans suite verte n'est pas déclarable supporté — un profil incomplet est refusé
exactement comme un build sans carte (D14). La suite est un livrable obligatoire de
l'instanciation d'un profil et le critère d'acceptation des jalons M6 et M7. Elle est
exécutée à chaque cristallisation de version rc et finale (§ 9) sur le profil concerné.

### 8.3 Parité inter-profils à contrat constant

Deux profils P1 et P2 sont **paritaires** pour le contrat σ si et seulement si : (1) σ est
instancié sur les deux profils depuis la même spécification I, à la paramétrisation près ;
(2) l'oracle — dérivé de I, mutualisé — est vert sur les deux ; (3) les verdicts des
vecteurs de vérification de σ sont équivalents sur les deux profils ; (4) les différences
de profil sont documentées dans frag-con de chaque bloc. La parité se **vérifie par
exécution**, jamais par déduction : c'est le critère de sortie de M6 (inter-OS, à ISA
constante) et M7 (inter-ISA). Aucune couche d'abstraction n'est introduite pour l'obtenir —
un bytecode portable trahirait la fonction objectif Performance (rejet consigné, D14 et
§ 19.2).

### 8.4 La validation terrain — la boucle d'évidence

La v0.5.0 élève la validation terrain au rang de couche de vérification normée (D43). Le
principe est né d'un constat structurel : l'oracle différentiel exécute le binaire contre
un **modèle** de l'environnement — chargeur, ABI, sémantique des API, protections
mémoire. Un binaire peut donc être exact au sens du round-trip, intègre au sens de la
porte R10, conforme au sens de la suite du profil, vert au sens de l'oracle — et mourir
au premier appel sur machine réelle, parce que le modèle était plus pauvre que la
réalité. Les jalons M1 et M2 en ont fourni la preuve expérimentale : huit classes de
défauts ainsi invisibles (§ 8.5) n'ont été révélées que par l'exécution terrain.

La boucle d'évidence comporte cinq éléments normés :

1. **Le journal d'exécution** — l'artefact livré écrit ses preuves au fil de l'eau
   (fichier à côté de l'exécutable, ligne par ligne). La règle d'honnêteté est absolue :
   une ligne n'est écrite qu'après la vérification de l'étape qu'elle atteste (memcmp
   exact) — une ligne présente vaut preuve ; la dernière ligne visible localise toute
   mortalité à l'intervalle près.
2. **La lecture asymétrique** — le terrain retourne son verdict par un canal à faible
   bande passante : le journal (éventuellement complété d'une capture). L'atelier
   n'exige du terrain que ce document, jamais un diagnostic : la charge d'analyse reste
   à l'agent.
3. **L'instrumentation contractualisée** — quand l'intervalle de mortalité reste
   aveugle, l'itération suivante embarque des sondes de trace aux frontières (D40) :
   elles journalisent des faits (positions d'exécution, retours vérifiés), jamais un
   succès non prouvé ; leur retrait après constat vert est promis dans la spécification
   (D43 a honoré la promesse) et vérifié par l'oracle — le journal nominal redevient
   exactement sa séquence de preuves, toute ligne parasite est un échec.
4. **Le diff chirurgical** — chaque itération terrain ne modifie que les blocs révisés ;
   l'audit d'itération vérifie mécaniquement qu'aucun octet hors des zones autorisées
   (blocs révisés, chaînes, version, sommes) n'a bougé — l'héritage scellé reste
   octet-identique (R7).
5. **L'archive brute** — chaque journal terrain est archivé tel quel (octets d'origine,
   encodage et CRLF compris) avec son empreinte : la preuve est le document, pas son
   résumé.

Le protocole est ensuite économique : huit lectures de journal ont suffi à nommer huit
classes de défauts en deux jours (demo.1 à demo.8), et le dernier diagnostic a été obtenu
sans run supplémentaire — par lecture statique des octets appuyée sur les preuves
accumulées (D42). La contrepartie est la garantie de progression : chaque défaut nommé
devient un vecteur de falsification permanent de l'oracle — le modèle d'environnement
s'enrichit de chaque lecture terrain et ne peut plus régresser en silence.

### 8.5 Taxonomie étendue — les défauts invisibles à l'émulation (X1–X8)

Les classes T1–T6 (§ 3) classent les défauts de contrat non écrit : lisibles dans la
spécification, corrigeables en écrivant le contrat. La campagne M2 a révélé une seconde
famille, structurellement différente : des défauts dont ni la spécification, ni la
notation, ni le round-trip, ni l'oracle ne parlent — parce que le modèle d'environnement
de l'oracle était, sur un point précis, plus pauvre que le système réel. La v0.5.0 en
fixe la taxonomie (D35–D43) :

| Classe | Décision | Dimension du modèle défaillant | Défaut de référence | Garde permanente |
|---|---|---|---|---|
| X1 | D35 | sémantique du chargeur | `FirstThunk` ≠ slots appelés : le chargeur réel résout ailleurs que le code n'appelle — `call 0` au premier appel réseau | verrou « chargeur réel » : FirstThunk = slots appelés, contrôlé au build et par l'oracle |
| X2 | D36 | lecture de structure | `RECT.top` lu comme largeur : spécification juste, octets faux — bloc jamais exécuté, shim témoin muet | coquille entière exécutée + invariant géométrique + falsification de l'octet |
| X3 | D37 | canal de vérité | jumeau silencieux : le journal fichier vivait, l'écran restait vide — le défaut vivait dans la spécification elle-même | miroir universel : chaque ligne écrite écran puis fichier, les deux canaux contrôlés |
| X4 | D38 | ABI caller-saved | dimensions relues dans des registres volatils après l'appel : un retour de syscall écrit RFLAGS dans r11 | clobber des volatiles à chaque retour simulé + falsification |
| X5 | D39 | protections mémoire | phase de patch `PAGE_READWRITE` sans bit execute : DEP permanent x64, le fetch suivant faute | le shim applique les permissions réelles + falsification 0x40 → 0x04 |
| X6 | D40 | écart émulation/terrain | défaut latent qu'aucune exécution n'avait déclenché : l'audit exhaustif était vert | sondes de trace aux frontières (§ 8.4), instrumentation contractualisée |
| X7 | D41 | obligations ABI de l'appelant | zone d'accueil msx64 absente : l'appelé (/homeparams) écrit sur l'adresse de retour — le ret saute à 0x700 | shim /homeparams + audit systémique des sites d'appel + falsification |
| X8 | D42 | état hérité | section critique exigée par un bloc scellé (P5) mais initialisée par un bloc orchestrateur retiré de l'hôte | shims à état + exécution réelle du bloc consommateur + contrôle post-run |

Trois règles d'usage, miroir de celles de la taxonomie T. Premièrement, tout défaut
terrain corrigé est classé T ou X au journal des décisions — la métrique « défauts
ouverts par classe » du tableau de bord (§ 17.2) couvre désormais les deux familles.
Deuxièmement, chaque classe X est gardée par une falsification : réintroduire le défaut
doit faire échouer l'oracle — le modèle s'enrichit mais ne régresse jamais en silence.
Troisièmement, la taxonomie est ouverte : une neuvième classe sera nommée X9 avec sa
décision, jamais dissimulée dans un correctif muet.

La lecture académique : un oracle différentiel valide la conformité d'un artefact à un
modèle ; la validation terrain valide le modèle lui-même. Les deux couches sont
complémentaires, non redondantes — l'oracle couvre l'espace des entrées à coût nul, le
terrain couvre l'espace des environnements au coût d'un run. Le protocole exige les
deux : R5 (vérifie-puis-écrit) pour la première, la boucle d'évidence (§ 8.4) pour la
seconde.

## 9. Cristallisation et pré-versions

La v0.3 connaissait les balises de version sans en fixer la sémantique ; la démonstration
RoomEq a inventé en cours de route la pré-version `-dev.N` pour distinguer « vérifié par
l'oracle » de « validé sur le terrain ». La v0.4.0 formalise le schéma complet (D23) :

| Segment | Signification | Conditions d'ouverture |
|---|---|---|
| `X.Y.Z-dev.N` | pré-version de développement | oracle vert (R5) ; construction 0 erreur / 0 avertissement ; jamais validée terrain ; usage interne |
| `X.Y.Z-rc.N` | candidate à la validation | dev + suite de conformité du profil verte (§ 8.2) + critères du jalon courant ; soumise à la validation terrain |
| `X.Y.Z` | version finale | validation terrain consignée au journal des décisions ; balise immuable |

Trois règles gouvernent le schéma. **Monotonie** : pour un même triplet X.Y.Z,
dev.N < rc.N < version finale ; la version minimale acceptée alimente le contrôle
anti-rollback de R10. **Immuabilité** : une balise posée n'est jamais déplacée ni
supprimée ; un défaut découvert après cristallisation se corrige en `X.Y.Z+1` à contrat
stable (R4) — l'échec est honoré, pas effacé. **Progression de contrat** : une évolution
qui rompt un contrat publié passe par `X.(Y+1).0` avec révision explicite de la
spécification I concernée (§ 2.3). Le schéma généralise la séquence vécue par RoomEq
(v3.0.0-dev.1 → v3.0.0 → v3.0.1 → v3.0.2 : deux échecs d'intégration continue honorés puis
corrigés en patchs à contrat stable), qui demeure l'occurrence de référence.

## 10. Binaires scellés hérités : reverse-specs

Un projet agent-first hérite presque toujours d'un patrimoine : binaires scellés, validés
sur le terrain, dont le code source existe mais dont les contrats ne sont écrits nulle
part. La v0.3 ne disait rien de ce cas — la démonstration RoomEq y a répondu par
invention, en écrivant les spécifications de l'installateur scellé v2.2.2 par
rétro-ingénierie (décision D11 du dépôt de démonstration, huit modules M-INS). La v0.4.0
officialise la pratique (D23).

**Définition.** Une *reverse-spec* est une spécification I extraite d'un artefact scellé
existant : le gabarit § 2.2 s'applique intégralement, avec deux particularités. La
**provenance** est `reverse-spec de <binaire scellé @ tag>` — elle identifie l'artefact
source et sa balise. Le **statut** est « prête » tant que la spécification n'a pas été
confrontée au comportement réel (fixtures issues de l'artefact, tests de discrimination) ;
il passe à « validée » lorsque les vecteurs ont tranché. Une reverse-spec ne modifie
jamais l'artefact scellé : elle le documente.

**Règles.** Premièrement, le recodage d'un binaire scellé ne peut partir que de sa
reverse-spec validée — jamais du code relu en séance, jamais d'une mémoire de session.
Deuxièmement, une reverse-spec en statut « prête » figure dans la traçabilité (§ 4.2) avec
son statut visible : l'exception est nommée, pas silencieuse. Troisièmement, la
rétro-ingénierie se fait par lecture ligne à ligne du code source scellé — la méthode est
déclarée dans la spécification, reproductible par un tiers. La reverse-spec étend la couche
I au patrimoine sans l'exiger de recoder : figer la connaissance avant de décider.

## 11. Optimisation : interdiction du prématuré et journal

La fonction objectif place l'optimisation au troisième rang — après sécurité et
performance, avant le coût en tokens — et l'assortit d'une condition : « descente à l'ISA
sur les hot paths identifiés par profilage ». La v0.4.0 en tire l'interdiction normative
(R11) et son instrument, le **journal d'optimisation** (D21) : l'optimisation sans hot
path identifié ni mesure est prématurée, donc interdite ; sa demande est refusée et
consignée — le refus motivé fait partie de la gouvernance, exactement comme les
alternatives rejetées du journal des décisions.

Format normalisé d'une entrée :

```
[OPT-NN] date · bloc/chemin · décideur
  hot path       : <identification + preuve de mesure (profilage, charge)>
  mesure avant   : <valeur, conditions, matériel>
  changement     : <description> · contrat stable : oui/non (R4)
  mesure après   : <valeur, conditions identiques>
  gain           : <× ou %> · décision : appliquée | refusée (motif)
  décision liée  : Dxx
```

Le journal est versionné avec la couche I ; toute entrée d'optimisation appliquée doit
précéder le commit du bloc optimisé (R11 sanctionne le commit, pas seulement
l'intention). L'entrée de référence est l'occurrence RoomEq : la demande d'« optimisation
maximale » a été honorée par la mesure — chaîne d'égalisation à 152× le temps réel, zéro
allocation par bloc — puis refusée en tant que transformation, faute de problème de
performance à corriger ; le tout consigné en une entrée unique (décision D15 du dépôt de
démonstration). La métrique « optimisations sans mesure » du tableau de bord (§ 17.2) doit
rester à zéro.

## 12. Souveraineté cryptographique — le programme v0.6.0

La menace fondatrice est nommée depuis D84 : *l'expropriation* — un tiers (typ.
l'employeur) qui s'empare du binaire, du dépôt, voire des clés du poste. La barrière
juridique (licence BSL 1.1) répond aux tribunaux ; la barrière cryptographique répond à
la machine. Sources normatives de ce chapitre : les spécifications scellées sous le
sceau de l'Intention — `v06/I/README.md` (axe 3), `v06/I/CF2/README.md` (axe 2),
`v06/I/CF3/README.md` (axe 4). En cas de divergence, l'arbre signé fait foi.

| Axe | Décision | Mécanisme livré | État à la passation |
|---|---|---|---|
| 1 · Attestation de non-exfiltration | D85 | quote vérifiable TPM 2.0/SGX du code manipulant le coffre ; refus de déverrouillage sans quote | **exigence consignée** — infrastructure sans TEE |
| 2 · Interrupteur d'homme mort | D86 | clé maîtresse CF2 jamais stockée entière (Shamir, 5 gardes seuil 3) ; sentinelle à double seuil ; destruction des fragments ; PORTE D120 | **livré, prouvé terrain** — chaîne réelle migrée CF1 → CF2 le 31/10/2026 |
| 3 · Filigrane de l'Intention | D87 | chaque arbre de couche I condensé puis signé par la clé Ed25519 *hors-ligne* ; build et chemin de patch refusent une couche I non signée | **livré, prouvé terrain** — treize arbres signés ; re-cérémonie réelle D126, cérémonies d'ère M8 (12 arbres, D162/D163) et M9 (13 arbres, D166/D168) passées sur pièces, garde 13/13 |
| 4 · Serrure piégée | D121 | coffre CF3 : clé utilisateur invariable, moitiés serrure/piège fraîches à chaque époque, piège sur média séparé, cycle en deux actes, sentinelle instantanée par invocation | **livré, prouvé terrain** — chaîne réelle migrée CF2 → CF3 le 30–31/10/2026 |

### 12.1 La hiérarchie des gardes — quatre secrets, quatre menaces

| Garde | Menace couverte | Où elle vit |
|---|---|---|
| Phrase de lignée | chiffre les enveloppes de carte — vol du dépôt au repos | en tête du développeur, secours au coffre Drive (D81, du 4 au 19 novembre 2026 : le fichier FUT la remise — amendé D223) |
| Graine Ed25519 en ligne | signe les cartes — atteste les FAITS (les octets scellés) | dépôt du développeur (jamais confiée au bac à sable, D30) |
| Clé I hors-ligne | signe l'intention — atteste la VOLONTÉ (le droit de faire évoluer) | support physique hors machine ; le dépôt ne voit que la clé publique |
| Clave du coffre (CF2/CF3) | le secret maître — expropriation du poste vivant | CF2 : répartie par Shamir ; CF3 : moitié piège sur média séparé |

### 12.2 CF2 — la clé maîtresse répartie (D86)

Le secret maître **M** (32 octets CSPRNG) n'est *jamais* écrit entier — nulle part,
jamais. Découpage Shamir sur GF(2^8) (polynôme générateur **0x11B**) : pour chacun des
32 octets, un polynôme distinct de degré T−1 à coefficients frais du CSPRNG ; le
fragment j porte les évaluations. Bornes : 2 ≤ T ≤ N ≤ 255, **T = 1 refusé**.
Reconstruction par Lagrange sur T fragments valides, vérifiée contre `verif` (16 o)
avant toute interprétation. **Sous le seuil, la sécurité est informationnelle** : tout
M′ reste compatible — la destruction des fragments est une mort, pas une révocation.
Valeurs terrain : **N = 5, T = 3** ; la relève exige T copies hors-ligne (erratum D121 :
TROIS, pas deux). Format fragment ASCII (transportable sur papier) :

```
TRIADE-CF2-FRAG v1
coffre: <sel HKDF du conteneur, 64 hex - identite STABLE du coffre>
x: <indice, decimal>
seuil: t=3/n=5
fragment: <64 hex - 32 o>
tag: <16 hex - sha256("TRIADE-CF2-frag" || x || fragment) tronque>
```

La sentinelle CF2 surveille la couche C à **double seuil** (processus hors liste
blanche ET lecture de contenu) ; moteur laboratoire inotify + `/proc`, moteur Windows
SACL/4663/ETW exigence consignée. La **PORTE D120** exige une sentinelle vivante pour
déverrouiller ; sans moteur, la porte *avertit nommément* à chaque déverrouillage —
l'ère intermédiaire est dite, pas cachée. Destruction `bruler` : trois passes + PV
nommant le déclencheur ; restauration atomique (toute anomalie et rien n'est écrit).

### 12.3 CF3 — la serrure à triple scellement (D121)

Trois éléments : **K_user** (`Argon2id(phrase, sel_argon)`, 65536 Kio / 3 it / p=1 —
**invariable à travers les époques**) ; **S_serrure** (32 o frais par époque, dans
l'en-tête clair) ; **S_piège** (32 o frais par époque, *exclusivement sur le média
séparé*). L'**époque** (u64, incrémentée à chaque clôture) est l'horloge de la
métamorphose et le témoin anti-retour ; **H_projet** lie la clé de clôture au contenu.
Dérivation : `KEK = HKDF-SHA256(ikm = K_user ‖ S_serrure ‖ S_piège ; salt = sel_hkdf ;
info = "triade-CF3/v1|" ‖ époque ‖ H_projet)` ; le champ **verif** rend l'essai
hors-ligne impossible au voleur de la machine seule (il manque V_piège, publique,
portée par le piège). Conteneur :

```
"TRIADE-CF3" 10 o | version u16 (=1) | époque u64 | H_projet 32 o |
sel_argon 16 o | params (t,m,p : u32×3) | sel_hkdf 32 o | S_serrure 32 o |
nonce 24 o |                       <- fin de l'AAD (168 o)
empreinte 32 o = sha256(chiffretexte) | verif 16 o |
chiffretexte = AEAD(clair, aad, nonce, KEK)
```

Le fichier **piège** (un ASCII par époque, sur le média du sachet) : une clôture
AJOUTE le piège N+1 et ne ronge jamais les pièges passés ; un piège entièrement forgé
se présente comme une phrase erronée — bénin, jamais de destruction. La **sentinelle
instantanée** réalise l'exigence D120 *par invocation au lieu de résidence* : cinq
vérifications ordonnées à tout acte (piège présent → tag → cohérence époques/H_projet
→ phrase → AEAD + étiquette) — le démon résident, usurpable par faux heart-beat, est
mort ; *le piège est le témoin, et il est hors machine*. Le **cycle en deux actes**
borne la session : ouverture → brouillon sous K_session (média débranché, canonique
jamais réécrit) ; clôture → phrase retapée, moitiés fraîches, époque N+1, piège
additif, staging relu à froid, remplacement atomique — une panne auto-nettoie. La
**réponse à la falsification prouvée** (AEAD + étiquette après quatre verts) détruit
côté machine (trois passes + PV) — jamais le média ni les fragments. L'**anti-retour**
repose sur trois témoins d'époque : journal local (effaçable par un admin), **carte
papier du sachet** (checksum à la main, indécevable par logiciel), journal Git
(poussé, hors machine).

### 12.4 Le sceau de l'Intention (D87)

Treize arbres de couche I vivent sous le sceau — les lignées m0 à m8 (le domaine
`sys` depuis l'ère M8), l'arbre `tls13` (le domaine TLS 1.3 pur depuis l'ère M9),
`demo`, `terrain`, et `v06/I` : la spécification du sceau est la première couche
qu'il garde. **Le quatorzième arbre est nommé** : l'ère du TGN (le domaine
`loupe`, D171) porte sa dette de cérémonie à la naissance — l'arbre `loupe` et
l'extension du registre figé m0 attendent la re-signature hors-ligne du
développeur AVANT tout build de l'application ; le garde demeure à treize arbres
jusque-là, AUCUN arbre signé n'est touché. Chaque ère qui ouvre un arbre nomme sa dette de cérémonie à la
naissance (D166, règle 8) : le registre figé étendu et l'arbre neuf exigent la clé
hors-ligne avant tout build — la charge se prépare au geste qui sert la main du
développeur (D168), et la continuité de la clé se prouve par le déterminisme
Ed25519 (D163) : re-signer les arbres inchangés redonne exactement les signatures
déposées. Manifeste canonique (UTF-8,
LF, tri lexicographique déterministe) ; chaque ligne porte le SHA-256 du contenu
**canonique LF** (D115 — la représentation du checkout n'est pas l'intention) ;
l'empreinte d'arbre est le SHA-256 du manifeste entier ; la signature **Ed25519**
(RFC 8032) couvre l'empreinte — 32 octets, imprimables : la cérémonie hors-ligne
manipule quelques lignes hexadécimales, jamais le dépôt. Cérémonie autoportée (stdlib
seule) : `generer`, `signer` (chaque signature vérifiée avant écriture), `verifier`.
Gardes dans la source des chaînes : `build_m4.py` et `build_terrain.py` refusent le
build sur arbre divergé ; tout script qui modifie une couche I appelle la garde en
sortie. `sceau_I.py verifier` : codes nommés 0/10/11/12.

### 12.5 Le niveau du coffre neuf — un arbitrage du développeur (D137)

La chaîne CF1 → CF2 → CF3 est le chemin *historique* du coffre réel ; elle n'est plus
un rang de naissance. La v0.6.0 fixait la règle « un coffre neuf naît CF3 » (`init`
direct, époque 1, média du piège dès le premier jour) ; la v0.6.1 revient sur cet
arbitrage : **le niveau de sécurité d'un coffre neuf — CF1, CF2 ou CF3 — est choisi
par le développeur lors de la création de son projet de développement** (D137).
Imposer CF3 par défaut risque d'être trop contraignant selon le projet : le niveau le
plus fort exige un média de piège dès le premier jour, le cycle en deux actes à chaque
session, le sachet physique et sa carte — la contrainte se justifie quand le secret la
mérite, pas pour tout projet.

**Les trois naissances** — l'acte de création détermine le niveau et ses obligations :

| Niveau | Acte de création | Ce qui vient avec |
|---|---|---|
| CF1 | `coffre_fort.py init` | conteneur chiffré à phrase (D75) ; la garde de la phrase à l'arbitrage du développeur (D137 — la garde active D223 : le séquestre à reconstitution à froid, la phrase en AUCUN dépôt ; l'histoire D81 datée) ; relève simple |
| CF2 | `coffre_fort.py init` puis cérémonie `coffre_cf2.py migrer` — l'`init` direct de CF2 demeure un outil de LABORATOIRE, la spécification scellée CF2 (§ 12 — phase laboratoire / cérémonie réelle) fait foi | clé maîtresse répartie Shamir (N gardes, seuil T), T copies hors-ligne, liste blanche, sentinelle/porte D120 |
| CF3 | `coffre_cf3.py init` | époque 1, média du piège dès le premier jour, cycle en deux actes, sentinelle par invocation, sachet + carte papier (§ 13) |

**Le guide de l'arbitrage** (recommandation, pas contrainte) : CF1 suffit quand la
menace est le vol au repos du poste seul et que la simplicité de relève prime —
prototype, projet jetable, secrets reproductibles ; CF2 quand la garde doit être
partagée ou survivre au maître — quorum, relève à plusieurs ; CF3 pour les secrets
maîtresses d'un projet vivant sous menace d'expropriation — la référence demeure le
coffre réel de TRIADE, né CF1 et monté à CF3 par cérémonies. La montée n'est jamais
bloquée : **la chaîne de migration CF1 → CF2 → CF3 reste disponible à tout moment** —
les besoins grandissent, le coffre suit ; la descente de niveau n'existe pas (`bruler`
demeure l'acte de fin de vie). Le niveau choisi se consigne au journal des décisions
du projet avec sa raison — un arbitrage muet serait un contrat non écrit (§ 3).

La question du terrain — *puisqu'un coffre né CF3 porte sa sentinelle dès la
création, celle-ci ne devient-elle pas inutile ?* — garde sa réponse normative au
niveau CF3 : la sentinelle de CF3 n'est pas un composant qu'on peut oublier de
lancer, c'est la serrure elle-même ; l'exigence D120 est réalisée *par construction*.
Ce qui demeure obligatoire, niveau par niveau : CF1 — la garde de la phrase à l'arbitrage du développeur (D137 ; la garde active D223 : la reconstitution à froid de trois parts, la phrase en AUCUN dépôt) ;
CF2 — les T copies hors-ligne et la liste blanche ; CF3 — le média du piège (sans
S_piège, le déverrouillage est *impossible*) et la discipline du sachet (§ 13).

### 12.6 Bornes honnêtes consolidées

Attaquant admin pendant un acte (le rayon est borné à UNE époque) ; zéroïsation au
mieux de Python (garantie native au déploiement Windows) ; sentinelle CF2 tuable (le
heart-beat rend la mort visible — CF3 supprime la classe du risque) ; lecture non
attribuée < ~10 ms (journalée, non brûlée) ; CoW/instantanés (l'écrasement logique ne
tue pas les copies physiques) ; carte papier regardée (le verdict à froid est le
filet) ; axe 1 TEE non satisfait (exigence consignée, pas promesse).

## 13. Les cérémonies et le kit du terrain

Les cérémonies de la souveraineté sont des *actes du maître* : le bac à sable ne
touche jamais le conteneur ni les phrases réels (discipline D105). L'outillage les
guide sans les réimplémenter.

### 13.1 La chaîne des cérémonies

| Cérémonie | Gestes | Preuve attendue |
|---|---|---|
| Sceau de l'Intention (D87/D126) | `preparer` ; cérémonie hors-ligne `signer` (clé physique) ; `deposer` (vérifié avant écriture) ; `verifier` | treize arbres VERTS, code 0 ; commit poussé |
| CF1 → CF2 (D106) | phrase (la garde en vigueur : D223 — la reconstitution à froid de trois parts du séquestre ; l'histoire D81 « remise AVANT tout » datée du 4 au 19 novembre 2026) ; `migrer` ; 5 gardes ; T = 3 copies hors-ligne (feuille g3–g5 ou USB) ; relecture ; liste blanche | CF2 `verifier` VERT ; CF1 laissé intact |
| CF2 → CF3 (D121/D127) | MIGRER (conteneur CF2, gardes, *média du piège requis*, phrase deux fois) ; VÉRIFIER (checksum contre la carte) ; DÉTRUIRE (case explicite) | époque 1, checksum 8 hex noté ; verdict à froid VERT (machine froide recommandé) |
| Clôture CF3 (usage courant) | acte I (média débranché) ; session sur le brouillon ; acte II (phrase retapée, époque N+1) | checksum affiché, ligne sur la carte ; journal Git consigné |
| Destruction locale (`bruler`) | commande explicite `--oui-je-comprends` ; trois passes + PV | PV nommé ; fragments et médias jamais touchés |

### 13.2 Le maître de cérémonie graphique et le trio D122

Les cérémonies sont conduites par le maître de cérémonie graphique
(`v06/ceremonie_gui.py` pour le sceau et CF2 ; `v06/migration_cf3_gui.py` pour CF2 →
CF3) : zéro ligne de commande, un fichier, deux profils. Le GUI est un *relais* : il
lance les vérités vivantes et croise code de sortie ET marque de verdict. La phrase
passe par STDIN, jamais affichée, jamais dans un rapport. Chaque module porte le trio
D122 : une GUI, une boîte noire locale horodatée, un bouton « Envoyer le rapport ».
L'habit a appris du terrain : cahier numéroté (D128), pilier droit permanent (D129),
un bouton d'attachement par page (D131), grille — chaque bouton « Parcourir » sur la
ligne de son champ (D132).

### 13.3 Le kit Drive — identité par construction (D130)

Les cérémonies s'arment depuis le dépôt *ou* depuis le kit du dossier `/Cérémonie` du
Drive. Depuis D130, le `v06/` du kit est déployé depuis `git ls-files v06/` — la même
source que le miroir, lue dans le même arbre : **identité octet pour octet par
construction**, `I/` et `sceau-I/` inclus. Le hook post-commit porte le miroir PUIS le
kit dans le même geste. Le `MANIFESTE.txt` du kit porte le commit de référence : un
kit périmé se *lit*, ne se devine pas.

### 13.4 La preuve terrain de la chaîne réelle (30–31 octobre 2026)

CF1 statut VERT ; CF1 verifier INTÈGRE ; phrase changée (D110) ; un premier `migrer`
CF2 refusé nommément (« phrase de contrôle divergente » — la remise D81 n'était pas
encore remplacée : le fail-closed a travaillé, la cérémonie rejouée) ; CF2 né (cinq
gardes, seuil 3, CF1 intact, porte D120 posée en ère sans moteur) ; feuille exportée ;
puis CF2 → CF3 : MIGRER VERT (base re-scellée, schéma identique — rien à traduire ;
piège posé sur le média ; re-lecture à froide verte ; époque 1, checksum
`0cc89a96`, CF2 laissé intact) et VÉRIFIER VERT deux fois, checksum identique. La
destruction du conteneur CF2 (acte 4) est un geste *explicite* du maître, après
recoupement sur machine froide : jamais l'ancien avant le vert du neuf. Observation
honnête consignée : l'empreinte du `coffre_fort.py` mesurée au clone terrain
(`299fd124…`) diverge de celle du dépôt (`8c79263b…`) — à recouper au prochain
`git pull`.

### 13.5 Les cérémonies d'ère du sceau de l'Intention (5 novembre 2026)

Le sceau a traversé deux cérémonies d'ère en un jour, chacune née d'un garde qui
refusait. **Ère M8** : l'ouverture du domaine `sys` avait étendu le registre figé m0
et créé l'arbre m8 — le garde a nommé la dette AVANT tout build (D162 : un diff
d'intention non signé ; la clé hors-ligne du développeur requise, le laboratoire ne
signe jamais à sa place) ; le kit de cérémonie servi au dossier `/Cérémonie` du
Drive (la remise, le LISEZMOI pas à pas, la règle d'or « JAMAIS generer »), la
cérémonie passée sur pièces : douze arbres, les dix inchangés rendant les MÊMES
signatures que celles du 04/11 (la preuve D163 de la réutilisation de la clé, sans
jamais voir la clé privée), le garde repassé VERT 12/12 — puis le build 0.9.0-dev.1
né, déterministe d'un poste à l'autre. **Ère M9** : la dette fut nommée À LA
NAISSANCE (D166, règle 8) ; le geste des 24 spécifications ayant bougé l'arbre, la
charge fut RÉGÉNÉRÉE au geste de la cérémonie (D168 : la charge de l'ouverture était
périmée — une remise signée dessus aurait laissé l'arbre divergé APRÈS
installation) ; le développeur signa hors ligne la remise de TREIZE arbres et
déposa signatures-I.txt et cle-publique-I.txt au coffre `/test` ; le laboratoire
rapatrie, recoupe — la clé déposée égale l'ancre `173fae9c…`, les ONZE arbres
inchangés rendent les signatures de l'ère M8, m0 re-signé, tls13 arbre neuf, les
empreintes vivantes égales la remise, chaque signature vérifiée Ed25519 — puis
installe canoniquement (tout vérifié AVANT toute écriture) et le garde est repassé
VERT 13/13, l'état « reelle » tenant. La règle qui en découle : la cérémonie d'ère
n'est pas une formalité de documentation — c'est le geste qui rend le build de
l'ère possible, et il suit le calendrier du garde, jamais l'inverse. **L'ère du
TGN (le domaine `loupe`, D171/D175)** suit la même discipline : la dette fut
nommée à la naissance de la couche I (D171, règle 8) et la notation des 18 blocs
s'accomplit sous elle — quatre chantiers, la table de routage de loupe-09 étendue
en révision nommée sans cascade — AUCUN build : la cérémonie précède (le miroir
des ères M8/M9). Le kit de cérémonie vit au dossier `/Cérémonie` du Drive (la
remise FRAÎCHE des quatorze arbres — la charge se prépare AU GESTE de la
cérémonie, D168 : les empreintes bougent avec chaque révision de spécification —
le LISEZMOI pas à pas, la règle d'or « JAMAIS generer ») : le développeur signe
hors ligne à la clé du 04/11 (l'ancre de toutes les ères), ramène
signatures-I.txt et cle-publique-I.txt au coffre `/test` ; le laboratoire
rapatrie, recoupe (l'ancre de clé, les arbres inchangés rendant les MÊMES
signatures par le déterminisme Ed25519, m0 re-signé au registre étendu, l'arbre
`loupe` neuf), installe canoniquement — et le garde passe à QUATORZE arbres
VERTS : le build de Loupe peut naître.

## 14. Coût en tokens : fragmentation, localisation, budgets

Le coût en tokens est le seul des quatre objectifs spécifique à l'ère agent-first. Il est
traité comme une contrainte d'ingénierie — budgets, mécanismes, instrumentation — toujours
subordonnée aux trois objectifs supérieurs : aucune économie de tokens ne justifie de
sauter une vérification.

**Fragmentation (norme).** La carte est fragmentée en quatre (frag-loc, frag-con, frag-prf,
frag-bld ; FORMAT_CARTE § 2), et la v0.4.0 pose la norme en trois volets : aucune opération
de la boucle n'exige la lecture de plus d'un fragment ; **aucune opération n'exige la
lecture intégrale du binaire** — la carte est l'unique index, le balayage est interdit
(§ 7) ; l'audit complet de la carte est une opération exceptionnelle, non budgétée,
journalisée. Le multi-profils n'alourdit pas la localisation : l'entrée de frag-loc porte
le profil, et l'instanciation d'un contrat sur un profil nouveau est budgétée comme un
ajout — la couche I, elle, n'est jamais dupliquée.

**Budgets par type d'opération** (désormais instrumentés — § 17.2 ; le budget de
localisation est amendé à 64 tokens par D31 : la mesure M1 a constaté 43 tokens sur le
gabarit canonique de la v0.4.0 lui-même, tokenizer BPE cl100k_base) :

| Opération | Fragments et données lus | Budget |
|---|---|---|
| Localiser un bloc | frag-loc — une entrée | 64 tokens max (D31) |
| Éditer simplement un bloc | frag-loc + frag-con du bloc + notation du bloc | 3 000 tokens max |
| Ajouter un bloc | frag-loc + frag-con + seuils frag-prf | 6 000 tokens max |
| Instancier un profil nouveau pour un contrat existant | I partagée + frag-con + notation du profil | 6 000 tokens max par bloc |
| Audit complet (rare) | Carte entière déchiffrée | Non budgété — opération exceptionnelle |

Indicateurs de santé : précision de localisation (cible 95 % au jalon M0), coût moyen
d'une édition simple (cible 5 000 tokens), taux de régression post-patch (cible zéro,
rollback exclu). Ces budgets, cibles de conception jusqu'à leur instrumentation, sont
mesurés depuis M1 (`m1/budgets_tokens.py`, tokenizer cl100k_base, mesure sur la carte
scellée et les sources réelles) ; le tableau de bord les affiche comme métriques
mesurées, avec leur écart.

## 15. Sécurité : modèle de menace et limites

Le principe directeur demeure : séparer l'obfuscation, qui protège la propriété
intellectuelle (le comment), du durcissement, qui protège l'exécution (le où ça casse).
La carte privée relève du premier ; la sûreté mémoire, les contrats et le fuzzing relèvent
du second. Conformément au principe de Kerckhoffs, la sécurité du système ne repose jamais
sur le secret de la carte : elle survivrait à sa divulgation.

### 15.1 Modèle de menace (étendu en v0.4.0, D20)

| Menace | Acteur | Cible | Contre-mesure | Résiduel |
|---|---|---|---|---|
| Rétro-ingénierie de l'IP | Concurrent, pirate | Binaire livré | Carte privée ; binaire sémantiquement muet ; variantes par build | Temps acheté — s'érode avec les LLM de décompilation |
| Empoisonnement de carte | Attaquant supply-chain | Fragments | Signature (algo de l'en-tête) ; refus de carte non signée ; verrou croisé (R8, R9) | Détecté — session bloquée |
| Corruption de carte (accidentelle) | Bit rot, panne de stockage | Fragments au repos | AEAD (intégrité par fragment) + signature + verrou croisé | Détecté au chargement — refus propre |
| Fuite de la carte | Initié, poste compromis | Fragments au repos | Chiffrement (algo de l'en-tête) ; sharding ; escrow | Perte partielle limitée à un fragment |
| Vol de l'export de continuité | Voleur, stockage cloud compromis | Conteneur exporté | Chiffrement intégral (phrase maîtresse + Argon2id) ; signature | Sans la phrase, indéchiffrable |
| **Vol du coffre-fort des phrases** | Voleur, stockage cloud compromis | Conteneur du coffre-fort (D75) ; de D81 au 19 novembre 2026 la phrase de contrôle vivait au coffre Drive et dans le dépôt (l'arbitrage d'époque PERTE > EXPOSITION) ; depuis D223 la phrase vit sous séquestre à seuil, en AUCUN dépôt | Chiffrement intégral (Argon2id, contexte HKDF dédié, AEAD) ; écriture atomique 0600 ; mitigation première : restreindre le partage par lien du dossier (§ 17.3) | Confidentialité ramenée au contrôle d'accès du dossier ; une phrase commise en git y demeure à vie — on ne compte plus sur sa confidentialité, la rotation reste le remède |
| **Expropriation (employeur, tiers)** | D84 | Barrière juridique BSL 1.1 ; barrière cryptographique : clé maîtresse jamais entière (Shamir, axe 2), intention signée par la clé hors-ligne (sceau I, axe 3), serrure piégée à média séparé (axe 4) | Le code volé est inexploitable et ne peut pas évoluer ; l'axe 1 (TEE) reste une exigence consignée |
| **Evil maid sur le conteneur ou le média du piège** | D121 | Tag du piège, époques croisées conteneur/piège, AEAD + étiquette, champ `verif` indérivable | Détecté — refus nommé ; la falsification prouvée détruit côté machine, jamais le média |
| **Roll-back du couple conteneur + piège** | D121 | Trois témoins d'époque : journal local, carte papier du sachet (à la main), journal Git poussé | Détecté — « RETOUR EN ARRIÈRE » nommé ; recoupement humain à froid |
| **Binaire altéré** | Attaquant local, fichier modifié | Artefact livré | Checksums par bloc + signature du manifeste au lancement (R10 a, b) | Détecté — arrêt avant tout effet |
| **Rollback non autorisé** | Rejeu d'une version ancienne vulnérable | Artefact, état | Monotonie de version signée, plancher anti-rollback (R10 c) | Détecté — refus |
| **Agent défaillant** | Hallucination, dérive hors périmètre | Processus de développement | R2 (intention d'abord) ; R5 (vérifie-puis-écrit) ; oracle dérivé de I ; budgets (§ 14) | L'erreur ne devient jamais permanente sans vérification |
| **Données embarquées modifiées** | Supply chain des données | Tables, profils, ressources livrés | Empreintes des données dans la carte ; vérification au lancement (R10 b) ; parité par hachage | Détecté — arrêt propre |
| **Environnement non conforme** | OS, ABI, protections inattendues | Exécution | Contrôles de conformité au profil au lancement (R10 d) ; fail-closed | Refus propre avant exécution |
| Fuzzing boîte noire | Attaquant externe | Runtime | Contrats, oracle, tests par propriétés, fail-closed | Indépendant du secret de la carte |
| Redistribution frauduleuse | Pirate | Binaire livré | Empreintes par build — canary trap | Fuite traçable à son destinataire |
| Instrumentation dynamique | Analyste | Exécution | Anti-debug léger par mesure de temps | Assumé — l'obscurité n'est pas la sécurité |

Les six menaces en gras sont les additions de la v0.4.0 ; toutes sont neutralisées par des
mécanismes **locaux et vérifiables** — la contre-mesure anti-rollback ne dépend d'aucun
service en ligne (le chargement doit échouer proprement hors ligne), et les vérifications
de R10 s'exécutent avant toute entrée dans le chemin d'exécution.

### 15.2 Limites assumées

La rétro-ingénierie est traitée comme un objectif d'économie, pas d'impossibilité : rendre
le coût de l'analyse supérieur à la valeur de ce qu'on obtient. Un binaire strippé, sans
structure ni symboles, dont chaque exemplaire diffère, coûte sensiblement plus cher à
analyser qu'un binaire compilé standard — mais les modèles de langage appliqués à la
décompilation progressent, et l'avantage doit être réévalué à chaque génération de
modèles. L'anti-debug reste léger et assumé : l'obscurité n'est pas la sécurité. La
furtivité face aux EDR est hors périmètre (§ 1.2) : un outil légitime par construction,
dont la transparence vis-à-vis du système est totale. Et la gouvernance du protocole a été
validée sur un cas unique (N = 1) — l'étude de cas RoomEq, dont les limites sont
documentées dans l'édition académique (D18) : la généralité reste à établir par
réplication, le cœur natif par les jalons M0 à M7 — dont M0, M1 et M2 sont désormais
franchis (§ 18), preuves terrain archivées.

## 16. Profils de cible — universalité

Le cœur du protocole — couches, règles, boucle, vérification — est indépendant de la cible
par construction, et tout ce qui dépend de la cible est regroupé dans un **profil de
cible**. L'universalité reste une propriété structurelle : instancier une plateforme
nouvelle revient à écrire un profil — ses sept éléments **et sa suite de conformité**
(§ 8.2, D22) — jamais à modifier le protocole.

Un profil définit obligatoirement sept éléments, qui font de l'extension une opération
vérifiable plutôt que déclarative : (1) l'ISA et la largeur de ses types — `usize`,
alignements, boutisme ; (2) l'ABI d'appel — registres de passage, volatilité, shadow space
ou zone rouge ; (3) le format d'exécutable et les protections à honorer — DEP/NX,
ASLR/PIE, CFI/CFG ; (4) l'interface système autorisée — IAT, syscalls, libc de la cible ;
(5) le mécanisme de patch à chaud natif — taille minimale de bascule atomique et procédure
d'invalidation du cache d'instructions ; (6) le moteur de notation et son vérificateur de
round-trip ; (7) la granularité des blocs et le padding garantissant les adresses stables
(R7). Un huitième livrable s'ajoute en v0.4.0 : la **politique anti-rollback et de
vérification au chargement** propre au profil (déclinaison concrète de R10 — registre des
versions acceptées, stockage du plancher, contrôles d'environnement).

| Profil | ISA | OS | Format | Interface | Statut |
|---|---|---|---|---|---|
| `x86-64-win11-pe` | x86-64 | Windows 11 | PE32+ | IAT (kernel32, ws2_32, Schannel) | Primaire — jalons M0-M5 |
| `x86-64-linux-elf64` | x86-64 | Linux | ELF64 | syscalls + libc | M6 — portabilité inter-OS |
| `riscv64-linux-elf64` | RISC-V 64 | Linux | ELF64 | syscalls + libc | M7 — portabilité inter-ISA |
| `aarch64-macos-macho` | AArch64 | macOS | Mach-O | libSystem | Réservé — hors feuille de route courante |
| `wasm32-wasi` | WebAssembly | WASI | module Wasm | WASI | Réservé — étude de niche |

L'identifiant d'un profil suit la convention `<isa>-<os>-<format>`. La correspondance des
couches est la suivante : la couche I est partagée par tous les profils du projet ; chaque
entrée de la carte porte son profil ; chaque profil possède son binaire, ses empreintes de
build et son registre de variantes dans frag-bld. « Sans compilateur » ne signifie pas
« sans système d'exploitation » — les interfaces sont appelées selon les conventions du
profil, comme tout binaire natif légitime.

### 16.1 Profil primaire : ABI Microsoft x64

| Convention | Règle |
|---|---|
| Passation des arguments | RCX, RDX, R8, R9, puis la pile — de droite à gauche |
| Valeur de retour | RAX (RDX pour une valeur de 128 bits) |
| Shadow space | 32 octets réservés par l'appelant avant chaque CALL |
| Registres volatils | RAX, RCX, RDX, R8 à R11 — détruits par l'appelé |
| Registres non volatils | RBX, RBP, RDI, RSI, R12 à R15 — préservés par l'appelé |
| Registres flottants | XMM0 à XMM5 volatils, XMM6 à XMM15 préservés |
| Alignement de pile | RSP multiple de 16 au point d'appel |
| Zone rouge | Aucune — contrairement à System V : stocker sous RSP sans allocation préalable est interdit |

L'absence de zone rouge est le piège classique pour qui vient de System V. La convention
interne du projet en tire les conséquences : R10 et R11 sont désignés registres de travail
internes — volatils selon l'ABI, donc jamais promis à un appelant ; aucune donnée vivante
ne séjourne entre RSP et RSP+32 au moment d'un appel ; tout bloc qui appelle une API
alloue son cadre avant d'y toucher. Ces règles internes sont portées par frag-con.

### 16.2 Différences entre profils — aperçu

| Élément | `x86-64-win11-pe` (primaire) | `x86-64-linux-elf64` (M6) | `riscv64-linux-elf64` (M7) |
|---|---|---|---|
| ABI | msx64 : RCX RDX R8 R9 ; shadow space 32 o. | SysV : RDI RSI RDX RCX R8 R9 ; zone rouge 128 o. | psABI RISC-V : a0-a7 |
| Format | PE32+ : DYNAMICBASE, HIGH_ENTROPY_VA, NX | ELF64 : PIE, RELRO, NX | ELF64 : PIE, RELRO, NX |
| Interface | IAT : kernel32, ws2_32, Schannel | syscalls + libc | syscalls + libc |
| Patch à chaud | publication atomique d'un mot de **8 o. aligné** (`E9 rel32` + trois `NOP`), ou `LOCK CMPXCHG16B` pour la forme absolue ; quiescence obligatoire (§ 7.1.1, D253) | identique x86-64 | magasin de **4 o.** aligné, `fence.i` puis synchronisation des autres harts (aucune cohérence I/D implicite) |
| Notation | keystone / capstone x86-64 | keystone / capstone x86-64 | keystone / capstone RISC-V |

Deux transitions méritent une vigilance documentée. Le passage Windows → Linux **inverse**
le piège de la zone rouge : ce qui était interdit sur msx64 (stocker sous RSP) redevient
permis sur SysV pour une fonction feuille — l'agent doit désapprendre le réflexe acquis sur
le profil primaire, et frag-con porte la convention effective de chaque bloc. Le passage
x86-64 → RISC-V change la nature du patch à chaud : sur une ISA à instructions de taille
fixe, il n'existe pas de trampoline relatif de 5 octets insérable n'importe où ; la bascule
passe par un registre scratch chargé de l'adresse cible, suivi d'une barrière
d'invalidation du cache d'instructions (`fence.i`) — le profil spécifie la séquence exacte
et son atomicité.

## 17. Gouvernance

### 17.1 Journal des décisions — format normalisé

Le protocole ne se révisant jamais en silence, chaque décision structurante est consignée
dans un journal des décisions. La v0.4.0 normalise le format (D24) — les entrées D19 à
D25 du dépôt l'appliquent dès à présent :

| Champ | Exigence |
|---|---|
| ID | `DNNN`, séquentiel, jamais réutilisé |
| Date | date de consignation |
| Statut | active · amendée par Dxx · invalidée par Dxx |
| Contexte | exigence, incident ou évaluation qui motive la décision |
| Choix retenu | décision en une phrase, rattachée à la fonction objectif |
| Alternatives rejetées | au moins une, avec motif |
| Amendements | référence explicite à la décision remplacée, le cas échéant |
| Développement | argumentaire détaillé si la décision engage l'architecture |

Trois règles : le journal est **append-only** (une entrée ne s'efface jamais) ; une
révision **invalide explicitement** ce qu'elle remplace (la procédure D14→amende D10
illustre le mécanisme) ; aucune entrée n'est rétrodatée. La conformité du journal —
présence des champs, unicité des ID, chaînage des amendements — est contrôlée
mécaniquement par l'audit de gouvernance (§ 17.2).

### 17.2 Tableau de bord de conformité

La v0.4.0 unifie les indicateurs de santé en un **tableau de bord de conformité** (D24),
généré par la commande d'audit à chaque commit et à chaque cristallisation, archivé avec
la carte :

| Métrique | Cible | Source de mesure |
|---|---|---|
| Blocs avec spécification I à jour | 100 % | audit de traçabilité (§ 4.2) |
| Chaînes de traçabilité complètes I ↔ C ↔ B ↔ tests | 100 % | audit de traçabilité |
| Construction | 0 erreur · 0 avertissement | build |
| Tests différentiels | 100 % verts | oracle |
| Empreintes des données embarquées | conformes à la carte | hachage |
| Défauts ouverts par classe T1–T6 | 0 | journal des décisions (classification) |
| Optimisations sans mesure (R11) | 0 | journal d'optimisation |
| Budgets tokens (localiser / éditer / ajouter) | ≤ 64 / 3 000 / 6 000 | instrumentation — mesurés M1 : 51 / 719 / 1 088 (D31) |
| Suite de conformité par profil actif | verte | suite du profil (§ 8.2) |
| Changements hors journal des décisions | 0 | diff vs journal (audit de gouvernance) |
| Pré-versions : dev/rc/final correctement balisées | 100 % | registre des balises (§ 9) |

Le tableau de bord est la contrepartie mesurable de la gouvernance : chaque affirmation du
protocole s'y retrouve sous forme de métrique avec sa cible et sa source — aucune ne
s'appuie sur une déclaration non vérifiable. Les métriques dépendantes de l'outillage
(instrumentation des budgets) affichent leur statut « cible » jusqu'à leur premier
mesurage.

### 17.3 Continuité et anti-enfermement

L'export de continuité (D16, FORMAT_CARTE § 8) demeure l'unique forme de transfert de
l'état de développement : conteneur chiffré et signé regroupant I, B, C et un manifeste
autodescriptif ; oracle régénéré depuis I à l'arrivée, jamais exporté ; procédure d'import
en cinq étapes dont l'échec d'une seule est terminal. Les pré-requis de sauvegarde (3-2-1
chiffrée, escrow de la clé maîtresse) sont inchangés.

**Le coffre-fort des phrases maîtresses (D75, FORMAT_CARTE § 11).** Le composant qui
centralise toutes les phrases maîtresses d'un projet — et de tout projet ultérieur conduit
sous le protocole — dans un conteneur unique chiffré « TRIADE-CF1 » (`coffre_fort.py`) :
phrase de contrôle détenue par le seul développeur (jamais stockée), Argon2id aux
planchers de la carte au repos puis HKDF à contexte dédié, XChaCha20-Poly1305 avec
l'en-tête clair pour AAD, écriture atomique 0600, autotest de falsification exigé à chaque
installation de l'outil. Le conteneur chiffré s'exporte tel quel vers le coffre Drive du
projet et le coffre personnel du développeur — son vol relève de la menace « sans la
phrase, indéchiffrable » (§ 15.1). Après une réinitialisation du poste, l'import du
conteneur puis `obtenir --vers-fichier` restaurent la phrase opérationnelle sans cérémonie
de régénération. La règle de discipline évolue en D81 sur un point, l'arbitrage étant
consigné : chaque cérémonie de clés (D27/D30) alimente le coffre-fort dans la même
session. **La garde de la phrase est le séquestre à seuil depuis le 19 novembre 2026
(D223)** : la phrase répartie en CINQ parts à seuil TROIS, AUCUNE phrase en clair au
dépôt ni au coffre Drive — la voie de survie est la cérémonie de reconstitution à
froid de trois parts (§ 17.3bis), le refus nommé D223 garde la ligne ; l'affichage
unique de cérémonie (D27/D30) demeure possible mais n'est jamais le canal de survie.
(L'histoire D81 — la phrase au fichier-remise `PHRASE-CONTROLE-COFFRE.txt`, commit
dédié, push GitHub, miroir et coffre Drive, AVANT toute autre action — est DATÉE :
du 4 au 19 novembre 2026, amendée par D223, jamais un geste courant.) À chaque rotation le
fichier est remplacé et git conserve les phrases retirées du service. La graine Ed25519
reste hors coffre (D30) — la relève d'une lignée perdue resterait la cérémonie avec
preuve byte-identique. Contrepartie consignée : la phrase vit désormais sur le stockage
du coffre Drive partagé par lien — la confidentialité au repos y repose sur le contrôle
d'accès au dossier (restriction du partage par lien et vidage de corbeille sont les
mitigations premières) ; une phrase entrée dans l'historique git y demeure, la rotation
reste le remède à toute exposition avérée.

## 18. Critères d'acceptation des jalons M0 à M10

Onze jalons, chacun couvrant une capacité nouvelle et se terminant par des critères de
sortie mesurables — détail dans `docs/PLAN_MILESTONES.md`, mis à jour avec la présente
révision. **Conditions transverses** (v0.4.0) : aucun jalon n'est franchi sans oracle
vert, suite de conformité verte pour les éléments couverts, tableau de bord conforme
(§ 17.2) et carte signée. Les critères propres à chaque jalon :

| Jalon | Capacité | Critères de sortie mesurables | Statut |
|---|---|---|---|
| M0 | Chaîne artefact | exécution sur Windows 11 ; round-trip 100 % ; carte v0 signée et vérifiée ; exécutable < 4 Kio ; R1-R3, R8-R9 dès le premier octet | **franchi** 26/10/2026 (D26) |
| M1 | Blocs réutilisables | oracle 100 % sur la mini-libc ; première cristallisation ; adresses stables démontrées ; budgets tokens instrumentés (première mesure) | **franchi** 26/10/2026 — balise 0.2.0 (D32) |
| M2 | Patch à chaud | remplacement du bloc d'écho en exécution, sans interruption ; rollback démontré ; taux de régression post-patch nul | **franchi** 27/10/2026 — balise 0.3.0, boucle § 5 démontrée sur machine réelle (D43) |
| M3 | Entrées non fiables | un million de requêtes fuzzées sans crash ; proxy transparent ; contrats renforcés sur la surface de parsing | **franchi** 28/10/2026 — balise 0.4.0 (D74) |
| M4 | Tunnel chiffré | HTTPS en transit via Schannel ; échec propre sur certificat invalide | **franchi** 29/10/2026 — balise 0.5.0 (D104 : run 17-H — S49 OK + témoin HTTP/1.1 200 + S05C 2b6481a1) |
| M5 | Outil complet | interception d'un flux navigateur en VM isolée ; patch à chaud du journal en production ; empreintes par build actives ; programme d'étapes et critères dans `PLAN_MILESTONES.md` | **franchi** 04/11/2026 — balise `0.6.0` (Entrée 143, D148 : critère (b) de D136 constaté VERT sur pièces au run e4 ; le chantier (c) « patch du journal en production » reporté au programme M6 par D149 — démonstration sur le profil Linux, moteur embarqué) |
| M6 | Portabilité inter-OS | profil `x86-64-linux-elf64` : suite de conformité verte ; **diff nul sur la couche I** ; parité inter-profils vérifiée (§ 8.3) ; même oracle vert sur les deux profils | **franchi** 05/11/2026 — balise `0.7.0` (Entrée 149, D154 : run terrain WSL2 vert sur pièces — recoup labo 22/22, noyau de la machine du développeur DISTINCT de celui du labo ; conformité 7/7 exécutée au scellage même, l'artefact INTACT ; le chantier M5-(c) « patch du journal en production » refermé sur le profil Linux) |
| M7 | Portabilité inter-ISA | profil `riscv64-linux-elf64` : round-trip 100 % sur la nouvelle ISA ; patch à chaud conforme (scratch + `fence.i`) ; verrou croisé multi-profils ; export de continuité multi-profils vérifié | **franchi** 05/11/2026 — balise `0.8.0` (Entrée 155 : run terrain M7-(d) vert sur pièces, recoup labo 29/29 sur pièces croisées, export multi-profils de bout en bout — l'universalité démontrée : win `0.6.0` / linux `0.7.0` / riscv `0.8.0`) |
| M8 | Syscalls directs (domaine `sys`) | la charte à huit règles et les spécifications sys-01…03 écrites-avant-code ; le harnais différentiel sur fixtures ntdll synthétiques (le labo ne connaît jamais le SSN du terrain) ; le motif du stub vérifié avant toute extraction ; le run terrain sur le VRAI ntdll — la même observable par les DEUX chemins, les refus nommés ; la cérémonie de l'ère avant le build | **franchi** 05/11/2026 — balise `0.9.0` (Entrées 156–164, D160–D165 : harnais 61 verts ; cérémonie de l'ère passée 12/12 ; run terrain m8d VERT — 35 verts / 0 échec, la twin octet pour octet, le refus -4 du stub crocheté ; recoup labo 30/30 ; finale `0.9.0` scellée sur recoup exigé comme pièce) |
| M9 | TLS 1.3 pur (domaine `tls13`) | la charte à huit règles et les 28 spécifications en six familles écrites-avant-code ; les primitives aux vecteurs officiels (FIPS 180-4, RFC 2104/4231, RFC 5869, RFC 7748, SP 800-38D) ; la poignée rejouée sur le transcript RFC 8448 ; le socle socket par syscalls directs (sys-04+) ; la cérémonie de l'ère avant construire() ; la session réelle avec un serveur réel — la ligne applicative chiffrée | **franchi** 07/11/2026 — finale `1.0.0` (Entrées 170–194, D166–D170 : les 28 blocs notés-mesurés-prouvés, le run terrain vert recoupé EXIGÉ COMME PIÈCE du scellage, LA SESSION RÉELLE — la ligne applicative chiffrée échangée avec un serveur réel, le témoin déchiffré par la machine, l'épinglage -6 nommé ; le scellage un fait de carte, proxy.exe byte-identique `446279f3…`) |
| M10 | Le test grandeur nature — « Loupe » (domaine `loupe`) | coder une application réelle NEUVE entièrement avec TRIADE, de l'intention (la couche I) à l'octet livré (le kit terrain) ; les 18 spécifications écrites-avant-code avant tout octet de notation (R2) ; les héritages PAR LA CARTE byte-identiques aux adresses scellées (R7) ; l'oracle à scénarios vert — l'écran attendu octet par octet ; le kit déployé au coffre `/test` (modèle m9f) ; la balise `loupe 0.1.0` scellée sur run terrain recoupé | **franchi** 11/11/2026 (Entrées 218/219, D178) — l'application est NÉE ENTIÈREMENT DE LA MÉTHODE : la cérémonie d'ère PASSÉE SUR PIÈCES (le 14e arbre, la dette D166/D171 SOLDÉE — le garde 14/14), les 18 blocs NOTÉS-MESURÉS-PROUVÉS (59 + 53 + 45 contrôles verts aux trois graines), le kit déployé (M10-(d)) — ET ONZE RUNS TERRAIN, ONZE DÉFAUTS NOMMÉS, ONZE RETOUCHES DOCUMENTÉES : les refus du chargeur 0xc000007b (dev.1/dev.2 — l'enveloppe de la lignée NORME DE FAIT), [CADRE-NÉ] (dev.4 — l'initialiseur .data MIROIR EXACT du CADRE_VIERGE, LE GARDE GUÉRI : le contrôle dérive du plan, jamais de la pièce qu'il contrôle), la classe des arguments pile (dev.5 — l'audit d'ABI msx64 NÉ AU BUILD), [SESSION] -7 VERROUILLÉ (dev.6 kit — L'OMBRE temoin-session.bin, la pièce ACQUITTÉE), [HINSTANCE-PEB] (dev.6 — l'entrée réécrite r12 = GetModuleHandleW(NULL)), [D54-QUATRIÈME] + [EAX-SANS-SIGNE] (dev.7 — l'IAT relogée 0x3100 en QUATRE plages séparées par NULL, les 20 rendus au 64 bits), [OFT-QWORD] (dev.8 — les QUATRE OFT au pas DWORD : la sixième mort nommée par le journal d'événements [4/4]), [FREE-SANS-TYPE] (dev.12 kit — le HMODULE en POINTEUR, l'essai pour TOUTE classe), [RET-NU] (dev.11 kit — mov eax, 1 ; ret), [SONDE-EXE] (le faux négatif STRUCTUREL : le chargeur de bibliothèque ne résout JAMAIS les imports d'un EXE — LA LIAISON PROUVÉE PAR LE VIVANT) ; LA VITRINE VIVANTE (0 et 0 aux 10e/11e runs — après six morts, L'APPLICATION NÉE DE TRIADE A VÉCU CHEZ SON UTILISATEUR) ; LE ONZIÈME RUN recoupé 39/39 (T0→T7 TOUT VERT la quatrième fois, LA CASCADE 205 VÉCUE ENTIÈRE la première, la vitrine la seconde) : LE VERT TIENT ENTIER — LA BALISE `loupe 0.1.0` SCELLÉE PAR FAIT DE CARTE (D178 : la dette de la carte soldée par la RÉGÉNÉRATION DES NOTATIONS [18/18 == la pièce OCTET POUR OCTET, 587 → 0], la cristallisation 26 × 10/10, l'anti-rollback ARMÉ, loupe.exe INTACT 054de960…) — LA MÉTHODE TRIADE ENTIÈRE PROUVÉE PAR LA CRÉATION ; LA SUITE COMMANDÉE (D179) : la version 0.1.1-dev.1 née de la recomposition — la dette [R10-PÉRIMÉE] SOLDÉE À LA NAISSANCE (17 sommes rafraîchies à la vérité des blocs, le qword porté 0x00010101, 0 octet de code changé), le douzième run attendu : la balise `loupe 0.1.1` sur le vert recoupé |

M0 est le jalon existentiel — il prouve la chaîne notation, octets, exécutable, exécution
sans compilateur ; il est franchi. M2 est le jalon de vérité — le patch à chaud sur code
en exécution a motivé l'architecture ; il est franchi : la boucle complète (bascule
pendant le trafic, vérification memcmp, retour arrière, re-vérification) a été
démontrée sur machine réelle le 27 octobre 2026 (D43), au terme de la campagne
d'instrumentation relatée en § 8.4 — huit itérations, huit classes de défauts nommées,
zéro régression possible (chaque classe est gardée par une falsification). M6 et M7 transforment la portabilité de promesse en propriété
démontrée, en isolant chaque variable ; la suite de conformité par profil (§ 8.2) en est
désormais le critère d'acceptation explicite. M8 et M9 sont les additions mesurées du
programme d'après M7 (D160) : la fondation d'abord — le domaine `sys` est la
condition d'une pile TLS 1.3 qui n'émettrait plus par l'IAT userland ; chaque
famille s'appuie sur les résultats mesurés de la précédente. M10 est l'épreuve de
la MÉTHODE ENTIÈRE (D171) : non plus une capacité, mais une application réelle
neuve — l'outil du quotidien du projet — développée de l'intention à l'octet
livré, chaque geste prouvé — ET ELLE EST FRANCHIE (D178) : onze runs terrain,
onze leçons, la balise `loupe 0.1.0` scellée sur le onzième run recoupé — la
création a vécu chez son utilisateur ; la version 0.1.1 (D179) poursuit : la
dette [R10-PÉRIMÉE] soldée à la naissance, le douzième run attendu.

## 19. Correspondance des versions

### 19.1 Traçabilité des évolutions

| # | Évolution | En v0.3 | En v0.4.0 | Statut |
|---|---|---|---|---|
| 1 | Couche I normalisée | « contrats légers » sans gabarit | gabarit § 2 : identifiants stables, pre/post, invariants, cas d'échec, vecteurs | renforcé (D19) |
| 2 | Taxonomie des défauts | absente (analyse dans la seule démonstration) | classes T1–T6, § 3 | nouveau (D19) |
| 3 | Threat model minimal | 7 menaces | 13, dont 6 nouvelles, § 15.1 | étendu (D20) |
| 4 | R10 renforcée | checksums au lancement | + signature du manifeste, anti-rollback, conformité environnement, fail-closed explicite | renforcé (D20) |
| 5 | Optimisation prématurée | interdite implicitement (ordre lexicographique) | interdiction normative R11 | explicité (D21) |
| 6 | Journal d'optimisation | pratique de la démonstration (D15 RoomEq) | format normalisé OPT-NN, § 11 | officialisé (D21) |
| 7 | Fragmentation de la carte | 4 fragments (D4) | + norme « aucune opération ne lit tout », § 14 | consolidé (D24) |
| 8 | Localisation par intention | étape 2 de la boucle, implicite | interdiction du balayage formalisée, § 7 | renforcé (D24) |
| 9 | Budgets de tokens | 40 / 3 000 / 6 000 | inchangés, instrumentés au tableau de bord | consolidé (D24) |
| 10 | Suite de conformité par profil | implicite (7 éléments du profil) | suite obligatoire, § 8.2 | nouveau (D22) |
| 11 | Parité inter-profils | critères M6/M7 dispersés | définition formelle à contrat constant, § 8.3 | formalisé (D22) |
| 12 | Reverse-specs | absente (pratique née de la démonstration) | officialisées, § 10 | officialisé (D23) |
| 13 | Pré-versions | absente (pratique `-dev.1`) | dev.N / rc.N / X.Y.Z, § 9 | officialisé (D23) |
| 14 | Fixtures partagées | absente (pratique installateur) | contractuelles, § 2.4 | officialisé (D23) |
| 15 | Traçabilité I ↔ C ↔ B ↔ tests | implicite | table normative + audit mécanique, § 4.2 | formalisé (D24) |
| 16 | Journal des décisions | pratique (« mode de gouvernance ») | format normalisé, § 17.1 | normalisé (D24) |
| 17 | Tableau de bord de conformité | indicateurs dispersés (plan M0-M7) | métriques unifiées mesurables, § 17.2 | nouveau (D24) |

### 19.2 Modifications explicitement rejetées

Conformément au cahier de révision, les modifications suivantes — demandées ou
envisageables — ont été examinées et **rejetées, donc non appliquées** :

| Modification | Verdict | Motif |
|---|---|---|
| Modifier la hiérarchie Sécurité > Performance > Optimisation > Coût en tokens | rejetée | invariant de révision (D19) — c'est la condition même de l'arbitrage |
| Introduire une couche d'abstraction à l'exécution (bytecode portable, VM) | rejetée | trahit la fonction objectif Performance (D14) ; la parité s'obtient par vérification, pas par couche |
| Promettre la portabilité universelle immédiate | rejetée | la portabilité se vérifie par profil (M6/M7), elle ne se déclare pas |
| Introduire des mécanismes de furtivité face aux EDR | rejetée | hors périmètre assumé (§ 1.2) — transparence totale de l'outil |
| Affaiblir R5, R8, R9 ou R10 | rejeté | la révision ne contient que des renforcements ; les énoncés v0.3 de R1-R9 sont repris à l'identique |
| Anti-rollback par contrôle en ligne au chargement | rejetée | R10 doit échouer proprement hors ligne — aucune dépendance réseau |
| Optimisation validée sans mesure | rejetée | R11 : hot path + mesure avant/après + contrat stable |

### 19.3 Correspondance v0.4.0 → v0.5.0

| # | Évolution | En v0.4.0 | En v0.5.0 | Statut |
|---|---|---|---|---|
| 1 | Validation terrain | constats dispersés au journal des décisions | couche normée : boucle d'évidence, journal d'exécution, sondes contractualisées, diff chirurgical (§ 8.4) | nouveau (D43) |
| 2 | Taxonomie des défauts | classes T1–T6 (contrat non écrit) | + classes X1–X8, défauts invisibles à l'émulation (§ 8.5) | étendu (D35–D42) |
| 3 | État des jalons | M0 planifié, M1-M7 à venir | M0, M1, M2 franchis — preuves terrain archivées (§ 18) | constaté (D26, D32, D43) |
| 4 | Budgets de tokens | 40 / 3 000 / 6 000 (cibles) | 64 / 3 000 / 6 000 — corrigé et mesuré : 51 / 719 / 1 088 (D31) | corrigé (D31) |
| 5 | Suite de conformité | définie (7 éléments, 124 contrôles) | exécutée à chaque scellage rc/final — 124/124 sur le profil primaire | mesuré (D39–D43) |
| 6 | Volume d'oracle | 12 000 cas par bloc critique (référence) | campagnes effectives consignées : M1 76 010 cas, M2 50 533 cas, démo 86 cas | consolidé |
| 7 | Preuves terrain | non normées | archives brutes (journaux octet-exacts, empreintes) référencées au journal des décisions | officialisé (D43) |
| 8 | Fuzzing | mentionné (menace « fuzzing boîte noire », § 15.1) | jalon M3 ouvert : fuzzing à propriétés sur la surface d'entrées non fiables (D45) | structuré |

### 19.4 Modifications explicitement rejetées (v0.5.0)

Conformément au cahier de révision, les modifications suivantes ont été examinées et
**rejetées, donc non appliquées** :

| Modification | Verdict | Motif |
|---|---|---|
| Ajouter une règle R12 « validation terrain obligatoire » | rejetée | la boucle d'évidence découle de R5 et des critères de jalon ; une règle de plus diluerait le corpus sans rien exiger de nouveau |
| Étendre le fuzzing à tous les blocs scellés | rejetée | M3 cible la surface d'entrées non fiables ; les blocs à appelants de confiance relèvent des vecteurs existants (§ 8.1) |
| Reconstruire les artefacts scellés 0.2.0 / 0.3.0 pour la documentation | rejetée | les balises finales sont immuables (§ 9) ; la documentation cite les empreintes |
| Fusionner les classes X dans les classes T (T7–T14) | rejetée | les deux familles appellent des remèdes distincts : écrire le contrat (T) contre enrichir le modèle d'environnement et falsifier (X) |

### 19.5 Correspondance v0.5.0 → v0.5.1

| # | Évolution | En v0.5.0 | En v0.5.1 | Statut |
|---|---|---|---|---|
| 1 | Phrases maîtresses | instruction de cérémonie seule (D27/D30) — quatre réinitialisations du poste ont montré la limite | coffre-fort TRIADE-CF1 : conteneur chiffré par projet, export/import, restauration post-réinitialisation (§ 17.3, FORMAT_CARTE § 11) | nouveau (D75) |
| 2 | État des jalons | M0–M2 constatés, M3 ouvert | M3 franchi 28/10/2026 — campagne million (D72), conformité permanente (D73), scellage 0.4.0 (D74) | constaté (D72–D74) |
| 3 | Modèle de menace | 13 menaces, dont le vol de l'export de continuité | + vol du coffre-fort des phrases — sans la phrase de contrôle, indéchiffrable | étendu (D75) |

Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée. Les
alternatives rejetées à D75 : conserver la seule instruction de coffre développeur (le
statu quo que les quatre réinitialisations ont démenti) ; stocker les phrases en clair
dans `.keys/` (l'état opérationnel du poste n'est pas un coffre) ; embarquer la graine
Ed25519 dans le coffre (contraire à D30 — jamais confiée) ; confier le conteneur au seul
gestionnaire de mots de passe du développeur sans copie de coffre projet (la continuité
exige les deux copies, le conteneur étant indéchiffrable sans la phrase).

### 19.6 Correspondance v0.5.1 → v0.5.2

| # | Évolution | En v0.5.1 | En v0.5.2 | Statut |
|---|---|---|---|---|
| 1 | Garde de la phrase de contrôle | détenue par le seul développeur, jamais stockée, affichée une seule fois (D75) | sauvegardée durablement dès production : `PHRASE-CONTROLE-COFFRE.txt` au dépôt (git + GitHub + miroir Drive) et au racine du coffre Drive, AVANT toute autre action ; le fichier est la remise — HISTOIRE DATÉE du 4 au 19 novembre 2026 (§ 17.3, FORMAT_CARTE § 11) | modifié (D81, du 4 au 19 novembre 2026, amendé D223) |
| 2 | Menace « vol du coffre-fort » | sans la phrase, indéchiffrable | la phrase vit sur le coffre Drive partagé par lien : confidentialité au repos ramenée au contrôle d'accès du dossier ; mitigation première = restreindre le partage ; une phrase commise en git y demeure à vie, la rotation reste le remède | étendu (D81) |
| 3 | État des jalons | M0–M3 franchis, M4 à venir | M4 ouvert (D77 — couche I écrite-avant-code : huit spécifications tls + deux révisions http) ; M0–M3 inchangés | constaté (D77) |

Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée. Les
alternatives rejetées à D81 : conserver la remise par affichage unique (le statu quo que
la session morte de D80 a démenti — la phrase ne vivait plus que dans le bac à sable) ;
sceller la phrase de contrôle sous une phrase antérieure (déplace le problème : la phrase
de secours exigerait sa propre garde) ; exporter la seule copie chiffrée du coffre sans
garder la phrase (le conteneur indéchiffrable protège de l'exposition, pas de la perte —
or c'est la perte qui est le risque vécu) ; restreindre d'office le partage du dossier
Drive (décision appartenant au développeur, hors du champ de l'agent — consignée en
recommandation, § 17.3).

### 19.7 Correspondance v0.5.2 → v0.6.0

| Évolution | En v0.5.2 | En v0.6.0 | Statut |
|---|---|---|---|
| Coffre-fort | conteneur TRIADE-CF1 à phrase (D75), garde durable de la phrase (D81) | chaîne complète : CF2 (clé maîtresse Shamir, cinq gardes seuil 3, sentinelle/porte D120) puis CF3 (serrure à triple scellement, piège sur média, cycle en deux actes, sentinelle instantanée par invocation) — le coffre réel a migré par cérémonies (30–31/10/2026) ; un coffre neuf naît CF3 | ajouté (D86, D106, D121, D127, D133) |
| Souveraineté de l'intention | exigence consignée (D87) | le sceau de l'Intention vit : dix arbres signés par la clé Ed25519 hors-ligne, cérémonie autoportée, gardes de build et de patch, re-cérémonie réelle (D126) | ajouté (D87, D105, D126) |
| Cérémonies et kit | non couverts | maître de cérémonie graphique, trio D122, kit Drive identique au miroir par construction (D130), lanceurs Windows/POSIX | ajouté (D107–D132) |
| Attestation TEE (axe 1) | exigence consignée (D85) | inchangée — l'infrastructure sans racine de confiance ne peut pas la satisfaire et le dit | constaté (D133) |
| Menaces | vol du coffre, rollback binaire | lignes nouvelles : expropriation, evil maid, roll-back du couple conteneur + piège | étendu (D133) |
| Jalons | M4 ouvert (D77) | M4 franchi (0.5.0 scellée, terrain.17-D) ; M5 ouvert (D133) | constaté |

Modifications explicitement rejetées (v0.6.0) : supprimer la sentinelle en guise de
simplification — rejeté : l'exigence D120 est réalisée *par invocation* (la sentinelle
instantanée est la serrure) ; ce qui meurt est le démon résident, usurpable. N'imposer
la chaîne de migration aux coffres neufs — rejeté : un coffre neuf naît CF3. Signer la
présente spécification avant passation — reporté : les sources `docs/` sont hors
périmètre du sceau courant (modèle par-version, `v06/I/README.md` § 1). Passer à
v0.6.0 en attendant l'axe 1 — arbitrée par le développeur : la passation se fait avec
l'axe 1 consigné (D133).

### 19.8 Correspondance v0.6.0 → v0.6.1

| Évolution | En v0.6.0 | En v0.6.1 | Statut |
|---|---|---|---|
| Niveau de naissance d'un coffre neuf | un coffre neuf naît CF3 — `init` direct à l'époque 1 (D133) | le niveau (CF1/CF2/CF3) est arbitré par le développeur à la création de son projet : les trois naissances, le guide et les obligations par niveau (§ 12.5) ; la chaîne de migration demeure disponible à tout moment | révisé (D137) |
| Le coffre réel | CF3 (époque 1, checksum `0cc89a96`) | inchangé — la révision est un droit de création, pas un geste sur le coffre vivant | constaté |
| Chaîne PDF et Livre du Coffre | spécification v0.6.0 (37 p.) ; Livre v1.0 | chaîne spec_v061 (l'erratum typographique « tbp] » page 31 réparé au passage) ; Livre v1.1 — runbook « coffre neuf » et FAQ terrain alignés sur D137 | révisé (D137) |
| Le reste de la spécification | — | inchangé : aucune autre règle, aucune couche d'exécution ajoutée, hiérarchie inchangée | constaté |

Modifications explicitement rejetées (v0.6.1) : imposer CF1 par défaut en guise de
souplesse — rejeté : remplacer une imposition par une autre ne rend pas la décision au
développeur. Rendre le niveau mutable sans cérémonie — rejeté : le niveau change par
MIGRATION uniquement, acte explicite et fail-closed (l'anti-retour d'époque et le
verrou croisé demeurent). Promouvoir l'`init` de CF2 (laboratoire) en cérémonie réelle
dans cette révision — rejeté : la spécification scellée CF2 fait foi ; la naissance
CF2 passe par `init` CF1 puis `migrer`, tout est prouvé ; l'arbitrage est consigné si
le besoin naît. Toucher au code des trois outils — rejeté : les trois actes de
création existent et sont prouvés ; c'est le droit de choisir qui manquait, pas la
mécanique.

### 19.9 Correspondance v0.6.1 → v0.7.0

| Évolution | En v0.6.1 | En v0.7.0 | Statut |
|---|---|---|---|
| Programme d'après M7 | clause de clôture : syscalls directs et TLS 1.3 pur « hors périmètre courant » | le programme D160 entre en spécification : la clause est LEVÉE NOMMÉMENT pour les deux premières familles — le jalon M8 (domaine `sys`) franchi, le jalon M9 (domaine `tls13`) ouvert ; les profils additionnels demeurent hors périmètre | révisé (D160, D166) |
| Sceau de l'Intention | dix arbres sous le sceau | treize arbres (m0–m8, tls13, demo, terrain, v06) ; les cérémonies d'ère entrent au protocole : la dette nommée à la naissance (D166 règle 8), la charge préparée au geste qui sert la main (D168), la continuité de clé prouvée par le déterminisme Ed25519 (D163) | étendu (D162, D166, D168) |
| État des jalons | M0–M6 franchis, M7 ouvert | M0–M8 franchis (balises 0.2.0 à 0.9.0), M9 ouvert — la cérémonie de l'ère M9 passée (garde 13/13) | constaté (Entrées 155–168) |
| Chaîne PDF | spec_v061 | chaîne spec_v070 ; l'archive v0.6.1 demeure (dernier build consigné : sha256 `4aac10f1…`, 984 555 o) | révisé (D169) |

Modifications explicitement rejetées (v0.7.0) : réviser la spécification à chaque
franchissement de jalon — rejeté : le versionnement suit les RÉVISIONS, jamais les
franchissements (l'état des jalons vit aux sources de travail, régénérées à chaque
geste ; la v0.7.0 consolide un PROGRAMME, pas un simple constat). Signer les
sources `docs/` sous le sceau courant — rejeté : le modèle par-version demeure
(`v06/I/README.md` § 1). Ouvrir les profils additionnels (`aarch64-macos-macho`,
`wasm32-wasi`) dans la même révision — rejeté : chacun répétera M6/M7 sur
résultats mesurés, hors périmètre. Fusionner les cérémonies d'ère dans la cérémonie
CF3 — rejeté : trois gardes, trois menaces ; le sceau garde l'intention, le coffre
garde les secrets.

### 19.10 Correspondance v0.7.0 → v0.8.0

| Évolution | En v0.7.0 | En v0.8.0 | Statut |
|---|---|---|---|
| Programme d'après M9 | M9 ouvert : couche I complète, la cérémonie passée, les chantiers (b) à (f) attendent | M9 FRANCHI : les 28 blocs notés-mesurés-prouvés, le septième run terrain vert recoupé, LA SESSION RÉELLE (la ligne applicative chiffrée avec un serveur réel), la finale `1.0.0` scellée sur recoup exigé comme pièce (D170) | révisé (D170) |
| Le test grandeur nature | — | LE TGN ouvert (D171) : « Loupe », l'éditeur hexadécimal au panneau d'empreintes — coder une application réelle NEUVE entièrement avec TRIADE ; le domaine `loupe` fondé, la couche I de 18 spécifications posée (D172) et les QUATRE chantiers de notation accomplis (D173/D174/D175 : les 18 blocs notés-mesurés-prouvés, la table de routage de loupe-09 étendue en révision nommée) | nouveau (D171–D175) |
| Sceau de l'Intention | treize arbres, les cérémonies d'ère M8/M9 passées | treize arbres + LA DETTE DU QUATORZIÈME nommée (l'ère du TGN : l'arbre `loupe` et le registre figé étendu attendent la clé hors-ligne AVANT tout build — § 13.5) ; le garde demeure à 13/13 jusque-là | étendu (D166/D171/D175) |
| Projet fils COFFRE-FORT | développement différé (D135) | DÉGELÉ en parallèle du TGN (D171) : le fils vit son rythme, la frontière fondatrice intacte — aucun code TRIADE forké, aucune dépendance vivante | révisé (D171) |
| Chaîne PDF | spec_v070 | chaîne spec_v080 ; l'archive v0.7.0 demeure | révisé (D176) |

Modifications explicitement rejetées (v0.8.0) : réviser la spécification à chaque
franchissement — rejeté : le versionnement suit les RÉVISIONS (la v0.8.0 consolide
le PROGRAMME d'après M9 : M9 franchi ET le TGN ouvert, deux moteurs d'une même
passation). Mettre l'application « Loupe » sous le sceau AVANT la cérémonie —
rejeté : le garde suit le calendrier de la cérémonie, jamais l'inverse (§ 13.5).
Ajouter un profil de cible pour le TGN — rejeté : le profil primaire
`x86-64-win11-pe` est l'épreuve ; l'universalité est déjà prouvée (M6/M7).
Sceller la 0.1.0 de Loupe au build — rejeté : la balise de développement naît au
build (geste de BUILD jamais scellage, miroir M6/M7/M8) ; la 0.1.0 se scellera sur
le run terrain vert recoupé.

### 19.11 Correspondance v0.8.4 → v0.9.0

| Évolution | En v0.8.4 | En v0.9.0 | Statut |
|---|---|---|---|
| Jalon M10 (le TGN « Loupe ») | ouvert : cinq runs vécus, cinq défauts nommés (les refus du chargeur, [CADRE-NÉ], la classe des arguments pile, [SESSION] -7 — la pièce acquittée), la retouche dev.6 au kit seul | FRANCHI : ONZE RUNS TERRAIN, ONZE DÉFAUTS NOMMÉS, ONZE RETOUCHES DOCUMENTÉES ([HINSTANCE-PEB], [D54-QUATRIÈME] + [EAX-SANS-SIGNE], [OFT-QWORD], [FREE-SANS-TYPE], [RET-NU], [SONDE-EXE] — la liaison prouvée par le vivant) ; LA VITRINE VIVANTE (0 et 0 aux dixième et onzième runs — l'application née de TRIADE a vécu chez son utilisateur) ; le onzième run recoupé 39/39 | révisé (D178, Entrées 209–219) |
| La balise `loupe 0.1.0` | attend le vert entier (la dette de la carte nommée : génération 13/dev.5, la pièce dev.8) | SCELLÉE PAR FAIT DE CARTE : la dette de la carte soldée par la RÉGÉNÉRATION DES NOTATIONS (18/18 == la pièce octet pour octet, l'écart 587 → 0), la cristallisation 26 × 10/10, la re-signature à la graine durable (le témoin ne bouge pas), l'anti-rollback ARMÉ, loupe.exe INTACT (054de960…) — le même binaire que le onzième run a couru | révisé (D178) |
| La dette [R10-PÉRIMÉE] | nommée au scellage (17 sommes de l'ère dev.5 à la porte de la pièce — réparable à 0.1.1+, jamais un hot-fix d'un scellé) | SOLDÉE À LA NAISSANCE : la version `0.1.1-dev.1` COMMANDÉE (D179) naît de la recomposition même — les 17 sommes rafraîchies à la vérité des blocs, le qword porté 0x00010101, 0 octet de code changé (R4/R7) ; la carte GÉNÉRATION 17 ; le kit 0.1.1-dev.1 déposé au coffre `/test`, LE DOUZIÈME RUN ATTENDU — la balise `loupe 0.1.1` se scellera sur le vert recoupé (le miroir D165/D170) | révisé (D179) |
| Programme d'après M10 | — (le jalon attend son scellage) | OUVERT À LA COMMANDE DU DÉVELOPPEUR : la consolidation v0.9.0 (le modèle D169/D176), la version 0.1.1 (D179) ; le projet fils COFFRE-FORT demeure dégélable au rythme du développeur (D135 amendée par D171) | nouveau (D179) |
| Chaîne PDF | spec_v084 (née spec_v083 — les révisions de terrain v0.8.1 à v0.8.4) ; les archives v0.7.0 à v0.8.3 demeurent | chaîne spec_v090 (née spec_v084) ; les archives v0.7.0 à v0.8.4 demeurent | révisé (D180) |

Modifications explicitement rejetées (v0.9.0) : rafraîchir la table R10 au scellage
de la 0.1.0 — rejeté : LA PIÈCE ne bouge jamais au scellage (fait de carte) ; la
dette se nomme et se paie à la version suivante, jamais un hot-fix d'un scellé
(D178). Sceller la 0.1.1 au build sans le run terrain — rejeté : le miroir
D165/D170 exige le verdict du recoup vert COMME PIÈCE, la porte est de processus.
Rouvrir le jalon M10 pour la 0.1.1 — rejeté : M10 est clos sur sa balise ; la 0.1.1
est une version de maintenance à contrat stable (R4), pas une réépreuve du jalon.
Modifier les notations D172–D175 pour la 0.1.1 — rejeté : le code est
byte-identique au vécu des onze runs ; les notations décrivent LA PIÈCE (R2/R5).

### 19.12 Correspondance v0.9.0 → v0.10.0

| Évolution | En v0.9.0 | En v0.10.0 | Statut |
|---|---|---|---|
| Édition académique | — (le manuscrit n'existe pas ; l'article v0.4 de la démonstration RoomEq demeure) | LE MANUSCRIT IMRAD en anglais (résumé français), quatre questions de recherche, les données réelles du journal extraites par script, l'auteur humain unique, l'agent IA en méthodes et remerciements, les déclarations Ethics/Data/Limitations (D182) | nouveau (D182) |
| Formulation | « le compilateur disparaît » ; « code volé inexploitable » ; majuscules emphatiques | « aucune chaîne de traduction optimisante ni opaque ; assemblage WYSIWYG vérifié par round-trip » ; « l'évolution du code volé est bloquée, son exécution ne l'est pas » ; termes standards (key ceremony, signed manifest, sealed build) ; D19 requalifiée politique de projet explicite | révisé (D182) |
| Garde de la phrase de contrôle | D81 : la phrase en clair au dépôt et au coffre Drive (PERTE > EXPOSITION) | D81 DEMEURE la décision active ; la PROPOSITION D183 (séquestre chiffré : clé hors-ligne ou parts Shamir à seuil, analyse chiffrée perte/exposition) documentée — NON appliquée au coffre réel, aucune clé touchée | proposition (D183) |
| Annexe A (empreintes de gouvernance) | md5 des 15 modules du coffre (contenu canonique LF, D133) | sha-256 des 15 modules (la même méthode, D184) ; md5 demeure une fonctionnalité d'affichage de Loupe (loupe-06) — AUCUN octet de la pièce ne change ; les preuves historiques md5 demeurent | révisé (D184) |
| Livrables d'édition | — | `TRIADE_soumission_v0.10.0.zip` (cinq fichiers au plus, readme inclus, le manuscrit en pdf) et `TRIADE_complet_v0.10.0.zip` (l'intégralité) | nouveau (D182) |
| Chaîne PDF | spec_v090 (née spec_v084) ; les archives v0.7.0 à v0.8.4 demeurent | chaîne spec_v100 (née spec_v090) + la chaîne manuscrit_v100 ; les archives demeurent | révisé (D182) |

Modifications explicitement rejetées (v0.10.0) : appliquer D183 au coffre réel
sans le geste du développeur — rejeté : la proposition est documentée, l'arbitrage
PERTE > EXPOSITION demeure la décision active (D81). Réécrire les empreintes md5
des preuves historiques en sha-256 — rejeté : les preuves sont immuables, la
migration ne porte que sur la documentation de gouvernance vivante. Toucher à la
pièce Loupe (le panneau md5) — rejeté : md5 y est une fonctionnalité d'affichage
(RFC 1321 notée à la spécification loupe-06), l'artefact scellé ne bouge jamais.
Modifier les règles ou la hiérarchie — rejeté : l'édition consigne, elle ne
légifère pas (D180).

### 19.13 Correspondance v0.10.0 → v0.11.0

| Évolution | En v0.10.0 | En v0.11.0 | Statut |
|---|---|---|---|
| Mutation testing | — (non mesuré) | 832 mutants : 694 tués (83,4 %) par les instruments existants ; familles crypto 100 % ; 138 survivants nommés | nouveau (D185) |
| Fuzzage guidé par couverture | — (le fuzzing M3 à volume, non guidé) | loupe-01 : 60,5 % de couverture, zéro crash, zéro canari violé ; http-10 : 358 instructions, zéro faute (graines fixées) | nouveau (D185) |
| Sûreté mémoire | « non prouvée » (la limite déclarée) | BORNÉE : 2 098 accès classés, zéro hors-cadre, 463 non résolus nommés — l'analyse bornée, pas une preuve | renforcé (D185) |
| Temps constant | « non analysé » (la limite déclarée) | STRUCTUREL : traces indépendantes du secret (dudect d'émulation) ; le temps réel NON MESURÉ — la limite demeure, nommée | renforcé (D185) |
| Benchmarks | — | sha256 : 4 524 ins/op contre 69 132 (gcc -O2) au même émulateur, facteur 15,3 ; md5/aes écartés par l'auto-vérification | nouveau (D185) |
| Indépendance de l'oracle | — | zéro divergence par voies distinctes (décimal, os.urandom, tripartite) ; le second AGENT à venir | nouveau (D185) |
| Spécification CSPRNG | manquante (nommée par la commande) | le brouillon tls13-29 (générateur OS-hôte via le kit, reseed noyau, fail-closed, KIT96) — la cérémonie d'ère attend le développeur | nouveau (D186) |
| Vecteurs RFC 8446 | — (le RFC 8448 déjà rejoué au harnais poignée) | les constantes natives (DOWNGRD, HRR, types, suite, groupe) au corpus partagé, le plan recroisé | nouveau (D186) |
| Chaîne PDF | spec_v100 (née spec_v090) + manuscrit_v100 | chaîne spec_v110 (née spec_v100) + manuscrit_v110 ; les archives demeurent | révisé (D185) |

Modifications explicitement rejetées (v0.11.0) : entrer la spec CSPRNG à
l'arbre signé sans la cérémonie — rejeté : la clé hors-ligne appartient au
développeur (D87/D177). Mesurer le temps réel des blocs — rejeté pour cette
édition : le terrain de mesure n'est pas au laboratoire, la limite est
consignée. Publier les chiffres md5/aes du banc — rejeté : l'auto-
vérification a attrapé la référence fautive, jamais un chiffre faux.

### 19.14 Correspondance v0.11.0 → v0.12.0

| Évolution | En v0.11.0 | En v0.12.0 | Statut |
|---|---|---|---|
| Modèle formel CF3 | — (hors périmètre) | quatre propriétés PROUVÉES DANS LE MODÈLE (154 états, 1 152 transitions, adversaire ≤ 2 éléments) ; hypothèses A1-A5 explicites ; le hors modèle nommé | nouveau (D187) |
| Modèle de menace | tableau unique (§ 15.1) | DEUX PLANS : IP (remédiable) / sûreté d'exécution (irrémédiable) ; l'ordre intra-sécurité explicite ; D81↔D183 chiffrée (facteur ≈ 40) | révisé (D188) |
| Cristallisation | règle R6 (10 rebuilds) | le seuil JUSTIFIÉ par le SPRT (α = 1,08 × 10⁻³) — le seuil DEMEURE | évalué (D189) |
| Réplication | « N=1, la limite déclarée » | le protocole PROPOSÉ (trois axes, grille T/X, κ de Cohen ≥ 0,61) — jamais exécuté | proposé (D189) |
| Manifestes de kit | md5 (le manifeste du kit de cérémonie) | sha256 (maj_kit.py, la suite de D184) ; les kits livrés demeurent ; md5 à l'idempotence et à l'affichage | révisé (D187) |
| Chaîne PDF | spec_v110 + manuscrit_v110 | chaîne spec_v120 (née spec_v110) + manuscrit_v120 | révisé (D187) |

Modifications explicitement rejetées (v0.12.0) : remplacer le seuil de 10 par
le critère séquentiel à 5 — rejeté : le seuil est la politique de projet,
l'analyse la justifie sans la remplacer. Exécuter la réplication — rejeté :
le protocole est proposé, l'arbitrage appartient au développeur. Modifier la
hiérarchie D19 — rejeté : la restructuration en deux plans porte l'ordre
intra-sécurité en POLITIQUE EXPLICITE, la hiérarchie demeure la règle.

### 19.15 Correspondance v0.12.0 → v0.13.0

| Évolution | En v0.12.0 | En v0.13.0 | Statut |
|---|---|---|---|
| Incohérences documentaires | onze runs au § 1.10, « Fig. 5 », comptes arrondis, Table 6 tronquée à la main | douze runs (D181), « Table 5 », comptes exacts en macros, Table 6 RÉGÉNÉRÉE anti-troncature | corrigé (D190) |
| Cristallisation | « α = 1,08 × 10⁻³, 46× plus strict » (des rapports de vraisemblance mal étiquetés) | P(sceller\|q) = (1−q)ⁿ : 3,1 %/0,098 % à q = 50 %, 32× ; quantiles 1,87σ/3,10σ ; l'IC95 exact de 11/12 ; la règle de comptage opérationnelle | reformulé (D190) |
| Benchmark | « facteur 15,3 » (4 524 contre 69 132) | l'opération complète : 75 983 contre 69 132 (-O2) et 77 505 (-Os) — le facteur RETIRÉ, la parité ISA au baseline constatée | audité (D191) |
| Neutralité | « no anti-analysis » (manuscrit) contre l'anti-debug léger (spec) non réconciliés | l'arbitrage D190 : documenté honnêtement dans les DEUX documents ; la conséquence D81 au modèle de menace ; le M7 requalifié (qemu TCG, fence.i non prouvé sur silicium) | arbitré (D190) |
| Séquestre D183 | la proposition documentée (D183), la conséquence D81 absente du modèle de menace | la conséquence D81 consignée (deux éléments trivialement disponibles) ; le kit de cérémonie PRÉPARÉ sans l'appliquer (l'outil CF2 D120, l'autotest VERT, le LISEZMOI, les listes de contrôle) ; la frontière D105/D81 du clone | préparé (D192) |
| État de l'art | design by contract, N-version, DO-178C, supply-chain, live patching, repo-maps | + LLM Compiler, CompCert, Kitsune/POLUS, SWE-agent, sim-to-real (Jakobi/Peng), hardware-in-the-loop (Bacic) — la revendication scopée, RQ3 recadrée | étendu (D192) |

Modifications explicitement rejetées (v0.13.0) : retirer l'anti-debug de la
spécification — rejeté (le mécanisme existe dans l'œuvre scellée, le retirer
du document le falsifierait) ; corriger les décisions historiques en place —
rejeté (le journal est append-only, les corrections vivent en décisions
nouvelles D190-D192) ; masquer le retrait du facteur 15,3 — rejeté (la
correction est publiée avec son mécanisme).

### 19.16 Correspondance v0.13.0 → v0.14.0

| Évolution | En v0.13.0 | En v0.14.0 | Statut |
|---|---|---|---|
| Comparaison compilateur | le facteur 15,3 retiré par l'audit (une mesure d'émulation) | le bras de référence PRÉ-ENREGISTRÉ : zéro divergence aux contrats, sha-256 paritaire à travail égal, la mutation au même degré (H4) | mesuré (D195) |
| RQ2 | les valeurs M1 historiques seules | les distributions de bout en bout (580/2 143/3 510, la baseline naive 300 304, le raisonnement estimé nommé) — M1 demeure historique | re-mesuré (D195) |
| Indépendance de l'oracle | les voies distinctes (v0.11.0) | l'instance isolée : 128 constantes, zéro divergence ; l'écart de famille nommé (une seule famille au labo) | exécuté (D195) |
| Survivants de mutation | 138 survivants nommés (83,4 %) | le re-jeu aux composition-killers : 93,3 %, tls13/sys à 100 %, 56 loupe nommés | re-jeué (D195) |
| Kits terrain | — | le kit du bras C préparé, EN ATTENTE du geste du développeur | en attente |

Modifications explicitement rejetées (v0.14.0) : mesurer sans le
pré-enregistrement — rejeté (la fraude que CA5 interdit) ; remplacer les
valeurs M1 — rejeté (les deux ères coexistent au rapport) ; extrapoler
le raisonnement à la mesure — rejeté (l'estimation est nommée).

### 19.17 Correspondance v0.14.0 → v0.15.0

| Évolution | En v0.14.0 | En v0.15.0 | Statut |
|---|---|---|---|
| Le modèle formel | prouvé BORNÉ (époques ≤ 3, le plafond de l'explorateur) | PROUVÉ NON BORNÉ (l'invariant inductif I, la préservation par les 13 règles, la translation δ) | livré (D198) |
| La fidélité du portage | — | D187 reproduit EXACTEMENT (154/1 152), bornes étendues zéro hors I | livré (D198) |
| Le raffinement | — | 34 pas rejoués contre l'implémentation, ZÉRO ÉCART, les chemins d'échec inclus | livré (D198) |
| Les statuts de preuve | « prouvé dans le modèle » (borné, la nuance dans le texte) | SYSTÉMATIQUES : prouvé non borné / prouvé borné / en attente de run matériel | livré (D198) |
| La table des preuves du manuscrit | générée mais JAMAIS RENDUE (le flot rejeté silencieusement) | LONGTABLE : les 34 lignes rendues | guéri (D198) |
| Les kits matériels | le kit terrain du bras C (en attente) | TROIS kits (dudect temps réel [l'appel natif validé FIPS], fence.i sur silicium, terrain tiers) — EN ATTENTE | préparés (D198) |
| La réplication | la grille T/X proposée (D189) | la grille FINALISÉE (définitions opérationnelles, exemples vécus), le κ AUTOTESTÉ, les critères INCHANGÉS, les statuts consignés | outillé (D198) |
| La gouvernance | — | le croisement d'attribution RECOUPÉ et CORRIGÉ (D197), la règle du contenu cité, la règle d'archivage des versions | consigné (D197) |

Modifications explicitement rejetées (v0.15.0) : relâcher la moindre
hypothèse A1-A5 au bénéfice de la preuve non bornée — rejeté (la
généralisation porte sur l'ÉPOQUE, jamais sur le modèle symbolique) ;
consigner un résultat matériel d'après l'autotest POSIX du kit dudect —
rejeté (l'autotest éprouve le MÉCANISME, le run appartient au
développeur) ; réécrire les entrées d'hier au sujet du croisement —
rejeté (append-only : la correction vit dans l'Entrée 230 et D197).

## 20. Glossaire

| Terme | Définition |
|---|---|
| Carte | Couche C : index signé et chiffré liant intention et binaire, unique interface de développement de l'agent |
| Bloc | Unité de code machine de 32 à 512 instructions, une responsabilité, un point d'entrée stable |
| Spécification I | Artefact normalisé (§ 2) : identifiant stable, intention, contrat pré/post, invariants, cas d'échec, vecteurs, fixtures, provenance |
| Identifiant stable | Clé `<DOM>-<NN>` d'une spécification I — immuable, jamais réutilisée (miroir de l'adresse stable côté B) |
| Scellage | Acte atomique d'engagement : écriture du bloc, mise à jour de la carte, inscription de l'empreinte |
| Cristallisation | Immuabilité d'un bloc après dix vérifications réussies ; modification dès lors soumise à procédure lourde |
| Pré-version | Segment `dev.N` (oracle vert) ou `rc.N` (candidate terrain) précédant une version finale `X.Y.Z` |
| Oracle éphémère | Implémentation de référence triviale dérivée de la couche I, générée par session et détruite après usage |
| Verrou croisé | Contrôle bilatéral d'intégrité : empreintes des blocs dans la carte, signature de la carte, contrôles au chargement |
| Contrat | Signature typée, pré et post-conditions, invariants et cas d'échec publiés d'un bloc — la partie de I embarquée dans C |
| Fragment | Quart de carte chiffré séparément : localisation, contrats, preuves, builds |
| Profil de cible | Instanciation complète du protocole pour un couple ISA/OS : sept éléments + suite de conformité |
| Suite de conformité | Suite de tests vérifiant les sept éléments d'un profil (§ 8.2) — condition de déclaration de support |
| Parité inter-profils | Équivalence vérifiée par exécution de deux profils sur un même contrat, à paramétrisation près (§ 8.3) |
| Reverse-spec | Spécification I extraite d'un binaire scellé hérité, avec provenance et statut (§ 10) |
| Taxonomie T1–T6 | Classification des défauts de contrat non écrit (§ 3) |
| Journal d'optimisation | Registre normalisé des optimisations mesurées — appliquées ou refusées (§ 11) |
| Fixtures contractuelles | Échantillons partagés d'un contrat externe, portés par la spécification I (§ 2.4) |
| Traçabilité I ↔ C ↔ B ↔ tests | Chaîne complète exigence → index → bloc → défense, auditée mécaniquement (§ 4.2) |
| Tableau de bord de conformité | Métriques mesurables avec cibles, générées à chaque cycle (§ 17.2) |
| Suite cryptographique | Paramètres de l'en-tête de carte — hachage, signature, chiffrement — choisis par le développeur dans une liste blanche |
| Re-cryptage | Migration atomique de la suite cryptographique : recalcul des empreintes, re-chiffrement, re-signature, archivage |
| Export de continuité | Conteneur chiffré et signé regroupant I, B, C et un manifeste — seule forme de transfert de l'état de développement |
| Empreinte de build | Variante binaire unique par livraison et par profil, rendant toute fuite traçable |
| Vecteurs de vérification | Vecteurs dorés, propriétés différentielles et tests de rejet rattachés aux exigences (§ 8.1) |
| Notation | Représentation textuelle des instructions assemblées par le moteur du profil — un média, jamais un langage compilé |
| Round-trip | Contrôle de fidélité : assemblage puis désassemblage d'un bloc, comparaison exacte |
| Validation terrain | Exécution de l'artefact livré sur système réel, preuve archivée — valide le modèle d'environnement de l'oracle (§ 8.4) |
| Journal d'exécution | Fichier de preuves écrit au fil de l'eau par l'artefact ; une ligne n'est écrite qu'après vérification de l'étape qu'elle atteste |
| Sonde de trace | Instrumentation temporaire aux frontières d'un intervalle suspect : journalise des faits vérifiés ; retrait promis dans la spécification (D40, D43) |
| Défaut invisible à l'émulation | Défaut dont le modèle d'environnement de l'oracle ne rend pas compte — classes X1–X8 (§ 8.5) |
| Diff chirurgical | Itération terrain dont l'audit vérifie qu'aucun octet hors des zones autorisées n'a changé |
| Fuzzing à propriétés | Génération d'entrées aléatoires contraintes, vérifiées par propriétés (jamais de crash, domaines de retour, bornes mémoire) — cœur du jalon M3 |
| Coffre-fort des phrases maîtresses | Conteneur chiffré TRIADE-CF1 centralisant toutes les phrases maîtresses d'un projet (D75, § 17.3) — l'outil vit dans le dépôt, le conteneur jamais |
| Phrase de contrôle | Secret ouvrant le coffre-fort — sous séquestre à seuil depuis le 19 novembre 2026 (D223) : répartie en CINQ parts à seuil TROIS, AUCUNE phrase en clair au dépôt ni au coffre Drive, la reconstitution à froid de trois parts l'unique voie (§ 17.3) ; l'histoire D81 (le fichier-remise au dépôt) est datée du 4 au 19 novembre 2026 |

- **Époque** — compteur u64 du coffre CF3, incrémenté à chaque clôture : l'horloge de la métamorphose et le témoin anti-retour.
- **Piège** — la moitié S_piège de la clé CF3, vivant exclusivement sur le média séparé ; sans elle, le déverrouillage est impossible.
- **Sentinelle instantanée** — les cinq vérifications ordonnées qui courent à chaque acte CF3, par invocation : la serrure est le témoin.
- **Sachet** — la pochette physique individuelle : pièges d'époque, copies hors-ligne des fragments, carte papier.
- **Carte du sachet** — fiche où le maître consigne à la main le checksum de chaque clôture : témoin indécevable par logiciel.
- **PORTE D120** — l'exigence de sentinelle vivante au déverrouillage CF2 ; sans moteur de plateforme, avertissement nommé à chaque acte.

## 21. Journal des versions

| Version | Date | Contenu |
|---|---|---|
| v0.15.0 | 12 nov. 2026 | Révision des PREUVES NON BORNÉES ET DU RAFFINEMENT (D197/D198) : le croisement d'attribution des instructions n°5/n°6 recoupé aux métadonnées Drive et corrigé aux gestes (la règle du contenu cité, la règle d'archivage des versions) ; l'invariant inductif (P1-P4 PROUVÉES NON BORNÉES : le plafond d'époque retiré, la préservation par les 13 règles sur 288 formes, la translation δ∈{7,50,1000}, la monotonie inconditionnelle, la fidélité D187 reproduite 154/1 152, les bornes étendues zéro hors I) ; le raffinement modèle↔implémentation (34 pas, zéro écart, les chemins d'échec inclus, cinq époques vécues aux deux niveaux) ; les trois kits de mesure matérielle EN ATTENTE (dudect temps réel à l'appel natif validé FIPS, fence.i sur silicium, terrain tiers Loupe) ; la réplication outillée (grille T/X finalisée, κ autotesté, critères inchangés, statuts consignés) ; les statuts de preuve systématiques ; la dette de la table des preuves du manuscrit guérie (longtable). Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |
| v0.14.0 | 11 nov. 2026 | Révision du PROGRAMME EMPIRIQUE (D193/D194/D195) : le bras de référence compilateur pré-enregistré (zéro divergence aux vecteurs, sha-256 paritaire à travail égal [9 089/9 146], H4 tenue) ; la re-mesure RQ2 en distributions (580/2 143/3 510, la baseline naive 300 304, les valeurs M1 historiques, la lecture défavorable consignée) ; l'indépendance par instance isolée (128 constantes, zéro divergence, l'écart de famille nommé) ; le re-jeu des 832 mutants aux composition-killers (93,3 %, tls13/sys à 100 %, 56 loupe nommés) ; le kit terrain en attente. Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |
| v0.13.0 | 11 nov. 2026 | Révision des CORRECTIONS DE L'ÉDITION (D190/D191/D192) : les incohérences vérifiées une à une (quatorze arbres, douze runs au § 1.10, comptes exacts en macros, Table 6 régénérée anti-troncature, la note TOTAL/brouillons, les renvois recalés) ; les statistiques reformulées (P(sceller\|q) = (1−q)ⁿ, quantiles 1,87σ/3,10σ, l'IC95 exact de 11/12 [0,615 ; 0,998], la règle de comptage opérationnelle) ; le benchmark AUDITÉ — le facteur 15,3 retiré comme artefact de périmètre, les chiffres corrigés (75 983 contre 69 132/-Os 77 505), le M7 requalifié (qemu TCG, fence.i non prouvé sur silicium) ; la neutralité documentaire (l'anti-debug arbitré, la conséquence D81 au modèle de menace, la frontière D105/D81, le kit D183 préparé sans l'appliquer) ; l'état de l'art étendu (huit références vérifiées, la revendication scopée, RQ3 recadrée en garanties silencieuses du compilateur). Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |
| v0.12.0 | 11 nov. 2026 | Révision du MODÈLE FORMEL ET DE LA GOUVERNANCE ASSAINIE (D187/D188/D189) : CF3 modélisé et vérifié par exploration exhaustive — quatre propriétés prouvées dans le modèle (secret sous seuil, refus du roll-back, pas de destruction sur phrase erronée, rayon borné), hypothèses A1-A5 explicites, hors modèle nommé ; le modèle de menace en deux plans (IP/sûreté) avec l'ordre intra-sécurité explicite et la tension D81↔D183 chiffrée ; la cristallisation justifiée par le SPRT (le seuil 10 demeure) ; le protocole de réplication proposé (grille T/X, κ de Cohen) ; les manifestes de kit à sha256 ; le manuscrit v0.12.0 § 4.6. Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |
| v0.11.0 | 11 nov. 2026 | Révision des PREUVES RENFORCÉES (D185/D186) : les six instruments de laboratoire — mutation testing (832 mutants, 83,4 % tués, crypto 100 %, survivants nommés), fuzzage guidé par couverture (loupe-01 60,5 %, zéro crash ; http-10 zéro faute), sûreté mémoire statique bornée (2 098 accès, zéro hors-cadre, 463 non résolus nommés), temps constant d'émulation (structurel, le temps réel non mesuré), benchmarks comparatifs (sha256 facteur 15,3 en instructions contre gcc -O2 au même émulateur ; md5/aes écartés par l'auto-vérification), indépendance de l'oracle (zéro divergence par voies distinctes) ; la spec CSPRNG manquante en brouillon (tls13-29, la cérémonie d'ère attend le geste du développeur) ; les vecteurs RFC 8446 au corpus de fixtures ; le manuscrit v0.11.0 (Results § 4.5 étendu, limites mises à jour). Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |
| v0.10.0 | 11 nov. 2026 | Révision de L'ÉDITION ACADÉMIQUE (D182/D183/D184) : le manuscrit IMRAD en anglais (résumé français) — quatre questions de recherche, les données réelles du journal extraites par script, la formulation corrigée (WYSIWYG par round-trip ; l'évolution du code volé bloquée, son exécution non ; termes standards ; D19 requalifiée politique de projet), l'auteur humain unique, l'agent IA en méthodes et remerciements, les déclarations Ethics/Data/Limitations ; la proposition D183 (séquestre chiffré de la phrase de contrôle — documentée, non appliquée) ; l'annexe A portée à sha-256 (D184 — md5 demeure une fonctionnalité de Loupe) ; les livrables soumission et complet. La balise `loupe 0.1.1` scellée sur le douzième run recoupé (D181) est consignée à la rangée M10. Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |
| v0.9.0 | 11 nov. 2026 | Révision de consolidation du programme d'après M10 (D178/D179) : LE JALON M10 — le test grandeur nature « Loupe » — est FRANCHI (l'application NÉE ENTIÈREMENT DE LA MÉTHODE : onze runs terrain, onze défauts nommés, onze retouches documentées, LA VITRINE VIVANTE chez son utilisateur, le onzième run recoupé 39/39 — la balise `loupe 0.1.0` SCELLÉE PAR FAIT DE CARTE, la dette de la carte soldée par la régénération des notations, la cristallisation 26 × 10/10, l'anti-rollback ARMÉ) : LA MÉTHODE TRIADE ENTIÈRE PROUVÉE PAR LA CRÉATION ; LE PROGRAMME D'APRÈS M10 (D179) : la version `0.1.1-dev.1` COMMANDÉE — la dette [R10-PÉRIMÉE] (17 sommes de l'ère dev.5) SOLDÉE À LA NAISSANCE (la pièce née de la recomposition, le qword porté 0x00010101, 0 octet de code changé — R4/R7), le kit 0.1.1-dev.1 déposé au coffre /test, LE DOUZIÈME RUN ATTENDU (la balise `loupe 0.1.1` sur le vert recoupé, le miroir D165/D170). Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |
| v0.8.2 | 9 nov. 2026 | SECONDE RÉVISION DE TERRAIN DU TGN (Entrées 201–206) : le run M10-(e) REFUSÉ TROIS FOIS, CHAQUE REFUS NOMMÉ — dev.1 puis dev.2 du refus du chargeur 0xc000007b (l'oubli du BASERELOC, puis la table nécessaire mais PAS suffisante), puis LE PAS DÉCISIF : **LE VRAI CHARGEUR DE WINDOWS A CARTOGRAPHIÉ dev.3 — la première fois au terrain, l'enveloppe prouvée de la lignée DEMEURE NORME DE FAIT** — et LE TÉMOIN A NOMMÉ AU T0 [CADRE-NÉ] : le CADRE .data pas né poignée INVALIDE, l'initialiseur du build (le sentinel à +8 — UNE TAILLE CADRE_POIGNEE prise pour un offset — au lieu de +528, la chaîne des tailles du plan ; le zéro aurait été UNE SESSION FANTÔME au premier ouvrir()) ; LA RETOUCHE dev.4 : l'initialiseur .data devient LE MIROIR EXACT du CADRE_VIERGE du harnais (l'offset CALCULÉ, jamais gravé de tête), LE GARDE EST GUÉRI (le validateur du build validait à +8 — la même constante fautive : un garde blessé par le défaut qu'il croyait garder ne garde rien ; il relit désormais LE MÊME miroir, la comparaison ENTIÈRE : le .data des 0x12000 octets relu à l'octet près) ET le scénario relit LE .data ENTIER contre le miroir. LES ENSEIGNEMENTS CONSIGNÉS : LE CONTRÔLE DÉRIVE DU PLAN, JAMAIS DE LA PIÈCE QU'IL CONTRÔLE ; l'initialiseur de l'image est LE MIROIR de l'état de naissance prouvé par le harnais. Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |
| v0.8.1 | 9 nov. 2026 | RÉVISION DE TERRAIN DU TGN (Entrées 201–205) : la cérémonie d'ère PASSÉE SUR PIÈCES (le garde à QUATORZE arbres, la dette D166/D171 soldée, la remise du développeur installée au coffre /test) ; le build `loupe.exe 0.1.0-dev.1` NÉ (la carte génération 13, le verrou croisé 26/26, les trois harnais verts au geste du build) ; LE RUN TERRAIN REFUSÉ DEUX FOIS par le VRAI chargeur Windows — 0xc000007b au geste de cartographie : dev.1 (l'oubli du BASERELOC minimal, l'Entrée 204) puis dev.2 (la table nécessaire mais PAS suffisante — l'image sortait de l'enveloppe des HUIT artefacts de la lignée : le trou de page 0x3000-0x4000, le BSS massif .data, le sous-système GUI) ; LA RETOUCHE dev.3 : l'image ramenée DANS l'enveloppe prouvée (plus de trou, plus de BSS — aucune adresse scellée ne bouge) ET LE KIT PORTE SA CASCADE DIAGNOSTIQUE (les axes reconstitués UN À UN sur des copies éphémères %TEMP%, le VRAI chargeur NOMME l'axe au témoin ; le mode d'erreur coupe les boîtes bloquantes — le refus est nommé PAR LE TÉMOIN). L'enseignement consigné : l'enveloppe prouvée de la lignée devient NORME DE FAIT pour l'éditeur PE — ce que le terrain n'a pas prouvé, le build ne l'ose pas ; un échec nommé vaut plus qu'un vert muet. Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |
| v0.8.0 | 8 nov. 2026 | Révision de consolidation du programme d'après M9 (D170/D171) : le jalon M9 — TLS 1.3 pur en blocs scellés — est FRANCHI (les 28 blocs notés-mesurés-prouvés, la finale `1.0.0` scellée sur recoup exigé comme pièce, LA SESSION RÉELLE la ligne applicative chiffrée avec un serveur réel — D170) ; LE TEST GRANDEUR NATURE ouvert (D171) : le jalon M10 porte « Loupe », l'éditeur hexadécimal au panneau d'empreintes — la couche I de 18 spécifications (D172) et les QUATRE chantiers de notation accomplis (D173–D175 : les 18 blocs notés-mesurés-prouvés, la table de routage de loupe-09 étendue) ; la dette du quatorzième arbre nommée (la cérémonie d'ère du TGN précède le build) ; le projet fils COFFRE-FORT dégelé en parallèle. Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |
| v0.1 | 25 oct. 2026 | Première ébauche : couches I/B/C, règles R1 à R7, boucle en sept étapes, feuille de route M0–M5 |
| v0.2 | 25 oct. 2026 | Décisions D1 à D10 ; sharding en quatre fragments chiffrés ; suite cryptographique (Ed25519, XChaCha20-Poly1305, Argon2id) ; règles R8 à R10 ; empreintes par build ; budgets en tokens ; spécification de la cible x86-64 / Windows 11 ; critères de sortie mesurables |
| v0.3 | 25 oct. 2026 | Universalité par profils de cible (D14, amende D10) ; suite cryptographique paramétrable (D15, amende D5) ; export de continuité chiffré et signé (D16, précise R1) ; en-tête de carte normalisé ; jalons M6-M7 |
| v0.5.0 | 27 oct. 2026 | Révision du retour du terrain : validation terrain normée — boucle d'évidence, journal d'exécution, instrumentation contractualisée, diff chirurgical (D43) ; taxonomie étendue X1–X8 des défauts invisibles à l'émulation (D35–D42) ; jalons M0–M2 constatés franchis (balises 0.2.0 et 0.3.0 — D26, D32, D43) ; budget de localisation corrigé à 64 tokens et budgets mesurés (D31) ; ouverture du jalon M3 — contrats renforcés sur entrées non fiables, fuzzing à propriétés (D45). Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |
| v0.5.1 | 28 oct. 2026 | Coffre-fort des phrases maîtresses (D75) : conteneur chiffré TRIADE-CF1 centralisant toutes les phrases maîtresses par projet — Argon2id aux planchers de la carte, HKDF à contexte dédié, XChaCha20-Poly1305, autotest de falsification (19 contrôles), export chiffré vers les coffres projet et développeur, restauration post-réinitialisation (§ 17.3, FORMAT_CARTE § 11) ; état des jalons constaté — M3 franchi le 28/10/2026 (campagne million D72, conformité permanente D73, scellage balise 0.4.0 D74) ; modèle de menace étendu au vol du coffre-fort (§ 15.1). Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |
| v0.5.2 | 28 oct. 2026 | Garde durable de la phrase de contrôle du coffre-fort (D81) : sauvegardée AVANT TOUTE AUTRE ACTION dès production — fichier `PHRASE-CONTROLE-COFFRE.txt` au racine du dépôt (phrase seule sur une ligne, lisible par `--phrase-fichier`), commit dédié, push GitHub, miroir du coffre Drive, copie au racine du coffre Drive ; le fichier est la remise, l'affichage unique de cérémonie cesse d'être le canal de survie ; restauration post-panne prouvée de bout en bout (téléchargement Drive → coffre ouvert, entrées listées) ; menace « vol du coffre-fort » étendue — la confidentialité au repos repose désormais sur le contrôle d'accès au dossier Drive (mitigation première : restriction du partage par lien), une phrase commise en git y demeure à vie ; M4 constaté ouvert (D77, couche I écrite-avant-code). Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |
| v0.7.0 | 5 nov. 2026 | Révision de consolidation du programme d'après M7 (D160) : le jalon M8 — le bloc optionnel de syscalls directs, le domaine `sys` — est franchi (charte à huit règles, spécifications écrites-avant-code, harnais 61 verts, cérémonie de l'ère passée 12 arbres, run terrain m8d vert sur le VRAI ntdll recoupé 30/30, finale `0.9.0` scellée — D160–D165) ; le jalon M9 — TLS 1.3 pur en blocs scellés, le domaine `tls13`, l'ère 1.0.0 — est ouvert (D166) : couche I complète (28 spécifications, six familles, instrument 117 verts — D167), cérémonie de l'ère passée le 05/11 (13 arbres, garde 13/13, la dette D166 soldée) ; le sceau de l'Intention porte treize arbres, les cérémonies d'ère entrent au protocole (§ 12.4, § 13.5) ; M7 franchi constaté (balise `0.8.0`, Entrée 155). Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |
| v0.6.1 | 31 oct. 2026 | Révision de l'arbitrage de naissance du coffre (D137) : le niveau de sécurité d'un coffre neuf — CF1, CF2 ou CF3 — est choisi par le développeur lors de la création de son projet de développement ; la règle v0.6.0 « un coffre neuf naît CF3 » (D133) est explicitement invalidée et remplacée — imposer CF3 par défaut risque d'être trop contraignant selon le projet. § 12.5 réécrit (les trois naissances, guide de l'arbitrage, obligations par niveau) ; § 1.8 ajouté ; correspondance v0.6.0 → v0.6.1 (§ 19.8) ; la chaîne de migration CF1 → CF2 → CF3 demeure disponible à tout moment ; le coffre réel reste CF3 ; le *Livre du Coffre* passe à v1.1 (runbook et FAQ alignés) ; erratum typographique « tbp] » (page 31 du PDF v0.6.0) réparé dans la chaîne spec_v061. Une règle modifiée et nommée ; aucune couche d'exécution ajoutée ; hiérarchie inchangée |
| v0.6.0 | 31 oct. 2026 | Passation du programme de souveraineté cryptographique (D133) : axes 2-3-4 accomplis et prouvés terrain — la chaîne réelle du coffre a migré CF1 → CF2 → CF3 les 30–31/10 (CF2 : Shamir 5/3, sentinelle/porte D120 ; CF3 : serrure piégée, époque 1, checksum `0cc89a96`, verdict à froid VERT ×2) —, axe 1 TEE consigné ; nouveau chapitre 12 (souveraineté : hiérarchie des gardes, CF2, CF3, sceau de l'Intention, coffre neuf né CF3, bornes) et chapitre 13 (cérémonies et kit du terrain) ; menaces étendues (expropriation, evil maid, roll-back du couple conteneur+piège) ; M5 ouvert ; correspondance § 19.7 ; le PDF formel porte annexe empreintes et tableau décisionnel ; le *Livre du Coffre* accompagne (complément opératoire). Aucune règle modifiée, aucune couche ajoutée à l'exécution, hiérarchie inchangée |
| v0.4.0 | 26 oct. 2026 | Révision de gouvernance vérifiée : couche I normalisée et taxonomie des défauts T1–T6 (D19) ; threat model étendu et R10 renforcée — checksums, signature de manifeste, anti-rollback, fail-closed explicite (D20) ; R11 optimisation mesurée et journal d'optimisation (D21) ; suite de conformité par profil et parité inter-profils à contrat constant (D22) ; reverse-specs, pré-versions dev.N/rc.N/final et fixtures partagées officialisées (D23) ; traçabilité I↔C↔B↔tests, journal des décisions normalisé, tableau de bord de conformité, norme de fragmentation et localisation par intention, budgets tokens instrumentés (D24). Hiérarchie de la fonction objectif inchangée et verrouillée (D19) ; aucune règle affaiblie ; aucune couche d'exécution ajoutée ; numérotation à trois segments |

La présente version consigne LA RÉVISION DU MODÈLE FORMEL ET DE LA GOUVERNANCE ASSAINIE (v0.12.0, D187) : le
protocole entre en manuscrit — quatre questions de recherche, les données réelles
du journal extraites par script, la formulation corrigée dans les termes standards
de l'ingénierie, l'auteur humain unique, l'agent IA décrit en méthodes et
remerciements, les déclarations Ethics/Data/Limitations explicites (N=1, la
circularité de l'oracle, l'absence de baseline, la sécurité mémoire non prouvée,
le temps constant non analysé) ; la proposition D183 (le séquestre chiffré de la
phrase de contrôle) documentée sans être appliquée ; l'annexe A de gouvernance
portée à sha-256. La version précédente (v0.9.0) avait consigné LA RÉVISION DE
CONSOLIDATION DU PROGRAMME D'APRÈS M10 (D178/D179) : les jalons M0 à M10 sont TOUS franchis sur validations terrain (balises finales 0.2.0, 0.9.0, `1.0.0` et `loupe 0.1.0` — la session réelle la ligne applicative chiffrée, la création l'application née de TRIADE vécue chez son utilisateur), le programme de souveraineté cryptographique accompli (axes 2-3-4, D133) ; LE JALON M10 est l'épreuve de la MÉTHODE ENTIÈRE — onze runs terrain, onze défauts nommés, onze retouches documentées : chaque défaut du kit ou de la pièce nommé sur pièces (le chargeur, le CADRE-NÉ, la classe des arguments pile, L'OMBRE, le HINSTANCE, l'IAT relogée, les OFT au pas DWORD, le POINTEUR du FreeLibrary, le RET-NU, le SONDE-EXE), chaque enseignement consigné (le contrôle dérive du plan, jamais de la pièce qu'il contrôle ; l'échec nommé vaut plus que le vert muet ; la vitrine vivante prouve la liaison mieux que toute sonde) — et la balise `loupe 0.1.0` scellée sur le onzième run recoupé 39/39 : LA MÉTHODE TRIADE ENTIÈRE PROUVÉE PAR LA CRÉATION. Le programme d'après M10 est ouvert à la commande du développeur : la version 0.1.1-dev.1 (D179) porte la dette [R10-PÉRIMÉE] soldée à la naissance — le douzième run attendu scellera la balise `loupe 0.1.1` sur le vert recoupé. Les profils additionnels après M7 restent volontairement hors du périmètre courant afin que chaque addition s'appuie sur des résultats mesurés. La règle de gouvernance demeure : toute évolution invalide explicitement ce qu'elle remplace, et rien ne se change en silence — le terrain compris : chaque lecture d'exécution est une révision potentielle du modèle, et son enseignement se consigne (§ 8.4, § 8.5).


