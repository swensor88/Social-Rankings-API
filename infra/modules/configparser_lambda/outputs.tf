output "function_name" {
  value = aws_lambda_function.config_parser.function_name
}

output "function_arn" {
  value = aws_lambda_function.config_parser.arn
}

output "role_arn" {
  value = aws_iam_role.lambda.arn
}
