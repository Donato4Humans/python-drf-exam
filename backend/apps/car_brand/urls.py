from django.urls import path

from apps.car_brand.views import CarBrandListCreateView, CarBrandRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', CarBrandListCreateView.as_view(), name='car_brand_list'),
    path('/<int:pk>', CarBrandRetrieveUpdateDestroyAPIView.as_view(), name='car_brand_retrieve'),
]