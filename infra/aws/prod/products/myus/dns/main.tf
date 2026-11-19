###
### dns
###

terraform {
  backend "s3" {
    bucket       = "terraform-myus-prod"
    key          = "products/myus/dns/terraform.tfstate"
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

data "aws_route53_zone" "main" {
  name = local.p.domain
}

resource "aws_route53_record" "api_a" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = local.api.domain_name
  type    = "A"

  alias {
    name                   = local.api.cloudfront_domain_name
    zone_id                = local.api.cloudfront_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "api_aaaa" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = local.api.domain_name
  type    = "AAAA"

  alias {
    name                   = local.api.cloudfront_domain_name
    zone_id                = local.api.cloudfront_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "media_a" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = local.media.domain_name
  type    = "A"

  alias {
    name                   = local.media.cloudfront_domain_name
    zone_id                = local.media.cloudfront_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "media_aaaa" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = local.media.domain_name
  type    = "AAAA"

  alias {
    name                   = local.media.cloudfront_domain_name
    zone_id                = local.media.cloudfront_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "frontend" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = local.p.domain
  type    = "A"
  ttl     = 300
  records = [local.vercel_ip]
}

resource "aws_route53_record" "frontend_www" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = "www.${local.p.domain}"
  type    = "CNAME"
  ttl     = 300
  records = [local.vercel_cname]
}
