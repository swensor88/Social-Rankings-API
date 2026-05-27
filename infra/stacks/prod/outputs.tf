output "api_endpoint" {
  value = module.apigateway.api_endpoint
}

output "ecr_repository_url" {
  value = module.ecs.ecr_repository_url
}
