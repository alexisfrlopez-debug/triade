sup-09 · scénario (orchestrateur des tests) · révision 1
Intention : le fil ouvrier du superviseur — lancé par UN clic (win-04
scellé, tcp-06 scellé), il enchaîne porte R10, libc, T1 (démo M2), T2
(proxy M3), T3 (envoi Drive), et rend le verdict final : « SUPERVISEUR :
TOUT OK » ou « SUPERVISEUR : ECHEC ». Chaque test est indépendant : un KO
n'arrête pas les suivants (le constat veut TOUT le tableau, pas la
première ligne). Le journal produit est le constat § 8.4 complet —
prêtes à partir dans le Drive par T3.
Contrat :
  pre  : P1 lancé une fois par win-04 (drapeau DRAPEAU_WORKER) ; P2
         TAMPON_NOM/TAMPON_AFF posés (sup-01) ; P3 journal opérationnel ;
         P4 pile alignée.
  post : Q1 en-tête : S00 (bannière), S01 (date, TAMPON_AFF mode 0,
         longueur = retour de sup-21 conservée) ; Q2 autotest win-06
         scellé : -1 -> S02 KO + S91 + rax = 0 (arrêt immédiat — la porte
         invalide TOUT le reste, fail-closed R10) ; 4 -> S02 VERTE +
         S03 4/4 ; autre -> S03 KO + arrêt ; Q3 T1 (sup-33) -> verdict
         journalisé par lui-même (S16) ; Q4 T2 (sup-34) -> S28 ; Q5 T3
         (sup-35) -> S36 ; Q6 verdict final : les trois rax == 1 -> S90
         « SUPERVISEUR : TOUT OK », rax = 1 ; sinon S91 « SUPERVISEUR :
         ECHEC (voir lignes KO) », rax = 0 ; Q7 le fil se termine TOUJOURS
         (retour) — la fenêtre reste ouverte, le journal est complet,
         l'envoi a déjà été tenté.
  inv  : I1 un seul appel par test, dans l'ordre T1 -> T2 -> T3 (l'envoi
         se fait APRÈS que le journal contient tout le reste) ; I2 aucune
         dépendance entre tests (T2 lance son proxy APRÈS la fermeture de
         la démo : le port 25000 partagé impose la séquence — verrou
         d'ordre dans l'oracle) ; I3 le verdict final agrège les trois
         retours — jamais une impression ; I4 la porte R10 précède tout
         test (héritage win-09, R10).
Échecs :
  E1 : porte KO (image corrompue) -> S02 KO + S91, rax = 0, AUCUN test
       lancé — exactement le comportement démo éprouvé.
  E2 : tout test KO -> sa ligne KO, les suivants quand même, S91 final.
Vecteurs :
  V1 : round-trip 100 %.
  V2 : émulation nominale COMPLÈTE (T1 vert, T2 vert, T3 vert) — journal
       ÉCRAN + FICHIER comparés exactement à la séquence d'or dérivée des
       constantes (l'ordre des appels observé : porte avant T1, T1 avant
       T2, T2 avant T3), rax = 1.
  V3 : T2 KO seul -> S91 final, rax = 0, T3 quand même exécuté.
  V4 : porte KO (octet d'un bloc corrompu — falsification) -> arrêt
       immédiat après S02, aucun spawn.
  V5 : falsification — réordonner T3 avant T2 fait échouer le verrou
       d'ordre (le journal serait téléversé incomplet).
Fixtures    : lignes S00..S03, S90, S91 (.rdata zone données sup).
Provenance  : écrite-avant-code.
Décisions   : D48 ; squelette win-09:R4 (porte -> libc -> séquence) ;
              l'indépendance des tests est le cœur du superviseur (un
              constat partiel vaut mieux qu'un arrêt au premier échec).
