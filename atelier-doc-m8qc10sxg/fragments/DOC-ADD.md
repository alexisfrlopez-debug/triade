# DOC-ADD — the ADD operation (canonical English, compact)
The addition rides the skeleton SQUELETTE-v2: the ABI frame and the
typed holes are given; you emit the LOGIC lines only. One instruction
per line; one memory operand per instruction at most; typed holes
only (register / offset / LBL-CST target); the dictionary IDs —
CST-001..NNN for constants and IAT entries (the IAT is called: call
CST-004), LBL-001..NNN for internal labels, uppercase, on their own
line; the narrow source (movzx rax, ecx); no inline data (the data
lives in the frame); no string-prefix REP instructions. Budget:
2200 (unrounded at the manifest); the repair budget is 3. On a
refusal, read the named diff, repair the named cause alone, resubmit
— the judges are intact, a weakened judge is a lost gain. The
canonical form is expected from you at the first emission: the
normalizer never repairs a forbidden form.
