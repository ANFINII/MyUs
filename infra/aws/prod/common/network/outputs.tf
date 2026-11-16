output "vpc" {
  value = module.vpc
}

output "security_group_ids" {
  value = {
    api      = aws_security_group.api.id
    database = aws_security_group.database.id
  }
}
