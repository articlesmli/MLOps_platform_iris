from pathlib import Path
import yaml
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
import mlflow
import mlflow.sklearn

def load_params():
    root_dir = Path(__file__).resolve().parent.parent
    params_path = root_dir / "params.yaml"
    if not params_path.exists():
        raise FileNotFoundError(f"Configuration file not found at: {params_path}")
    with open(params_path, "r") as f:
        return yaml.safe_load(f)

def train_model():
    params = load_params()
    root_dir = Path(__file__).resolve().parent.parent
    data_path = root_dir / params["data"]["dataset_path"]
    
    print(f"Loading dataset from: {data_path}")
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset not found at: {data_path}")
        
    df = pd.read_csv(data_path)
    target_col = params["data"]["target_column"]
    
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    test_size = params["training"].get("test_size", 0.2)
    random_state = params["training"].get("random_state", 42)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    # Set up MLflow Experiment
    exp_name = params["training"].get("mlflow_experiment_name", "iris_experiment")
    mlflow.set_experiment(exp_name)
    
    with mlflow.start_run():
        print("Training Logistic Regression model...")
        model = LogisticRegression(max_iter=200, random_state=random_state)
        model.fit(X_train, y_train)
        
        # Evaluate
        predictions = model.predict(X_test)
        acc = accuracy_score(y_test, predictions)
        f1 = f1_score(y_test, predictions, average="weighted")
        
        print(f"Model Evaluation -> Accuracy: {acc:.4f}, F1-Score: {f1:.4f}")
        
        # Log parameters and metrics
        mlflow.log_param("test_size", test_size)
        mlflow.log_param("random_state", random_state)
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)
        
        # Save locally
        models_dir = root_dir / "models"
        models_dir.mkdir(exist_ok=True)
        m_path = models_dir / "model.pkl"
        
        with open(m_path, "wb") as f:
            pickle.dump(model, f)
        print(f"Successfully saved winning model locally to {m_path}!")

        # --- MLflow Model Registry Integration & Promotion Gating ---
        try:
            model_name = "iris_classification_model"
            print(f"Registering model '{model_name}' to MLflow Registry...")
            
            # Log and register model artifact
            mlflow.sklearn.log_model(
                model, 
                artifact_path="model",
                registered_model_name=model_name
            )
            print("Model successfully registered to MLflow Model Registry!")
        except Exception as e:
            print(f"Warning: Could not register model to MLflow registry: {e}")

if __name__ == "__main__":
    train_model()