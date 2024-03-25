import django_filters

from customers.models import Account
from users_resume.models import Resume


class ResumeFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    resume_id = django_filters.NumberFilter(field_name="id")
    resume_course_lvl = django_filters.NumberFilter(
        field_name="extra_info__resume_course_lvl"
    )

    class Meta:
        model = Resume
        fields = ['title', 'resume_id', 'resume_course_lvl']