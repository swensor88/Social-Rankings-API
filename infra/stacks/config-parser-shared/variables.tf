variable "config_parser_environments" {
  description = "Environment-specific Lambda configuration for AWS Config file parsing"
  type = map(object({
    s3_bucket_name      = string
    s3_key_prefix       = optional(string, "")
    subnet_ids          = list(string)
    security_group_ids  = list(string)
    cluster_endpoint    = string
    cluster_port        = optional(number, 8182)
    timeout             = optional(number, 120)
    memory_size         = optional(number, 256)
  }))
  default = {}
}
