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

variable "github_repository_owner" {
  type    = string
  default = "swensor88"
}

variable "github_repository_name" {
  type    = string
  default = "Social-Rankings-API"
}

variable "github_prod_branch" {
  type    = string
  default = "main"
}
