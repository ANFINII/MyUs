output "media" {
  value = {
    bucket_name     = module.media.s3.bucket
    bucket_arn      = module.media.s3.arn
    domain_name     = module.media.domain_name
    distribution_id = module.media.distribution_id
  }
}
