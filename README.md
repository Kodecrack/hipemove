# HiperMove – AI movement coach
Browser-side pose tracking (MediaPipe Pose Landmarker, WASM/GPU) counts reps via joint-angle state machine,
live angle chart, and Gemma 4 (Gemini API) writes plain-language coaching from the measured data.

## Run
    pip install -r requirements.txt
    export GEMINI_API_KEY=your_key   # never commit this
    export GEMMA_MODEL=gemma-4-31b-it  # check exact id in AI Studio
    uvicorn server:app --port 8000
Open http://127.0.0.1:8000 (camera needs localhost or HTTPS).

## Deploy (DigitalOcean App Platform)
Push to GitHub, create App, run command `uvicorn server:app --host 0.0.0.0 --port 8080`, add GEMINI_API_KEY as an encrypted env var.

## Credits
MediaPipe Tasks Vision (Google, Apache-2.0), Gemma 4 via Gemini API, FastAPI. Rep logic, UI and coaching prompt written during the hackathon.

## Limits
Single person, side-on camera works best, approximate angles, wellness feedback only, not a replacement for a trainer.
