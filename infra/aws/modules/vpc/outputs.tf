output "vpc_id" {
  value = aws_vpc.main.id
}

output "cidr_block" {
  value = aws_vpc.main.cidr_block
}

output "public_subnet_ids" {
  value = { for k, s in aws_subnet.public : k => s.id }
}

output "datastore_subnet_ids" {
  value = { for k, s in aws_subnet.datastore : k => s.id }
}

output "app_subnet_ids" {
  value = { for k, s in aws_subnet.app : k => s.id }
}

output "app_route_table_id" {
  value = aws_route_table.app.id
}
