from django.db import transaction
from rest_framework.exceptions import ValidationError
from .models import Warehouse, WarehouseJournalEntry

class WarehouseTransactionService:
    """Сервіс для виконання операцій обліку зерна на складі."""

    @staticmethod
    def execute_transaction(validated_data: dict) -> WarehouseJournalEntry:
        """Виконати атомарну операцію обліку зерна на складі"""

        warehouse = validated_data['warehouse']
        entry_type = validated_data['entry_type']
        weight_tons = validated_data['weight_tons']
        
        with transaction.atomic():
            # Блокуємо склад від Race Conditions на час транзакції
            warehouse_locked = Warehouse.objects.select_for_update().get(id=warehouse.id)
            
            if entry_type == 'INCOMING':
                if warehouse_locked.current_balance_tons + weight_tons > warehouse_locked.capacity_tons:
                    raise ValidationError({
                        "detail": f"Недостатньо місця на складі. Вільно: {warehouse_locked.capacity_tons - warehouse_locked.current_balance_tons} тонн."
                    })
                warehouse_locked.current_balance_tons += weight_tons
                
            elif entry_type in ['OUTGOING', 'RESERVED']:
                if warehouse_locked.current_balance_tons < weight_tons:
                    raise ValidationError({
                        "detail": f"Недостатньо зерна для операції ({entry_type}). Доступно лише: {warehouse_locked.current_balance_tons} тонн."
                    })
                warehouse_locked.current_balance_tons -= weight_tons
                
            warehouse_locked.save()
            validated_data['warehouse'] = warehouse_locked

            entry = WarehouseJournalEntry.objects.create(**validated_data)
            return entry