#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compose_prompt_notation.py — assemble le prompt de la phase notation de
la campagne (l'unité 1, loupe-01 × bras T) : le contrat VERROUILLÉ + les
notes d'auteur (phase spec) + l'oracle (phase oracle) + LES FAITS DU PLAN
(adresses, ABI, réseau des specs, format du brouillon). JAMAIS la notation
scellée — la pièce mesurée naît de cet appel seul."""
import pathlib

UNITE = pathlib.Path(__file__).resolve().parent
CONTRAT = pathlib.Path(UNITE).parent.parent.parent / "loupe" / "I" / "loupe-01-ouvrir.md"

entete = """Tu es l'auteur du domaine Loupe au laboratoire TRIADE : tu écris des blocs en
notation d'assembleur x86-64 À LA MAIN (jamais un compilateur), chaque bloc
contre son contrat de couche I. Tu as déjà lu le contrat (tes notes de
lecture et l'oracle du juge suivent). Écris maintenant LE BROUILLON du bloc
loupe-01 · ouvrir : la notation à étiquettes symboliques que l'outil auteur
résoudra (l'arithmétique d'adresses est à l'outil, la LOGIQUE est à toi).

================================================================================
LE CONTRAT (loupe/I/loupe-01-ouvrir.md, révision 3 — VERROUILLÉ)
================================================================================

"""

faits = """

================================================================================
LES FAITS DU PLAN (loupe/layout.py — la source unique ; l'auteur les connaît
AVANT d'écrire ; les symboles s'utilisent PAR NOM, l'outil auteur résout)
================================================================================

LE SLOT : le bloc loupe-01 vit au slot RVA 0x4080, TAILLE 448 octets — ton
code doit faire AU PLUS 432 octets (le slot se remplit de NOP 0x90, padding
d'au moins 16 octets — multiple de 64).

LE PROFIL : x86-64-win11-pe · ABI msx64.

LES SYMBOLES DU PLAN (par nom, dans le brouillon) :
  CADRE       le cadre de session (.data) — les champs, PAR OFFSET :
              chemin    @+0    (520 o, UTF-16 NUL-terminé)
              taille    @+520  (qword)
              poignée   @+528  (qword ; INVALIDE = -1 = 0xFFFF...FF)
              vue       @+536  (qword)
              curseur   @+544  (qword)
              remplissage @+552 (dword)
              tampon    @+568  (384 o)
  EMPREINTES  le panneau d'empreintes (48 o, .data) — l'argument de loupe-07
  LOUPE02     le bloc fenêtre (l'appel direct : call LOUPE02 ; argument :
              la vue en ecx)
  LOUPE03     le bloc fermeture (la clôture de session, sans argument)
  LOUPE04     le bloc cadre (pose le cadre VIERGE : zéros partout, poignée
              INVALIDE ; sans argument ; rend 0)
  LOUPE07     le bloc panneau (calcule md5+sha256 du fichier ENTIER au
              panneau ; argument : le pointeur du panneau en rcx ; LE VIDE
              AUSSI : son panneau est défini)
  LIBC01      le memcpy hérité (rcx = destination, rdx = source,
              r8d = nombre d'octets)
  IAT_CREATEFILEW, IAT_GETFILESIZEEX, IAT_CLOSEHANDLE, IAT_GETLASTERROR
              les QUATRE feuilles IAT du bloc — l'appel s'écrit :
              call qword ptr [rip + IAT_CREATEFILEW]

L'ABI msx64 (le profil ; l'audit statique du build la vérifie) :
  - les arguments 1 à 4 : rcx, rdx, r8, r9 ;
  - les arguments 5 ET PLUS vivent à [rsp+0x20], [rsp+0x28], [rsp+0x30]…
    JAMAIS au home space [rsp..0x18] ; chaque slot d'argument 5+ doit être
    ÉCRIT dans la branche qui appelle (le défaut de la lignée : trois slots
    au home space, un pointeur fantôme) ;
  - rsp ≡ 0 (mod 16) à CHAQUE appel (compte tes push/pop/sub/add) ;
  - les registres non volatils (rbx, rbp, rdi, rsi, r12 à r15) rendus
    INTACTS (sauve-les si tu les utilises) ;
  - le verdict : rax signé 32 bits (la table des verdicts).

LES FEUILLES (la sémantique des quatre) :
  CreateFileW(lpFileName, dwDesiredAccess, dwShareMode, lpSecurityAttributes,
              dwCreationDisposition, dwFlagsAndAttributes, hTemplateFile)
    7 arguments : rcx = le chemin UTF-16 ; rdx = 0xC0000000
    (GENERIC_READ|GENERIC_WRITE) ; r8 = 1 (FILE_SHARE_READ, offert jamais
    reçu) ; r9 = 0 ; [rsp+0x20] = 3 (OPEN_EXISTING) ; [rsp+0x28] = 0 ;
    [rsp+0x30] = 0. Rend la poignée, ou -1 (INVALID_HANDLE_VALUE) au refus
    (alors GetLastError parle).
  GetFileSizeEx(hFile, lpFileSize) : rcx = la poignée, rdx = le pointeur
    de sortie (qword) ; rend non-zéro au succès.
  CloseHandle(hObject) : rcx = la poignée ; rend non-zéro au succès.
  GetLastError() : aucun argument ; rend le code (2 = FILE_NOT_FOUND,
    3 = PATH_NOT_FOUND, 32 = SHARING_VIOLATION, 5 = ACCESS_DENIED).

LE RÉSEAU DES SPECS (la liste FERMÉE des appels directs attendus — le
build REFUSE tout appel hors réseau, et REFUSE un appelé manquant) :
  LOUPE04, LOUPE02, LOUPE07, LOUPE03, LIBC01 — pas un de plus, pas un de
  moins. Les quatre feuilles IAT ci-dessus — pas une de plus.

L'ORDRE DU GESTE (le contrat le dit, le réseau l'exige) :
  1. E4 D'ABORD : la poignée du cadre (@+528) lue — si ≠ -1, la session
     est déjà ouverte : rax = -5, RIEN TOUCHÉ (l'ancien cadre demeure
     INTACT — le test précède TOUT geste, même loupe-04) ;
  2. LOUPE04 : le cadre vierge posé (les zéros, la poignée INVALIDE) ;
  3. CreateFileW : au refus (-1), GetLastError → la table (2 ou 3 → -2 ;
     32 → -7 ; le reste → -6), la barre le nomme, RETOUR ;
  4. la poignée au cadre (+528), GetFileSizeEx → la taille au cadre (+520) ;
  5. Q2 LA BORNE : taille > 0x80000000 (comparaison NON signée, la taille
     est un qword) → CloseHandle (la poignée JAMAIS pendante), LOUPE04
     (le cadre re-vierge : la session échouée ne laisse RIEN), rax = -3 ;
  6. LA MESURE DU CHEMIN : les caractères UTF-16 comptés jusqu'au NUL ;
     si 260 caractères SANS NUL → CloseHandle, LOUPE04, rax = -5 (jamais
     un débordement) ;
  7. LA COPIE : le chemin copié au cadre (+0) PAR LIBC01 (jamais octet
     par octet réécrit) — n = (longueur + 1) × 2 octets, le NUL compris ;
     la vue = 0, le curseur = 0 (loupe-04 les a posés) ;
  8. Q4 LA SESSION NÉE ENTIÈRE : si taille > 0, LOUPE02 (la fenêtre à la
     vue 0 — argument ecx = 0) ; puis LOUPE07 (le panneau — rcx = le
     pointeur EMPREINTES, posé par lea rcx, [rip + EMPREINTES]) ; le vide
     SAUTE la fenêtre mais PAS le panneau ;
  9. LE REFUS D'UN APPELÉ (loupe-02 ou loupe-07 rend un eax négatif) :
     LOUPE03 (la session se clôt — la poignée rendue, le cadre re-vierge),
     le verdict de l'appelé remonte TEL QUEL dans rax ;
  10. le succès : rax = 0.

================================================================================
LE FORMAT DU BROUILLON (ce que l'outil auteur accepte — rien d'autre)
================================================================================

  - les commentaires : une ligne qui commence par « ; »
  - les étiquettes locales : « .nom: » SEULE sur sa ligne
  - les sauts : « jmp .nom », « je .nom », « jne .nom », « jbe .nom »…
  - les appels directs : « call LOUPE04 » (le NOM du symbole)
  - les appels IAT : « call qword ptr [rip + IAT_CREATEFILEW] »
  - les données : « lea rbx, [rip + CADRE] » — toute instruction peut
    porter « [rip + SYMBOLE] » (jamais « [rip - SYMBOLE] »)
  - une instruction par ligne, syntaxe Intel (mov, movzx, movsxd, lea,
    cmp, test, jcc, call, push, pop, sub, add, xor, shl, inc, nop, ret…)
  - les valeurs négatives immédiates : « push -3 » puis « pop rax » est la
    manière de la lignée pour poser un verdict négatif dans rax (mov
    eax, -3 convient aussi)

================================================================================
TON TRAVAIL : écris LE BROUILLON — les lignes « ; » d'en-tête (la spec, tes
choix, l'ordre du geste — tes mots d'auteur), puis les instructions, une par
ligne. Le code doit faire AU PLUS 432 octets (une centaine d'instructions
suffisent largement — sois économe : pas de sous-routine, le bloc est droit).

Réponds par le BROUILLON SEUL : aucun texte avant, aucun texte après,
AUCUN bloc de code markdown (des lignes « ; » puis des instructions, rien
d'autre).
"""

spec = pathlib.Path(UNITE, "spec-lue.txt").read_text(encoding="utf-8")
oracle = pathlib.Path(UNITE, "oracle-depuis-I.txt").read_text(encoding="utf-8")
contrat = CONTRAT.read_text(encoding="utf-8")

notes = ("\n\n" + "=" * 80 + "\n"
         "TES NOTES DE LECTURE (la phase spec — tes propres notes d'auteur)\n"
         + "=" * 80 + "\n\n" + spec
         + "\n\n" + "=" * 80 + "\n"
         + "L'ORACLE DU JUGE (la phase oracle — écrit-avant-code ; ta\n"
           "notation devra tenir CES attentes exactes)\n"
         + "=" * 80 + "\n\n" + oracle)

sortie = pathlib.Path(UNITE, "prompts", "notation.txt")
sortie.write_text(entete + contrat + notes + faits, encoding="utf-8")
print(f"[prompt] {sortie} : {sortie.stat().st_size} o "
      f"(contrat {len(contrat)} + notes {len(spec)} + oracle {len(oracle)} "
      f"+ faits {len(faits)})")
