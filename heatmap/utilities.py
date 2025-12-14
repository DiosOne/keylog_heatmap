# heatmap/utilites.py
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
from pathlib import Path
from typing import Dict, List, Tuple
import math

def load_json(path: Path):
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)
    
def normalise_freqs(freqs: Dict[str, float]) -> Tuple[Dict[str, float], float, float]:
    values= list(freqs.values()) or [0.0]
    log_vals= [math.log1p(v) for v in values]
    min_v, max_v= min(log_vals), max(log_vals)
    span= max(max_v - min_v, 1e-6)
    normalised= {k: (math.log1p(v) - min_v) / span for k, v in freqs.items()}
    return normalised, min(values), max(values)

def measure_layout(keys: List[dict]) -> Tuple[float, float]:
    max_x= max((k['x'] + k.get('w', 1)) for k in keys)
    max_y= max((k['y'] + k.get('h', 1)) for k in keys)
    return max_x, max_y
