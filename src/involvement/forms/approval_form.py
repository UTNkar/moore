from django import forms
from django.utils.translation import ugettext_lazy as _
from datetime import date
from involvement.models import Application
import sys


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
        status = self.cleaned_data['status']
        self.instance.status = status

        if (status == 'disapproved'):
            self.instance.rejection_date = date.today()

        super(ApprovalForm, self).save(commit)
