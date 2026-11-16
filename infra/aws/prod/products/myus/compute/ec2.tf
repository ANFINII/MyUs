data "aws_ssm_parameter" "al2023_arm64" {
  name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-arm64"
}

resource "aws_instance" "api" {
  ami                    = data.aws_ssm_parameter.al2023_arm64.insecure_value
  instance_type          = "t4g.small"
  subnet_id              = local.vpc.public_subnet_ids.a
  vpc_security_group_ids = [local.security_group_ids.api]
  iam_instance_profile   = aws_iam_instance_profile.api.name

  credit_specification {
    cpu_credits = "standard"
  }

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 2
  }

  root_block_device {
    volume_type = "gp3"
    volume_size = 30
    encrypted   = true
  }

  user_data = templatefile("${path.module}/user_data/cloud-init.yml", {
    compose_version = local.compose_version
  })

  lifecycle {
    ignore_changes = [ami, user_data]
  }

  tags = {
    Name = "myus-api-${local.p.env}"
  }
}

resource "aws_eip" "api" {
  instance = aws_instance.api.id
  domain   = "vpc"

  tags = {
    Name = "myus-api-${local.p.env}"
  }
}
