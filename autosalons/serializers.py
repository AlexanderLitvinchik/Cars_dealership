from rest_framework import serializers

from suppliers.models import Supplier_Discount, Supplier
from .models import Specification, CarModel, Autosalon, CarInAutosalon, Autosalon_Sales, Discount_autosalon, \
    Supplier_Specification_price
from customers.serializers import CustomerSerializer
from suppliers.serializers import SupplierSerializer


class DiscountAutosalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount_autosalon
        fields = '__all__'


class CarModelSerializer(serializers.ModelSerializer):
    specification = serializers.PrimaryKeyRelatedField(queryset=Specification.objects.all())

    class Meta:
        model = CarModel
        fields = '__all__'


class CarInAutosalonSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset=CarModel.objects.all(), required=False,
                                             allow_null=True)
    autosalon = serializers.PrimaryKeyRelatedField(queryset=Autosalon.objects.all())
    discount_autosalon = serializers.PrimaryKeyRelatedField(queryset=Discount_autosalon.objects.all())

    class Meta:
        model = CarInAutosalon
        fields = '__all__'


class AutosalonSalesSerializer(serializers.ModelSerializer):
    car = CarModelSerializer(read_only=True)
    unique_customer = CustomerSerializer(read_only=True)
    autosalon = serializers.PrimaryKeyRelatedField(queryset=Autosalon.objects.all())

    class Meta:
        model = Autosalon_Sales
        fields = '__all__'


class SupplierSpecificationPriceSerializer(serializers.ModelSerializer):
    specification = serializers.PrimaryKeyRelatedField(queryset=Specification.objects.all())
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())
    discount_supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier_Discount.objects.all(), required=False,
                                                           allow_null=True)

    class Meta:
        model = Supplier_Specification_price
        fields = '__all__'


class SpecificationSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(many=True, read_only=True)

    class Meta:
        model = Specification
        fields = '__all__'


class AutosalonSerializer(serializers.ModelSerializer):
    cars = CarInAutosalonSerializer(many=True, read_only=True)
    autosalons_discount = DiscountAutosalonSerializer(many=True, read_only=True)
    autosalons_specification = SpecificationSerializer(many=True, read_only=True)

    class Meta:
        model = Autosalon
        fields = '__all__'
