tcp-06 · lancement de thread · révision 1
Intention : lancer un thread par CreateThread — le seul point de concurrence
créé du jalon : un thread console et un thread par connexion, tous détachés
de leur handle dès restitution (le handle est fermé par l'appelant, le thread
vit sa vie).
Contrat :
  pre  : P1 rcx contient l'adresse du point d'entrée du thread (une frontière
             d'instruction dans une zone de code de l'image) ;
         P2 rdx contient l'argument unique transmis au thread (valeur
             opaque — socket cliente pour tcp-09, 0 pour tcp-10) ;
         P3 la pile est alignée à l'entrée (rsp ≡ 8 mod 16).
  post : Q1 succès : rax contient le handle du thread créé ; Q2 CreateThread
             est appelé avec attributs NULL, pile 0 (défaut système),
             point d'entrée et argument transmis, fanions de création 0
             (démarrage immédiat), lpThreadId NULL ;
         Q3 échec : rax = 0 propagé — l'appelant décide (fail-closed côté
             orchestrateur) ;
         Q4 le handle rendu n'est PAS fermé par le bloc (l'appelant le
             ferme — la fermeture du handle ne termine pas le thread).
  inv  : I1 unique appel système : IAT kernel32 CreateThread ; I2 les
             arguments 5 et 6 sont posés sur la pile aux loges
             conventionnelles [rsp+0x20] et [rsp+0x28] avant l'appel ;
         I3 le bloc alloue 0x38 octets de pile et n'écrit rien dans le
             shadow space en dehors de ces loges ; I4 aucun état.
Échecs :
  E1 : CreateThread échoue → rax = 0 ; l'orchestrateur journalise « erreur
       reseau » et termine (code 2) : un serveur qui ne peut pas servir une
       connexion refusée refuse tout — pas de file d'attente de threads à M2.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle, shim CreateThread enregistreur) :
       (point d'entrée, argument) transmis intacts, faniers et identifiants
       nuls, handle propagé ; échec propagé par 0 (couvre Q1-Q3).
  V3 : émulation binaire : le thread console est lancé au démarrage, un
       thread par connexion acceptée ; les point d'entrée constatés sont
       les frontières tcp-09/tcp-10 (couvre P1, P2).
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D33.
