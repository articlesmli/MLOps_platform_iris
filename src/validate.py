# src/validate.py
from pathlib import Path
import yaml
import sys
import pandas as pd

def load_params():
    root_dir = Path(__file__).resolve().parent.parent
    params_path = root_dir / "params.yaml"
    with open(params_path, "r") as f:
        return yaml.safe_load(f)

def validate_data():
    params = load_params()
    root_dir = Path(__file__).resolve().parent.parent
    data_path = root_dir / params["data"]["dataset_path"]
    
    print(f"Loading and validating dataset from: {data_path}")
    if not data_path.exists():
        print(f"Error: Dataset not found at {data_path}")
        sys.exit(1)
        
    df = pd.read_csv(data_path)
    target_col = params["data"]["target_column"]
    
    # Define expected columns for Iris dataset benchmark
    expected_columns = ["sepal_length", "sepal_width", "petal_length", "petal_width", target_col]
    
    # 1. Check schema / columns existence
    for col in expected_columns:
        if col not in df.columns:
            print(f"Validation Error: Missing expected column '{col}'")
            sys.exit(1)
            
    # 2. Check for null values
    if df.isnull().any().any():
        print("Validation Error: Dataset contains null values.")
        sys.exit(1)
        
    # 3. Check row count and basic bounds
    if len(df) == 0:
        print("Validation Error: Dataset is empty.")
        sys.exit(1)
        
    if (df["sepal_length"] <= 0).any() or (df["petal_length"] <= 0).any():
        print("Validation Error: Feature dimensions must be greater than 0.")
        sys.exit(1)
        
    print("DATA VALIDATION PASSED: Dataset conforms to expected schema and quality rules.")
    sys.exit(0)

if __name__ == "__main__":
    validate_data()