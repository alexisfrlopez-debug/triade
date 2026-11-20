# PLAN PRÉ-ENREGISTRÉ — LA VAGUE 9, L'INSTRUCTION bk79jvzbm : LA SÉCURITÉ AU PLANCHER (la sûreté mémoire à zéro non-résolu, les tuables tués, le fuzzing à 90 %, le temps constant statique, la preuve CF3 mécanisée, l'ancrage de transparence)

> Pré-enregistré AVANT toute mesure (hypothèses, critères d'acceptation,
> graines, empreinte sha256 verrouillée — la règle D204/D211 reconduite).
> Exécution AU LABORATOIRE UNIQUEMENT. Aucun artefact scellé, aucun
> arbre signé, aucun coffre réel touché : la campagne est LECTURE SEULE
> sur les scellés (empreintes vérifiées avant/après), les preuves vivent
> en pièces de laboratoire.

## 1. LES HYPOTHÈSES (falsifiables, pré-enregistrées)

H1 — LA SÛRETÉ MÉMOIRE : les 2 098 accès de l'analyse bornée v110
(surete_memoire.csv : 1 181 vérifiés au cadre, 263 médiés au contrat,
191 constants RIP, 463 NON RÉSOLUS, zéro hors-cadre) se déchargent par
INFÉRENCE D'INVARIANTS DE BOUCLE + ANALYSE D'INTERVALLES + ANALYSE
D'ALIAS, puis MODEL CHECKING BORNÉ (z3, la notation liftée) sur les
non-résolus restants. OBJECTIF : 0 non résolu ; tout accès restant non
déchargeable est NOMMÉ avec sa cause et son mécanisme (l'échec est un
résultat, jamais un angle mort).

H2 — LA MUTATION : les 21 survivants de la vague 8 (12 équivalents
prouvés, 3 TUABLES-RESTANTS, 6 limites du harnais) — les TROIS tuables
(loupe-11 @0x137, loupe-11 @0x1d5, loupe-16 @0x21e : les scénarios
NOMMÉS — la saisie à la dernière cellule puis le défilement, le
recadrage après la saisie au bord) meurent aux NOUVEAUX SCÉNARIOS
D'INJECTION (la batterie K4 ÉTENDUE : les scénarios nommés ajoutés,
AUCUN scénario existant retiré, AUCUN tueur affaibli). Le score ajusté
(équivalents exclus du dénominateur) publié À CÔTÉ du brut : attente
811+3/832 = 814/832 brut, 814/820 = 99,3 % ajusté — JAMAIS fusionnés.

H3 — LE FUZZING : la couverture des blocs d'entrée non fiable (loupe-01
l'ouverture, loupe-02 la lecture, loupe-13 la recherche, loupe-16 la
saisie — les blocs aux entrées non fiables du million fuzzé M3) atteint
AU MOINS 90 % par CORPUS SATURANT + GUIDAGE PAR BRANCHE, MÉMOIRE-OMBRE
et CANARIS ÉTENDUS, les graines consignées. ZÉRO crash, ZÉRO violation
de canari exigés.

H4 — LE TEMPS CONSTANT : la preuve STATIQUE de non-interférence sur la
notation (AUCUNE branche ni adresse mémoire ne dépend du secret —
l'analyse de flux au solveur SMT sur la notation liftée, les secrets
nommés par le contrat I : les clés, les jetons, les verdicts GCM) en
PLUS du hash de trace complète (l'instrument D221 reconduit). Le
protocole de répétition matérielle déjà pré-enregistré demeure
PRÉPARÉ — AUCUN chiffre matériel inventé (le geste appartient au
développeur).

H5 — LA PREUVE CF3 : l'invariant inductif du modèle CF3 (le coffre-
fort : les treize règles, la garde à garde, l'effet à effet — les
sources TLA+ aux archives) se MÉCANISE dans un assistant de preuve
INDÉPENDANT de l'explorateur maison (z3 : le solveur SMT aux certificats
archivés, la batterie des obligations par règle) ; les CERTIFICATS SMT
archivés ; le statut porté à la table des preuves. TOUT lemme non
déchargé est NOMMÉ.

H6 — L'ANCRAGE DE TRANSPARENCE : le témoin d'époque (l'empreinte de
l'ère courante — la chaîne des époques du coffre) s'ancre au JOURNAL DE
TRANSPARENCE DOCUMENTÉ (D219 : le registre public des époques), avec
VÉRIFICATION MACHINE (la chaîne de hachage recalculée, le témoin
confronté, tout écart un refus nommé) et le DELTA AU MODÈLE DE MENACE
aux DEUX bords (ce que l'ancrage ajoute : la détection de la
réécriture d'époque ; ce qu'il n'ajoute pas : la preuve de publication
au monde — nommé tel quel).

## 2. LES PROTOCOLES

H1 — L'OUTIL : surete_memoire_v200.py — l'extension de l'analyse v110 :
(1) l'INFÉRENCE D'INVARIANTS DE BOUCLE (le corps de boucle vérifié par
l'invariant déduit des bornes du contrat I) ; (2) l'ANALYSE
D'INTERVALLES (les registres d'index bornés par les intervalles déduits
— le z3 solveur sur le corps lifté) ; (3) l'ANALYSE D'ALIAS (les
registres médiums suivis aux sources : les arguments, les lea du plan,
les déplacements fixes) ; (4) le MODEL CHECKING BORNÉ des restants (le
chemin lifté en SMT, les boucles déroulées à la borne du contrat, la
preuve de sûreté de l'accès par z3, le certificat UNSAT archivé par
bloc). LE CERTIFICAT PAR BLOC : le compte des accès par classe AVANT/
APRÈS, les preuves z3 aux pièces, le récapitulatif 2 098 = Σ classes.
LA CONFRONTATION : le CSV v110 RE-PRODUIT d'abord à l'identique (le
rejeu des mêmes 2 098 — la base saine), PUIS l'extension mesurée.

H2 — LA BATTERIE : rejeu_fautes_v200.py — la reproduction de la
console v0.14.0 (776/832) AUX MÊMES GRAINES D'ABORD (la graine
20261111, l'ordre inchangé), PUIS la console courante 811/832, PUIS
l'INJECTION des nouveaux scénarios (la saisie à la dernière cellule +
WM_VSCROLL ; la saisie au bord + le recadrage WM_SIZE — les scénarios
NOMMÉS de la vague 8) : les trois tuables meurent, le reste INTACT.
LES PIÈCES : les consoles horodatées, le CSV des 21 (avant/après), le
score brut ET ajusté côte à côte.

H3 — LE FUZZING : fuzz_couverture_v200.py — l'instrument de couverture
(par-bloc : le compteur d'instructions exécutées de CHAQUE bloc du
domaine au million fuzzé, la couverture = instructions exécutées /
instructions du bloc), le CORPUS SATURANT (les graines de M3 + les
bords nommés : les tampons vides, 1 o, les non-hexa, les journaux
pleins, les lignes au fond), le GUIDAGE PAR BRANCHE (les mutations de
corpus guidées par les branches non couvertes — le compteur par
bloc), la MÉMOIRE-OMBRE et les CANARIS ÉTENDUS (les sentinelles
autour des tampons du plan — le modèle du harnais). LES GRAINES
consignées (20261120). LE VERDICT : ≥ 90 % par bloc d'entrée non
fiable, zéro crash, zéro violation de canari.

H4 — LE TEMPS CONSTANT : non_interference_v200.py — le lift de la
notation des blocs crypto (tls13-05/06/15/16, les familles secrètes),
les SECRETS nommés par le contrat I (les clés, les jetons, les
verdicts), l'analyse de flux au solveur (toute branche conditionnée
par un secret, toute adresse mémoire dépendante d'un secret : l'objet
SMT — SAT = l'écart NOMMÉ, UNSAT = la preuve archivée). LA CONTRE-
ÉPREUVE : un bloc volontairement fautif (une branche sur un octet de
clé) est ATTRAPÉ (le contrôle négatif — la preuve que l'outil voit).

H5 — LA PREUVE CF3 : cf3_smt_v200.py — les OBLIGATIONS par règle (la
garde, l'effet — les treize règles du modèle CF3 traduites en SMT
depuis les sources TLA+), l'INVARIANT INDUCTIF (l'initialisation le
porte, le pas le préserve — les deux obligations par règle), le
CERTIFICAT z3 (UNSAT archivé par obligation, le script rejouable
depuis un clone frais), le CONTRÔLE NÉGATIF (une règle mutée : le
modèle rejette l'invariant — la preuve que la preuve voit). LA TABLE
DES PREUVES portée au statut mécanisé (le document des preuves).

H6 — L'ANCRAGE : transparence_v200.py — le journal de transparence
(la chaîne des époques : l'ère D80 courante, les témoins aux pièces),
l'ANCRAGE du témoin d'époque (l'empreinte de l'ère + la hauteur de la
chaîne + le témoin signé), la VÉRIFICATION MACHINE (la chaîne
recalculée du_genesis, le témoin confronté, TOUT écart un refus nommé
ANCRAGE-DIVERGENT), LE DELTA AU MODÈLE DE MENACE aux deux bords (ce
que l'ancrage détecte : la réécriture, l'omission d'époque ; ce qu'il
ne détecte pas : la publication — nommé). LE CONTRÔLE NÉGATIF : une
époque réécrite au journal → l'ancrage la REFUSE nommément.

## 3. LES RÈGLES DE VERDICT PRÉ-ENREGISTRÉES (fail-closed)

  - le REJEU complet aux graines consignées : BIT-IDENTIQUE (la console
    v0.14.0 776/832 reproduite AVANT toute nouvelle injection ; la
    console courante 811/832 ensuite — jamais l'inverse) ;
  - chaque mutant déclaré équivalent porte sa preuve mécanique (la
    vague 8 — les 12 demeurent, AUCUN re-qualifié) ; un contrôle
    négatif volontairement faux est ATTRAPÉ ;
  - round-trip 100 %, garde du sceau 14/14, empreintes des artefacts
    scellés intactes avant/après ;
  - l'assistant de preuve indépendant REJOUE l'invariant depuis un
    clone frais ; tout lemme non déchargé est NOMMÉ ;
  - AUCUN résultat matériel consigné sans témoin signé du développeur ;
  - tout écart défavorable NOMMÉ (l'échec est un résultat).

## 4. LA CONSIGNATION

UNE DÉCISION APPEND-ONLY PAR CHANTIER (H1..H6 = jusqu'à six décisions),
les alternatives rejetées nommées ; les pièces aux ateliers ; les
certificats (SMT, z3) archivés rejouables ; la présente empreinte au
journal AVANT la première donnée.
