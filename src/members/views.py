from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from members.forms import MemberForm, CustomPasswordResetForm
from members.models import Section, StudyProgram
from rest_framework.decorators import api_view
from rest_framework.response import Response
from members.serializers import MemberCheckSerializer
from utils.melos_client import MelosClient
from rest_framework import status


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'members/profile.html'
    form_class = MemberForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS,
                             _('Your account settings have been saved.'))
        return super(ProfileView, self).form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        kwargs['studies'] = StudyProgram.objects.all()
        kwargs['sections'] = Section.objects.all()
        kwargs['can_update_status'] = self.request.user.get_status != 'member'
        kwargs['status'] = self.request.user.get_status
        return super(ProfileView, self).get_context_data(**kwargs)


class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context


class CustomPasswordResetView(PasswordContextMixin, FormView):
    email_template_name = 'registration/password_reset_email.html'
    extra_email_context = None
    form_class = CustomPasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'registration/password_reset_form.html'
    title = _('Password reset')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


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


@api_view(['POST'])
def member_check_api(request):
    """
    Checks whether a person with a given personnummer is a member in UTN.
    """
    serializer = MemberCheckSerializer(data=request.data)
    status_code = None
    data = {}

    if serializer.is_valid():
        ssn = serializer.data.get('ssn')
        is_member = MelosClient.is_member(ssn)
        data = {"is_member": is_member}
    else:
        error = serializer.errors.get("ssn")
        data = {'error': "Personnummer: " + ", ".join(error)}
        status_code = status.HTTP_400_BAD_REQUEST

    return Response(
        data,
        status=status_code,
        headers={"Access-Control-Allow-Origin": "*"}
    )
