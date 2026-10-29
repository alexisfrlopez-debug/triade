sup-39 · prévol — orphelins + réseau amont (avant l'extraction) · révision 1
Intention : les ÉTAPES 0 et 0 BIS du protocole LISEZMOI, exécutées JUSQU'ICI
à la main par le développeur (constat D98 : « la fenêtre principale se ferme,
proxy.exe reste ouvert » → taskkill manuel ; constat D99/D100 : le run 17-D
est mort de l'amont, pas du code → curl manuel), deviennent AUTOMATIQUES —
demande développeur du 29/10 : « peux-tu intégrer la commande taskkill et la
verif curl dans le superviseur ? ». Deux sondes bornées, AVANT l'extraction
du kit : (1) taskkill.exe /f /IM proxy.exe /IM demo.exe tue les orphelins
d'un run ANTÉRIEUR — un proxy.exe survivant VERROUILLE le fichier proxy.exe
que l'extraction doit re-poser (CreateFileA en écriture refusé sur un exe en
cours d'exécution) ET tient le port 25000 ; un demo.exe survivant ferait de
mêmes findings FindWindowW mensongers (T1 lirait la fenêtre d'un mort) ;
(2) curl.exe -s --max-time 20 -o NUL https://example.com/ sonde l'AMONT
DIRECT — sans proxy, la cible exacte du critère M4 — : code 0 = réseau
vivant, 6/7/28 = DNS/connexion/timeout. Les DEUX codes partent au journal
(S08/S09) et NE TOUCHENT JAMAIS le verdict : le prévol est une EVIDENCE, pas
un juge (miroir du témoin D99 : le résultat ignoré, jamais un bit — un
réseau coupé n'est pas un échec du superviseur, c'est un FAIT du run).
Contrat :
  pre  : P1 appelé par sup-09:R4 APRÈS la porte R10 et le verdict libc,
         AVANT l'extraction (sup-37 mode 0) — jamais avant la porte (un
         taskkill est un EFFET : image invalide = aucun effet, R10) ; P2
         journal opérationnel (les lignes S08/S09 passent par win-05 scellé,
         entrée trace, mode numérique r8=1 — miroir S13/S22/S47) ; P3
         sup-31 opérationnel ; P4 pile alignée.
  post : Q1 sonde orphelins : taskkill lancé MODE 0 (sans tuyaux, sans
         héritage — il vit et meurt seul), mort attendue bornée
         WaitForSingleObject(HPROC, 30000), code lu à CODE_SORTIE, handle
         fermé, ligne « S08 orphelins proxy/demo : taskkill code=N » ; Q2
         sonde amont : curl lancé MODE 0 (curl s'autolimite : --max-time
         20), même attente bornée, même lecture, handle fermé, ligne
         « S09 reseau amont : curl code=N » ; Q3 rax = 0 sur TOUT chemin —
         le prévol n'échoue jamais, il constate ; Q4 lancement impossible
         (CreateProcessA faux : taskkill absent d'une politique machine,
         curl.exe introuvable) = ligne SAUTÉE, jamais un crash — un run
         privé de prévol vaut mieux qu'un run mort au prévol ; Q5 chaque
         handle ouvert (HPROC) est fermé avant le retour — zéro fuite,
         même en échec de lancement (le handle n'existe alors pas).
  inv  : I1 une seule tentative par sonde — aucune retry, aucune boucle
         d'attente active (WaitForSingleObject borné : zéro gel, charte
         § 1) ; I2 les codes bruts partent au journal SANS interprétation
         in-code (0/128/1 côté taskkill, 0/6/7/28/259 côté curl : la
         lecture vit au LISEZMOI, pas dans le binaire — un journal
         d'événements rapporte, il ne commente pas) ; I3 le prévol ne
         lit NI tuyaux NI fichiers — aucun CreateFileA, aucun ReadFile :
         le processus sondé est une boîte noire dont seul le code de
         sortie existe ; I4 MODE 0 partout (les sondes n'héritent de
         rien, n'écrivent nulle part — curl écrit dans NUL) ; I5 l'ordre
         taskkill PUIS curl est fixe (tuer d'abord : un orphelin tué
         après la sonde réseau laisserait un run qui « passe » avec un
         zombie) ; I6 le résultat n'entre JAMAIS dans le verdict final
         (sup-09 ignore rax).
Échecs :
  E1 : lancement taskkill impossible -> S08 sautée, la sonde amont
       continue (l'indépendance des sondes est le cœur du prévol).
  E2 : lancement curl impossible -> S09 sautée, retour propre.
  E3 : mort non observée sous 30000 ms -> GetExitCodeProcess rend 259
       (STILL_ACTIVE), la ligne porte 259 : l'évidence reste brute —
       curl --max-time 20 rend le cas pathologique (échéance ignorée)
       ; jamais de TerminateProcess sauvage : la sonde ne tue pas ce
       qu'elle observe.
Vecteurs :
  V1 : round-trip 100 %.
  V2 : émulation — les DEUX cmdlines exactes observées (taskkill puis
       curl amont), MODE 0, cwd répertoire de l'exe, S08 code=128 (rien
       à tuer — l'état propre d'un FS vierge) + S09 code=0 dans le
       journal d'or, AVANT S04 ; ordre verrouillé par la composition du
       journal d'or (prévol -> extraction -> T1…).
  V3 : échec piloté CreateProcessA (taskkill) -> S08 absente, S09
       présente, rax = 0, aucun crash.
  V4 : falsification — la longueur de la ligne S08 corrompue (41 -> 40)
       fait rejeter le journal d'or : l'évidence de prévol est une
       preuve gardée (M10, miroir M9/S47).
Géométrie   : ZONE-RÉSIDENT — slot 0x4B40-0x4BFF (0xC0) dans la queue de
              la zone données sup 1, APRÈS FIN_SUP_1 + marge 16 : le code
              est couvert par l'ENTRÉE DE ZONE R10 (la table est PLEINE
              depuis terrain.17 — 28 entrées, miroir D95/D96/D99 : un bloc
              neuf vit sous une couverture EXISTANTE, jamais comme entrée
              neuve ; la falsification d'un octet du bloc est détectée
              par la somme de zone, la porte reste juge).
Fixtures    : CMD_TASKKILL + CMD_CURL_AMONT + S08 + S09 (zone données
              sup 3, avec les lignes du kit — le prévol précède le kit).
Provenance  : écrite-avant-code.
Décisions   : D101 ; l'exigence développeur du 29/10 ; D98 (le proxy
              orphelin tient le port 25000 — ÉTAPE 0 manuelle née là) ;
              D99/D100 (l'amont intermittent du run 17-D — ÉTAPE 0 BIS
              manuelle née là) ; charte § 4 (« le journal est la preuve »)
              et miroir D99 (« le résultat ignoré, jamais un bit »).
