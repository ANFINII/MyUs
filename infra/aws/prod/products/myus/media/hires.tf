resource "aws_s3_bucket" "hires" {
  bucket = "${local.p.base_name}-hires"

  tags = {
    Name = "${local.p.base_name}-hires"
  }
}

resource "aws_s3_bucket_public_access_block" "hires" {
  bucket = aws_s3_bucket.hires.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_ownership_controls" "hires" {
  bucket = aws_s3_bucket.hires.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }

  depends_on = [aws_s3_bucket_public_access_block.hires]
}

resource "aws_s3_bucket_versioning" "hires" {
  bucket = aws_s3_bucket.hires.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "hires" {
  bucket = aws_s3_bucket.hires.id

  rule {
    id     = "abort-incomplete-multipart-upload"
    status = "Enabled"

    filter {}

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }

  rule {
    id     = "expire-noncurrent-versions"
    status = "Enabled"

    filter {}

    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }

  depends_on = [aws_s3_bucket_versioning.hires]
}

resource "aws_s3_bucket_policy" "hires" {
  bucket = aws_s3_bucket.hires.id
  policy = data.aws_iam_policy_document.hires.json

  depends_on = [aws_s3_bucket_public_access_block.hires]
}

data "aws_iam_policy_document" "hires" {
  statement {
    sid     = "TLSOnly"
    effect  = "Deny"
    actions = ["s3:*"]

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    resources = [
      aws_s3_bucket.hires.arn,
      "${aws_s3_bucket.hires.arn}/*",
    ]

    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = ["false"]
    }
  }
}
