from datetime import date

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from involvement.forms import ApplicationForm, ReferenceFormSet
from involvement.models import Position, Team, Application


def open_positions(request, context):
    """View redirect for the currently open positions"""
    # TODO: Limit accorting to inclusion/exclusion rules
    context['positions'] = Position.objects.filter(
        recruitment_start__lte=date.today()
    ).filter(
        recruitment_end__gte=date.today()
    )
    context['teams'] = Team.objects.all()
    return render(request, 'involvement/open_positions.html', context)


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
                context['error'] = _('You cannot delete an application that '
                                     'is not yours!')
            elif appl.position.recruitment_end < date.today():
                context['error'] = _('You cannot delete an application after '
                                     'its deadline has passed!')
            else:
                if action == 'delete':
                    appl.delete()
                    context['message'] = _('Your application has been '
                                           'removed!')
                else:
                    context['error'] = _('No action has been supplied!')
        except ObjectDoesNotExist:
            context['error'] = _('This application does not exist!')

    applications = Application.objects.filter(applicant=request.user).order_by(
        'position__recruitment_end'
    )

    context['drafts'] = applications.filter(
        position__recruitment_end__gte=date.today(),
        status='draft',
    )
    context['submitted'] = applications.filter(
        position__recruitment_end__gte=date.today(),
        status='submitted',
    )
    context['waiting'] = applications.filter(
        Q(position__recruitment_end__lt=date.today(), status='submitted')
        | Q(status='approved')
    )
    context['old'] = applications.filter(
        status__in=['disapproved', 'appointed', 'turned_down'],
    )

    return render(request, 'involvement/my_applications.html', context)


def position(request, context, page, position=None):
    """
    View function for specific positions.
    """
    context['position'] = get_object_or_404(Position, id=position)

    # Load application form if user is logged in
    if request.user.is_authenticated:
        # Did the user already have an application?
        try:
            appl = Application.objects.get(applicant=request.user,
                                           position=context['position'])
            context['status'] = appl.status
        except ObjectDoesNotExist:
            appl = Application()
            context['status'] = 'draft'
        # Did the user already fill in the form?
        if request.method == 'POST' and not context['position'].is_past_due:
            context['form'] = ApplicationForm(request.POST, instance=appl)
            context['reference_forms'] = ReferenceFormSet(request.POST,
                                                          request.FILES,
                                                          instance=appl)
            if context['form'].is_valid() \
                    and context['reference_forms'].is_valid():
                appl = context['form'].save(commit=False)
                appl.applicant = request.user
                appl.position = context['position']
                appl.save()
                context['reference_forms'].save()
                if not appl.status == 'draft':
                    return HttpResponseRedirect(
                        page.url + page.reverse_subpage('my_applications')
                    )
            else:
                return render(request, 'involvement/position.html', context)

        # Render fresh: empty or after saving draft.
        context['form'] = ApplicationForm(instance=appl)
        context['reference_forms'] = ReferenceFormSet(instance=appl)

    return render(request, 'involvement/position.html', context)
