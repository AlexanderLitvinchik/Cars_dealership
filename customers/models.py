from django.db import models
from django.contrib.auth.models import User
from autosalons.models import Car, BaseModel


# class Purchase(models.Model):
#     car_models = models.ManyToManyField(CarModel, related_name='purchases')
#     purchase_date = models.DateTimeField(auto_now_add=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)


class Customer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.user}"
