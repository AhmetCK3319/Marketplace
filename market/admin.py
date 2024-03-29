from django.contrib import admin
from .models import Cart,Tax

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user','fooditem','quantity','created_at')

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('tax_type','tax_percentage','is_active')    