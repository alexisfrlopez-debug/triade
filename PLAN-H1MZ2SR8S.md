# PLAN GELÉ — H1MZ2SR8S (la vague 14)
> L'atelier de performance pré-enregistré : le GHASH agrégé 4 blocs à réduction
> différée + l'entrelacement AES-CTR pipeliné dans la composition GCM.
> R11 : le hot path identifié par mesure — le GHASH par bloc à 63-64 c et le
> sondage cpuid par appel sont les hot paths nommés par la vague 13.
> Gelé AVANT toute mesure ; aucun artefact scellé touché.

## Le mandat
Trois chantiers :
(1) **GHASH AGRÉGÉ 4 BLOCS à réduction différée** (Karatsuba sur 4 blocs,
réduction unique) + entrelacement AES-CTR pipeliné dans la composition GCM — le
mécanisme nommé des 13× d'OpenSSL@4096 ; **cible pré-enregistrée ≤2,0 c/octet@4096**
(l'opérande : 8 192 cycles pour 4 096 octets), parité de repli au scellé par bloc ;
(2) **RENOTATION SHA-NI à dispatch hissé** (la sonde de session vit déjà ; le
corridor d'époque porte ~2 660 c × 64 = 92 % de sondages) — cible corps ≤3,6
c/octet puis schedule 2-way, cible étirée ≤2,2 c/octet (EVP 2,036 nommé) ;
(3) **AVX2 : dispatch hissé hors boucle** (le coût as-sealed 5 846 c dominé par cpuid).

## Les contraintes
Round-trip 100 % (keystone==capstone==keystone) ; différentielle 0/320 contre le
scellé ; KAT SP 800-38D / FIPS 197 / FIPS 180-4 ; parité triple
couloir==scellé==OpenSSL EVP octet pour octet (ct ET étiquette) ; repli au scellé
32/32 ; mutant attrapé au premier vecteur ; commutativité et X/Y intacts ; marges
sans chevauchement par code. Temps-constant STRUCTUREL : H ta INTÉ comme secret
(tls13-17 P3), aucune branche ni adresse sur secret, twist sans branche, UNE
empreinte de trace complète par classe (60 mesures), instructions à latence
variable absentes du corridor.

## La mesure
Rig natif RDTSCP, cœur épinglé, n≥20, médianes non arrondies + IQR, cycles bruts
publiés ; la machine virtualisée nommée (le silicium nu au geste du développeur).
Aucun artefact scellé touché — les couloirs vivent à la marge (0xF300-0xF7FF),
les scellés intacts avant/après chaque run.

## La vérification après modifications
Parité triple re-vérifiée octet pour octet sur tous vecteurs ; différentielle et
KAT re-roulées ; temps-constant re-haché (une empreinte/classe) ; mutant et repli
re-prouvés ; re-mesure n≥20 aux mêmes conditions (avant/après consigné au journal
OPT) ; ratios recalculés depuis les médianes non arrondies ; sceau 14/14 ;
consigner OPT-NN avec hot path, mesure avant/après, contrat stable R4, décision.

## Les refus
Jamais un vecteur KAT passé sous silence ; jamais le scellé réécrit ; jamais un
canon arrondi sans ses opérandes ; jamais la machine virtualisée maquillée en
silicium.
