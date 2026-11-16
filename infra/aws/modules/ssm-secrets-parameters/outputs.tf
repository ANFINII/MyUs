output "ssm_secret_parameters" {
  value = {
    for k, v in aws_ssm_parameter.this : v.name => {
      arn = v.arn
    }
  }
}

output "parameter_store_name_prefix" {
  value = local.parameter_store_name_prefix
}
