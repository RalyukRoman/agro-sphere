from scipy.optimize import linprog
from decimal import Decimal
from django.shortcuts import get_object_or_404
from geo_analytics.models import Field
from .models import CropCulture, CropPlan


class CropSolverService:
    """Сервіс для розрахунку оптимального плану посіву."""

    @staticmethod
    def calculate_optimal_plan(field_id: str, budget: float) -> dict:
        """Розрахувати оптимальний план посіву."""

        field = get_object_or_404(Field, id=field_id)
        area = float(field.area_hectares)

        cultures = list(CropCulture.objects.all())
        if not cultures:
            return {"error": "У базі даних немає доступних культур для розрахунку."}

        num_cultures = len(cultures)

        # Рахуємо приблизний прибуток з 1 гектара
        c = []
        costs_per_ha = []
        for culture in cultures:
            yield_per_ha = float(culture.average_yield_per_ha)
            price_per_ton = float(culture.base_market_price)
            
            revenue_per_ha = yield_per_ha * price_per_ton
            cost_ha = revenue_per_ha * 0.30
            profit_per_ha = revenue_per_ha - cost_ha
            
            costs_per_ha.append(cost_ha)
            c.append(-profit_per_ha)

        # Формуємо обмеження
        A_ub = [
            [1.0] * num_cultures,
            costs_per_ha
        ]
        
        b_ub = [
            area, 
            float(budget) if budget else float('inf')
        ]
        
        bounds = [(0, None) for _ in range(num_cultures)]

        # Запуск Solver
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

        if not res.success:
            return {"error": f"Оптимальний план не знайдено: {res.message}"}

        allocated_areas = res.x
        total_estimated_profit = -res.fun

        # Формуємо красиву відповідь з розподілом площі
        breakdown = []
        primary_crop = None
        max_allocated_area = 0.0

        for i, culture in enumerate(cultures):
            crop_area = round(allocated_areas[i], 2)
            if crop_area > 0:
                breakdown.append({
                    "crop_name": culture.name,
                    "allocated_hectares": crop_area,
                    "expected_yield_tons": round(crop_area * float(culture.average_yield_per_ha), 2)
                })

                if crop_area > max_allocated_area:
                    max_allocated_area = crop_area
                    primary_crop = culture

        if not primary_crop:
            return {"error": "Бюджет занадто малий для посіву будь-якої культури."}

        plan = CropPlan.objects.create(
            field=field,
            suggested_crop=primary_crop,
            confidence_score=0.95,
            expected_yield=Decimal(str(sum(b['expected_yield_tons'] for b in breakdown))),
            estimated_profit=Decimal(str(round(total_estimated_profit, 2)))
        )

        return {
            "status": "Success",
            "plan_id": plan.id,
            "total_area_ha": area,
            "total_estimated_profit_usd": round(total_estimated_profit, 2),
            "allocation_breakdown": breakdown,
            "created_at": plan.created_at
        }