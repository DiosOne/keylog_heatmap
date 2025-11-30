# Keyboard Heatmap (104 ANSI)

I was interested in what keys I press the most now that I use the computer for more than games, so I thought about a heatmap/keylogger (nb: doesnt record the order, just frequency).  

This will generate a PNG heatmap of your most pressed keys using Pillow. The idea being you can customise your keyboards colours to highlight important keys if you wanted.  

Set up for a 104 ANSI as thats what I use..

## Files

- `keymap_104.json` - positions and sizes for every key.
- `keyfreq.json` - example frequencies (edit oe replace with your data if needed).
- `gradient.py` - Colours based on the Decepticon Devastator, these two in particular are the complementary colour scheme versions.
- `utilities.py` - JSON helpers and frequency normalisation.
- `renderer.py` - loads data, draws the keyboard, writes out the heatmap PNG.

## Usage

1. Install deps: `python -m pip install pillow`
2. Run: `python renderer.py`
3. Output: `heatmap.png` (~2400px wide) on a dark backround.

## Notes

- Layout and colours are JSON-driven; missing keys default to zero frequency.
- Rounded keycaps with outlines, high-contrast labels, and a min/max legend.
- Tweak `target_width` in `renderer.py` if you want a different resolution.

## Next Steps

- Turn into a stand alone exe.
- Store sessions of keylogging and combine them into one heatmap.
- Only generate heatmap on request by user.

Essentially, make it so you choose when to gather data so theres no contamination from non use cases. ie you work, game, and general internet on the same pc, but only want the data from work.

- Turn on, work, turn off. Data from that session is saved.
- At the end of the week/month (or however long you want) press a button to generate a heatmap of all the saved data.
