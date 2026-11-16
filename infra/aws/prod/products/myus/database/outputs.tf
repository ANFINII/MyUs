output "mysql" {
  value = {
    identifier              = aws_db_instance.main.identifier
    host                    = aws_db_instance.main.address
    port                    = aws_db_instance.main.port
    database                = aws_db_instance.main.db_name
    user                    = aws_db_instance.main.username
    password_parameter_name = aws_ssm_parameter.mysql_password.name
    password_parameter_arn  = aws_ssm_parameter.mysql_password.arn
  }
}
