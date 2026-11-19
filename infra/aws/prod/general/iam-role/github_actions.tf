module "github_actions" {
  source = "../../../modules/github-actions"

  roles = {
    github-actions-terraform-plan = {
      subjects = [
        "repo:${local.github_repository}:pull_request",
        "repo:${local.github_repository}:ref:refs/heads/main",
      ]
      managed_policy_arns = ["arn:aws:iam::aws:policy/ReadOnlyAccess"]
      iam_policies = {
        terraform-state-lock = data.aws_iam_policy_document.terraform_state_lock.json
      }
    }
    github-actions-terraform-apply = {
      subjects            = ["repo:${local.github_repository}:ref:refs/heads/main"]
      managed_policy_arns = ["arn:aws:iam::aws:policy/AdministratorAccess"]
    }
    github-actions-deploy = {
      subjects = ["repo:${local.github_repository}:ref:refs/heads/main"]
      iam_policies = {
        deploy = data.aws_iam_policy_document.deploy.json
      }
    }
  }
}

data "aws_iam_policy_document" "terraform_state_lock" {
  statement {
    actions = [
      "s3:PutObject",
      "s3:DeleteObject",
    ]

    resources = ["arn:aws:s3:::${local.terraform_state_bucket}/*.tflock"]

    effect = "Allow"
  }
}

data "aws_iam_policy_document" "deploy" {
  statement {
    actions   = ["ecr:GetAuthorizationToken"]
    resources = ["*"]
  }

  statement {
    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:BatchGetImage",
      "ecr:CompleteLayerUpload",
      "ecr:DescribeImages",
      "ecr:GetDownloadUrlForLayer",
      "ecr:InitiateLayerUpload",
      "ecr:PutImage",
      "ecr:UploadLayerPart",
    ]

    resources = ["arn:aws:ecr:${local.p.region}:${data.aws_caller_identity.current.account_id}:repository/myus-backend"]
  }

  statement {
    actions   = ["ssm:SendCommand"]
    resources = ["arn:aws:ssm:${local.p.region}::document/AWS-RunShellScript"]
  }

  statement {
    actions   = ["ssm:SendCommand"]
    resources = ["arn:aws:ec2:${local.p.region}:${data.aws_caller_identity.current.account_id}:instance/*"]

    condition {
      test     = "StringEquals"
      variable = "ssm:resourceTag/Name"
      values   = ["myus-api-${local.p.env}"]
    }
  }

  statement {
    actions = [
      "ssm:GetCommandInvocation",
      "ec2:DescribeInstances",
    ]
    resources = ["*"]
  }

  statement {
    actions   = ["s3:ListBucket"]
    resources = ["arn:aws:s3:::${local.p.base_name}-frontend"]
  }

  statement {
    actions = [
      "s3:PutObject",
      "s3:DeleteObject",
    ]
    resources = ["arn:aws:s3:::${local.p.base_name}-frontend/*"]
  }

  statement {
    actions   = ["cloudfront:ListDistributions"]
    resources = ["*"]
  }

  statement {
    actions   = ["cloudfront:CreateInvalidation"]
    resources = ["arn:aws:cloudfront::${data.aws_caller_identity.current.account_id}:distribution/*"]
  }
}
