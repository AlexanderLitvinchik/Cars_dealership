from django.contrib import admin
from .models import Specification, Supplier_Specification_price, Discount_autosalon, CarModel, Autosalon, \
    Autosalon_History, CarInAutosalon


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ('name_of_car',)
    filter_horizontal = ('autosalons_specification', 'supplier')
    list_filter = ('name_of_car',)


@admin.register(Supplier_Specification_price)
class SupplierSpecificationPriceAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'specification', 'supplier_specification_price', 'discount_supplier')
    list_filter = ('supplier', 'specification')


@admin.register(Discount_autosalon)
class DiscountAutosalonAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'discount_percentage')
    filter_horizontal = ('autosalons_discount',)
    list_filter = ('start_date', 'end_date', 'discount_percentage')


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('in_autosalon', 'specification','autosalons')
    list_filter = ('in_autosalon',)


@admin.register(Autosalon)
class AutosalonAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'balance')
    filter_horizontal = ('discount_autosalon', 'specifications')
    list_filter = ('name', 'location', 'balance')


@admin.register(CarInAutosalon)
class CarInAutosalonAdmin(admin.ModelAdmin):
    list_display = ('car_model', 'autosalon', 'price', 'quantity', 'discount_autosalon')
    list_filter = ('car_model', 'autosalon', 'quantity')


@admin.register(Autosalon_History)
class Autosalon_HistoryAdmin(admin.ModelAdmin):
    list_display = ('car', 'sale_date', 'amount', 'autosalon', 'unique_customer')
    list_filter = ('sale_date', 'amount')
