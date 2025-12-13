# Running venv on PowerShell

1. `python -m venv .venv`
2. `.\.venv\Scripts\Activate.ps1`
3. (first time) `python -m pip install --upgrade pip`
4. Install deps: `pip install pillow pynput`  # add `pyinstaller` later if packaging
5. If activation fails: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` (or `RemoteSigned` if you want it persistent)
6. Double-check: `where python` -> ...\keylog_heatmap\.venv\Scripts\python.exe
7. Cleanup/reset:
   - `deactivate`
  
   - ```ps
     Remove-Item -Recurse -Force .venv
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
