###
### mail
###

terraform {
  backend "s3" {
    bucket       = "terraform-myus-prod"
    key          = "products/myus/mail/terraform.tfstate"
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

resource "aws_sesv2_email_identity" "main" {
  email_identity = local.p.domain
}

resource "aws_route53_record" "dkim" {
  count = 3

  zone_id = data.aws_route53_zone.main.zone_id
  name    = "${aws_sesv2_email_identity.main.dkim_signing_attributes[0].tokens[count.index]}._domainkey.${local.p.domain}"
  type    = "CNAME"
  ttl     = 300
  records = ["${aws_sesv2_email_identity.main.dkim_signing_attributes[0].tokens[count.index]}.dkim.amazonses.com"]
}

resource "aws_sesv2_email_identity_mail_from_attributes" "main" {
  email_identity         = aws_sesv2_email_identity.main.email_identity
  mail_from_domain       = local.mail_from_domain
  behavior_on_mx_failure = "USE_DEFAULT_VALUE"
}

resource "aws_route53_record" "mail_from_mx" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = local.mail_from_domain
  type    = "MX"
  ttl     = 300
  records = ["10 feedback-smtp.${local.p.region}.amazonses.com"]
}

resource "aws_route53_record" "mail_from_spf" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = local.mail_from_domain
  type    = "TXT"
  ttl     = 300
  records = ["v=spf1 include:amazonses.com ~all"]
}

resource "aws_route53_record" "dmarc" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = "_dmarc.${local.p.domain}"
  type    = "TXT"
  ttl     = 300
  records = ["v=DMARC1; p=none"]
}
