from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, \
    modeladmin_register
from members.models import StudyProgram, Section
from django.utils.translation import ugettext_lazy as _


class StudyProgramAdmin(ModelAdmin):
    model = StudyProgram
    menu_icon = 'fa-graduation-cap'
    menu_order = 510
    add_to_settings_menu = False
    list_display = ('degree', 'name_en', 'name_sv')
    search_fields = ('name_en', 'name_sv', 'abbreviation_en',
                     'abbreviation_sv')


class SectionAdmin(ModelAdmin):
    model = Section
    menu_icon = 'fa-eye'
    menu_order = 520
    add_to_settings_menu = False
    list_display = ('abbreviation', 'name_en', 'name_sv')
    search_fields = ('name_en', 'name_sv', 'abbreviation')


class EducationAdminGroup(ModelAdminGroup):
    menu_label = _('Education')
    menu_icon = 'fa-university'
    menu_order = 450
    items = (StudyProgramAdmin, SectionAdmin)

modeladmin_register(EducationAdminGroup)
