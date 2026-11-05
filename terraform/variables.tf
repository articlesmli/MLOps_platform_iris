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

variable "image_name" {
  type    = string
  default = "articlesmli/mlops_platform_iris"
}