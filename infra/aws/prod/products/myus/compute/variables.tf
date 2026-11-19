data "terraform_remote_state" "acm" {
  backend = "s3"

  config = {
    bucket  = "terraform-myus-prod"
    key     = "common/acm/terraform.tfstate"
    region  = "ap-northeast-1"
    profile = "myus-prod"
  }
}

data "terraform_remote_state" "network" {
  backend = "s3"

  config = {
    bucket  = "terraform-myus-prod"
    key     = "common/network/terraform.tfstate"
    region  = "ap-northeast-1"
    profile = "myus-prod"
  }
}

data "terraform_remote_state" "parameters" {
  backend = "s3"

  config = {
    bucket  = "terraform-myus-prod"
    key     = "common/parameters/terraform.tfstate"
    region  = "ap-northeast-1"
    profile = "myus-prod"
  }
}

data "terraform_remote_state" "database" {
  backend = "s3"

  config = {
    bucket  = "terraform-myus-prod"
    key     = "products/myus/database/terraform.tfstate"
    region  = "ap-northeast-1"
    profile = "myus-prod"
  }
}

data "terraform_remote_state" "media" {
  backend = "s3"

  config = {
    bucket  = "terraform-myus-prod"
    key     = "products/myus/media/terraform.tfstate"
    region  = "ap-northeast-1"
    profile = "myus-prod"
  }
}

locals {
  # params module variables
  p = module.params.params

  # network variables
  vpc                = data.terraform_remote_state.network.outputs.vpc
  security_group_ids = data.terraform_remote_state.network.outputs.security_group_ids

  # parameters variables
  parameter_store_name_prefix = data.terraform_remote_state.parameters.outputs.parameter_store_name_prefix

  # database variables
  mysql = data.terraform_remote_state.database.outputs.mysql

  # acm variables
  acm = data.terraform_remote_state.acm.outputs.acm

  # media variables
  media = data.terraform_remote_state.media.outputs.media
  hires = data.terraform_remote_state.media.outputs.hires

  compose_version = "v5.6.1"
}
