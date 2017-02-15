from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from members.models import StudyProgram


class StudyProgramAdmin(ModelAdmin):
    model = StudyProgram
    menu_icon = 'bold'  # TODO: Is there a better option?
    menu_order = 500  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    list_display = ('degree', 'name_en', 'name_sv')
    search_fields = ('name_en','name_sv', 'abbreviation_en', 'abbreviation_sv')


# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(StudyProgramAdmin)