from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, get_user_model
from django.views.generic import CreateView
from users.models import User
from users.forms import UserRegisterForm
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

# def email_verification(request, key):
#     User = get_user_model()
#     try:
#         user = User.objects.get(verif_code=key)
#     except ObjectDoesNotExist:
#         return render(request, 'Sky_store:error.html', {'message':'Ошибка отправки кода'})