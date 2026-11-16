resource "aws_vpc" "main" {
  cidr_block           = "${var.vpc_cidr16}.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = var.name
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = var.name
  }
}

###
# public: インターネットゲートウェイに出られるサブネット
###
resource "aws_subnet" "public" {
  for_each = local.public_subnets

  vpc_id                  = aws_vpc.main.id
  availability_zone       = each.value.availability_zone
  cidr_block              = each.value.cidr_block
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.name}-public-${each.key}"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${var.name}-public"
  }
}

resource "aws_route_table_association" "public" {
  for_each = aws_subnet.public

  subnet_id      = each.value.id
  route_table_id = aws_route_table.public.id
}

###
# datastore: VPC の外に出られないサブネット
###
resource "aws_subnet" "datastore" {
  for_each = local.datastore_subnets

  vpc_id            = aws_vpc.main.id
  availability_zone = each.value.availability_zone
  cidr_block        = each.value.cidr_block

  tags = {
    Name = "${var.name}-datastore-${each.key}"
  }
}

resource "aws_route_table" "datastore" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.name}-datastore"
  }
}

resource "aws_route_table_association" "datastore" {
  for_each = aws_subnet.datastore

  subnet_id      = each.value.id
  route_table_id = aws_route_table.datastore.id
}
