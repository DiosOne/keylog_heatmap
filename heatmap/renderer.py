# heatmap/renderer.py
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
from typing import Dict, List
from PIL import Image, ImageDraw, ImageFont
from heatmap.gradient import grad_colour
from heatmap.utilities import load_json, normalise_freqs, measure_layout

BG= (17, 17, 17)
OUTLINE= (200, 200, 200)
TEXT= (245, 245, 245)
LEGEND_TEXT= (220, 220, 220)

def round_rect(draw: ImageDraw.ImageDraw, xy, radius, fill, outline, width: int= 3):
    x0, y0, x1, y1= xy
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)
    
def draw_legend(draw: ImageDraw.ImageDraw, img_width: int, y: int, min_v: float, max_v: float, font, legend_w: int= 500, legend_h: int= 38):
    x0= (img_width - legend_w) //2
    x1= x0 + legend_w
    for i in range(legend_w):
        t= i / max(legend_w - 1, 1)
        colour= grad_colour(t)
        draw.line([(x0 + i, y), (x0 +i, y + legend_h)], fill=colour)
    draw.rectangle([x0, y, x1, y + legend_h], outline=OUTLINE, width=2)
    pad= 8
    draw.text((x0, y - legend_h - pad), f'Min: {min_v:.0f}', fill=LEGEND_TEXT, font=font)
    draw.text((x1 - 70, y -legend_h - pad), f'Max: {max_v:.0f}', fill=LEGEND_TEXT, font=font)
    
     
def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates= [
        Path(__file__).parent/ "trebuc.ttf",
        r"C:\Windows\Fonts\tahoma.ttf",
        r"C:\Windows\Fonts\verdana.ttf",
    ]
    for fp in candidates:
        try:
            return ImageFont.truetype(str(fp), size=size)
        except OSError:
            continue
    return ImageFont.load_default()

"""
Render a keyboard heatmap PNG from a key latout JSON and a key frequency JSON.
"""   
def render(keymap_path: Path, freq_path: Path, out_path: Path, target_width: int= 3200):
    """
    Load key layout and frequencies, normalise counts, draw keys and legend, and save the PNG.
    :param keymap_path: JSON with key positions/sizes/labels.
    :param freq_path: JSON with key frequencies (id->count).
    :param out_path: Destination PNG path.
    :param target_width: Desired image width. Height is computed in layout.
    """
    keys: List[Dict]= load_json(keymap_path)
    freqs_raw: Dict[str, float]= load_json(freq_path)
    
    freqs_norm, min_v, max_v= normalise_freqs(freqs_raw)
    
    max_x, max_y= measure_layout(keys)
    margin_units= 1.0
    legend_extra_units= 1.5
    unit_px= target_width/ (max_x + margin_units*2)
    keycap_radius= unit_px * 0.25
    padding_px= int(unit_px * margin_units)
    img_height= int((max_y + margin_units*2 + legend_extra_units) * unit_px)
    
    img= Image.new('RGB', (target_width, img_height), BG)
    draw= ImageDraw.Draw(img)
    font= load_font(max(24, int(unit_px * 0.4)))
    # font= load_font(max(30, int(unit_px * 1.0)))

    
    # frame
    draw.rounded_rectangle(
        [padding_px//2, padding_px//2, target_width - padding_px//2, img_height - padding_px//2],
        radius=int(unit_px * 0.4),
        outline=OUTLINE,
        width=3,
        fill=None,
    )
    
    # space around keys
    key_gap= unit_px * 0.06
    for key in keys:
        x= (key['x'] + margin_units) * unit_px + key_gap / 2
        y= (key['y'] + margin_units) * unit_px + key_gap / 2
        w= max(key.get('w', 1) * unit_px - key_gap, unit_px * 0.2)
        h= max(key.get('h', 1) * unit_px - key_gap, unit_px * 0.2)
        
        freq_norm= freqs_norm.get(key['id'], 0.0)
        fill= grad_colour(freq_norm)
        
        round_rect(draw, (x, y, x+w, y+h), radius=keycap_radius, fill=fill, outline=OUTLINE, width=3)
        freq_norm= pow(freq_norm, 0.5)
        fill= grad_colour(freq_norm)
        label= key.get('label', key['id'])
        bbox= draw.textbbox((0,0), label, font=font)
        tw= bbox[2] - bbox[0]
        th= bbox[3] - bbox[1]              
        draw.text((x + (w - tw) / 2, y + (h - th) / 2), label, fill=TEXT, font=font)
        
        
    legend_y= img_height - padding_px - 50        
    draw_legend(draw, target_width, legend_y, min_v, max_v, font)
    
    img.save(out_path)
    print(f'Saved {out_path} ({target_width} px wide)')
    
if __name__ == '__main__':
    base= Path(__file__).parent
    render(base / 'keymap_104.json', base / 'keyfreq.json', base / 'heatmap.png')
