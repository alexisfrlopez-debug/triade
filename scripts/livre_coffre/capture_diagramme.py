#!/usr/bin/env python3
"""TRIADE — capture du diagramme chaîne CF en PNG @2× (300 dpi équivalent).

Scénario B chemin B du brief académique : diagramme complexe (>6 nœuds)
rendu par Playwright+CSS puis embarqué par \\includegraphics. La capture
d'élément (page.screenshot) est la voie prévue pour les FIGURES — la règle
« pas de script Playwright manuel » ne vise que les page.pdf() documents.
"""
import sys
from playwright.sync_api import sync_playwright

HTML, PNG = sys.argv[1], sys.argv[2]

with sync_playwright() as p:
    nav = p.chromium.launch()
    page = nav.new_page(device_scale_factor=2, viewport={"width": 1200, "height": 900})
    page.goto("file://" + HTML)
    page.wait_for_timeout(400)
    elt = page.query_selector(".canvas")
    elt.screenshot(path=PNG)
    nav.close()
print("PNG écrit :", PNG)
