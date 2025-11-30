import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Optional

from pynput import keyboard

SESSIONS_DIR= Path(__file__).parent / 'sessions'
SESSIONS_DIR.mkdir(exist_ok=True)

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

def to_key_id(k) -> Optional[str]:
    # character keys
    if isinstance(k, keyboard.KeyCode) and k.char:
        ch= k.char
        if ch.isalpha():
            return f"Key{ch.upper()}"
        if ch.isdigit():
            return f"Digit{ch}"
        return KEYBOARD_TO_KEYMAP.get(ch)
    # special keys
    if isinstance(k, keyboard.Key):
        # standardise naming from pynput to match keymap
        name= k.name or ""
        name= name.replace("_", " ")
        return KEYBOARD_TO_KEYMAP.get(name)
    return None

def run_session():
    counts= defaultdict(int)
    
    def on_press(k):
        key_id= to_key_id(k)
        if key_id:
            counts[key_id] += 1
        
    print('Logging keys... Press Ctrl+C to stop and save session.')
    with keyboard.Listener(on_press=on_press) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            listener.stop()
    
    ts= datetime.now().strftime('%Y%m%d-%H%M%S')
    out_path= SESSIONS_DIR / f"session-{ts}.json"
    with out_path.open('w', encoding='utf-8') as f:
        json.dump(counts, f, indent=2)
    print(f"Saved session to {out_path}")
    
if __name__== "__main__":
    run_session()