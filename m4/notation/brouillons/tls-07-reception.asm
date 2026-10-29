; tls-07 · réception déchiffrée · spec tls-07:R2 · bloc carte g70007
; pre : rcx pointe le cadre de session TLS (offsets documentés layout.CADRE_*,
;       convention D81 AMENDÉE D89 — le contexte est ÉTABLI par tls-04 :
;       phContext @+0x10 vivant ; les champs +0x3A/+0x3C [longueur utile /
;       offset résidu, D89] décrivent la région vivante de la zone de
;       réception léguée par l'appel précédent — vierge : (0, 0)) ;
;       rdx pointe la zone de réception (capacité 2 × MAX_JETON = 32768,
;       D89 — le résidu Extra suivi des octets bruts reçus par-dessus PAR
;       L'APPELANT tls-08, jamais ailleurs : la région vivante est
;       [zone + offset, zone + offset + longueur]) ;
;       r8 contient la longueur utile TOTALE de la région vivante
;       (résidu Extra PRÉCÉDENT + octets bruts reçus depuis le dernier
;       appel — le descripteur reçoit la zone ENTIÈRE à chaque appel,
;       sémantique SSPI) ;
;       r9 pointe le span de sortie (deux mots : ptr, longueur — propriété
;       de l'appelant http-10:R2, rempli UNIQUEMENT sur succès Q1)
; post : rax = 0 — UN enregistrement déchiffré (Q1) : le span EST le
;       PREMIER tampon reclassé SECBUFFER_DATA PAR la bibliothèque
;       (D102 — Schannel réelle réécrit les QUATRE tampons en sortie de
;       son SEC_E_OK : [0]=STREAM_HEADER [l'en-tête du record — 13 o en
;       GCM : 5 en-tête + 8 nonce, la preuve byte-level du témoin 17-C/
;       17-F], [1]=DATA [LE clair, pv = zone + en-tête], [2]=TRAILER,
;       [3]=EXTRA ou EMPTY — et msdn « Extra Buffers Returned by
;       Schannel » nomme l'EXTRA rendu « seul, à une position
;       quelconque » : le scan PAR TYPE est le contrat, JAMAIS la
;       position — l'exemple canonique msdn « Decrypting a Message »
;       scanne i < 4 par BufferType, le PREMIER DATA gagne) — le span
;       pointe DANS la zone (déchiffrement sur place — le clair remplace
;       le brut à l'offset de l'en-tête d'enregistrement, tampon DATA
;       réécrit PAR la bibliothèque ; l'appelant pompe ce clair AVANT
;       tout nouvel appel : IL SERA ÉCRASÉ — par la normalisation de
;       l'appel SUIVANT, lecture géométrique D89) ;
;       le résidu Extra éventuel = le tampon reclassé SECBUFFER_EXTRA
;       (le DERNIER gagne si la bibliothèque en rend plusieurs — cas
;       pathologique hors msdn, un seul en pratique) est CONSIGNÉ :
;       longueur utile @+0x3A := résidu, offset @+0x3C := lot −
;       résidu — la région vivante [offset, offset+longueur) est
;       exactement le résidu ; le DÉPLACEMENT en tête (libc-01)
;       appartient au PROCHAIN appel (I1 : personne d'autre ne touche
;       la zone entre deux appels) ;
;       rax = 2 — message incomplet (Q2) : AUCUN octet consommé, la zone est
;       laissée EN L'ÉTAT (normalisée ce tour : (0, lot)), la bibliothèque
;       a reclassé le tampon porteur en SECBUFFER_MISSING (octets
;       manquants — IGNORÉS : la quantité n'est jamais une dépendance) ;
;       l'appelant réceptionne davantage et rappelle avec la nouvelle
;       longueur totale ;
;       rax = 4 — fin de contexte (Q3, close_notify) : fin PROPRE, le
;       résidu éventuel (= le tampon SECBUFFER_EXTRA, CHERCHÉ PAR TYPE —
;       D102 : l'ancienne lecture positionnelle du tampon 1 tombait sur
;       le DATA reclassé) est PURGÉ (lu, curiosité « fin propre avec
;       résidu » consignée @+0x3A si longueur > 0 — le serveur a parlé
;       après sa fermeture, pas d'interprétation), offset := 0 ;
;       rax = 6 — E4 D102 : SEC_E_OK SANS aucun tampon reclassé
;       SECBUFFER_DATA (bibliothèque dégénérée, descripteur altéré en
;       vol) — AVANT toute écriture au span et au cadre-résidu
;       (fail-closed : le clair est introuvable, l'échec est nommé,
;       le span de sortie reste INTACT — jamais un mot forgé) ;
;       rax = autre verdict non nul (Q4 — 5 altération, 6 fatal…) : le
;       cadre porte le verdict @+0x30 ET l'HRESULT d'origine @+0x34
;       (tls-02:Q2) ;
;       rax = 5 « zone de réception dépassée » (E2) : la région utile ne
;       tient pas dans la zone (lot > 2 × MAX_JETON ou offset + lot >
;       capacité) — refusé AVANT tout appel SSPI et AVANT tout déplacement,
;       la zone et les champs sont laissés INTACTS (fail-closed : le flux
;       est anormalement dense, la session refuse)
; inv : I1 le résidu Extra n'appartient qu'à tls-07 (normalisation libc-01
;       en tête — personne d'autre ne touche la zone entre deux appels) ;
;       I2 aucune fermeture de socket (tls-08 seul propriétaire — ici :
;       AUCUNE socket, AUCUN ws2_32) ; I3 aucune journalisation de brut ni
;       de clair (charte § 3 — aucun WRITE, aucun IAT kernel32) ; I4 aucune
;       écriture hors zone de réception, cadre et span de sortie (le
;       descripteur vit dans la PILE de travail) ; I5 volatils seuls
;       modifiés — cadre, zone, longueurs et span sauvegardés dans la
;       pile ; I6 la POSITION d'un tampon n'est JAMAIS une hypothèse —
;       seuls les TYPES parlent (D102)
; ABI : msx64 — DecryptMessageW = 4 arguments registre (phContext cadre+0x10,
;       pMessage = descripteur de pile tls-03 type 2 [QUATRE tampons :
;       DATA zone entière + 3 EMPTY — EN ENTRÉE ; la bibliothèque répond
;       en RECLASSANT les types : [0]=STREAM_HEADER, [1]=DATA le clair,
;       [2]=STREAM_TRAILER, [3]=EXTRA le résidu — règles D89 AMENDÉES
;       D102, partagées modèle/émulation], MessageSeqNo 0 [schannel suit
;       la séquence via le contexte], pfQOP = mot de pile RÉÉCRIT 0 avant
;       l'appel — aucun état résiduel, la valeur n'est jamais interprétée) ;
;       tls-03 type 2 = 4 arguments registre (2, zone, lot, cadre de
;       destination) ; pile de travail : pfQOP @rsp+0x58, cadre @rsp+0x60,
;       zone @rsp+0x68, lot @rsp+0x70, span @rsp+0x78, descripteur
;       @rsp+0x90 (80 o = 16 + 4 × 16) — sub rsp 0xE8 aligne la frontière
;       msx64 ; libc-01 copie en AVANT (rep movsb croissant) : dest zone <
;       src zone+offset est sûr MÊME en recouvrement, pour tout résidu et
;       tout consommé ; tls-02 route chaque HRESULT (volatils morts au
;       retour : le cadre est RECHARGÉ de la pile après chaque appel) ;
;       le scan D102 lit pBuffers @rsp+0x98 et fouille les 4 tampons (16 o
;       chacun : cb +0, type +4, pv +8) — r11 = pBuffers, r8 = indice,
;       rcx = 2×indice (adresse [r11 + rcx*8]), rax/rdx = ptr/longueur
;       DATA, r9 = cb EXTRA
sub rsp, 0xE8
mov qword ptr [rsp + 0x60], rcx
mov qword ptr [rsp + 0x68], rdx
mov qword ptr [rsp + 0x70], r8
mov qword ptr [rsp + 0x78], r9

; --- E2 : densité hostile — la région vivante [offset, offset+lot) doit
; --- TENIR dans la zone (2 × MAX_JETON) : la garde UNIQUE tient la SOMME
; --- (elle subsume la longueur seule — offset lu u16, donc >= 0 : tout
; --- lot > capacité donne somme > capacité), AVANT tout appel SSPI et
; --- AVANT tout déplacement (fail-closed ; une garde redondante serait
; --- infalsifiable — le différentiel l'a nommée, elle est partie)
mov r10, [rsp + 0x60]
movzx eax, word ptr [r10 + 0x3C]
lea rcx, [rax + r8]
cmp rcx, 0x8000
ja .depassee

; --- normalisation D89 : le lot vivant descend en tête — le clair de
; --- l'appel précédent (pompé par l'appelant) est de la mémoire morte,
; --- le résidu devient le début du PROCHAIN enregistrement (P1 : le lot
; --- au déchiffrement est [résidu][octets bruts récents] depuis la tête)
test eax, eax
jz .normalise
mov rcx, [rsp + 0x68]
lea rdx, [rcx + rax]
call MEMCPY
mov r10, [rsp + 0x60]
mov word ptr [r10 + 0x3C], 0

; --- descripteur tls-03 type 2 : la zone ENTIÈRE (normalisée) en DATA
; --- + trois EMPTY — EN ENTRÉE ; la bibliothèque répond en RECLASSANT
; --- les types (règles D89 AMENDÉES D102)
.normalise:
mov rdx, [rsp + 0x68]
mov r8, [rsp + 0x70]
lea r9, [rsp + 0x90]
mov ecx, 2
call TLS_JETONS

; --- DecryptMessageW : déchiffrement SUR PLACE dans la zone
mov rax, [rsp + 0x60]
lea rcx, [rax + 0x10]
lea rdx, [rsp + 0x90]
xor r8d, r8d
lea r9, [rsp + 0x58]
mov dword ptr [rsp + 0x58], 0
call qword ptr [rip + IAT_DM]

; --- verdict tls-02 (HRESULT brut JAMAIS propagé — charte § 1)
movsxd rcx, eax
call TLS_VERDICTS
mov r10, [rsp + 0x60]
mov dword ptr [r10 + 0x34], edx
test eax, eax
jz .succes
cmp eax, 2
je .incomplet
cmp eax, 4
je .fin_contexte

; --- Q4 : verdict 1/3/5/6… — échec nommé, la région (normalisée ce tour)
; --- est consignée (0, lot), l'échec remonte tel quel
mov [r10 + 0x30], eax
mov word ptr [r10 + 0x3C], 0
mov r8, [rsp + 0x70]
mov word ptr [r10 + 0x3A], r8w
add rsp, 0xE8
ret

; --- E2 : « zone de réception dépassée » — zone et champs INTACTS
.depassee:
mov r10, [rsp + 0x60]
mov dword ptr [r10 + 0x30], 5
mov eax, 5
add rsp, 0xE8
ret

; --- Q2 : message incomplet — aucun octet consommé, tampon MISSING
; --- ignoré : l'appelant réceptionne DAVANTAGE par-dessus le lot
.incomplet:
mov dword ptr [r10 + 0x30], 2
mov rax, [rsp + 0x70]
mov word ptr [r10 + 0x3A], ax
mov word ptr [r10 + 0x3C], 0
mov eax, 2
add rsp, 0xE8
ret

; --- Q3 : fin de contexte — fin PROPRE, le résidu éventuel est PURGÉ
; --- (consigné @+0x3A : « fin propre avec résidu » si > 0, curiosité
; --- sans interprétation — le serveur a parlé après sa fermeture).
; --- D102 : le résidu est le tampon SECBUFFER_EXTRA (= 5, sspi.h) CHERCHÉ
; --- PAR TYPE (l'ancienne lecture du tampon 1 tombait sur le DATA reclassé)
.fin_contexte:
mov dword ptr [r10 + 0x30], 4
mov r11, [rsp + 0x98]
xor r8d, r8d
xor r9d, r9d
.scan_fin:
lea rdx, [r8 + r8]
cmp r8, 4
jae .fin_consigne
cmp dword ptr [r11 + rdx*8 + 4], 5
jne .pas_extra_fin
mov r9d, dword ptr [r11 + rdx*8]
.pas_extra_fin:
inc r8d
jmp .scan_fin
.fin_consigne:
mov r10, [rsp + 0x60]
mov eax, r9d
mov word ptr [r10 + 0x3A], ax
mov word ptr [r10 + 0x3C], 0
mov eax, 4
add rsp, 0xE8
ret

; --- Q1 : le span = le PREMIER tampon SECBUFFER_DATA (= 1, sspi.h ; scan
; --- PAR TYPE, miroir de l'exemple canonique msdn « Decrypting a Message »
; --- — le PREMIER gagne), le résidu = le SECBUFFER_EXTRA (= 5 ; le
; --- DERNIER gagne si plusieurs — cas hors msdn) : région vivante
; --- (lot − résidu, résidu). E4 : aucun DATA → verdict 6, span INTACT,
; --- région consignée normalisée (0, lot) — miroir de Q4, la géométrie
; --- de la région vivante reste VRAIE (la normalisation a déjà joué).
.succes:
mov r11, [rsp + 0x98]
xor r8d, r8d
xor eax, eax
xor r9d, r9d
.scan:
lea rcx, [r8 + r8]
cmp r8d, 4
jae .scan_fini
cmp dword ptr [r11 + rcx*8 + 4], 1
jne .pas_data
test rax, rax
jnz .pas_data
mov rax, qword ptr [r11 + rcx*8 + 8]
mov edx, dword ptr [r11 + rcx*8]
.pas_data:
cmp dword ptr [r11 + rcx*8 + 4], 5
jne .pas_extra
mov r9d, dword ptr [r11 + rcx*8]
.pas_extra:
inc r8d
jmp .scan
.scan_fini:
test rax, rax
jz .sans_data
mov r10, [rsp + 0x78]
mov [r10], rax
mov [r10 + 8], rdx
mov r10, [rsp + 0x60]
mov dword ptr [r10 + 0x30], 0
mov word ptr [r10 + 0x3A], r9w
mov rax, [rsp + 0x70]
sub rax, r9
mov word ptr [r10 + 0x3C], ax
xor eax, eax
add rsp, 0xE8
ret
.sans_data:
mov r10, [rsp + 0x60]
mov dword ptr [r10 + 0x30], 6
mov word ptr [r10 + 0x3C], 0
mov r8, [rsp + 0x70]
mov word ptr [r10 + 0x3A], r8w
mov eax, 6
add rsp, 0xE8
ret
