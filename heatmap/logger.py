import json
import os
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Optional

SESSIONS_DIR= Path(__file__).parent / 'sessions'
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

# map the keyboard library names to match keymap_104
KEYBOARD_TO_KEYMAP= {
    "escape": "Esc", "esc": "Esc",
    "space": "Space",
    "enter": "Enter", "return": "Enter",
    "backspace": "Backspace",
    "tab": "Tab",
    "caps lock": "CapsLock",
    "shift": "Shift_L", "left shift": "Shift_L", "right shift": "Shift_R",
    "ctrl": "Control_L", "control": "Control_L", "left ctrl": "Control_L", "right ctrl": "Control_R",
    "alt": "Alt_L", "left alt": "Alt_L", "right alt": "Alt_R",
    "windows": "Meta_L", "left windows": "Meta_L", "right windows": "Meta_R",
    "menu": "ContextMenu",
    "up": "ArrowUp", "down": "ArrowDown", "left": "ArrowLeft", "right": "ArrowRight",
    "insert": "Insert", "delete": "Delete", "home": "Home", "end": "End",
    "page up": "PageUp", "page down": "PageDown",
    "print screen": "PrintScreen", "scroll lock": "ScrollLock", "pause": "Pause",
    "num lock": "NumLock",
    "divide": "NumpadSlash", "multiply": "NumpadAsterisk", "subtract": "NumpadMinus",
    "add": "NumpadPlus", "decimal": "NumpadDecimal",
    "num 0": "Numpad0", "num 1": "Numpad1", "num 2": "Numpad2", "num 3": "Numpad3",
    "num 4": "Numpad4", "num 5": "Numpad5", "num 6": "Numpad6",
    "num 7": "Numpad7", "num 8": "Numpad8", "num 9": "Numpad9",
    # F-keys
    **{f"f{i}": f"F{i}" for i in range(1, 13)},
    # Punctuation/top-row symbols
    "grave": "Backquote", "`": "Backquote",
    "minus": "Minus", "-": "Minus",
    "equal": "Equal", "=": "Equal",
    "left bracket": "BracketLeft", "[": "BracketLeft",
    "right bracket": "BracketRight", "]": "BracketRight",
    "backslash": "Backslash", "\\": "Backslash",
    "semicolon": "Semicolon", ";": "Semicolon",
    "apostrophe": "Quote", "'": "Quote",
    "comma": "Comma", ",": "Comma",
    "dot": "Period", "period": "Period", ".": "Period",
    "slash": "Slash", "/": "Slash",
}

def save_counts(counts: dict[str, int]) -> None:
    ts= datetime.now().strftime('%Y%m%d-%H%M%S')
    out_path= SESSIONS_DIR / f"session-{ts}.json"
    with out_path.open('w', encoding='utf-8') as f:
        json.dump(counts, f, indent=2)
    print(f"Saved session to {out_path}")
    
# pynput backend (Windows)
def run_pynput() -> dict[str, int]:
    from pynput import keyboard as pkb
    counts= defaultdict(int)
    stop_keys= {pkb.Key.esc, pkb.Key.pause}
    
    def to_key_id(k) -> Optional[str]:
        if isinstance(k, pkb.KeyCode):
            if k.char:
                ch= k.char
                if ch.isalpha():
                    return f"Key{ch.upper()}"
                if ch.isdigit():
                    return f"Digit{ch}"
                return KEYBOARD_TO_KEYMAP.get(ch)
            vk= getattr(k, 'vk', None)  
            if k.vk is not None:
                if vk is not None:
                    if 96 <= vk <= 105:
                        return f"Numpad{vk - 96}"
                    if vk == 110:
                        return 'NumpadDecimal'
                    if vk == 107:
                        return 'NumpadPlus'
                    if vk == 109:
                        return 'NumpadMinus'
                    if vk == 106:
                        return 'NumpadAsterisk'
                    if vk == 111:
                        return'NumpadSlash'
        if isinstance(k, pkb.Key):
            name= (k.name or "").replace("_", " ")           
            return KEYBOARD_TO_KEYMAP.get(name)
        return None
    
    def on_press(k):
        if isinstance(k, pkb.Key) and k in stop_keys:
            listener.stop()
            return
        key_id= to_key_id(k)
        if key_id:
            counts[key_id] += 1
            
    print('Logging keys (pynput)... Press Esc/Break to stop and save session.')
    with pkb.Listener(on_press=on_press) as listener:
        listener.join()
            
    return dict(counts)

# removed to focus on windows return once functional

# # keyboard backend - needs sudo on Linux
# def run_keyboard() -> dict[str, int]:
#     import keyboard as kbd
#     counts= defaultdict(int)
    
#     def to_key_id(name:str) -> Optional[str]:
#         n= name.lower()
#         if len(n) == 1 and n.isalpha():
#             return f"Key{n.upper()}"
#         if len(n) == 1 and n.isdigit():
#             return f"Digit{n}"
#         return KEYBOARD_TO_KEYMAP.get(n)
    
#     def on_event(event):
#         if event.event_type != 'down':
#             return
#         key_id= to_key_id(event.name)
#         if key_id:
#             counts[key_id] += 1
            
#     print('Logging keys (keyboard)... Press Ctrl+C to stop and save session.')
#     kbd.hook(on_event)
#     try:
#         kbd.wait()
#     except KeyboardInterrupt:
#         pass
    
#     return dict(counts)
        
def is_wayland() -> bool:
    return os.environ.get('XDG_SESSION_TYPE', "").lower() == 'wayland'

if __name__ == '__main__':
    if not sys.platform.startswith('win'):
        print('This logger path is windows only. Exiting.')
        sys.exit(0)
        
    counts: dict[str, int] = {}
    try:
        counts= run_pynput()
    except Exception as e:
        print(f"pynput backend failed({e!r}); no Windows fallback in this build.")
          
    if counts:
        save_counts(counts)
    else:
        print('No keypresses captured on Windows.')
