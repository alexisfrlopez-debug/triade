sup-38 · test T4 — tunnel TLS du proxy M4 (run terrain étape c) · révision 1
Intention : le run terrain que M4 attend (étape c, charte § 8.4 du jalon)
: le tunnel chiffré vit SOUS le proxy. Le superviseur lance proxy.exe
0.5.0-dev.2 avec TUYAUX (sup-31 MODE 1, la voix du proxy captée ligne à
ligne), pose le script client terrain_m4.ps1 (composant système
powershell.exe : la requête « GET https://… HTTP/1.1 » en forme ABSOLUE
n'existe dans AUCUN client standard — curl envoie CONNECT — le script
TCP brut est le seul véhicule honnête de la passerelle M4), puis joue les
DEUX moitiés du critère M4 : (a) https saine — example.com, certificat
valide, la page déchiffrée revient au client (« HTTP/1.1 200 » en tête,
journal console « tunnel chiffre etabli ») ; (b) certificat invalide —
self-signed.badssl.com, SEC_E_UNTRUSTED_ROOT attendu de Schannel, la
502 ÉTIQUETÉE du scellé M4 revient OCTET POUR OCTET (« HTTP/1.1 502
Certificat rejete », 34 o, fixture == artefact, croisement au build) et
la ligne console « certificat rejete ». Les pages reçues sont comptées
(jamais journalisées — discipline M3 : journal d'événements, pas d'octets)
; les événements console du proxy SONT journalisés (flux recopié — le
constat § 8.4 veut la voix du proxy).
Contrat :
  pre  : P1 proxy.exe 0.5.0-dev.2 présent à côté du superviseur (posé par
         sup-37 ; sinon S41B « proxy.exe ABSENT » + suppression du script
         + rax = 0) ; P2 powershell.exe résoluble (composant système
         Windows 10/11 ; sinon S43B « powershell.exe ABSENT » + arrêt
         propre du proxy + rax = 0) ; P3 port 25000 libre (T2 a rendu le
         sien avant nous — l'ordre T2 -> T4 est un invariant de sup-09) ;
         P4 pile alignée ; P5 le script est écrit AVANT le lancement du
         proxy (l'échec d'écriture S40B ne lance rien).
  post : Q1 script posé : terrain_m4.ps1 (fixture FIX_PS1, zone données
         RX, couverte par la table R10) copié vers TAMPON_COMPO (libc-01)
         puis écrit par sup-36 op 1 — le client est une DONNÉE du plan,
         jamais un octet de code superviseur ;
         Q2 lancement proxy.exe par sup-31 MODE 1 (tuyaux) ; Q3 bannière :
         même discipline que T2 ( sondage PeekNamedPipe, 300 essais ×
         50 ms) puis memcmp 40 o == fixture « TRIADE M3 : proxy demarre
         (port 25000)\r\n » (R7 — l'octet bannière du scellé M3 vit dans
         le proxy M4, crossé au build) -> S42A ; divergence -> S42B +
         consommation + arrêt ;
         Q4 requête A : cmdline « powershell.exe -NoProfile
         -ExecutionPolicy Bypass -File terrain_m4.ps1 example.com a »
         (sup-31 MODE 0, attente 45 s, code -> S43A) ; le script TCP
         émet « GET https://example.com/ HTTP/1.1\r\nHost: example.com
         \r\nConnection: close\r\n\r\n » sur 127.0.0.1:25000 et recopie
         la réponse reçue dans page_m4a.txt (jusqu'à fermeture — le
         « Connection: close » garantit la fin propre du relais tls-08
         côté serveur) ;
         Q5 page A : lue par sup-36 (<= 640 o gardés, comptage), LU >= 12
         et memcmp 12 o == « HTTP/1.1 200 » (FIX_200) -> bit ; octets ->
         S44A ; jamais journalisés ;
         Q6 événements A : sondage puis memcmp 58 o == « connexion
         entrante\r\ntunnel chiffre etabli\r\nfin connexion\r\n »
         (FIX_EVT_M4A — la concaténation des fixtures du SCELLÉ M3/M4 :
         msg connexion M3 + ligne tls-08 M4 + fin M3, croisée au build
         contre les octets de l'artefact embarqué) -> les trois lignes
         journalisées (.flux par ligne, miroir T2) ;
         Q7 requête B : même discipline, cmdline « … self-signed.
         badssl.com b », réponse attendue OCTET POUR OCTET : memcmp 34 o
         == « HTTP/1.1 502 Certificat rejete\r\n\r\n » (FIX_502_M4 ==
         TXT_502_CERT du scellé M4 — LE critère « échec propre ») et LU
         == 34 (la réponse étiquetée est COURTE et EXACTE : tout octet
         de plus est une divergence nommée) ;
         Q8 événements B : memcmp 54 o == « connexion entrante\r\n
         certificat rejete\r\nfin connexion\r\n » (FIX_EVT_M4B) -> lignes
         journalisées ;
         Q9 arrêt : « quit\r\n » sur TUYAU_IN_WR, sondage « arret\r\n »
         (7 o), WaitForSingleObject (10 s) — timeout -> TerminateProcess
         (miroir T2 : un proxy muet ne reste pas vivant), second sondage
         5 s, GetExitCodeProcess -> exit 0 exigé, fermeture du handle ;
         Q10 verdict : NEUF bits de succès (bannière, code A, page A,
         événements A, code B, page B 502 exacte, événements B, arret,
         exit 0) tous posés -> S48A « verdict console : conforme » +
         S49A « T4 VERDICT OK » + rax = 1 ; sinon S48B + S49B + rax = 0
         (le flux capté embarqué localise l'intervalle : la dernière
         ligne visible du journal est le diagnostic, leçon demo.3/T2) ;
         Q11 nettoyage : page_m4a.txt, page_m4b.txt, terrain_m4.ps1
         supprimés (sup-36 op 2), extrémités parent des tuyaux fermées —
         TOUT chemin, succès comme échec.
  inv  : I1 les événements sont comparés par memcmp EXACT sur le flux
         brut (l'ordre est séquentiel PAR CONSTRUCTION : la requête B ne
         part qu'après la fin de A — le script les enchaîne, le sondage
         Q6 a vu « fin connexion » avant que la connexion B existe) ;
         I2 rien du contenu des pages n'est journalisé (taille seule,
         memcmp des préfixes attendus — le reste n'est pas à nous) ;
         I3 toutes les attentes bornées par timeout (PeekNamedPipe +
         Sleep ; WaitForSingleObject 45/10/5 s) — aucun ReadFile
         bloquant sans garantie de disponibilité : le superviseur ne
         peut pas GELER ; I4 zéro fuite de handle (fermetures sur tout
         chemin, I3 de sup-31 complété : les DEUX extrémités parent sont
         fermées au nettoyage, le handle processus au Q9) ; I5 le script
         client est une DONNÉE (fixture RX couverte par R10) — le
         superviseur n'interprète RIEN de https : le TLS vit dans le
         proxy testé, la preuve vit dans ses événements et ses octets ;
         I6 powershell.exe est lancé en MODE 0 (héritage nul) — le
         script n'hérite d'aucun handle du superviseur, il ne voit NI
         les tuyaux du proxy NI le journal.
Échecs :
  E1 : script non posé (disque, droits) -> S40B, rien lancé, rax = 0 ;
  E2 : proxy muet (port occupé, intégrité KO) -> bannière divergeante,
       S42B, arrêt tenté quand même, rax = 0 ;
  E3 : powershell absent -> S43B, proxy arrêté proprement, rax = 0 ;
  E4 : page A absente/divergeante (tunnel KO, 502 inattendue, timeout
       ReceiveTimeout 30 s du script) -> bits non posés, S49B final —
       l'événement manquant nomme l'étage (bannière -> poignée ->
       relais) ;
  E5 : page B != 34 o exactes (la 502 étiquetée est le contrat : tout
       autre octet est une falsification ou une régression du scellé) ;
  E6 : exit proxy != 0 (compensation M4 défaillante : un handle SSPI
       survivant tuerait le processus en sortie) -> bit non posé.
Vecteurs :
  V1 : round-trip 100 %.
  V2 : émulation — les DEUX requêtes scriptées (powershell enfui par
       cmdline, effets de bord page_m4a.txt/page_m4b.txt servis par le
       scénario) : journal d'or EXACT (S40..S49 + la voix du proxy
       recopiée : bannière, 6 lignes d'événements, arret), neufs bits,
       rax = 1 ; l'ordre des appels observé (lancement proxy AVANT
       powershell, quit APRÈS la requête B, nettoyage en DERNIER).
  V3 : dégradés nommés — page A vide (LU = 0), page B à 33 o (un octet
       volé), événements B absents (timeout sondage), code A != 0,
       arret muet (timeout) : chaque cas nomme SES bits manquants,
       rax = 0, nettoyage quand même.
  V4 : falsification — corrompre FIX_502_M4 d'un octet fait échouer le
       memcmp du build (croisement artefact) ; inverser l'ordre requête
       A/B fait échouer le verrou d'ordre ; omettre « Connection: close »
       du script fait échouer la relecture de spécification (le relais
       tls-08 ne finirait jamais côté serveur — la fin propre est un
       contrat du script, vérifié à la relecture du FIX_PS1).
Fixtures    : FIX_PS1 (script client, 0x6E00+ zone données sup 3),
              FIX_BANNIERE/FIX_ARRET (partagées T2), FIX_200 (12 o),
              FIX_502_M4 (34 o, == TXT_502_CERT m4/layout.py), FIX_EVT_M4A
              (58 o), FIX_EVT_M4B (54 o), CMD_PS_M4A/CMD_PS_M4B (zone
              données sup 2), NOM_PS1/NOM_PAGE_M4A/NOM_PAGE_M4B.
Provenance  : écrite-avant-code (terrain.17, M4 étape c — le critère M4
              « HTTPS en transit ; échec propre sur certificat invalide »
              atterrit ICI : la preuve du tunnel est la voix du proxy +
              la 502 étiquetée octet pour octet).
Décisions   : D48 (cadre terrain), D49 (kit 1 exe), D77 (charte M4 § 8.4),
              D96 ; le client TCP est powershell.exe parce que la forme
              absolue https:// n'existe dans aucun client standard —
              l'exigence est le CONTRAT du proxy M4 (http-08:R2 Q4),
              le véhicule est une donnée du plan.
