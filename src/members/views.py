import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import UpdateView

from members.forms import MemberForm
from members.models import Section, StudyProgram


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'members/profile.html'
    form_class = MemberForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS,
                             _('Your account settings have been saved.'))
        return super(ProfileView, self).form_valid(form)

    def get_object(self, queryset=None):
        if len(self.request.user.get_unconfirmed_emails()) > 0:
            messages.add_message(
                self.request, messages.WARNING,
                _('Your newly set email address has not yet been confirmed')
            )
        return self.request.user

    def get_context_data(self, **kwargs):
        kwargs['studies'] = StudyProgram.objects.all()
        kwargs['sections'] = Section.objects.all()
        kwargs['can_update_status'] = (
            self.request.user.status != 'member'
            and (timezone.now() - self.request.user.status_changed
                 > datetime.timedelta(1))
        )
        return super(ProfileView, self).get_context_data(**kwargs)


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
    return HttpResponseRedirect(reverse_lazy('profile'))
