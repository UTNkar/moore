import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render

from involvement.models import Position, Team, Application

from involvement.forms import ApplicationForm, ReferenceFormSet


def open_positions(request, context):
    """View redirect for the currently open positions"""
    # TODO: Limit accorting to inclusion/exclusion rules
    context['positions'] = Position.objects.filter(
        commencement__lte=datetime.date.today()
    ).filter(
        deadline__gte=datetime.date.today()
    )
    context['teams'] = Team.objects.all()
    return render(request, 'involvement/open_positions.html', context)


def my_applications(request, context):
    """View redirect for the applications by user"""
    return render(request, 'involvement/my_applications.html', context)


def action_list(request, context):
    """
    View redirect for the applications that require (future) attention
    from the user
    """
    return render(request, 'involvement/action_list.html', context)


def position(request, context, page, position=None):
    """
    View function for specific positions.
    """
    if position is None:
        raise Http404
    try:
        context['position'] = Position.objects.get(id=position)
    except ObjectDoesNotExist:
        raise Http404

    # Load application form if user is logged in
    if request.user.is_authenticated:
        # Did the user already have an application?
        try:
            appl = Application.objects.get(applicant=request.user,
                                           position=context['position'])
            context['draft'] = appl.draft
        except ObjectDoesNotExist:
            appl = Application()
            context['draft'] = True
        # Did the user already fill in the form?
        if request.method == 'POST':
            context['form'] = ApplicationForm(request.POST, instance=appl)
            context['reference_forms'] = ReferenceFormSet(request.POST,
                                                          request.FILES,
                                                          instance=appl)
            # Was all data correct?
            if context['form'].is_valid() \
                    and context['reference_forms'].is_valid():
                appl = context['form'].save(commit=False)
                appl.applicant = request.user
                appl.position = context['position']
                appl.save()
                context['reference_forms'].save()
                if not appl.draft:
                    return HttpResponseRedirect(
                        page.url + page.reverse_subpage('my_applications')
                    )
            else:
                return render(request, 'involvement/position.html', context)

        context['form'] = ApplicationForm(instance=appl)
        context['reference_forms'] = ReferenceFormSet(instance=appl)

    return render(request, 'involvement/position.html', context)
