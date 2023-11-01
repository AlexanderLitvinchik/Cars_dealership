from rest_framework import serializers

from autosalons.models import CarModel, Autosalon
from .models import Supplier, Supplier_Discount, Supplier_History


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


class Supplier_HistorySerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer()
    autosalon = serializers.PrimaryKeyRelatedField(queryset=Autosalon.objects.all())
    car = serializers.PrimaryKeyRelatedField(queryset=CarModel.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Supplier_History
        fields = '__all__'
