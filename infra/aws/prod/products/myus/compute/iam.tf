data "aws_iam_policy_document" "ec2_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "api" {
  name               = "myus-api-${local.p.env}"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json

  tags = {
    Name = "myus-api-${local.p.env}"
  }
}

resource "aws_iam_instance_profile" "api" {
  name = aws_iam_role.api.name
  role = aws_iam_role.api.name
}

resource "aws_iam_role_policy_attachment" "api" {
  for_each = toset([
    "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore",
    "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly",
    "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy",
  ])

  role       = aws_iam_role.api.name
  policy_arn = each.value
}

data "aws_iam_policy_document" "api" {
  statement {
    actions = [
      "ssm:GetParameter",
      "ssm:GetParameters",
      "ssm:GetParametersByPath",
    ]

    resources = [
      "arn:aws:ssm:${local.p.region}:${data.aws_caller_identity.current.account_id}:parameter${local.parameter_store_name_prefix}*",
    ]
  }

  statement {
    actions = ["s3:ListBucket"]

    resources = [
      local.media.bucket_arn,
      local.hires.bucket_arn,
    ]
  }

  statement {
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject",
    ]

    resources = [
      "${local.media.bucket_arn}/*",
      "${local.hires.bucket_arn}/*",
    ]
  }
}

resource "aws_iam_role_policy" "api" {
  name   = "myus-api-${local.p.env}"
  role   = aws_iam_role.api.id
  policy = data.aws_iam_policy_document.api.json
}
