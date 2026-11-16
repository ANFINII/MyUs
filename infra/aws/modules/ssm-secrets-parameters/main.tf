resource "aws_ssm_parameter" "this" {
  for_each = toset(var.secret_parameters)

  key_id = var.key_id

  name             = "${local.parameter_store_name_prefix}${each.value}"
  type             = "SecureString"
  value_wo         = "FIXME"
  value_wo_version = 1

  tags = {
    Name = "${local.parameter_store_name_prefix}${each.value}"
  }
}
