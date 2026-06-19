from django.urls import path

from .views import (
    PlanCalculatorView, 
    PlanResultsView,
    CropCultureListView, 
    CropCultureCreateView, 
    CropCultureUpdateView, 
    CropCultureDeleteView
)


urlpatterns = [
    path('planning/calculate/', PlanCalculatorView.as_view(), name='plan_calculate'),
    path('planning/results/', PlanResultsView.as_view(), name='plan_results'),

    path('cultures/', CropCultureListView.as_view(), name='culture_list'),
    path('cultures/add/', CropCultureCreateView.as_view(), name='culture_create'),
    path('cultures/<uuid:pk>/edit/', CropCultureUpdateView.as_view(), name='culture_update'),
    path('cultures/<uuid:pk>/delete/', CropCultureDeleteView.as_view(), name='culture_delete'),
]