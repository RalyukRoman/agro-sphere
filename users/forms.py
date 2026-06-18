from django import forms
from django.contrib.auth import get_user_model
from geo_analytics.models import Company

from django.contrib.auth.forms import (
    UserCreationForm, 
    AuthenticationForm
)

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    """Форма для реєстрації звичайного користувача всередині компанії."""

    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        label="Оберіть вашу компанію",
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="-- Виберіть компанію зі списку --"
    )
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'phone_number']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Введіть логін'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'example@mail.com'
            }),

            'phone_number': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '+380...'
            }),
        }


class UserLoginForm(AuthenticationForm):
    """Форма для входу на сайт."""

    username = forms.CharField(
        label="Логін",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Ваш логін'
        })
    )

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Ваш пароль'
        })
    )


class UserProfileForm(forms.ModelForm):
    """Форма для редагування профілю."""
    
    class Meta:
        model = User
        fields = ['email', 'phone_number']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),

            'phone_number': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }