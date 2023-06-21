from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=28, required=True)
    country = forms.CharField(max_length=30, required=True)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['email', 'phone', 'country', 'password1', 'password2', 'avatar']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.phone = self.cleaned_data['phone']
        user.country = self.cleaned_data['country']
        user.avatar = self.cleaned_data['avatar']
        if commit:
            user.save()
        return user