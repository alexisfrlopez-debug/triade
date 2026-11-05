sys-02 · le résolveur SSN · révision 1
Intention : lire le numéro de service d'une fonction NT dans l'EAT de
ntdll, SUR LA MACHINE qui exécute — le SSN comme DONNÉE (charte § 1), la
fondation du domaine. Le bloc reçoit la base du module et le span du nom
ASCII ; il marche les noms exportés, confronte le stub au motif (charte § 2)
et rend le numéro — ou un refus nommé. ntdll est LUE, jamais appelée
(charte § 3) : de la mémoire directe, des tables pointées, rien d'autre.
Révision 1 (D160) : la base est FOURNIE par l'appelant (l'obtenir sans IAT
— la PEB-walk — est un chantier futur nommé, frontière du README ; le
principal du jalon la fournira, chantier (c)).
Contrat :
  pre  : P1 rcx = le pointeur du span du nom ASCII (le nom EXACT de
             l'export, p. ex. « NtWriteFile » — jamais une approximation,
             jamais une terminaison NUL supposée : c'est un span) ;
         P2 rdx = la longueur du span (> 0 — le verdict -5 sinon) ;
         P3 r8 = la base du module ntdll (l'adresse de sa première page
             mappée — le bloc la LIT ; il ne la vérifie qu'au motif PE,
             verdict -2 sinon).
  post : Q1 succès : rax = le SSN (l'imm32 du `mov eax` du stub — un
             entier positif ; les numéros des services NT tiennent
             largement dans 16 bits, le bloc ne les borne pas au-delà :
             la borne est le motif, pas un plafond inventé) ;
         Q2 à la réussite, rdx = l'adresse du stub (l'entrée est consommée
             — la PIÈCE de la lecture : l'appelant peut re-vérifier le
             motif lui-même, la preuve ne doit dépendre que de la
             mémoire lue) ;
         Q3 échecs nommés (rax négatif, la table du plan d'adressage —
             charte § 5, jamais un numéro deviné) :
             -1 le nom est introuvable dans l'EAT — la marche COMPLÈTE des
                NumberOfNames noms a été faite (jamais une recherche
                avortée : l'absence constatée est une réponse, pas un
                accident) ;
             -2 la base n'est pas un module PE (le motif « PE\0\0 » à
                e_lfanew est absent, ou e_lfanew lui-même est hors de la
                fenêtre lisible [0x40, 0x400] — un décalage fou est un
                refus, pas un crash) ;
             -3 le répertoire export est ABSENT (son RVA est nul — le
                module n'exporte rien : ce n'est pas ntdll) ;
             -4 le stub diverge du MOTIF_STUB (charte § 2 — hook ou ère
                inconnue : le numéro n'est PAS extrait, il ne le sera
                jamais d'un stub inattendu) ;
             -5 le span est invalide (pointeur nul ou longueur nulle).
  inv  : I1 la marche des noms est BORNÉE par NumberOfNames lue UNE fois
             au répertoire export (charte § 8 — aucun accès hors des trois
             tables : AddressOfNames, AddressOfNameOrdinals,
             AddressOfFunctions ; l'ordinal lu est un indice dans la table
             des fonctions, la fonction lue est un RVA dans l'image du
             module) ;
         I2 la comparaison du nom est libc-02 (memcmp de l'héritage scellé
             M1 — appel direct DÉCLARÉ, le seul du bloc : le domaine ne
             réécrit pas memcmp ; erratum M8-(b) : la couche I naissante
             citait libc-04 — itoa ; le registre figé m1 fait foi) ;
         I3 le motif du stub est vérifié AVANT la lecture de l'imm32
             (charte § 2 — les quatre octets du MOTIF_STUB d'abord, le
             numéro à +4 ensuite ; l'ordre est le contrat, jamais
             l'inverse) ;
         I4 le bloc n'émet JAMAIS l'instruction syscall (le domaine sépare
             LIRE le numéro — sys-02 — et ÉMETTRE l'appel — sys-01 : la
             séparation est la garde, un résolveur qui appellerait serait
             un émetteur déguisé) ;
         I5 aucun IAT (charte § 3) ; I6 le bloc ne détient AUCUN état
             (charte § 6 — le SSN rendu vit chez l'appelant) ;
         I7 aucun registre non volatil modifié (les adresses de travail
             vivent en volatils — le bloc rend la main propre) ;
         I8 aucune écriture mémoire (le bloc LIT ntdll, il ne la touche
             jamais — un résolveur qui écrirait dans le module lu serait
             une falsification de la pièce).
