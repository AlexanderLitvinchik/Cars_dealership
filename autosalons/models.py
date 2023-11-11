from django.db import models
from django.utils import timezone

from suppliers.models import Supplier, SupplierDiscount
from django_countries.fields import CountryField


# Create your models here.

class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# class CarCategory(BaseModel):
#     name = models.CharField(max_length=200)


class Specification(BaseModel):
    name_of_car = models.CharField(max_length=50)
    supplier = models.ManyToManyField(Supplier, related_name='supplier_specifications',
                                      through='autosalons.SupplierSpecificationRelationship')
    color = models.CharField(max_length=30)
    mileage = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name_of_car}"


# лучше перенести это в suppliers
class SupplierSpecificationRelationship(BaseModel):
    supplier_specification_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='supplier_specification_prices')
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE,
                                      related_name='supplier_specification_prices')
    discount_supplier = models.ForeignKey(SupplierDiscount, blank=True, null=True, on_delete=models.SET_NULL,
                                          related_name='discount_suppliers_of_specifications')

    def __str__(self):
        return f"{self.specification.name_of_car} in {self.supplier} with {self.supplier_specification_price}"


class ShowroomDiscount(BaseModel):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    discount_percentage = models.FloatField()

    def __str__(self):
        return f"{self.discount_percentage}% discount"


class Car(BaseModel):
    in_showroom = models.BooleanField(default=True)
    specification = models.ForeignKey('Specification', related_name='car_specification', on_delete=models.CASCADE)
    """
    serial_number (str): A unique serial number for the car to distinguish cars from the same specification
    """

    serial_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.specification} with serial number{self.serial_number}"


class Showroom(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    location = CountryField()
    car = models.ManyToManyField(Car, blank=True, related_name='showrooms',
                                 through='ShowroomCarRelationship')
    balance = models.DecimalField(max_digits=20, decimal_places=2)
    discount_showroom = models.ManyToManyField(ShowroomDiscount, blank=True,
                                               related_name='showrooms_discount')
    specifications = models.ManyToManyField(Specification, blank=True, related_name='showrooms_specification'
                                            )

    def __str__(self):
        return f"{self.name}"


class ShowroomCarRelationship(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='cars')
    showroom = models.ForeignKey(Showroom, on_delete=models.CASCADE)
    discount_showroom = models.ForeignKey(ShowroomDiscount, null=True, blank=True, on_delete=models.SET_NULL,
                                          related_name='cars_showroom_discount')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.car.specification.name_of_car} in {self.showroom}"


class ShowroomHistory(BaseModel):
    """"
    Change Relationship
    """
    car = models.OneToOneField(Car, null=True,
                               on_delete=models.SET_NULL, related_name='saled_cars')

    """
    added default value
    """
    sale_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    showroom = models.ForeignKey(Showroom, related_name='showroom_histories', on_delete=models.CASCADE)
    unique_customer = models.ForeignKey('customers.Customer', related_name='customer_histories',
                                        on_delete=models.CASCADE)

    def __str__(self):
        return f"Sale of {self.car} on {self.sale_date}"
