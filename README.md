# GCS FastAPI App

A complete application that provides secure user resource management using **Google Cloud Storage**, **KMS encryption**, and **FastAPI**, with a static frontend deployed to **GCS Website Hosting** and backend to **GKE**.

---

## 🔐 Features

- ✅ JWT-based authentication (register, login)
- ☁️ File upload, list, delete (scoped per user)
- 🔑 Per-user Google Cloud KMS encryption
- 🌐 Frontend as static site hosted in GCS
- ☁️ Backend hosted in GKE (FastAPI + GCS + KMS)
- ✅ TLS/HTTPS via GCP-managed certificates
- ⚙️ CI/CD with GitHub Actions and Helm

---

## 🚀 Quick Start

### 1. Clone & Configure

```bash
git clone https://github.com/your-org/gcs-fastapi-app.git
cd gcs-fastapi-app
```

Create a `.env` file or set environment variables for:
- `GCP_PROJECT_ID`
- `GKE_CLUSTER`, `GKE_ZONE`
- `GAR_LOCATION` (e.g. europe)
- `GCP_BUCKET_NAME`
- `APP_DOMAIN` (e.g. backend.example.com)
- `JWT_SECRET_KEY`

---

### 2. Deploy with Terraform

```bash
terraform init
terraform apply -var="project_id=your-project" \
                -var="bucket_name=your-bucket" \
                -var="frontend_domain=your.frontend.domain"
```

---

### 3. Deploy Backend (GKE) + Frontend (GCS) via GitHub Actions

Ensure you set the following **repository secrets**:

- `GCP_SA_KEY`
- `GCP_PROJECT_ID`
- `GKE_CLUSTER`, `GKE_ZONE`
- `GAR_LOCATION`
- `GCP_BUCKET_NAME`
- `JWT_SECRET_KEY`
- `APP_DOMAIN`
- `APP_EMAIL`

Then push to `main` branch to trigger deployment.

---

### 4. Access

- **Frontend**: https://k-gontarz.com
- **Backend API**: https://api.k-gontarz.com

---

## 📁 Project Structure

```
.
├── app/                    # FastAPI app (models, routes, services)
├── frontend/               # Static frontend HTML+JS
├── terraform/              # Full IaC for GKE, GCS, KMS, CDN, etc.
├── helm/                   # Helm chart for GKE backend
├── .github/workflows/      # CI/CD via GitHub Actions
└── README.md
```

---

## 🛡 Security

- GCS bucket access is restricted per user.
- Each file is encrypted using the user’s KMS key.
- JWT auth ensures isolation of access and operations.
- GKE services exposed via HTTPS Ingress with TLS cert.

---

## 📦 Tech Stack

- FastAPI + Python
- GCP (GCS, KMS, GKE, IAM, Artifact Registry, CDN)
- Terraform + Helm + GitHub Actions
- Static site hosting (GCS website)

---

## 🧪 Running Locally

```bash
uvicorn main:app --reload
```

Use any static server to preview `frontend/index.html`, or deploy with `gsutil`.

---

## 📬 License

MIT © 2025 GCS FastAPI App
