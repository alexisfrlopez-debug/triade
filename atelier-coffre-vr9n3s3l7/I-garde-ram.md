# I-garde-ram · GARDE RAM : le bloc natif scellé · révision 1

> La spec I du bloc natif « GARDE RAM » (l'atelier coffre-vr9n3s3l7, plan
> (e) — le gabarit du projet : Intention / Contrat pre-post / invariants,
> à la manière de tls13/I/*.md). Le bloc vit la notation x86-64 (les
> appels à l'interface du profil — IAT win11, syscalls linux en miroir) ;
> le présent texte en est le CONTRAT. L'implémentation de LABORATOIRE
> livrée avec cette spec est le DÉMONSTRATEUR Python ctypes
> (labo/garde_ram_demo.py) — NOMMÉ démonstrateur, JAMAIS le bloc natif
> scellé : la vérification par émulation (Unicorn : les effets observés,
> la page verrouillée simulée par les hooks, la destruction vérifiée octet
> pour octet) et le terrain Windows réel vivent AU GESTE DU MAÎTRE (le
> gap nommé au rapport).

Intention : aucune page RAM qui porte un secret du coffre (K_user, KEK,
K_emp, les moitiés, la phrase assemblée du séquestre) ne quitte la
mémoire vive : elle est VERROUILLÉE (pas de swap — le vol à froid d'un
disque échangé ne voit rien), EXCLUE des dumps (un core ou une capture
mémoire d'admin ne voit rien), et DETRUITE octet par octet à la sortie
(zéro résidu — le reliquat ne survit pas à l'acte). Le refus est NOMMÉ à
chaque geste : l'OS qui refuse un verrou n'est pas contourné, l'acte qui
exigeait la page est REFUSÉ (fail-closed — jamais le secret dans une page
non verrouillée « en attendant »).

Contrat :
  pre  : P1 rcx = l'adresse du tampon secret (alignée page, N octets,
             N ≤ 16 pages) ; P2 rdx = N ; P3 r8 = le NUMÉRO DU GESTE :
             1 = verrouiller+mettre en exclusion, 2 = détruire+déverrouiller
             (l'ordre du contrat : détruire PUIS déverrouiller) ; P4 r9 = 0
             (réservé, doit être nul — toute autre valeur : rax = -2 NOMMÉ
             « paramètre hors contrat ») ; la pile alignée 16.
  post : Q1 geste 1 : la page verrouillée en RAM — Linux :
             mlock(2) (syscall 149 du miroir linux) ; Windows :
             VirtualLock (IAT win11, kernel32) ; SI l'OS REFUSE
             (rlimit MEMLOCK dépassée, quota insuffisant, page non
             allouable) : rax = -1 NOMMÉ « l'OS refuse le verrou —
             fail-closed : le secret N'EST PAS chargé, l'appelant
             REFUSE l'acte » et AUCUNE écriture n'a eu lieu dans le
             tampon ; l'exclusion des dumps posée dans la foulée :
             Linux : madvise(MADV_DONTDUMP) sur la page (best-effort,
             consigné) ET prctl(PR_SET_DUMPABLE, 0) une fois par
             processus (vérifié par PR_GET_DUMPABLE = 0) ; Windows :
             l'exclusion WER de l'application (l'entrée IAT
             WerAddExcludedApplication) — SPÉCIFIÉE au contrat, exécutée
             au terrain Windows (le gap nommé) ;
         Q2 geste 2 : la destruction SecureZeroMemory/explicit_bzero —
             Windows : SecureZeroMemory (l'idiome volatile+memset de
             winnt.h, IAT win11) ; Linux : explicit_bzero(3) (glibc ≥
             2.25 ; à défaut memset via pointeur volatile — la
             SUBSTITUTION NOMMÉE, la vérification octet par octet fait
             foi) ; les N octets sont ENSUITE relus : tout octet non
             nul ⇒ rax = -3 NOMMÉ « la destruction a laissé un reliquat
             — la page n'est pas prouvée nulle » (le verdict est sur
             pièces, jamais présupposé) ; PUIS munlock(2)/VirtualUnlock —
             si le déverrouillage échoue : rax = -4 NOMMÉ (le verrou
             résiduel est consigné, la destruction est DÉJÀ faite) ;
         Q3 le tampon, l'adresse et N sont INTACTS (aucun octet du
             tampon modifié par le geste 1) ;
         Q4 la preuve : les vecteurs du démonstrateur rejoués — le
             verrou refusé sur demande démesurée (le refus -1 NOMMÉ
             observé), la destruction vérifiée OCTET PAR OCTET (4096
             lectures nulles), le dumpable 0 vérifié par PR_GET_DUMPABLE.
  inv  : I1 l'ORDRE : verrouiller AVANT la première écriture du secret,
             détruire AVANT de déverrouiller — le secret ne vit JAMAIS
             dans une page non verrouillée, le reliquat ne vit JAMAIS
             dans une page rendue à l'OS ;
         I2 la destruction est TOTALE ou NOMMÉE : aucun retour de
             succès sans la relecture intégrale à zéro (le -3 est la
             seule issue d'un reliquat) ;
         I3 aucun secret n'entre dans un journal, un PV, une sortie ou
             une valeur de retour (les codes -1..-4 sont des noms, pas
             des contenus) ;
         I4 AUCUNE entrée IAT au-delà de la liste blanche du profil
             (mlock/munlock/madvise/prctl/explicit_bzero côté linux en
             miroir syscalls ; VirtualLock/VirtualUnlock/
             SecureZeroMemory/WerAddExcludedApplication côté win11 —
             charte § 7 : aucun site d'appel hors profil) ;
         I5 le bloc est SANS ÉTAT entre les appels (aucune page retenue,
             aucun handle détenu — charte § 6) ; le geste 2 sur une page
             non verrouillée par le geste 1 : rax = -5 NOMMÉ « déverrouiller
             sans verrou — l'ordre du contrat violé ».

Position dans le coffre : le bloc est appelé par la sentinelle LCF3 à
chaque acte qui porte un secret en RAM (l'ouverture : K_user, KEK, K_emp ;
la cérémonie (d) : la phrase assemblée du séquestre — le démonstrateur
l'applique avant la destruction de la phrase). Le bloc natif scellé
remplacera les appels du démonstrateur UN À UN (la même interface, les
mêmes codes nommés) — le scellage en copie de labo puis le terrain
Windows réel AU GESTE DU MAÎTRE.
