from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .services import WarehouseTransactionService

from .models import (
    Warehouse, 
    GrainBatch, 
    WarehouseJournalEntry
)

from .serializers import (
    WarehouseSerializer, 
    GrainBatchSerializer, 
    WarehouseJournalEntrySerializer
)


class WarehouseViewSet(viewsets.ModelViewSet):
    """Набір контролерів для керування складами."""
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

    @action(detail=True, methods=['get'])
    def balance(self, request, pk: str = None) -> Response:
        """Отримати поточний баланс конкретного складу."""

        warehouse = self.get_object()
        
        return Response({
            "warehouse_name": warehouse.name,
            "current_balance_tons": warehouse.current_balance_tons,
            "capacity_tons": warehouse.capacity_tons
        })

    @action(detail=False, methods=['post'], url_path='transactions')
    def create_transaction(self, request) -> Response:
        """Створити нову операцію в журналі (приймання/відвантаження)."""

        serializer = WarehouseJournalEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        entry = WarehouseTransactionService.execute_transaction(
            serializer.validated_data
        )
        
        return Response(
            WarehouseJournalEntrySerializer(entry).data, 
            status=status.HTTP_201_CREATED
        )


class GrainBatchViewSet(viewsets.ModelViewSet):
    """Набір контролерів для керування партіями зерна."""
    queryset = GrainBatch.objects.all()
    serializer_class = GrainBatchSerializer