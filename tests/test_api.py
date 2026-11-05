from fastapi.testclient import TestClient
from src.app import app

def test_read_main():
    with TestClient(app) as client:
        response = client.get("/")
        # Now that lifespan runs, model is loaded and returns 200 OK
        assert response.status_code == 200
        assert "Iris MLOps Inference API" in response.json()["message"]

def test_predict_endpoint_valid_data():
    with TestClient(app) as client:
        payload = {
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
        assert "class_name" in data
        assert data["class_name"] in ["setosa", "versicolor", "virginica"]

def test_predict_endpoint_invalid_data():
    with TestClient(app) as client:
        # Negative dimensions should fail Pydantic validation
        payload = {
            "sepal_length": -1.0,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == 422  # Unprocessable Entity (Validation Error)
        