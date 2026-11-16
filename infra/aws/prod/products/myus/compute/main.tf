###
### compute
###

terraform {
  backend "s3" {
    bucket       = "terraform-myus-prod"
    key          = "products/myus/compute/terraform.tfstate"
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
  source = "../../.."
}

data "aws_caller_identity" "current" {}
