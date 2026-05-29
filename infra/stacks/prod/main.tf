locals {
  name_prefix              = "social-rankings-prod"
  github_oidc_provider_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/token.actions.githubusercontent.com"
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "aws_iam_policy_document" "github_actions_assume" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [local.github_oidc_provider_arn]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values = [
        "repo:${var.github_repository_owner}/${var.github_repository_name}:*",
        "repo:${var.github_repository_owner}/${lower(var.github_repository_name)}:*",
        "repo:${lower(var.github_repository_owner)}/${var.github_repository_name}:*",
        "repo:${lower(var.github_repository_owner)}/${lower(var.github_repository_name)}:*",
      ]
    }
  }
}

resource "aws_iam_role" "github_actions_prod_deploy" {
  name               = "github-actions-prod-deploy"
  assume_role_policy = data.aws_iam_policy_document.github_actions_assume.json
}

data "aws_iam_policy_document" "github_actions_prod_deploy" {
  statement {
    sid    = "ECRAuth"
    effect = "Allow"
    actions = [
      "ecr:GetAuthorizationToken"
    ]
    resources = ["*"]
  }

  statement {
    sid    = "ECRPush"
    effect = "Allow"
    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:BatchGetImage",
      "ecr:CompleteLayerUpload",
      "ecr:DescribeImages",
      "ecr:DescribeRepositories",
      "ecr:GetDownloadUrlForLayer",
      "ecr:InitiateLayerUpload",
      "ecr:PutImage",
      "ecr:UploadLayerPart"
    ]
    resources = [
      "arn:aws:ecr:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:repository/${local.name_prefix}-repo"
    ]
  }

  statement {
    sid    = "ECSDeploy"
    effect = "Allow"
    actions = [
      "ecs:UpdateService",
      "ecs:DescribeServices"
    ]
    resources = [
      "arn:aws:ecs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:service/${local.name_prefix}-cluster/${local.name_prefix}-service"
    ]
  }
}

resource "aws_iam_role_policy" "github_actions_prod_deploy" {
  name   = "github-actions-prod-deploy"
  role   = aws_iam_role.github_actions_prod_deploy.id
  policy = data.aws_iam_policy_document.github_actions_prod_deploy.json
}

module "vpc" {
  source      = "../../modules/vpc"
  name_prefix = local.name_prefix
  environment = "prod"
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
  environment             = "prod"
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
  source              = "../../modules/rds"
  name_prefix         = local.name_prefix
  vpc_id              = module.vpc.vpc_id
  private_subnet_ids  = module.vpc.private_subnet_ids
  allowed_cidr_blocks = ["10.0.0.0/16"]
  db_name             = var.db_name
  db_username         = var.db_username
  db_password         = var.db_password
  instance_class      = var.db_instance_class
  multi_az            = false
  deletion_protection = true
  skip_final_snapshot = false
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
  stage_name   = "prod"
}
