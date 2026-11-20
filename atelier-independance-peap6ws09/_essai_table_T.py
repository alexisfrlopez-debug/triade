import json, sys
sys.path.insert(0, '/home/z/my-project/triade/atelier-independance-peap6ws09')
from derivation_table_T_qwen import table_T
print(json.dumps(list(table_T())))
