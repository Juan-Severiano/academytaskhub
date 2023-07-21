from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_email(path_template: str, subject: str, to: list, **kwargs) -> dict:
    html_content = render_to_string(path_template, kwargs)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, to
    )

    email.attach_alternative(html_content, "text/html")
    email.send()
    return {'status': 1}
