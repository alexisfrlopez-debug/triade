hello-03 · sortir (bloc de terminaison) · révision 2
Intention : terminer le processus proprement par le service de sortie du
profil, bloc sans retour — le dernier mot du processus appartient au contrat,
pas au hasard du chargeur.
Contrat :
  pre  : P1 code (argument 1, 32 bits significatifs) : le code de sortie du
             processus (attendu : 0 en nominal, le verdict sinon) ;
         P2 la pile est alignée à l'entrée du bloc (rsp ≡ 8 mod 16 —
             discipline partagée, frag-con, § 8.3-4).
  post : Q1 le processus est terminé au service de sortie du profil (frag-con :
             Windows — ExitProcess, l'appel ne revient jamais ; Linux —
             exit_group, l'appel ne revient jamais) — le bloc ne retourne
             jamais à son appelant.
  inv  : I1 aucun chemin d'exécution au-delà de l'appel : `ud2` défensif
         immédiat, materialisant l'inaccessibilité (fail-closed, esprit
         R10) — l'arrêt défensif est du profil mais la discipline est la
         même : jamais de poursuite en état indéterminé.
Échecs :
  E1 : le service de sortie est intercepté ou échoue (chemin réputé
       inaccessible) → arrêt dur par `ud2` plutôt que poursuite d'exécution
       en état indéterminé.
Vecteurs :
  V1 : round-trip de notation 100 % (couvre P1, P2, Q1, I1).
  V2 : propriété structurelle (oracle) : aucune instruction `ret` dans le
       bloc, `ud2` présent après l'appel au service unique (couvre Q1, I1).
  V3 : test de rejet : toute notation du bloc contenant un `ret`, ou retournant
       à son appelant après l'appel, est refusée par l'oracle (couvre Q1, I1).
  V4 : exécution réelle sur le profil — le code de sortie du processus est le
       code demandé (couvre Q1 ; validation terrain M0 côté Windows, exécution
       native au labo côté Linux — parité par exécution § 8.3).
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D7 (l'interface du profil), D8 (granularité/padding), D26 (M0),
              D149 (révision de granularité — le contrat d'interface sortir
              du corpus).
Historique  : R1 (m0/I, instance Windows scellée 0.1.0, réutilisée octet pour
              octet dans selftest.exe et echo.exe — R7) révisée en R2 au
              chantier M6-(b) : ExitProcess devient « le service de sortie du
              profil » (exit_group chez l'instance Linux), l'argument quitte
              rcx pour son NOM (code), la convention vit en frag-con ;
              l'OBSERVABLE (le processus termine au code demandé, jamais de
              retour) est INVARIANT.
