from django.forms import inlineformset_factory, Textarea, TextInput, ModelForm

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
