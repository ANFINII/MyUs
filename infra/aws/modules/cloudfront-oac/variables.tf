variable "bucket_name" {
  description = "作成する S3 バケットの名前"
  type        = string
}

variable "domain_name" {
  description = "CloudFront の別名。null のときは CloudFront の既定のドメイン (*.cloudfront.net) で配信する"
  type        = string
  default     = null
}

variable "alternate_domain_names" {
  description = "domain_name のほかに付ける CloudFront の別名。証明書がこの名前も含んでいること"
  type        = list(string)
  default     = []
}

variable "acm_certificate_arn" {
  description = "domain_name の証明書 (us-east-1 の ACM)。domain_name と一緒に渡す"
  type        = string
  default     = null
}

variable "cloudfront_origin_access_control_id" {
  type = string
}

variable "cache_policy_id" {
  type = string
}

variable "response_headers_policy_id" {
  type    = string
  default = null
}

variable "is_spa" {
  description = "SPA のとき true。/ で index.html を返し、S3 に無いパスにも index.html を返す"
  type        = bool
  default     = false
}

variable "noncurrent_version_expiration_days" {
  description = "上書き・削除された古いバージョンを残す日数"
  type        = number
  default     = 30
}

locals {
  acm_enabled = var.acm_certificate_arn != null
}
