from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import redirect

from geo_analytics.forms import CompanyForm
from users.models import User
from users.forms import UserLoginForm, UserProfileForm

from django.views.generic import (
    CreateView, 
    UpdateView, 
)

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)


class RegisterCompanyView(CreateView):
    """Сторінка реєстрації компанії та її адміністратора."""

    template_name = 'users/register_company.html'
    form_class = CompanyForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """Зберігає форму та перенаправляє на сторінку входу."""
        form.save()
        return redirect(self.success_url)


class UserLoginView(LoginView):
    """Сторінка входу до системи."""
    template_name = 'users/login.html'
    authentication_form = UserLoginForm


class UserProfileView(LoginRequiredMixin, UpdateView):
    """Редагування профілю поточного користувача."""

    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('user_profile')

    def get_object(self):
        return self.request.user