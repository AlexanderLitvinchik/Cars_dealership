from django.contrib import admin
from .models import Specification, ShowroomDiscount, Car, Showroom, \
    ShowroomHistory, ShowroomCarRelationship


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ('name_of_car', 'color', 'mileage')
    filter_horizontal = ('showrooms_specification', 'supplier')
    list_filter = ('name_of_car',)


@admin.register(ShowroomDiscount)
class ShowroomDiscountAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'discount_percentage')
    filter_horizontal = ('showrooms_discount',)
    list_filter = ('start_date', 'end_date', 'discount_percentage')


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('in_showroom', 'specification', 'serial_number', 'get_showrooms')
    list_filter = ('in_showroom',)

    def get_showrooms(self, obj):
        return ", ".join([showroom.name for showroom in obj.showrooms.all()])

    get_showrooms.short_description = 'Showrooms'


class ShowroomCarRelationshipInline(admin.TabularInline):
    model = ShowroomCarRelationship
    extra = 1


@admin.register(Showroom)
class ShowroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'balance', 'get_cars')
    filter_horizontal = ('discount_showroom', 'specifications', 'car')
    list_filter = ('name', 'location', 'balance')
    inlines = [ShowroomCarRelationshipInline]

    def get_cars(self, obj):
        return ", ".join([str(car) for car in obj.car.all()])

    get_cars.short_description = 'Cars'


@admin.register(ShowroomHistory)
class ShowroomHistoryAdmin(admin.ModelAdmin):
    list_display = ('car', 'sale_date', 'amount', 'showroom', 'unique_customer')
    list_filter = ('sale_date', 'amount')
