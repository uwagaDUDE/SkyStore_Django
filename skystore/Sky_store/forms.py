from django import forms
from Sky_store.models import Product

class NewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_desc', 'product_price', 'product_pic']