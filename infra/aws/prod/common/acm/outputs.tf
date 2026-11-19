output "acm" {
  value = {
    cloudfront_certificate_arn = aws_acm_certificate_validation.cloudfront.certificate_arn
  }
}
