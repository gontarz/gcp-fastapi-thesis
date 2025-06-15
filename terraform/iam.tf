##### Service Accounts

# TODO create service account for CICD

resource "google_service_account" "fastapi_sa" {
  account_id   = "fastapi-app-sa"
  display_name = "Service Account for FastAPI App"
}

resource "google_service_account_key" "fastapi_sa_key" {
  service_account_id = google_service_account.fastapi_sa.name
  keepers = {
    request_id = "initial"
  }
}

##### GKE

resource "google_project_iam_member" "artifact_registry_writer" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${google_service_account.fastapi_sa.email}"
}

resource "google_project_iam_member" "container_admin" {
  project = var.project_id
  role    = "roles/container.admin"
  member  = "serviceAccount:${google_service_account.fastapi_sa.email}"
}

##### Firestore

resource "google_project_iam_member" "firestore_user" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.fastapi_sa.email}"
}

##### KMS

resource "google_kms_crypto_key_iam_member" "allow_bucket_encryption" {
  crypto_key_id = google_kms_crypto_key.fastapi_crypto_key.id
  role          = "roles/cloudkms.cryptoKeyEncrypterDecrypter"
  member        = "serviceAccount:${google_service_account.fastapi_sa.email}"
}

# resource "google_kms_key_ring_iam_member" "crypto_creator" {
#   key_ring_id = google_kms_key_ring.fastapi_key_ring.id
#   role        = "roles/cloudkms.cryptoKeyCreator"
#   member      = "serviceAccount:${google_service_account.fastapi_sa.email}"
# }

##### GCS

resource "google_project_iam_member" "storage_admin" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.fastapi_sa.email}"
}

# Backend bucket access
resource "google_storage_bucket_iam_member" "bucket_access" {
  bucket = google_storage_bucket.user_bucket.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.fastapi_sa.email}"
}

data "google_project" "current" {
}

# https://cloud.google.com/storage/docs/projects#service-accounts
locals {
  cloud_storage_service_account = "service-${data.google_project.current.number}@gs-project-accounts.iam.gserviceaccount.com"
}

# Bind role for kms
resource "google_project_iam_binding" "project" {
  project = data.google_project.current.id
  role    = "roles/cloudkms.cryptoKeyEncrypterDecrypter"
  members = [
    "serviceAccount:${local.cloud_storage_service_account}",
  ]
}

# Make frontend bucket public by granting allUsers storage.objectViewer access
resource "google_storage_bucket_iam_member" "public_rule" {
  bucket = google_storage_bucket.frontend_bucket.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}