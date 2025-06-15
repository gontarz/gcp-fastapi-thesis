resource "google_kms_key_ring" "fastapi_key_ring" {
  name     = "fastapi-key-ring"
  location = var.region
}

resource "google_kms_crypto_key" "fastapi_crypto_key" {
  name     = "fastapi-crypto-key"
  key_ring = google_kms_key_ring.fastapi_key_ring.id
  # rotation_period = "100000s"

  lifecycle {
    prevent_destroy = false
  }
}

