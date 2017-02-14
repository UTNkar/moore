from django.contrib import admin

from members.models import StudyProgram


@admin.register(StudyProgram)
class StudyProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'degree')
