from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from involvement.models import MandateHistory


@login_required
def my_mandates(request, context):
    """View redirect for the positions by user"""

    context['mandates'] = MandateHistory.objects \
        .filter(applicant=request.user) \
        .order_by('term_to')

    return render(request, 'involvement/my_mandates.html', context)
