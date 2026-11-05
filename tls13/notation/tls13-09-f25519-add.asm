; tls13-09-f25519-add · bloc f25519 addition réduite (cinq membres, miroir av-07) · spec tls13-09:R1 · bloc carte h100009
; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0xc980, taille 128 octets
; Domaine : tls13 (M9, l'ère 1.0.0) · Dépendances : bloc feuille de la famille x25519 ; tls13-12 (UNE passe — I1) ; les CINQ additions membres à membres IN PLACE, la sortie ÉCRASE a (Q2, miroir av-07) ; les bornes < 2^53 en registres volatils — AUCUN déplacement RIP
; Notation explicite générée par outils/auteur.py depuis brouillons/tls13-09-f25519-add.asm
; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)
; Code : 54 o · padding : 74 o (NOP, 0x90)
; Appels directs (l'adresse scellée du plan — I1) : call 0xcfc0
mov rax, qword ptr [rdx]
add qword ptr [rcx], rax
mov rax, qword ptr [rdx + 8]
add qword ptr [rcx + 8], rax
mov rax, qword ptr [rdx + 16]
add qword ptr [rcx + 16], rax
mov rax, qword ptr [rdx + 24]
add qword ptr [rcx + 24], rax
mov rax, qword ptr [rdx + 32]
add qword ptr [rcx + 32], rax
sub rsp, 0x28
call 0xcfc0
add rsp, 0x28
xor eax, eax
ret
