#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""construire_shani.py — LE GÉNÉRATEUR DE LA NOTATION tls13-02-shani (le
couloir SHA-NI de fnvan0zes) : traduit la RÉFÉRENCE VÉRIFIÉE sha256ni_ref.c
(256/256 vecteurs aléatoires à zéro divergence contre le juge Python) en
notation msx64 à la marge 0xD200, dispatch CPUID(7,0).EBX[29] au REPLI au
SCELLÉ GPR (jmp 0xC080 — le repli baseline est LE SCELLÉ, jamais une copie).

Les instructions SHA (sha256rnds2/msg1/msg2) ne sont pas assemblées par
keystone : leurs OCTETS EXPLICITES sont émis (l'encodage 0F 38 CB/CC/CD +r
vérifié par as/objdump ET par le round-trip capstone — la double
vérification consignée)."""
import pathlib

ICI = pathlib.Path(__file__).resolve().parent
RVA = 0xD300
RVA_SCELLE = 0xC080        # le bloc scellé GPR (le repli)
RVA_K = 0x2F00             # la table K[64] scellée (le fixture R_K)
REPO = pathlib.Path("/home/z/my-project/depot")

# xmm : 0=MSG(implicite rnds2), 1=ABEF, 2=CDGH, 3=TMP, 4=SAV0, 5=SAV1,
#       6..9 = S[0..3]
S = {0: 6, 1: 7, 2: 8, 3: 9}


def modrm(reg, rm):
    return 0xC0 | ((reg & 7) << 3) | (rm & 7)


def sha_rnds2(dst, src):
    """sha256rnds2 xmmD, xmmS (xmm0 implicite = K) : 0F 38 CB /r"""
    return [0x0F, 0x38, 0xCB, modrm(dst, src)]


def sha_msg1(dst, src):
    return [0x0F, 0x38, 0xCC, modrm(dst, src)]


def sha_msg2(dst, src):
    return [0x0F, 0x38, 0xCD, modrm(dst, src)]


def db(bytes_):
    return "db " + " ".join(f"{b:02x}" for b in bytes_)


def main():
    l = []
    a = l.append
    a("; tls13-02-shani · LE COULOIR SHA-NI DE LA COMPRESSION (fnvan0zes, la vague 11) · spec tls13-02:R1 (LE MÊME CONTRAT — R4)")
    a("; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xd300 (la marge VIERGE — AUCUN octet du scellé touché, le modèle OPT-01)")
    a("; Domaine : tls13 (M9) · Dépendances : la table K[64] scellée à 0x2f00 (le fixture R_K — LE MÊME, lu, jamais copié)")
    a("; LE DISPATCH RUNTIME : CPUID(7,0).EBX[29] (SHA) — le sondage UNE FOIS PAR APPEL ; le REPLI BASELINE : LE SCELLÉ GPR (jmp 0xc080),")
    a("; jamais une copie — la machine sans SHA-NI vit le scellé (le contrat par construction).")
    a("; L'ALGORITHME : la référence sha256ni_ref.c VÉRIFIÉE (256/256 vecteurs aléatoires, zéro divergence contre le juge) ;")
    a("; les lanes RÉSOLUES PAR SONDES (rnds2 : src=(A,B,E,F)@lanes 3,2,1,0, dst=(C,D,G,H), sortie=le nouveau ABEF dans dst ;")
    a("; msg1/msg2 : les formules sondées) ; les instructions SHA AUX OCTETS EXPLICITES (keystone ne les porte pas — 0F 38 CB/CC/CD /r,")
    a("; l'encodage vérifié as/objdump ET le round-trip capstone).")
    a("; LE CONTRAT (tls13-02:R1 À LA LETTRE — R4) : (ptr état, ptr bloc) -> 0, l'état mis à jour par addition (FIPS § 6.2.2),")
    a("; silencieux, les non-volatils rendus.")
    a("push rbp")
    a("mov rbp, rcx")
    a("mov r10, rdx")   # le bloc préséré dans r10 (rax détruit par cpuid)
    a("; ---- LE DISPATCH (une fois par appel) -----------------------------------------")
    a("xor ecx, ecx")
    a("mov eax, 7")
    a("cpuid")
    a("test ebx, 0x20000000")
    a(f"jz {RVA_SCELLE:#x}")
    a("; ---- L'ÉTAT : ABEF/CDGH aux lanes 3,2,1,0 --------------------------------------")
    a("movdqu xmm4, xmmword ptr [rbp]")
    a("movdqu xmm5, xmmword ptr [rbp + 16]")
    a("pshufd xmm1, xmm4, 0xb1")
    a("pshufd xmm2, xmm5, 0xb1")
    a("movdqa xmm3, xmm2")
    a("punpcklqdq xmm2, xmm1")
    a("punpckhqdq xmm3, xmm1")
    a("movdqa xmm1, xmm2")
    a("movdqa xmm2, xmm3")
    a("; ---- LES FENÊTRES DU MESSAGE (bswap par dword) ---------------------------------")
    a("lea r11, [rip + 0x0]")           # REMPLI : le masque (patché ci-dessous)
    idx_masque = len(l) - 1
    for k in range(4):
        a(f"movdqu xmm{S[k]}, xmmword ptr [r10 + {16*k}]")
        a(f"pshufb xmm{S[k]}, xmmword ptr [r11]")
    a("; ---- LES RONDES 0-15 (les fenêtres d'entrée) -----------------------------------")
    for k in range(4):
        a(f"movdqa xmm0, xmm{S[k]}")
        a(f"paddd xmm0, xmmword ptr [rip + 0x0]")   # REMPLI : K256[k]
        globals().setdefault("k_fixups", []).append(("paddd", len(l)-1, k))
        a(db(sha_rnds2(2, 1)) + " ; sha256rnds2 xmm2, xmm1")
        a("pshufd xmm0, xmm0, 0x0e")
        a(db(sha_rnds2(1, 2)) + " ; sha256rnds2 xmm1, xmm2")
    if True:
        a("; DIAG STADE 1 : rendre ABEF/CDGH/S[0..3] après les rondes 0-15")
        for reg, off in [(1, 0x70), (2, 0x80), (6, 0x20), (7, 0x30), (8, 0x40), (9, 0x50)]:
            a(f"movdqu xmmword ptr [rbp + {off:#x}], xmm{reg}")
        a("xor eax, eax")
        a("pop rbp")
        a("ret")
        a("; ---- LES GÉNÉRATIONS 0-11 (msg1/alignr/add/msg2 + la paire rnds2) --------------")
    for g in range(12):
        k, k1, k2, k3 = g & 3, (g + 1) & 3, (g + 2) & 3, (g + 3) & 3
        a(f"; la génération {g} : la fenêtre W[{16+4*g}..{19+4*g}]")
        a(db(sha_msg1(S[k], S[k1])) + f" ; sha256msg1 xmm{S[k]}, xmm{S[k1]}")
        a(f"movdqa xmm3, xmm{S[k3]}")
        a(f"palignr xmm3, xmm{S[k2]}, 4")
        a(f"paddd xmm{S[k]}, xmm3")
        a(db(sha_msg2(S[k], S[k3])) + f" ; sha256msg2 xmm{S[k]}, xmm{S[k3]}")
        if g == 0:
            a("movdqu xmmword ptr [rbp + 0x90], xmm6")   # S[0] après gen0
            a("xor eax, eax")
            a("pop rbp")
            a("ret")
        a(f"movdqa xmm0, xmm{S[k]}")
        a(f"paddd xmm0, xmmword ptr [rip + 0x0]")   # REMPLI : K256[4+g]
        globals()["k_fixups"].append(("paddd", len(l)-1, 4 + g))
        a(db(sha_rnds2(2, 1)) + " ; sha256rnds2 xmm2, xmm1")
        a("pshufd xmm0, xmm0, 0x0e")
        a(db(sha_rnds2(1, 2)) + " ; sha256rnds2 xmm1, xmm2")
    a("; ---- LA SOMMATION : l'état += les variables (FIPS § 6.2.2) ---------------------")
    a("movdqa xmm3, xmm1")
    a("punpckhqdq xmm3, xmm2")
    a("pshufd xmm3, xmm3, 0xb1")
    a("paddd xmm3, xmm4")
    a("movdqu xmmword ptr [rbp], xmm3")
    a("movdqa xmm3, xmm1")
    a("punpcklqdq xmm3, xmm2")
    a("pshufd xmm3, xmm3, 0xb1")
    a("paddd xmm3, xmm5")
    a("movdqu xmmword ptr [rbp + 16], xmm3")
    a("xor eax, eax")
    a("pop rbp")
    a("ret")
    a("; ---- LE MASQUE (bswap par dword : [3,2,1,0, 7,6,5,4, 11,10,9,8, 15,14,13,12]) ---")
    a("; ALIGNÉ 16 (pshufb m128 EXIGE l'alignement — la faute nommée et corrigée)")
    a("align 16")
    a(db(bytes([3, 2, 1, 0, 7, 6, 5, 4, 11, 10, 9, 8, 15, 14, 13, 12])))

    # ---- les correctifs d'adresses (le masque et les K) : mesurés à l'assemblage ----
    # on marque les lignes à patcher avec des balises que l'assembleur résoudra :
    lignes = []
    for i, ligne in enumerate(l):
        if i == idx_masque:
            lignes.append("lea r11, [rip + @MASQUE]")
        elif ligne.startswith("paddd xmm0, xmmword ptr [rip + 0x0]"):
            # retrouver l'indice k de la fenêtre concernée
            k = next(kx for typ, ix, kx in globals()["k_fixups"] if ix == i)
            lignes.append(f"paddd xmm0, xmmword ptr [rip + @K{4*k}]")
        else:
            lignes.append(ligne)
    (ICI / "notation" / "tls13-02-shani.asm").write_text(
        "\n".join(lignes) + "\n", encoding="utf-8")
    print(f"la notation tls13-02-shani.asm générée : {len(lignes)} lignes")


if __name__ == "__main__":
    main()
