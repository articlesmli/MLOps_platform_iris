variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "AWS Region to deploy the MLOps infrastructure"
}

variable "cluster_name" {
  type        = string
  default     = "iris-mlops-cluster"
  description = "Name of the EKS Kubernetes cluster"
}

variable "environment" {
  type        = string
  default     = "production"
  description = "Deployment environment tag"
}

variable "node_instance_type" {
  type        = string
  default     = "t3.medium"
  description = "EC2 instance type for Kubernetes worker nodes"
}
