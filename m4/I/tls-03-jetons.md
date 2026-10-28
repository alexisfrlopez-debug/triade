tls-03 · jetons SSPI (descripteurs) · révision 1
Intention : construire les descripteurs de tampons SSPI (SecBufferDesc +
SecBuffer) dans le cadre de travail TLS — LE seul propriétaire de la mise
en page SSPI du projet (verrou T5) : les tailles, les types de tampons et
l'ordre des champs vivent ici ; aucun autre bloc n'écrit un descripteur.
Contrat :
  pre  : P1 rcx = type de descripteur :
             0 poignée de main  : descripteur à UN tampon SECBUFFER_TOKEN ;
             1 émission         : descripteur à TROIS tampons SECBUFFER_
                                 HEADER / DATA / TRAILER (cadre d'un
                                 enregistrement chiffré) ;
             2 réception        : descripteur à QUATRE tampons SECBUFFER_
                                 DATA / EMPTY / EMPTY / EMPTY ;
         P2 rdx pointe le tampon utile (jeton, clair ou brut reçus) ;
         P3 r8 contient sa longueur utile (u64) ;
         P4 r9 pointe le cadre de destination (zone de travail TLS de la
             session, capacité documentée : 64 + 3 × 16 octets pour le
             descripteur le plus large + alignement) ;
         P5 pour le type 1 uniquement : [rsp+0x28] porte l'adresse des
             tailles de flux (structure acquise par tls-06 — en-tête,
             queue, message maximal) — le descripteur d'émission est
             construit SUR les tailles négociées, jamais sur des
             constantes inventées (charte § 8) ;
         P6 le tampon utile et le cadre sont disjoints.
  post : Q1 succès : rax = 0 — le cadre contient le descripteur complet
             (en-tête 16 octets : ulVersion SECBUFFER_VERSION, compte,
             pointeur vers la suite ; puis les SecBuffer 16 octets :
             longueur, type, pointeur — petit-boutiste, pointeurs 64 bits) ;
             les tampons pointent DANS la zone utile de l'appelant (aucune
             copie — le descripteur RÉFÈRE, il ne possède pas) ;
         Q2 refus de longueur : rax = 1 — jeton > MAX_JETON (16384, type
             0) ou clair > message maximal négocié (type 1) : le
             descripteur n'est pas écrit (l'appelant découpe avant, jamais
             après) ;
         Q3 refus de type : rax = 2 — rcx hors {0, 1, 2} : rien n'est
             écrit (fail-closed sur l'entrée interne).
  inv  : I1 aucune écriture hors du cadre de destination ; I2 aucun
             appel, aucun IAT, aucun état ; I3 le tampon utile de
             l'appelant n'est JAMAIS modifié (lecture de pointeur seule) ;
             I4 aucun registre non volatil modifié ; I5 la mise en page
             est l'unique source de vérité — toute autre écriture de
             descripteur dans le projet est un défaut T5.
Échecs :
  E1 : débordement de jeton (Q2) — nommé « jeton hors borne » : la poignée
       de main refuse les jetons serveur > MAX_JETON (tls-04:E2 fait
       remonte ce refus AVANT la construction).
  E2 : clair trop long (Q2, type 1) — tls-06 découpe en chaîne
       d'enregistrements, chaque morceau sous la borne négociée.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle) : 20 000 triplets (type, ptr,
       longueur) dont longueurs aux bornes exactes (0, MAX_JETON,
       MAX_JETON+1, message maximal ± 1) contre un modèle de référence —
       contenu du cadre octet par octet, verdicts (couvre P1-P6, Q1-Q3,
       I1-I5) ; non-volatils inchangés.
  V3 : fuzzing à propriétés : survie, terminaison, aucun octet écrit hors
       cadre (I1) sur types et longueurs hostiles.
  V4 : test de rejet : toute notation copiant le tampon utile, appelant un
       autre bloc ou écrivant hors cadre est refusée.
Fixtures    : néant (le tampon appartient à l'appelant, le descripteur au
              cadre de session).
Provenance  : écrite-avant-code.
Décisions   : D45, D77, charte M4 § 5 (spans) et § 8 (MAX_JETON).
