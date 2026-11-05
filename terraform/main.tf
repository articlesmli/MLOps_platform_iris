terraform {
  required_version = ">= 1.0.0"
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23.0"
    }
  }
}

provider "kubernetes" {
  # Automatically uses the active kubectl context (Minikube locally, Kind in CI)
}

resource "kubernetes_manifest" "iris_kserve_service" {
  field_manager {
    force_conflicts = true
  }

  manifest = {
    apiVersion = "serving.kserve.io/v1beta1"
    kind       = "InferenceService"
 metadata = {
      name      = "iris-inference-service"
      namespace = "kserve"
      annotations = {
        "serving.kserve.io/deploymentMode"   = "Standard"
        "sidecar.istio.io/inject"            = "false"
        "serving.kserve.io/autoscalingClass" = "raw"
      }
    }
    spec = {
      predictor = {
        containers = [
          {
            image = "ghcr.io/articlesmli/mlops_platform_iris/iris-api:${var.image_tag}"
            ports = [
              {
                containerPort = 8080
              }
            ]
            resources = {
              requests = {
                cpu    = "100m"
                memory = "256Mi"
              }
              limits = {
                cpu    = "500m"
                memory = "512Mi"
              }
            }
          }
        ]
      }
    }
  }
}