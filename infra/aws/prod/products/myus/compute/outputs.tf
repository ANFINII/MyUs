output "api" {
  value = {
    instance_id     = aws_instance.api.id
    public_ip       = aws_eip.api.public_ip
    domain_name     = aws_cloudfront_distribution.api.domain_name
    distribution_id = aws_cloudfront_distribution.api.id
  }
}
