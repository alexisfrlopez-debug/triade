#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Décoder les EventTime + signatures de tous les Report.wer extraits.

Corrélation avec la chronologie des runs terrain du 27/10/2026 :
  16:27:17 terrain.3/4?  16:52:17 terrain.5  17:43:38 terrain.6
  18:00:07 terrain.7     18:43:12 terrain.8  19:23:46 terrain.8 (relance)
"""
import datetime
import pathlib
import re

RACINE = pathlib.Path("/home/z/my-project/upload/wer_extract")

def filetime_a_date(ft):
    """FILETIME (100 ns depuis 1601-01-01) -> datetime UTC, arrondi à la seconde."""
    return datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=ft / 10)

print(f"{'rapport':58} {'date UTC':19} {'version':9} {'code':10} {'data':4}")
print("-" * 106)
for d in sorted(RACINE.iterdir()):
    f = d / "Report.wer"
    if not f.exists():
        continue
    brut = f.read_bytes().decode("utf-16-le", errors="replace")
    # champs
    def champ(nom):
        m = re.search(rf"^{nom}=(.*)$", brut, re.M)
        return m.group(1).strip() if m else "?"
    ev = champ("EventTime")
    try:
        date = filetime_a_date(int(ev)).strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        date = "?"
    app = champ("NsAppName") or "?"
    ver = re.search(r"Sig\[1\]\.Value=(.*)", brut)
    code = re.search(r"Sig\[7\]\.Value=(.*)", brut)
    data = re.search(r"Sig\[8\]\.Value=(.*)", brut)
    dv = data.group(1).strip() if data else "?"
    print(f"{app[:58]:58} {date:19} {ver.group(1)[:9] if ver else '?':9} "
          f"{code.group(1)[:10] if code else '?':10} {dv[-4:]:4}")
