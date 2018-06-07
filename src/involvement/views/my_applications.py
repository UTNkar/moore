from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from involvement.models import Application


@login_required
def my_applications(request, context):
    """View redirect for the applications by user"""
    if request.method == 'POST':
        # TODO: Use form?
        try:
            action = request.POST.get('action')
            appl_id = request.POST.get('application')
            appl = Application.objects.get(id=appl_id)
            if appl.applicant != request.user:
                messages.add_message(request, messages.ERROR,
                                     _('You cannot delete an application that '
                                       'is not yours!'))
            elif appl.position.recruitment_end < date.today():
                messages.add_message(request, messages.ERROR,
                                     _('You cannot delete an application '
                                       'after its deadline has passed!'))
            else:
                if action == 'delete':
                    appl.delete()
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        _('Your application has been removed!')
                    )
                else:
                    messages.add_message(request, messages.ERROR,
                                         _('No action has been supplied!'))
        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR,
                                 _('This application does not exist!'))

    applications = Application.objects.filter(applicant=request.user).order_by(
        'position__recruitment_end'
    )

    context['drafts'] = applications.filter(
        position__in=context['positions'],
        position__recruitment_end__gte=date.today(),
        status='draft',
    )
    context['submitted'] = applications.filter(
        position__in=context['positions'],
        position__recruitment_end__gte=date.today(),
        status='submitted',
    )
    context['waiting'] = applications.filter(
        Q(position__in=context['positions'],
          position__recruitment_end__lt=date.today(),
          status='submitted')
        | Q(position__in=context['positions'],
            status='approved')
    )
    context['old'] = applications.filter(
        position__in=context['positions'],
        status__in=['disapproved', 'appointed', 'turned_down'],
    )

    return render(request, 'involvement/my_applications.html', context)
