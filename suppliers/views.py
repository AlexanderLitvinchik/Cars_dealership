from rest_framework import viewsets, mixins
from autosalons.models import Supplier_Specification_price
from autosalons.serializers import SupplierSpecificationPriceSerializer
from .models import Supplier_Discount, Supplier_History
from .serializers import SupplierDiscountSerializer, Supplier_HistorySerializer


class SupplierDiscountViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                              viewsets.GenericViewSet):
    queryset = Supplier_Discount.objects.all()
    serializer_class = SupplierDiscountSerializer


class Supplier_HistoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                              viewsets.GenericViewSet):
    queryset = Supplier_History.objects.all()
    serializer_class = Supplier_HistorySerializer


class SupplierSpecificationPriceViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                                        viewsets.GenericViewSet):
    queryset = Supplier_Specification_price.objects.all()
    serializer_class = SupplierSpecificationPriceSerializer
