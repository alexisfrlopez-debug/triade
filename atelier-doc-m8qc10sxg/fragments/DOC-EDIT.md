# DOC-EDIT — the EDIT operation (canonical English, compact)
The edit rides the sealed template TPL-EDIT-v1: emit the hunks, never
a free-text rewrite. The four edit refusals are named — HORS-FORMAT
(the hunk shape violates the template), HUNK-INCONNU (the hunk does
not apply at its anchor), CONTEXTE-DIVERGENT (the surrounding bytes
moved), ROUND-TRIP-DIVERGENT (what you wrote does not come back) —
repair the named cause alone, every untouched line byte for byte.
The patch honors the published contract (R4): same signature, same
pre- and post-conditions, the callers are never invalidated. No
commit without the oracle, the gold vectors and the round-trip (R5).
Budget: 674 (unrounded at the manifest); the repair budget is
3. The reference is the sealed notation of the block — never a
recitation of a neighbor, the exemplar is a reference, not a
shortcut.
