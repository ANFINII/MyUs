variable "name" {
  description = "VPC とサブネットなどの名前"
  type        = string
}

variable "region" {
  type = string
}

variable "vpc_cidr16" {
  description = "VPC の CIDR の上位 2 オクテット (例: 10.0)"
  type        = string
}

locals {
  public_subnets = {
    a = { availability_zone = "${var.region}a", cidr_block = "${var.vpc_cidr16}.0.0/24" }
    c = { availability_zone = "${var.region}c", cidr_block = "${var.vpc_cidr16}.1.0/24" }
  }

  datastore_subnets = {
    a = { availability_zone = "${var.region}a", cidr_block = "${var.vpc_cidr16}.10.0/24" }
    c = { availability_zone = "${var.region}c", cidr_block = "${var.vpc_cidr16}.11.0/24" }
  }
}
