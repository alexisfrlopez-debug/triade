### NOTES D'AUTEUR

#### Exigences et signature
- **Signature** : `rcx` (fenêtre), `rdx` (taille fenêtre), `r8` (motif), `r9` (taille motif), `[rsp+0x28]` (départ).
- **Postulat** : `P1` à `P5` (préconditions sur les arguments et la mémoire).
- **Verdicts** :
  - `Q1/Q4` : `rax` = position absolue de la première occurrence (memcmp héritée).
  - `Q2/Q3` : `rax` = -1 (absence, plage vide, motif trop long).
- **Échecs** : `E1`, `E2`, `E3` → `rax` = -5 (entrée invalide).
- **Signature d'appel** : Seul `libc-02` (`memcmp`) autorisé, liste fermée.

#### Pièges nommés
- **R7** : Interdiction de réécrire la comparaison byte-à-byte (toujours passer par `memcmp`).
- **Falsification (V4)** : Ne jamais retourner une occurrence autre que la première (différentielle Python exigeante).
- **Trivialité (Q2)** : Vérifier immédiatement si `r9 > (rdx - départ)` → `-1` sans boucle.

#### Invariants à tenir
- **I1** : Aucune IAT, aucun syscall, aucun état détenu (pureté fonctionnelle).
- **I2** : Seul `memcmp` (libc-02) pour les comparaisons, via bloc scellé M1.
- **I3** : Fenêtre et motif non modifiés, complexité `O(n·m)` honnête (m ≤ 32).
- **I4** : Registres non volatils préservés (`NOP`, `0x90`).

#### Cas d'échec
- **E1** : `r9 = 0` (motif vide) → `-5`.
- **E2** : `r9 > 32` (motif trop long) → `-5`.
- **E3** : `départ > rdx` (départ hors fenêtre) → `-5`.
- **Cas limites** : `départ = rdx` → `-1` (Q3), `r9 > (rdx - départ)` → `-1` (Q2).