from django.contrib import admin
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Resume, ExtraResumeInfo

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'creatorID', 'created_at', 'updated_at', 'min_price', 'amount_orders')
    list_filter = ('created_at', 'updated_at', 'creatorID')
    search_fields = ('title', 'description', 'creatorID__username')
    date_hierarchy = 'created_at'
    ordering = ('created_at', 'title')


@admin.register(ExtraResumeInfo)
class ExtraResumeInfoAdmin(admin.ModelAdmin):
    list_display = ('resume_title', 'resume_course_lvl')
    list_filter = ('resume_course_lvl',)
    search_fields = ('resume__title',)

    def resume_title(self, obj):
        return obj.resume.title
    resume_title.short_description = 'Resume Title'
    resume_title.admin_order_field = 'resume__title'