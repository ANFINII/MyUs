output "frontend" {
  value = {
    bucket_name     = module.frontend.s3.bucket
    domain_name     = local.p.domain
    distribution_id = module.frontend.distribution_id

    cloudfront_domain_name = module.frontend.domain_name
    cloudfront_zone_id     = module.frontend.zone_id
  }
}
