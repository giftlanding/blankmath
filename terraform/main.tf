resource "random_password" "internal_api_token" {
  length  = 48
  special = false
}

resource "aws_s3_bucket" "generated_pdfs" {
  bucket        = var.generated_pdfs_domain_name
  force_destroy = true

  tags = local.common_tags
}

resource "aws_s3_bucket_public_access_block" "generated_pdfs" {
  bucket = aws_s3_bucket.generated_pdfs.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = true
  restrict_public_buckets = false
}

data "aws_iam_policy_document" "generated_pdfs_public_read" {
  statement {
    sid = "PublicReadGeneratedPdfs"

    actions = ["s3:GetObject"]

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    resources = ["${aws_s3_bucket.generated_pdfs.arn}/*"]
  }
}

resource "aws_s3_bucket_policy" "generated_pdfs_public_read" {
  bucket = aws_s3_bucket.generated_pdfs.id
  policy = data.aws_iam_policy_document.generated_pdfs_public_read.json

  depends_on = [aws_s3_bucket_public_access_block.generated_pdfs]
}

resource "aws_s3_bucket_server_side_encryption_configuration" "generated_pdfs" {
  bucket = aws_s3_bucket.generated_pdfs.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "generated_pdfs" {
  bucket = aws_s3_bucket.generated_pdfs.id

  rule {
    id     = "expire-generated-pdfs"
    status = "Enabled"

    filter {
      prefix = ""
    }

    expiration {
      days = var.pdf_retention_days
    }
  }
}

resource "aws_cloudwatch_log_group" "pdf_generator" {
  name              = "/aws/lambda/${local.name_prefix}-pdf-generator"
  retention_in_days = 14

  tags = local.common_tags
}

data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "pdf_generator" {
  name               = "${local.name_prefix}-pdf-generator"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json

  tags = local.common_tags
}

data "aws_iam_policy_document" "pdf_generator" {
  statement {
    sid = "WriteGeneratedPdfs"

    actions = [
      "s3:PutObject",
      "s3:GetObject",
      "s3:DeleteObject",
    ]

    resources = ["${aws_s3_bucket.generated_pdfs.arn}/*"]
  }

  statement {
    sid = "WriteLogs"

    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = ["${aws_cloudwatch_log_group.pdf_generator.arn}:*"]
  }
}

resource "aws_iam_role_policy" "pdf_generator" {
  name   = "${local.name_prefix}-pdf-generator"
  role   = aws_iam_role.pdf_generator.id
  policy = data.aws_iam_policy_document.pdf_generator.json
}

resource "aws_iam_user" "github_action" {
  name = "blankmath_github_action_user"

  tags = local.common_tags
}

data "aws_iam_policy_document" "github_action_lambda_deploy" {
  statement {
    sid = "DeployPdfGeneratorLambdaCode"

    actions = [
      "lambda:UpdateFunctionCode",
    ]

    resources = [aws_lambda_function.pdf_generator.arn]
  }
}

resource "aws_iam_user_policy" "github_action_lambda_deploy" {
  name   = "${local.name_prefix}-github-action-lambda-deploy"
  user   = aws_iam_user.github_action.name
  policy = data.aws_iam_policy_document.github_action_lambda_deploy.json
}

data "archive_file" "pdf_generator" {
  type        = "zip"
  source_dir  = "${path.module}/bootstrap/pdf_generator"
  output_path = "${path.module}/pdf_generator.zip"
}

resource "aws_lambda_function" "pdf_generator" {
  function_name = "${local.name_prefix}-pdf-generator"
  role          = aws_iam_role.pdf_generator.arn
  handler       = "handler.handler"
  runtime       = "python3.12"

  filename         = data.archive_file.pdf_generator.output_path
  source_code_hash = data.archive_file.pdf_generator.output_base64sha256

  memory_size = 256
  timeout     = 30

  reserved_concurrent_executions = var.lambda_reserved_concurrency

  environment {
    variables = {
      GENERATED_PDFS_BUCKET = aws_s3_bucket.generated_pdfs.bucket
      GENERATED_PDFS_PUBLIC_BASE_URL = "https://${var.generated_pdfs_domain_name}"
      INTERNAL_API_TOKEN    = random_password.internal_api_token.result
    }
  }

  depends_on = [
    aws_cloudwatch_log_group.pdf_generator,
    aws_iam_role_policy.pdf_generator,
  ]

  lifecycle {
    ignore_changes = [
      filename,
      source_code_hash,
    ]
  }

  tags = local.common_tags
}

resource "aws_lambda_function_url" "pdf_generator" {
  function_name      = aws_lambda_function.pdf_generator.function_name
  authorization_type = "NONE"

  cors {
    allow_credentials = false
    allow_headers     = ["content-type"]
    allow_methods     = ["POST"]
    allow_origins     = ["https://${var.domain_name}", "https://www.${var.domain_name}"]
    max_age           = 300
  }
}

resource "cloudflare_pages_project" "frontend" {
  account_id        = var.cloudflare_account_id
  name              = var.cloudflare_pages_project_name
  production_branch = "main"

  build_config = {
    build_caching   = true
    build_command   = "npm run build"
    destination_dir = "dist"
    root_dir        = "frontend"
  }

  source = {
    type = "github"
    config = {
      owner                          = "giftlanding"
      repo_name                      = "blankmath"
      production_branch              = "main"
      production_deployments_enabled = true
      preview_deployment_setting     = "none"
      pr_comments_enabled            = false
      path_includes                  = ["frontend/**"]
    }
  }

  deployment_configs = {
    preview = {
      fail_open = true
    }

    production = {
      fail_open = true

      env_vars = {
        LAMBDA_FUNCTION_URL = {
          type  = "plain_text"
          value = aws_lambda_function_url.pdf_generator.function_url
        }
        INTERNAL_API_TOKEN = {
          type  = "secret_text"
          value = random_password.internal_api_token.result
        }
      }
    }
  }
}

resource "cloudflare_pages_domain" "apex" {
  account_id   = var.cloudflare_account_id
  project_name = cloudflare_pages_project.frontend.name
  name         = var.domain_name
}

resource "cloudflare_pages_domain" "www" {
  account_id   = var.cloudflare_account_id
  project_name = cloudflare_pages_project.frontend.name
  name         = "www.${var.domain_name}"
}

resource "cloudflare_dns_record" "apex" {
  zone_id = var.cloudflare_zone_id
  name    = var.domain_name
  type    = "CNAME"
  content = cloudflare_pages_project.frontend.subdomain
  ttl     = 1
  proxied = true

  comment = "Managed by OpenTofu for Cloudflare Pages."

  depends_on = [cloudflare_pages_domain.apex]
}

resource "cloudflare_dns_record" "www" {
  zone_id = var.cloudflare_zone_id
  name    = "www.${var.domain_name}"
  type    = "CNAME"
  content = cloudflare_pages_project.frontend.subdomain
  ttl     = 1
  proxied = true

  comment = "Managed by OpenTofu for Cloudflare Pages."

  depends_on = [cloudflare_pages_domain.www]
}

resource "cloudflare_dns_record" "generated_pdfs" {
  zone_id = var.cloudflare_zone_id
  name    = var.generated_pdfs_domain_name
  type    = "CNAME"
  content = aws_s3_bucket.generated_pdfs.bucket_regional_domain_name
  ttl     = 1
  proxied = true

  comment = "Managed by OpenTofu for public generated PDFs."
}
