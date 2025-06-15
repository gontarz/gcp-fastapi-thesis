resource "google_container_cluster" "primary" {
  name                     = "fastapi-gke-cluster"
  location                 = var.zone
  remove_default_node_pool = true
  initial_node_count       = 1
}

resource "google_container_node_pool" "primary_nodes" {
  name     = "primary-node-pool"
  location = var.zone
  cluster  = google_container_cluster.primary.name

  node_config {
    preemptible  = true
    machine_type = "e2-medium"
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }

  initial_node_count = 1
}

resource "google_artifact_registry_repository" "app_repo" {
  provider      = google
  location      = var.region
  repository_id = "gcs-fastapi-repo"
  format        = "DOCKER"
}

