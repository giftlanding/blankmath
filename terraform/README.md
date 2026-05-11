# Blankmath Infrastructure

This folder contains the production infrastructure for the Blankmath rewrite.

## Runtime

- OpenTofu `1.11.6`
- AWS provider
- Cloudflare provider
- Spacelift-managed state

## Required Environment Variables

Spacelift should provide these values:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `CLOUDFLARE_API_TOKEN`
- `TF_VAR_cloudflare_account_id`
- `TF_VAR_cloudflare_zone_id`

Optional:

- `TF_VAR_aws_region`, defaults to `us-east-1`

## Current Architecture

The initial production architecture is intentionally small and scale-to-zero:

- Cloudflare Pages project for the frontend.
- Cloudflare custom domains for `blankmath.com` and `www.blankmath.com`.
- AWS Lambda placeholder for PDF generation.
- Lambda Function URL for the backend endpoint.
- Private S3 bucket for generated PDFs.
- S3 lifecycle expiration for generated PDFs.
- Random internal API token shared by Cloudflare Pages Functions and Lambda.

The browser should eventually call a Cloudflare Pages Function at `/api/generate`.
The Pages Function will validate the request and call the Lambda Function URL with
the internal token. The raw Lambda Function URL should not be exposed to browser
code.

## Notes

- Terraform creates infrastructure only. Application builds and deployments should
  be handled by Cloudflare Pages and backend deployment workflows.
- The Lambda is created from a small Terraform-owned bootstrap package. Real backend
  code is deployed by `.github/workflows/deploy-backend.yml`.
- Generated PDFs are private S3 objects and should be returned to users through
  presigned URLs.
