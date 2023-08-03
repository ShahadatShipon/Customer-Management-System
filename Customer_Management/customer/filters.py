import django_filters 
from .models import *
from django_filters import DateFilter

class OrderFilter(django_filters.FilterSet):

    start_date=DateFilter(field_name='date_created' , lookup_expr='gte')
    end_date=DateFilter(field_name='date_created' , lookup_expr='lte')
    #category=django_filters.CharFilter(field_name='category',lookup_expr='icontains')

    """min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')"""

    class Meta:
        model=Order
        fields='__all__'
        exclude='customer','date_created'