##### User data storage bucket

resource "google_storage_bucket" "user_bucket" {
  name                        = var.bucket_name
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true
  encryption {
    default_kms_key_name = google_kms_crypto_key.fastapi_crypto_key.id
  }
}

##### Bucket for static website

resource "google_storage_bucket" "frontend_bucket" {
  name                        = "${var.bucket_name}-frontend"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true
  website {
    main_page_suffix = "index.html"
    not_found_page   = "404.html"
  }
}

resource "google_storage_bucket_object" "frontend_index" {
  name         = "index.html"
  content_type = "text/html"
  bucket       = google_storage_bucket.frontend_bucket.name
  source       = "${path.module}/../frontend/index.html"
}

# Upload a simple 404 / error page to the bucket
resource "google_storage_bucket_object" "errorpage" {
  name         = "404.html"
  content_type = "text/html"
  bucket       = google_storage_bucket.frontend_bucket.name
  source       = "${path.module}/../frontend/404.html"
}

##### Terraform state bucket

resource "google_storage_bucket" "terraform_state_bucket" {
  name     = "${var.app_name}-terraform-state-bucket"
  location = var.region

  force_destroy               = false
  public_access_prevention    = "enforced"
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }
}