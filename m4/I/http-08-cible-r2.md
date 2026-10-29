http-08 · cible : forme absolue https · révision 2
Ancêtre : http-08:R1 (D46, scellée 0.4.0 — la spécification R1 vit dans
m3/I/ et ne change pas : la balise est immuable § 9). La révision vit en
M4 et ne modifie que CE que le tunnel exige : la reconnaissance du schéma
« https:// » en forme absolue. Tout le reste de R1 (forme origine, forme
autorité CONNECT, chemin, casse, bornes) est REPRIS TEL QUEL — cité, non
recopié (T5).
Intention : étendre la lecture de la cible au schéma chiffré — LE seul
point du parseur qui sait que le tunnel existe : verdict distinct pour
« https:// », strict minuscule (durcissement délibéré hérité de R1 pour
« http:// » — pas de « HTTPS:// », pas de casse mixte).
Contrat :
  pre  : P1-P4 de http-08:R1 repris tels quels (span cible, longueur,
             sorties méthode/chemin/autorité, cadres de l'appelant).
  post : Q1-Q3 de http-08:R1 repris tels quels pour « http:// », forme
             origine et forme autorité ;
         Q4 NOUVEAU — forme absolue « https:// » (les 8 octets exacts,
             minuscules) : rax = verdict « cible TLS » (valeur propre à
             la révision, distincte du verdict « cible http » de R1) ;
             autorité et chemin découpés aux règles R1 (port implicite
             443 au lieu de 80 — consigné DANS la sortie, la décision
             d'appeler tls-08 appartient à http-10:R2) ;
         Q5 tout schéma non reconnu — y compris « https:// » mal cassé
             (« HTTPs:// », « https:/ », « https:\\ ») — reçoit le
             refus de schéma de R1 (400) : AUCUNE tolérance nouvelle, la
             surface de contrebande n'augmente que des 8 octets exacts.
  inv  : I1-I4 de http-08:R1 repris (feuille pure, aucune écriture, pas
             de NUL supposé, non-volatils) ; I5 NOUVEAU : la comparaison
             https est BYTE-EXACTE sur 8 octets — 8, pas 7, pas 9 : un
             schéma préfixe (« https://x » contre « http://s://x ») ne
             peut jamais produire le verdict TLS (l'ordre des tests est
             documenté : http:// d'abord, https:// ensuite — R1 n'a pas
             changé, la révision AJOUTE).
Échecs :
  E1 : schéma malformé → refus R1 (Q5) — hérité, inchangé.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : différentiel hérité V2 de R1 + 5 000 cibles https (casse mixte,
       préfixes piégeux, autorités dégénérées, ports explicites) contre
       modèle de référence — verdicts http/TLS/refus, découpages exacts.
  V3 : fuzzing à propriétés hérité (la cible reste une entrée non
       fiable directe : le harnais V3 de R1 s'étend au verdict TLS).
  V4 : test de rejet hérité (feuille pure).
Fixtures    : néant.
Provenance  : écrite-avant-code (révision inter-jalon, modèle win-02:R2).
Décisions   : D46 (ancêtre), D77, charte M4 § 5.
