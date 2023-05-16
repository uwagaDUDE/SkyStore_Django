from django.shortcuts import render
from Sky_store.models import Product

def store_page(request):
    context = {'object_list': Product.objects.all()}
    return render(request, 'sky_store/home.html', context=context)
# Create your views here.
