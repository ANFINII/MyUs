module "github_actions" {
  source = "../../../modules/github-actions"

  roles = {
    github-actions-terraform-plan = {
      subjects            = ["repo:${local.github_repository}:pull_request"]
      managed_policy_arns = ["arn:aws:iam::aws:policy/ReadOnlyAccess"]
      iam_policies = {
        terraform-state-lock = data.aws_iam_policy_document.terraform_state_lock.json
      }
    }
    github-actions-terraform-apply = {
      subjects            = ["repo:${local.github_repository}:ref:refs/heads/main"]
      managed_policy_arns = ["arn:aws:iam::aws:policy/AdministratorAccess"]
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
