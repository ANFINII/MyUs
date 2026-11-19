resource "aws_cloudfront_distribution" "main" {
  enabled         = true
  is_ipv6_enabled = true

  aliases = local.acm_enabled ? concat([var.domain_name], var.alternate_domain_names) : []

  price_class = "PriceClass_200"

  default_root_object = var.is_spa ? "index.html" : null

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

  dynamic "custom_error_response" {
    for_each = var.is_spa ? [403, 404] : []

    content {
      error_code            = custom_error_response.value
      response_code         = 200
      response_page_path    = "/index.html"
      error_caching_min_ttl = 0
    }
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
