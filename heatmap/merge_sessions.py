import json
from collections import defaultdict
from pathlib import Path

from heatmap.utilities import load_json

SESSIONS_DIR= Path(__file__).parent/ 'sessions'
OUT_PATH= Path(__file__).parent/ 'keyfreq.json'

def merge_sessions() -> None:
    totals= defaultdict(int)
    files= sorted(SESSIONS_DIR.glob('session-*.json'))
    if not files:
        print('No sessions files found in sessions folder')
        return
    for fp in files:
        data= load_json(fp)
        for k, v in data.items():
            totals[k] += int(v)
    if not totals:
        print('Session files contained no counts. Skipping write to keyfreq')
        return
    with OUT_PATH.open('w', encoding='utf-8') as f:
        json.dump(totals, f, indent=2)
    print(f"Merged {len(files)} session(s) --> {OUT_PATH}")
    
if __name__== '__main__':
    merge_sessions()
    