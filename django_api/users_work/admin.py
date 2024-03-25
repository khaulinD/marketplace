from django.contrib import admin
from django.db.models import F
from .models import UserWork, ExtraWorkInfo
from django.utils.html import format_html


@admin.register(UserWork)
class UserWorkAdmin(admin.ModelAdmin):
    list_display = ("id", 'title', 'creatorID', 'created_at', 'updated_at', 'price')
    list_filter = ('created_at', 'updated_at', 'creatorID')
    search_fields = ('title', 'description', 'creatorID__username')
    date_hierarchy = 'created_at'
    ordering = ('created_at', 'title')



@admin.register(ExtraWorkInfo)
class ExtraWorkInfoAdmin(admin.ModelAdmin):
    list_display = ("workID", 'work_course_lvl', 'work_subject_name', 'work_subject_teacher')
    list_filter = ('work_course_lvl', 'work_subject_name', 'work_subject_teacher')
    search_fields = ('work_subject_name', 'work_subject_teacher', 'work__title')

    def resume_title(self, obj):
        return obj.resume.title

    resume_title.short_description = 'User Work Title'
    resume_title.admin_order_field = 'resume__title'