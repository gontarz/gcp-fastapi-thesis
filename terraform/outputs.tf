output "bucket_name" {
  value = google_storage_bucket.user_bucket.name
}

output "cluster_name" {
  value = google_container_cluster.primary.name
}

output "artifact_repo" {
  value = google_artifact_registry_repository.app_repo.repository_id
}

output "service_account_email" {
  value = google_service_account.fastapi_sa.email
}

output "service_account_key" {
  value     = google_service_account_key.fastapi_sa_key.private_key
  sensitive = true
}

output "firestore_database_name" {
  value = google_firestore_database.default.name
}
