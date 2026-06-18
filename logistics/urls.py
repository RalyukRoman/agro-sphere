from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TruckViewSet, TransportOrderViewSet

router = DefaultRouter()

router.register(r'trucks', TruckViewSet)
router.register(r'transport-orders', TransportOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]