from django.urls import path

from .views import (
    PlanCalculatorView, 
    PlanResultsView,
)


urlpatterns = [
    path('planning/calculate/', PlanCalculatorView.as_view(), name='plan_calculate'),
    path('planning/results/', PlanResultsView.as_view(), name='plan_results'),
]