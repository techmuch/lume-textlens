from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import time

from src.processor import TextProcessor

app = FastAPI(title="Lume / TextLens API")

# Add CORS middleware for demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    text: str
    policy: str = "no-phi"

class Violation(BaseModel):
    type: str
    match: str
    start: int
    end: int
    reason: str

class AnalyzeResponse(BaseModel):
    has_violation: bool
    violations: list[Violation]
    score: float
    suggestions: list[str]
    inference_time_ms: float

# Serve static files for the UI
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(request: AnalyzeRequest):
    start_time = time.perf_counter()
    
    processor = TextProcessor(policy=request.policy)
    result = processor.analyze(request.text)
    
    end_time = time.perf_counter()
    inference_time_ms = (end_time - start_time) * 1000
    
    return {
        **result,
        "inference_time_ms": round(inference_time_ms, 2)
    }

@app.get("/")
async def root():
    return {"message": "Welcome to Lume / TextLens API. Visit /static/index.html for the UI."}
