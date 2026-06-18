from django.db import models
from django.contrib.gis.db import models

from django.core.validators import (
    MinValueValidator, 
    MaxValueValidator
)

import uuid


class Company(models.Model):
    """Модель для представлення компанії."""

    id = models.UUIDField(
        verbose_name="ID",
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
        
    name = models.CharField(
        verbose_name="Назва", 
        max_length=100
    )

    created_at = models.DateTimeField(
        verbose_name="Дата створення", 
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Field(models.Model):
    """Модель для представлення поля."""

    id = models.UUIDField(
        verbose_name="ID",
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )

    company = models.ForeignKey(
        verbose_name="Компанія",
        to=Company, 
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        verbose_name="Назва",
        max_length=100
    )

    geom = models.PolygonField(
        verbose_name="Координати меж поля"
    )

    area_hectares = models.FloatField(
        verbose_name="Площа (га)",
        blank=True, 
        null=True
    )

    class CropStatusChoice(models.TextChoices):
        PLANNED = "PLANNED", "Заплановано"
        SOWN = "SOWN", "Посіяно"
        GERMINATED = "GERMINATED", "Сходи (Проростання)"
        GROWING = "GROWING", "Вегетація (Росте)"
        FLOWERING = "FLOWERING", "Цвітіння"
        RIPENING = "RIPENING", "Дозрівання"
        READY = "READY", "Готово до збору"
        HARVESTED = "HARVESTED", "Зібрано"
        FAILED = "FAILED", "Втрачено (Загинуло)"

    crop_status = models.CharField(
        verbose_name="Статус",
        max_length=15,
        choices=CropStatusChoice.choices,
        default=CropStatusChoice.PLANNED,
    )
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.geom:
            geom_projected = self.geom.transform(3857, clone=True)
            self.area_hectares = round(geom_projected.area / 10000, 2)
        super().save(*args, **kwargs)


class FieldMetricHistory(models.Model):
    """Модель для представлення історії метрик для поля."""

    id = models.UUIDField(
        verbose_name="ID",
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )

    field = models.ForeignKey(
        verbose_name="Поле",
        to=Field, 
        on_delete=models.CASCADE
    )

    date = models.DateField(
        verbose_name="Дата"
    )

    weather_raw_data = models.JSONField(
        verbose_name="Сира відповідь"
    )

    ndvi_index = models.FloatField(
        verbose_name="Індекс вегетації",
        validators=[
            MinValueValidator(-1.0),
            MaxValueValidator(1.0)
        ]
    )

    soil_moisture = models.FloatField(
        verbose_name="Вологість",
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(100.0)
        ]
    )

    temperature = models.FloatField(
        verbose_name="Температура",
        validators=[
            MinValueValidator(-100.0),
            MaxValueValidator(100.0)
        ]
    )

    def __str__(self):
        return f"{self.field.name} - {self.date}"