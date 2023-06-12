from django import forms
from Sky_store.models import Product, ProdVersion

class NewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_desc', 'product_price', 'product_pic']

class ProductEditor(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_desc', 'product_price', 'product_pic']

    def save(self, commit=True):
        product = super().save(commit=False)
        if commit:
            product.save()
            version_update = ProdVersion(product=product,
                                         version_num=product.version_cur.version_num +1)
            version_update.save()
            product.version_cur = version_update
            product.save()
        return product