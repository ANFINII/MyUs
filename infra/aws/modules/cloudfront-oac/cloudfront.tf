resource "aws_cloudfront_distribution" "main" {
  enabled         = true
  is_ipv6_enabled = true

  aliases = local.acm_enabled ? [var.domain_name] : []

  price_class = "PriceClass_200"

  origin {
    origin_id                = aws_s3_bucket.main.id
    domain_name              = aws_s3_bucket.main.bucket_regional_domain_name
    origin_access_control_id = var.cloudfront_origin_access_control_id
  }

  viewer_certificate {
    ssl_support_method             = local.acm_enabled ? "sni-only" : null
    acm_certificate_arn            = local.acm_enabled ? var.acm_certificate_arn : null
    cloudfront_default_certificate = local.acm_enabled ? false : true
    minimum_protocol_version       = local.acm_enabled ? "TLSv1.2_2025" : "TLSv1"
  }

  default_cache_behavior {
    target_origin_id       = aws_s3_bucket.main.id
    viewer_protocol_policy = "redirect-to-https"
    cached_methods         = ["GET", "HEAD"]
    allowed_methods        = ["GET", "HEAD", "OPTIONS"]

    cache_policy_id            = var.cache_policy_id
    response_headers_policy_id = var.response_headers_policy_id

    compress = true
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  tags = {
    Name = var.bucket_name
  }
}
