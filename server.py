import os, httpx
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="HiperMove")
KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL = os.environ.get("GEMMA_MODEL", "gemma-4-31b-it")

class Rep(BaseModel):
    min: int
    dur: float
    form: int = 0
    d: int = 0
    q: int = 0
    tip: str = ""

class Session(BaseModel):
    exercise: str
    reps: list[Rep]

@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/api/coach")
async def coach(s: Session):
    lines = "\n".join(
        f"Rep {i+1}: lowest joint angle {r.min} deg, form {r.form}% (range {r.d}%, posture {r.q}%), {r.dur}s, note: {r.tip}"
        for i, r in enumerate(s.reps))
    avg = round(sum(r.form for r in s.reps) / max(1, len(s.reps)))
    prompt = (
        f"You are a friendly, precise fitness coach. The user did a set of {len(s.reps)} {s.exercise} reps. "
        f"Pose estimation measured each rep (form score = how close to ideal technique):\n{lines}\n"
        f"Average form {avg}% (so about {100-avg}% error).\n"
        "Reply in EXACTLY three plain-text lines, no markdown, each under 22 words:\n"
        "WELL: one thing done well\n"
        "FIX: the main technique error with its approximate error percentage, and whether form faded with fatigue\n"
        "TIP: one concrete cue for the next set\n"
        "Wellness feedback only. No medical advice or diagnosis."
    )
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.post(url, headers={"x-goog-api-key": KEY},
                             json={"contents": [{"parts": [{"text": prompt}]}]})
            r.raise_for_status()
            return {"text": r.json()["candidates"][0]["content"]["parts"][0]["text"]}
    except Exception as e:
        return {"error": f"Gemma call failed: {e}"}
