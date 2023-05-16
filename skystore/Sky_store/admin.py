from django.contrib import admin
from Sky_store.models import Product
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'product_price', 'product_cat',)