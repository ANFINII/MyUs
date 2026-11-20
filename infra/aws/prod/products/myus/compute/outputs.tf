output "api" {
  value = {
    instance_id     = aws_instance.api.id
    domain_name     = "api.${local.p.domain}"
    distribution_id = aws_cloudfront_distribution.api.id

    cloudfront_domain_name = aws_cloudfront_distribution.api.domain_name
    cloudfront_zone_id     = aws_cloudfront_distribution.api.hosted_zone_id
  }
}
