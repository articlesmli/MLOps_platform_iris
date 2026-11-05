output "container_id" {
  description = "The ID of the running Iris FastAPI container"
  value       = docker_container.iris_api_container.id
}

output "api_url" {
  description = "Local URL to access the inference API"
  value       = "http://localhost:8000"
}

output "network_id" {
  description = "The ID of the local Docker bridge network"
  value       = docker_network.iris_bridge.id
}