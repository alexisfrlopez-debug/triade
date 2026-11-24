#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nettoyage du coffre TRIADE (25/11/2026) — déplacements vérifiés vers /ARCHIVE.
Doctrine D143/D76 : RIEN n'est jeté, chaque pièce est DÉPLACÉE (mêmes
identifiants, mêmes octets), chaque déplacement recoupé par md5 avant/après.

Usage : python3 nettoyer_coffre.py <racine|livrables|test|creer-dossiers|journal>
Le journal local scripts/journal_nettoyage.json trace chaque geste.
"""
import json, sys, time, urllib.request, urllib.parse

TOK = json.load(open('/home/z/my-project/work/tokens/access_token.json'))['access_token']
RACINE = '105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp'
LIVRABLES = '1wF0p0g-OPdnL7fgnNsJb6D1rXhtyHqIZ'
TEST = '1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0'
ARCHIVE = '1uJ5yU7ma5dYQM1GuWzm9Fx1I1U3Ywepr'
FOLDER_MIME = 'application/vnd.google-apps.folder'
JOURNAL = '/home/z/my-project/scripts/journal_nettoyage.json'

# Sous-dossiers de destination (créés dans /ARCHIVE)
DEST_RACINE = 'supersede-racine-20261125'
DEST_LIVRABLES = 'livrables_supersedes_20261125'
DEST_TEST = 'test-ateliers-20261125'


def api(method, url, body=None, essais=3):
    """Appel API Drive avec retries."""
    for i in range(essais):
        try:
            data = json.dumps(body).encode() if body is not None else None
            req = urllib.request.Request(url, data=data, method=method)
            req.add_header('Authorization', 'Bearer ' + TOK)
            req.add_header('Content-Type', 'application/json')
            with urllib.request.urlopen(req) as r:
                return r.status, json.loads(r.read() or b'{}')
        except urllib.error.HTTPError as e:
            corps = e.read().decode('utf-8', 'replace')
            if e.code in (500, 502, 503, 429) and i < essais - 1:
                time.sleep(2 * (i + 1))
                continue
            raise RuntimeError('HTTP %d : %s' % (e.code, corps[:300]))
        except urllib.error.URLError:
            if i < essais - 1:
                time.sleep(2 * (i + 1))
                continue
            raise
    raise RuntimeError('impossible')


def lister(fid):
    """Liste un dossier -> {nom: [fichiers]} (plusieurs fichiers de meme nom possibles)."""
    entrees, page = [], None
    while True:
        params = {'q': "'%s' in parents and trashed = false" % fid,
                  'fields': 'nextPageToken, files(id, name, mimeType, size, md5Checksum, modifiedTime)',
                  'pageSize': 100}
        if page:
            params['pageToken'] = page
        st, d = api('GET', 'https://www.googleapis.com/drive/v3/files?' + urllib.parse.urlencode(params))
        entrees.extend(d.get('files', []))
        page = d.get('nextPageToken')
        if not page:
            break
    return entrees


def trouver_ou_creer(parent_id, nom):
    ent = lister(parent_id)
    for f in ent:
        if f['name'] == nom and f['mimeType'] == FOLDER_MIME:
            return f['id'], False
    st, d = api('POST', 'https://www.googleapis.com/drive/v3/files',
                {'name': nom, 'mimeType': FOLDER_MIME, 'parents': [parent_id]})
    return d['id'], True


def deplacer(f, dest_id, src_nom):
    """Déplace f vers dest_id et recoupe le md5. Retourne (ok, detail)."""
    fid, nom, md5_avant = f['id'], f['name'], f.get('md5Checksum', '')
    url = ('https://www.googleapis.com/drive/v3/files/%s?addParents=%s&removeParents=%s'
           % (fid, dest_id, src_nom))
    st, _ = api('PATCH', url, {})
    # recoupement : parents + md5
    st, meta = api('GET', 'https://www.googleapis.com/drive/v3/files/%s?fields=md5Checksum,parents,name' % fid)
    ok_parents = dest_id in meta.get('parents', [])
    ok_md5 = (meta.get('md5Checksum', '') == md5_avant) if md5_avant else True
    ok = ok_parents and ok_md5 and meta.get('name') == nom
    return ok, {'id': fid, 'nom': nom, 'md5': md5_avant, 'parents_ok': ok_parents, 'md5_ok': ok_md5}


def journaliser(geste):
    try:
        j = json.load(open(JOURNAL))
    except Exception:
        j = []
    j.append(geste)
    json.dump(j, open(JOURNAL, 'w'), ensure_ascii=False, indent=1)


# ---------------------------------------------------------------- listes

# Racine : noms a archiver INTEGRALEMENT
RACINE_ARCHIVE = [
    'TRIADE_complet_v0.23.3.zip', 'TRIADE_complet_v0.24.0.zip',
    'empreintes_livrables_v0.23.3.txt', 'rapport_verification_v0.23.3.txt',
    'rapport-release-v0234-20261123.txt', 'rapport-release-v0240-20261124.txt',
    'RAPPORT-89488hblm.txt', 'RAPPORT-fkkqc7v8t.txt', 'RAPPORT-M4-vljfs6pcj.txt',
    'rapport-execution-vague6.txt', 'CHANTIER-OPTIMISATION-TOKENS-v1.md',
    'JOURNAL-OPTIMISATION-TOKENS.txt',
]
# Racine : doublons -> garder le plus recent, archiver les autres
RACINE_DOUBLONS_GARDER_RECENT = ['OU-TROUVER-LES-LIVRABLES.md', 'REPRISE_PROJET.md']
# Racine : ce qui DOIT demeurer (controle de cohérence finale)
RACINE_DEMEURE = {
    'worklog.md', 'OU-TROUVER-LES-LIVRABLES.md', 'REPRISE_PROJET.md',
    'PROTOCOLE_TRIADE_AGENT.md', 'LISEZMOI-PHRASE-CONTROLE.txt', 'coffre_fort.bin',
    'TRIADE-continuite-multiprofils-0.9.0-20261105T115943Z.bin',
    'manifeste-p3-20261125.txt', 'rapport-execution-p3-20261125.txt',
    'tableau-p3-harnais-image-20261125.txt',
    'ARCHIVE', 'Cérémonie', 'instructions', 'livrables', 'test', 'Tokens',
    'TRIADE-sauvegarde-git', 'OU-TROUVER-LES-LIVRABLES', 'LISEZMOI-NETTOYAGE-20261125.txt',
}

# /livrables : le set courant v0.31.0 + kits terrain + kit dev v1.3.0 + participer v1.1.0
LIVRABLES_DEMEURE = {
    'empreintes_livrables_v0.31.0.txt', 'LISEZMOI-livrables-v0.31.0.txt',
    'LISEZMOI-KITS-TERRAIN-2026-11-24.txt',
    'Livre_du_Coffre_TRIADE_CF1-CF3_v1.15.pdf',
    'Protocole_TRIADE_v0.15.16_Specification.pdf',
    'rapport_verification_v0.31.0.txt', 'TRIADE_complet_v0.31.0.zip',
    'TRIADE_kit_developpement_v1.3.0.zip', 'TRIADE_kits_terrain_Windows_v0150.zip',
    'TRIADE_manuscrit_v0.31.0.pdf', 'TRIADE_participer_v1.1.0.zip',
    'TRIADE_presentation_v0.31.0.zip', 'TRIADE_presentation_v0310.pdf',
    'TRIADE_preuves_et_calculs_v0.31.0.pdf', 'TRIADE_soumission_v0.31.0.zip',
}

# /test : rendu P3 + les deux archives de campagne (referencees par les scripts d'archivage de runs)
TEST_DEMEURE = {
    'manifeste-p3-20261125.txt', 'rapport-execution-p3-20261125.txt',
    'tableau-p3-harnais-image-20261125.txt',
    'archives-livraisons', 'archives-preuves',
    'LISEZMOI-TEST-20261125.txt',
}


# ---------------------------------------------------------------- commandes

def cmd_creer_dossiers():
    for nom in (DEST_RACINE, DEST_LIVRABLES, DEST_TEST):
        fid, cree = trouver_ou_creer(ARCHIVE, nom)
        print('%s : %s%s' % (nom, fid, ' (CRÉÉ)' if cree else ' (existant)'))


def cmd_racine():
    dest_id, _ = trouver_ou_creer(ARCHIVE, DEST_RACINE)
    ent = lister(RACINE)
    a_bouger = []
    for f in ent:
        if f['name'] in RACINE_ARCHIVE:
            a_bouger.append(f)
    for nom in RACINE_DOUBLONS_GARDER_RECENT:
        memes = sorted([f for f in ent if f['name'] == nom], key=lambda x: x.get('modifiedTime', ''))
        for vieux in memes[:-1]:          # tous sauf le plus récent
            a_bouger.append(vieux)
    print('À archiver depuis la racine : %d' % len(a_bouger))
    for f in a_bouger:
        print('  -', f['name'], f.get('size', '?'), f.get('modifiedTime', '?')[:16])
    bouger(a_bouger, dest_id, RACINE, 'racine')
    # contrôle de cohérence : que reste-t-il ?
    reste = lister(RACINE)
    inattendus = [f['name'] for f in reste if f['name'] not in RACINE_DEMEURE]
    print('Racine après : %d éléments. Inattendus : %s' % (len(reste), inattendus or 'aucun'))


def cmd_livrables():
    dest_id, _ = trouver_ou_creer(ARCHIVE, DEST_LIVRABLES)
    ent = lister(LIVRABLES)
    a_bouger = [f for f in ent if f['name'] not in LIVRABLES_DEMEURE]
    print('À archiver depuis /livrables : %d (demeurent %d)' % (len(a_bouger), len(ent) - len(a_bouger)))
    for f in a_bouger:
        print('  -', f['name'])
    bouger(a_bouger, dest_id, LIVRABLES, 'livrables')
    reste = lister(LIVRABLES)
    manquants = LIVRABLES_DEMEURE - {f['name'] for f in reste}
    print('Livrables après : %d éléments. Courants manquants : %s' % (len(reste), manquants or 'aucun'))


def cmd_test():
    dest_id, _ = trouver_ou_creer(ARCHIVE, DEST_TEST)
    ent = lister(TEST)
    a_bouger = [f for f in ent if f['name'] not in TEST_DEMEURE]
    print('À archiver depuis /test : %d (demeurent %d)' % (len(a_bouger), len(ent) - len(a_bouger)))
    for f in a_bouger:
        print('  -', f['name'])
    bouger(a_bouger, dest_id, TEST, 'test')
    reste = lister(TEST)
    manquants = TEST_DEMEURE - {f['name'] for f in reste}
    print('Test après : %d éléments. Attendus manquants : %s' % (len(reste), manquants or 'aucun'))


def bouger(fichiers, dest_id, src_id, etiquette):
    ok_n, ko = 0, []
    for i, f in enumerate(fichiers, 1):
        try:
            ok, detail = deplacer(f, dest_id, src_id)
        except Exception as e:
            ok, detail = False, {'erreur': str(e)[:200]}
        if ok:
            ok_n += 1
        else:
            ko.append((f['name'], detail))
        journaliser({'source': etiquette, 'nom': f['name'], 'id': f['id'],
                     'md5': f.get('md5Checksum', ''), 'ok': ok, 'detail': detail,
                     'dest': dest_id, 'heure': time.strftime('%H:%M:%S')})
        if i % 20 == 0:
            print('  ... %d/%d' % (i, len(fichiers)))
    print('DÉPLACÉS VERT : %d/%d' % (ok_n, len(fichiers)))
    if ko:
        print('ROUGES :')
        for nom, d in ko:
            print('  !', nom, json.dumps(d)[:200])
    return ok_n, len(fichiers)


def cmd_verifier():
    """Recoupe le journal : chaque entree doit avoir son fichier au bon parent, md5 inchangé."""
    j = json.load(open(JOURNAL))
    dests = {DEST_RACINE: 'supersede-racine', DEST_LIVRABLES: 'livrables_supersedes', DEST_TEST: 'test-ateliers'}
    vert, rouge = 0, []
    vus = {}
    for e in j:
        fid, md5j = e['id'], e['md5']
        if fid in vus:
            continue
        vus[fid] = True
        try:
            st, meta = api('GET', 'https://www.googleapis.com/drive/v3/files/%s?fields=md5Checksum,parents,name' % fid)
            ok_p = e['dest'] in meta.get('parents', [])
            ok_m = (meta.get('md5Checksum', '') == md5j) if md5j else True
            ok_n = meta.get('name') == e['nom']
            if ok_p and ok_m and ok_n:
                vert += 1
            else:
                rouge.append((e['nom'], ok_p, ok_m, ok_n))
        except Exception as ex:
            rouge.append((e['nom'], str(ex)[:120]))
    print('VÉRIFICATION : %d VERT / %d entrées uniques' % (vert, len(vus)))
    for r in rouge:
        print('  ROUGE :', r)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    {'creer-dossiers': cmd_creer_dossiers, 'racine': cmd_racine,
     'livrables': cmd_livrables, 'test': cmd_test,
     'verifier': cmd_verifier}.get(cmd, lambda: print(__doc__))()
