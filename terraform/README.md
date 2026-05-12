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

## GitHub Actions AWS Credentials

The backend deployment workflow uses GitHub Actions secrets named
`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`. Those credentials should belong
to the Terraform-managed IAM user `blankmath_github_action_user`.

That IAM user is only allowed to update the code package for the production PDF
generator Lambda function. It is separate from the AWS credentials used by
Spacelift to manage infrastructure.

Create an access key for `blankmath_github_action_user` in AWS IAM, then store
that key pair in the GitHub repository secrets used by
`.github/workflows/deploy-backend.yml`. Do not reuse the broader Spacelift AWS
credentials for GitHub Actions.

## Current Architecture

The initial production architecture is intentionally small and scale-to-zero:

- Cloudflare Pages project for the frontend.
- Cloudflare custom domains for `blankmath.com` and `www.blankmath.com`.
- AWS Lambda placeholder for PDF generation.
- Lambda Function URL for the backend endpoint.
- Public S3 bucket for generated PDFs at `https://r.blankmath.com`.
- Cloudflare DNS for the generated PDF domain.
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
- Generated PDFs are public S3 objects returned through `https://r.blankmath.com`.
  They are temporary and expire through the S3 lifecycle policy.
