###
### parameters
###

terraform {
  backend "s3" {
    bucket       = "terraform-myus-prod"
    key          = "common/parameters/terraform.tfstate"
    region       = "ap-northeast-1"
    use_lockfile = true
    profile      = "myus-prod"
  }
  required_version = ">= 1.14.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.33.0"
    }
  }
}

provider "aws" {
  region  = local.p.region
  profile = local.p.profile

  default_tags {
    tags = {
      Env       = local.p.env
      Product   = "myus"
      ManagedBy = "terraform"
    }
  }
}

module "params" {
  source = "../.."
}

module "ssm_secrets_parameters" {
  source = "../../../modules/ssm-secrets-parameters"

  product_name = "myus"
  env          = local.p.env
  key_id       = "alias/aws/ssm"

  secret_parameters = [
    "SECRET_KEY",
    "REDIS_PASSWORD",
    "EMAIL_HOST_USER",
    "EMAIL_HOST_PASSWORD",
    "STRIPE_SECRET_KEY",
    "STRIPE_WEBHOOK_SECRET",
    "STRIPE_PUBLIC_KEY",
    "STRIPE_PRICE_ID_BASIC",
    "STRIPE_PRICE_ID_STANDARD",
    "STRIPE_PRICE_ID_PREMIUM",
    "ALLOWED_HOSTS",
    "CORS_ALLOWED_ORIGINS",
    "CSRF_TRUSTED_ORIGINS",
    "FRONTEND_URL",
    "EMAIL_HOST",
    "EMAIL_PORT",
    "EMAIL_FROM",
  ]
}
