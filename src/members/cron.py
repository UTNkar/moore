import kronos
from datetime import timedelta
from django.utils import timezone
from members.models import Member


# There is now good way for bulk updates and
# without bulk update we will need to make at least 2 requests against melos to
# update one single member. To reduce the amounts of requests,
# we will only update status for active members e.g the ones that has
# status="member" as this value is updated when you log in to your account.
# We also restrict the updates to every 3 days.
@kronos.register('0 3 * * 1')  # At 03:00 on Monday.
def update_membership_status():
    for member in Member.objects.filter(
                    status='member',
                    status_changed__gte=timezone.now() - timedelta(days=3)
                ):
        member.update_status()
