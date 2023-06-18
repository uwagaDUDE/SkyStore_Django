from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
import uuid

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email_verification_token = str(uuid.uuid4())
        if commit:
            user.save()
            verification_url = settings.BASE_URL + reverse('email_verification', args=[user.email_verification_token])
            html_message = render_to_string('email_verification.html', {'verification_url': verification_url})
            subject = 'Подтверждение адреса электронной почты'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            send_mail(subject, '', from_email, recipient_list, html_message=html_message, fail_silently=False)
        return user