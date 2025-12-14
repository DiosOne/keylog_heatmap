# heatmap/merge_sessions.py
# Copyright (C) 2025 Dom Andrewartha
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
from collections import defaultdict
from pathlib import Path

from heatmap.utilities import load_json

SESSIONS_DIR= Path(__file__).parent/ 'sessions'
OUT_PATH= Path(__file__).parent/ 'keyfreq.json'

"""
Merge all session-*.json files in heatmap/sessions into heatmap/kryfreq.json.
Run directly or import/trigger from main.py
"""
def merge_sessions() -> None:
    """Accumulate counts across all session JSON files and write the combined keyfreq.json."""
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
    