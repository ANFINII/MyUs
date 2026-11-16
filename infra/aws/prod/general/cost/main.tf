###
### Budgets・Cost Explorer
###

terraform {
  backend "s3" {
    bucket       = "terraform-myus-prod"
    key          = "general/cost/terraform.tfstate"
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

module "common" {
  source = "../../../modules/cost"

  name                          = "common"
  emails                        = var.emails_for_cost
  monthly_limit_dollar          = 60
  cost_anomaly_threshold_dollar = 5
}
