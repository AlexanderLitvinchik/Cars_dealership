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
    brand = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    autosalon = models.ManyToManyField('Autosalon', related_name='specification_autosalons')
    supplier = models.ManyToManyField(Supplier, related_name='specification_suppliers')
    discount_supplier = models.OneToOneField(Supplier_Discount, on_delete=models.SET_NULL, null=True,
                                             related_name='specification_discount_supplier')


class Supplier_Specification_price(models.Model):
    supplier_specification_price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='supplier_specification_prices')
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE,
                                      related_name='supplier_specification_prices')


class Discount_autosalon(BaseModel):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    discount_percentage = models.FloatField()
    autosalons = models.ManyToManyField('Autosalon', related_name='discount_autosalons')

    def __str__(self):
        return f"{self.discount_percentage}% discount on {self.car}"


class CarModel(BaseModel):
    # цена на машину в автосалоне и у паставщика разная
    # если поставщик меняет цену для салона то салон поменяет ее для покупателя ?

    price_autosalon = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    autosolons = models.ManyToManyField('Autosalon',null=True,
                                        related_name='cars_in_autosalon')
    # category = models.ForeignKey(CarCategory, on_delete=models.CASCADE)
    specification = models.OneToOneField('Specification', related_name='car_specification', on_delete=models.CASCADE)

    discount_autosalon = models.OneToOneField(Discount_autosalon, on_delete=models.SET_NULL, null=True,
                                              related_name='cars_autosalon_discount')


class Autosalon(BaseModel):
    name = models.CharField(max_length=255)
    location = CountryField()
    car = models.ManyToManyField(CarModel, related_name='autosalons')
    # не понятно какие ограничения и balance это состояние автосолона ?

    balance = models.DecimalField(max_digits=20, decimal_places=2)
    dicount_autosalon = models.ManyToManyField(Discount_autosalon,
                                               related_name='autosalons_diccount')
    specifications = models.ManyToManyField(Specification, related_name='autosalons_specification'
                                            )


class Autosalon_Sales(BaseModel):
    # нужно ли мнгоие ко многим
    car = models.OneToOneField(CarModel,on_delete=models.CASCADE, related_name='saled_cars')
    sale_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    autosalon = models.ForeignKey(Autosalon, related_name='autosalon_sales', on_delete=models.CASCADE)
    # продажи автоссалона это и есть покупки покупателей так зачем же две таблицы создавать
    unique_customers = models.ForeignKey('customers.Customer', related_name='customers_purchases',
                                         on_delete=models.CASCADE)

    def __str__(self):
        return f"Sale of {self.car} on {self.sale_date}"
