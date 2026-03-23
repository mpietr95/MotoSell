from django.db import models
from django.contrib.auth.models import User


class Vehicle(models.Model):

    CATEGORY_MOTORCYCLE = 'motocykl'
    CATEGORY_CAR = 'osobowy'
    CATEGORY_TRUCK = 'ciezarowy'

    CATEGORY_CHOICES = {
        CATEGORY_MOTORCYCLE: 'Motocykl',
        CATEGORY_CAR: 'Osobowy',
        CATEGORY_TRUCK: 'Ciężarowy',
    }

    FUEL_PETROL = 'benzyna'
    FUEL_DIESEL = 'diesel'
    FUEL_LPG = 'lpg'

    FUEL_CHOICES = {
        FUEL_PETROL: 'Benzyna',
        FUEL_DIESEL: 'Diesel',
        FUEL_LPG: 'LPG',
    }

    title = models.CharField(max_length=255, verbose_name='Tytuł')
    description = models.TextField(verbose_name='Opis')
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name='Kategoria',
    )
    brand = models.CharField(max_length=100, verbose_name='Marka')
    model = models.CharField(max_length=100, verbose_name='Model')
    year = models.PositiveIntegerField(verbose_name='Rok produkcji')
    mileage = models.PositiveIntegerField(verbose_name='Przebieg (km)')
    engine_capacity = models.PositiveIntegerField(verbose_name='Pojemność skokowa (cm³)')
    power = models.PositiveIntegerField(verbose_name='Moc (KM)')
    fuel_type = models.CharField(
        max_length=10,
        choices=FUEL_CHOICES,
        verbose_name='Rodzaj paliwa',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vehicles',
        verbose_name='Użytkownik',
    )
    image = models.ImageField(
        upload_to='vehicles/%Y/%m/%d',
        blank=True,
        null=True,
        verbose_name='Zdjęcie',
    )
    created_at = models.DateField(auto_now_add=True, verbose_name='Data dodania')
    published_at = models.DateField(null=True, blank=True, verbose_name='Data publikacji')
    is_deleted = models.BooleanField(default=False, verbose_name='Usunięty')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Pojazd'
        verbose_name_plural = 'Pojazdy'

    def __str__(self):
        return f'{self.brand} {self.model} ({self.year}) — {self.title}'


# Opcjonalna galeria zdjęć
class VehicleImage(models.Model):
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Pojazd',
    )
    image = models.ImageField(
        upload_to='vehicles/gallery/%Y/%m/%d',
        verbose_name='Zdjęcie',
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Data przesłania')

    class Meta:
        verbose_name = 'Zdjęcie pojazdu'
        verbose_name_plural = 'Zdjęcia pojazdu'

    def __str__(self):
        return f'Zdjęcie #{self.pk} — {self.vehicle}'
