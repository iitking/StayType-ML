# 🏠 StayType AI - NYC Airbnb Stay & Room Type Classifier

[![Live Demo](https://img.shields.io/badge/Live_Demo-Render-00c7b7.svg?style=for-the-badge&logo=render&logoColor=white)](https://staytype-ml.onrender.com)
[![Swagger Docs](https://img.shields.io/badge/API_Docs-Swagger-85EA2D.svg?style=for-the-badge&logo=swagger&logoColor=black)](https://staytype-ml.onrender.com/docs)

[![Python Version](https://img.shields.io/badge/Python-3.12%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.142%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.6.1-F7931E.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 🚀 **Live Application**: **[https://staytype-ml.onrender.com](https://staytype-ml.onrender.com)**  
> 📖 **Interactive OpenAPI (Swagger) Docs**: **[https://staytype-ml.onrender.com/docs](https://staytype-ml.onrender.com/docs)**
>
> **StayType AI** is an end-to-end Machine Learning web platform and high-performance REST API that predicts the optimal accommodation type (**Entire home/apt**, **Private room**, or **Shared room**) for New York City listings based on spatial location, pricing dynamics, availability, and host activity metrics.

---

## 🌟 Key Features

- **🧠 End-to-End Scikit-Learn Pipeline**: Fully encapsulates numerical imputers, standard scalers, categorical encoders, and a tuned **Random Forest Classifier** (`class_weight='balanced'`).
- **⚡ Production FastAPI Backend**: Async architecture, strict Pydantic V2 schema validations, Swagger/OpenAPI documentation at `/docs`, and dynamic market heuristic insights.
- **🎨 Modern Glassmorphism UI**:
  - Sleek dark/light theme switching with state memory.
  - Interactive NYC Borough pills dynamically updating 217 distinct neighborhood options.
  - Real-time **Chart.js Radar Chart** (Listing Profile vs NYC Median) & **Doughnut Chart** (Probability Distribution).
  - 1-Click **Instant Preset Scenarios** (*Manhattan Luxury Loft*, *Williamsburg Studio*, *Queens Shared Pod*, *SoHo Penthouse*).
  - Built-in **Developer Drawer** with live JSON inspect, formatted cURL commands, and 1-click clipboard copy.
  - Session prediction history table for comparative testing.
- **🐳 Dockerized & Cloud Ready**: Production-grade `Dockerfile` and `docker-compose.yml` for 1-command deployment.
- **🧪 Automated CI & Testing**: Pytest test suite covering endpoints, model inference, and edge-case schema validation with GitHub Actions CI workflow.

---

## 📊 Machine Learning Model Benchmarks

Trained and evaluated on **48,895 verified New York City Airbnb records** ([AB_NYC_2019 dataset](https://www.kaggle.com/datasets/dgomonov/new-york-city-airbnb-open-data)).

### Model Comparison & Evaluation

| Model Architecture | 3-Fold CV Accuracy | 3-Fold CV Macro-F1 | Test Set Accuracy | Test Set Macro-F1 |
| :--- | :---: | :---: | :---: | :---: |
| Logistic Regression (Baseline) | 65.9% | 52.2% | - | - |
| Decision Tree Classifier | 78.2% | 64.7% | - | - |
| Gradient Boosting Classifier | 85.0% | 70.5% | - | - |
| **Random Forest (Tuned)** 🏆 | **85.1%** | **71.5%** | **85.61%** | **73.90%** |

### Optimal Hyperparameters (RandomizedSearchCV)
- `classifier__n_estimators`: `200`
- `classifier__min_samples_split`: `10`
- `classifier__max_depth`: `None`
- `class_weight`: `'balanced'`

---

## 📁 Repository Structure

```text
StayType-ML/
├── .github/
│   └── workflows/
│       └── ci.yml               # Automated GitHub Actions CI workflow
├── app/
│   ├── __init__.py
│   ├── config.py                # Application settings and environment paths
│   ├── data_mapping.py          # 217 NYC neighborhoods mapped across 5 boroughs + presets
│   ├── main.py                  # FastAPI application, static mounting & routes
│   ├── model.py                 # Singleton model loader, inference & heuristic insights
│   ├── schemas.py               # Pydantic V2 schemas for input validation & responses
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css        # Responsive glassmorphism, animations & theme styles
│   │   └── js/
│   │       └── app.js           # Dynamic UI, Chart.js integrations & API handlers
│   └── templates/
│       └── index.html           # Modern SaaS dashboard with Tailwind CSS & FontAwesome
├── tests/
│   └── test_api.py              # Pytest API integration and inference test suite
├── .dockerignore
├── .gitignore                   # Git ignore for virtualenvs, caches & checkpoints
├── docker-compose.yml           # Multi-platform container configuration
├── Dockerfile                   # Production Python 3.12-slim Dockerfile
├── Model_Pipeline.pkl           # Saved scikit-learn pipeline (37.5 MB)
├── requirements.txt             # Pinned production and test dependencies
├── StayType_ML.ipynb            # Original Jupyter Notebook containing full EDA & model training
└── README.md
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10+ (Python 3.12 recommended)
- Git

### 2. Clone the Repository
```bash
git clone https://github.com/<your-username>/StayType-ML.git
cd StayType-ML
```

### 3. Create a Virtual Environment & Install Dependencies
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS / Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the Development Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser at: **[http://localhost:8000](http://localhost:8000)**

---

## 🐳 Docker Deployment

You can run the entire application using Docker with zero local Python setup:

### Using Docker Compose:
```bash
docker compose up --build
```

### Using Plain Docker:
```bash
docker build -t staytype-ml .
docker run -p 8000:8000 staytype-ml
```

Access the application at `http://localhost:8000`.

---

## 📡 API Reference & Endpoints

### 1. Classify Stay Type
- **Method**: `POST`
- **Path**: `/api/predict`
- **Request Body**:
```json
{
  "neighbourhood_group": "Manhattan",
  "neighbourhood": "Midtown",
  "latitude": 40.758,
  "longitude": -73.9855,
  "price": 350.0,
  "minimum_nights": 3,
  "number_of_reviews": 48,
  "reviews_per_month": 2.15,
  "calculated_host_listings_count": 2,
  "availability_365": 240
}
```

- **Response Body**:
```json
{
  "predicted_stay_type": "Entire home/apt",
  "confidence": 0.7432,
  "confidence_percentage": "74.3%",
  "probabilities": {
    "Entire home/apt": 0.7432,
    "Private room": 0.2532,
    "Shared room": 0.0036
  },
  "details": {
    "title": "Entire Home / Apartment",
    "icon": "fa-house-chimney",
    "color": "emerald",
    "bg_class": "bg-emerald-500/10 border-emerald-500/30 text-emerald-400",
    "description": "Guests have the whole place to themselves. Typically includes a private bedroom, bathroom, living space, and kitchen.",
    "best_for": "Couples, families, executives, and travelers seeking maximum privacy."
  },
  "insights": [
    "Premium Nightly Rate: $350/night is significantly above the Manhattan median ($150), strongly correlating with entire residential units or luxury suites.",
    "Individual Host Profile: Listing appears to be operated by a private resident or small-scale property owner."
  ],
  "input_received": { ... }
}
```

### 2. Metadata Endpoint
- **Method**: `GET`
- **Path**: `/api/metadata`
- Returns all 5 NYC boroughs mapped with their corresponding 217 neighborhoods and demo presets.

### 3. System Health Check
- **Method**: `GET`
- **Path**: `/api/health`
- Returns model load status, scikit-learn version, and target classes.

### 4. Interactive Swagger Documentation
Access the interactive OpenAPI interface at **[http://localhost:8000/docs](http://localhost:8000/docs)** or Redoc at **[http://localhost:8000/redoc](http://localhost:8000/redoc)**.

---

## 🧪 Running Automated Tests

Run the full pytest suite with:

```bash
PYTHONPATH=. pytest tests/ -v
```

All 7 test cases will execute:
```text
tests/test_api.py::test_health_endpoint PASSED
tests/test_api.py::test_metadata_endpoint PASSED
tests/test_api.py::test_presets_endpoint PASSED
tests/test_api.py::test_home_page_renders_html PASSED
tests/test_api.py::test_predict_entire_home PASSED
tests/test_api.py::test_predict_private_room PASSED
tests/test_api.py::test_predict_validation_error PASSED
```

---

## 🛠️ Technology Stack

- **Machine Learning**: Scikit-Learn 1.6.1, Joblib, NumPy, Pandas
- **Backend Framework**: FastAPI 0.142, Starlette, Pydantic V2, Uvicorn
- **Frontend / UI**: HTML5, Tailwind CSS, FontAwesome 6, Chart.js, Canvas-Confetti, JetBrains Mono & Plus Jakarta Sans fonts
- **DevOps & Testing**: Docker, Docker Compose, Pytest, HTTPX, GitHub Actions

---

## 👨‍💻 Author

<div align="center">

<a href="https://github.com/iitking">
  <img src="https://github.com/iitking.png" width="110" height="110" style="border-radius:50%" alt="Nivesh Kumar Meena" />
</a>

### **Nivesh Kumar Meena**

**AI Architect · MLOps Engineer** | B.Tech Electrical Engineering, **IIT Roorkee**

*Building agentic AI systems, RAG pipelines and production-ready ML.*

<a href="https://www.linkedin.com/in/nivesh-kumar-meena-a31465221/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
<a href="https://github.com/iitking"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" /></a>
<a href="mailto:niveshkr149@gmail.com"><img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>

<br/><br/>

⭐ **If you found this project useful, please give it a star!** ⭐

<sub>Open to AI/ML engineering opportunities and collaborations.</sub>

</div>

---

<div align="center">
  <sub>Made with ❤️ by <a href="https://github.com/iitking">Nivesh Kumar Meena</a> · © 2026 · MIT License</sub>
</div>

