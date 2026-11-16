output "ssm_secret_parameters" {
  value = module.ssm_secrets_parameters.ssm_secret_parameters
}

output "parameter_store_name_prefix" {
  value = module.ssm_secrets_parameters.parameter_store_name_prefix
}
