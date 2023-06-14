from django import forms
from Sky_store.models import Product, ProdVersion

class NewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_desc', 'product_price', 'product_pic']

    def save(self, commit=True):
        product = super().save(commit=False)
        product.version_num = 0
        product.save()

class ProductEditor(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_desc', 'product_price', 'product_pic']

    def save(self, commit=True):
        product = super().save(commit=False)
        if commit:
            product.save()
            if product.version_cur:
                latest_version = ProdVersion.objects.filter(product=product).latest('created_at')
                version_update = ProdVersion(product=product, version_num=latest_version.version_num + 1)
            else:
                version_update = ProdVersion(product=product, version_num=1)
            version_update.save()
            product.version_cur = True
            product.version_num = version_update.version_num
            product.save()
        return product
