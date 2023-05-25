from django.shortcuts import render
from Sky_store.models import Product
from django.views.generic import ListView
from Sky_store.services import send_email
from django.core.mail import send_mail

# def store_page(request):
#     context = {'object_list': Product.objects.all()}
#     return render(request, 'sky_store/home.html', context=context)

def start_page(request):
    return render(request, 'sky_store/home.html')
class ProductStore(ListView):
    model = Product
    mail = send_email

    def mail_sender(self):

# Create your views here.
