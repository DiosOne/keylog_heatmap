from datetime import datetime
from pathlib import Path

from heatmap.merge_sessions import merge_sessions
from heatmap.renderer import render

def next_output_path(base_dir: Path) -> Path:
    stamp= datetime.now().strftime('%Y%m%d')
    out_dir= base_dir / 'output_png'
    out_dir.mkdir(exist_ok=True)
    pattern= f'heatmap-{stamp}-*.png'
    
    max_idx= 0
    for fp in out_dir.glob(pattern):
        try:
            idx= int(fp.stem.rsplit("-", 1)[1])
            max_idx= max(max_idx, idx)
        except (IndexError, ValueError):
            continue
    
    next_idx= max_idx + 1
    return out_dir / f'heatmap-{stamp}-{next_idx:02d}.png'


def main() -> None:
    base_dir= Path(__file__).parent
    keymap_path= base_dir / 'heatmap' / 'keymap_104.json'
    keyfreq_path= base_dir / 'heatmap' / 'keyfreq.json'
    output_path= next_output_path(base_dir)
    
    merge_sessions()
    render(keymap_path, keyfreq_path, output_path)
    
if __name__ == '__main__':
    main()
