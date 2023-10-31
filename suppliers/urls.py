from django.urls import path
from . import views

urlpatterns = [
    path('supplier_discounts/', views.SupplierDiscountListCreateView.as_view(), name='supplier-discount-list-create'),
    path('supplier_discounts/<int:pk>/', views.SupplierDiscountUpdateView.as_view(), name='supplier-discount-update'),
    path('sales_of_suppliers/', views.SalesOfSuppliersListCreateView.as_view(), name='sales-of-suppliers-list-create'),
    path('sales_of_suppliers/<int:pk>/', views.SalesOfSuppliersUpdateView.as_view(), name='sales-of-suppliers-update'),
    path('supplier_specification_prices/', views.SupplierSpecificationPriceListCreateView.as_view(),
         name='supplier-specification-price-list-create'),
    path('supplier_specification_prices/<int:pk>/', views.SupplierSpecificationPriceUpdateView.as_view(),
         name='supplier-specification-price-update'),
    path('supplier_specification_prices/api/', views.SupplierSpecificationPriceAPIView.as_view(),
         name='supplier-specification-price-api'),
]
