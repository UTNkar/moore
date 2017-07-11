from datetime import date, timedelta

import kronos
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader

from involvement.models import Team, Application, Position


@kronos.register('1 0,6,12,18 * * *')  # At minute 1 past hour 0, 6, 12, and 18
def sync_groups():
    for team in Team.objects.all():
        # Add new members
        for member in team.get_members():
            if team.group not in member.groups.all():
                team.group.user_set.add(member)

                applications = member.application_set.filter(
                    position__role__team=team,
                    position__term_from__lte=date.today(),
                    position__term_to__gte=date.today(),
                    status='appointed',
                )
                for a in applications:
                    a.removed = False
                    a.save()

        # Remove old members
        old_members = Application.objects.filter(
            position__role__team=team,
            position__term_to__lt=date.today(),
            status='appointed',
            removed=False,
        )
        for member in old_members:
            if team.group in member.applicant.groups.all():
                team.group.user_set.remove(member.applicant)
            member.removed = True
            member.save()


@kronos.register('30 6 * * *')  # At 06:30.
def send_extension_emails():
    vacant_positions = Position.objects.filter(
        recruitment_end=date.today() - timedelta(days=1),
    ).exclude(
        applications__status='submitted'
    )

    for pos in vacant_positions:
        context = {
            'email': pos.role.election_email,
            'domain': settings.BASE_URL,
            'position': pos,
        }
        subject = loader.render_to_string(
            'involvement/admin/extend_deadline_subject.txt', context
        )
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(
            'involvement/admin/email_extend_deadline.html', context
        )

        email_message = EmailMultiAlternatives(
            subject, body, None, [pos.role.election_email]
        )
        email_message.send()


@kronos.register('0 3 * * *')  # At 03:00.
def remove_old_applications():
    old_applications = Application.objects.filter(
        position__recruitment_end__lte=date.today() - timedelta(days=730)
    ).exclude(
        status='appointed'
    )

    for app in old_applications:
        app.delete()
