output "lambda_function_names" {
  value = {
    for env, mod in module.config_parser_lambda : env => mod.function_name
  }
}

output "lambda_function_arns" {
  value = {
    for env, mod in module.config_parser_lambda : env => mod.function_arn
  }
}

output "lambda_role_arns" {
  value = {
    for env, mod in module.config_parser_lambda : env => mod.role_arn
  }
}
