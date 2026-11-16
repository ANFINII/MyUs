variable "name" {
  description = "予算と異常検出の名前"
  type        = string
}

variable "emails" {
  description = "予算の超過と異常を通知するメールアドレス"
  type        = list(string)
}

variable "monthly_limit_dollar" {
  description = "月次の予算 (ドル)"
  type        = number
}

variable "cost_anomaly_threshold_dollar" {
  description = "異常として通知するしきい値 (ドル)"
  type        = number
}
