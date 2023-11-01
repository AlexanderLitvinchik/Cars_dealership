from django.contrib import admin
from .models import Supplier, Supplier_Discount, Supplier_History


# class SupplierDiscountInline(admin.TabularInline):
#     model = Supplier.discount_suppliers.through
#     extra = 1
#
#
# class DiscountSippliersInline(admin.TabularInline):
#     model = Supplier.discount_suppliers.through
#     extra = 1


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'year_founded', 'get_discounts')
    list_filter = ('year_founded',)
    search_fields = ('name',)
    filter_horizontal = ('discount_suppliers',)

    def get_discounts(self, obj):
        return ", ".join([str(discount) for discount in obj.discount_suppliers.all()])

    get_discounts.short_description = 'Discounts'


@admin.register(Supplier_Discount)
class SupplierDiscountAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'discount_percentage')
    filter_horizontal = ('discount_suppliers',)
    list_filter = ('start_date', 'end_date', 'discount_percentage')

    search_fields = ('discount_percentage',)


@admin.register(Supplier_History)
class Supplier_HistoryAdmin(admin.ModelAdmin):
    list_display = ('sale_date', 'supplier', 'autosalon', 'car')
    list_filter = ('sale_date', 'autosalon', 'car')

    search_fields = ('autosalon__name', 'car')
