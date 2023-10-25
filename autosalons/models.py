from django.db import models

from suppliers.models import Supplier


# Create your models here.


class CarCategory(models.Model):
    name = models.CharField(max_length=200)


class CarModel(models.Model):
    name = models.CharField(max_length=255)
    # цена на машину в автосалоне и у паставщика разная как и количество
    # или оставить как есть и цену на автомобиль прнимать как цены у поставщика
    # а потом применять скидки от постовщика и автосолона + наценку у салона взять равным 0
    # и такую цену выводить полбзователю
    # (иначе она совсем разная для каждой машина)
    # если поставщик меняет цену для салона то салон поменяет ее для покупателя ?

    price = models.DecimalField(max_digits=10, decimal_places=2)
    # price_autosalon = models.DecimalField(max_digits=10, decimal_places=2)
    # price_suppliers = models.DecimalField(max_digits=10, decimal_places=2)

    # что-то запутано, по логики количество должно считаться через постащиков
    quantity = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    suppliers = models.ManyToManyField(Supplier,  related_name='cars_in_supplier')

    autosolons = models.ManyToManyField('Autosalon',  related_name='cars_in_supplier')
    category = models.ForeignKey(CarCategory, on_delete=models.CASCADE)


class Discount(models.Model):
    car = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='autosalon_discounts')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    discount_percentage = models.FloatField()

    def __str__(self):
        return f"{self.discount_percentage}% discount on {self.car}"


class Autosalon(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    # сказано, что автосолон уже хранит автомобили,
    # зачем тогда поле(характеристики автомобиле) по которому находим нужные авто, если они уже хранятся?

    # не соввсем понял, что такие  характеристики автомобилей
    # в моем понимание содержит категории продоваемых авто
    # пусть будет строка состоящая из категорий, найдем все категории
    # по данным категориям найдем нужные авто через model CarModel сранивая наши категории с категориями из CarModel,
    # это отличатеся немного от того что в файле

    categories = models.TextField()
    car_model = models.ManyToManyField(CarModel, related_name='autosalon_cars')
    # не понятно какие ограничения и balance это состояние автосолона ?
    balance = models.DecimalField(max_digits=20, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    sales_history = models.ManyToManyField('SaleHistory',related_name='autosalon_history', blank=True)
    # для избежания циклического иморта
    unique_customers = models.ManyToManyField('customers.Customer', related_name='autosalon_customers', blank=True)
    dicount = models.ForeignKey(Discount, on_delete=models.CASCADE)




class SaleHistory(models.Model):
    car = models.ManyToManyField(CarModel,related_name='sale_histories',)
    sale_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sale of {self.car} on {self.sale_date}"
