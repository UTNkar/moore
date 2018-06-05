from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from involvement.models import Application, Reference, MandateHistory
from members.forms import PersonNumberField
from utils.forms import AdvancedModelMultipleChoiceField


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude = ['position', 'applicant']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'style': 'height: 200px',
                                                  'class': 'form-control'}),
            'qualifications': forms.Textarea(attrs={'style': 'height: 200px',
                                                    'class': 'form-control'}),
        }

    def clean_status(self):
        status = self.cleaned_data['status']
        if status not in ['draft', 'submitted'] \
                or (self.initial['status'] == 'submitted'
                    and status == 'draft'):
            raise forms.ValidationError(_('The submitted status was invalid.'))
        return status


ReferenceFormSet = forms.inlineformset_factory(
    Application,
    Reference,
    fields=('name', 'position', 'email', 'phone_number', 'comment'),
    widgets={
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'position': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.TextInput(attrs={'class': 'form-control'}),
        'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        'comment': forms.TextInput(attrs={'class': 'form-control'}),
    },
    extra=0,
)


class ApprovalForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=(
            ('submitted', '---------'),
            ('approved', _('Approved')),
            ('disapproved', _('Disapproved')),
        ),
    )

    class Meta:
        model = Application
        fields = []

    def clean_status(self):
        status = self.cleaned_data['status']
        if status not in ['submitted', 'approved', 'disapproved']:
            raise forms.ValidationError(_('The submitted status was invalid.'))
        return status

    def save(self, commit=True):
        self.instance.status = self.cleaned_data['status']

        super(ApprovalForm, self).save(commit)


class AppointmentForm(forms.Form):
    appoint = AdvancedModelMultipleChoiceField(
        Application.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
    overturn = forms.CharField(
        required=False,
        label=_('Overturn'),
        help_text=_('Enter a comma separated list of person numbers you want '
                    'to appoint to the position, even though did not apply for'
                    ' the position.')
    )

    def __init__(self, position, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.position = position
        self.fields['appoint'].queryset = position.applications.filter(
            status__in=['submitted', 'approved', 'appointed', 'turned_down']
        )
        self.initial['appoint'] = position.applications.filter(
            status='appointed'
        )

    def clean_overturn(self):
        string = self.cleaned_data['overturn']
        string = string.replace(' ', '')
        if string == '':
            return []
        else:
            pnrs = string.split(',')
            users = []
            for pnr in pnrs:
                date, number = PersonNumberField().to_python(pnr)
                if not get_user_model().objects.filter(
                    birthday=date,
                    person_number_ext=number,
                ).exists():
                    raise forms.ValidationError(
                        _('No user with the person number %(pnr)s exists.'),
                        params={'pnr': pnr},
                    )
                elif self.position.applications.filter(
                    applicant__birthday=date,
                    applicant__person_number_ext=number,
                ).exclude(
                    status='draft'
                ).exists():
                    raise forms.ValidationError(
                        _('User with person number %(pnr)s already applied for'
                          ' this position and can not be appointed through the'
                          ' overturn field.'),
                        params={'pnr': pnr},
                    )
                else:
                    users.append(get_user_model().objects.get(
                        birthday=date,
                        person_number_ext=number,
                    ))
            return users

    def clean(self):
        super(AppointmentForm, self).clean()
        appoint = self.cleaned_data.get('appoint', [])
        overturn = self.cleaned_data.get('overturn', [])
        nr_appointment = len(appoint) + len(overturn)
        if nr_appointment > self.position.appointments:
            raise forms.ValidationError(
                _('You cannot appoint %(current)s applicants. The maximum '
                  'for this position is %(max)s.'),
                params={
                    'current': nr_appointment,
                    'max': self.position.appointments,
                },
            )
        return self.cleaned_data

    def save(self):
        for application in self.fields['appoint'].queryset:
            if application in self.cleaned_data['appoint']:
                application.status = 'appointed'

                MandateHistory.objects.get_or_create(
                    position=self.position,
                    applicant=application.applicant,
                    term_from=self.position.term_from,
                    term_to=self.position.term_to
                )
            else:
                application.status = 'turned_down'
            application.save()


        for user in self.cleaned_data['overturn']:
            appl, created = Application.objects.get_or_create(
                position=self.position,
                applicant=user,
                defaults={'status': 'appointed'}
            )
            if not created:
                appl.status = 'appointed'
                appl.save()

            MandateHistory.objects.get_or_create(
                position=self.position,
                applicant=user,
                term_from=self.position.term_from,
                term_to=self.position.term_to
            )
