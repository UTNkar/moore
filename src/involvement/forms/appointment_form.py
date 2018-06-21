from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from involvement.models import Application, MandateHistory
from members.forms import PersonNumberField
from utils.forms import AdvancedModelMultipleChoiceField


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
            )
