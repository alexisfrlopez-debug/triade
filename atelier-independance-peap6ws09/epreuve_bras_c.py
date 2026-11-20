#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""epreuve_bras_c.py — L'ÉPREUVE POSIX DU BRAS C AUX TROIS CONTRATS (le
plan peap6ws09 § 2) : l'école (les cas tenus pour toujours), les rejets
nommés, LA DIFFÉRENTIELLE (2 000 cas par contrat, la graine 20261115,
le juge Python indépendant). gcc -O2, la sortie EPREUVE n/total VERT.
Les sources générés demeurent VERBATIM — l'écart exact consigné, jamais
corrigé silencieusement."""
from __future__ import annotations

import pathlib
import random
import subprocess
import sys

ICI = pathlib.Path(__file__).resolve().parent

PILOTES = {}

PILOTES["loupe-13"] = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
long loupe_13_recherche(const unsigned char *, long, const unsigned char *,
                        long, long);
static int verts = 0, total = 0;
static void cas(const unsigned char *f, long tf, const unsigned char *m,
                long tm, long d, long attendu, const char *nom) {
    long r = loupe_13_recherche(f, tf, m, tm, d);
    total++;
    if (r == attendu) verts++;
    else printf("ROUGE %s : rendu %ld attendu %ld\n", nom, r, attendu);
}
int main(int argc, char **argv) {
    unsigned char ecole[] = "AAAAAB";
    unsigned char m1[] = "A", m2[] = "AAAA", m3[] = "AB", m4[] = "Z";
    cas(ecole, 6, m1, 1, 0, 0, "ecole-premier-octet");
    cas(ecole, 6, m2, 4, 0, 0, "ecole-motif-repetitif");
    cas(ecole, 6, m3, 2, 5, -1, "ecole-depart-apres-occurrence");
    cas(ecole, 6, m4, 1, 0, -1, "ecole-absent");
    cas(ecole, 6, m1, 1, 3, 3, "ecole-depart-au-milieu");
    cas(ecole, 6, m2, 4, 2, -1, "ecole-plage-trop-courte");
    cas(ecole, 0, m1, 1, 0, -1, "ecole-fenetre-vide");
    cas(ecole, 6, m1, 1, 6, -1, "ecole-plage-vide");
    cas(ecole, 6, m1, 0, 0, -5, "rejet-motif-vide");
    unsigned char m33[33]; memset(m33, 'A', 33);
    cas(ecole, 6, m33, 33, 0, -5, "rejet-motif-33");
    cas(ecole, 6, m1, 1, 7, -5, "rejet-depart-au-dela");
    FILE *fv = fopen(argv[1], "rb");
    long n; fread(&n, 8, 1, fv);
    for (long k = 0; k < n; k++) {
        long tf, tm, d, attendu;
        fread(&tf, 8, 1, fv); fread(&tm, 8, 1, fv);
        fread(&d, 8, 1, fv); fread(&attendu, 8, 1, fv);
        unsigned char *f = malloc(tf ? tf : 1), *m = malloc(tm ? tm : 1);
        if (tf) fread(f, 1, tf, fv); if (tm) fread(m, 1, tm, fv);
        cas(f, tf, m, tm, d, attendu, "differentiel");
        free(f); free(m);
    }
    fclose(fv);
    printf("EPREUVE %d/%d VERT\n", verts, total);
    return verts == total ? 0 : 1;
}
'''

PILOTES["loupe-02"] = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
long loupe_02_lire(const unsigned char *, long, const long *,
                   const unsigned char *, long, unsigned char *,
                   long *, long);
static int verts = 0, total = 0;
static void cas(const unsigned char *f, long tf, const long *jd,
                const unsigned char *jo, long jn, long dec, long attendu,
                long att_rempl, const char *nom) {
    unsigned char tampon[384]; long rempl = -1;
    for (long i = 0; i < 384; i++) tampon[i] = 0xEE;
    long r = loupe_02_lire(f, tf, jd, jo, jn, tampon, &rempl, dec);
    total++;
    if (r != attendu || (attendu == 0 && rempl != att_rempl)) {
        printf("ROUGE %s : rendu %ld rempl %ld attendus %ld %ld\n",
               nom, r, rempl, attendu, att_rempl);
    } else verts++;
}
int main(int argc, char **argv) {
    unsigned char fichier[800]; memset(fichier, 'A', 800);
    const long jd1[] = {16}; const unsigned char jo1[] = {'Z'};
    cas(fichier, 800, jd1, jo1, 1, 0, 0, 384, "ecole-premiere-fenetre");
    cas(fichier, 800, jd1, jo1, 1, 384, 0, 384, "ecole-deuxieme-fenetre");
    cas(fichier, 800, jd1, jo1, 1, 768, 0, 32, "ecole-derniere-fenetre");
    cas(fichier, 100, jd1, jo1, 0, 96, 0, 4, "ecole-queue-4");
    cas(fichier, 800, NULL, NULL, 0, 0, -5, -1, "rejet-decalage-non-16");
    cas(fichier, 800, NULL, NULL, 0, 800, -3, -1, "rejet-hors-bornes");
    cas(fichier, 800, NULL, NULL, 0, 801, -3, -1, "rejet-au-dela");
    cas(fichier, 0, NULL, NULL, 0, 0, -3, -1, "rejet-fichier-vide");
    FILE *fv = fopen(argv[1], "rb");
    long n; fread(&n, 8, 1, fv);
    for (long k = 0; k < n; k++) {
        long tf, jn, dec, attendu, att_rempl, verif_tampon;
        fread(&tf, 8, 1, fv); fread(&jn, 8, 1, fv);
        fread(&dec, 8, 1, fv); fread(&attendu, 8, 1, fv);
        fread(&att_rempl, 8, 1, fv); fread(&verif_tampon, 8, 1, fv);
        unsigned char *f = malloc(tf ? tf : 1);
        if (tf) fread(f, 1, tf, fv);
        long *jd = malloc(jn ? jn * 8 : 8);
        unsigned char *jo = malloc(jn ? jn : 1);
        for (long j = 0; j < jn; j++) { fread(&jd[j], 8, 1, fv); fread(&jo[j], 1, 1, fv); }
        unsigned char tampon[384]; long rempl = -1;
        for (long i = 0; i < 384; i++) tampon[i] = 0xEE;
        long r = loupe_02_lire(f, tf, jd, jo, jn, tampon, &rempl, dec);
        total++;
        /* LE JUGE DU RECOUVREMENT : l'octet du journal à sa place (la
           cellule pointée par verif_tampon, -1 = la borne remplissage) */
        int ok = (r == attendu) && (rempl == att_rempl);
        if (ok && verif_tampon >= 0) {
            long dec_j = -1; unsigned char oct_j = 0;
            for (long j = 0; j < jn; j++)
                if (jd[j] >= dec && jd[j] < dec + att_rempl
                    && jd[j] - dec == verif_tampon) { dec_j = jd[j]; oct_j = jo[j]; }
            if (dec_j >= 0 && tampon[verif_tampon] != oct_j) ok = 0;
        }
        if (!ok) printf("ROUGE differentiel : rendu %ld rempl %ld attendus %ld %ld\n",
                        r, rempl, attendu, att_rempl);
        else verts++;
        free(f); free(jd); free(jo);
    }
    fclose(fv);
    printf("EPREUVE %d/%d VERT\n", verts, total);
    return verts == total ? 0 : 1;
}
'''

PILOTES["loupe-16"] = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
long loupe_16_saisie(long, unsigned char, long *, unsigned char *,
                     long *, unsigned char *, long, long, long *);
static int verts = 0, total = 0;
static void cas(long curseur, unsigned char octet, long jn_avant,
                long deja_au_journal, long attendu, long jn_attendu,
                long sale_attendu, const char *nom) {
    long jd[300]; unsigned char jo[300]; long jn = jn_avant;
    for (long i = 0; i < 300; i++) { jd[i] = -1; jo[i] = 0; }
    if (deja_au_journal >= 0) { jd[deja_au_journal] = curseur; jo[deja_au_journal] = 'x'; }

    for (long i = 0; i < 384; i++) tampon[i] = 'A';
    long sale = 0;
    long r = loupe_16_saisie(curseur, octet, jd, jo, &jn, tampon, 384, 0, &sale);
    total++;
    if (r != attendu || jn != jn_attendu || sale != sale_attendu) {
        printf("ROUGE %s : rendu %ld jn %ld sale %ld attendus %ld %ld %ld\n",
               nom, r, jn, sale, attendu, jn_attendu, sale_attendu);
    } else verts++;
}
int main(void) {
    cas(16, 'Z', 0, -1, 0, 1, 1, "ecole-premier-ajout");
    cas(32, 'Y', 1, -1, 0, 2, 1, "ecole-deuxieme-ajout");
    cas(16, 'W', 1, 0, 0, 1, 1, "ecole-remplacement");
    /* le journal plein : 256 distincts, le 257e refuse */
    long jd[300]; unsigned char jo[300]; long jn = 256;
    for (long i = 0; i < 256; i++) { jd[i] = i * 4; jo[i] = 'q'; }
    unsigned char tampon[384]; for (long i = 0; i < 384; i++) tampon[i] = 'A';
    long sale = 0;
    long r = loupe_16_saisie(5000, 'K', jd, jo, &jn, tampon, 384, 0, &sale);
    total++;
    if (r == -3 && jn == 256) verts++;
    else printf("ROUGE journal-plein : rendu %ld jn %ld\n", r, jn);
    printf("EPREUVE %d/%d VERT\n", verts, total);
    return verts == total ? 0 : 1;
}
'''


def vecteurs_13(rng) -> bytes:
    v = bytearray()
    N = 2000
    v += N.to_bytes(8, "little")
    for _ in range(N):
        tf = rng.randrange(0, 400)
        tm = rng.randrange(1, 33)
        d = rng.randrange(0, tf + 2) if tf else 0
        alphabet = bytes(range(256)) if rng.random() < .5 else b"AB"
        f = bytes(rng.choice(alphabet) for _ in range(tf))
        m = bytes(rng.choice(alphabet) for _ in range(tm))
        attendu = -5 if d > tf else (f.find(m, d) if 0 < tm <= 32 else -5)
        v += tf.to_bytes(8, "little") + tm.to_bytes(8, "little")
        v += d.to_bytes(8, "little")
        v += (attendu if attendu >= 0 else -1).to_bytes(8, "little", signed=True)
        v += f + m
    return bytes(v)


def vecteurs_02(rng) -> bytes:
    v = bytearray()
    N = 2000
    v += N.to_bytes(8, "little")
    for _ in range(N):
        tf = rng.randrange(0, 800)
        jn = rng.randrange(0, 6)
        dec = rng.randrange(0, 40) * 16 if rng.random() < .8 else rng.randrange(0, 801)
        f = bytes(rng.randrange(256) for _ in range(tf))
        jd = sorted(rng.sample(range(0, max(tf, 1)), jn)) if tf else []
        jo = bytes(rng.randrange(256) for _ in range(jn))
        # LE JUGE : remplissage et le recouvrement vérifié à UNE cellule
        if dec % 16 != 0:
            attendu, att_rempl = -5, -1
        elif dec >= tf:
            attendu, att_rempl = -3, -1
        else:
            attendu, att_rempl = 0, min(384, tf - dec)
        # la cellule vérifiée : la PREMIÈRE entrée du journal dans la fenêtre
        verif = -1
        for j in range(jn):
            if attendu == 0 and jd[j] >= dec and jd[j] < dec + att_rempl:
                verif = jd[j] - dec
                break
        v += tf.to_bytes(8, "little") + jn.to_bytes(8, "little")
        v += dec.to_bytes(8, "little")
        v += attendu.to_bytes(8, "little", signed=True)
        v += att_rempl.to_bytes(8, "little", signed=True)
        v += verif.to_bytes(8, "little", signed=True)
        v += f
        for j in range(jn):
            v += jd[j].to_bytes(8, "little") + bytes([jo[j]])
    return bytes(v)


def epreuver(nom: str) -> dict:
    src = ICI / f"bras_c_qwen_{nom}.c"
    pilote = ICI / f"pilote_{nom}.c"
    pilote.write_text(PILOTES[nom], encoding="utf-8")
    exe = ICI / f"epreuve_{nom.replace('-', '_')}"
    r = subprocess.run(["gcc", "-O2", "-o", str(exe), str(src), str(pilote)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return {"contrat": nom, "compilation": "ÉCHEC",
                "detail": r.stderr[:400]}
    rng = random.Random(20261115)
    vec = vecteurs_13(rng) if nom == "loupe-13" else (
        vecteurs_02(rng) if nom == "loupe-02" else b"")
    chemin_vec = ICI / f"vecteurs_{nom}.bin"
    chemin_vec.write_bytes(vec)
    cmd = [str(exe)] + ([str(chemin_vec)] if nom != "loupe-16" else [])
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return {"contrat": nom, "compilation": "OK", "code": r.returncode,
            "console": r.stdout[-2500:]}


if __name__ == "__main__":
    for nom in ("loupe-13", "loupe-02", "loupe-16"):
        res = epreuver(nom)
        print(f"== {nom} ==")
        for k, val in res.items():
            print(f"  {k}: {str(val)[:400]}")
