output "repositories" {
  value = {
    for k, v in aws_ecr_repository.this : k => {
      arn            = v.arn
      repository_url = v.repository_url
    }
  }
}
