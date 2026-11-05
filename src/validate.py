from pathlib import Path
import yaml
import pandas as pd
import great_expectations as ge

def load_params():
    # Automatically locate root-level params.yaml regardless of execution path
    root_dir = Path(__file__).resolve().parent.parent
    params_path = root_dir / "params.yaml"
    
    if not params_path.exists():
        raise FileNotFoundError(f"Configuration file not found at: {params_path}")
    with open(params_path, "r") as f:
        return yaml.safe_load(f)

def validate_data():
    params = load_params()
    root_dir = Path(__file__).resolve().parent.parent
    data_path = root_dir / params["data"]["dataset_path"]
    
    print(f"Loading and validating dataset from: {data_path}")
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset not found at: {data_path}")
        
    df = pd.read_csv(data_path)
    
    # Great Expectations validation wrapper
    gdf = ge.from_pandas(df)
    
    target_col = params["data"]["target_column"]
    feature_columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    expected_columns = feature_columns + [target_col]
    
    # 1. Verify all required columns exist
    for col in expected_columns:
        res = gdf.expect_column_to_exist(col)
        if not res["success"]:
            raise ValueError(f"Validation failed: Column '{col}' does not exist.")
            
    # 2. Verify no null values in critical columns
    for col in expected_columns:
        res = gdf.expect_column_values_to_not_be_null(col)
        if not res["success"]:
            raise ValueError(f"Validation failed: Column '{col}' contains null values.")

    # 3. Verify feature values fall within realistic biological bounds
    for col in feature_columns:
        res = gdf.expect_column_values_to_be_between(col, min_value=0.1, max_value=20.0)
        if not res["success"]:
            raise ValueError(f"Validation failed: Column '{col}' contains values out of expected biological bounds.")
            
    print("Success: Data validation passed!")

if __name__ == "__main__":
    validate_data()