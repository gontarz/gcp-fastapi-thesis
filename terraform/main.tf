provider "google" {
  project = var.project_id
  region  = var.region
}

terraform {
  backend "gcs" {
    bucket = "gcs-fastapi-app-terraform-state-bucket"
    prefix = "terraform/state"
  }
}
