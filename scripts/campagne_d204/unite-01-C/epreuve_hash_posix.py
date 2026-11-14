#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""epreuve_hash_posix.py — L'ÉPREUVE D122 DE LA COUCHE DE HACHAGE du bras
C (loupe-01 × C, campagne D204) : les fonctions md5_*/sha256_* livrées
par le correctif-3, compilées au POSIX du labo (gcc -O2 natif — le même
compilateur, la cible seule change), confrontées au juge indépendant
hashlib sur le corpus des frontières du rembourrage (0..128, 384,
196 609 — les témoins) et des octets pseudo-aléatoires déterministes."""
import hashlib
import pathlib
import subprocess
import sys

UNITE = pathlib.Path(__file__).resolve().parent
SOURCE = UNITE / "source" / "loupe-01-c.c"
ATELIER = UNITE / "epreuves"

# le harnais : la couche de hachage de la pièce, incluse telle quelle
HARNESS = r"""
#include <stdio.h>
#include <stdint.h>
#include <string.h>
/* la pièce incluse jusqu'à loupe_01_ouvrir (la couche Win32 exclue) */
"""

def main() -> int:
    src = SOURCE.read_text(encoding="utf-8")
    coupe = src.index("long long loupe_01_ouvrir")
    noyau = src[:coupe]
    # retire les inclusions Windows et les définitions Win32-dures
    noyau = noyau.replace("#include <windows.h>\n", "")
    noyau = noyau.replace("#include <stdint.h>\n", "")
    noyau = noyau.replace("char cadre[960];\n", "")
    noyau = noyau.replace("char panneau[48];\n", "")
    noyau = noyau.replace("static HANDLE g_session_handle = INVALID_HANDLE_VALUE;\n", "")

    testeur = """
#include <stdio.h>
#include <stdint.h>
#include <string.h>
typedef unsigned long long QWORD_;
typedef unsigned long DWORD_;
#define LARGE_INTEGER union { QWORD_ q; }
""" + noyau + """
char panneau[48];

int main(void) {
    /* le corpus : les frontières du rembourrage + les tailles des témoins */
    static const int tailles[] = {0, 1, 2, 31, 32, 33, 54, 55, 56, 57, 63,
                                  64, 65, 111, 112, 119, 120, 127, 128,
                                  129, 255, 256, 383, 384, 385, 511, 512,
                                  4096, 4097, 65536, 131072, 196609};
    static unsigned char donnees[196609];
    for (size_t i = 0; i < sizeof donnees; i++)
        donnees[i] = (unsigned char)(i * 131 + (i >> 7) * 17 + i / 251);
    for (size_t t = 0; t < sizeof tailles / sizeof tailles[0]; t++) {
        int n = tailles[t];
        ctx_md5 m5 = {{0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476}, {0}, 0, 0};
        ctx_sha256 s2 = {{0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,
                          0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19}, {0}, 0, 0};
        /* l'absorption en morceaux IRREGULIERS (7, 1, 4090, 13...) —
           l'incrémentalité éprouvée, pas seulement les blocs entiers */
        size_t reste = (size_t)n, pris = 0;
        static const size_t pas[] = {7, 1, 4090, 13, 64, 3, 5000, 2};
        size_t k = 0;
        while (reste > 0) {
            size_t a = pas[k++ % (sizeof pas / sizeof pas[0])];
            if (a > reste) a = reste;
            md5_absorbe(&m5, donnees + pris, (uint32_t)a);
            sha256_absorbe(&s2, donnees + pris, (uint32_t)a);
            pris += a; reste -= a;
        }
        md5_final(&m5, panneau);
        sha256_final(&s2, panneau + 16);
        printf("%d ", n);
        for (int i = 0; i < 48; i++) printf("%02x", (unsigned char)panneau[i]);
        printf("\\n");
    }
    return 0;
}
"""
    ATELIER.mkdir(exist_ok=True)
    chemin_c = ATELIER / "testeur_hash.c"
    chemin_c.write_text(testeur, encoding="utf-8")
    binaire = ATELIER / "testeur_hash"
    r = subprocess.run(["gcc", "-O2", "-o", str(binaire), str(chemin_c)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("[ROUGE] la compilation du testeur échoue :")
        print(r.stderr[:2000])
        return 1
    print("[VERT] le testeur compile (gcc -O2, le POSIX du labo)")

    r = subprocess.run([str(binaire)], capture_output=True, text=True, timeout=120)
    vert, rouge = 0, 0
    for ligne in r.stdout.strip().splitlines():
        n_s, hexa = ligne.split(" ", 1)
        n = int(n_s)
        attendu = (hashlib.md5(bytes((i * 131 + (i >> 7) * 17 + i // 251) & 255
                                     for i in range(n))).hexdigest()
                   + hashlib.sha256(bytes((i * 131 + (i >> 7) * 17 + i // 251) & 255
                                          for i in range(n))).hexdigest())
        if hexa == attendu:
            vert += 1
        else:
            rouge += 1
            print(f"  ROUGE {n} o : obtenu {hexa[:32]}… != attendu {attendu[:32]}…")
    print(f"[éprouvées] {vert} VERT, {rouge} ROUGE "
          f"(les frontières du rembourrage, l'incrémentalité irrégulière)")
    return 0 if rouge == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
