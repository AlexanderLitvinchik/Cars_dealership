# statistics_app/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShowroomStatisticsViewSet, SupplierStatisticsViewSet, CustomerStatisticsViewSet

router = DefaultRouter()
router.register(r'showroom', ShowroomStatisticsViewSet, basename='showroom_statistics')
router.register(r'supplier', SupplierStatisticsViewSet, basename='supplier_statistics')
router.register(r'customer', CustomerStatisticsViewSet, basename='customer_statistics')

urlpatterns = [
    path('', include(router.urls)),
]
