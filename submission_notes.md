# Submission Notes

- This repo includes a Dockerfile and .dockerignore to containerise the heatmap app.
- The container runs merge+render automatically (`python main.py`) in a dev environment.
- heatmap/keyfreq.sample.json provides a default dataset so the app runs on a clean checkout.
- The keylogger cannot capture keystrokes from inside the container, the container is used to merge session files and render the output_png.

## To run the app (container)

    Build: docker build -t keylog_heatmap:dev-<gitsha> \
                --build-arg APP_ENV=development \
                --build-arg APP_VERSION=0.1.0 \
                --build-arg GIT_SHA=<gitsha> .

    Naming/Tagging:
    - Format: keylog_heatmap:<env>-<gitsha>
    - Example: keylog_heatmap:dev-abcd123

    Run: docker run --rm -e APP_ENV=development -v %CD%/heatmap:/app/heatmap -v %CD%/output_png:/app/output_png keylog_heatmap:dev
<!-- I had to format it like this, instead of a normal list, as vsc was giving me a linting error with the <> around gitsha. It thinks it's an inline link -->

## To generate your own session files (host)

1. Create/activate a venv:
    - `python -m venv .venv`
    - `.\.venv\Scripts\Activate.ps1`
2. Install deps: `pip install pillow pynput`
3. Start logging: `python -m heatmap.logger` (press esc/break to stop)
4. Run the container to merge+render using your sessions:
    - `docker run --rm -e APP_ENV=development -v %CD%/heatmap:/app/heatmap -v %CD%/output_png:/app/output_png keylog_heatmap:dev`
