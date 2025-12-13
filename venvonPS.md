# running venv on powershell

1. `python -m venv .venv`
2. `.\.venv\Scripts\Activate.ps1`
3. (do this the first time) `python -m pip install --upgrade pip`
4. install deps - `pip install pillow matplotlib pynput`

5. if fails - `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

6. Double check - `where python` -> ...\keylog_heatmap\.venv\Scripts\python.exe

7. cleanup

    `Deactivate`

    ```PS
    Remove-Item -Recurse -Force .venv
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
