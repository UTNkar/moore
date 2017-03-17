from django.forms import inlineformset_factory, Textarea, TextInput, \
    ModelForm, ValidationError, RadioSelect, \
    ChoiceField
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
        if status not in ['draft', 'submitted'] \
                or (self.initial['status'] == 'submitted'
                    and status == 'draft'):
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


class ApprovalForm(ModelForm):
    status = ChoiceField(
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
            raise ValidationError(_('The submitted status was invalid.'))
        return status

    def save(self, commit=True):
        self.instance.status = self.cleaned_data['status']

        super(ApprovalForm, self).save(commit)
