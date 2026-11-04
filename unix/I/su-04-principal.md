su-04 · orchestration sonde · révision 1
Intention : le point d'entrée ELF de la sonde — la démonstration exécutable
du durcissement format (le critère de sortie du chantier M6-(a)) : calculer
la base de chargement PIE à l'exécution (lea rip sur le témoin .rodata,
l'adresse de liaison soustraite — le code est indifférent à la base, tous
les autres accès vivent en [base + RVA]), émettre la ligne de base, puis
exercer la table ERRNOS sur ses deux branches : une sonde volontaire
write(-1, …) rend -EBADF (errno nommé → verdict 1, la sonde continue), une
sonde volontaire write(1, 0x1, …) rend -EFAULT (errno hors table au
chantier (a) → VERDICT_FATAL 6, ligne fatale, arrêt propre code 6). C'est
le seul bloc non appelable : personne ne l'appelle, le noyau y saute — à
une base que lui seul choisit (ASLR).
Contrat :
  pre  : P1 l'exécution démarre à l'entrée ELF (e_entry 0x1140, RELATIF à
             la base — ET_DYN/PIE) : [rsp] = argc (u64), [rsp+8] = argv[0],
             … terminateur nul — l'ABI de démarrage Linux, et rsp ≡ 0 mod
             16 (sans adresse de retour : la pile d'un _start n'a pas de
             cadre d'appelant) ;
         P2 aucun registre n'est garanti par le noyau à l'entrée (hors
             rsp) — le bloc n'hérite de RIEN ; la base n'est connue de
             nulle part : elle se calcule (lea rip - lien-temps).
  post : Q1 nominal (stdout vivant, noyau conforme) : quatre lignes sur
             stdout — "sonde : base 0x" + hex16(base) + "\n" ; la ligne de
             la sonde 1 (préfixe write(-1), hex16(rax) = fffffffffffffff7,
             verdict 0000000000000001) ; la ligne de la sonde 2 (préfixe
             write(0x1), hex16(rax) = fffffffffffffff2, verdict
             0000000000000006) ; "sonde : VERDICT_FATAL (arret propre)\n"
             — et le code de sortie est 6 (le verdict fatal final, la
             démonstration complète des deux branches) ;
         Q2 émission déficiente (stdout fermé/plein au premier essai) : la
             première émission rend un rax négatif → consultation su-03 ;
             errno nommé → arrêt propre code 0 (le canal de constat est
             mort : plus rien n'est observable, chaque ligne restante serait
             également muette — jamais un crash) ; errno inattendu → ligne
             fatale tentée (muette si le canal est mort) et arrêt code 6 ;
         Q3 aucune sonde ne réussit par accident : les arguments (-1 hors
             domaine, 0x1 sous mmap_min_addr) sont des garanties du noyau ;
             le flux est générique (tout rax négatif passe par su-03), les
             lignes portent les valeurs réelles, jamais les attendues.
  inv  : I1 appels directs : su-01 @ 0x1000, su-02 @ 0x1040, su-03 @
             0x10C0, et le sous-programme local .emit (étiquette interne au
             bloc, frontière d'instruction — déclaré : il émet la ligne
             d'une sonde et rend le verdict) exclusivement ;
         I2 appels système directs : sys_exit_group (rax = 231)
             exclusivement — trois sites (sortie nominale code 0, sortie
             canal-mort code 0, sortie fatale code 6) ; les write passent
             TOUS par su-01, jamais en direct ;
         I3 données : le témoin de base = MSG_BASE @ 0x1C0 (le lea rip
             cible .rodata segment R) ; les autres accès vivent en
             [rbx + RVA] (rbx = base, non-volatil SysV, traversant) :
             messages @ 0x1C0-0x284, tampon @ 0x2000 (.bss segment RW — trois
             sous-zones : +0 hex16 du brut, +16 hex16 du verdict, +32 le
             verdict u32) — chaque déplacement est documenté dans la
             notation ;
         I4 la pile : _start n'a pas de cadre d'appelant (aucun push dans
             le corps) ; le sous-programme .emit s'aligne (sub rsp, 8 à
             l'entrée, add rsp, 8 avant ret — ses appels partent à 0 mod
             16) ; r10 = registre de travail interne : il porte le rax brut
             à travers su-02/su-03 (qui clobber r8/r9 — su-01 n'y touche
             pas : syscall détruit rcx/r11 seuls) ; r8/r9 (préfixe de la
             ligne) sont consommés avant le premier appel ; le verdict vit
             au tampon +32 (la mémoire traverse les appels et les
             syscalls, les registres volatils non) ;
         I5 aucune écriture hors .bss de l'image ; le code n'est jamais
             écrit (pas d'auto-modification — ce n'est pas le chantier (d)).
Échecs :
  E1 : stdout fermé (les deux sondes passent quand même — leurs write
       défaillants rendent EBADF nommé) → Q2 ;
  E2 : le noyau rend un errno imprévu sur une émission → Q2 branche
       fatale ; sur une sonde → la ligne porte le verdict réel (Q3).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : oracle natif (artefact entier) : sur >= 6 exécutions, quatre lignes
       conformes et code 6 à chaque fois ; les bases sont distinctes entre
       exécutions (>= 2 bases — ASLR noyau CONSTATÉ, jamais décrété) et
       alignées à la page ; sous setarch -R (ADDR_NO_RANDOMIZE), deux
       exécutions rendent la MÊME base (la base vient du noyau, pas du
       programme) ;
  V3 : falsification : la corruption d'un octet de n'importe quel bloc
       diverge (sortie, code ou crash) — zéro silence.
Fixtures    : les messages .rodata (longueurs figées par le plan
              d'adressage), la table ERRNOS, HEXCHARS.
Provenance  : écrite-avant-code.
Décisions   : D149 (programme M6/M7), D34 (modèle ah-09 de l'échelle).
Historique  : R1. La symétrie avec ah-09:R1 est délibérée (même rôle,
              profil identique) ; la différence est le SUJET : le hachoir
              hachait, la sonde constate — la sortie n'est pas un service,
              c'est une preuve. Le code de sortie porte le verdict final
              (6) : la sonde démontre les deux branches de la table, la
              branche fatale est terminale par contrat.
