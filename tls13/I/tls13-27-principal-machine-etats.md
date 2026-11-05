tls13-27 · le principal : la machine d'états du client · révision 1
Intention : L'ORCHESTRATION — le client TLS 1.3 ENTIER comme machine
d'états sur UN contexte (17 520 o, la disposition DÉCLARÉE ci-dessous) :
QUATRE événements nommés, la poignée ENTIÈRE tenue par OUVRIR (une
boucle bloquante : le socle tls13-28 fournit les rappels émettre/
recevoir — la machine ne fait JAMAIS d'entrée/sortie elle-même, charte
§ 7 : le transport est un ARGUMENT pointé). Le transcript est tenu ICI
(la source de vérité de la poignée, charte § 4) : chaque message de
poignée absorbé DANS L'ORDRE EXACT d'émission/réception (RFC 8446
§ 4.4.1).
Contrat :
  pre  : P1 rcx = le contexte session (17 520 o : le transcript
             [contexte SHA, 112 o] @ +0 ; le calendrier [48 o] @ +112 ;
             la clé privée x25519 [32 o] @ +160 ; la clé publique
             [32 o] @ +192 ; l'émission POIGNÉE [200 o] @ +224 ; la
             réception POIGNÉE [200 o] @ +424 ; l'émission APPLICATION
             [200 o] @ +624 ; la réception APPLICATION [200 o] @ +824 ;
             la clé Finished client [32 o] @ +1024 ; la clé Finished
             serveur [32 o] @ +1056 ; l'empreinte attendue [32 o] @
             +1088 ; l'état u32 @ +1120 ; le remplissage de
             réassemblage u32 @ +1124 ; le pointeur socle u64 @ +1128 ;
             le tampon de réassemblage [2^14 o] @ +1136) ;
         P2 rdx = l'ÉVÉNEMENT ; P3 r8 = l'argument (pointeur) ; P4 r9 =
             sa longueur (ou la capacité) ; la pile alignée 16.
  post : Q1 LA TABLE DES ÉVÉNEMENTS (les états : 0 VIERGE, 1 CH ÉMIS,
             2 POIGNÉE ÉTABLIE — des points de contrôle internes —,
             3 CONNECTÉ, 4 CLOS, 5 MORT ; tout événement hors de sa
             ligne : verdict -3 NOMMÉ, la machine ne devine JAMAIS
             l'intention de l'appelant) :
             É1 OUVRIR (r8 = le pointeur socle [le contexte tls13-28],
               r9 = le pointeur des 96 o : aléa 32 + clé privée 32 +
               empreinte attendue 32 — le kit fournit TOUT : le CSPRG,
               le couple, la confiance) : le couple x25519 (tls13-14),
               le CH composé (tls13-22) et ABSORBÉ, l'enregistrement en
               clair cadrée (5 o : type 22, 0x0303, 114) et ÉMISE au
               socle ; la boucle de lecture : le ServerHello
               (l'enregistrement en clair type 22) → tls13-23, ABSORBÉ,
               l'étage 2 du calendrier (tls13-24) ; les enregistrements
               protégés (tls13-21, réception POIGNÉE) : la marche des
               messages internes avec RÉASSEMBLAGE (le tampon @ +1136,
               la borne NOMMÉE : un message de poignée reçu > 2^14 est
               le verdict -2 — le certificat du monde réel tient en
               2^14, la borne du jalon) — chaque message complet
               ABSORBÉ AVANT tout traitement (charte § 4) ; au
               Certificate : l'extraction de la première entrée de la
               certificate_list (le u24 lu, le DÉTROIT de tls13-26)
               puis l'ÉPINGLAGE ; le CertificateVerify est ABSORBÉ sans
               vérification cryptographique (le chantier futur nommé
               de tls13-26 : la confiance a tranché à l'épinglage — le
               domaine le NOMME, il ne le cache pas) ; au Finished
               serveur : tls13-25 VÉRIFIER, l'étage 3 du calendrier,
               PUIS le Finished client CALCULÉ (tls13-25 sur le
               transcript clos), ABSORBÉ, scellé (tls13-20, type interne
               22) et ÉMIS — ÉTAT 3 (CONNECTÉ), rax = 0 ;
             É2 ÉMETTRE (r8 = la charge, r9 = N ≤ 2^14 ; état 3) :
               tls13-20 (émission APPLICATION, type 23), l'enregistre-
               ment ÉMISE au socle ; rax = 0 ;
             É3 RECEVOIR (r8 = le tampon, r9 = la capacité — elle DOIT
               couvrir l'enregistrement entier [5 + L ≤ 5 + 2^14 + 17] :
               la machine lit l'enregistrement DANS le tampon de
               l'appelant puis restitue la charge AU DÉBUT du même
               tampon — la restitution n'a lieu qu'après le
               déverrouillage, l'écrasement est licite et NOMMÉ) : un
               enregistrement lu au socle, tls13-21 (réception
               APPLICATION), la charge restituée ; rax = la LONGUEUR
               rendue ; un type interne 21 : si close_notify (01 00) →
               état 4, rax = 0 (la fin PROPRE du protocole, la charge
               vide) ; une autre alerne → état 5, rax = -3 NOMMÉ (la
               session est MORTE — le couple niveau/description de
               l'alerne laissé au tampon pour le témoin du kit :
               l'information CONSIGNÉE, jamais muette) ;
             É4 FERMER (états 3 ou 4) : le close_notify composé (2 o :
               01 00 — RFC 8446 § 6.1), scellé (tls13-20, type interne
               21) et ÉMIS ; état 4 ; rax = 0 ;
         Q2 LA DISCIPLINE D'ÉCHEC (charte § 5) : tout verdict négatif
             des briques est PROPAGÉ NOMMÉ (-4/-5/-6/-7 tels quels,
             les -1/-2/-3 des gardes aussi) ; l'état passe à 5 (MORT)
             et AUCUN octet applicatif n'est jamais rendu après (É2/É3
             sur état 5 : -3) ; le close_notify de É4 n'est atteint
             que sur le chemin propre — un échec n'ÉMET RIEN
             (l'exception nommée : le protocole N'EXIGE rien d'un
             client qui vient de constater l'échec) ;
         Q3 LA PREUVE : le TRANSFERT RFC 8448 INTÉGRAL au chantier (c)
             — le transcript enregistré rejoué ÉVÉNEMENT PAR ÉVÉNEMENT
             (le simulateur sert les octets du fixture au socle), les
             octets émis == les octets du RFC 8448 (le CH, le Finished
             client, les enregistrements d'application, le
             close_notify), ET LA FALSIFICATION à chaque étage (le
             ServerHello muté → -5 ; l'étiquette mutée → -4 ;
             l'empreinte mutée → -6 ; la coupure du socle → -7) rend
             SON verdict nommé.
  inv  : I1 les compositions DÉCLARÉES : tls13-14, tls13-22, tls13-23,
             tls13-24, tls13-25, tls13-26, tls13-20, tls13-21 et LE
             SOCLE tls13-28 pour TOUTE entrée/sortie — LA LISTE EST
             FERMÉE (la machine n'appelle rien d'autre : AUCUNE entrée
             IAT, AUCUN site syscall — charte § 7 ; le transport par
             l'argument pointé, l'oracle structurel du jalon le
             constatera sur LE PLUS GRAND bloc comme sur la plus
             petite brique) ;
         I2 la coupe du hash aux étages du calendrier : le contexte
             transcript COPIÉ sur la pile (112 o), la COPIE finalisée
             par tls13-04 (le hachage clos de tls13-04 Q3 ne s'applique
             qu'à la copie — l'original continue de vivre, RFC 8446
             § 7.1 exige le hash COURANT à chaque étage) ;
         I3 le temps constant : les branches de la machine portent sur
             l'ÉTAT et les LONGUEURS (publiques) ; les secrets ne
             traversent que les briques qui les protègent (charte § 3
             héritée par composition) ;
         I4 AUCUN état détenu hors du contexte pointé (charte § 6) ;
             aucun registre non volatil détruit ; NOP, 0x90 (charte
             § 8).
