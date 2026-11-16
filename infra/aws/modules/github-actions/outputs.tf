output "role_arns" {
  value = { for name, role in aws_iam_role.github_actions : name => role.arn }
}
