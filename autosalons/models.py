from django.db import models
from django.utils import timezone

from suppliers.models import Supplier, Supplier_Discount
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
    # имеется в виду полное название Audi A7 ,  не понятно стоит ли учитывать пробег и остальные парметры  
    name_of_car = models.CharField(max_length=50)
    supplier = models.ManyToManyField(Supplier, related_name='specification_suppliers',
                                      through='Supplier_Specification_price')

    def __str__(self):
        return f"{self.name_of_car}"


# лучше перенести это в suppliers
class Supplier_Specification_price(BaseModel):
    supplier_specification_price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='supplier_specification_prices')
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE,
                                      related_name='supplier_specification_prices')
    discount_supplier = models.ForeignKey(Supplier_Discount, on_delete=models.SET_NULL, null=True,
                                          related_name='discount_supplier')

    def __str__(self):
        return f"{self.specification.name_of_car} in {self.supplier} with {self.supplier_specification_price} and {self.discount_supplier}% discount"


class Discount_autosalon(BaseModel):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    discount_percentage = models.FloatField()

    def __str__(self):
        return f"{self.discount_percentage}% discount"


# Нужна ли связь с Specification?, или  просто здесь добавить поле имя авто
# полное название (Audi A7) получать из spetification, немного не логично

class CarModel(BaseModel):
    # number_of_car = models.CharField(max_length=30, unique=True)
    in_autosalon = models.BooleanField(default=True)
    # category = models.ForeignKey(CarCategory, on_delete=models.CASCADE)
    specification = models.OneToOneField('Specification', related_name='car_specification', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.specification}"


class Autosalon(BaseModel):
    name = models.CharField(max_length=255)
    location = CountryField()
    car = models.ManyToManyField(CarModel, blank=True, related_name='autosalons',
                                 through='CarInAutosalon')
    # не понятно какие ограничения и balance это состояние автосолона ?
    balance = models.DecimalField(max_digits=20, decimal_places=2)
    discount_autosalon = models.ManyToManyField(Discount_autosalon, blank=True,
                                                related_name='autosalons_discount')
    specifications = models.ManyToManyField(Specification, blank=True, related_name='autosalons_specification'
                                            )

    def __str__(self):
        return f"{self.name}"


class CarInAutosalon(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    autosalon = models.ForeignKey(Autosalon, on_delete=models.CASCADE)
    discount_autosalon = models.ForeignKey(Discount_autosalon, null=True, blank=True, on_delete=models.SET_NULL,
                                           related_name='cars_autosalon_discount')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.car_model.specification.name_of_car} in {self.autosalon}"


class Autosalon_Sales(BaseModel):
    # нужно ли мнгоие ко многим
    car = models.ForeignKey(CarModel, null=True,
                            on_delete=models.SET_NULL, related_name='saled_cars')
    sale_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    autosalon = models.ForeignKey(Autosalon, related_name='autosalon_sales', on_delete=models.CASCADE)
    # продажи автоссалона это и есть покупки покупателей так зачем же две таблицы создавать
    unique_customer = models.ForeignKey('customers.Customer', related_name='customer_sales',
                                        on_delete=models.CASCADE)

    def __str__(self):
        return f"Sale of {self.car} on {self.sale_date}"
