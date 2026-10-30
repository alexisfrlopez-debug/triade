# Couche I — v0.6.0 axe 4 : CF3, la serrure à triple scellement et le cycle en deux actes (D121)

Spécification écrite **avant** tout code (R2, provenance `écrite-avant-code`). Elle
instancie la décision D121, née de deux demandes du terrain servies ensemble :

1. **« Plutôt qu'une sentinelle externe, une serrure du coffre piégée »** — un
   système à trois éléments : clé utilisateur invariable, serrure du coffre
   métamorphe, piège de la serrure métamorphe aussi. Sans la seconde moitié du
   piège, la tentative de déverrouillage est impossible ; un problème prouvé sur
   une moitié détruit le coffre ; plus de démon qui tourne en permanence pour ne
   servir qu'au déverrouillage.
2. **« Une vulnérabilité réside durant le temps où la session est ouverte »** —
   deux déverrouillages : un à l'ouverture pour la modification, un à la
   fermeture pour la validation.

La présente spec durcit les deux intuitions là où elles étaient attaquables
(les trois pièges de § 2), réalise l'exigence D120 (« la sentinelle est
indispensable au déverrouillage ») **par invocation au lieu de résidence**, et
ajoute le cycle en deux actes qui borne la fenêtre de session.

> **Position dans le sceau.** CE texte vit dans l'arbre scellé
> `v06/I/CF3/README.md` — écrit D121 sous `docs/I/CF3/` (hors périmètre du
> sceau, spec § 1 de v06/I/README.md : aucune divergence créée), il y est
> entré à la re-cérémonie D126, en compagnie de l'erratum § 12 du README
> CF2 (« 2 fragments » → TROIS, consigné 47e704f) : la même signature
> couvre l'entrée et le correctif.

## 1. Périmètre et adversaire modélisé

Sous la spécification : la serrure à trois éléments (§ 2), la dérivation et le
conteneur **TRIADE-CF3** (§ 3), le fichier **piège** (§ 4), la **sentinelle
instantanée** (§ 5), le **cycle en deux actes** (§ 6), la réponse à la
falsification (§ 7), la discipline RAM (§ 8), l'anti-retour-en-arrière (§ 9),
la course de clôture et la liaison au contenu (§ 10), le laboratoire (§ 11),
la cérémonie de migration CF2 → CF3 (§ 12), les critères de sortie (§ 13).

Hors périmètre D121 : la migration du coffre RÉEL du développeur (cérémonie
§ 12 — le bac à sable ne touchera JAMAIS le conteneur ni les phrases réels) ;
l'intégration au GUI de cérémonie (livrée après preuve terrain, même loi que
CF2 → GUI) ; le support physique à bouton (FIDO2/smartcard) pour le piège —
le protocole l'accueille sans rien renverser (§ 4, borne montante).

L'adversaire modélisé (borne consignée, même famille que CF2 § 1) :

- **voleur de la machine seule** (conteneur + disque + RAM froide) : il n'a
  pas le média du piège. Contre lui, le brute-force de la phrase n'est même
  pas *tentable* (§ 3, champ `verif` — il lui manque une valeur publique du
  piège) ;
- **evil maid** sur le conteneur ou sur le média du piège : détecté par tag,
  époques et AEAD (§ 5, § 7) ;
- **processus tiers aux privilèges utilisateur pendant la session** : borné
  par le cycle en deux actes (§ 6, § 10) — aucune clé maîtresse en RAM entre
  les actes, le canonique n'est jamais réécrit pendant la session ;
- **PAS un attaquant admin/noyau qui contrôle la machine PENDANT un acte** :
  un logiciel pur ne pare pas ça (borne assumée, § 10) — cérémonie sur machine
  propre, sessions courtes, re-verrouillage rapide. La frontière est dite, pas
  cachée.

## 2. Les trois éléments (normatif) — et les trois pièges évités

- **K_user** : la clé de l'utilisateur, `Argon2id(phrase, sel_argon)` —
  32 octets, paramètres miroir CF1 (65536 Kio, 3 itérations, parallélisme 1 —
  plancher FORMAT_CARTE § 3.1). **INVARIABLE à travers les époques** (la
  demande du terrain : « clé utilisateur qui ne change pas ») : `sel_argon`
  et les paramètres sont posés à l'init et JAMAIS retouchés par une clôture.
- **S_serrure** : la moitié « serrure », 32 octets frais du CSPRNG **à chaque
  époque**, logée dans l'en-tête clair du conteneur (côté machine).
- **S_piège** : la moitié « piège », 32 octets frais du CSPRNG **à chaque
  époque**, logée **exclusivement sur un média séparé** (§ 4) — jamais écrite
  sur la machine hors l'instant de l'acte.
- **époque** : compteur monotone u64, posé à 1 à l'init, incrémenté à CHAQUE
  clôture. C'est l'horloge de la métamorphose et le témoin anti-retour
  (§ 9).
- **H_projet** : sha256 de l'état scellé (le contenu clair du coffre au
  moment du scellement). C'est le **liant** de la clé de clôture au contenu
  (§ 10).

Les trois pièges de l'intuition d'origine, désamorcés et consignés :

1. **Un hash de projet est public** (le dépôt est sur GitHub). Un élément
   public n'est pas un secret : il LIE, il ne protège pas. Le hash du projet
   n'entre donc JAMAIS comme source d'entropie — seulement comme *contexte* de
   dérivation (§ 3). L'entropie vient de K_user, S_serrure et S_piège.
2. **Le piège ne doit pas être dérivable de la serrure** (« piège dépendant de
   la serrure » — si piège = H(serrure), le voleur de l'en-tête calcule le
   piège et le facteur possession s'effondre). S_serrure et S_piège sont deux
   aléas **indépendants**, liés par le format (époques, tag) et la dérivation
   commune — aucun des deux calculable depuis l'autre.
3. **Détruire sur mauvaise clé = un DoS offert** (une faute de frappe suffirait
   à l'attaquant). La séparation des modes de défaillance (§ 5) : la phrase
   erronée est BÉNIGNE (réessai, délai croissant), seule la falsification
   **prouvée** détruit (§ 7).

## 3. La dérivation et le conteneur TRIADE-CF3 (normatif)

KEK = HKDF-SHA256(ikm = K_user ‖ S_serrure ‖ S_piège ; salt = sel_hkdf ;
info = `"triade-CF3/v1|" ‖ époque(le64) ‖ H_projet`), 32 octets — puis
XChaCha20-Poly1305 (nonce 24 o, AAD = tout l'en-tête jusqu'au nonce inclus —
miroir CF2 § 11.2 : l'empreinte du chiffretexte est posée APRÈS la zone AAD,
le tag AEAD reste la preuve, l'empreinte la redondance nommée).

Le champ **`verif`** rend l'essai-hors-ligne impossible au voleur de la
machine seule :

> verif = sha256(HKDF(ikm = K_user ‖ V_piège ; salt = sel_hkdf ;
> info = `"triade-CF3/verif/v1"`))[:16]

V_piège est une valeur **publique** de 16 octets portée par le fichier piège
(§ 4). Le conteneur seul ne suffit donc pas à tester des phrases : il manque
V_piège, qui vit sur le média. Contre le voleur de TOUT (machine + média), la
défense est Argon2id — borne consignée, même famille que CF1.

Format binaire du conteneur `.keys/coffre_cf3.bin` (petit-boutiste) :

```
"TRIADE-CF3" 10 o | version u16 (=1) | époque u64 | H_projet 32 o |
sel_argon 16 o | params (t,m,p : u32×3) | sel_hkdf 32 o | S_serrure 32 o |
nonce 24 o |                        <- fin de l'AAD (168 o)
empreinte 32 o = sha256(chiffretexte) | verif 16 o |
chiffretexte = AEAD(clair, aad, nonce, KEK)
```

La base claire est le MÊME schéma JSON que CF1/CF2 (`format`, `protocole`,
`cree`, `modifie`, `description`, `projets`) — la future migration traduit
**rien** (§ 12).

## 4. Le fichier piège (normatif)

Un fichier **texte ASCII** par époque, sur le média séparé (le sachet du kit,
à côté des fragments hors-ligne) — nom :
`piege-CF3-epoque-<époque>.txt`. Une époque, un fichier : une clôture AJOUTE le piège N+1 et ne ronge JAMAIS les pièges des époques passées (crash-cohérence § 6 ; l'ancien piège est la relève du canonique précédent). Seul le créneau N+1 peut être REMPLACÉ — par le REJEU d'une clôture interrompue (son orphelin ne protège rien : le canonique est encore à N) ; un média du piège par coffre (le sachet est individuel) — borne consignée.

```
TRIADE-CF3-PIEGE v1
epoque: <u64 décimal>
projet: <H_projet hex (64)>
piege: <S_piège hex (64)>
verif: <V_piège hex (32)>
tag: <hex (16)>
```

`tag = sha256("TRIADE-CF3-piege" ‖ époque(le64) ‖ H_projet ‖ S_piège ‖
V_piège)[:8]` — nomme la corruption sans divulguer (miroir `tag_fragment`
CF2 § 4). Le tag n'est PAS un MAC (un evil maid peut le recalculer) : il
garantit l'INTÉGRITÉ du média, pas son authenticité — l'authenticité vient de
`verif` (indérivable sans K_user) et de l'AEAD. Borne consignée : **un piège
entièrement forgé se présente comme une phrase erronée** (verif diverge) —
bénin, refus nommé, jamais de destruction.

Le média du piège peut demain être une clé USB à bouton physique
(FIDO2/smartcard) : seul le support change, le protocole est inchangé.

## 5. La sentinelle instantanée (normatif — l'ordre EST la loi)

L'exigence D120 — « si le déverrouillage est tenté et qu'elle n'est pas
lancée, tous nos efforts sont inutiles » — reste. Ce qui change : elle est
réalisée **par invocation** (vérifications in-process, à chaque acte) au lieu
d'un démon résident. Le démon résident était usurpable (faux heart-beat —
borne D120 consignée) ; la sentinelle instantanée ne dépend d'AUCUN état de
machine falsifiable : **le piège EST le témoin, et il est hors machine**.
Sine qua non réalisé sans démon : le déverrouillage est *impossible* (pas
seulement refusé) sans la seconde moitié de la serrure.

L'ordre des vérifications, à TOUT acte qui déverrouille (ouvrir, clôture,
verifier, re-lecture à froid) :

1. **Piège présent** — absent : refus nommé, **déverrouillage impossible**
   (fail-closed). Rien n'est lu, rien ne brûle.
2. **Piège intègre** (tag) — invalide : refus nommé + journal. PAS de
   destruction (borne : le média est hors limite de confiance, une corruption
   bénigne — lecteur défaillant, secteur mort — doit pouvoir être relue depuis
   les copies hors-ligne ; la destruction attend la PREUVE cryptographique,
   § 7).
3. **Cohérence des champs publics** — époque du piège == époque du conteneur
   (divergence : « piège PÉRIMÉ », refus + journal — anti roll-back § 9) ;
   H_projet du piège == H_projet du conteneur (divergence : piège d'un AUTRE
   coffre).
4. **Phrase** (verif) — diverge : « phrase ERRONÉE », réessai avec délai
   croissant (1, 2, 4 s, plafond 8 s — le plafond borne aussi le verrouillage
   de compte de l'utilisateur par lui-même). **JAMAIS de destruction.**
5. **AEAD + étiquette** (KEK complet) — échec APRÈS 1–4 verts : falsification ou
   corruption **prouvée** côté machine (§ 7) → destruction locale + PV +
   journal. L'ÉTIQUETTE est vérifiée : le clair déchiffré doit hacher vers
   le H_projet de l'en-tête — c'est ce qui ferme la course de clôture
   (§ 10 : un KEK volé qui chiffre un contenu substitué sous une étiquette
   honnête est une falsification PROUVÉE).

Un échec à une étape NOMME son étape ; les étapes suivantes ne courent pas.

## 6. Le cycle en deux actes (normatif)

**Acte I — ouverture.** Phrase + piège → sentinelle instantanée (§ 5) →
clair → **brouillon** chiffré sur disque sous une **clé de session éphémère**
K_session (32 o CSPRNG, en RAM dans l'objet Session SEULEMENT). Puis : K_user,
KEK, S_serrure, S_piège sont effacés de la mémoire (§ 8) ; le média du piège
est **débranché** (geste humain, consigné au journal de cérémonie) ; le
conteneur canonique n'est **jamais réécrit** pendant la session.

**Session.** Travail sur le brouillon (`lire`/`ecrire`, AEAD sous K_session).
Une panne ou un abandon tue K_session avec le processus : le brouillon devient
illisible, le canonique reste scellé — **une panne auto-nettoie**.
`abandonner()` efface le brouillon et efface K_session ; un brouillon
abandonné est un déchet indéchiffrable.

**Acte II — clôture.** Média rebranché + phrase **retapée**. L'ordre des
écritures est crash-cohérent (toute panne laisse un état rejouable) :

1. phrase VÉRIFIÉE contre le canonique courant (verif — une faute de frappe
   à la clôture est BÉNIGNE, aucun scellement n'a lieu) ;
2. H_final = sha256(brouillon final) ; **checksum court de 8 hex AFFICHÉ**
   — l'humain recoupe avec sa carte (§ 9) ;
3. moitiés FRAÎCHES (S_serrure′, S_piège′, V_piège′, sel_hkdf′), époque N+1 ;
   `sel_argon` INTACT (K_user invariable) ;
4. KEK_clôture = dérivation(§ 3) avec H_final et époque N+1 — **liée au
   contenu** (§ 10) ;
5. écriture du piège N+1 sur le média (ADDITIVE, § 4) puis du conteneur en
   **staging** (`.keys/coffre_cf3.bin.staging`) ;
6. **re-lecture à froid** du staging par la sentinelle complète (§ 5) —
   uniquement depuis les artefacts ÉCRITS : VERTE → `os.replace` (atomique)
   staging → canonique ; ÉCHEC → staging détruit, canonique INTACT, brouillon
   INTACT (la clôture est rejouable), échec nommé ;
7. miroir journal : époque N+1 + checksum consignés ; brouillon effacé ;
   K_session, KEK_clôture et moitiés effacés (§ 8) ; nouveau piège N+1 devient
   LA seconde moitié, l'ancien devient relève.

Analyse de panne (consignée, prouvée § 11) : panne avant 5 — rien n'a changé ;
entre 5 et 6 — piège orphelin inoffensif, canonique intact ; entre 6 et 7 —
canonique N+1 + pièges N et N+1 présents, miroir à N : la prochaine ouverture
prend le piège D'ÉPOQUE ÉGALE au conteneur et le contrôle « conteneur ≥
miroir » passe (§ 9) — aucune clôture n'est perdue, aucun faux refus.

## 7. La réponse à la falsification (normatif)

La destruction locale ne touche QUE ce qui vit sur la machine : conteneur,
staging, brouillon. **JAMAIS** le média du piège (externe — c'est la relève),
**JAMAIS** les fragments CF2 ni les copies hors-ligne (coexistence § 12 —
la destruction reste survivable : c'est la contrepartie qui rend le piège
destructif acceptable).

Trois passes (aléa CSPRNG, 0xFF, 0x00) + truncate + renommage aléatoire +
unlink + fsync (miroir `bruler` CF2 § 7), PV horodaté avec la RAISON NOMMÉE
dans `.keys/pv-cf3/`, ligne au journal. Chaque destruction laisse SON PV :
deux destructions la même seconde produisent DEUX fichiers distincts
(suffixe `-2`, correctif D123 — le rapport terrain D122 a prouvé
l'écrasement même-seconde : le second PV écrasait le premier).
`bruler` (commande explicite,
`--oui-je-comprends`) reste la destruction MANUELLE — même routine, déclencheur
humain.

## 8. La discipline RAM (normatif)

Même discipline que CF2 § 8 : K_user, KEK, S_piège, S_serrure, K_session ne
vivent qu'en `bytearray`, effacés (`_effacer` + `del`) au mieux de Python
après usage ; l'objet Session ne retient QUE K_session ; aucun secret n'entre
dans un journal, un PV, une sortie ou une exception. La garantie native est
une affaire Windows.

## 9. L'anti-retour-en-arrière (normatif)

Le roll-back restaure un COUPLE cohérent (conteneur N + piège N) — l'AEAD
passerait seul. Trois miroirs d'époque, du plus faible au plus fort :

- **journal local** (`.keys/journal-cf3.txt`) : contrôle automatique à chaque
  acte — l'époque du conteneur doit être ≥ l'époque du miroir ; divergence →
  « RETOUR EN ARRIÈRE » nommé. Borne : effaçable par un attaquant admin ;
- **carte papier du sachet** : le checksum de 8 hex consigné À LA MAIN à
  chaque clôture ; `verifier` l'affiche à froid pour recoupement humain —
  indécevable par logiciel ;
- **journal Git** (JOURNAL_TRAVAIL, poussé) : l'époque et le checksum
  consignés à chaque cérémonie de clôture — témoin archivé hors machine ;
  `verifier --epoque-attendue N` le confronte.

## 10. La course de clôture et la liaison au contenu (normatif + bornes)

L'attaque : un malware attend la frappe de la phrase à la clôture, vole la
clé dérivée et scelle SON état à la place. La parade est DOUBLE :

- **la clé de clôture est dérivée AVEC H_final** — elle ne peut sceller
  QUE l'état exact dont le hash a servi à la dériver ;
- **l'étiquette est vérifiée à l'ouverture** (§ 5.5) : le clair déchiffré
  doit hacher vers le H_projet de l'en-tête. Le faux conteneur « étiquette
  honnête, contenu substitué » (en-tête H(A), chiffretexte B sous le KEK
  volé) est démasqué : sha256(B) ≠ H(A) — falsification PROUVÉE,
  destruction locale.

Un KEK volé ne produit donc AUCUN conteneur ouvrable pour un autre
contenu (prouvé § 11 : les deux variantes du faux conteneur — étiquette
menteuse H(B), ou étiquette honnête H(A) avec chiffretexte B — échouent,
l'une à l'AEAD, l'autre à l'étiquette, toutes deux détruites), et le faux
conteneur exige en outre d'écrire le média du piège pendant qu'il est
branché.

Bornes consignées (le modèle de menace dit ses limites) :

- un attaquant admin qui contrôle la machine PENDANT l'acte voit la phrase,
  peut photographier le média branché et forger un conteneur complet — aucun
  logiciel pur ne pare ça ; le rayon est borné à UNE époque (moitiés neuves
  à chaque clôture, § 6) ; cérémonie sur machine propre ;
- l'affichage du checksum ne protège que s'il est regardé — le verdict à
  froid re-exécuté par la machine (§ 9) est le filet ;
- le contenu de la session reste lisible par un malware présent pendant que
  l'utilisateur travaille (inhérent : il a ouvert pour lire) — sessions
  courtes, re-verrouillage rapide.

## 11. Le laboratoire

`v06/test_coffre_cf3.py` (falsifiabilité — une garde qui ne rejette rien ne
garde rien, leçon M3) et l'`autotest` embarqué. Aucun conteneur réel ni
phrase réelle n'est touché (répertoires temporaires — discipline D105).
Critères de sortie mesurables : § 13.

## 12. La cérémonie de migration CF2 → CF3 (consignée, outillage différé)

CF3 ne remplace pas CF2 d'un claquement : la serrure est une génération de
PLUS (CF1 : phrase ; CF2 : + fragments Shamir + sentinelle/porte ; CF3 : +
piège sur média + cycle en deux actes). Le coffre RÉEL migre par cérémonie,
quand le terrain a prouvé la serrure en laboratoire : (1) CF2 déverrouillé
une dernière fois (porte D120 honorée) ; (2) la base re-scellée sous CF3
(schéma identique — rien à traduire) ; (3) verdict à froid de CF3 VERT ;
(4) destruction explicite du conteneur CF2 (les fragments CF2 et leurs
copies hors-ligne restent la relève historique). L'outillage `migrer` sera
livré avec la preuve terrain ; le protocole ci-dessus est déjà complet.

## 13. Critères de sortie (mesurables)

1. round-trip deux actes : init → ouvrir → modifier → fermer → ouvrir —
   contenu exact, époque incrémentée, moitiés remplacées, `sel_argon`
   invariant ;
2. phrase erronée (acte I ET acte II) : refus nommé, JAMAIS de destruction,
   aucune écriture ;
3. piège absent : déverrouillage impossible, refus nommé ;
4. piège périmé / roll-back du couple : refus nommé + journal ;
5. tag du piège invalide : refus nommé SANS destruction (média hors limite) ;
6. falsification prouvée côté machine : destruction locale + PV nommé, média
   et fragments intacts ;
7. course de clôture : KEK volé + faux conteneur (étiquette menteuse, OU
   étiquette honnête à contenu substitué) → refus nommé + destruction
   locale, jamais une ouverture ;
8. panne simulée à chaque phase de la clôture : canonique intact, cycle
   rejouable ;
9. auto-nettoyage par panne : brouillon indéchiffrable sans K_session,
   canonique jamais réécrit pendant la session ;
10. non-régression : sceau_I verifier CODE 0, suites CF2/sceau-I/GUI vertes
    (CF3 n'écrit que hors `v06/I/`).
