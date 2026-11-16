variable "product_name" {
  type = string
}

variable "env" {
  type = string
}

variable "key_id" {
  type = string
}

variable "secret_parameters" {
  description = "値を手で入れるパラメータの名前 (SecureString)。apply では値を FIXME で作り、本当の値は CLI で入れる。value_wo は state に残らない"
  type        = list(string)
}

locals {
  parameter_store_name_prefix = "/${var.product_name}/${var.env}/"
}
