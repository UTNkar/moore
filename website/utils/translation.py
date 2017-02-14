"""
This module defines helping structures for translating content or models.
"""
from django.utils import translation


class TranslatedField(object):
    def __init__(self, en_field, sv_field):
        self.en_field = en_field
        self.sv_field = sv_field

    def __get__(self, instance, owner):
        if translation.get_language() == 'sv':
            return getattr(instance, self.sv_field)
        else:
            return getattr(instance, self.en_field)