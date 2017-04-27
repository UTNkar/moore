import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from members.forms import MemberForm
from members.models import Section, StudyProgram


@login_required
def profile(request):
    if request.POST:
        form = MemberForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 _('Your account settings have been saved.'))
            form = MemberForm(instance=request.user)
    else:
        form = MemberForm(instance=request.user)

    if len(request.user.get_unconfirmed_emails()) > 0:
        messages.add_message(
            request, messages.WARNING,
            _('Your newly set email address has not yet been confirmed')
        )

    can_update_status = (
        request.user.status != 'member'
        and (timezone.now() - request.user.status_changed
             > datetime.timedelta(1))
    )

    return render(request, 'members/profile.html', {
        'form': form,
        'studies': StudyProgram.objects.all(),
        'sections': Section.objects.all(),
        'can_update_status': can_update_status,
    })


@login_required
def email_change_confirm(request, token):
    try:
        email = request.user.confirm_email(token)
        request.user.set_primary_email(email)
        request.user.remove_old_email()
        messages.add_message(request, messages.SUCCESS,
                             _('Your email address has been confirmed.'))
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR,
                             _('The provided confirmation token was invalid.'))
    return HttpResponseRedirect(reverse('profile'))
