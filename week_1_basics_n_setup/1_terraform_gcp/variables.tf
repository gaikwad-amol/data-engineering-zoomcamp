variable "project_id" {
  description = "Project ID"
  default     = "learn-from-datatalksclub"
}

variable "location" {
  description = "Project Location"
  default     = "asia-south1"
}

variable "bq_dataset_name" {
  description = "Name of the dataset"
  default     = "raw_trips_data_all"
}

variable "gcs_bucket_name" {
  description = "Name of the bucket"
  default     = "dtc_nyc_taxi_data"
}

variable "gcs_storage_class" {
  description = "Bucket storage class"
  default     = "STANDARD"
}

