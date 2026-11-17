### NOTES D'AUTEUR

#### Exigences et signature
- **Intention** : Condensé SHA-256 d'une gamme de fichier via une composition héritée (tls13-01..04), lecture fenêtrée (64 Kio), sans copie des blocs hérités.
- **Signature** :  
  `loupe-05 · sha256 d'une gamme : l'héritage tls13 PAR LA CARTE · révision 1`  
- **Fixtures** : Vecteurs FIPS 180-4 (vide, "abc"), proxy.exe scellé (gamme entière, empreinte attendue `446279f3…`).

#### Pièges nommés
- **P1** : Session fermée → `-4 SESSION`.  
- **P2/P3** : Décalage/longueur invalides → `-3 HORS-BORNES`.  
- **P4** : Sortie non accessible → `-5 ENTRÉE`.  
- **E4** : Échec `ReadFile`/`SetFilePointerEx` → `-6 SYSTÈME` (sortie intacte).  
- **Falsification** : Mutation de `TAMPON_CUMUL` entre fenêtres → divergence de condensé (test V5).

#### Invariants à tenir
- **I1** : Héritage PAR LA CARTE (tls13-01..04 octet-identiques au scellé 1.0.0, R7).  
- **I2** : Aucune SHA redéclarée (contexte 112o à tls13-01, source unique T5).  
- **I3** : Lecture via `TAMPON_CUMUL` (jamais la vue du cadre).  
- **I4** : Repositionnement systématique du pointeur fichier (`SetFilePointerEx` avant chaque `ReadFile`).  
- **I5** : IAT déclarée (D161 : `SetFilePointerEx`, `ReadFile`, `GetLastError`), registres non volatils rendus, NOP (0x90).

#### Cas d'échec
- **E1** : Session absente → `rax = -4`.  
- **E2** : Gamme hors fichier → `rax = -3`.  
- **E3** : Sortie inutilisable → `rax = -5`.  
- **E4** : Erreur système → `rax = -6` (code `GetLastError` consigné, sortie intacte).