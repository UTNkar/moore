from django.forms import CheckboxSelectMultiple
from django.template import loader
from django.utils.translation import ugettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, \
    modeladmin_register
from wagtail.contrib.modeladmin.views import EditView, CreateView
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList, \
    FieldPanel
from wagtail.core import hooks

from members.models import StudyProgram, Section, Member


class StudyProgramEditHandler:
    def get_edit_handler_class(self):
        edit_handler = TabbedInterface([
            ObjectList([
                FieldPanel('name_en'),
                FieldPanel('name_sv'),
                FieldPanel('degree'),
            ], heading=_('General'),
            ),
            # TODO: http://stackoverflow.com/questions/43188124/
            # ObjectList([
            #     FieldPanel('sections', widget=CheckboxSelectMultiple),
            # ], heading=_('Sections'),
            # ),
        ])
        return edit_handler.bind_to_model(self.model)


class StudyProgramEditView(StudyProgramEditHandler, EditView):
    pass


class StudyProgramCreateView(StudyProgramEditHandler, CreateView):
    pass


class StudyProgramAdmin(ModelAdmin):
    model = StudyProgram
    menu_label = _('Study Program')
    menu_icon = 'fa-graduation-cap'
    menu_order = 510
    add_to_settings_menu = False
    create_view_class = StudyProgramCreateView
    edit_view_class = StudyProgramEditView
    list_display = ('degree', 'name_en', 'name_sv')
    search_fields = ('name_en', 'name_sv')


class SectionEditHandler:
    def get_edit_handler_class(self):
        edit_handler = TabbedInterface([
            ObjectList([
                FieldPanel('name_en'),
                FieldPanel('name_sv'),
                FieldPanel('abbreviation'),
            ], heading=_('General'), ),
            ObjectList([
                FieldPanel('studies', widget=CheckboxSelectMultiple),
            ], heading=_('Studies'), ),
        ])
        return edit_handler.bind_to_model(self.model)


class SectionEditView(SectionEditHandler, EditView):
    pass


class SectionCreateView(SectionEditHandler, CreateView):
    pass


class SectionAdmin(ModelAdmin):
    model = Section
    menu_label = _('Sections')
    menu_icon = 'fa-eye'
    menu_order = 520
    add_to_settings_menu = False
    create_view_class = SectionCreateView
    edit_view_class = SectionEditView
    list_display = ('abbreviation', 'name_en', 'name_sv')
    search_fields = ('name_en', 'name_sv', 'abbreviation')


class EducationAdminGroup(ModelAdminGroup):
    menu_label = _('Education')
    menu_icon = 'fa-university'
    menu_order = 450
    items = (StudyProgramAdmin, SectionAdmin)


modeladmin_register(EducationAdminGroup)


class SuperUserPanel(object):
    order = 1000

    def __init__(self, request):
        self.request = request

    def render(self):
        c = {
            'supers': Member.objects.filter(is_superuser=True),
            'user': self.request.user
        }
        return loader.get_template('members/admin_panel.html').render(c)


@hooks.register('construct_homepage_panels')
def add_super_user_panel(request, panels):
    return panels.append(SuperUserPanel(request))
