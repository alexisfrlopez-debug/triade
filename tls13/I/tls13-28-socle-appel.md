tls13-28 · le socle d'appel : le principal ↔ le transport · révision 1
Intention : LA ROTULE — le seul point du domaine où le calcul touche le
monde : un contexte de DEUX rappels (émettre, recevoir) fournis par
l'appelant (le kit), invoqués PAR POINTEUR DEPUIS LE CONTEXTE (charte
§ 7 : l'appel indirect sur une cible qui est une DONNÉE du contexte
n'est NI un import NI un syscall — l'oracle structurel le constatera :
AUCUNE entrée IAT, AUCUN site syscall, UN appel indirect déclaré). Au
harnais : le SIMULATEUR (les octets servis par fixtures — RFC 8448) ;
au terrain : les sockets par SYSCALLS DIRECTS du domaine sys (sys-04+,
le chantier (d) nommé par la couche I) — JAMAIS l'IAT ws2_32 (la
surface de hook que M8 a nommée).
Contrat :
  pre  : P1 rcx = le contexte socle (32 o : le pointeur émettre @ +0,
             le contexte émettre @ +8, le pointeur recevoir @ +16, le
             contexte recevoir @ +24) ;
         P2 rdx = l'OPÉRATION (1 = émettre, 2 = recevoir — toute autre
             valeur : verdict -1) ;
         P3 r8 = le pointeur de données ; P4 r9 = la longueur (émettre)
             ou la CAPACITÉ (recevoir) ; la pile alignée 16.
  post : Q1 ÉMETTRE : le rappel (contexte, r8, r9) invoqué — il rend 0
             (tout émis) ou négatif ; le bloc rend 0 ou -7 NOMMÉ
             (transport en échec — la table du domaine) ;
         Q2 RECEVOIR : le rappel (contexte, r8, r9) invoqué — il rend
             n ≥ 0 (les octets lus, ≤ capacité) ou négatif ; le bloc
             rend n ou -7 NOMMÉ ; le zéro de réception (la demi-fin)
             est le refus -7 du KIT, jamais une lecture vide silencieuse ;
         Q3 L'ABI DES RAPPELS (la frontière DU KIT) : msx64, rcx = le
             contexte du rappel, rdx = le pointeur, r8 = la longueur/
             capacité, rax = le verdict — le kit garantit la RÉCEPTION
             TOTALE à l'émission (un envoi partiel est le refus du
             kit) et la LECTURE BLOQUANTE à la réception ;
         Q4 aucune copie, aucun tampon : le socle est UN ADAPTATEUR —
             les octets appartiennent à l'appelant (charte § 6 : le
             bloc ne détient rien, pas même une mémoire de transport).
  inv  : I1 le temps constant n'a RIEN à sceller ici (charte § 3 : le
             socle ne touche AUCUNE donnée secrète — il transporte des
             OCTETS, chiffrés ou publics ; les longueurs et verdicts
             du transport sont publics) ;
         I2 AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ; aucun
             état détenu (charte § 6) ; aucun registre non volatil
             détruit ; NOP, 0x90 (charte § 8) ;
         I3 les frontières NOMMÉES : le SIMULATEUR du harnais et le
             socle sys-04+ du terrain sont les DEUX réalisations
             licites du contexte — tout autre transport (une
             bibliothèque importée, un IAT) est HORS charte :
             l'oracle structurel du jalon le dira.
