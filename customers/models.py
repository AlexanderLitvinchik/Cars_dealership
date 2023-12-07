import jwt
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from autosalons.models import Car, BaseModel, ShowroomCarRelationship, Showroom, Car, ShowroomHistory
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Offer(models.Model):
    """
      Represents an offer made by a customer to buy a car.
    """
    # указал  все кроме колиметорожа и цвета, если его тоже указывать, то можно было просто сразу car_specification указать ,  а задние как я это понял этого не рпедусматривает
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='offers')
    max_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    name_of_car = models.CharField(max_length=50)
    year = models.PositiveIntegerField()

    def __str__(self):
        return f"Offer #{self.pk} - {self.customer} wants to buy {self.name_of_car} for {self.max_price}"


class Customer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    """Added new field"""
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"

    def generate_token(self, expiration_time):
        payload = {
            'user_id': self.user.id,
            'exp': expiration_time,
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
