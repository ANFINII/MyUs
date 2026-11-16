output "domain_name" {
  value = aws_cloudfront_distribution.main.domain_name
}

output "zone_id" {
  value = aws_cloudfront_distribution.main.hosted_zone_id
}

output "distribution_id" {
  value = aws_cloudfront_distribution.main.id
}

output "s3" {
  value = aws_s3_bucket.main
}
