from smtplib import SMTPException
from django.core.mail import send_mail
from django.template.loader import render_to_string
from ..common.logger import log


def send_template_mail(template_dir: str, context: dict[str, str], email: str) -> bool:
    subject = render_to_string(f"{template_dir}/subject.txt").strip()
    message = render_to_string(f"{template_dir}/message.txt", context)
    try:
        send_mail(subject, message, None, [email])
    except (SMTPException, OSError) as e:
        log.error("send failed", exc=e)
        return False

    return True
