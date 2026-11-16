data "terraform_remote_state" "network" {
  backend = "s3"

  config = {
    bucket  = "terraform-myus-prod"
    key     = "common/network/terraform.tfstate"
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
}
