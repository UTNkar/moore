import datetime

from django.shortcuts import render

from involvement.models import Position, Team


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


def sent_applications(request, context):
    """View redirect for the sent applications by user"""
    return render(request, 'involvement/sent_applications.html', context)


def action_list(request, context):
    """
    View redirect for the applications that require (future) attention
    from the user
    """
    return render(request, 'involvement/action_list.html', context)


def position(request, context, position=None):
    """
    View function for specific positions.
    """
    return render(request, 'involvement/position.html', context)
