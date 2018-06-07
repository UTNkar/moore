from datetime import date
from django.shortcuts import render
from involvement.models import Team


def open_positions(request, context):
    """View redirect for the currently open positions"""
    context['positions'] = context['positions'].filter(
        recruitment_start__lte=date.today()
    ).filter(
        recruitment_end__gte=date.today()
    )
    context['teams'] = Team.objects.all()
    return render(request, 'involvement/open_positions.html', context)
