from datetime import date

import kronos

from involvement.models import Team, Application


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
