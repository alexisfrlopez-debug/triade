# TROUBLESHOOTING — the named refusals and what they mean (canonical English)
The protocol never fails silently: every gate refuses with a NAMED
cause. Find the name, repair the named cause alone.

Model notations refused (the judge chain v2 + the validators v3):
- HORS-FORMAT — a line is not an admitted form (a string-prefix REP
  instruction, an inline db, a lowercase label glued to an
  instruction, a truncated literal). Repair: the canonical motif —
  one instruction per line, typed holes.
- ID-INCONNU — an ID absent from the block dictionary. Repair: the
  enumerated IDs only (CST-001..NNN, LBL-001..NNN), never a bare
  symbol.
- EXPANSION-DIVERGENTE — the expanded line diverges (a round-trip
  mismatch, an IAT reached through a label, an ID in a non-expandable
  operand). Repair: the typed hole (mov reg, CST-001 for a constant;
  call CST-004 for the IAT; jcc LBL-001 for an internal jump).
- FORME-INVALIDE — the emitted shape violates the sealed template.
The four pointer refusals at LOCATE (null, out-of-zone, size,
alignment) are named at the gate.

The budget (3 repairs) exhausted: the task ends refused — the verdict
is a piece as precious as a green; never a re-drawn task, never a
silently widened budget.
The doc linter refuses: a numeric divergence between the EN and FR
mirrors, a translated identifier — the parity gates.
The secret scan refuses: a secret, or the marked test phrase (D105) —
the lab copies carry visible marks; the real vault is never touched
in the lab.
The kit gate refuses: an incompatible checkpoint / kit / judges
triplet — fail-closed, named.
The aggregator refuses: a missing run (exit 2, never a partial
verdict); fewer than 10 complete strata reads NOT TESTED (D207).
The kappa gate needs BOTH conditions together (D203): 0.61 reached ON
at least 50 double-coded items.
R10 refuses at launch (checksums, manifest signature, anti-rollback,
environment) — no degraded path exists.
Without response_format at the endpoint: the grammar rides the prompt
and the validators judge — never a weakened judge (the graceful
degradation).
