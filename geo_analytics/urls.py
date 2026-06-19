from django.urls import path

from .views import (
    MapDashboardView, 
    FieldCreateView, 
    FieldUpdateView, 
    FieldDeleteView,
)


urlpatterns = [
    path('dashboard/', MapDashboardView.as_view(), name='map_dashboard'),
    path('fields/add/', FieldCreateView.as_view(), name='field_add'),
    path('fields/<uuid:pk>/edit/', FieldUpdateView.as_view(), name='field_edit'),
    path('fields/<uuid:pk>/delete/', FieldDeleteView.as_view(), name='field_delete')
]