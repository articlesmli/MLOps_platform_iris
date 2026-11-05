output "kubernetes_manifest_applied" {
  description = "The name of the applied KServe InferenceService manifest."
  value       = kubernetes_manifest.iris_kserve_service.manifest["metadata"]["name"]
}