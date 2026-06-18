from django.urls import path
from .views import (
    LandingPageView, RegisterCompanyView, UserLoginView,
    MapDashboardView, FieldAnalyticsView,
    WarehouseListView, WarehouseCreateView, WarehouseDeleteView,
    InventoryJournalView, CreateTransactionView,
    EmployeeCreateView,
    FieldCreateView, FieldUpdateView, FieldDeleteView,
    PlanCalculatorView, PlanResultsView,
    EmployeeManagementView, CompanySettingsView,
    UserProfileView
)

urlpatterns = [
    # Публічні сторінки
    path('', LandingPageView.as_view(), name='index'),
    path('register/', RegisterCompanyView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),

    # ГІС та Поля
    path('dashboard/', MapDashboardView.as_view(), name='map_dashboard'),
    path('fields/add/', FieldCreateView.as_view(), name='field_add'),
    path('fields/<uuid:pk>/edit/', FieldUpdateView.as_view(), name='field_edit'),
    path('fields/<uuid:pk>/delete/', FieldDeleteView.as_view(), name='field_delete'),
    path('fields/<uuid:pk>/analytics/', FieldAnalyticsView.as_view(), name='field_analytics'),

    # Склади
    path('warehouses/', WarehouseListView.as_view(), name='warehouse_list'),
    path('warehouses/add/', WarehouseCreateView.as_view(), name='warehouse_add'),
    path('warehouses/<uuid:pk>/delete/', WarehouseDeleteView.as_view(), name='warehouse_delete'),
    path('warehouses/journal/', InventoryJournalView.as_view(), name='inventory_journal'),
    path('warehouses/transaction/add/', CreateTransactionView.as_view(), name='transaction_add'),

    # Розумне планування
    path('planning/calculate/', PlanCalculatorView.as_view(), name='plan_calculate'),
    path('planning/results/', PlanResultsView.as_view(), name='plan_results'),

    # Адмінка компанії
    path('admin/employees/', EmployeeManagementView.as_view(), name='employee_mgmt'),
    path('admin/employees/add/', EmployeeCreateView.as_view(), name='employee_add'),
    path('admin/company/', CompanySettingsView.as_view(), name='company_settings'),

    # Профіль користувача
    path('accounts/profile/', UserProfileView.as_view(), name='user_profile'),
]