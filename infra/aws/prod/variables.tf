locals {
  env       = "prod"
  region    = "ap-northeast-1"
  base_name = "myus-prod"
}

locals {
  params = {
    base_name = local.base_name
    env       = local.env
    region    = local.region
    profile   = local.base_name
  }
}
