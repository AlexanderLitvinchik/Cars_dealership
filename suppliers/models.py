from django.db import models


class Discount(models.Model):
    car = models.ForeignKey('autosalons.CarModel', on_delete=models.CASCADE,related_name='supplier_discounts')
    discount_percentage = models.FloatField()

    def __str__(self):
        return f"{self.discount_percentage}% discount on {self.car}"


class History_of_Sales(models.Model):
    car = models.ManyToManyField('autosalons.CarModel', related_name='History_of_Sales')
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale of {self.car} on {self.sale_date}"


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    year_founded = models.PositiveIntegerField()
    num_customers = models.IntegerField()
    cars = models.ManyToManyField('autosalons.CarModel',  related_name='suppliers_of_car')
    # сказано хранить соответсвующие цены, но они же доступны модель cars
    # и вообще  у меня так получилось цена в cars лежит и одинакова и для салона и для поставщика
    # должно быть так есть машина поставщик продает машину в салон , а салон продает покупателю c наценкой
    # в модели car что ли сделать два поля price для салона и для поставщика

    discounts = models.ManyToManyField(Discount, related_name="suppliers")

    sales_history = models.ManyToManyField(History_of_Sales, related_name="suppliers_history")

    def __str__(self):
        return self.name
