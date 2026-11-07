loupe-07 · cumul : les empreintes du fichier entier au panneau · révision 1
Intention : LES empreintes du fichier ENTIER — MD5 ET SHA-256, la double
empreinte du panneau, née à l'ouverture (loupe-01 l'appelle) et
renaissant à chaque sauvegarde (loupe-17 l'appelle) : le panneau
d'empreintes est TOUJOURS celui du DISQUE, jamais un mensonge de
session. Deux passages par fenêtres glissantes (loupe-05 puis loupe-06)
— un fichier de 2 Gio passe, jamais tout en mémoire.
Contrat :
  pre  : P1 la session est ouverte ; P2 rcx = la sortie, 48 o
             accessibles (md5[16] @ +0 · sha256[32] @ +16 — la
             disposition du panneau, la source unique).
  post : Q1 la sortie = (MD5(F), SHA-256(F)) — F le fichier ENTIER du
             disque, par DEUX passages : loupe-05(0, taille, sortie+16)
             PUIS loupe-06(0, taille, sortie+0) — la composition
             seule, chacun son passage ;
         Q2 la ZONE_EMPREINTES du plan d'adressage EST la sortie
             canonique (loupe-01 et loupe-17 la passent : le panneau
             de la barre la lit — jamais une seconde copie) ;
         Q3 rax = 0.
  inv  : I1 AUCUNE entrée IAT, AUCUN site syscall : le bloc est LA
             COMPOSITION (loupe-05 et loupe-06 PAR LA CARTE — le
             miroir des feuilles pures, charte § 9 ; la lecture vit
             dans les blocs composés) ;
         I2 les DEUX passages passent par TAMPON_CUMUL, L'UN APRÈS
             L'AUTRE (l'exclusion de famille : jamais deux flux
             simultanés — l'application est monofile) ;
         I3 le panneau est CELUI DU DISQUE : les écritures du journal
             (non sauvées) n'y figurent PAS — la barre porte l'asté-
             risque qui nomme la divergence (loupe-10 Q1), la vérité
             n'attend pas la sauvegarde ;
         I4 la vue, le curseur et le journal INTACTS (le calcul ne
             touche à rien de la session) ; registres non volatils
             rendus ; NOP, 0x90.
Échecs :
  E1 : sans session (P1) → verdict -4 SESSION, rax = -4.
  E2 : la sortie inutilisable (P2) → verdict -5 ENTRÉE, rax = -5.
  E3 : un refus de lecture des blocs composés (le verdict -6 rendu
       par loupe-05 ou loupe-06) est RELAYÉ TEL QUEL (le verdict
       traverse : le refus nommé remonte, jamais avalé) — le panneau
       ne publie RIEN.
Vecteurs :
  V1 : différentiel — les témoins du kit + proxy.exe scellé : la
       sortie comparée à (hashlib.md5, hashlib.sha256) du fichier
       entier — l'égalité des 48 o (couvre Q1, Q3).
  V2 : scénario — la chaîne du panneau : ouverture (le panneau né),
       édition (l'astérisque nommé à la barre — le panneau du disque
       DEMEURE), sauvegarde (loupe-17 → le rappel : le panneau
       re-naît vrai) — l'écran attendu à chaque étape (couvre Q2).
  V3 : rejet — sans session, sortie nulle : les DEUX verdicts nommés
       (couvre E1, E2).
  V4 : rejet — le refus -6 du bloc composé relayé tel quel : le
       panneau intact (les 48 o inchangés), rax = -6 (couvre E3).
Fixtures    : proxy.exe scellé (LE témoin absolu : la double empreinte
              du panneau == (md5 hashlib, sha256 446279f3…) — la pièce
              de l'ère jugée par sa propre application).
Provenance  : écrite-avant-code.
Décisions   : D171, D161, D7 (la composition PAR LA CARTE), D134 (les
              empreintes du quotidien).
