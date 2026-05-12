variable "project_name" {
  description = "Project name used for resource naming."
  type        = string
  default     = "blankmath"
}

variable "environment" {
  description = "Single deployment environment for this project."
  type        = string
  default     = "prod"
}

variable "aws_region" {
  description = "AWS region for Lambda and S3 resources."
  type        = string
  default     = "us-east-1"
}

variable "domain_name" {
  description = "Primary public domain."
  type        = string
  default     = "blankmath.com"
}

variable "generated_pdfs_domain_name" {
  description = "Public custom domain for generated PDF objects."
  type        = string
  default     = "r.blankmath.com"
}

variable "cloudflare_account_id" {
  description = "Cloudflare account ID."
  type        = string
  sensitive   = true
}

variable "cloudflare_zone_id" {
  description = "Cloudflare zone ID for the primary domain."
  type        = string
  sensitive   = true
}

variable "pdf_retention_days" {
  description = "Number of days to retain generated PDFs in S3."
  type        = number
  default     = 1

  validation {
    condition     = var.pdf_retention_days >= 1 && var.pdf_retention_days <= 30
    error_message = "pdf_retention_days must be between 1 and 30."
  }
}

variable "lambda_reserved_concurrency" {
  description = "Reserved concurrency cap for the PDF generator Lambda."
  type        = number
  default     = 2

  validation {
    condition     = var.lambda_reserved_concurrency >= 0 && var.lambda_reserved_concurrency <= 10
    error_message = "lambda_reserved_concurrency must be between 0 and 10."
  }
}

variable "cloudflare_pages_project_name" {
  description = "Cloudflare Pages project name."
  type        = string
  default     = "blankmath"
}
