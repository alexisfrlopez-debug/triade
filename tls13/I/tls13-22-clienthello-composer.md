tls13-22 · la poignée : composer le ClientHello · révision 1
Intention : LE premier message — l'offre du client en 114 octets FIXES
(la longueur est une CONSTANTE du plan d'adressage, vérifiée par
construction au chantier (b)) : version héritage 0x0303, aléa 32 o (UN
ARGUMENT — le CSPRG vit au kit/au domaine sys, jamais dans les briques :
frontière nommée), session_id héritage VIDE (le mode compatibilité
boîtes intermédiaires est un chantier futur nommé), LA suite seule
(0x1301, charte § 1), compression nulle, QUATRE extensions :
supported_versions (0x0304), supported_groups (x25519),
signature_algorithms (rsa_pss_rsae_sha256, rsa_pkcs1_sha256 — des
préférences DECLARATIVES de forme : le client n'envoie aucun certificat
et n'en VÉRIFIE AUCUN — l'épinglage tls13-26 tranche la confiance ; la
liste satisfait l'exigence du RFC 8446 § 4.2.3), key_share x25519 (la
clé publique de tls13-14).
Contrat :
  pre  : P1 rcx = l'aléa (32 o — la sortie du CSPRG de l'appelant) ;
         P2 rdx = la clé publique x25519 (32 o — le produit de
             tls13-14) ;
         P3 r8 = la sortie (114 o accessibles : le message de poignée
             COMPLET — l'en-tête type 1 + longueur u24 + le corps) ;
         P4 r9 = la capacité offerte (≥ 114, verdict -2) ; la pile
             alignée 16.
  post : Q1 la sortie = le ClientHello de 114 octets — OCTET POUR
             OCTET la structure du premier message du transfert RFC
             8448 § 3 (l'aléa et la clé du fixture à la place des
             nôtres : mêmes champs, mêmes ordres, mêmes longueurs) ;
             la preuve du chantier (b) joue le fixture ET l'oracle
             structurel (chaque champ à son offset déclaré, la
             longueur totale == la constante) ;
         Q2 l'aléa et la clé INTACTS ; Q3 rax = 0.
  inv  : I1 la composition par OCTETS FIXES : chaque champ est écrit à
             son offset constant (les valeurs protocolaires — 0x0303,
             0x0304, 0x1301, 0x001d, 0x002b, 0x000a, 0x000d, 0x0033,
             0x0804, 0x0401 — sont des CONSTANTES du plan d'adressage,
             source unique : la spec ne les recopie pas dans la
             notation, T5) ; AUCUNE branche, AUCUNE construction
             variable : le message est FIXE, il n'y a rien à négocier
             (charte § 1) ;
         I2 le message ne TOUCHE PAS au transcript (l'absorption est le
             geste du principal tls13-27, dans l'ordre D'ÉMISSION — la
             séparation est nommée : le compositeur compose, la
             machine d'états chronique) ;
         I3 frontière nommée : SNI (l'extension nom de serveur) est un
             CHANTIER FUTUR NOMMÉ — le ClientHello minimal du jalon
             n'en porte pas (le kit cible le serveur par son adresse,
             l'épinglage fait la confiance) ;
         I4 AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ; aucun
             état détenu (charte § 6) ; aucun registre non volatil
             détruit ; NOP, 0x90 (charte § 8).
