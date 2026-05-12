output "generated_pdfs_bucket_name" {
  description = "Private S3 bucket for temporary generated PDFs."
  value       = aws_s3_bucket.generated_pdfs.bucket
}

output "generated_pdfs_public_url" {
  description = "Public custom-domain base URL for generated PDFs."
  value       = "https://${var.generated_pdfs_domain_name}"
}

output "lambda_function_name" {
  description = "PDF generator Lambda function name."
  value       = aws_lambda_function.pdf_generator.function_name
}

output "lambda_function_url" {
  description = "Raw Lambda Function URL. Do not expose this directly in browser code."
  value       = aws_lambda_function_url.pdf_generator.function_url
  sensitive   = true
}

output "github_action_iam_user_name" {
  description = "IAM user for the GitHub Actions backend deployment credentials."
  value       = aws_iam_user.github_action.name
}

output "github_action_iam_user_arn" {
  description = "IAM user ARN for the GitHub Actions backend deployment credentials."
  value       = aws_iam_user.github_action.arn
}

output "cloudflare_pages_project_name" {
  description = "Cloudflare Pages project name."
  value       = cloudflare_pages_project.frontend.name
}

output "cloudflare_pages_subdomain" {
  description = "Cloudflare Pages project subdomain."
  value       = cloudflare_pages_project.frontend.subdomain
}

output "website_url" {
  description = "Primary website URL."
  value       = "https://${var.domain_name}"
}
