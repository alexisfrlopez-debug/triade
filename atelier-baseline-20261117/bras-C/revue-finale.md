=== LA REVUE ===

**Conformité au contrat :**
  P1 : honorée.
  P2 : honorée.
  P3 : honorée.
  P4 : honorée.
  Q1 : honorée.
  Q2 : honorée.
  Q3 : honorée.
  Q4 : honorée.
  I1 : ÉCART.
  I2 : ÉCART.
  I3 : honorée.
  I4 : honorée.
  I5 : honorée.

**Écarts nommés :**
  I1 : L'héritage PAR LA CARTE n'est pas respecté. Le code redéclare et implémente les fonctions SHA-256 (ctx_sha256, K[], sha256_transform, etc.) au lieu d'utiliser les blocs tls13-01..04 fournis par l'héritage.
  I2 : Le code viole l'invariant "AUCUNE constante SHA re-déclarée". La table de constantes K[] et la structure ctx_sha256 sont définies localement, alors que tls13-01 (le bloc d'initialisation) doit être la source unique de ces éléments.

**Verdict :**
  ÉCART