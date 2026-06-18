from django.db import models
from django.contrib.gis.db import models
from django.core.validators import MinValueValidator
from warehousing.models import Warehouse, GrainBatch
import uuid


class Truck(models.Model):
    """Модель для представлення транспортного засобу."""

    id = models.UUIDField(
        verbose_name="Ідентифікатор",
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    
    license_plate = models.CharField(
        verbose_name="Номерний знак",
        max_length=10
    )

    driver_name = models.CharField(
        verbose_name="Ім'я водія",
        max_length=100
    )
    
    current_location = models.PointField(
        verbose_name="Поточна локація",
    )
    
    max_capacity_tons = models.FloatField(
        verbose_name="Вантажопідйомність",
        validators=[
            MinValueValidator(0.01)
        ]
    )

    class StatusChoices(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Доступний"
        ON_WAY = "ON_WAY", "В дорозі"
        LOADING = "LOADING", "Завантаження"
        DELIVERING = "DELIVERING", "Доставляється"
        UNLOADING = "UNLOADING", "Розвантаження"

    status = models.CharField(
        verbose_name="Статус",
        max_length=15,
        choices=StatusChoices.choices,
        default=StatusChoices.AVAILABLE,
    )
    
    def __str__(self):
        return self.license_plate


class TransportOrder(models.Model):
    """Модель для представлення заявки на транспортування."""

    id = models.UUIDField(
        verbose_name="ID",
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )

    source_warehouse = models.ForeignKey(
        verbose_name="Місце збору",
        to=Warehouse, 
        on_delete=models.CASCADE
    )

    destination = models.PointField(
        verbose_name="Місце доставки"
    )

    batch = models.OneToOneField(
        verbose_name="Партія",
        to=GrainBatch, 
        on_delete=models.CASCADE
    )

    truck = models.ForeignKey(
        verbose_name="Транспортний засіб",
        to=Truck, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )

    class StatusChoices(models.TextChoices):
        CREATED = "CREATED", "Створено"
        ASSIGNED = "ASSIGNED", "Назначено"
        IN_PROGRESS = "IN_PROGRESS", "В процесі"
        COMPLETED = "COMPLETED", "Завершено"
        CANCELLED = "CANCELLED", "Відмінено"

    status = models.CharField(
        verbose_name="Статус",
        max_length=15,
        choices=StatusChoices.choices,
        default=StatusChoices.CREATED,
    )

    distance_km = models.FloatField(
        verbose_name="Відстань (км)",
        validators=[
            MinValueValidator(0.0)
        ]
    )

    created_at = models.DateTimeField(
        verbose_name="Час створення",
        auto_now_add=True
    )

    completed_at = models.DateTimeField(
        verbose_name="Час завершення",
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"Замовлення {self.id}"