sup-21 · horodatage du run · révision 1
Intention : donner au run terrain son identité temporelle avant la moindre
écriture : le nom du fichier journal (terrain_YYYYMMDD_HHMMSS.txt, unique
par run — les journaux s'accumulent dans le dossier Drive au lieu de
s'écraser) ET la ligne d'ouverture "S01 date YYYYMMDD_HHMMSS" que le
scénario journalisera. Un run = un nom = un fichier téléversé : le
développeur relance autant de fois qu'il veut, chaque constat arrive
séparé dans le dossier test.
Contrat :
  pre  : P1 appelé par sup-01 avant sup-02 (P1 de sup-01) ; P2 TAMPON_NOM
         (32 o @0x3AD0) et TAMPON_AFF (32 o @0x3AF0) vierges ou
         recyclables ; P3 pile alignée.
  post : Q1 GetLocalTime(SYSTEMTIME pile 16 o) ; Q2 TAMPON_NOM contient
         exactement 27 caractères + NUL : "terrain_" + AAAA + MM + JJ +
         "_" + HH + MM + SS + ".txt" (chiffres décimaux zéro-paddés,
         aucune virgule, aucun séparateur régional — le nom est un
         identifiant, pas une phrase) ; Q3 TAMPON_AFF contient "S01 date "
         + les 15 mêmes chiffres (24 o, sans NUL utile — la longueur est
         portée par le retour) ; Q4 rax = 24 (longueur de TAMPON_AFF).
  inv  : I1 chiffres produits par division binaire inline (u16 -> 4 ou 2
         chiffres, '0' + quotient) — aucun itoa signé (libc-04 formate un
         i32, pas un u16 paddé : réutilisation impropre rejetée) ; I2
         aucune allocation : tout vit sur pile et .data ; I3 le même
         flottement de secondes sert les DEUX compositions (une seule
         lecture de l'heure — le nom et la ligne ne peuvent diverger).
Échecs :
  E1 : GetLocalTime ne peut pas échouer (remplit toujours) ; aucune
       branche d'échec — le bloc est total, rax = 24 garanti.
Vecteurs :
  V1 : round-trip 100 %.
  V2 : émulation GetLocalTime fixé (2026-10-27, 09:30:12, mardi) ->
       TAMPON_NOM == "terrain_20261027_093012.txt\0" octet par octet,
       TAMPON_AFF == "S01 date 20261027_093012", rax = 24.
  V3 : minuit/frontières — (2000-01-01 00:00:00) -> "terrain_20000101_
       000000.txt" (paddage à zéro prouvé) ; (2026-12-31 23:59:59) ->
       chiffres exacts.
  V4 : falsification — remplacer le diviseur 10 par 16 fait échouer V2
       (chiffres hexadécimaux parasites).
Fixtures    : aucune (données produites, jamais lues).
Provenance  : écrite-avant-code.
Décisions   : D48 (journal horodaté unique par run — exigence développeur
              « les logs envoyés automatiquement dans un dossier du drive » :
              l'accumulation exige des noms distincts) ; GetLocalTime et non
              GetSystemTime (constat en heure locale du terrain).
