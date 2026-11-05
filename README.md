Here is your updated **`README.md`** file complete with a dedicated **License** section referencing the MIT License:

```markdown
# 🚀 Enterprise MLOps Platform (`MLOps_platform_iris`)

An end-to-end, enterprise-grade MLOps platform built with a modular, config-driven architecture. While pre-configured with the **Iris dataset** as a baseline smoke test, the platform is designed to seamlessly swap out datasets and models for enterprise computer vision, NLP, or tabular workflows.

This platform leverages modern Cloud Native, GitOps, IaC, and Observability patterns.

---

## 🏗 System Architecture

```text
                                  +-----------------------+
                                  |     params.yaml       |
                                  |  (Central Pipeline)   |
                                  +-----------+-----------+
                                              |
 +-------------------+             +----------v----------+             +-------------------+
 | Great Expectations | ---------> | Multi-Model Training| ---------> |  MLflow Registry  |
 | (Data Validation) |             |     (train.py)      |             | & Artifact Store  |
 +-------------------+             +---------------------+             +---------+---------+
                                                                                 |
 +-------------------+             +---------------------+                       |
 |  Evidently AI     | <---------- |  Inference Service  | <---------------------+
 | (Drift Monitoring)|             | (FastAPI / KServe)  |
 +-------------------+             +----------+----------+
                                              |
                                   +----------v----------+
                                   | Prometheus/Grafana  |
                                   | (Metrics & Scrapes) |
                                   +---------------------+


```

---

## 🛠 Tech Stack

* **Infrastructure as Code (IaC):** Terraform (AWS EKS, VPC, Security Groups)
* **Containerization & Orchestration:** Docker, Kubernetes, KServe (CRD inference serving)
* **Continuous Integration & Delivery:** GitHub Actions (CI/CD), Argo CD (GitOps deployment)
* **Model Experiment Tracking & Benchmarking:** MLflow (Multi-model runs)
* **Data Quality & Validation:** Great Expectations
* **Security & Vulnerability Scanning:** Trivy
* **Observability & Monitoring:** Prometheus, Grafana, Evidently AI (Data & Target drift detection)

---

## 📂 Repository Structure

```text
MLOps_platform_iris/
├── .github/workflows/
│   └── ci.yml                   # CI/CD pipeline (Validation, Training, Testing, Trivy)
├── data/
│   └── iris.csv                 # Raw/Injected dataset
├── k8s/
│   ├── kserve-service.yaml      # KServe InferenceService CRD manifest
│   ├── argocd-app.yaml          # Argo CD Application GitOps definition
│   └── monitoring/
│       └── prometheus-monitor.yaml # Prometheus ServiceMonitor configuration
├── models/
│   └── model.pkl                # Local trained model artifact
├── src/
│   ├── app.py                   # FastAPI prediction service
│   ├── train.py                 # Config-driven 5-model benchmarking & MLflow logging script
│   ├── validate.py              # Great Expectations validation suite
│   └── drift_monitor.py         # Evidently AI drift analysis runner
├── terraform/
│   ├── main.tf                  # AWS EKS & VPC network infrastructure definition
│   ├── variables.tf             # Infrastructure variables
│   └── outputs.tf               # Terraform output hooks
├── tests/
│   └── test_api.py              # Pytest API integration tests
├── Dockerfile                   # Production container definition
├── params.yaml                  # Central pipeline configuration file
└── requirements.txt             # Project Python dependencies


```

---

## ⚡ Quick Start

### 1. Environment Setup

Clone the repository and activate a Python 3.10 virtual environment:

```bash
git clone [https://github.com/your-username/MLOps_platform_iris.git](https://github.com/your-username/MLOps_platform_iris.git)
cd MLOps_platform_iris

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


```

### 2. Generate Dataset & Validate Data

Generate the baseline dataset and run the Great Expectations validation suite:

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

### 3. Multi-Model Benchmark Training & Experiment Tracking

Train and evaluate the suite of **five machine learning models** defined in `params.yaml`, automatically logging each run and metric to MLflow:

```bash
python src/train.py


```

To view and compare all model runs side-by-side in the MLflow UI:

```bash
mlflow ui
# Open http://localhost:5000 in your browser


```

### 4. Run API Server & Execute Tests

Launch the FastAPI serving app and execute automated pytest suites:

```bash
# Start API locally
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload

# In a separate terminal, run unit tests
pytest tests/test_api.py


```

### 5. Monitor Data Drift

Execute the Evidently AI monitoring engine to compare production inferences against training data:

```bash
python src/drift_monitor.py
# Generates drift_report.html


```

---

## ☁ Cloud Infrastructure & Kubernetes Deployment

### Provision AWS Infrastructure via Terraform

Ensure AWS credentials are configured (`aws configure` or `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` exported):

```bash
cd terraform
terraform init
terraform plan
terraform apply -auto-approve

# Configure local kubectl context
aws eks update-kubeconfig --region us-east-1 --name iris-mlops-cluster


```

### Deploy via Argo CD & KServe

Apply the GitOps and KServe manifests to your Kubernetes cluster:

```bash
kubectl create namespace kserve-test
kubectl apply -f k8s/kserve-service.yaml
kubectl apply -f k8s/argocd-app.yaml
kubectl apply -f k8s/monitoring/prometheus-monitor.yaml


```

---

## ⚙️ Configuration (`params.yaml`)

Centralize pipeline settings and define your suite of **five machine learning models** without editing core source code:

```yaml
base:
  project: "mlops-universal-platform"
  random_state: 42
  test_size: 0.2

data:
  dataset_path: "data/iris.csv"
  target_column: "target"

models:
  - name: "random_forest"
    hyperparameters:
      n_estimators: 100
      max_depth: 8
  - name: "logistic_regression"
    hyperparameters:
      C: 1.0
      max_iter: 200
  - name: "svc"
    hyperparameters:
      C: 1.0
      kernel: "rbf"
  - name: "knn"
    hyperparameters:
      n_neighbors: 5
  - name: "decision_tree"
    hyperparameters:
      max_depth: 5

training:
  mlflow_experiment_name: "universal_classification_benchmark"

```

---

## 📄 License

This project is licensed under the terms of the **MIT License**. See the `LICENSE` file for details.

