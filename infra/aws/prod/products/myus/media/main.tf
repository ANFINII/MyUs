###
### media
###

terraform {
  backend "s3" {
    bucket       = "terraform-myus-prod"
    key          = "products/myus/media/terraform.tfstate"
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

data "aws_cloudfront_cache_policy" "caching_optimized" {
  name = "Managed-CachingOptimized"
}

data "aws_cloudfront_response_headers_policy" "simple_cors" {
  name = "Managed-SimpleCORS"
}

resource "aws_cloudfront_origin_access_control" "media" {
  name                              = "media-${local.p.env}"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

module "media" {
  source = "../../../../modules/cloudfront-oac"

  bucket_name                         = "${local.p.base_name}-media"
  domain_name                         = "media.${local.p.domain}"
  acm_certificate_arn                 = local.acm.cloudfront_certificate_arn
  cloudfront_origin_access_control_id = aws_cloudfront_origin_access_control.media.id
  cache_policy_id                     = data.aws_cloudfront_cache_policy.caching_optimized.id
  response_headers_policy_id          = data.aws_cloudfront_response_headers_policy.simple_cors.id
}
