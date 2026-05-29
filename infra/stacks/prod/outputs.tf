output "api_endpoint" {
  value = module.apigateway.api_endpoint
}

output "ecr_repository_url" {
  value = module.ecs.ecr_repository_url
}

output "github_actions_deploy_role_arn" {
  value = aws_iam_role.github_actions_prod_deploy.arn
}
