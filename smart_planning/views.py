from django.urls import reverse_lazy
from django.http import Http404
from django.shortcuts import get_object_or_404

from smart_planning.forms import SmartPlanningCalculateForm
from smart_planning.models import CropPlan

import json

from django.views.generic import (
    TemplateView, 
    FormView
)

from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
)


class PlanCalculatorView(LoginRequiredMixin, FormView):
    """Форма для розрахунку оптимального плану посіву."""
    
    form_class = SmartPlanningCalculateForm
    template_name = 'smart_planning/calculator.html'
    success_url = reverse_lazy('plan_results')


class PlanResultsView(LoginRequiredMixin, TemplateView):
    """Сторінка результатів розрахунку з динамічними даними від CropSolverService."""
    template_name = 'smart_planning/results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        plan_id = self.request.GET.get('plan_id')
        if not plan_id:
            raise Http404("Параметр plan_id відсутній. Будь ласка, виконайте розрахунок спочатку.")

        crop_plan = get_object_or_404(
            CropPlan.objects.select_related('field', 'suggested_crop'), 
            id=plan_id, 
            field__company=self.request.user.company
        )
        
        chart_labels = []
        chart_data = []
        table_rows = []

        chart_labels.append(crop_plan.suggested_crop.name)
        chart_data.append(float(crop_plan.field.area_hectares))
        
        table_rows.append({
            'field': crop_plan.field.name,
            'crop': crop_plan.suggested_crop.name,
            'area': float(crop_plan.field.area_hectares),
            'yield': float(crop_plan.expected_yield),
            'costs': float(crop_plan.estimated_profit) * 0.30
        })

        efficiency_rate = int(crop_plan.confidence_score * 100) if crop_plan.confidence_score else 100

        calculated_data = {
            'total_profit': float(crop_plan.estimated_profit),
            'efficiency_rate': efficiency_rate,
            'recommended_crop': crop_plan.suggested_crop.name,
            'table_rows': table_rows
        }

        context['plan'] = calculated_data
        
        context['chart_labels_json'] = json.dumps(chart_labels)
        context['chart_data_json'] = json.dumps(chart_data)
        
        return context