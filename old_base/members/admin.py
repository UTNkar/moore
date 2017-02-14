from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from modeltranslation.admin import TranslationAdmin

from members.models import StudyProgram, Member


@admin.register(StudyProgram)
class StudyProgramAdmin(TranslationAdmin):
    list_display = ('name', 'degree')


class MemberInline(admin.StackedInline):
    model = Member
    extra = 0


class UserAdmin(BaseUserAdmin):
    inlines = [MemberInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
