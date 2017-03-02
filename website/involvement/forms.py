from django.forms import inlineformset_factory, Textarea, TextInput,\
    ModelForm, ValidationError
from django.utils.translation import ugettext_lazy as _

from involvement.models import Application, Reference


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        exclude = ['position', 'applicant']
        widgets = {
            'cover_letter': Textarea(attrs={'style': 'height: 200px',
                                            'class': 'form-control'}),
            'qualifications': Textarea(attrs={'style': 'height: 200px',
                                              'class': 'form-control'}),
        }

    def clean_status(self):
        status = self.cleaned_data['status']
        if status not in ['draft', 'submitted']:
            raise ValidationError(_('The submitted status was invalid.'))
        return status


ReferenceFormSet = inlineformset_factory(
    Application,
    Reference,
    fields=('name', 'position', 'email', 'phone_number', 'comment'),
    widgets={
        'name': TextInput(attrs={'class': 'form-control'}),
        'position': TextInput(attrs={'class': 'form-control'}),
        'email': TextInput(attrs={'class': 'form-control'}),
        'phone_number': TextInput(attrs={'class': 'form-control'}),
        'comment': TextInput(attrs={'class': 'form-control'}),
    },
    extra=0,
)
