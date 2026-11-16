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

    vpc_cidr16 = "10.0"

    # UTC。JST の 3:00〜4:00 にバックアップ、日曜 4:00〜5:00 にメンテナンス
    backup_window      = "18:00-19:00"
    maintenance_window = "sat:19:00-sat:20:00"
  }
}
