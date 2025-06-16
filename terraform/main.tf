provider "google" {
  project = var.project_id
  region  = var.region
}

terraform {
  required_providers {
    google = {
      version = "~> 6.39.0"
    }
  }
  backend "gcs" {
    bucket = "gcs-fastapi-app-terraform-state-bucket"
    prefix = "terraform/state"
  }
}
