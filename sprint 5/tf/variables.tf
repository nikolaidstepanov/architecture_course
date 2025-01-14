variable "yc_token" {
  description = "Yandex Cloud OAuth token"
}

variable "cloud_id" {
  description = "Cloud ID"
}

variable "folder_id" {
  description = "Folder ID"
}

variable "zone" {
  description = "Zone for VM"
  default     = "ru-central1-a"
}

variable "subnet_id" {
  description = "Subnet ID"
}