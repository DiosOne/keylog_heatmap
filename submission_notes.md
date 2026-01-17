# Submission Notes

- This repo includes a Dockerfile and .dockerignore to containerise the heatmap app.
- The container runs merge+render automatically (`python main.py`) in a dev environment.
- heatmap/keyfreq.sample.json provides a default dataset so the app runs on a clean checkout.
- The keylogger cannot capture keystrokes from inside the container, the container is used to merge session files and render the output_png.

## To run the app (container)

    - Build: `docker build -t keylog-heatmap:dev .`
    - Run: `docker run --rm -e APP_ENV=development -v %CD%/heatmap:/app/heatmap -v %CD%/output_png:/app/output_png keylog-heatmap:dev`

## To generate your own session files (host)

1. Create/activate a venv:
    - `python -m venv .venv`
    - `.\.venv\Scripts\Activate.ps1`
2. Install deps: `pip install pillow pynput`
3. Start logging: `python -m heatmap.logger` (press esc/break to stop)
4. Run the container to merge+render using your sessions:
    - `docker run --rm -e APP_ENV=development -v %CD%/heatmap:/app/heatmap -v %CD%/output_png:/app/output_png keylog-heatmap:dev`
