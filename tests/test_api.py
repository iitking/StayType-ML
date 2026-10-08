"""
StayType AI - API & Inference Test Suite
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True
    assert set(data["model_classes"]) == {"Entire home/apt", "Private room", "Shared room"}

def test_metadata_endpoint(client):
    response = client.get("/api/metadata")
    assert response.status_code == 200
    data = response.json()
    assert "boroughs" in data
    assert len(data["boroughs"]) == 5
    assert set(data["boroughs"]) == {"Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"}
    assert data["total_neighborhoods"] == 217
    assert len(data["presets"]) >= 4

def test_presets_endpoint(client):
    response = client.get("/api/presets")
    assert response.status_code == 200
    data = response.json()
    assert "presets" in data
    assert len(data["presets"]) >= 4

def test_home_page_renders_html(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "StayType" in response.text
    assert "Listing Feature Studio" in response.text
    assert "Classified Stay Type" in response.text

def test_predict_entire_home(client):
    payload = {
        "neighbourhood_group": "Manhattan",
        "neighbourhood": "Midtown",
        "latitude": 40.7549,
        "longitude": -73.9840,
        "price": 350.0,
        "minimum_nights": 3,
        "number_of_reviews": 48,
        "reviews_per_month": 2.15,
        "calculated_host_listings_count": 2,
        "availability_365": 240
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_stay_type"] in ["Entire home/apt", "Private room", "Shared room"]
    assert "confidence" in data
    assert "confidence_percentage" in data
    assert "probabilities" in data
    assert len(data["probabilities"]) == 3
    assert "Entire home/apt" in data["probabilities"]
    assert "insights" in data
    assert len(data["insights"]) >= 1

def test_predict_private_room(client):
    payload = {
        "neighbourhood_group": "Brooklyn",
        "neighbourhood": "Williamsburg",
        "latitude": 40.7081,
        "longitude": -73.9571,
        "price": 75.0,
        "minimum_nights": 2,
        "number_of_reviews": 65,
        "reviews_per_month": 3.40,
        "calculated_host_listings_count": 1,
        "availability_365": 120
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_stay_type"] in ["Entire home/apt", "Private room", "Shared room"]
    assert data["probabilities"]["Private room"] > 0

def test_predict_validation_error(client):
    # Missing required fields and negative price
    payload = {
        "neighbourhood_group": "Manhattan",
        "price": -50.0
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 422
