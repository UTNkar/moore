from django import forms
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailusers.forms import UserEditForm, UserCreationForm

from members.models import StudyProgram


class CustomUserEditForm(UserEditForm):
    birthday = forms.DateField(required=True, label=_('Birthday'))
    person_number_ext = forms.CharField(
        required=True,
        label=_('Person number extension')
    )
    phone_number = forms.CharField(
        required=False,
        label=_('Phone number')
    )
    registration_year = forms.CharField(
        required=False,
        label=_('Registration year')
    )
    study = forms.ModelChoiceField(
        required=False,
        queryset=StudyProgram.objects,
        label=_("Study Program")
    )


class CustomUserCreationForm(UserCreationForm):
    birthday = forms.DateField(required=True, label=_('Birthday'))
    person_number_ext = forms.CharField(
        required=True,
        label=_('Person number extension')
    )
    phone_number = forms.CharField(
        required=False,
        label=_('Phone number')
    )
    registration_year = forms.CharField(
        required=False,
        label=_('Registration year')
    )
    study = forms.ModelChoiceField(
        required=False,
        queryset=StudyProgram.objects,
        label=_("Study Program")
    )
