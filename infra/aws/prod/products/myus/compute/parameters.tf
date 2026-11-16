locals {
  parameters = {
    DOMAIN_URL              = "https://${aws_cloudfront_distribution.api.domain_name}"
    MYSQL_HOST              = local.mysql.host
    MYSQL_PORT              = tostring(local.mysql.port)
    MYSQL_DATABASE          = local.mysql.database
    MYSQL_USER              = local.mysql.user
    AWS_STORAGE_BUCKET_NAME = local.media.bucket_name
    AWS_S3_REGION_NAME      = local.p.region
    MEDIA_DOMAIN            = local.media.domain_name
  }
}

resource "aws_ssm_parameter" "api" {
  for_each = local.parameters

  name  = "${local.parameter_store_name_prefix}${each.key}"
  type  = "String"
  value = each.value

  tags = {
    Name = "${local.parameter_store_name_prefix}${each.key}"
  }
}
