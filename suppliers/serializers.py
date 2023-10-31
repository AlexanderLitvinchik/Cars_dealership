from rest_framework import serializers

from autosalons.models import CarModel, Autosalon
from .models import Supplier, Supplier_Discount, Sales_of_suppliers


# from autosalons.serializers import AutosalonSerializer, CarModelSerializer


class SupplierDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier_Discount
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    discount_suppliers = SupplierDiscountSerializer(many=True, read_only=True)

    class Meta:
        model = Supplier
        fields = '__all__'


class SalesOfSuppliersSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer()
    autosalon = serializers.PrimaryKeyRelatedField(queryset=Autosalon.objects.all())
    car = serializers.PrimaryKeyRelatedField(queryset=CarModel.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Sales_of_suppliers
        fields = '__all__'
