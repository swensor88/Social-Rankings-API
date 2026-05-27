locals {
  name_prefix = "social-rankings-stage"
}

module "vpc" {
  source      = "../../modules/vpc"
  name_prefix = local.name_prefix
  environment = "stage"
  region      = "us-east-1"
}

module "iam" {
  source      = "../../modules/iam"
  name_prefix = local.name_prefix
  secret_arns = [module.secrets.db_secret_arn, module.secrets.api_key_secret_arn]
}

module "ecs" {
  source                  = "../../modules/ecs"
  name_prefix             = local.name_prefix
  environment             = "stage"
  region                  = "us-east-1"
  vpc_id                  = module.vpc.vpc_id
  public_subnet_ids       = module.vpc.public_subnet_ids
  private_subnet_ids      = module.vpc.private_subnet_ids
  task_execution_role_arn = module.iam.task_execution_role_arn
  task_role_arn           = module.iam.task_role_arn
  api_key_secret_arn      = module.secrets.api_key_secret_arn
  db_secret_arn           = module.secrets.db_secret_arn
}

module "rds" {
  source                = "../../modules/rds"
  name_prefix           = local.name_prefix
  vpc_id                = module.vpc.vpc_id
  private_subnet_ids    = module.vpc.private_subnet_ids
   allowed_cidr_blocks   = ["10.0.0.0/16"]
  db_name               = var.db_name
  db_username           = var.db_username
  db_password           = var.db_password
  instance_class        = var.db_instance_class
  multi_az              = false
  deletion_protection   = false
  skip_final_snapshot   = true
}

module "secrets" {
  source      = "../../modules/secrets"
  name_prefix = local.name_prefix
  db_username = var.db_username
  db_password = var.db_password
  db_host     = module.rds.db_endpoint
  db_name     = var.db_name
  api_key     = var.api_key
}

module "apigateway" {
  source       = "../../modules/apigateway"
  name_prefix  = local.name_prefix
  alb_dns_name = module.ecs.alb_dns_name
  stage_name   = "stage"
}
