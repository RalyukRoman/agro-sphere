from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import CropCulture, CropPlan
from .services import CropSolverService

from .serializers import (
    CropCultureSerializer, 
    CropPlanSerializer
)


class CropCultureViewSet(viewsets.ModelViewSet):
    """Набір контролерів для перегляду та редагування культур."""
    queryset = CropCulture.objects.all()
    serializer_class = CropCultureSerializer


class CropPlanViewSet(viewsets.ReadOnlyModelViewSet):
    """Набір контролерів для перегляду історії планів посіву."""
    queryset = CropPlan.objects.all()
    serializer_class = CropPlanSerializer


class SmartPlanningViewSet(viewsets.GenericViewSet):
    """Контролер для виконання складних операцій планування."""

    @action(detail=False, methods=['post'])
    def calculate(self, request) -> Response:
        """Запустити алгоритм оптимізації."""

        data = request.data
        field_id = data.get('field_id')
        budget_raw = data.get('budget')

        try:
            budget = float(budget_raw) if budget_raw is not None else None
        except ValueError:
            return Response(
                {"error": "Поле budget має бути числовим"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if not field_id:
            return Response(
                {"error": "field_id є обов'язковим полем"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        result = CropSolverService.calculate_optimal_plan(
            field_id, budget
        )

        if "error" in result:
            return Response(
                data=result, 
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        return Response(
            data=result, 
            status=status.HTTP_200_OK
        )