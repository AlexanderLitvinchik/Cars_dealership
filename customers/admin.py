from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'get_history')
    list_filter = ('balance',)
    search_fields = ('user__username', 'user__email')

    def get_history(self, obj):
        return ", ".join([str(history.car) for history in obj.customer_histories.all()])

    get_history.short_description = 'History'
