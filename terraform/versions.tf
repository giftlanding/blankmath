terraform {
  required_version = "~> 1.11.6"

  required_providers {
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.7"
    }

    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }

    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 5.19"
    }

    random = {
      source  = "hashicorp/random"
      version = "~> 3.7"
    }
  }
}
