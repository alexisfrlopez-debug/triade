su-01 · écriture par appel système · révision 1
Intention : écrire des octets sur un descripteur de fichiers — le bloc
d'entrée/sortie élémentaire du jalon, miroir exact de ah-01:R1 de l'échelle
auto-hôte et de hello-02:R1 du profil Windows (WriteFile) : l'artefact parle
directement au noyau, sans bibliothèque, sans tampon intermédiaire. Chez la
sonde, le bloc a un second rôle, déclaré : c'est L'INSTRUMENT DES SONDES
d'erreur — le principal l'appelle aussi avec des arguments volontairement
défaillants (descripteur invalide, tampon illisible) pour faire rendre au
noyau les errno que la table ERRNOS traduit (su-03).
Contrat :
  pre  : P1 edi contient le descripteur de fichiers (u32 ; ex. 1 = stdout ;
             les sondes passent -1, hors domaine, pour provoquer EBADF) ;
         P2 rsi pointe vers le tampon à écrire (mémoire lisible — sauf pour
             la sonde du tampon, qui passe délibérément 0x1, non mappé) ;
         P3 edx contient le nombre d'octets à écrire (u32 ; n <= 2^31-1) ;
         P4 la pile est alignée à l'entrée (rsp ≡ 8 mod 16 — l'appelant
             vient d'exécuter call).
  post : Q1 succès : rax contient le nombre d'octets écrits (>= 0) ;
         Q2 échec noyau : rax contient -errno (valeur négative, la plage
             [-4095, -1] du contrat d'erreurs du jalon — jamais un crash).
  inv  : I1 appel système : instruction syscall avec rax = 1 (sys_write)
             exclusivement — aucun autre numéro, aucune autre interface ;
         I2 feuille : 0 octet de pile consommé, aucun stockage sous rsp,
             aucun registre non volatil touché, aucun push — l'instruction
             syscall détruit rcx/r11 (documenté fiche § 4 : l'auteur ne le
             réapprend pas à chaque bloc) ;
         I3 le bloc ne tamponne pas : un appel, un verdict — l'appelant
             gère les écritures partielles et les errno (le principal de la
             sonde route tout rax négatif par su-03, jamais au hasard).
Échecs :
  E1 : descripteur invalide ou fermé → rax = -EBADF (-9) — échec nommé de
       la table (verdict 1) ; c'est le chemin de la sonde 1 ;
  E2 : tampon illisible → rax = -EFAULT (-14) — errno hors table au
       chantier (a) → VERDICT_FATAL ; c'est le chemin de la sonde 2 ;
  E3 : n > ce que le descripteur accepte → écriture partielle (Q1).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : oracle natif (artefact entier) : les émissions de la sonde passent
       toutes par ce bloc (code de sortie et lignes attendus octet pour
       octet) ; les deux sondes d'erreur rendent exactement -9 et -14.
Fixtures    : néant (le bloc ne possède aucune donnée).
Provenance  : écrite-avant-code.
Décisions   : D149 (programme M6/M7), D34 (modèle ah-01 de l'échelle).
Historique  : R1. Premier bloc du domaine su — la sonde du durcissement.
              Le contrat est celui de ah-01:R1, révisé pour le second rôle
              déclaré (instrument des sondes) : P1/P2 élargies aux arguments
              défaillants VOLONTAIRES, les échecs E1/E2 nommés comme
              chemins de démonstration, jamais comme accidents.
