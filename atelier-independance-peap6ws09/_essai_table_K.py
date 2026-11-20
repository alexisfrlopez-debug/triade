import io, json, contextlib, sys
sys.path.insert(0, '/home/z/my-project/triade/atelier-independance-peap6ws09')
with contextlib.redirect_stdout(io.StringIO()):
    from derivation_table_K_qwen import table_K
print(json.dumps(list(table_K())))
