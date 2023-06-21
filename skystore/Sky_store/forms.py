from django import forms
from Sky_store.models import Product, ProdVersion

class NewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_desc', 'product_price', 'product_pic']

    def save(self, commit=True, user=None):
        product = super().save(commit=False)
        product.user = user
        if commit:
            product.save()
        return product


class ProductEditor(forms.ModelForm):
    version = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:

        model = Product
        fields = ('product_name', 'product_desc', 'product_price', 'product_pic')

    def save(self, commit=True):
        product = super().save(commit=False)
        version = self.cleaned_data['version'] or 1
        print(f'Номер версии в форме: {version}')
        product.save()
        version_update = ProdVersion(
            product=product,
            version=version,
            description=self.cleaned_data['product_desc'],
            price=self.cleaned_data['product_price'],
            photo=self.cleaned_data['product_pic']
        )


        version_update.set_current()
        return product

class ProdVersionForm(forms.ModelForm):

    version = forms.ModelChoiceField(queryset=ProdVersion.objects.none(), required=False)
    class Meta:
        model = Product
        fields = ['product_name', 'product_desc', 'product_price', 'product_pic', 'product_cat', 'version']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['version'].queryset = self.instance.versions.all()  # фильтруем версии текущего экземпляра
        if self.instance.current_version:
            self.fields['version'].initial = self.instance.current_version

    def save(self, commit=True):
        product = super().save(commit=False)
        product.current_version = self.cleaned_data.get('version')
        if commit:
            product.save()
        return product