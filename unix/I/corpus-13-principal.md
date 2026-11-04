corpus-13 · orchestration du corpus paritaire · révision 1
Intention : le point d'entrée ELF de l'artefact du jalon M6 — le rituel de
parité : lancer l'auto-test du patrimoine (libc-08, les 21 vecteurs dorés de
la mini-libc scellée en 0.2.0 sous Windows, exécutés ici par l'instance SysV
des MÊMES contrats), journaliser le verdict par la ligne de journal du
patrimoine (tcp-11, le bloc de M2), terminer au code du verdict par le
service de sortie (sortir). C'est le seul bloc non appelable : personne ne
l'appelle, le noyau y saute — à une base que lui seul choisit (PIE, ASLR).
Le code est indifférent à la base : tout accès vit en relatif RIP, jamais en
lien-temps absolu — nul besoin de calculer la base, contrairement à la sonde
qui la CONSTATAIT (le sujet de la sonde était la base ; le sujet du corpus
est le patrimoine).
Contrat :
  pre  : P1 l'exécution démarre à l'entrée ELF (e_entry, RELATIF à la base —
             ET_DYN/PIE) : [rsp] = argc (u64), [rsp+8] = argv[0], …
             terminateur nul — l'ABI de démarrage Linux, et rsp ≡ 0 mod 16
             (sans adresse de retour : la pile d'un _start n'a pas de cadre
             d'appelant) ;
         P2 aucun registre n'est garanti par le noyau à l'entrée (hors rsp)
             — le bloc n'hérite de RIEN ;
         P3 l'état .bss de l'image est vierge (chargement) : curseur d'arène
             nul, verrou journal né déverrouillé (tcp-11:R2 P5), état patch
             v1 (tcp-07:R4 P4) ;
         P4 aucun argument n'est requis ni interprété (argc/argv sont reçus
             et ignorés — le rituel ne prend pas de paramètre).
  post : Q1 nominal (N = 21) : la sortie standard porte exactement DEUX
             lignes, dans l'ordre — la ligne d'auto-test du patrimoine
             ("TRIADE M1 : minilibc 21/21 OK\n", émise par libc-08 pendant
             l'appel) puis la ligne de journal du verdict ("corpus : "
             + "autotest " + décimale de N + " vecteurs\n", composée par
             tcp-11) — et le processus termine au code 0 ;
         Q2 vecteur défaillant (N < 21) : les DEUX lignes sont émises quand
             même (la ligne d'auto-test porte " KO", la ligne de journal
             porte la décimale réelle de N) et le processus termine au
             code 1 — le verdict est TOUJOURS rendu, jamais avorté (le rituel
             est un constat, pas une exécution) ;
         Q3 le code de sortie est porté par sortir (l'unique terminaison —
             deux sites, verdict 0 ou 1, la valeur N tranche).
  inv  : I1 appels directs : libc-08 @ 0x1340, tcp-11 @ 0x1840, sortir @
             0x1040 exclusivement — aucun autre bloc n'est appelé (tcp-07
             vit dans l'image pour l'oracle et le chantier (d), le rituel ne
             le touche pas) ;
         I2 appels système : AUCUN direct — tout service passe par les blocs
             du corpus (écrire par libc-08 et tcp-11, la terminaison par
             sortir) ;
         I3 données : les chaînes du rituel (préfixe et suffixe du journal)
             vivent au plan d'adressage de l'image (.rodata), atteintes en
             relatif RIP ; aucune donnée n'est calculée depuis une adresse
             absolue ;
         I4 la pile : _start n'a pas de cadre d'appelant (aucun push dans le
             corps) ; chaque appel part à rsp ≡ 0 mod 16 (l'ABI exige
             l'alignement AU point d'appel — un _start déjà aligné l'est
             aussi à ses calls directs) ; la valeur N qui traverse les
             appels vit dans un non volatil (rbx — D150 : jamais un
             volatile) ;
         I5 aucune écriture hors .bss de l'image ; le code n'est jamais
             écrit (le patch est le chantier (d), pas le rituel).
Échecs :
  E1 : l'émission de la ligne d'auto-test échoue (sortie indisponible) →
       libc-08 rend N quand même (son contrat Q3 rend le verdict par le
       code), le rituel suit son cours : la ligne de journal est tentée,
       la terminaison porte le verdict (même discipline de propagation que
       hello-01/libc-08:E1 — le canal mort ne change jamais le verdict,
       seulement sa visibilité).
  E2 : l'émission de la ligne de journal échoue → tcp-11 rend le verdict
       brut, le rituel termine au code du verdict (la ligne est perdue,
       le verdict demeure — le journal n'est pas un chemin critique).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : oracle natif (artefact entier, exécution réelle au labo) : la sortie
       est EXACTEMENT les deux lignes nominales (octet pour octet, l'ordre
       et le terminateur \n) et le code de sortie 0 ; l'artefact est PIE :
       des exécutions répétées rendent des bases distinctes (le noyau
       choisit) et le comportement est IDENTIQUE à chaque base — la
       position-indépendance du PATRIMOINE constatée en exécution (couvre
       Q1, P1, I3).
  V3 : falsification : la corruption d'un octet d'un bloc quelconque du
       corpus fait dévier la sortie ou le code (zéro silence — non-vacuité
       de l'oracle, couvre l'ensemble).
  V4 : vecteur défaillant (oracle, en laboratoire) : un vecteur doré falsifié
       (une fixture mutée dans l'image de test, jamais dans l'artefact) →
       N < 21, les deux lignes portent le verdict réel, code 1 (couvre Q2).
Fixtures    : les chaînes du rituel (.rodata, longueurs figées par le plan
              d'adressage).
Provenance  : écrite-avant-code.
Décisions   : D149 (programme M6/M7 — le principal propre au jalon, modèle
              ah-09), D150 (l'état qui traverse vit en non volatil), D26
              (la chaîne artefact).
Historique  : R1. Le domaine est NEUF (le rituel de parité — ni le filtre du
              hachoir ah-09, ni la sonde de su-04 : le patrimoine M0-M5
              exécuté) ; le modèle est ah-09 (l'orchestration _start à
              l'ABI de démarrage Linux, les échecs nommés à chaque étape).
              La symétrie avec tcp-12:R1 (l'orchestration M2 — la porte R10
              puis l'initialisation puis la boucle) est délibérée : même
              rôle, l'orchestrateur du patrimoine — là-bas un serveur qui
              boucle, ici un rituel qui rend son verdict et termine.
