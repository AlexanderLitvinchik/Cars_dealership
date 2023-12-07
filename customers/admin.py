from django.contrib import admin
from .models import Customer, Offer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'get_history', 'email_confirmed',)
    list_filter = ('balance',)
    search_fields = ('user__username', 'user__email')

    def get_history(self, obj):
        return ", ".join([str(history.car) for history in obj.customer_histories.all()])

    get_history.short_description = 'History'





@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """
    Added admin for new model offer
    """
    list_display = ('customer', 'max_price', 'name_of_car', 'year')
