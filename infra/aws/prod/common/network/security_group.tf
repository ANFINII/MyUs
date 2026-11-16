###
# api: CloudFront からの HTTP だけを受ける
###
data "aws_ec2_managed_prefix_list" "cloudfront_origin_facing" {
  name = "com.amazonaws.global.cloudfront.origin-facing"
}

resource "aws_security_group" "api" {
  name        = "api-${local.p.env}"
  description = "Security Group for API"
  vpc_id      = local.vpc.vpc_id

  tags = {
    Name = "api-${local.p.env}"
  }
}

resource "aws_vpc_security_group_ingress_rule" "api_from_cloudfront_http" {
  security_group_id = aws_security_group.api.id
  prefix_list_id    = data.aws_ec2_managed_prefix_list.cloudfront_origin_facing.id
  ip_protocol       = "tcp"
  from_port         = 80
  to_port           = 80
}

resource "aws_vpc_security_group_egress_rule" "api_to_all" {
  security_group_id = aws_security_group.api.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

###
# database: api からの MySQL だけを受ける
###
resource "aws_security_group" "database" {
  name        = "database-${local.p.env}"
  description = "Security Group for Database"
  vpc_id      = local.vpc.vpc_id

  tags = {
    Name = "database-${local.p.env}"
  }
}

resource "aws_vpc_security_group_ingress_rule" "database_from_api_mysql" {
  security_group_id            = aws_security_group.database.id
  referenced_security_group_id = aws_security_group.api.id
  ip_protocol                  = "tcp"
  from_port                    = 3306
  to_port                      = 3306
}
