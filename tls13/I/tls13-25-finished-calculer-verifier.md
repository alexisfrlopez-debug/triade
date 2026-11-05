tls13-25 · la poignée : le Finished — calculer et vérifier · révision 1
Intention : la preuve de possession des clés — verify_data =
HMAC(clé_Finished, hash du transcript) (RFC 8446 § 4.4.4 : le Finished
EST le HMAC du transcript — la preuve de possession n'est jamais une
parole, charte § 4). DEUX modes NOMMÉS : CALCULER (le nôtre, à émettre)
et VÉRIFIER (celui du serveur, à confronter).
Contrat :
  pre  : P1 rcx = la clé Finished (32 o — le produit de l'étage 2 de
             tls13-24, la DIRECTION correspond à l'ÉMETTEUR du
             message) ;
         P2 rdx = le hash du transcript (32 o — au point de coupe
             NOMMÉ par le RFC 8446 § 4.4.4 : pour le serveur, CH..
             Certificate/CertificateVerify ; pour le client, CH..le
             Finished serveur) ;
         P3 r8 = le pointeur 32 o : en mode CALCULER, la SORTIE (le
             verify_data à émettre) ; en mode VÉRIFIER, le REÇU (les
             32 octets du message Finished reçu) ;
         P4 r9 = le mode (0 = calculer, 1 = vérifier — toute autre
             valeur : verdict -1) ; la pile alignée 16.
  post : Q1 mode CALCULER : la sortie = HMAC(clé, hash), rax = 0 — le
             TRANSFERT RFC 8448 (le finished_verify_data du client du
             transcript enregistré, octet pour octet) ;
         Q2 mode VÉRIFIER : le reçu CONFRONTÉ par OU cumulatif des 32
             différences (charte § 3 : AUCUNE court-circuit — la
             comparaison d'un secret ne s'arrête jamais au premier
             octet différent) ; conforme → rax = 0 ; divergent → rax =
             -4 NOMMÉ (cryptographie divergente — la session MEURT,
             charte § 5) ; le reçu n'est JAMAIS modifié ;
         Q3 la clé et le hash INTACTS.
  inv  : I1 UNE composition : tls13-05 (l'HMAC — le Finished n'est
             RIEN d'autre) ;
         I2 le mode est une donnée PUBLIQUE de contrôle (le branch sur
             r9 n'est pas une branche de donnée secrète — la charte § 3
             nomme la frontière : les branches de CONTRÔLE sur des
             arguments publics sont licites) ;
         I3 AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ; aucun
             état détenu (charte § 6) ; aucun registre non volatil
             détruit ; NOP, 0x90 (charte § 8).
