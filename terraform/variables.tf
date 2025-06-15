variable "project_id" {
  type        = string
  description = "GCP project ID"
  default     = "thesis-460510" # TODO
}

variable "region" {
  type        = string
  default     = "europe-central2"
  description = "GCP region"
}

variable "zone" {
  type        = string
  default     = "europe-central2-a"
  description = "GCP zone"
}

variable "bucket_name" {
  type        = string
  default     = "gcs_fastapi_bucket"
  description = "Name of the GCS bucket"
}

variable "frontend_domain" {
  type        = string
  description = "Domain for frontend static website"
  default     = "k-gontarz.com" # TODO
}

variable "backend_sub_domain" {
  type        = string
  description = "Subdomain for backend api"
  default     = "api.k-gontarz.com" # TODO
}

variable "app_name" {
  type        = string
  default     = "gcs-fastapi-app"
  description = "Name of application"
}