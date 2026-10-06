"""
StayType AI - FastAPI Application Server
"""

import logging
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.data_mapping import (
    BOROUGH_NEIGHBORHOOD_MAP,
    PRESET_LISTINGS,
    BOROUGH_DEFAULT_COORDS
)
from app.model import get_model
from app.schemas import (
    ListingInput,
    PredictionResponse,
    HealthResponse,
    MetadataResponse
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("staytype-app")

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Warm up the model during startup."""
    logger.info("Initializing StayType AI ML Pipeline...")
    model = get_model()
    if model.is_loaded:
        logger.info(f"Model initialized with classes: {model.classes}")
    else:
        logger.error("Model pipeline could not be loaded!")
    yield
    logger.info("Shutting down StayType AI server...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Jinja2 Templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    """Serve the modern interactive UI dashboard."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "description": settings.APP_DESCRIPTION,
        }
    )

@app.post("/api/predict", response_model=PredictionResponse)
async def predict_stay_type(payload: ListingInput):
    """
    Predict the Airbnb stay/room type (Entire home/apt, Private room, Shared room)
    given listing characteristics and location.
    """
    try:
        model = get_model()
        result = model.predict(payload)
        return result
    except Exception as e:
        logger.exception(f"Inference error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Inference error: {str(e)}"
        )

@app.get("/api/metadata", response_model=MetadataResponse)
async def get_metadata():
    """
    Returns the complete list of NYC boroughs, mapped neighborhoods,
    and demo presets.
    """
    total_nh = sum(len(v) for v in BOROUGH_NEIGHBORHOOD_MAP.values())
    return MetadataResponse(
        boroughs=list(BOROUGH_NEIGHBORHOOD_MAP.keys()),
        neighborhoods=BOROUGH_NEIGHBORHOOD_MAP,
        presets=PRESET_LISTINGS,
        total_neighborhoods=total_nh
    )

@app.get("/api/presets")
async def get_presets():
    """Returns demo listing presets for 1-click testing."""
    return {"presets": PRESET_LISTINGS}

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """System and model health check endpoint."""
    model = get_model()
    return HealthResponse(
        status="healthy" if model.is_loaded else "degraded",
        app=settings.APP_NAME,
        version=settings.APP_VERSION,
        model_loaded=model.is_loaded,
        model_classes=model.classes,
        sklearn_version=model.sklearn_version
    )
