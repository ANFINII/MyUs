data "terraform_remote_state" "media" {
  backend = "s3"

  config = {
    bucket  = "terraform-myus-prod"
    key     = "products/myus/media/terraform.tfstate"
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

  # compute variables
  api = data.terraform_remote_state.compute.outputs.api

  # Vercel
  vercel_ip    = "76.76.21.21"
  vercel_cname = "cname.vercel-dns.com"
}
