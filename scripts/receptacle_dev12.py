#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Le réceptacle preuves-loupe dev.12 — la suite du texte dev.11.

LA TÊTE raconte LE DIXIÈME RUN : la vitrine VÉCUE la première fois
(0 et 0) T0→T7 tout vert pour la troisième fois — mais la cascade 205
morte à son premier geste ([FREE-SANS-TYPE]) et LA LIAISON jamais
courue ; la retouche dev.12 du kit seul. LE GESTE et LE CRITÈRE
portés à loupe-kit-12/.
"""
import hashlib

SRC = "/home/z/my-project/build-dev11/LISEZMOI-preuves-NEUF.txt"
DST = "/home/z/my-project/build-dev12/LISEZMOI-preuves-NEUF.txt"

assert hashlib.md5(open(SRC, "rb").read()).hexdigest().startswith("cb9dab10"), \
    "la base n'est pas le réceptacle dev.11"
rz = open(SRC, encoding="utf-8").read()


def remplace(ancien, nouveau, combien=1):
    global rz
    n = rz.count(ancien)
    assert n == combien, f"ancre {n}x (attendu {combien}) : {ancien[:70]!r}"
    rz = rz.replace(ancien, nouveau)


# la tête — le récit du dixième run + la retouche dev.12
remplace("""(LE RUN DE LOUPE, LE GRANDE NATURE : la première application née de
TRIADE chez son utilisateur ; l'artefact attendu 0.1.0-dev.8, sha256
054de960c31425d0… — LA RETOUCHÉE DE L'ENTRÉE 214, INTACTE
À L'ENTRÉE 215 (la vague dev.11 est UNE RETOUCHE DU KIT
SEUL : la pièce n'a pas bougé d'un octet, la carte demeure
génération 16) : le neuvième run
tint T0→T7 TOUT VERT pour la seconde fois, puis LA SIXIÈME MORT DE LA
VITRINE FUT NOMMÉE — par le système [le journal d'événements du témoin
portant : BEX64, module « unknown », exécution sur mémoire non
exécutable] puis par le labo [OFT-QWORD : les QUATRE tableaux
OriginalFirstThunk écrits à pas de qword — le chargeur lisait OFT[1] =
0, croyait la liste finie, résolvait UNE fonction par DLL, laissait
les 33 autres slots à leur valeur fichier — le second appel de
l'entrée sautait à l'adresse du NOM : 0xC0000005, module unknown] ; LA
RETOUCHE : les OFT compactés au pas DWORD [10 · 18 · 6 · 3], 89 octets
en tout, le .text/.text2/.data octet-identiques, les adresses scellées
INTACTES ; la carte génération 16 — la régénération est dette au labo,
l'Entrée 211 ; le kit dev.11 ([RET-NU] retouché avant le
run — la vague dev.10 ne courut jamais) : LE CONTRÔLE D54 ÉTENDU [les QUATRE OFT
marchés au pas DWORD du chargeur — chaque entrée == le préremplissage
de son slot], LA SONDE 205 RÉPARÉE DE SON PROPRE NETTOYAGE
[FreeLibrary avant suppression — le PermissionError du run 9 ne
passera plus, chaque essai dans son try], ET LA NOUVELLE SONDE DE
LIAISON [une copie chargée SANS DONT_RESOLVE, l'entrée neutralisée
de SIX OCTETS mov eax, 1 ; ret — [RET-NU] NOMMÉ AVANT LE RUN
(l'Entrée 215 : un ret nu eût rendu le verdict ATTACH FAUX au
chargeur qui appelle l'entrée en sémantique DllMain ET LIT SON
RETOUR — REFUS FAUX, liaison perdue), les 37 slots RELUS : le
VRAI chargeur doit y avoir posé les ADRESSES DES FONCTIONS — la
liaison vécue au témoin AVANT MÊME LA FENÊTRE] ; la balise `loupe 0.1.0` se scellera sur le vert
recoupé)""",
"""(LE RUN DE LOUPE, LE GRANDE NATURE : la première application née de
TRIADE chez son utilisateur ; l'artefact attendu 0.1.0-dev.8, sha256
054de960c31425d0… — LA RETOUCHÉE DE L'ENTRÉE 214, INTACTE
DEPUIS (la pièce n'a pas bougé d'un octet, la carte demeure
génération 16) : LE DIXIÈME RUN (kit dev.11) TINT T0→T7 TOUT VERT
POUR LA TROISIÈME FOIS ET VÉCUT LA VITRINE LA PREMIÈRE FOIS — 0 ET 0,
LES DEUX FENÊTRES, AUCUN WER : L'APPLICATION NÉE DE TRIADE A VÉCU CHEZ
SON UTILISATEUR — MAIS LA CASCADE 205 MOURUT À SON PREMIER GESTE :
[FREE-SANS-TYPE] — le FreeLibrary de la leçon du run 9 fut appelé SANS
argtypes avec le HMODULE 64 bits du restype c_void_p : ctypes
convertit l'argument nu en int 32 bits — ArgumentError('argument 1:
OverflowError: int too long to convert') — et l'ArgumentError n'est
PAS un OSError : l'essai isolé ne tenait que pour OSError, LA LIAISON
NE COURUT JAMAIS ; la ligne d'échec NOMMA le défaut, LA PIÈCE EST
ACQUITTÉE (T7 la relut inchangée ; la vitrine vivante prouve la
liaison mieux que toute sonde — la fenêtre n'eût pas vécu d'un import
non résolu) ; LA RETOUCHE dev.12, DU KIT SEUL : FreeLibrary.argtypes =
[c_void_p] posé au T0 (le POINTEUR passe, aux DEUX sondes d'un seul
geste), l'essai de la cascade 205 élargi à TOUTE classe d'exception,
la sonde de liaison blindée de même — AUCUNE exception de sonde ne
tue le run ; la balise `loupe 0.1.0` se scellera sur le vert ENTIER
recoupé : le scénario T0 → S0 → LA LIAISON ET la vitrine vivante)""")

# le témoin vitrine — la vitrine a déjà vécu
remplace("""D'ÉVÉNEMENTS [4/4] — **0 ET 0 SONT ATTENDUS : la
                       vitrine dev.8 est née pour VIVRE** (six morts
                       déjà — la sixième A NOMMÉ SON DÉFAUT [OFT-QWORD]
                       et la retouche est portée : la liaison sera vécue
                       par la sonde AVANT la fenêtre ; si la septième
                       vient, le journal la nommera de la même façon) ;""",
"""D'ÉVÉNEMENTS [4/4] — **0 ET 0 SONT ATTENDUS : la
                       vitrine dev.8 A DÉJÀ VÉCU AU DIXIÈME RUN** (0 et
                       0, la première fois après six morts — le
                       onzième run la reverra vivre ; si une mort
                       vient, le journal la nommera de la même façon) ;""")

# le témoin complet — la cascade 205 attendue ENTIÈRE cette fois
remplace("""contrat c_int64, la clôture), LA CASCADE 205
                       ENFIN JOUÉE [P0..P4 — FreeLibrary avant
                       suppression : elle vivra enfin] ET LA LIAISON
                       [sonde-214 : les 37 slots relus chargés — le
                       VRAI chargeur a posé les fonctions] ;""",
"""contrat c_int64, la clôture), LA CASCADE 205
                       JOUÉE ENTIÈRE [P0..P4 — le FreeLibrary en
                       POINTEUR, l'essai isolé pour TOUTE classe :
                       elle vivra enfin, la leçon du run 10] ET LA
                       LIAISON [sonde-214 : les 37 slots relus chargés —
                       le VRAI chargeur a posé les fonctions — JAMAIS
                       courue à ce jour, le run 10 mourut avant] ;""")

# le geste — le dossier neuf dev.12
remplace("""LE GESTE (D99) : dézippez kit-loupe.zip dans un dossier NEUF — si le
dossier d'un run dev.1 à dev.10 existe encore, NE LE RÉUTILISEZ PAS
(loupe-kit-10/ par exemple —
la vague dev.10 retouchée AVANT le run — un dossier neuf par run ; le dossier
loupe-kit-11/ du coffre Drive EST le kit lui-même, prêt à courir).""",
"""LE GESTE (D99) : dézippez kit-loupe.zip dans un dossier NEUF — si le
dossier d'un run dev.1 à dev.11 existe encore, NE LE RÉUTILISEZ PAS
(loupe-kit-11/ par exemple — la vague courue au run 10) — un dossier
neuf par run ; le dossier loupe-kit-12/ du coffre Drive EST le kit
lui-même, prêt à courir.""")

# le verdict rouge — dix runs, dix leçons, le septième défaut nommé
remplace("""Un verdict ROUGE se renvoie TEL QUEL : la ligne d'échec NOMME le
défaut (chaque défaut a été nommé, chaque défaut a reçu sa retouche —
neuf runs, neuf leçons ; la sixième mort a nommé [OFT-QWORD] : la
septième, si elle vient, sera nommée PAR LE JOURNAL D'ÉVÉNEMENTS ;
le défaut [RET-NU] fut nommé AVANT le dixième run — la liaison ne
peut plus être perdue de fausse cause).""",
"""Un verdict ROUGE se renvoie TEL QUEL : la ligne d'échec NOMME le
défaut (chaque défaut a été nommé, chaque défaut a reçu sa retouche —
dix runs, dix leçons ; la sixième mort a nommé [OFT-QWORD] ; le
défaut [RET-NU] fut nommé AVANT le dixième run ; le dixième nomma
[FREE-SANS-TYPE] — LE DÉFAUT DU KIT, LA PIÈCE ACQUITTÉE, la vitrine
VÉCUE quand même : la dette restante est le scénario ENTIER).""")

open(DST, "w", encoding="utf-8", newline="\n").write(rz)
print(f"le réceptacle dev.12 : {len(rz)} octets, md5 "
      f"{hashlib.md5(open(DST, 'rb').read()).hexdigest()[:8]}…")
assert "dev.12" in rz and "[FREE-SANS-TYPE]" in rz
assert "loupe-kit-12/" in rz
# « kit dev.11 » demeure légitimement dans le récit du dixième run (la tête) ;
# le geste et les attentes portent dev.12
assert "LE GESTE (D99)" in rz and rz.count("kit dev.11") == 1
