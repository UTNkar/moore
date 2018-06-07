from django.contrib import messages
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from rules.contrib.views import permission_required
from involvement.forms import ApprovalForm
from involvement.models import Application, Position
from utils.view_utils import get_position_by_pk


@permission_required('involvement.approve_position', fn=get_position_by_pk)
def admin_approve_applicants(request, key):
    """
    Admin view to approve members for a position
    """
    position = get_object_or_404(Position, pk=key)
    applications = position.applications.filter(
        status__in=['submitted', 'approved', 'disapproved']
    )

    formset_class = modelformset_factory(
        Application,
        form=ApprovalForm,
        can_delete=False,
        extra=0,
    )
    if request.method == 'POST':
        formset = formset_class(request.POST, request.FILES,
                                queryset=applications)
        if formset.is_valid():
            formset.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                _('Your decisions have successfully been saved.'),
            )
            return HttpResponseRedirect(
                reverse('involvement_position_modeladmin_index')
            )
    else:
        formset = formset_class(queryset=applications)

    view = {
        'get_meta_title': 'Approve applicants',
        'get_page_title': 'Approve applicants for',
        'get_page_subtitle': position.__str__(),
        'header_icon': 'tick',
    }
    context = {
        'view': view,
        'request': request,
        'position': position,
        'formset': formset,
    }
    return render(request, 'involvement/admin/position_approval.html', context)
