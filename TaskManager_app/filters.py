# TaskManager_app/filters.py
import django_filters
from django_filters import rest_framework as filters
from .models import SubTask

# class SubTaskFilter(filters.FilterSet):
#     status = filters.CharFilter(lookup_expr='exact')
#     deadline = filters.DateFilter(lookup_expr='exact')
#
#     class Meta:
#         model = SubTask
#         fields = ['status', 'deadline']



class SubTaskFilter(django_filters.FilterSet):
    # Фильтрация по точному статусу (например, ?status=Pending)
    status = django_filters.CharFilter(field_name='status', lookup_expr='iexact')

    # Фильтрация по дате (например, ?deadline=2025-07-20)
    deadline = django_filters.DateFilter(field_name='deadline', lookup_expr='date')

    class Meta:
        model = SubTask
        fields = ['status', 'deadline']