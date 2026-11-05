tls13-15 · AES-128 : le déploiement des clés de tour · révision 1
Intention : l'expansion FIPS 197 § 5.2 / SP 800-38A — les ONZE clés de
tour (176 o) depuis la clé de 16 o : le mot w[i] = w[i−4] ⊕ T(w[i−1])
où T = RotWord ∘ SubWord ⊕ Rcon. L'ARRÊT AES-NI NOMMÉ (charte § 3) : la
transcription se fait par l'instruction AESKEYGENASSIST (le SubWord/
RotWord MATÉRIEL) — le S-box n'est PAS une table logicielle : une table
indexée par la donnée secrète est la faille que la charte § 3 interdit,
l'instruction matérielle est temps constant PAR CONSTRUCTION.
Contrat :
  pre  : P1 rcx = la clé (16 o lisibles) ; P2 rdx = la sortie (176 o
             accessibles en écriture : les clés RK[0..10] — RK[0] est
             la clé elle-même) ;
         P3 la pile alignée 16, l'ombre 0x20 fournie.
  post : Q1 le déploiement conforme FIPS 197 § 5.2 — prouvé DIRECTEMENT
             par l'oracle différentiel du chantier (b) (les 176 octets
             confrontés à Python sur les clés FIPS 197 appendice B et
             SP 800-38A F.1.1) ET à L'USAGE par tls13-16 (un
             déploiement faux rend un chiffrement faux : la § F.1.1
             applique SES clés de tour) ;
         Q2 la clé INTACTE ; Q3 rax = 0.
  inv  : I1 les Rcon (les dix constantes de rond) sont des IMMÉDIATS —
             aucune donnée RIP (le miroir du choix av-01/av-08 : le
             bloc autoporteur) ;
         I2 le temps est constant PAR RAPPORT À LA CLÉ (charte § 3 : la
             clé est secrète — AESKEYGENASSIST est L'ARRÊT NOMMÉ,
             aucune table logicielle, aucune branche sur la clé) ;
         I3 L'ÈRE NOMMÉE : AES-NI est exigé par le profil win de l'ère
             (Win10/11 x64 — le miroir de la réserve d'ère du domaine
             sys : le domaine ne s'adapte JAMAIS en silence) ; le
             constat CPUID éventuel est l'affaire du KIT au lancement,
             jamais de la brique ;
         I4 AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ; aucun
             état détenu (charte § 6) ;
         I5 aucun registre non volatil détruit ; NOP, 0x90 (charte § 8).
