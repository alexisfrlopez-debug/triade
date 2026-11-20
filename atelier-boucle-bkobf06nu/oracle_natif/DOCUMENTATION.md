# LE RÉGIME « ORACLE NATIF » — LE TROISIÈME RÉGIME DE PREUVE (PRÉPARÉ au laboratoire)

> La vague 9, l'instruction bkobf06nu point 3, le PLAN-BKOBF06NU H3 gelé.
> Le régime est PRÉPARÉ ici : le runner, les scénarios, la confrontation,
> les témoins signés, la documentation. SON EXÉCUTION vit au Windows du
> CI — jamais confondue avec le terrain du développeur (la distinction
> portée au modèle de menace, ci-dessous).

## 1. CE QU'EST LE RÉGIME NATIF

UN EXÉCUTEUR WINDOWS AUTOMATISÉ (le runner CI) qui exécute LES OCTETS
SCELLÉS et les scénarios de la campagne au VRAI Windows (une machine
virtuelle ou un conteneur Windows du CI), produit des TÉMOINS HASHÉS ET
SIGNÉS, et les confronte aux attentes du laboratoire (les vecteurs
dorés, les oracles hashlib, les observables de la boucle WinMain).

LES TROIS RÉGIMES DE PREUVE (la table des statuts) :
  1. L'ÉMULATION (Unicorn) — l'audit échantillon, la divergence 0, les
     scénarios de la batterie — LE LABO, reproductible à l'infini ;
  2. LE DOUBLE MOTEUR (QEMU-user au volume) — la mécanique autre, les
     octets PAR CONSTRUCTION identiques, la divergence 0 au volume —
     LE LABO, le faux-fuyant de l'émulation unique refermé ;
  3. L'ORACLE NATIF (le présent) — les octets scellés AU VRAI Windows,
     les témoins signés — LE CI, automatise ce que la vitrine vivait à
     la main (M10 : le douzième run terrain — LE RÉGIME LE PRÉCÈDE et
     le couvre en partie).

## 2. LE RUNNER (le livrable — runner_natif/)

- `runner.ps1` — l'acquisition (le clone frais du dépôt public, la
  vérification des empreintes scellées AVANT toute exécution : loupe.exe
  c1115105…, proxy.exe 446279f3…, selftest.exe 8038585b…), l'exécution
  des scénarios (`scenarios.json` : la boucle WinMain T0-T7 de la
  vitrine, les vecteurs dorés loupe-13/02/16, le témoin 196 609 o), la
  production des témoins (le hash de chaque observable : l'écran, le
  disque, le code de sortie, la console), LA SIGNATURE (Ed25519, la clé
  du CI — la clé publique au dépôt, la privée au secret du CI) ;
- `confronter.py` — la confrontation au labo : les témoins reçus contre
  les attentes (les oracles hashlib du panneau, les découpes Python des
  fenêtres, la base SANE de la boucle) — TOUT écart un refus nommé
  TEMOIN-DIVERGENT ;
- `scenarios.json` — la liste CONSIGNÉE des scénarios (les mêmes que la
  campagne, la graine 20261120) ;
- LE CONTRÔLE NÉGATIF (vécu au labo sur le mécanisme) : un lanceur muté
  (le shim falsifié) est REFUSÉ À LA PREMIÈRE LIGNE — l'empreinte du
  lanceur signée dans le témoin, la vérification la rejette nommément.

## 3. CE QU'IL ATTRAPE (le gain nommé)

- L'ÉCART ÉMULATION/NATIF : le comportement des octets scellés au VRAI
  Windows — l'ABI réelle (le shadow space servi par le chargeur, les
  volatils réellement détruits), l'IAT résolue par LE VRAI chargeur
  (les 34 feuilles aux adresses réelles, la hint/RVA de l'Entrée 304),
  les feuilles kernel32/user32/gdi32 RÉELLES (le CreateFileW vrai, le
  ReadFile vrai — les shims du harnais sont bons, le natif le PROUVE) ;
- LA RÉGRESSION D'ENVIRONNEMENT : le Windows du CI (une version, un
  correctif — le témoin daté le porte) ;
- LA DISCIPLINE DU TÉMOIN : chaque exécution laisse une pièce signée,
  vérifiable, datée — le journal de transparence s'y ancre (bk79jvzbm
  point 6 : le témoin d'époque).

## 4. CE QU'IL N'ATTRAPE PAS (les limites nommées)

- LA MESURE DU TERRAIN DU DÉVELOPPEUR : la machine du maître (le CPU
  SHA-NI réel, l'horloge, la charge) — le CI n'est PAS le terrain, ses
  chiffres ne sont JAMAIS présentés comme terrain ;
- LA PREUVE DE SÛRETÉ FACE AUX ENTRÉES NON FIABLES À VOLUME : le
  million fuzzé vit au HARNAIS (la mémoire-ombre, les canaris — le
  natif n'en porte pas) ;
- LA MESURE DE PERFORMANCE EN RÉGIME : l'horloge du CI est CONTENDUE
  (les runners partagés) — les mesures de régime demeurent au labo
  (RDTSC isolé) et au terrain (la machine du maître) ;
- LA COUVERTURE DES CONFIGURATIONS : UN Windows du CI — pas la
  matrice des machines réelles (le terrain demeure).

## 5. LE DELTA AU MODÈLE DE MENACE (aux deux bords)

- CE QUE LE RÉGIME AJOUTE (le bord du labo) : la détection de la
  divergence émulation/native AVANT le terrain (la classe de l'Entrée
  207 : le défaut que SEUL le vrai chargeur révèle) — la fenêtre des
  défauts d'environnement se FERME au CI, plus seulement au terrain ;
- CE QUE LE RÉGIME AJOUTE (le bord du public) : le témoin signé est
  VÉRIFIABLE PAR TIERS (la clé publique au dépôt) — la preuve
  d'exécution natif devient une pièce publique, pas une affirmation ;
- CE QU'IL N'AJOUTE PAS : la preuve d'absence de défaut (le natif
  exécute les scénarios CONSIGNÉS — l'espace non couvert demeure), la
  confiance dans la clé du CI (un secret de CI — jamais la clé du
  sceau-I : la cérémonie hors-ligne demeure l'autorité).

## 6. LA DÉCISION (append-only, au journal des décisions)

LE TROISIÈME RÉGIME NOMMÉ « ORACLE NATIF » : les résultats du régime
sont NOMMÉS « natif » PARTOUT où ils apparaissent (le manuscrit, la
table des statuts, les preuves) — JAMAIS confondus avec le terrain du
développeur ; le runner vit au dépôt (oracle_natif/), sa clé publique
au dépôt, sa clé privée au secret du CI ; l'exécution appartient au CI
(le geste du maître : l'armement du runner), la confrontation au labo
(automatique, fail-closed).

**Alternatives rejetées** : (a) l'exécution natif MANUELLE au terrain
seulement (le précédent M10 — le natif AUTOMATISE la répétition, la
dette de la vitrine vivante à la main) ; (b) le natif SANS signature
(le témoin muet n'est pas une preuve — la signature fait le témoin) ;
(c) le natif comme REMPLACEMENT du harnais (le refus : la sûreté à
volume et la mutation demeurent au labo — les trois régimes se
COMPLÈTENT, jamais ne se remplacent).
