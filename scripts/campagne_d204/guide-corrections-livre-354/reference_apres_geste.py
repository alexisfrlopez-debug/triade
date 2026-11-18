#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Référence-après-geste du guide-354 — LES CORRECTIONS DU LIVRE.

Construit, à partir des QUATRE registres tels que déposés au coffre /test
(état de la sonde : atelier re-déposé le 18/11 16:04:15 locale, après le run
v3 de l'unité 04), l'état attendu APRÈS les gestes prescrits :

  livraisons.csv :
    ① le bloc T-loupe-16 (2 lignes : la ligne du GUI it1 + la ligne de la
       main it2) DEVIENT TROIS lignes chronologiques :
         it1 ROUGE  — le refus v1 du 18/11 12:12 (RVA-HORS-SECTIONS, code 2)
         it2 ROUGE  — la ligne de la main (le crash v2 du 18/11 14:09) —
                      DEMEURE byte-byte (la 4e colonne « 1 », écart nommé
                      R11-② de la 352, jamais corrigé)
         it3 ROUGE  — la ligne du GUI RENOMMÉE (le run v3 du 18/11 15:59 —
                      la 4e colonne 1 → 3, la chirurgie ① de la 352)
    ② la ligne d'attribution posée à la suite :
         C-loupe-16-attr-it1 VERT — le run d'attribution du 18/11 18:08
         (14 VERT 0 ROUGE, le verdict RECOPIÉ du témoin/de la console)
  defauts.csv :
    ③ les TROIS DÉFAUTS du bloc de l'unité 04 (jamais nommés — R11-④ de la
       352) : it1 guichet-descripteur-quatre-champs (la 350),
       it2 liaison-memmove-deux-arguments (la 351),
       it3 les-metriques-ecran-jamais-posees-par-le-juge (la 352).
  carnet_temps_humain.csv : AUCUNE référence — les lignes M3 sont à la main
  (D189/D99, la même frontière que le témoin).
  journal-ouverture.txt : INCHANGÉ.

Calcule les sha256 attendus (la vérification au terrain : certutil -hashfile).
"""
import hashlib
import os

BAC = "/home/z/my-project/scripts/campagne_d204/sonde-dernier-run"
REF = "/home/z/my-project/scripts/campagne_d204/guide-corrections-livre-354/reference-apres-geste"
os.makedirs(REF, exist_ok=True)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def lire(nom: str) -> bytes:
    with open(os.path.join(BAC, nom), "rb") as f:
        return f.read()


def ecrire(nom: str, data: bytes) -> None:
    with open(os.path.join(REF, nom), "wb") as f:
        f.write(data)


# ---- livraisons.csv ---------------------------------------------------------

liv = lire("livraisons.csv").decode("utf-8")
assert liv.endswith("\n") and "\r" not in liv

V1_REFUS = "T-loupe-16-d210-it1,T,loupe-16-d210,1,2026-11-18,2026-11-18,ROUGE,en attente\n"
LIGNE_MAIN_IT2 = "T-loupe-16-d210-it2,T,loupe-16-d210,1,2026-11-18,2026-11-18,ROUGE,en attente\n"  # demeure
V3_RENOMMEE = "T-loupe-16-d210-it3,T,loupe-16-d210,3,2026-11-18,2026-11-18,ROUGE,en attente\n"
ATTRIBUTION = "C-loupe-16-attr-it1,C,loupe-16-attr,1,2026-11-18,2026-11-18,VERT,en attente\n"

# le bloc actuel des DEUX lignes T-loupe-16 (la ligne du GUI it1 puis celle de la main it2)
bloc_avant = ("T-loupe-16-d210-it1,T,loupe-16-d210,1,2026-11-18,2026-11-18,ROUGE,en attente\n"
              + LIGNE_MAIN_IT2)
assert liv.count(bloc_avant) == 1, "le bloc T-loupe-16 attendu n'est pas trouvé tel quel"
bloc_apres = V1_REFUS + LIGNE_MAIN_IT2 + V3_RENOMMEE
liv_apres = liv.replace(bloc_avant, bloc_apres) + ATTRIBUTION

# contrôles : la ligne du GUI renommée n'existe plus sous it1 ; 29 lignes de campagne
# (les 27 reçues : 22 D204 + loupe-02/loupe-08/loupe-13 VERT + it1 GUI + it2 main ;
#  le bloc 2 → 3 lignes et la ligne d'attribution : 27 + 2 = 29)
corps = [l for l in liv_apres.split("\n") if l and not l.startswith("#")]
assert corps[0] == "livraison,bras,tache,numero_iteration,date_kit,date_run,verdict,recoup"
lignes_campagne = corps[1:]
assert len(lignes_campagne) == 29, len(lignes_campagne)
assert lignes_campagne[-4:] == [
    "T-loupe-16-d210-it1,T,loupe-16-d210,1,2026-11-18,2026-11-18,ROUGE,en attente",
    "T-loupe-16-d210-it2,T,loupe-16-d210,1,2026-11-18,2026-11-18,ROUGE,en attente",
    "T-loupe-16-d210-it3,T,loupe-16-d210,3,2026-11-18,2026-11-18,ROUGE,en attente",
    "C-loupe-16-attr-it1,C,loupe-16-attr,1,2026-11-18,2026-11-18,VERT,en attente",
]
liv_apres_b = liv_apres.encode("utf-8")
assert liv_apres_b.endswith(b"\n") and b"\r" not in liv_apres_b and not liv_apres_b.startswith(b"\xef\xbb\xbf")
ecrire("livraisons.csv", liv_apres_b)

# ---- defauts.csv ------------------------------------------------------------

deff = lire("defauts.csv").decode("utf-8")
assert deff.endswith("\n") and "\r" not in deff

D1 = ('T-loupe-16-d210-it1,T,loupe-16-d210,guichet-descripteur-quatre-champs,'
      'le champ +8 ForwarderChain lu comme la RVA du nom (la RVA 0x0) ; la marche '
      "de l'OFT au lieu des plages FT (D54) ; la 4e feuille GetLastError non liée"
      ',kit,run-console-unite16-d210-20261118-121219.txt,non,\n')
D2 = ('T-loupe-16-d210-it2,T,loupe-16-d210,liaison-memmove-deux-arguments,'
      '"memmove appelé à DEUX arguments (dst, src) — le compte 8 manquant, contraire '
      "à l'arité des DOUZE autres appels du fichier ; la ligne née du correctif v2, "
      "l'épreuve du guichet n'éprouvait que la découverte\""
      ',kit,run-console-unite16-d210-20261118-140903.txt,non,\n')
D3 = ('T-loupe-16-d210-it3,T,loupe-16-d210,les-metriques-ecran-jamais-posees-par-le-juge,'
      '"la pièce lit les lignes visibles à R_METRIQUES+8 [0xFDF8] (la zone WM_SIZE) ; '
      'le harnais du labo la pose (poser_metriques 27), l\'épreuve POSIX la passe (27) — '
      "le scénario-juge n'a AUCUN geste pour elle : la zone vit aux zéros du .data, "
      'lignes=0, la vitrine dégénère à la vue même, la vue rampe à chaque engagement — '
      'le modèle tient 384 : la vue diverge dès la frappe 328"'
      ',kit,run-console-unite16-d210-20261118-155959.txt,non,\n')

def_apres = deff + D1 + D2 + D3
def_apres_b = def_apres.encode("utf-8")
assert def_apres_b.endswith(b"\n") and b"\r" not in def_apres_b
corps_d = [l for l in def_apres.split("\n") if l and not l.startswith("#")]
assert corps_d[0] == "livraison,bras,tache,classe,mecanisme,cote,piece_appui,exclusion,raison_exclusion"
assert len(corps_d) == 12, len(corps_d)  # l'en-tête + les 8 lignes D204 + les 3 nouvelles
ecrire("defauts.csv", def_apres_b)

# ---- le tableau des condensés ------------------------------------------------

print("LES CONDENSÉS — l'état reçu (la sonde) et l'état attendu après les gestes")
print()
for nom in ["livraisons.csv", "defauts.csv"]:
    avant = lire(nom)
    apres = liv_apres_b if nom == "livraisons.csv" else def_apres_b
    print("%-24s reçu  : %5d o  sha256 %s" % (nom, len(avant), sha256(avant)))
    print("%-24s après : %5d o  sha256 %s" % ("", len(apres), sha256(apres)))
    print()
for nom in ["carnet_temps_humain.csv", "journal-ouverture.txt"]:
    d = lire(nom)
    print("%-24s reçu  : %5d o  sha256 %s  (INCHANGÉ — %s)" % (
        nom, len(d), sha256(d),
        "vos lignes à la main" if "carnet" in nom else "l'ouverture scellée du 14/11"))
print()
print("Les références vivent au bac :", REF)
