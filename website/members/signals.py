import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template import loader
from django.utils import timezone
from simple_email_confirmation import unconfirmed_email_created

from members.models import Member


@receiver(unconfirmed_email_created, dispatch_uid='send_email_confirmation')
def send_confirmation_email(sender, email, user=None, **kwargs):
    if user is not None:
        context = {
            'email': email,
            'domain': settings.BASE_URL,
            'site_name': settings.WAGTAIL_SITE_NAME,
            'token': user.get_confirmation_key(email),
        }

        subject = loader.render_to_string(
            'members/email_change_subject.txt', context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string('members/email_change_email.html',
                                       context)

        email_message = EmailMultiAlternatives(subject, body, None, [email])
        email_message.send()


@receiver(pre_save, sender=Member, dispatch_uid='member_check_membership')
def check_membership(sender, instance, **kwargs):
    if timezone.now() - instance.status_changed > datetime.timedelta(1):
        instance.update_status()
