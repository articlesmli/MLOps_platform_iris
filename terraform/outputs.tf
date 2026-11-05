output "kubernetes_manifest_applied" {
  description = "Indicates whether the KServe InferenceService manifest was managed via Terraform."
  value       = kubernetes_manifest.iris_kserve_service.id
}

output "inference_service_name" {
  description = "The name of the deployed KServe InferenceService"
  value       = kubernetes_manifest.iris_kserve_service.manifest["metadata"]["name"]
}