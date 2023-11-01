from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'supplier_discounts', views.SupplierDiscountViewSet)
router.register(r'history_of_suppliers', views.Supplier_HistoryViewSet)
router.register(r'supplier_specification_prices', views.SupplierSpecificationPriceViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
