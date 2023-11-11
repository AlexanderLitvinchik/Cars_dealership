from rest_framework import serializers

from customers.models import Customer
from suppliers.models import SupplierDiscount, Supplier
from .models import Specification, Car, Showroom, ShowroomCarRelationship, ShowroomHistory, ShowroomDiscount, \
    SupplierSpecificationRelationship
from suppliers.serializers import SupplierSerializer


class ShowroomDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowroomDiscount
        fields = '__all__'


class SpecificationSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(many=True)

    class Meta:
        model = Specification
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    specification = serializers.PrimaryKeyRelatedField(many=False, queryset=Specification.objects.all())

    class Meta:
        model = Car
        fields = '__all__'


class ShowroomCarRelationshipSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(), required=False,
                                             allow_null=True)
    showroom = serializers.PrimaryKeyRelatedField(queryset=Showroom.objects.all())
    discount_showroom = serializers.PrimaryKeyRelatedField(queryset=ShowroomDiscount.objects.all(), required=False,
                                                           allow_null=True)

    class Meta:
        model = ShowroomCarRelationship
        fields = '__all__'


class ShowroomHistorySerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())
    unique_customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    showroom = serializers.PrimaryKeyRelatedField(queryset=Showroom.objects.all())

    class Meta:
        model = ShowroomHistory
        fields = '__all__'


class SupplierSpecificationRelationshipSerializer(serializers.ModelSerializer):
    specification = serializers.PrimaryKeyRelatedField(queryset=Specification.objects.all())
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())
    discount_supplier = serializers.PrimaryKeyRelatedField(queryset=SupplierDiscount.objects.all(), required=False,
                                                           allow_null=True)

    class Meta:
        model = SupplierSpecificationRelationship
        fields = '__all__'


class ShowroomSerializer(serializers.ModelSerializer):
    # car = ShowroomCarRelationshipSerializer(many=True)
    discount_showroom = ShowroomDiscountSerializer(many=True, required=False)
    specifications = SpecificationSerializer(many=True)

    class Meta:
        model = Showroom
        fields = '__all__'
