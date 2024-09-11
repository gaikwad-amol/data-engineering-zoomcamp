terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.1.0"
    }
  }
}

provider "google" {
  # credentials = file(var.my_creds) in the variables you can have the keys file path from the machine
  project = var.project_id
  region  = var.location
}

resource "google_storage_bucket" "bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "Delete"
    }
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id                  = var.bq_dataset_name
  friendly_name               = "nyc_taxi_dataset"
  location                    = var.location
  default_table_expiration_ms = 3600000

  labels = {
    env = "default"
  }
}