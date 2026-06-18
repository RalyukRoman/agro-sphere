from django.contrib.auth.models import AbstractUser
from django.db import models
from geo_analytics.models import Company


class User(AbstractUser):
    """Модель для представлення користувача."""

    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Адміністратор'
        USER = 'user', 'Користувач'

    role = models.CharField(
        verbose_name="Роль в системі",
        max_length=10,
        choices=Roles.choices,
        default=Roles.USER
    )
    
    phone_number = models.CharField(
        verbose_name="Номер телефону",
        max_length=15, 
        blank=True, 
        null=True
    )

    email = models.EmailField(
        verbose_name="Електронна пошта", 
        max_length=100, 
        blank=True, 
        null=True
    )
    
    company = models.ForeignKey(
        verbose_name="Компанія",
        related_name="employees",
        to=Company,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"