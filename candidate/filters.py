from django_filters import rest_framework as filters
from playfairauth.models import CustomUserProfile
from datetime import datetime, timedelta
from django.db.models import Q
class CandidateFilter(filters.FilterSet):

    keyword = filters.CharFilter( method="keyword_filter")
    location = filters.CharFilter(method="location_filter")
    industry = filters.CharFilter(field_name="industry", lookup_expr="icontains")
    languages = filters.CharFilter(method="languages_filter")

    def keyword_filter(self, queryset, name, value):
        return queryset.filter(Q(bio__contains=value) | Q(title__contains=value))

    def location_filter(self, queryset, name, value):
        return queryset.filter(Q(city__icontains=value) | Q(country__icontains=value) | Q(state__icontains=value))
    
    def languages_filter(self, queryset, name, value):
        return queryset.filter(Q(languages__icontains=value))

    class Meta:
        model = CustomUserProfile
        fields = ('keyword', 'languages', 'location', 'industry')
