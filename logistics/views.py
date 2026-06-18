from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import (
    Truck, 
    TransportOrder
)

from .serializers import (
    TruckSerializer, 
    TransportOrderSerializer
)


class TruckViewSet(viewsets.ModelViewSet):
    """Набір контролерів для моделі Truck."""
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer


class TransportOrderViewSet(viewsets.ModelViewSet):
    """Набір контролерів для моделі TransportOrder."""
    queryset = TransportOrder.objects.all()
    serializer_class = TransportOrderSerializer