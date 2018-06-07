from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from rules.contrib.views import permission_required
from involvement.forms import AppointmentForm
from involvement.models import Position
from utils.view_utils import get_position_by_pk


@permission_required('involvement.appoint_position', fn=get_position_by_pk)
def admin_appoint(request, pos_id=None):
    """
    Admin view to appoint members to the position
    """
    position = get_object_or_404(Position, pk=pos_id)

    if request.method == 'POST':
        form = AppointmentForm(position, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                _('Your decisions have successfully been saved.'),
            )
            return HttpResponseRedirect(
                reverse('involvement_position_modeladmin_index')
            )
    else:
        form = AppointmentForm(position)

    view = {
        'get_meta_title': 'Appoint applicants',
        'get_page_title': 'Appoint applicants for',
        'get_page_subtitle': position.__str__(),
        'header_icon': 'pick',
    }
    context = {
        'view': view,
        'request': request,
        'position': position,
        'form': form,
    }
    return render(request, 'involvement/admin/position_appointment.html',
                  context)
