"""
StayType AI - Configuration Settings
"""

import os
from pathlib import Path

class Settings:
    APP_NAME: str = "StayType AI"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "NYC Airbnb Stay & Room Type Intelligent Prediction Engine"
    
    # Model configuration
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    MODEL_PATH: Path = BASE_DIR / "Model_Pipeline.pkl"
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

settings = Settings()
