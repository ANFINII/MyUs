output "hires" {
  value = {
    bucket_name = aws_s3_bucket.hires.bucket
    bucket_arn  = aws_s3_bucket.hires.arn
  }
}

output "media" {
  value = {
    bucket_name     = module.media.s3.bucket
    bucket_arn      = module.media.s3.arn
    domain_name     = module.media.domain_name
    distribution_id = module.media.distribution_id
  }
}
