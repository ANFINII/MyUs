variable "emails_for_alarm" {
  description = "アラームを通知するメールアドレス。公開リポジトリなので terraform.tfvars（Git 管理外）か TF_VAR_emails_for_alarm で渡す"
  type        = list(string)
  sensitive   = true
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

  # database variables
  mysql = data.terraform_remote_state.database.outputs.mysql

  # compute variables
  api = data.terraform_remote_state.compute.outputs.api

  name = "myus-${local.p.env}"
}
