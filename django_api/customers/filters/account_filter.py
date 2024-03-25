import django_filters

from customers.models import Account


class AccountFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name="username", lookup_expr="exact")
    user_id = django_filters.NumberFilter(field_name="id")

    class Meta:
        model = Account
        fields = ['username', "user_id"]