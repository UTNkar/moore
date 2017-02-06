from modeltranslation.translator import register, TranslationOptions
from members.models import StudyProgram


@register(StudyProgram)
class StudyProgramTranslationOptions(TranslationOptions):
    fields = ('name', 'abbreviation',)
