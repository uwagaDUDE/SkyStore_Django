from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import get_user_model, login
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from users.models import User
from users.forms import UserRegistrationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.text import slugify

# Create your views here.

def mail_verif(request, user):
    site_url = 'http://localhost:8000/'
    verify_url = reverse('users:confirm_email', args=[slugify(user.email).replace('@', '-')])
    subject = "Подтверждение электронного адреса"
    message = f"Для подтверждения вашего электронного адреса перейдите по ссылке: {site_url}{verify_url}"
    from_email = 'skystoremessage@yandex.ru'
    to_email = user.email
    send_mail(subject, message, from_email, [to_email])

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            mail_verif(request, user)
            return render(request, 'users/email_confirmed.html', {'user': user})
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def email_verification(request, slug):
    user = get_object_or_404(User, slug=slug)
    user.is_active = True
    user.save()
    login(request, user)
    return redirect('home')