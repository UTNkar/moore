from django import forms
from django.utils.translation import gettext_lazy as _
from involvement.models import Application


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
