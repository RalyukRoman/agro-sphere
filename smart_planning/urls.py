from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CropCultureViewSet, CropPlanViewSet, SmartPlanningViewSet

router = DefaultRouter()

router.register(r'crop-cultures', CropCultureViewSet)
router.register(r'crop-plans', CropPlanViewSet)
router.register(r'smart-planning', SmartPlanningViewSet, basename='smart-planning')

urlpatterns = [
    path('', include(router.urls)),
]