terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
    null = {
      source = "hashicorp/null"
    }
  }
}

locals {
  build_dir        = abspath("${path.root}/.terraform/lambda-build/${var.function_name}")
  package_dir      = "${local.build_dir}/package"
  source_file      = "${path.module}/lambda/configparser_lambdafunction.py"
  requirements_file = "${path.module}/lambda/requirements.txt"
  zip_file         = "${local.build_dir}/function.zip"
}

data "aws_iam_policy_document" "lambda_assume" {
  statement {
    effect = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_region" "current" {}

data "aws_subnet" "selected" {
  id = var.subnet_ids[0]
}

data "aws_route_tables" "vpc" {
  vpc_id = data.aws_subnet.selected.vpc_id
}

resource "aws_iam_role" "lambda" {
  name               = "${var.function_name}-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

resource "aws_iam_role_policy_attachment" "managed" {
  for_each = toset([
    "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole",
    "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess",
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
  ])

  role       = aws_iam_role.lambda.name
  policy_arn = each.value
}

resource "null_resource" "build_package" {
  triggers = {
    source_sha       = filesha256(local.source_file)
    requirements_sha = filesha256(local.requirements_file)
    runtime          = var.runtime
  }

  provisioner "local-exec" {
    interpreter = ["/bin/bash", "-c"]
    command     = <<-EOT
      set -euo pipefail
      rm -rf "${local.build_dir}"
      mkdir -p "${local.package_dir}"

      python3 -m pip install --quiet --target "${local.package_dir}" -r "${local.requirements_file}"
      cp "${local.source_file}" "${local.build_dir}/configparser_lambdafunction.py"

      cd "${local.package_dir}"
      zip -qr "${local.zip_file}" .

      cd "${local.build_dir}"
      zip -qg "${local.zip_file}" configparser_lambdafunction.py
    EOT
  }
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${var.function_name}"
  retention_in_days = var.log_retention_days
}

resource "aws_vpc_endpoint" "s3" {
  count = var.create_s3_vpc_endpoint ? 1 : 0

  vpc_id            = data.aws_subnet.selected.vpc_id
  service_name      = "com.amazonaws.${data.aws_region.current.name}.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = data.aws_route_tables.vpc.ids
}

resource "aws_lambda_function" "config_parser" {
  function_name = var.function_name
  description   = var.description
  role          = aws_iam_role.lambda.arn
  runtime       = var.runtime
  handler       = "configparser_lambdafunction.lambda_handler"

  filename         = local.zip_file

  timeout     = var.timeout
  memory_size = var.memory_size

  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = var.security_group_ids
  }

  environment {
    variables = {
      CLUSTER_ENDPOINT = var.cluster_endpoint
      CLUSTER_PORT     = tostring(var.cluster_port)
    }
  }

  depends_on = [
    null_resource.build_package,
    aws_cloudwatch_log_group.lambda,
    aws_iam_role_policy_attachment.managed,
    aws_vpc_endpoint.s3,
  ]

  lifecycle {
    replace_triggered_by = [null_resource.build_package]
  }
}

resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowExecutionFromS3-${var.function_name}"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.config_parser.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::${var.s3_bucket_name}"
}

resource "aws_s3_bucket_notification" "config_delivery" {
  bucket = var.s3_bucket_name

  lambda_function {
    lambda_function_arn = aws_lambda_function.config_parser.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = var.s3_key_prefix != "" ? var.s3_key_prefix : null
    filter_suffix       = ".gz"
  }

  depends_on = [aws_lambda_permission.allow_s3]
}
