resource "google_compute_managed_ssl_certificate" "frontend_cert" {
  name = "frontend-ssl-cert"
  managed {
    domains = [var.frontend_domain]
  }
}

resource "google_compute_managed_ssl_certificate" "backend_cert" {
  name = "backend-ssl-cert"
  managed {
    domains = [var.backend_sub_domain]
  }
}
