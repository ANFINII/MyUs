###
### network
###

terraform {
  backend "s3" {
    bucket       = "terraform-myus-prod"
    key          = "common/network/terraform.tfstate"
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
      Product   = "common"
      ManagedBy = "terraform"
    }
  }
}

module "params" {
  source = "../.."
}

module "vpc" {
  source = "../../../modules/vpc"

  name       = local.p.base_name
  region     = local.p.region
  vpc_cidr16 = local.p.vpc_cidr16
}
