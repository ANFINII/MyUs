data "terraform_remote_state" "media" {
  backend = "s3"

  config = {
    bucket  = "terraform-myus-prod"
    key     = "products/myus/media/terraform.tfstate"
    region  = "ap-northeast-1"
    profile = "myus-prod"
  }
}

data "terraform_remote_state" "frontend" {
  backend = "s3"

  config = {
    bucket  = "terraform-myus-prod"
    key     = "products/myus/frontend/terraform.tfstate"
    region  = "ap-northeast-1"
    profile = "myus-prod"
  }
}

data "terraform_remote_state" "compute" {
  backend = "s3"

  config = {
    bucket  = "terraform-myus-prod"
    key     = "products/myus/compute/terraform.tfstate"
    region  = "ap-northeast-1"
    profile = "myus-prod"
  }
}

locals {
  # params module variables
  p = module.params.params

  # media variables
  media = data.terraform_remote_state.media.outputs.media

  # frontend variables
  frontend = data.terraform_remote_state.frontend.outputs.frontend

  # compute variables
  api = data.terraform_remote_state.compute.outputs.api
}
