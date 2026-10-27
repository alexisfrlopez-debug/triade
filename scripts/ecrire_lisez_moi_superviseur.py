#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Écrit LISEZMOI-superviseur.txt (lignée terrain.2, D49) en CP1252 — TRIADE.

La révision D49 : « fais moi 1 seul exe qui contient tout » — le kit
quatre-fichiers devient UN SEUL exécutable, et la fausse alerte Defender
du 27/10 (Wacatac sur proxy.exe téléchargé) reçoit sa réponse documentée.
"""

TEXTE = """TRIADE terrain \u2014 superviseur : TOUS les tests en 1 clic, 1 SEUL exe
====================================================================

superviseur.exe  (61 952 octets, PE32+ WINDOWS_GUI x86-64, \u00e9crit \u00e0 la main)
version 0.5.0-terrain.2 \u2014 le kit embarqu\u00e9 (D49)

CE QUI CHANGE (r\u00e9ponse \u00e0 votre demande \u00ab fais moi 1 seul exe qui
contient tout \u00bb) : fini le kit de QUATRE fichiers \u00e0 poser c\u00f4te \u00e0
c\u00f4te. demo.exe (jalon M2 scell\u00e9), proxy.exe (jalon M3 scell\u00e9) et
l'annexe de jetons Drive vivent DANS superviseur.exe (section .blob,
lecture seule). Un double-clic, un clic sur \u00ab TOUT D\u00c9MARRER \u00bb, c'est
tout : le superviseur pose les artefacts sur disque, les RELIT octet
par octet (la preuve que le disque porte les scell\u00e9s, pas une
impression), encha\u00eene T1/T2/T3, envoie le journal, puis RETIRE les
fichiers pos\u00e9s \u2014 avant et apr\u00e8s le run, votre dossier ne contient
que superviseur.exe et le journal.

  T1 \u2014 demo.exe 0.3.0 (M2 scell\u00e9, embarqu\u00e9) : la d\u00e9mo compl\u00e8te est
       rejou\u00e9e SANS main humaine (fen\u00eatre trouv\u00e9e, bouton cliqu\u00e9
       \u00e0 votre place, 17 lignes exactes v\u00e9rifi\u00e9es et embarqu\u00e9es).
  T2 \u2014 proxy.exe 0.4.0-dev.1 (M3 scell\u00e9, embarqu\u00e9) : le proxy est
       pos\u00e9, curl traverse en HTTP puis en HTTPS (tunnel), la console
       est v\u00e9rifi\u00e9e \u00e9v\u00e9nement par \u00e9v\u00e9nement, arr\u00eat propre par
       \u00ab quit \u00bb, tout le flux est embarqu\u00e9.
  T3 \u2014 envoi Drive : le journal de CE run part automatiquement dans
       le dossier \u00ab test \u00bb du Drive (rafra\u00eechissement OAuth puis
       t\u00e9l\u00e9versement r\u00e9sumable via curl.exe, composant syst\u00e8me).

ANTIVIRUS \u2014 L'ALERTE SUR proxy.exe DU 27/10 : votre capture Defender
(\u00ab Trojan:Script/Wacatac.C!ml \u00bb, niveau Grave) est une FAUSSE alerte,
et voici pourquoi vous pouvez le v\u00e9rifier vous-m\u00eame. Le suffixe
\u00ab !ml \u00bb signifie d\u00e9tection par APPRENTISSAGE AUTOMATIQUE : aucune
signature connue, juste un mod\u00e8le statistique. Ce qu'il a vu : un
petit ex\u00e9cutable sans \u00e9diteur, sans ressources, sans signature
num\u00e9rique \u2014 \u00e9crit OCTET PAR OCTET \u00e0 la main, ce qui est le c\u0153ur du
projet TRIADE (z\u00e9ro compilateur) \u2014 qui \u00e9coute sur un port et relaie
des connexions : c'est le M\u00c9TIER d'un proxy HTTP, et aussi le portrait
robot des proxys malveillants. Le fichier que vous avez re\u00e7u est
strictement celui que j'ai scell\u00e9 : md5 8740e1ca0dbd5967c27cf92bdf713be4
(v\u00e9rifiable : PowerShell, \u00ab Get-FileHash -Algorithm MD5 proxy.exe \u00bb),
chaque octet est auditable dans le d\u00e9p\u00f4t (m3/notation/*.asm). Depuis
cette version, les artefacts voyagent EMBARQU\u00c9S dans superviseur.exe,
qui porte maintenant une VERSION de ressource et un manifeste l\u00e9gitimes
(FileDescription \u00ab TRIADE superviseur terrain \u00bb, asInvoker) \u2014 de quoi
rassurer les heuristiques. Si Defender bloque malgr\u00e9 tout l'extraction
(ligne S04D/S05D \u00ab echec ecriture \u00bb), ajoutez une EXCLUSION de dossier
avant le run : S\u00e9curit\u00e9 Windows -> Protection contre les virus et
menaces -> G\u00e9rer les param\u00e8tres -> Exclusions -> Ajouter un dossier
-> le dossier de test. C'est votre machine : l'exclusion est un choix
de confiance, et le md5 ci-dessus est l'outil de cette confiance.

PR\u00c9PARATION : AUCUNE. Posez superviseur.exe o\u00f9 vous voulez (id\u00e9alement
un dossier d\u00e9di\u00e9). curl.exe n'est PAS \u00e0 installer (composant de
Windows, System32, 10 1803+). Une connexion Internet est requise pour
T2 (neverssl.com, example.com) et T3 (Google Drive).

PROC\u00c9DURE :
  1. Double-cliquez superviseur.exe. La fen\u00eatre \u00ab TRIADE superviseur
     terrain \u00bb s'ouvre, le bouton \u00ab TOUT D\u00c9MARRER \u00bb est en bas.
  2. Un clic sur \u00ab TOUT D\u00c9MARRER \u00bb. C'est tout.
  3. Attendez la fin (comptez ~30 s \u00e0 3 minutes : T1 ~15 s, T2 ~10 s
     \u00e0 2 min selon le r\u00e9seau, T3 ~10 s ; chaque attente est born\u00e9e).
  4. La derni\u00e8re ligne dit tout :
       S90 SUPERVISEUR : TOUT OK
     ou
       S91 SUPERVISEUR : ECHEC (voir lignes KO)
  5. Le journal terrain_YYYYMMDD_HHMMSS.txt est pos\u00e9 \u00e0 c\u00f4t\u00e9 de l'exe
     ET (si T3 a r\u00e9ussi) t\u00e9l\u00e9vers\u00e9 dans le dossier \u00ab test \u00bb du Drive.
     Je le r\u00e9cup\u00e9rerai de l\u00e0 \u2014 vous n'avez RIEN \u00e0 m'envoyer.

LECTURE DE L'\u00c9CRAN (lignes S principales) :
- S02 porte R10 : OK / KO \u2014 l'int\u00e9grit\u00e9 du binaire ET du kit embarqu\u00e9
  (un KO = transfert ab\u00eem\u00e9 : re-t\u00e9l\u00e9charger superviseur.exe).
- S03 libc M1 scell\u00e9e : 4/4 verts \u2014 l'autotest interne.
- S04/S05 : le kit \u2014 demo.exe et proxy.exe extraits, RELUS octet par
  octet (\u00ab octets conformes \u00bb), md5 attendus affich\u00e9s.
- S06 : l'annexe de jetons \u2014 \u00ab extraite, T3 actif \u00bb (cette version).
- S10..S16 : T1 d\u00e9mo. S20..S28 : T2 proxy. S30..S36 : T3 envoi Drive.
- S07 : le nettoyage \u2014 les trois fichiers pos\u00e9s sont retir\u00e9s.
- S90 / S91 : le verdict global.

LECTURE DES ISSUES (si quelque chose casse) :
- S02 KO : binaire ab\u00eem\u00e9 au transfert \u2014 la porte a arr\u00eat\u00e9 AVANT tout
  effet. Re-t\u00e9l\u00e9charger.
- S04D/S05D \u00ab echec ecriture \u00bb : l'antivirus a bloqu\u00e9 la pose d'un
  artefact \u2014 voir la section ANTIVIRUS ci-dessus (exclusion de dossier).
- S04B/S05B \u00ab octets ECART \u00bb : le fichier pos\u00e9 n'est pas retourn\u00e9
  identique (antivirus qui r\u00e9\u00e9crit, disque fatigu\u00e9) \u2014 le test
  associ\u00e9 est saut\u00e9, jamais lanc\u00e9 sur un artefact douteux.
- S21 \u00ab banniere ABSENTE \u00bb : le port 25000 \u00e9tait occup\u00e9, ou le proxy
  a \u00e9t\u00e9 bloqu\u00e9 par une politique syst\u00e8me.
- S23/S25 \u00ab octets=0 \u00bb avec code 0 : le r\u00e9seau a r\u00e9pondu vide \u2014 tout
  le flux captur\u00e9 est dans le journal pour que je diagnostique.
- S33/S34/S35 \u00c9CHEC : le Drive a refus\u00e9 (jeton r\u00e9voqu\u00e9, quota,
  r\u00e9seau) \u2014 le journal reste local, rien n'est perdu.

S\u00c9CURIT\u00c9 : les jetons d'acc\u00e8s au dossier Drive du projet sont
EMBARQU\u00c9S dans cette version de livraison (l'annexe D48 int\u00e9gr\u00e9e) \u2014
gardez l'ex\u00e9cutable et le dossier de test priv\u00e9s ; supprimez l'exe
apr\u00e8s vos runs si vous pr\u00e9f\u00e9rez (je peux en relivrer un \u00e0 tout
moment). Le journal ne contient AUCUN octet des cl\u00e9s (interdit du
projet). Le md5 de CE fichier : 45ca729227867394236ba0fb82efcac5
(sha256 35fce4b7239569c\u2026) \u2014 v\u00e9rifiez-le apr\u00e8s t\u00e9l\u00e9chargement.

Merci \u2014 le premier journal re\u00e7u dans le Drive valide la lign\u00e9e
terrain 0.5.0-terrain.2 (D49).
"""


def main() -> None:
    import os
    chemin = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "LISEZMOI-superviseur.txt")
    with open(chemin, "w", encoding="cp1252", newline="\r\n") as f:
        f.write(TEXTE)
    print(f"écrit : {chemin} ({len(TEXTE.encode('cp1252'))} octets CP1252)")


if __name__ == "__main__":
    main()
