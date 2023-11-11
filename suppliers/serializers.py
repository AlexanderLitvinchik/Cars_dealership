from rest_framework import serializers

from autosalons.models import Car, Showroom
from .models import Supplier, SupplierDiscount, SupplierHistory


class SupplierDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierDiscount
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    discount_suppliers = SupplierDiscountSerializer(many=True, required=False)

    class Meta:
        model = Supplier
        fields = '__all__'


class SupplierHistorySerializer(serializers.ModelSerializer):
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())
    showroom = serializers.PrimaryKeyRelatedField(queryset=Showroom.objects.all())
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(), required=False, allow_null=True)

    class Meta:
        model = SupplierHistory
        fields = '__all__'
