"""
ModelChoiceFields that have access to the actual objects, not just their string
value. Inspired by the following blog post:
http://srcmvn.com/blog/2013/01/15/django-advanced-model-choice-field/
"""

from django.forms import models
from django.forms.fields import ChoiceField


class AdvancedModelChoiceIterator(models.ModelChoiceIterator):
    """
    Iterator user by Advanced[Multiple]ModelChoice fields. It adds the object
    itself as an additional argument to the choices
    """
    def choice(self, obj):
        return (
            self.field.prepare_value(obj),
            self.field.label_from_instance(obj),
            obj
        )


class AdvancedModelChoiceField(models.ModelChoiceField):
    """
    An extension of ModelChoiceField that contains the object itself within its
    choices.
    """
    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices

        return AdvancedModelChoiceIterator(self)

    choices = property(_get_choices, ChoiceField._set_choices)


class AdvancedModelMultipleChoiceField(models.ModelMultipleChoiceField):
    """
    An extension of ModelMultipleChoiceField that contains the object itself
    within its choices.
    """
    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices

        return AdvancedModelChoiceIterator(self)

    choices = property(_get_choices, ChoiceField._set_choices)
