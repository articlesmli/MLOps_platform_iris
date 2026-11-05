# Enterprise MLOps Platform (`MLOps_platform_iris`)

An end-to-end, enterprise-grade MLOps platform built with a modular, config-driven architecture[cite: 1]. While pre-configured with the **Iris dataset** as a baseline smoke test[cite: 1], the platform is designed to seamlessly swap out datasets and models for enterprise computer vision, NLP, or tabular workflows[cite: 1].

This platform leverages modern Cloud Native, GitOps, IaC, and Observability patterns[cite: 1].

---

## System Architecture

```text
                                  +-----------------------+
                                  |     params.yaml       |
                                  |  (Central Pipeline)   |
                                  +-----------+-----------+
                                              |
 +-------------------+             +----------v----------+             +-------------------+
 | Great Expectations | ---------> | Multi-Model Training| ---------> |  MLflow Registry  |
 | (Data Validation) |             |     (train.py)      |             | & Artifact Store  |
 +-------------------+             +----------+----------+             +---------+---------+
                                              |                                  |
                                   +----------v----------+                       |
                                   | Model Eval Gate     | <---------------------+
                                   |    (evaluate.py)    |
                                   +----------+----------+
                                              |
 +-------------------+             +----------v----------+
 |  Evidently AI     | <---------- |  Inference Service  |
 | (Drift Monitoring)|             | (FastAPI / KServe)  |
 +-------------------+             +----------+----------+
                                              |
                                   +----------v----------+
                                   | Prometheus/Grafana  |
                                   | (Metrics & Scrapes) |
                                   +---------------------+

```

---

## Tech Stack

* **Infrastructure as Code (IaC):** Terraform (Unified Kubernetes Provider, AWS EKS, VPC)


* **Containerization & Orchestration:** Docker, Kubernetes, KServe (CRD inference serving)


* **CI/CD & GitOps:** GitHub Actions (Hardened Pipeline with automated quality gating), Argo CD


* **Model Governance:** MLflow (Multi-model tracking & Model Registry integration)


* **Data Quality & Security:** Great Expectations, Trivy Vulnerability Scans


* **Observability & Monitoring:** Prometheus, Grafana, Evidently AI (Data & Target drift detection)



---

## Repository Structure

```text
MLOps_platform_iris/
├── .github/workflows/
│   └── ci-cd.yaml              # Hardened CI/CD pipeline (Validation, Training, Evaluation Gate, Testing, Trivy)
├── data/
│   └── iris.csv                # Raw/Injected dataset
├── k8s/
│   ├── kserve-service.yaml     # KServe InferenceService CRD manifest
│   ├── argocd-app.yaml         # Argo CD Application GitOps definition
│   └── monitoring/
│       └── prometheus-monitor.yaml # Prometheus ServiceMonitor configuration
├── models/
│   └── model.pkl               # Local trained model artifact fallback
├── src/
│   ├── app.py                  # FastAPI prediction service (Loads from MLflow Registry)
│   ├── train.py                # Training script with MLflow Model Registry integration
│   ├── evaluate.py             # Model performance gating script (Enforces accuracy threshold)
│   ├── validate.py             # Great Expectations validation suite
│   └── drift_monitor.py        # Evidently AI drift analysis runner
├── terraform/
│   ├── main.tf                 # Unified Kubernetes provider infrastructure definition
│   ├── variables.tf            # Infrastructure variables
│   └── outputs.tf              # Terraform output hooks
├── tests/
│   └── test_api.py             # Pytest API integration tests
├── Dockerfile                  # Production container definition
├── params.yaml                 # Central pipeline configuration file
└── requirements.txt            # Project Python dependencies

```

---

## Quick Start

### 1. Environment Setup

Clone the repository and set up your virtual environment:

```bash
git clone [https://github.com/articlesmli/MLOps_platform_iris.git](https://github.com/articlesmli/MLOps_platform_iris.git)
cd MLOps_platform_iris

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

```

### 2. Generate Dataset & Validate Data

Generate the baseline dataset and execute the Great Expectations validation suite:

```bash
# Generate baseline CSV
python -c "
import os, pandas as pd
from sklearn.datasets import load_iris
os.makedirs('data', exist_ok=True)
iris = load_iris(as_frame=True)
df = iris.frame
df.columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'target']
df.to_csv('data/iris.csv', index=False)
"

# Validate dataset schema and value bounds
python src/validate.py

```

### 3. Model Training, Registry Registration & Evaluation Gate

Train the model, register it to the MLflow Model Registry, and run the automated performance evaluation gate:

```bash
# Train model & log to MLflow Registry
python src/train.py

# Run quality gate to verify accuracy threshold (>= 90%)
python src/evaluate.py

```

### 4. Run API Server & Execute Tests

Launch the FastAPI serving app and execute automated pytest suites:

```bash
# Set PYTHONPATH and start API locally
PYTHONPATH=. uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload

# In a separate terminal, run unit tests
PYTHONPATH=. pytest tests/test_api.py -v

```

### 5. Monitor Data Drift

Execute the Evidently AI monitoring engine to compare production inferences against training data:

```bash
python src/drift_monitor.py
# Generates drift_report.html

```

---

## Cloud Infrastructure & Kubernetes Deployment

### Provision Infrastructure via Terraform

Initialize and apply the unified Kubernetes Terraform provider:

```bash
cd terraform
terraform init
terraform apply -auto-approve

```

### Deploy via Argo CD & KServe

Apply the GitOps and KServe manifests to your Kubernetes cluster:

```bash
kubectl apply -f k8s/kserve-service.yaml
kubectl apply -f k8s/argocd-app.yaml
kubectl apply -f k8s/monitoring/prometheus-monitor.yaml

```

---

## License

This project is licensed under the terms of the **MIT License**. See the `LICENSE` file for details.

