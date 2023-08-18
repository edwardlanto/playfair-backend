from django_filters import rest_framework as filters
from .models import Job
from candidate.models import AppliedJob
from datetime import datetime, timedelta
from django.db.models import Q

class JobsFilter(filters.FilterSet):

    keyword = filters.CharFilter(method="keyword_filter")
    location = filters.CharFilter(method="location_filter")
    industry = filters.CharFilter(method="industry_filter")
    city = filters.CharFilter(field_name="city", lookup_expr="icontains")
    experience = filters.CharFilter(field_name="experience", lookup_expr="icontains")
    type = filters.CharFilter(field_name="type", lookup_expr="icontains")
    min_salary = filters.NumberFilter(field_name="min_salary", lookup_expr="gt")

    def type_filter(self, queryset, name, value):
        return queryset.filter(type__contains=[{ "label": value, "value": value }])
    
    def location_filter(self, queryset, name, value):
        return queryset.filter(Q(country__icontains=value) | Q(city__icontains=value) | Q(state__icontains=value))
    
    def keyword_filter(self, queryset, name, value):
        return queryset.filter(Q(industry__icontains=value) | Q(description__icontains=value))
    
    def industry_filter(self, queryset, name, value):
        return queryset.filter(Q(industry__contains=value))

    class Meta:
        model = Job
        fields = ('education', 'type', 'experience', 'min_salary', 'featured', 'industry')

class CandidatesAppliedFilter(filters.FilterSet):
    class Meta:
        model = AppliedJob
        fields = ("appliedAt",)