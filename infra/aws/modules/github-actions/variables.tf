variable "roles" {
  description = "GitHub Actions から引き受けるロール。キーはロール名"
  type = map(object({
    subjects            = list(string)
    managed_policy_arns = optional(list(string), [])
    iam_policies        = optional(map(string), {})
  }))
}
