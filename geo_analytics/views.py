from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins

from .models import (
    Company, 
    Field, 
    FieldMetricHistory
)

from .serializers import (
    CompanySerializer, 
    CompanyCreateWithAdminSerializer,
    FieldSerializer, 
    FieldMetricHistorySerializer
)


class CompanyViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Набір контролерів для моделі Field."""

    queryset = Company.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CompanyCreateWithAdminSerializer
        return CompanySerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        company_name = instance.name
        
        self.perform_destroy(instance)
        
        return Response(
            {"message": f"Компанію '{company_name}' та всі пов'язані акаунти успішно видалено."},
            status=status.HTTP_200_OK
        )


class FieldViewSet(viewsets.ModelViewSet):
    """Набір контролерів для моделі Field."""
    queryset = Field.objects.all()
    serializer_class = FieldSerializer

    @action(detail=True, methods=['get'], url_path='metrics')
    def get_metrics(self, request, pk=None):
        field = self.get_object()  
        
        metrics = FieldMetricHistory.objects.filter(
            field=field
        ).order_by('-date')
        
        serializer = FieldMetricHistorySerializer(metrics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FieldMetricHistoryViewSet(viewsets.ModelViewSet):
    """Набір контролерів для моделі FieldMetricHistory."""
    queryset = FieldMetricHistory.objects.all()
    serializer_class = FieldMetricHistorySerializer

