locals {
  function_name_prefix = "social-rankings-configparser"
}

module "config_parser_lambda" {
  source = "../../modules/configparser_lambda"

  for_each = var.config_parser_environments

  function_name      = "${local.function_name_prefix}-${each.key}"
  s3_bucket_name     = each.value.s3_bucket_name
  s3_key_prefix      = each.value.s3_key_prefix
  subnet_ids         = each.value.subnet_ids
  security_group_ids = each.value.security_group_ids
  cluster_endpoint   = each.value.cluster_endpoint
  cluster_port       = each.value.cluster_port
  timeout            = each.value.timeout
  memory_size        = each.value.memory_size
}
