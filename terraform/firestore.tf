# CMEK is forbitten for default database
# https://cloud.google.com/firestore/native/docs/use-cmek
resource "google_firestore_database" "default" {
  project     = var.project_id
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"
  # cmek_config {
  #   kms_key_name = google_kms_crypto_key.fastapi_crypto_key.id
  # }
}