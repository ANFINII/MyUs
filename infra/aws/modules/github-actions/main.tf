resource "aws_iam_openid_connect_provider" "github_actions" {
  url = "https://token.actions.githubusercontent.com"

  client_id_list = ["sts.amazonaws.com"]

  tags = {
    Name = "github-actions"
  }
}

resource "aws_iam_role" "github_actions" {
  for_each = var.roles

  name               = each.key
  assume_role_policy = data.aws_iam_policy_document.github_actions_assume_role[each.key].json

  tags = {
    Name = each.key
  }
}

resource "aws_iam_role_policy_attachment" "github_actions" {
  for_each = {
    for e in flatten([
      for role_name, role in var.roles : [
        for arn in role.managed_policy_arns : { role_name = role_name, arn = arn }
      ]
    ]) : "${e.role_name}:${e.arn}" => e
  }

  role       = aws_iam_role.github_actions[each.value.role_name].name
  policy_arn = each.value.arn
}

resource "aws_iam_role_policy" "github_actions" {
  for_each = {
    for e in flatten([
      for role_name, role in var.roles : [
        for name, policy in role.iam_policies : { role_name = role_name, name = name, policy = policy }
      ]
    ]) : "${e.role_name}:${e.name}" => e
  }

  name   = each.value.name
  policy = each.value.policy
  role   = aws_iam_role.github_actions[each.value.role_name].id
}

data "aws_iam_policy_document" "github_actions_assume_role" {
  for_each = var.roles

  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.github_actions.arn]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = each.value.subjects
    }

    effect = "Allow"
  }
}
