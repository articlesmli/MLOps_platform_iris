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
  # Connects to your active Kubernetes context (Minikube, EKS, GKE, or Kind)
  config_path    = var.kubeconfig_path
  config_context = var.kubeconfig_context
}

variable "kubeconfig_path" {
  type    = string
  default = "~/.kube/config"
}

variable "kubeconfig_context" {
  type    = string
  default = ""
}

variable "image_tag" {
  type    = string
  default = "latest"
}

# Deploy the Iris MLOps Inference Service directly via Terraform Kubernetes Provider
resource "kubernetes_manifest" "iris_kserve_service" {
  manifest = {
    apiVersion = "serving.kserve.io/v1beta1"
    kind       = "InferenceService"
    metadata = {
      name      = "iris-inference-service"
      namespace = "default"
      labels = {
        app = "iris-mlops"
      }
    }
    spec = {
      predictor = {
        model = {
          modelFormat = {
            name = "sklearn"
          }
          storageUri = "oci://ghcr.io/${var.image_name}/iris-api:${var.image_tag}"
        }
      }
    }
  }
}

output "service_name" {
  value = kubernetes_manifest.iris_kserve_service.manifest.metadata.name
}

output "service_namespace" {
  value = kubernetes_manifest.iris_kserve_service.manifest.metadata.namespace
}