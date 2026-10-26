# Jalon M0 — chaîne artefact TRIADE

> Première implémentation du protocole : prouver la chaîne **notation → octets →
> PE32+ → exécution** sans compilateur, sur le profil primaire `x86-64-win11-pe`.
> M0 est le jalon existentiel : s'il échoue, le paradigme entier est remis en
> question avant tout investissement supplémentaire (PLAN_MILESTONES).

**Statut : M0-dev atteint** (oracle vert, construction 0/0, artefact
`0.1.0-dev.1` au sens du schéma § 9 de la spécification). La validation terrain
Windows 11 — exécuter `hello.exe` — reste le critère de sortie qui cloût le
jalon ; voir « Procédure de validation terrain » ci-dessous.

## Résultats mesurés (session du 26 octobre 2026)

| Contrôle | Résultat |
|---|---|
| Round-trip de notation (R5) | **100 %** — 18/18 instructions (9 + 6 + 3), keystone → capstone → keystone, octets et texte identiques |
| Oracle structurel (contrats I sur le code) | **31 verrous PASS** |
| Construction | **0 erreur / 0 avertissement** |
| Artefact | **hello.exe, 1 536 octets** (< 4 Kio), déterministe (sha256 `c89e330cd16f3fd48558ed4fdb6708fb671e6d907547d5c1ee28075ffd6507f2`) |
| Validation PE (3 outils indépendants) | capstone + pefile + objdump concordants : PE32+, entry `0x140001000`, console, `DYNAMICBASE \| HIGH_ENTROPY_VA \| NX_COMPAT`, imports kernel32 ×3, BASERELOC présent |
| Carte v0 (R9) | 4 fragments chiffrés XChaCha20-Poly1305, signature Ed25519, empreinte racine consignée |
| Verrou croisé (R8) | signature + racine + 3 empreintes de blocs revérifiées en relecture indépendante |
| Falsification | un octet modifié dans `.text` → **échec immédiat** (exit 1, fail-closed) |

## Structure

```
m0/
├── README.md              ce fichier
├── I/                     couche I : 3 spécifications (gabarit § 2.2, écrites avant la notation)
│   ├── README.md          registre des domaines du projet (figé, § 2.1)
│   ├── hello-01-main.md   orchestration (bloc a10001)
│   ├── hello-02-write.md  écriture stdout (bloc a10002)
│   └── hello-03-exit.md   sortie propre (bloc a10003)
├── notation/              notation x86-64 Intel des trois blocs (keystone)
├── build_m0.py            éditeur PE32+ + oracle + carte + verrou croisé (ci-dessous)
├── carte_m0.py            couche C : crypto (Argon2id, HKDF, XChaCha20, Ed25519)
├── hello.exe              artefact B (1 536 o)
├── carte/                 couche C : en-tête signé, 4 fragments chiffrés, signature, tableau de bord
└── .keys/                 secrets LOCAUX (phrase maîtresse, graine Ed25519) — jamais committés
```

R1 est honoré par construction : l'artefact (`hello.exe`) vit entouré de sa
couche I (`I/`) et de sa couche C (`carte/`) dans le même dépôt, au même commit.

## Layout fixe (R7 — jamais déplacé)

| Objet | RVA | Taille |
|---|---|---|
| Bloc a10001 (main, point d'entrée) | `0x1000` | slot 64 o (43 o de code + 21 de NOP) |
| Bloc a10002 (write) | `0x1040` | slot 64 o (27 o de code + 37 de NOP) |
| Bloc a10003 (exit) | `0x1080` | slot 64 o (12 o de code + 52 de NOP) |
| Message « TRIADE M0 : Hello, Windows 11 ! » | `0x2000` | 34 o (33 + NUL) |
| Descripteurs d'import kernel32 (+ terminateur) | `0x2030` | 40 o |
| IAT : GetStdHandle, WriteFile, ExitProcess | `0x20B0` | 32 o (4 qwords) |
| Bloc de relocalisation minimal (ASLR) | `0x20D0` | 12 o |

Sections : `.text` RX à `0x1000`, `.rdata` R à `0x2000`, alignements 0x1000/0x200,
ImageBase `0x140000000`, SizeOfImage `0x3000`. Les déplacements RIP de la
notation sont calculés **une fois pour toutes** depuis ce layout et vérifiés
**sémantiquement** par l'oracle (la cible de chaque `[rip ± d]` doit tomber
exactement sur le slot IAT ou de donnée attendu) : aucun post-patching, la
notation est ce qui s'exécute (WYSIWYG).

## L'oracle M0 (D1 : régénéré depuis I à chaque exécution)

1. **Round-trip de notation** : chaque bloc assemblé par keystone est désassemblé
   par capstone puis ré-assemblé — octets ET texte (normalisé) identiques.
2. **Contrat structurel** : les pré/post-conditions et invariants déclarés dans
   `I/*.md` sont vérifiés mécaniquement sur le code désassemblé — discipline
   d'entrée (`sub rsp, 0x28`), appels IAT uniquement (jamais `syscall`/`int`),
   aucun stockage sous RSP, arguments 4/5 de WriteFile annulés avant l'appel,
   frame équilibré, `ud2` défensif du bloc de sortie, padding inter-blocs ≥ 16,
   cibles RIP sémantiques, longueur du message exacte.

L'oracle différentiel complet (entrées aléatoires contraintes par les
pré-conditions, ~12 000 cas par bloc critique) est un livrable de M1 avec la
mini-libc — premier terrain de cristallisation. À M0, les blocs n'ont pas de
sémantique exécutable vérifiable hors Windows : l'oracle structurel + le
round-trip + la validation terrain forment la chaîne de preuve.

## Utilisation

```bash
cd m0
python3 build_m0.py             # construction + oracle + carte + verrou croisé
python3 build_m0.py --verifier  # verrou croisé seul (R8, avant chaque édition)
```

Dépendances : `keystone-engine`, `capstone`, `pefile`, `pynacl`, `argon2-cffi`,
`cryptography`. La construction est déterministe (horodatages nuls, layout
fixe) : deux exécutions produisent le même `hello.exe`.

## Clés et continuité

- La **phrase maîtresse** (128 bits, générée à la première exécution) dérive par
  Argon2id (64 Mio, 3 itérations) puis HKDF les clés des quatre fragments. Elle
  est affichée **une seule fois** puis stockée dans `.keys/passphrase.txt`
  (chmod 600, hors dépôt). **Mettez-la en coffre** (gestionnaire de mots de
  passe) : sans elle, la carte est indéchiffrable — par conception.
- La **graine Ed25519** (`.keys/ed25519.seed`) signe la carte ; la clé publique
  est committée (`carte/cle-publique.ed25519`).
- Perte de phrase : la carte peut être **reconstruite** depuis I + notation
  (le builder régénère tout) avec une nouvelle phrase — la valeur perdue est le
 continuité de l'historique chiffré, pas le projet.
- Le sel Argon2id est une constante documentée du projet : la dérivation est
  reproductible depuis la seule phrase maîtresse (choix D26).

## Procédure de validation terrain (critère de sortie M0)

1. Récupérer `hello.exe` (miroir Drive `TRIADE/m0/` ou copie `download/`).
2. Sur Windows 11 : `cd` vers le dossier, puis `.\\hello.exe` (PowerShell) ou
   `hello.exe` (cmd). Defender peut demander confirmation — l'exécutable est
   non signé (la signature de code est un chantier séparé, hors M0).
3. Attendu : la ligne `TRIADE M0 : Hello, Windows 11 !` s'affiche, code de
   sortie 0 (`$LASTEXITCODE` / `%ERRORLEVEL%`).
4. Consigner le résultat au journal des décisions → la balise `0.1.0-dev.1`
   devient candidate à la cristallisation M0 (écart éventuel → patch `0.1.0+1`
   à contrat stable, R4).

## Limites assumées (consignées D26)

- **CFG différé** : `DllCharacteristics` porte DEP/ASLR/HEVA ; Control Flow
  Guard exige une `LOAD_CONFIG` avec table GFIDS dont la conception (cibles
  d'appels indirects IAT) est reportée à M1+ — pas un affaiblissement de M0,
  dont le profil (manuel agent § 7.2) exige DYNAMICBASE, HIGH_ENTROPY_VA et
  NX_COMPAT, tous actifs.
- **Table de relocalisation minimale** : entrées ABSOLUTE (padding) — le code
  est entièrement RIP-relatif, aucune adresse absolue à corriger ; le
  descripteur BASERELOC existe pour honorer DYNAMICBASE.
- **Pas de tag git pour `0.1.0-dev.1`** : la balise d'artefact vit dans le
  manifeste frag-bld (usage interne, § 9) ; le tag viendra avec la
  cristallisation du jalon si le développeur la demande.
- **Génération de clé du bloc** : la graine Ed25519 du projet M0 est locale à
  ce poste ; l'export de continuité chiffré (D16) est le mécanisme prévu pour
  transférer l'état — non requis à M0 (première génération, aucune reprise
  inter-agents à ce stade).
