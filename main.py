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

from datetime import datetime
from pathlib import Path
from shutil import copy2 

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
    
    # ensure keyfreq.json exists so renderer.py doesn't fail
    sample_freq= base_dir / 'heatmap' / 'keyfreq.sample.json'
    if not keyfreq_path.exists():
        if sample_freq.exists():
            copy2(sample_freq, keyfreq_path)
        else:
            keyfreq_path.write_text('{}\n', encoding='utf-8')
    
    merge_sessions()
    render(keymap_path, keyfreq_path, output_path)
    
if __name__ == '__main__':
    main()
