# PLAN PRÉ-ENREGISTRÉ — v0.14.0 : LE BRAS DE RÉFÉRENCE COMPILATEUR

**Statut : PRÉ-ENREGISTREMENT — consigné AVANT TOUTE MESURE (la commande
ic09ydeli, point 1 : « rédiger et consigner un plan de comparaison avec
hypothèses et critères d'acceptation AVANT toute mesure »). L'empreinte
sha256 du présent fichier est consignée à la décision D193 ; toute
modification APRÈS le début des mesures serait une fraude nommée
(l'étape de vérification confronte l'empreinte).**

## 1. L'OBJET DE LA COMPARAISON

Les blocs scellés de Loupe (la notation à la main, msx64) contre une
RÉFÉRENCE COMPILÉE depuis les MÊMES CONTRATS de couche I (le C ci-dessous),
soumise aux MÊMES INSTRUMENTS. La question de recherche : **que coûte,
en vérifiabilité et en volume, l'écriture directe de la notation — et
que gagne-t-on ou perd-on contre un compilateur partant du même
contrat ?** La comparaison est contrôlée : mêmes contrats, mêmes shims
OS, mêmes vecteurs, mêmes graines, mêmes tueurs.

## 2. LES BLOCS (six, les cinq familles couvertes)

| Bloc | Famille | Contrat I |
|---|---|---|
| loupe-01 ouvrir | noyau/fichier | loupe/I/loupe-01-ouvrir.md (r3) |
| loupe-02 lire | noyau/fichier | loupe/I/loupe-02-lire.md |
| loupe-05 sha256 | empreintes | loupe/I/loupe-05-sha256.md |
| loupe-08 ligne | rendu | loupe/I/loupe-08-ligne.md |
| loupe-13 recherche | navigation | loupe/I/loupe-13-recherche.md |
| loupe-16 saisie | édition | loupe/I/loupe-16-saisie.md |

## 3. LES HYPOTHÈSES (pré-enregistrées)

- **H1 (référence saine)** : la référence C passe son auto-vérification
  contre les vecteurs officiels AVANT toute mesure (FIPS 180-4 pour
  sha-256 ; les verdicts nommés des contrats pour les blocs OS). Si H1
  échoue : AUCUN chiffre publié pour le bloc fautif (la doctrine md5/aes
  de v0.11.0 : mieux aucun chiffre qu'un chiffre faux).
- **H2 (compacité)** : la notation à la main est plus compacte que la
  référence compilée -O2 (l'audit v0.13.0 a établi 1,45× sur sha256 ;
  l'hypothèse est re-testée sur les six blocs — elle peut être INVALIDÉE,
  notamment contre -Os).
- **H3 (instructions exécutées)** : la notation est dans le MÊME ordre de
  grandeur que la référence en instructions par opération (l'audit v0.13.0
  a établi −9 %/+2 % sur sha256 ; l'hypothèse est qu'il n'y a pas de
  facteur spectaculaire dans AUCUN sens sur les six blocs).
- **H4 (testabilité)** : le taux de mort par mutation est du même ordre
  pour les deux camps sous les MÊMES tueurs (la question n'est pas « qui
  est le mieux testé » mais « la notation est-elle testable au même
  degré »).

## 4. LES CRITÈRES D'ACCEPTATION (pré-enregistrés, binaires)

- **CA1** : chaque fonction C est AUTO-VÉRIFIÉE contre les vecteurs
  officiels AVANT la mesure ; un échec = le bloc est exclu des chiffres
  et l'écart consigné.
- **CA2** : les deux camps sont mesurés par le MÊME harnais Unicorn sur
  les MÊMES shims (le mini-OS du harnais noyau de Loupe, les primitives
  OS servies aux DEUX camps par la même table), les MÊMES vecteurs, à la
  même graine (20261113).
- **CA3** : les résultats sont rapportés TELS QUELS — y compris
  DÉFAVORABLES au protocole (la consigne explicite de la commande).
- **CA4** : toute adaptation d'instrument est NOMMÉE dans le rapport
  (l'oracle structurel du camp C vérifie la SÉQUENCE des appels OS du
  contrat — le plan des notations n'existe pas pour du code compilé ;
  le round-trip est EXCLU du camp C par nature — la commande le dit).
- **CA5** : le plan n'est pas modifié après le début des mesures
  (confrontation de l'empreinte sha256 consignée à D193).

## 5. LA MÉTHODE

1. **La référence C** (`scripts/bras_c_v140/bras_c.c`) : les six fonctions
   écrites DEPUIS LES CONTRATS (chaque pre/post/inv relu avant l'écriture,
   les verdicts nommés −1..−7 identiques, les mêmes bornes). Les
   primitives OS (CreateFileW, ReadFile, GetFileSizeEx, CloseHandle,
   GetLastError) sont appelées via une TABLE DE POINTEURS posée par le
   harnais — les DEUX camps consomment les MÊMES shims du mini-OS.
   Compilation : gcc 14.2 -O2 et -Os (clang si installable, sinon
   l'écart NOMMÉ — le précédent v0.11.0 vaut).
2. **Le harnais commun** (`scripts/bras_c_v140/comparer_v140.py`) : le
   mini-OS du harnais noyau de Loupe (loupe/harnais_noyau.py) sert les
   fichiers virtuels, les échecs paramétrables et le journal des appels ;
   le camp notation est posé à ses RVA du plan ; le camp C est chargé à
   une base distincte. Pour CHAQUE bloc et CHAQUE vecteur : les mêmes
   entrées, les sorties CONFRONTÉES (verdicts, tampons, empreintes),
   le comptage d'instructions au même crochet, la SÉQUENCE des appels OS
   journalisée et confrontée au contrat (l'oracle structurel adapté).
3. **Les vecteurs** (pré-enregistrés) : le vide (taille 0), « abc », les
   NIST 448/896 bits (sha-256), un fichier de 1 Kio pseudo-aléatoire à la
   graine 20261113 (recherche de motifs présents/absents, lignes aux
   bornes 15/16/17, saisie aux bornes, ouverture absente/verrouillée/
   hors périmètre, session déjà ouverte) — chaque vecteur attend un
   verdict NOMMÉ et des octets exacts.
4. **La mutation** : les MÊMES mutations à un octet que la campagne
   v0.11.0 (16 mutants par bloc, la graine 20261111, les mêmes sites :
   instructions, opérandes, offsets) appliquées aux DEUX camps (les
   notations assemblées pour le camp notation ; le .text compilé pour le
   camp C), tuées par les MÊMES tueurs : K3 le sémantique (les vecteurs
   ci-dessus) et K2 adapté (la séquence d'appels OS du contrat pour le
   camp C ; l'oracle structurel du plan pour le camp notation). Le taux
   rapporté par bloc et par famille.
5. **Les métriques** : instructions par opération complète (la même
   convention que l'audit v0.13.0 : tout le pipeline du bloc, compté au
   crochet, zéro lecture de compteur intermédiaire — la leçon D191),
   tailles de code au bon périmètre (la fonction seule pour le C,
   l'objet notation + ses tables), le taux de mort par mutation, la
   fidélité de séquence OS.
6. **L'analyse** : les rapports par bloc (notation vs -O2 vs -Os), les
   agrégats par famille, les distributions (médiane, quartiles, min/max)
   — jamais une valeur unique. Les écarts interprétés avec prudence :
   la comparaison est UN échantillon de six blocs, pas une loi.

## 6. CE QUI N'EST PAS MESURÉ ICI (les frontières)

- Les tokens (mesurés à part par la re-mesure RQ2, point 2 de la
  commande — jamais confondus avec le présent bras).
- Les kits terrain (préparés, marqués « EN ATTENTE » : les runs terrain
  appartiennent au développeur ; AUCUN résultat terrain ne sera
  fabriqué).
- Le temps d'horloge (le débit d'émulation appartient à l'outil — la
  métrique est le compte d'instructions, la convention v0.13.0).

## 7. LA CONSIGNATION

Le présent plan est consigné (sha256 à D193) AVANT les mesures ; les
sorties brutes vivront à scripts/preuves_v140/ (bras_c.csv, le rapport) ;
les résultats entreront au manuscrit v0.14.0 par le générateur, jamais
tapés à la main.
