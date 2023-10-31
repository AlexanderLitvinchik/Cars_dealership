from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    list_filter = ('balance',)
    search_fields = ('user__username', 'user__email')
