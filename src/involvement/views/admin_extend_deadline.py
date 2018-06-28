from datetime import date, timedelta
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from rules.contrib.views import permission_required
from involvement.models import Position
from utils.view_utils import get_position_by_pk


@permission_required('involvement.change_position', fn=get_position_by_pk)
def admin_extend_deadline(request, key):
    """
    An admin view to automatically extend the deadline of vacant positions.
    """
    position = get_object_or_404(Position, pk=key)
    if position.recruitment_end >= date.today():
        messages.add_message(
            request, messages.ERROR,
            _('This position is not due for an extension yet.')
        )
    elif position.applications.exclude(status='draft').exists():
        messages.add_message(
            request, messages.ERROR,
            _('A position with submitted applications cannot be automatically '
              'extended.')
        )
    else:
        position.recruitment_end = date.today() + timedelta(days=7)
        position.save()
        messages.add_message(
            request, messages.SUCCESS,
            _('The recruitment deadline for %(position)s has been extended '
              'until %(date)s') % {
                'position': position,
                'date': position.recruitment_end,
            }
        )

    return HttpResponseRedirect(
        reverse('involvement_position_modeladmin_index')
    )
