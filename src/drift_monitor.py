import os
import pandas as pd
from sklearn import datasets
from evidently import Report
from evidently.presets import DataDriftPreset

def run_drift_analysis():
    print("Loading Iris dataset for drift analysis...")
    iris = datasets.load_iris(as_frame=True)
    df = iris.frame
    
    # Split dataset: Reference (baseline) vs Current (simulated production)
    reference_data = df.iloc[:100]
    current_data = df.iloc[100:]
    
    print("Running Evidently Data Drift Report...")
    drift_report = Report(metrics=[
        DataDriftPreset(),
    ])
    
    eval_result = drift_report.run(reference_data=reference_data, current_data=current_data)
    
    # Create a dedicated reports directory if it doesn't exist
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    # Save the report cleanly inside the reports folder
    report_path = os.path.join(reports_dir, "drift_report.html")
    eval_result.save_html(report_path)
    print(f"Success! Data drift report saved cleanly to {report_path}")

if __name__ == "__main__":
    run_drift_analysis()