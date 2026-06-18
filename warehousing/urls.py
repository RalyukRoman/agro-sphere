from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WarehouseViewSet, GrainBatchViewSet

router = DefaultRouter()

router.register(r'warehouses', WarehouseViewSet)
router.register(r'grain-batches', GrainBatchViewSet)

urlpatterns = [
    path('', include(router.urls)),
]