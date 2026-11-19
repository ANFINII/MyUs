data "terraform_remote_state" "acm" {
  backend = "s3"

  config = {
    bucket  = "terraform-myus-prod"
    key     = "common/acm/terraform.tfstate"
    region  = "ap-northeast-1"
    profile = "myus-prod"
  }
}

locals {
  # params module variables
  p = module.params.params

  # acm variables
  acm = data.terraform_remote_state.acm.outputs.acm
}
