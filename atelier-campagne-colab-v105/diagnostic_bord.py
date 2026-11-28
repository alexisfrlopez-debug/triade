#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE DIAGNOSTIC AU BORD : le runtime vit (bail renouvelé), le serving est
mort avec le notebook — la présente relance llama-server À LA MAIN (le binaire
prébâti et le GGUF caché y demeurent) et pose LES TROIS QUESTIONS au bord :
  1 · la RÉPONSE BRUTE de /completion à la sonde enrobée — la forme EXACTE
      (completion_probabilities ? probs ? la clé renommée à b12823 ?) ;
  2 · la TOKENIZATION des marqueurs spéciaux (l'enveloppe <|im_start|>… est-elle
      parsée en jetons SPÉCIAUX ou littéralisée en texte ?) ;
  3 · l'ESSAI PAR IDS (le prompt envoyé en tableau d'ids — le transport sans
      ambiguïté) ET l'offload GPU (-ngl 99 : combien de couches ?)."""
import importlib.util
import json
import pathlib
import uuid

spec = importlib.util.spec_from_file_location(
    "pilote", "/home/z/my-project/depot/atelier-pilote-campagne-v105/pilote_campagne_v105.py")
pilote = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pilote)

etat = json.loads(pathlib.Path("/home/z/my-project/work/v105-run/etat-enchaine.json").read_text())
creds = pilote.charge_jeton_colab()
client = pilote.Client(pilote.Prod(), pilote.session_autorisee(creds))
res = client.assign(uuid.UUID(etat["nbh"]), variant=pilote.Variant.GPU,
                    accelerator=pilote.Accelerator.T4)
print(f"[diagnostic] le runtime : {res.endpoint}")
porte = pilote.PorteFichiers(res.runtime_proxy_info.url, res.runtime_proxy_info.token)

DIAG = r'''
import json, os, pathlib, subprocess, time, urllib.request, urllib.error, glob, tarfile

# 0 · LES PIÈCES (idempotent : le runtime peut être neuf — le terrain du 28/11 :
#     recyclé toutes les 15-45 min, le diagnostic porte SES pièces)
DOS = pathlib.Path("/content/diag")
DOS.mkdir(exist_ok=True)
BIN_TAR = "https://github.com/ggml-org/llama.cpp/releases/download/b12823/llama-b12823-bin-ubuntu-cuda-12.8-x64.tar.gz"
LIB_TAR = "https://github.com/ggml-org/llama.cpp/releases/download/b12823/cudart-llama-b12823-bin-ubuntu-cuda-12.8-x64.tar.gz"
def tirer(url, nom):
    p = DOS / nom
    if not p.exists():
        print(f"[diag] tire {nom}…")
        urllib.request.urlretrieve(url, p)
    return p
bin_t, lib_t = tirer(BIN_TAR, "bin.tar.gz"), tirer(LIB_TAR, "lib.tar.gz")
if not (DOS / "bin").exists():
    with tarfile.open(bin_t) as t:
        t.extractall(DOS / "bin")
if not (DOS / "lib").exists():
    with tarfile.open(lib_t) as t:
        t.extractall(DOS / "lib")

# 1 · les pièces du bord : le binaire prébâti + le GGUF (hf_hub_download — le cache)
try:
    from huggingface_hub import hf_hub_download
    gguf = hf_hub_download(repo_id="bartowski/Qwen2.5-Coder-7B-Instruct-GGUF",
                           filename="Qwen2.5-Coder-7B-Instruct-Q6_K.gguf")
except Exception as e:
    print("[diag] le GGUF a manqué:", e.__class__.__name__, str(e)[:200])
    raise SystemExit("GGUF-ABSENT")
binaires = glob.glob(str(DOS / "bin" / "**" / "llama-server"), recursive=True)
print("[diag] binaires:", binaires)
print("[diag] gguf:", gguf)
if not binaires:
    raise SystemExit("PIÈCES-ABSENTES")
binaire, gguf = binaires[0], str(gguf)
dirs_cudart = [str(p) for p in (DOS / "lib").rglob("libcudart.so.12")]
lib_dir = str(pathlib.Path(dirs_cudart[0]).parent) if dirs_cudart else ""
env = dict(os.environ)
env["LD_LIBRARY_PATH"] = str(pathlib.Path(binaire).parent) + (":" + lib_dir if lib_dir else "")
print("[diag] LD_LIBRARY_PATH:", env["LD_LIBRARY_PATH"][:200])

# 2 · le serving relancé À LA MAIN (le journal au fichier)
log = open("/content/diag-serving.log", "w")
proc = subprocess.Popen(
    [binaire, "-m", gguf, "--host", "127.0.0.1", "--port", "8090",
     "-c", "8192", "-ngl", "99", "-v"],
    stdout=log, stderr=subprocess.STDOUT, env=env)
sain = False
for _ in range(90):
    time.sleep(2)
    if proc.poll() is not None:
        break
    try:
        with urllib.request.urlopen("http://127.0.0.1:8090/health", timeout=5) as r:
            if r.status == 200:
                sain = True
                break
    except Exception:
        pass
print("[diag] serving sain:", sain)
if not sain:
    print(open("/content/diag-serving.log").read()[-2500:])
    raise SystemExit("SERVING-MORT")
journal = open("/content/diag-serving.log").read()
for ligne in journal.splitlines():
    if "offload" in ligne.lower() or "offloaded" in ligne.lower() or "n_threads" in ligne:
        print("[diag·journal]", ligne[:160])

# 3 · la tokenization des marqueurs spéciaux
env_txt = "<|im_start|>user\nBonjour<|im_end|>\n<|im_start|>assistant\n"
req = urllib.request.Request("http://127.0.0.1:8090/tokenize",
    data=json.dumps({"content": env_txt}).encode(),
    headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=30) as r:
    toks = json.loads(r.read().decode())["tokens"]
print("[diag] la tokenization de l'enveloppe (10 premiers ids):", toks[:10])
req2 = urllib.request.Request("http://127.0.0.1:8090/tokenize",
    data=json.dumps({"content": env_txt, "add_special": True}).encode(),
    headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req2, timeout=30) as r:
    print("[diag] ids 151644 (im_start) présents ?", 151644 in toks)

# 4 · LA RÉPONSE BRUTE à la sonde enrobée (texte)
SONDE = ("LA SONDE DE PAROLE (le diagnostic de l'Entrée 451 : le prompt nu\\n"
         "contre le même enrobé de l'enveloppe de chat du modèle instruct).\\n"
         "Réponds STRICTEMENT en JSON, sans rien changer :\\n"
         '{"op": "editer", "dst": "loupe-07-cumul", "offset": 17, "src": "je 0x4997"}\\n'
         "LA RÉPONSE :")
prompt = "<|im_start|>user\n" + SONDE + "<|im_end|>\n<|im_start|>assistant\n"
corps = {"prompt": prompt, "n_predict": 4, "n_probs": 8, "temperature": 0.0,
         "cache_prompt": True, "return_tokens": True}
req = urllib.request.Request("http://127.0.0.1:8090/completion",
    data=json.dumps(corps).encode(), headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=300) as r:
        rep = json.loads(r.read().decode())
    print("[diag] LA RÉPONSE BRUTE (texte) — les clés:", sorted(rep.keys()))
    cp = rep.get("completion_probabilities")
    print("[diag] completion_probabilities:", json.dumps(cp)[:600] if cp is not None else "ABSENTES")
    print("[diag] content:", repr(rep.get("content", ""))[:200])
    print("[diag] stop type:", rep.get("stop_type"), "· stop:", repr(rep.get("stop"))[:80])
    print("[diag] tokens rendus:", rep.get("tokens", [])[:6])
except urllib.error.HTTPError as e:
    print("[diag] HTTP", e.code, e.read().decode()[:500])

# 5 · L'ESSAI PAR IDS (le prompt en tableau d'ids — l'ambiguïté abolie)
req = urllib.request.Request("http://127.0.0.1:8090/tokenize",
    data=json.dumps({"content": prompt}).encode(), headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=30) as r:
    ids = json.loads(r.read().decode())["tokens"]
corps2 = {"prompt": ids, "n_predict": 4, "n_probs": 8, "temperature": 0.0,
          "cache_prompt": True, "return_tokens": True}
req = urllib.request.Request("http://127.0.0.1:8090/completion",
    data=json.dumps(corps2).encode(), headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=300) as r:
        rep2 = json.loads(r.read().decode())
    print("[diag] LA RÉPONSE PAR IDS — content:", repr(rep2.get("content", ""))[:200])
    cp2 = rep2.get("completion_probabilities")
    print("[diag] par ids completion_probabilities:", json.dumps(cp2)[:400] if cp2 is not None else "ABSENTES")
except urllib.error.HTTPError as e:
    print("[diag] par ids HTTP", e.code, e.read().decode()[:300])

proc.terminate()
print("[diag] LE SERVING TUÉ — le diagnostic est clos.")
'''

from colab_cli.runtime import ColabRuntime
runtime = ColabRuntime(res.runtime_proxy_info.url, res.runtime_proxy_info.token)
try:
    sorties = runtime.execute_code(DIAG, timeout=600)
    for o in sorties:
        if o.get("output_type") == "stream":
            print("".join(o.get("text", [])))
        elif o.get("output_type") == "error":
            print(f"ERREUR: {o.get('ename')}: {o.get('evalue')}")
finally:
    try:
        runtime.stop(shutdown_kernel=True)
    except Exception:
        pass
