from django.contrib import admin
from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['name', 'condition', 'price', 'sale_status', 'created_at']
    list_filter = ['condition', 'sale_status', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']
