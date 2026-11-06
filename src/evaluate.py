# src/evaluate.py
from pathlib import Path
import yaml
import pickle
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

def load_params():
    root_dir = Path(__file__).resolve().parent.parent
    params_path = root_dir / "params.yaml"
    if not params_path.exists():
        raise FileNotFoundError(f"Configuration file not found at: {params_path}")
    with open(params_path, "r") as f:
        return yaml.safe_load(f)

def evaluate_model():
    params = load_params()
    root_dir = Path(__file__).resolve().parent.parent
    
    data_path = root_dir / params["data"]["dataset_path"]
    model_path = root_dir / "models" / "model.pkl"
    
    if not model_path.exists():
        print(f"Error: Trained model artifact not found at {model_path}")
        sys.exit(1)
        
    if not data_path.exists():
        print(f"Error: Dataset not found at {data_path}")
        sys.exit(1)

    # Load dataset and split test set matching training logic
    df = pd.read_csv(data_path)
    target_col = params["data"]["target_column"]
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    test_size = params["training"].get("test_size", 0.2)
    random_state = params["training"].get("random_state", 42)
    _, X_test, _, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    # Load model
    with open(model_path, "rb") as f:
        model = pickle.load(f)
        
    # Predict and evaluate
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions, average="weighted")
    
    print(f"=== Model Performance Evaluation ===")
    print(f"Test Accuracy: {accuracy:.4f}")
    print(f"Test F1-Score: {f1:.4f}")
    
    # Define production gating thresholds (e.g., minimum 95% accuracy)
    MIN_ACCURACY_THRESHOLD = 0.90
    
    if accuracy < MIN_ACCURACY_THRESHOLD:
        print(f"\nGATE FAILED: Model accuracy ({accuracy:.4f}) is below the required production threshold ({MIN_ACCURACY_THRESHOLD}).")
        sys.exit(1)
    else:
        print(f"\nGATE PASSED: Model meets all production performance criteria!")
        sys.exit(0)

if __name__ == "__main__":
    evaluate_model()