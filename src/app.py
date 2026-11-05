from pathlib import Path
import os
import pickle
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field
import mlflow.sklearn

# Define request body schema using Pydantic
class IrisInput(BaseModel):
    sepal_length: float = Field(..., gt=0, description="Sepal length in cm")
    sepal_width: float = Field(..., gt=0, description="Sepal width in cm")
    petal_length: float = Field(..., gt=0, description="Petal length in cm")
    petal_width: float = Field(..., gt=0, description="Petal width in cm")

    model_config = {
        "protected_namespaces": ()
    }

LOCAL_MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "model.pkl"
model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP LOGIC ---
    global model
    # Target MLflow Registry URI pointing to the Production model stage/alias
    mlflow_model_uri = os.getenv("MLFLOW_MODEL_URI", "models:/iris_classification_model/Production")
    
    # Option 1: Load from MLflow Model Registry (Primary Governance Path)
    try:
        print(f"Attempting to load model from MLflow Registry URI: {mlflow_model_uri}")
        model = mlflow.sklearn.load_model(mlflow_model_uri)
        print("Model loaded successfully from MLflow registry Production stage!")
    except Exception as e:
        print(f"Failed to load from MLflow Registry ({e}), falling back to local artifact...")

        # Option 2: Fallback to local pickle artifact
        if not LOCAL_MODEL_PATH.exists():
            print(f"Warning: Model artifact not found at {LOCAL_MODEL_PATH}. API will fail predictions until a model is placed here.")
        else:
            try:
                with open(LOCAL_MODEL_PATH, "rb") as f:
                    model = pickle.load(f)
                print("Model loaded successfully into serving memory from local path using pickle!")
            except Exception as ex:
                print(f"Error loading local model with pickle: {ex}")

    yield  # Runs the application
    
    # --- SHUTDOWN LOGIC ---
    print("Shutting down inference API application...")

app = FastAPI(
    title="MLOps Universal Platform - Inference API",
    description="Serves real-time predictions for the Iris classification benchmark suite with model registry version control.",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def health_check(response: Response):
    if model is None:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {
            "message": "Service degraded: Model artifact not loaded",
            "status": "unhealthy",
            "model_loaded": False,
            "service": "iris-mlops-inference"
        }
    return {
        "message": "Welcome to the Iris MLOps Inference API",
        "status": "healthy",
        "model_loaded": True,
        "service": "iris-mlops-inference"
    }

@app.get("/predict")
def predict_get(
    sepal_length: float = 5.1, 
    sepal_width: float = 3.5, 
    petal_length: float = 1.4, 
    petal_width: float = 0.2
):
    if model is None:
        raise HTTPException(status_code=503, detail="Model artifact not found or not loaded.")
    
    features = [[sepal_length, sepal_width, petal_length, petal_width]]
    
    try:
        prediction = model.predict(features)
        class_names = ["setosa", "versicolor", "virginica"]
        predicted_class = class_names[int(prediction[0])] if int(prediction[0]) < len(class_names) else str(prediction[0])
        
        return {
            "method": "GET",
            "prediction": int(prediction[0]),
            "class_name": predicted_class,
            "info": "For programmatic access, use POST /predict with a JSON body."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict")
def predict(data: IrisInput):
    if model is None:
        raise HTTPException(status_code=503, detail="Model artifact not found or not loaded.")
    
    features = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]]
    
    try:
        prediction = model.predict(features)
        class_names = ["setosa", "versicolor", "virginica"]
        predicted_class = class_names[int(prediction[0])] if int(prediction[0]) < len(class_names) else str(prediction[0])
        
        return {
            "prediction": int(prediction[0]),
            "class_name": predicted_class
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))