from rest_framework import serializers


class CustomerStatisticsSerializer(serializers.Serializer):
    customer_name = serializers.CharField()
    car_models_bought = serializers.ListField(allow_empty=True)
    cars_quantity = serializers.IntegerField(min_value=0)
    money_spent = serializers.DecimalField(max_digits=15, decimal_places=2, allow_null=True)


class ShowroomStatisticsSerializer(serializers.Serializer):
    showroom_name = serializers.CharField()
    cars_quantity_sold = serializers.IntegerField()
    money_earned = serializers.DecimalField(max_digits=15, decimal_places=2, allow_null=True)
    money_spent = serializers.DecimalField(max_digits=15, decimal_places=2, allow_null=True)
    money_income = serializers.DecimalField(max_digits=15, decimal_places=2, allow_null=True)
    most_expensive_deal = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    top_cars = serializers.ListField(allow_empty=True)
    top_customers = serializers.ListField(allow_empty=True)
    top_suppliers = serializers.ListField(allow_empty=True)


class SupplierStatisticsSerializer(serializers.Serializer):
    supplier_name = serializers.CharField()
    cars_quantity_sold = serializers.IntegerField()
    money_earned = serializers.DecimalField(max_digits=15, decimal_places=2, allow_null=True)
    most_expensive_deal = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    top_showrooms = serializers.ListField(allow_empty=True)
    top_cars = serializers.ListField(allow_empty=True)
