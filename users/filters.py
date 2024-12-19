import django_filters
from django.db.models import Q

from .models import User

class UserFilter(django_filters.FilterSet):
    search_field = django_filters.CharFilter(method='filter_by_search')


    def filter_by_search(self, queryset, name, value):
        splitted = value.split()
        if len(splitted) == 1:
            return queryset.filter(
                Q(first_name__icontains=value) |
                Q(last_name__icontains=value)
            )
        elif len(splitted) == 2:
            first_part, second_part = splitted
            return queryset.filter(
                Q(first_name__icontains=first_part) &
                Q(last_name__icontains=second_part) |
                Q(first_name__icontains=second_part) &
                Q(last_name__icontains=first_part)
            )
    class Meta:
        model = User
        fields = ['search_field']