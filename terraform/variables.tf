variable "project_id" {
  type        = string
  description = "GCP project ID"
}

variable "region" {
  type        = string
  description = "GCP region"
}

variable "zone" {
  type        = string
  description = "GCP zone"
}

variable "bucket_name" {
  type        = string
  description = "Name of the GCS bucket"
}

variable "frontend_domain" {
  type        = string
  description = "Domain for frontend static website"
}

variable "backend_sub_domain" {
  type        = string
  description = "Subdomain for backend api"
}

variable "app_name" {
  type        = string
  description = "Name of application"
}