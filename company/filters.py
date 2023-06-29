from django_filters import rest_framework as filters
from .models import Company
from datetime import datetime, timedelta

class CompanyFilter(filters.FilterSet):

    keyword = filters.CharFilter(field_name="name", lookup_expr="icontains")
    location = filters.CharFilter(field_name="address", lookup_expr="icontains")
    city = filters.CharFilter(field_name="city", lookup_expr="icontains")
    industry = filters.CharFilter(field_name="industry", lookup_expr="icontains")
    foundedInMin = filters.CharFilter(
        field_name="foundedIn", lookup_expr='gte'
    )
    foundedInMax = filters.CharFilter(
        field_name="foundedIn", lookup_expr='lte'
    )

    def foundedInMin_filter(self, queryset, name, value):
        return queryset.filter(city__contains=[{ "name": value }])

    def city_filter(self, queryset, name, value):
        return queryset.filter(city__contains=[{ "name": value }])
    
    class Meta:
        model = Company
        fields = ('keyword', 'location')

