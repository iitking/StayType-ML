"""
StayType AI - Model Inference Engine
"""

import logging
from typing import Dict, List, Tuple
import joblib
import pandas as pd
import sklearn

from app.config import settings
from app.data_mapping import STAY_TYPE_DETAILS, BOROUGH_NEIGHBORHOOD_MAP
from app.schemas import ListingInput, PredictionResponse, StayTypeDetail

logger = logging.getLogger(__name__)

# Typical NYC median prices per borough from Airbnb NYC 2019 dataset
BOROUGH_MEDIAN_PRICE = {
    "Manhattan": 150.0,
    "Brooklyn": 90.0,
    "Queens": 75.0,
    "Staten Island": 75.0,
    "Bronx": 65.0
}

class StayTypeModel:
    _instance = None
    _pipeline = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StayTypeModel, cls).__new__(cls)
            cls._instance._load_model()
        return cls._instance

    def _load_model(self):
        """Load trained scikit-learn pipeline from pickle file."""
        try:
            logger.info(f"Loading Model Pipeline from: {settings.MODEL_PATH}")
            self._pipeline = joblib.load(settings.MODEL_PATH)
            logger.info("Model Pipeline successfully loaded.")
        except Exception as e:
            logger.error(f"Failed to load Model Pipeline: {e}")
            self._pipeline = None
            raise RuntimeError(f"Could not load model pipeline: {e}")

    @property
    def is_loaded(self) -> bool:
        return self._pipeline is not None

    @property
    def classes(self) -> List[str]:
        if self._pipeline is not None and hasattr(self._pipeline.named_steps["classifier"], "classes_"):
            return list(self._pipeline.named_steps["classifier"].classes_)
        return ["Entire home/apt", "Private room", "Shared room"]

    @property
    def sklearn_version(self) -> str:
        return sklearn.__version__

    def _generate_insights(self, inp: ListingInput, pred_class: str, confidence: float) -> List[str]:
        """Generate dynamic, explainable market insights based on inputs and prediction."""
        insights = []
        borough = inp.neighbourhood_group
        median_price = BOROUGH_MEDIAN_PRICE.get(borough, 100.0)

        # Price analysis
        if inp.price > median_price * 1.5:
            insights.append(
                f"Premium Nightly Rate: ${inp.price:.0f}/night is significantly above the {borough} median (${median_price:.0f}), strongly correlating with entire residential units or luxury suites."
            )
        elif inp.price < median_price * 0.6:
            insights.append(
                f"Budget-Friendly Rate: ${inp.price:.0f}/night is well below the {borough} median (${median_price:.0f}), typical for shared spaces or cozy single bedrooms."
            )
        else:
            insights.append(
                f"Standard Market Rate: ${inp.price:.0f}/night aligns well with median listings in {inp.neighbourhood}, {borough}."
            )

        # Minimum nights pattern
        if inp.minimum_nights >= 30:
            insights.append(
                f"Extended Stay / Monthly Lease: Minimum requirement of {inp.minimum_nights} nights indicates long-term corporate or student housing rather than short-term transient tourism."
            )
        elif inp.minimum_nights <= 2:
            insights.append(
                f"High Turnover / Weekend Friendly: Low minimum stay ({inp.minimum_nights} night{'s' if inp.minimum_nights > 1 else ''}) maximizes weekend leisure and tourist bookings."
            )

        # Host activity
        if inp.calculated_host_listings_count > 5:
            insights.append(
                f"Commercial Operator / Property Group: Host manages {inp.calculated_host_listings_count} properties, reflecting structured multi-unit or co-living management."
            )
        else:
            insights.append(
                "Individual Host Profile: Listing appears to be operated by a private resident or small-scale property owner."
            )

        # Availability
        if inp.availability_365 > 300:
            insights.append(
                f"Year-Round Availability ({inp.availability_365} days/year): Full-time listing dedicated exclusively to guest stays."
            )
        elif inp.availability_365 < 60:
            insights.append(
                f"Occasional Availability ({inp.availability_365} days/year): Likely primary residence rented out selectively during host travel."
            )

        # Prediction confidence
        if confidence > 0.80:
            insights.append(
                f"High ML Model Certainty: Features match historical {pred_class} signatures with {confidence * 100:.1f}% confidence."
            )

        return insights

    def predict(self, inp: ListingInput) -> PredictionResponse:
        """Run inference on the listing inputs and return rich predictions."""
        if not self.is_loaded:
            raise RuntimeError("Model pipeline is not loaded.")

        # Prepare DataFrame with the exact column order expected by the ColumnTransformer
        # Training features: ['latitude', 'longitude', 'price', 'minimum_nights', 'number_of_reviews',
        #                    'reviews_per_month', 'calculated_host_listings_count', 'availability_365',
        #                    'neighbourhood_group', 'neighbourhood']
        
        # Soft-clip price and minimum_nights to match training distribution quantiles
        clipped_price = min(max(float(inp.price), 0.0), 800.0)
        clipped_nights = min(max(int(inp.minimum_nights), 1), 45)

        data = {
            "latitude": [float(inp.latitude)],
            "longitude": [float(inp.longitude)],
            "price": [clipped_price],
            "minimum_nights": [clipped_nights],
            "number_of_reviews": [int(inp.number_of_reviews)],
            "reviews_per_month": [float(inp.reviews_per_month)],
            "calculated_host_listings_count": [int(inp.calculated_host_listings_count)],
            "availability_365": [int(inp.availability_365)],
            "neighbourhood_group": [str(inp.neighbourhood_group)],
            "neighbourhood": [str(inp.neighbourhood)],
        }
        df = pd.DataFrame(data)

        # Run model prediction
        pred_label = self._pipeline.predict(df)[0]
        prob_array = self._pipeline.predict_proba(df)[0]
        class_names = self.classes

        # Map probabilities
        probabilities: Dict[str, float] = {
            cls_name: round(float(prob), 4)
            for cls_name, prob in zip(class_names, prob_array)
        }

        # Calculate confidence
        confidence = float(probabilities.get(pred_label, max(prob_array)))

        # Get visual details
        raw_detail = STAY_TYPE_DETAILS.get(
            pred_label,
            {
                "title": pred_label,
                "icon": "fa-house",
                "color": "indigo",
                "bg_class": "bg-indigo-500/10 border-indigo-500/30 text-indigo-400",
                "description": "Custom accommodation stay type.",
                "best_for": "General travelers."
            }
        )
        stay_detail = StayTypeDetail(**raw_detail)

        # Market insights
        insights = self._generate_insights(inp, pred_label, confidence)

        return PredictionResponse(
            predicted_stay_type=pred_label,
            confidence=confidence,
            confidence_percentage=f"{confidence * 100:.1f}%",
            probabilities=probabilities,
            details=stay_detail,
            insights=insights,
            input_received=inp.model_dump()
        )

# Global singleton accessor
def get_model() -> StayTypeModel:
    return StayTypeModel()
