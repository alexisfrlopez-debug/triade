tls13-29 · la source CSPRNG du kit (la provision d'entropie) · révision 1 — BROUILLON DE LABORATOIRE (la spécification I manquante, nommée par la commande v0.11.0 : ce brouillon attend la cérémonie d'ère du développeur pour entrer à l'arbre signé tls13/I/ — R2, l'écrit AVANT le code ; le code EXISTANT demeure ce qu'il est, ce document nomme son contrat)
Intention : la source d'aléa du domaine tls13 N'EST PAS dans la pièce —
elle est FOURNIE par le kit du terrain (le scénario-mère), et la pièce la
consomme sans jamais la générer. La spécification nomme CE contrat : le
générateur, le reseed, l'échec fail-closed — la frontière de confiance
entre le kit (la machine du développeur, son OS) et la pièce (les blocs
scellés).
Contrat :
  pre  : P1 le KIT96 du kit porte TROIS champs de 32 octets — l'aléa de
             ClientHello (les 32 octets du random), la clé privée
             x25519 BRUTE (le clamp est l'affaire de tls13-13, jamais de
             la source), et l'empreinte attendue du témoin — la source
             JAMAIS ne transmet autre chose ;
         P2 le générateur du kit est le CSPRNG de l'OS hôte — Python
             os.urandom : sur Windows 10/11, ProcessPrng/BCryptGenRandom
             (le CTR_DRBG du noyau, SP 800-90A, l'entropie des sources
             matérielles) ; AUCUN générateur maison, AUCUN cache de
             valeurs, AUCUNE graine dérivée ;
         P3 le reseed est CELUI DU NOYAU (la politique de l'OS, jamais
             contournée par le kit) : chaque appel à os.urandom tire du
             DRBG noyau en vie — le kit appelle DEUX fois par session
             (l'aléa, la clé privée), JAMAIS une fois pour deux ;
         P4 l'échec est FAIL-CLOSED : si os.urandom lève (l'OS refuse),
             le kit S'ARRÊTE AVANT TOUTE SESSION — aucun ClientHello n'est
             composé, aucune clé n'est dérivée, aucun socket n'est ouvert ;
             la pièce ne connaît pas l'échec de la source (elle ne
             l'atteint jamais) ;
         P5 la clé privée est ÉPHÉMÈRE PAR SESSION : née du tirage,
             JAMAIS stockée (le témoin du kit la journalise en clair pour
             le recoup — le témoin est une PREUVE DE LABORATOIRE, il meurt
             aux archives-preuves, jamais au dépôt).
  post : Q1 la pièce (tls13-22 ClientHello, tls13-13/14 x25519) consomme
             les 32 octets TELS QUELS — AUCUN post-traitement, AUCUN
             reformatage (la bonne foi de la source est le contrat du kit,
             pas un contrôle de la pièce) ;
         Q2 la pièce ne détient AUCUN état d'entropie (charte § 6 : aucun
             état détenu — la source vit au kit, la consommation à la
             pièce) ;
         Q3 rax = 0 à la composition (l'aléa absent ou dégénéré est une
             panne du KIT, nommée AVANT la pièce — la pièce n'a pas de
             verdict pour ce cas, elle ne le voit jamais).
  inv  : I1 UNE seule interface : le KIT96 (le tampon de 96 octets du
             scénario-mère — aléa 32 || clé privée 32 || empreinte 32) ;
             AUCUNE autre voie d'entropie vers la pièce ;
         I2 le générateur est PARAMÉTRABLE PAR LE DÉVELOPPEUR (le contrat
             du kit, D15 : la suite cryptographique appartient au
             développeur — remplacer os.urandom par un autre CSPRNG est
             un changement de KIT, pas de pièce) ;
         I3 l'aléa n'est JAMAIS une entrée de décision : la pièce ne
             BRANCHE sur aucun octet de l'aléa ou de la clé (le temps
             constant structurel, charte § 3 — tls13-13 l'exerce par
             construction) ;
         I4 AUCUN secret au dépôt : la clé privée d'une session vécue ne
             vit JAMAIS dans l'arbre (les témoins du coffre /test
             demeurent, la discipline D12/D87 les tient hors git).
Vecteurs : V1 le RFC 8448 (le transcript officiel) porte le random du
             ClientHello — le harnais poignée le rejoue octet pour octet
             (la valeur FIXE du vecteur, jamais l'aléa du kit : le
             laboratoire JUGE à entrée figée, le terrain VIT à entrée
             aléatoire) ; V2 la clé privée du RFC 7748 § 6.1 (9d61b19d…)
             et son point attendu — le clamp EXERCÉ par la clé publique ;
             V3 le KIT96 réel du septième run (le témoin aux
             archives-preuves : l'aléa et la clé d'une session VÉCUE,
             l'empreinte recoupée).
Provenance : RFC 8446 § 4.1.2 (le random de 32 octets du ClientHello —
             « MUST be generated with a CSPRNG ») ; RFC 7748 § 6.1 ; le
             contrat KIT96 du scénario-m9f (M9-(f), la structure de 96
             octets nommée au code du kit) ; Python os.urandom / Windows
             ProcessPrng (la documentation de l'hôte, la preuve de la
             chaîne : le kit ne fait AUCUNE hypothèse au-delà du CSPRNG
             de l'OS).
Décisions : la commande v0.11.0 nomme la spécification MANQUANTE — le
             présent brouillon la comble au laboratoire ; l'entrée à
             l'arbre signé exigera la cérémonie d'ère du développeur (le
             quinzième arbre, le modèle D177 : la clé hors-ligne, « JAMAIS
             generer ») ; jusqu'alors, CE document est la référence de
             laboratoire — le code du kit et de la pièce demeurent INTACTS
             (aucun octet ne bouge pour un document).
