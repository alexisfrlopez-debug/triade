#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compose_prompt_correctif7.py — le correctif-7 de la phase source-c
(bras C) : l'audit binaire du désassemblage nomma DEUX appels memset —
les boucles de bourrage zéro de md5_final et sha256_final que gcc -O2
reconnut comme l'idiome memset (l'appel au CRT JAMAIS résolu sous
DONT_RESOLVE : le run terrain cracherait à la finalisation). La parade
honnête du C : les écritures VOLATILE — le reconnaisseur d'idiomes ne
fusionne jamais des magasins volatils."""
import pathlib

UNITE = pathlib.Path(__file__).resolve().parent

prompt = """Tu es le même auteur du domaine Loupe au laboratoire TRIADE — le bras C de
la campagne D204. L'épreuve du contrat entier est PASSÉE au labo : 17
VERT, 0 ROUGE (les quatre témoins champ à champ, les rejets d'OS, la
borne 2 Gio, la session double l'ancien cadre INTACT, le chemin trop
long). MAIS l'AUDIT BINAIRE du désassemblage nomma DEUX APPELS MEMSET :
dans md5_final et sha256_final, les boucles de bourrage zéro
« for (int i = c->rempli; i < 56; ++i) c->tampon[i] = 0; » — gcc -O2 les
reconnut comme l'IDIOME memset et émet « call <memset> » — or la pièce
vit sous LoadLibraryEx DONT_RESOLVE au terrain : le CRT n'est JAMAIS
initialisé, l'appel sauterait dans un import non résolu — le run
cracherait à la première finalisation.

LA PARADE HONNÊTE DU C : les écritures VOLATILE. Le reconnaisseur
d'idiomes de gcc ne fusionne jamais des magasins volatils — chaque
écriture demeure un magasin explicite. C'est la technique standard du
code embarqué contre les optimisations de bibliothèque.

TON TRAVAIL (le correctif-7) — LE FORMAT PATCH
================================================================================
Réponds UNIQUEMENT par les remplacements, au format EXACT :

###REMPLACEMENTS
AVANT=<la ligne fautive, copiée au caractère près>
APRÈS=<la ligne corrigée>
###FIN REMPLACEMENTS

Les QUATRE remplacements attendus (les quatre boucles de bourrage zéro,
deux par finalisation — md5_final puis sha256_final) :
1. AVANT=        for (int i = c->rempli; i < 64; ++i) c->tampon[i] = 0;
   APRÈS=        for (int i = c->rempli; i < 64; ++i)
                   *(volatile uint8_t*)&c->tampon[i] = 0;   /* jamais un
                   appel memset — le CRT ne vit pas sous DONT_RESOLVE */
2. AVANT=    for (int i = c->rempli; i < 56; ++i) c->tampon[i] = 0;
   APRÈS=    for (int i = c->rempli; i < 56; ++i)
                 *(volatile uint8_t*)&c->tampon[i] = 0;  /* idem — jamais
                 un appel memset */
(les deux remplacements ci-dessus s'appliquent AUX DEUX finalisations :
md5_final ET sha256_final portent chacune les mêmes deux boucles —
quatre remplacements au total, dans l'ordre du fichier.)

Aucun texte avant ###REMPLACEMENTS, aucun texte après ###FIN
REMPLACEMENTS.
"""

(UNITE / "prompts" / "correctif-7.txt").write_text(prompt, encoding="utf-8")
print(f"[composé] prompts/correctif-7.txt : {len(prompt.encode())} o")
