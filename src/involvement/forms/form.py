from django import forms
from involvement.models import Application, Reference

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
