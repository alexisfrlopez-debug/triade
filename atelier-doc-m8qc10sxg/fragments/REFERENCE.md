# REFERENCE — the protocol in one page (canonical English)
Three inseparable layers: I (the signed specifications), C (the
encrypted card), B (the byte-locked artifact). Lexicographic
priorities: security > performance > optimization > token cost.

The notation: one instruction per line; typed holes (register /
offset / LBL-CST target); dictionary IDs only — CST-001..NNN for
constants and IAT entries (the IAT is called: call CST-004), LBL-001
..NNN for internal labels (uppercase, on their own line); the narrow
source (movzx rax, ecx); one memory operand per instruction at most.

The judges: the pointer-alone expansion chain v2, the validators v3,
the round-trip (what you write is what expands is what comes back).
A one-byte mutant is caught — never game the judge.

The budgets (unrounded operands at the kit manifest): locate 627
/ edit 674 / add 2200; the repair budget is 3.

The gates R1-R11:
- R1: never a bare binary (every B ships with I and C)
- R2: intent first (every change starts as a diff on I)
- R3: mandatory marking (every block is described in C)
- R4: patch at stable contract (callers are never invalidated)
- R5: verify-then-write (no commit without oracle, gold vectors, round-trip)
- R6: crystallization (ten green verifications make the block immutable)
- R7: stable addresses (entry points never move; padding)
- R8: cross-lock (block fingerprints and card signature checked before every edit)
- R9: signed card required (an unsigned card is refused at startup)
- R10: built-in controlled failure (checksums, manifest signature, anti-rollback, environment — fail-closed, no degraded path)
- R11: measured optimization (a hot path identified by measure, before/after journaled, contract stable)

The refusal classes: HORS-FORMAT, ID-INCONNU, EXPANSION-DIVERGENTE,
FORME-INVALIDE (the notation); HUNK-INCONNU, CONTEXTE-DIVERGENT,
ROUND-TRIP-DIVERGENT (the edit); POINTEUR-INCONNU,
EMPREINTE-DIVERGENTE (the pointer). Repair the named cause alone.

The 18 bench blocks (the sealed notations of the repository):
loupe-01-ouvrir
loupe-02-lire
loupe-03-fermer
loupe-04-cadre
loupe-05-sha256
loupe-06-md5
loupe-07-cumul
loupe-08-ligne
loupe-09-ecran
loupe-10-peinture
loupe-11-defilement
loupe-12-aller
loupe-13-recherche
loupe-14-suivant
loupe-15-curseur
loupe-16-saisie
loupe-17-sauver
loupe-18-quitter

The ceremonies: the air-gap key genesis, the LOCAL seal, the
append-only journal (corrections are errata, never rewrites), the
secret guard at commit, the release deposit as a human command.

Decisions cited as literals (never translated): D81 (the durable
guard), D105 (the marked test phrase), D122 (the human send), D130
(the kit by construction), D203 (the kappa grid), D207 (the stopping
rules), D209 (the grant), D250 (the arbitration to the developer).
