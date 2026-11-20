data "aws_ami" "fck_nat" {
  most_recent = true
  owners      = ["568608671756"]

  filter {
    name   = "name"
    values = ["fck-nat-al2023-*-arm64-ebs"]
  }
}

resource "aws_instance" "nat" {
  ami                    = data.aws_ami.fck_nat.id
  instance_type          = "t4g.nano"
  subnet_id              = local.vpc.public_subnet_ids.a
  vpc_security_group_ids = [aws_security_group.nat.id]
  source_dest_check      = false

  credit_specification {
    cpu_credits = "standard"
  }

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
  }

  root_block_device {
    volume_type = "gp3"
    encrypted   = true
  }

  lifecycle {
    ignore_changes = [ami]
  }

  tags = {
    Name = "${local.p.base_name}-nat"
  }
}

resource "aws_route" "app_to_nat" {
  route_table_id         = local.vpc.app_route_table_id
  destination_cidr_block = "0.0.0.0/0"
  network_interface_id   = aws_instance.nat.primary_network_interface_id
}
