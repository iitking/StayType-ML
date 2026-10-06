"""
StayType AI - Pydantic Request & Response Schemas
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class ListingInput(BaseModel):
    neighbourhood_group: str = Field(
        ...,
        description="Borough in NYC (e.g., Manhattan, Brooklyn, Queens, Bronx, Staten Island)",
        examples=["Manhattan"]
    )
    neighbourhood: str = Field(
        ...,
        description="Specific neighborhood within the borough",
        examples=["Midtown"]
    )
    latitude: float = Field(
        40.7580,
        ge=40.45,
        le=41.05,
        description="Listing Latitude coordinates (NYC range: 40.45 to 41.05)",
        examples=[40.7580]
    )
    longitude: float = Field(
        -73.9855,
        ge=-74.30,
        le=-73.65,
        description="Listing Longitude coordinates (NYC range: -74.30 to -73.65)",
        examples=[-73.9855]
    )
    price: float = Field(
        150.0,
        ge=0.0,
        description="Nightly listing price in USD ($)",
        examples=[150.0]
    )
    minimum_nights: int = Field(
        2,
        ge=1,
        le=365,
        description="Minimum number of stay nights required",
        examples=[2]
    )
    number_of_reviews: int = Field(
        15,
        ge=0,
        description="Total cumulative guest reviews",
        examples=[15]
    )
    reviews_per_month: float = Field(
        1.25,
        ge=0.0,
        description="Average number of reviews per month",
        examples=[1.25]
    )
    calculated_host_listings_count: int = Field(
        1,
        ge=1,
        description="Number of listings this host maintains on Airbnb",
        examples=[1]
    )
    availability_365: int = Field(
        180,
        ge=0,
        le=365,
        description="Number of available days per year (0-365)",
        examples=[180]
    )

class StayTypeDetail(BaseModel):
    title: str
    icon: str
    color: str
    bg_class: str
    description: str
    best_for: str

class PredictionResponse(BaseModel):
    predicted_stay_type: str
    confidence: float
    confidence_percentage: str
    probabilities: Dict[str, float]
    details: StayTypeDetail
    insights: List[str]
    input_received: Dict

class HealthResponse(BaseModel):
    status: str
    app: str
    version: str
    model_loaded: bool
    model_classes: List[str]
    sklearn_version: str

class MetadataResponse(BaseModel):
    boroughs: List[str]
    neighborhoods: Dict[str, List[str]]
    presets: List[Dict]
    total_neighborhoods: int
