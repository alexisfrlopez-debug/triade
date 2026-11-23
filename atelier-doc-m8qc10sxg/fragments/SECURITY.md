# SECURITY — the model in one page (canonical English)
Secrets: never committed — the pre-commit guard combines known-secret
sha256 fingerprints, Shannon entropy (3.8 bits/char on assignments of
28 characters or more) and class patterns (ghp_ / GOCSPX- / PEM /
refresh). The scrub gate is fail-closed with a lived negative control:
a planted secret MUST be caught.

Anchors: NO project trust anchor ships with the kit — neither the
project public key nor reference signatures. The adopter runs their
own air-gap key genesis; the seal is LOCAL.

The real vault is never touched in the lab (D105): lab copies carry a
visible marked test phrase; a report carrying one is REFUSED at the
gate.

Access discipline: the pointer alone (never a bare path); the four
named pointer refusals (null, out-of-zone, size, alignment); one
instruction per line; one memory operand per instruction at most.

Feedback reports: anonymized mechanically (paths, usernames), secret
scan at the door, the schema frozen by sha256 BEFORE any report; the
commentary (500 tokens at most) is marked UNVERIFIED; sending is a
human gesture (D122) — never automatic, the tool is offline.

Dual use: interceptor binaries and dual-use material are excluded
from the permissive subset; the Apache-2.0/CC-BY synthetic tasks stay
separate from the BSL corpus in every split.

Licence: BSL 1.1 with the D209 grant; public digests under CC-BY-4.0
(contributors acknowledged opt-in).

Offline by construction: no network dependency at build (R10); the
tooling runs air-gap.
