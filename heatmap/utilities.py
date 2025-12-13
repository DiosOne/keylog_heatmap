import json
from pathlib import Path
from typing import Dict, List, Tuple

def load_json(path: Path):
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)
    
def normalise_freqs(freqs: Dict[str, float]) -> Tuple[Dict[str, float], float, float]:
    values= list(freqs.values()) or [0.0]
    min_v= 0.0
    max_v= max(values + [0.0])
    span= max(max_v - min_v, 1e-6)
    normalised= {k: (v - min_v) / span for k, v in freqs.items()}
    return normalised, min_v, max_v

def measure_layout(keys: List[dict]) -> Tuple[float, float]:
    max_x= max((k['x'] + k.get('w', 1)) for k in keys)
    max_y= max((k['y'] + k.get('h', 1)) for k in keys)
    return max_x, max_y
