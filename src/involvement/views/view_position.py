from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from involvement.forms import ApplicationForm, ReferenceFormSet
from involvement.models import Application


def view_position(request, context, page, position=None):
    """
    View function for specific positions.
    """
    pos = get_object_or_404(context['positions'], id=position)
    context['position'] = pos

    if pos.role.teams.count():
        context['logo'] = pos.role.teams.first().logo

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
            context['form'] = ApplicationForm(request.POST,
                                              instance=appl)
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
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        _('Your application has been submitted!'),
                    )
                    return HttpResponseRedirect(
                        page.get_url(request=request)
                        + page.reverse_subpage('my_applications')
                    )
            else:
                return render(request, 'involvement/position.html', context)

        # Render fresh: empty or after saving draft.
        context['form'] = ApplicationForm(instance=appl)
        context['reference_forms'] = ReferenceFormSet(instance=appl)


    return render(request, 'involvement/position.html', context)
