###
### acm
###

terraform {
  backend "s3" {
    bucket       = "terraform-myus-prod"
    key          = "common/acm/terraform.tfstate"
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

provider "aws" {
  alias   = "nvirginia"
  region  = "us-east-1"
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

data "aws_route53_zone" "main" {
  name = local.p.domain
}

resource "aws_acm_certificate" "cloudfront" {
  provider = aws.nvirginia

  domain_name               = local.p.domain
  subject_alternative_names = ["*.${local.p.domain}"]
  validation_method         = "DNS"

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name = local.p.domain
  }
}

resource "aws_route53_record" "cloudfront_validation" {
  for_each = {
    for dvo in aws_acm_certificate.cloudfront.domain_validation_options : dvo.resource_record_name => dvo...
  }

  zone_id         = data.aws_route53_zone.main.zone_id
  name            = each.value[0].resource_record_name
  type            = each.value[0].resource_record_type
  ttl             = 300
  records         = [each.value[0].resource_record_value]
  allow_overwrite = true
}

resource "aws_acm_certificate_validation" "cloudfront" {
  provider = aws.nvirginia

  certificate_arn         = aws_acm_certificate.cloudfront.arn
  validation_record_fqdns = [for record in aws_route53_record.cloudfront_validation : record.fqdn]
}
