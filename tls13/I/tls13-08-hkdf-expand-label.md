tls13-08 · HKDF-Expand-Label (RFC 8446 § 7.1) · révision 1
Intention : l'étiquette du protocole — la structure HkdfLabel { longueur
u16 ; étiquette <7..255> = « tls13 » + libellé ; contexte <0..255> }
sérialisée GROS-BOUTISTE, puis HKDF-Expand(secret, HkdfLabel, longueur).
LE bloc du calendrier : TOUTES les clés de TLS 1.3 naissent de lui (les
libellés « derived », « c hs traffic », « key », « iv », « finished »… —
des DONNÉES PUBLIQUES du plan d'adressage, jamais des octets de code).
Contrat :
  pre  : P1 rcx = le secret (32 o) ;
         P2 rdx = le libellé (SANS le préfixe « tls13 » — le bloc le
             PRÉFIXE : la constante du plan d'adressage) ; P3 r8 = la
             longueur du libellé (1 ≤ r8 ≤ 249 : 6 + libellé ≤ 255) ;
         P4 r9 = le pointeur du contexte (C octets) ; P5 [rsp+0x28] = C
             (0 ≤ C ≤ 255) ; P6 [rsp+0x30] = L, la longueur de sortie
             (1 ≤ L ≤ 8160) ; P7 [rsp+0x38] = le pointeur de sortie
             (L o) ; pile alignée 16.
  post : Q1 la sortie = HKDF-Expand-Label(secret, libellé, contexte, L)
             — RFC 8446 § 7.1, prouvé au chantier (b) PAR L'ORACLE
             DIFFÉRENTIEL (la structure HkdfLabel reconstruite en
             Python, la comparaison octet pour octet) ET PAR LE
             TRANSFERT RFC 8448 (les clés de poignée du transcript
             enregistré : « c hs traffic », « key », « iv » — les
             clés consignées par le fixture, rendues par le bloc) ;
         Q2 le secret, le libellé et le contexte INTACTS ; Q3 rax = 0
             (ou -1/-2 NOMMÉS : pointeurs nuls, bornes de P3/P5/P6).
  inv  : I1 la sérialisation vit dans UN tampon local sur la pile
             (2 + 1 + 6 + libellé + 1 + C ≤ 264 o), construite par
             OCTETS FIXES — la longueur u16 GROS-BOUTISTE, le préfixe,
             les longueurs u8 — puis remise à tls13-07 : UNE
             composition déclarée ;
         I2 le préfixe « tls13 » et les bornes de structure sont des
             CONSTANTES du plan d'adressage (tls13/layout.py, source
             unique — jamais recopiées dans la notation, T5) ;
         I3 le temps est constant PAR RAPPORT AU SECRET (charte § 3 —
             le libellé et le contexte sont publics) ;
         I4 AUCUN état détenu (charte § 6) ; AUCUNE entrée IAT, AUCUN
             site syscall (charte § 7) ;
         I5 aucun registre non volatil détruit ; NOP, 0x90 (charte § 8).
