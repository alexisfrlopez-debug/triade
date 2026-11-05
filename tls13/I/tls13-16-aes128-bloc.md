tls13-16 · AES-128 : le chiffrement d'un bloc · révision 1
Intention : LE bloc de 16 octets — pxor RK[0], NEUF tours AESENC
(RK[1..9]), le tour final AESENCLAST (RK[10], sans MixColumns) — l'arrêt
AES-NI de tls13-15 poursuivi. Le chiffrement GCM est TOUJOURS le
chiffrement DIRECT : le compteur est re-chiffré pour produire le flot,
l'ouverture re-chiffre les compteurs (SP 800-38D § 6) — LA BRIQUE
D'INVERSION N'EXISTE PAS DANS LE DOMAINE, la découpe le nomme : AES
n'apparaît qu'en sens unique.
Contrat :
  pre  : P1 rcx = les clés de tour (176 o — le produit de tls13-15) ;
         P2 rdx = le bloc d'entrée (16 o) ; P3 r8 = le bloc de sortie
             (16 o — peut chevaucher rdx : le bloc charge AVANT
             d'écrire) ;
         P4 la pile alignée 16.
  post : Q1 la sortie = AES-128(chiffrement, clés, entrée) — FIPS 197 :
             l'exemple de l'appendice B (clé 000102…0f, entrée
             00112233…ff → 69c4e0d86a7b0430d8cdb78070b4c55a) et SP
             800-38A F.1.1 (ECB-AES128, les quatre vecteurs de clé) ;
         Q2 les clés de tour et l'entrée INTACTES ; Q3 rax = 0.
  inv  : I1 le flot : dix tours TOUJOURS exécutés, aucune branche de
             données (la propriété est GRATUITE PAR CONSTRUCTION — la
             spec la constate plutôt que de la payer : l'entrée du CTR
             est publique, le flot produit est secret, l'instruction
             matérielle ne branch pas) ;
         I2 AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ; aucun
             état détenu (charte § 6) ;
         I3 aucun registre non volatil détruit ; NOP, 0x90 (charte § 8).
