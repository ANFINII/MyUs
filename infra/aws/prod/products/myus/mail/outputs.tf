output "mail" {
  value = {
    domain           = aws_sesv2_email_identity.main.email_identity
    mail_from_domain = local.mail_from_domain
  }
}
