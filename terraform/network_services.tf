##### Cloud DNS

resource "google_dns_managed_zone" "kgontarz_zone" {
  name          = "k-gontarz-com"
  dns_name      = "${var.frontend_domain}."
  description   = "k-gontarz domain Public DNS zone"
  force_destroy = "true"
  dnssec_config {
    state = "on"
  }
  cloud_logging_config {
    enable_logging = true
  }
}

# fetching already created DNS zone
# data "google_dns_managed_zone" "kgontarz_dns_zone" {
#   name = "k-gontarz-com"
# }

resource "google_dns_record_set" "kgontarz_dns_record" {
  name         = google_dns_managed_zone.kgontarz_zone.dns_name
  managed_zone = google_dns_managed_zone.kgontarz_zone.name
  type         = "A"
  ttl          = 300
  rrdatas = [
    google_compute_global_address.frontend_ip.address
  ]
}

resource "google_dns_record_set" "api_kgontarz_dns_record" {
  name         = "api.${google_dns_managed_zone.kgontarz_zone.dns_name}"
  managed_zone = google_dns_managed_zone.kgontarz_zone.name
  type         = "A"
  ttl          = 300
  rrdatas = [
    google_compute_global_address.lb_static_ip_address.address
  ]
}

##### Cloud CDN

resource "google_compute_backend_bucket" "frontend_backend" {
  name        = "frontend-backend"
  bucket_name = google_storage_bucket.frontend_bucket.name
  enable_cdn  = true
}

resource "google_compute_url_map" "frontend_url_map" {
  name            = "frontend-url-map"
  default_service = google_compute_backend_bucket.frontend_backend.id
}

resource "google_compute_target_https_proxy" "frontend_proxy" {
  name             = "frontend-https-proxy"
  url_map          = google_compute_url_map.frontend_url_map.id
  ssl_certificates = [google_compute_managed_ssl_certificate.frontend_cert.id]
}

resource "google_compute_global_forwarding_rule" "frontend_https" {
  name                  = "frontend-https"
  target                = google_compute_target_https_proxy.frontend_proxy.id
  port_range            = "443"
  load_balancing_scheme = "EXTERNAL"
  ip_address            = google_compute_global_address.frontend_ip.id
}

#####  VPC Network IP Addresses

resource "google_compute_global_address" "lb_static_ip_address" {
  name = "fastapi-gke-ip-address"
}

resource "google_compute_global_address" "frontend_ip" {
  name = "frontend-ip"
}
