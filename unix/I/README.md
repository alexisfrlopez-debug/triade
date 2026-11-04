# Couche I — lignée du jalon M6 (unix/, D149) : la sonde du durcissement + le corpus paritaire

Quatre spécifications nouvelles au chantier M6-(a), écrites avant la notation
(R2, provenance `écrite-avant-code`). Elles instancient le gabarit § 2.2 de la
spécification et étendent le registre figé du projet (m0/I/README.md, § 2.1)
par le domaine **`su`, réservé à la sonde du jalon M6** (chantier M6-(a) — le
durcissement format) : le premier artefact du jalon, dans `unix/` (convention
de dossiers D149-(5)). Le domaine `ah` reste celui de l'échelle
d'auto-hébergement D34 ; aucune adresse n'est héritée — les deux lignées ne
partagent que la couche de méthode.

| Spécification | Bloc machine (carte) | Rôle | Zone |
|---|---|---|---|
| su-01:R1 | f60001 | Écriture par appel système (sys_write) | sys @ 0x1000 |
| su-02:R1 | f60002 | Formatage hexadécimal u64 → 16 caractères | hex @ 0x1040 |
| su-03:R1 | f60003 | Verdict d'erreur syscall (table ERRNOS) | sys @ 0x10C0 |
| su-04:R1 | f60004 | Orchestration — point d'entrée ELF `sonde` | app @ 0x1140 |

L'artefact `sonde` est la démonstration exécutable du durcissement format
(le critère de sortie du chantier M6-(a)) : image **ET_DYN/PIE** chargée par
le noyau à une base aléatoire — la sonde calcule sa propre base à l'exécution
(`lea rip` sur le témoin `.rodata`, lien-temps soustrait) et l'émet en tête
de sortie ; **trois segments R/RX/RW** (W^X : aucun segment inscriptible
exécutable, vérifié depuis les phdr par le build) ; **PT_GNU_STACK sans X**
(NX explicite) ; **table ERRNOS** (le contrat d'erreurs des syscalls, miroir
de la table HRESULTS) exercée en exécution sur ses deux branches : une
sonde volontaire `write(-1, …)` rend -EBADF (errno nommé → verdict 1), une
sonde volontaire `write(1, 0x1, …)` rend -EFAULT (errno hors table →
VERDICT_FATAL 6 → arrêt propre, code de sortie 6).

## Le corpus paritaire (chantier M6-(b) — le diff nul sur la couche I)

Le chantier M6-(b) ajoute le **corpus nominal** de D149-(2) : les révisions
de granularité R+1 des douze contrats du patrimoine (arguments nommés dans
la couche I, convention d'appel déplacée vers frag-con — spécification
§ 8.3-4) et le principal propre au jalon. Les ancêtres R1/R2/R3 demeurent
INTACTS dans m0/I, m1/I, m2/I (chaînes scellées vivantes, sceau-I à onze
arbres verts) ; les révisions vivent ICI, dans l'arbre du jalon — c'est la
même couche I que M7 instanciera en troisième (D149-(7)). L'audit complet
vit à `AUDIT-COUPLAGE-CORPUS.md` (classes A/B/C, la classe A est VIDE — le
paramétrage msx64 était partout).

| Spécification | Ancêtre (scellé) | Bloc machine (carte) | Rôle | Zone du corpus |
|---|---|---|---|---|
| hello-02:R2 (écrire) | hello-02:R1 (m0/I, 0.1.0) | f61001 | Interface — écriture du flux | io @ 0x1000 |
| hello-03:R2 (sortir) | hello-03:R1 (m0/I, 0.1.0) | f61002 | Interface — terminaison | io @ 0x1040 |
| libc-01:R2 | libc-01:R1 (m1/I, 0.2.0) | f61003 | memcpy (pur) | libc @ 0x1080 |
| libc-02:R2 | libc-02:R1 (m1/I, 0.2.0) | f61004 | memcmp (pur) | libc @ 0x10C0 |
| libc-03:R2 | libc-03:R1 (m1/I, 0.2.0) | f61005 | strlen (pur) | libc @ 0x1140 |
| libc-04:R3 | libc-04:R2 (m1/I, 0.2.0) | f61006 | itoa (pur) | libc @ 0x1180 |
| libc-05:R2 | libc-05:R1 (m1/I, 0.2.0) | f61007 | zone-alloc (pur) | libc @ 0x1200 |
| libc-06:R2 | libc-06:R1 (m1/I, 0.2.0) | f61008 | zone-reset (pur) | libc @ 0x1280 |
| libc-07:R2 | libc-07:R1 (m1/I, 0.2.0) | f61009 | memset (pur) | libc @ 0x12C0 |
| libc-08:R3 | libc-08:R2 (m1/I, 0.2.0) | f61010 | auto-test (21 vecteurs dorés) | app @ 0x1340 |
| tcp-11:R2 | tcp-11:R1 (m2/I, 0.3.0) | f61011 | ligne de journal (verrou tournant) | app @ 0x1840 |
| tcp-07:R4 | tcp-07:R3 (m2/I, 0.3.0) | f61012 | moteur de patch (mprotect) | app @ 0x19C0 |
| corpus-13:R1 | — (domaine neuf, modèle ah-09) | f61013 | Orchestration — point d'entrée ELF `corpus` | app @ 0x1BC0 |

L'artefact `corpus` (balise **0.7.0-dev.2**) hérite le durcissement de la
sonde (ET_DYN/PIE, segments R/RX/RW, PT_GNU_STACK sans X) et porte le
patrimoine : le rituel de parité de corpus-13 lance l'auto-test (la ligne
"TRIADE M1 : minilibc 21/21 OK" — les mêmes 21 vecteurs dorés que
selftest.exe, scellé 0.2.0), journalise le verdict par tcp-11 (le verrou
d'exclusion de l'instance Linux est un qword tournant `lock xchg`, né
déverrouillé — aucune initialisation) et termine au code du verdict par
sortir. tcp-07 vit dans l'image avec son staging (le journal v2 assemblé
pour la croissance — la démonstration M5-(c) du chantier (d)) ; la CIBLE du
patch, au plan du corpus, est l'entrée de tcp-11.

La discipline des adresses suit D28/D33 : slots multiples de 64, alignés 16,
padding inter-blocs >= 16, réserves int3. Le verrou croisé R8 s'applique dès
le premier octet ; la carte du corpus est une génération 1 propre (sel de
dérivation distinct de la sonde et de l'échelle auto-hôte, clés projet
partagées D27). La série d'identifiants f61xxx est nommée par la carte du
corpus (f60xxx demeure à la sonde).
