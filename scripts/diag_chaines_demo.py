#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Localise les chaînes du journal démo (CP1252 8 bits) dans les deux binaires."""

def trouve(d, s, enc):
    needle = s.encode(enc, errors="replace") + b"\x00"
    i = d.find(needle)
    res = []
    while i != -1:
        res.append(i)
        i = d.find(needle, i + 1)
    return res

d8 = open("/tmp/demo8.exe", "rb").read()
d9 = open("/tmp/demo9.exe", "rb").read()

chaines = ["réseau : échange en échec", "client : connecté",
           "serveur : écoute 127.0.0.1:25000",
           "écho réseau : aller-retour exact",
           "patch en production : MAJUSCULES",
           "retour arrière : identité confirmée",
           "boucle § 5 complète - DÉMO OK",
           "S1 accept ok", "S2 fil echo lance",
           "sonde4 envoye ok", "sonde5 recu ok",
           "salut triade\r\n", "SALUT TRIADE\r\n"]

for enc in ("cp1252", "utf-16-le"):
    print(f"=== encodage {enc} ===")
    for s in chaines:
        o8 = [hex(x) for x in trouve(d8, s, enc)]
        o9 = [hex(x) for x in trouve(d9, s, enc)]
        print(f"  {s!r:45} d8={o8} d9={o9}")
