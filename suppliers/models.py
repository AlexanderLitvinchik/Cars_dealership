from django.db import models


# from  autosalons.models import BaseModel

class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Supplier_Discount(BaseModel):
    discount_percentage = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.discount_percentage}% discount"


class Sales_of_suppliers(BaseModel):
    supplier = models.ForeignKey('Supplier', related_name='sales_of_supplier', on_delete=models.CASCADE)
    autosalon = models.ForeignKey('autosalons.Autosalon', related_name='sales_of_suppliers_to_autosalon',
                                  on_delete=models.CASCADE)
    car = models.ForeignKey('autosalons.CarModel', related_name='sales_of_suppliers_car', blank=True, null=True,
                            on_delete=models.SET_NULL)
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale of {self.car} on {self.sale_date}"


class Supplier(BaseModel):
    name = models.CharField(max_length=100)
    year_founded = models.PositiveIntegerField()
    # поупатели постовщика это автосолоны
    # num_customers = models.IntegerField()
    discount_suppliers = models.ManyToManyField(Supplier_Discount, blank=True, related_name="discount_suppliers")

    def __str__(self):
        return self.name
