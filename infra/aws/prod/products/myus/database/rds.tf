resource "aws_db_subnet_group" "main" {
  name       = "myus-${local.p.env}"
  subnet_ids = values(local.vpc.datastore_subnet_ids)

  tags = {
    Name = "myus-${local.p.env}"
  }
}

resource "aws_db_parameter_group" "mysql84" {
  name   = "myus-mysql84-${local.p.env}"
  family = "mysql8.4"

  parameter {
    name  = "character_set_server"
    value = "utf8mb4"
  }

  parameter {
    name  = "collation_server"
    value = "utf8mb4_unicode_ci"
  }

  parameter {
    name  = "sql_mode"
    value = "ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION"
  }

  tags = {
    Name = "myus-mysql84-${local.p.env}"
  }
}

ephemeral "random_password" "mysql" {
  length  = 32
  special = false
}

resource "aws_db_instance" "main" {
  identifier = "myus-${local.p.env}"

  engine                     = "mysql"
  engine_version             = "8.4"
  auto_minor_version_upgrade = true
  instance_class             = "db.t4g.micro"
  parameter_group_name       = aws_db_parameter_group.mysql84.name

  allocated_storage     = 20
  max_allocated_storage = 50
  storage_type          = "gp3"
  storage_encrypted     = true

  db_name             = "myus"
  username            = "myus"
  password_wo         = ephemeral.random_password.mysql.result
  password_wo_version = 1

  multi_az               = false
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [local.security_group_ids.database]
  publicly_accessible    = false

  backup_retention_period = 7
  backup_window           = local.p.backup_window
  maintenance_window      = local.p.maintenance_window
  copy_tags_to_snapshot   = true

  deletion_protection       = true
  skip_final_snapshot       = false
  final_snapshot_identifier = "myus-${local.p.env}-final"

  tags = {
    Name = "myus-${local.p.env}"
  }
}

resource "aws_ssm_parameter" "mysql_password" {
  name             = "/myus/${local.p.env}/MYSQL_PASSWORD"
  type             = "SecureString"
  key_id           = "alias/aws/ssm"
  value_wo         = ephemeral.random_password.mysql.result
  value_wo_version = 1

  tags = {
    Name = "/myus/${local.p.env}/MYSQL_PASSWORD"
  }
}
