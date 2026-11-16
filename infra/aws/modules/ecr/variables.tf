variable "repositories" {
  description = "作成するリポジトリの名前"
  type        = list(string)
}

variable "keep_image_count" {
  description = "リポジトリごとに残すイメージの数。古いものから消す"
  type        = number
  default     = 20
}
