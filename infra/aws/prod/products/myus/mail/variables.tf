locals {
  # params module variables
  p = module.params.params

  mail_from_domain = "mail.${local.p.domain}"
}
