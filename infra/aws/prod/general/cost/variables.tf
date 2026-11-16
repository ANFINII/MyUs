variable "emails_for_cost" {
  description = "予算の超過と異常を通知するメールアドレス。公開リポジトリなので terraform.tfvars（Git 管理外）か TF_VAR_emails_for_cost で渡す"
  type        = list(string)
}

locals {
  # params module variables
  p = module.params.params
}
