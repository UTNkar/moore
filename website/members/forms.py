from django import forms
from django.core import validators
from django.forms import ModelForm, TextInput, Select
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailusers.forms import UserEditForm, UserCreationForm

from members.models import StudyProgram, Member


class MemberForm(ModelForm):
    person_number = forms.CharField(
        max_length=13,
        min_length=12,
        help_text=_('Person number using the YYYYMMDD-XXXX format.'),
        validators=[validators.RegexValidator(
            regex=r'^\d{8}\-?\d{4}$',
            message=_('Use the format YYYYMMDD-XXXX for your person number.')
        )],
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'YYYYMMDD-XXXX',
        })
    )

    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'phone_number',
                  'registration_year', 'study']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'phone_number': TextInput(attrs={'class': 'form-control'}),
            'registration_year': TextInput(attrs={'class': 'form-control'}),
            'study': Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)

        if instance is not None:
            kwargs.update(initial={
                'person_number': instance.person_number()
            })

        super(MemberForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        person_number = self.cleaned_data['person_number']
        self.instance.birthday = '%s-%s-%s' % (
            person_number[:4], person_number[4:6], person_number[6:8]
        )
        self.instance.person_number_ext = person_number[-4:]

        return super(MemberForm, self).save(commit=commit)


class CustomUserEditForm(UserEditForm):
    """
    Custom form to edit users from within the wagtail admin interface.
    """
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
    """
    Custom form to create user from within the Wagtail admin user interface.
    """
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
