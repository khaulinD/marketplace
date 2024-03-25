import django_filters

from customers.models import Account
from ..models import UserWork


class WorkFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    work_id = django_filters.NumberFilter(field_name="id")
    work_course_lvl = django_filters.NumberFilter(
        field_name="extra_info__resume_course_lvl",
        lookup_expr="icontains"
    )
    work_subject_name = django_filters.NumberFilter(
        field_name="extra_info__work_subject_name",
        lookup_expr="icontains"
    )
    work_subject_teacher = django_filters.NumberFilter(
        field_name="extra_info__work_subject_teacher",
        lookup_expr="icontains"
    )

    class Meta:
        model = UserWork
        fields = ['title', 'work_id', 'work_course_lvl', "work_subject_name", 'work_subject_teacher']