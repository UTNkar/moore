from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from members.forms import MemberForm


@login_required
def profile(request):
    page = {'title': _('Account Settings')}

    if request.POST:
        form = MemberForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 _('Your account settings have been saved.'))
    else:
        form = MemberForm(instance=request.user)

    if len(request.user.get_unconfirmed_emails()) > 0:
        messages.add_message(
            request, messages.WARNING,
            _('Your newly set e-mail address has not yet been confirmed')
        )

    return render(request, 'members/profile.html', {
        'page': page,
        'form': form,
    })


@login_required
def email_change_confirm(request, token):
    try:
        email = request.user.confirm_email(token)
        request.user.set_primary_email(email)
        request.user.remove_old_email()
        messages.add_message(request, messages.SUCCESS,
                             _('Your e-mail address has been confirmed.'))
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR,
                             _('The provided confirmation token was invalid.'))
    return HttpResponseRedirect(reverse('profile'))
