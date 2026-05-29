variable "function_name" {
  type = string
}

variable "description" {
  type        = string
  default     = "Lambda function to parse AWS Config files and push to Neptune"
}

variable "runtime" {
  type    = string
  default = "python3.11"
}

variable "timeout" {
  type    = number
  default = 120
}

variable "memory_size" {
  type    = number
  default = 256
}

variable "log_retention_days" {
  type    = number
  default = 14
}

variable "s3_bucket_name" {
  type = string
}

variable "s3_key_prefix" {
  type    = string
  default = ""
}

variable "subnet_ids" {
  type = list(string)
}

variable "security_group_ids" {
  type = list(string)
}

variable "cluster_endpoint" {
  type = string
}

variable "cluster_port" {
  type    = number
  default = 8182
}

variable "create_s3_vpc_endpoint" {
  type    = bool
  default = true
}
