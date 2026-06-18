from django.urls import path

from .views import (
    WarehouseListView, 
    WarehouseCreateView, 
    WarehouseDeleteView,
    InventoryJournalView, 
    CreateTransactionView,
)


urlpatterns = [
    path('warehouses/', WarehouseListView.as_view(), name='warehouse_list'),
    path('warehouses/add/', WarehouseCreateView.as_view(), name='warehouse_add'),
    path('warehouses/<uuid:pk>/delete/', WarehouseDeleteView.as_view(), name='warehouse_delete'),
    path('warehouses/journal/', InventoryJournalView.as_view(), name='inventory_journal'),
    path('warehouses/transaction/add/', CreateTransactionView.as_view(), name='transaction_add'),
]