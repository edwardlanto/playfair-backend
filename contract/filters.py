from django_filters import rest_framework as filters
from datetime import datetime, timedelta
from django.db.models import Q
from .models import Contract

class ContractFilter(filters.FilterSet):

    keyword = filters.CharFilter(method="keyword_filter")
    location = filters.CharFilter(method="location_filter")
    industry = filters.CharFilter(field_name="industry", lookup_expr="icontains")
    city = filters.CharFilter(field_name="city", lookup_expr="icontains")
    experience = filters.CharFilter(field_name="experience", lookup_expr="icontains")
    type = filters.CharFilter(field_name="type", lookup_expr="icontains")
    min_salary = filters.NumberFilter(field_name="min_salary", lookup_expr="gt")

    def type_filter(self, queryset, name, value):
        return queryset.filter(type__contains=[{ "label": value, "value": value }])
    
    def location_filter(self, queryset, name, value):
            return queryset.filter(Q(country__icontains=value) | Q(city__icontains=value))
    
    def keyword_filter(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value))

    class Meta:
        model = Contract
        fields = ()
