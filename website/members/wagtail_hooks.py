from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from members.models import StudyProgram


class StudyProgramAdmin(ModelAdmin):
    model = StudyProgram
    menu_icon = 'bold'  # TODO: Is there a better option?
    menu_order = 500
    add_to_settings_menu = False
    list_display = ('degree', 'name_en', 'name_sv')
    search_fields = ('name_en', 'name_sv', 'abbreviation_en',
                     'abbreviation_sv')


modeladmin_register(StudyProgramAdmin)
