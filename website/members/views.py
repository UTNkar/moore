from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from members.forms import MemberForm


@login_required
def profile(request):
    page = {'title': _('Account Settings')}
    saved = False

    if request.POST:
        form = MemberForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            saved = True
    else:
        form = MemberForm(instance=request.user)

    return render(request, 'members/profile.html', {
        'saved': saved,
        'page': page,
        'form': form,
    })
