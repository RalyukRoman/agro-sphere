from django.urls import reverse_lazy
from django.http import Http404

from warehousing.models import Warehouse, WarehouseJournalEntry
from warehousing.forms import WarehouseJournalEntryForm, WarehouseForm

from django.views.generic import (
    CreateView, 
    ListView, 
    DeleteView,
)

from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
)


class WarehouseListView(LoginRequiredMixin, ListView):
    """Список складів компанії з показниками завантаженості."""

    model = Warehouse
    template_name = 'warehousing/warehouse_list.html'
    context_object_name = 'warehouses'

    def get_queryset(self):
        return Warehouse.objects.filter(
            company=self.request.user.company
        )


class WarehouseCreateView(LoginRequiredMixin, CreateView):
    """Сторінка додавання нового складу на карту."""

    model = Warehouse
    form_class = WarehouseForm
    template_name = 'warehousing/warehouse_form.html'
    success_url = reverse_lazy('warehouse_list')

    def form_valid(self, form):
        """Прив'язує новий склад до компанії користувача."""

        form.instance.company = self.request.user.company
        return super().form_valid(form)


class WarehouseDeleteView(LoginRequiredMixin, DeleteView):
    """Сторінка підтвердження видалення складу."""

    model = Warehouse
    template_name = 'warehouses/warehouse_confirm_delete.html'
    success_url = reverse_lazy('warehouse_list')

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_authenticated and hasattr(self.request.user, 'company'):
            return queryset.filter(company=self.request.user.company)
        
        raise Http404("Доступ заборонено.")


class InventoryJournalView(LoginRequiredMixin, ListView):
    """Журнал складських операцій для всіх складів компанії."""
    model = WarehouseJournalEntry
    template_name = 'warehousing/journal.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return WarehouseJournalEntry.objects.filter(
            warehouse__company=self.request.user.company
        )


class CreateTransactionView(LoginRequiredMixin, CreateView):
    """Сторінка створення нової транзакції."""

    model = WarehouseJournalEntry
    form_class = WarehouseJournalEntryForm
    template_name = 'warehousing/transaction_form.html'
    success_url = reverse_lazy('inventory_journal')

    def get_initial(self):
        return {'operator_id': self.request.user.id}