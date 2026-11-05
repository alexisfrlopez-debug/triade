tls13-21 · l'enregistrement : déprotéger · révision 1
Intention : l'inverse exact — l'enregistrement reçu (l'en-tête de 5 o, le
chiffré de L octets) est déverrouillé : l'AAD = l'en-tête REÇUE TELLE
QUELLE (RFC 8446 § 5.2 : l'authentification couvre les octets reçus),
le nonce = IV ⊕ séquence, tls13-19 rend le verdict. Une désynchronisation
de séquence (rejoue, perte) est une étiquette qui ne colle PAS — la
cryptographie tranche, le bloc n'interroge jamais.
Contrat :
  pre  : P1 rcx = le contexte enregistrement (200 o — la même
             disposition que tls13-20) ;
         P2 rdx = l'enregistrement reçu (5 + L octets, L ≥ 18 : au
             minimum 1 o de type interne + 16 o d'étiquette) ;
         P3 r8 = la longueur totale reçue (5 + L) ; P4 r9 = la sortie
             charge (L − 17 o accessibles) ;
         P5 [rsp+0x28] = le type restitué (1 o accessible — l'octet de
             type du texte interne) ; la pile alignée 16.
  post : Q1 l'en-tête CONFRONTÉE AVANT TOUT : le type doit être 23 (le
             protégé est TOUJOURS opaque — verdict -1 NOMMÉ sur
             divergence) ; la longueur DÉCLARÉE par l'en-tête == L
             (verdict -2 : l'enregistrement doit s'épuiser exactement,
             aucun octet traînant) ; la version héritage est IGNORÉE
             (RFC 8446 § 5.1 : « MUST be ignored for all purposes » —
             la spec ne promet pas ce que le protocole n'exige pas ;
             les octets version reçus restent couverts par l'AAD) ;
         Q2 si tls13-19 rend 0 : la charge restituée (L − 17 o), le type
             réel écrit à P5, la séquence du contexte INCRÉMENTÉE ;
             rax = 0 ;
         Q3 si tls13-19 rend -4 : rax = -4 NOMMÉ — la sortie charge et
             le type demeurent INTACTS (AUCUN octet restitué après un
             échec — charte § 5), la séquence N'EST PAS incrémentée
             (l'échec ne bouge RIEN) ;
         Q4 l'enregistrement reçu INTACT ;
         Q5 la preuve : le TRANSFERT RFC 8448 (les enregistrements du
             transcript OUVERTS par les clés du calendrier — chaque
             type restitué conforme, chaque charge octet pour octet)
             et LA FALSIFICATION INVITÉE (chaque octet du chiffré muté
             → -4 ; la REJOUE d'un enregistrement déjà consommé → -4
             par la séquence avancée — la preuve de l'anti-rejoue du
             protocole tient dans la cryptographie, pas dans un
             compteur de logique).
  inv  : I1 UNE composition : tls13-19 (le déverrouillage) ;
         I2 l'ordre : l'en-tête confrontée AVANT l'appel (les verdicts
             -1/-2 précèdent le -4), la restitution DERNIÈRE ;
         I3 le temps constant hérité (tls13-19 compare sans
             court-circuit) ; AUCUNE entrée IAT, AUCUN site syscall
             (charte § 7) ; aucune écriture hors du contexte, de la
             sortie et du type ;
         I4 aucun registre non volatil détruit ; NOP, 0x90 (charte § 8).
