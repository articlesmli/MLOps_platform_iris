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
  config_path    = var.kubeconfig_path
  config_context = var.kubeconfig_context
}

resource "kubernetes_manifest" "iris_kserve_service" {
  manifest = {
    apiVersion = "serving.kserve.io/v1beta1"
    kind       = "InferenceService"
    metadata = {
      name      = "iris-inference-service"
      namespace = "default"
      labels    = { app = "iris-mlops" }
    }
    spec = {
      predictor = {
        model = {
          modelFormat = { name = "sklearn" }
          storageUri  = "oci://ghcr.io/${var.image_name}/iris-api:${var.image_tag}"
        }
      }
    }
  }
}