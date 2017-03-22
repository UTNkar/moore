from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template import loader
from simple_email_confirmation import unconfirmed_email_created


@receiver(unconfirmed_email_created,  dispatch_uid='send_email_confirmation')
def send_confirmation_email(sender, email, user=None, **kwargs):
    member = user or sender
    context = {
        'email': email,
        'domain': settings.BASE_URL,
        'site_name': settings.WAGTAIL_SITE_NAME,
        'token': member.get_confirmation_key(email),
    }

    subject = loader.render_to_string(
        'members/email_change_subject.txt', context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string('members/email_change_email.html',
                                   context)

    email_message = EmailMultiAlternatives(subject, body, None, [email])
    email_message.send()
