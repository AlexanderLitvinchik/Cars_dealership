from django.contrib import admin
from .models import Supplier, SupplierDiscount, SupplierHistory
from autosalons.models import SupplierSpecificationRelationship

"""
Added for ManyToMany Relationship 
"""
class SupplierSpecificationRelationshipInLine(admin.TabularInline):
    model = SupplierSpecificationRelationship
    extra = 1


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'year_founded', 'get_discounts', 'get_supplier_specifications')
    list_filter = ('year_founded',)
    search_fields = ('name',)
    filter_horizontal = ('discount_suppliers',)
    inlines = [SupplierSpecificationRelationshipInLine]

    def get_discounts(self, obj):
        return ", ".join([str(discount) for discount in obj.discount_suppliers.all()])

    def get_supplier_specifications(self, obj):
        return ", ".join([str(specification) for specification in obj.supplier_specifications.all()])

    get_discounts.short_description = 'Discounts'
    get_supplier_specifications.short_description = 'Specifications'


@admin.register(SupplierDiscount)
class SupplierDiscountAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'discount_percentage')
    filter_horizontal = ('discount_suppliers',)
    list_filter = ('start_date', 'end_date', 'discount_percentage')

    search_fields = ('discount_percentage',)


@admin.register(SupplierHistory)
class SupplierHistoryAdmin(admin.ModelAdmin):
    list_display = ('sale_date', 'supplier', 'showroom', 'car')
    list_filter = ('sale_date', 'showroom', 'car')
    search_fields = ('showroom__name', 'car')
