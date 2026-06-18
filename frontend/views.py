from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import Http404

from geo_analytics.models import Field, Company, FieldMetricHistory
from geo_analytics.forms import CompanyForm, FieldForm, FieldMetricHistoryForm
from warehousing.models import Warehouse, WarehouseJournalEntry
from warehousing.forms import WarehouseJournalEntryForm, WarehouseForm
from smart_planning.forms import SmartPlanningCalculateForm
from users.models import User
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm

from smart_planning.models import CropPlan

import json

from django.views.generic import (
    TemplateView, 
    CreateView, 
    ListView, 
    DetailView, 
    UpdateView, 
    DeleteView,
    FormView
)

from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    UserPassesTestMixin
)

# =========================================================
#  Публічні сторінки
# =========================================================

class LandingPageView(TemplateView):
    """Головна сторінка (Landing Page) з презентацією платформи."""
    template_name = 'frontend/index.html'


class RegisterCompanyView(CreateView):
    """Сторінка B2B реєстрації компанії та її адміністратора."""

    template_name = 'frontend/auth/register.html'
    form_class = CompanyForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """Зберігає форму та перенаправляє на сторінку входу."""
        form.save()
        return redirect(self.success_url)


class UserLoginView(LoginView):
    """Сторінка входу до системи."""
    template_name = 'frontend/auth/login.html'
    authentication_form = UserLoginForm


# =========================================================
#  Модуль «Управління полями та ГІС»
# =========================================================

class MapDashboardView(LoginRequiredMixin, TemplateView):
    """Дашборд з інтерактивною картою."""
    template_name = 'frontend/geo/map_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = Field.objects.filter(company=self.request.user.company)
        context['warehouses'] = Warehouse.objects.filter(company=self.request.user.company)
        return context


class FieldCreateView(LoginRequiredMixin, CreateView):
    """Сторінка створення нового поля."""

    model = Field
    form_class = FieldForm
    template_name = 'frontend/geo/field_editor.html'
    success_url = reverse_lazy('map_dashboard')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.company = self.request.user.company
        return super().form_valid(form)


class FieldUpdateView(LoginRequiredMixin, UpdateView):
    """Сторінка редагування поля."""
    
    model = Field
    form_class = FieldForm
    template_name = 'frontend/geo/field_editor.html'
    success_url = reverse_lazy('map_dashboard')


class FieldDeleteView(LoginRequiredMixin, DeleteView):
    """Сторінка підтвердження видалення поля."""

    model = Field
    template_name = 'frontend/geo/field_confirm_delete.html'
    success_url = reverse_lazy('map_dashboard')

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_authenticated and hasattr(self.request.user, 'company'):
            return queryset.filter(company=self.request.user.company)
        
        raise Http404("Ви не маєте доступу до цього об'єкта або не авторизовані.")


class FieldAnalyticsView(LoginRequiredMixin, DetailView):
    """Детальна аналітика конкретного поля."""

    model = Field
    template_name = 'frontend/geo/field_analytics.html'
    context_object_name = 'field'

    def get_context_data(self, **kwargs):
        """Отримати інформацію про метрики поля."""

        context = super().get_context_data(**kwargs)

        context['metrics'] = FieldMetricHistory.objects.filter(
            field=self.get_object()
        ).order_by('-date')

        return context


class FieldMetricCreateView(LoginRequiredMixin, CreateView):
    """Контролер для додавання нових метрик стану поля."""

    model = FieldMetricHistory
    form_class = FieldMetricHistoryForm
    template_name = 'frontend/geo/metric_form.html'

    def get_success_url(self):
        """Повертає на сторінку аналітики відповідного поля."""
        return reverse_lazy(
            'field_analytics', 
            kwargs={'pk': self.object.field.pk}
        )


# =========================================================
#  Модуль «Склади та логістика»
# =========================================================

class WarehouseListView(LoginRequiredMixin, ListView):
    """Список складів компанії з показниками завантаженості."""

    model = Warehouse
    template_name = 'frontend/warehousing/warehouse_list.html'
    context_object_name = 'warehouses'

    def get_queryset(self):
        return Warehouse.objects.filter(
            company=self.request.user.company
        )


class WarehouseCreateView(LoginRequiredMixin, CreateView):
    """Сторінка додавання нового складу на карту."""

    model = Warehouse
    form_class = WarehouseForm
    template_name = 'frontend/warehousing/warehouse_form.html'
    success_url = reverse_lazy('warehouse_list')

    def form_valid(self, form):
        """Прив'язує новий склад до компанії користувача."""

        form.instance.company = self.request.user.company
        return super().form_valid(form)


class WarehouseDeleteView(LoginRequiredMixin, DeleteView):
    """Сторінка підтвердження видалення складу."""

    model = Warehouse
    template_name = 'frontend/warehouses/warehouse_confirm_delete.html'
    success_url = reverse_lazy('warehouse_list')

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_authenticated and hasattr(self.request.user, 'company'):
            return queryset.filter(company=self.request.user.company)
        
        raise Http404("Доступ заборонено.")


class InventoryJournalView(LoginRequiredMixin, ListView):
    """Журнал складських операцій для всіх складів компанії."""
    model = WarehouseJournalEntry
    template_name = 'frontend/warehousing/journal.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return WarehouseJournalEntry.objects.filter(
            warehouse__company=self.request.user.company
        )


class CreateTransactionView(LoginRequiredMixin, CreateView):
    """Сторінка створення нової транзакції."""

    model = WarehouseJournalEntry
    form_class = WarehouseJournalEntryForm
    template_name = 'frontend/warehousing/transaction_form.html'
    success_url = reverse_lazy('inventory_journal')

    def get_initial(self):
        return {'operator_id': self.request.user.id}


# =========================================================
#  Модуль «Розумне планування»
# =========================================================

class PlanCalculatorView(LoginRequiredMixin, FormView):
    """Форма для розрахунку оптимального плану посіву."""
    
    form_class = SmartPlanningCalculateForm
    template_name = 'frontend/planning/calculator.html'
    success_url = reverse_lazy('plan_results')


class PlanResultsView(LoginRequiredMixin, TemplateView):
    """Сторінка результатів розрахунку з динамічними даними від CropSolverService."""
    template_name = 'frontend/planning/results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        plan_id = self.request.GET.get('plan_id')
        if not plan_id:
            raise Http404("Параметр plan_id відсутній. Будь ласка, виконайте розрахунок спочатку.")

        crop_plan = get_object_or_404(
            CropPlan.objects.select_related('field', 'suggested_crop'), 
            id=plan_id, 
            field__company=self.request.user.company
        )
        
        chart_labels = []
        chart_data = []
        table_rows = []

        chart_labels.append(crop_plan.suggested_crop.name)
        chart_data.append(float(crop_plan.field.area_hectares))
        
        table_rows.append({
            'field': crop_plan.field.name,
            'crop': crop_plan.suggested_crop.name,
            'area': float(crop_plan.field.area_hectares),
            'yield': float(crop_plan.expected_yield),
            'costs': float(crop_plan.estimated_profit) * 0.30
        })

        efficiency_rate = int(crop_plan.confidence_score * 100) if crop_plan.confidence_score else 100

        calculated_data = {
            'total_profit': float(crop_plan.estimated_profit),
            'efficiency_rate': efficiency_rate,
            'recommended_crop': crop_plan.suggested_crop.name,
            'table_rows': table_rows
        }

        context['plan'] = calculated_data
        
        # Безпечно серіалізуємо масиви для JavaScript
        context['chart_labels_json'] = json.dumps(chart_labels)
        context['chart_data_json'] = json.dumps(chart_data)
        
        return context


# =========================================================
#  Адміністративна панель компанії
# =========================================================

class IsCompanyAdminMixin(UserPassesTestMixin):
    """Міксин, що дозволяє доступ тільки користувачам з роллю admin."""

    def test_func(self):
        return self.request.user.role == 'admin'


class EmployeeManagementView(LoginRequiredMixin, IsCompanyAdminMixin, ListView):
    """Управління працівниками компанії."""

    model = User
    template_name = 'frontend/admin/employees.html'
    context_object_name = 'employees'

    def get_queryset(self):
        return User.objects.filter(company=self.request.user.company)


class EmployeeCreateView(LoginRequiredMixin, IsCompanyAdminMixin, CreateView):
    """Додавання нового працівника адміністратором компанії."""

    model = User
    form_class = UserRegistrationForm
    template_name = 'frontend/admin/employee_form.html'
    success_url = reverse_lazy('employee_mgmt')

    def get_initial(self):
        """Передає компанію адміністратора у форму."""
        return {'company': self.request.user.company}


class CompanySettingsView(LoginRequiredMixin, IsCompanyAdminMixin, UpdateView):
    """Налаштування параметрів компанії."""

    model = Company
    fields = ['name']
    template_name = 'frontend/admin/company_settings.html'
    success_url = reverse_lazy('company_settings')

    def get_object(self):
        return self.request.user.company


# =========================================================
#  Загальні системні сторінки
# =========================================================

class UserProfileView(LoginRequiredMixin, UpdateView):
    """Редагування профілю поточного користувача."""

    model = User
    form_class = UserProfileForm
    template_name = 'frontend/accounts/profile.html'
    success_url = reverse_lazy('user_profile')

    def get_object(self):
        return self.request.user


class Error403View(TemplateView):
    """Сторінка помилки доступу."""
    template_name = 'frontend/errors/403.html'


class Error404View(TemplateView):
    """Сторінка «Не знайдено»."""
    template_name = 'frontend/errors/404.html'
