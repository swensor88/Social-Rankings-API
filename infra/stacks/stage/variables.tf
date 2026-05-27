variable "alb_certificate_arn" {
  type        = string
  description = "ACM certificate ARN for ALB HTTPS listener"
}

variable "db_name" {
  type    = string
  default = "social_rankings"
}

variable "db_username" {
  type    = string
  default = "social_rankings"
}

variable "db_password" {
  type      = string
  sensitive = true
}

variable "db_instance_class" {
  type    = string
  default = "db.t4g.micro"
}

variable "api_key" {
  type      = string
  sensitive = true
}
