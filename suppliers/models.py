from django.db import models


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SupplierDiscount(BaseModel):
    discount_percentage = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.discount_percentage}% discount"


class SupplierHistory(BaseModel):
    supplier = models.ForeignKey('Supplier', related_name='histories', on_delete=models.CASCADE)
    showroom = models.ForeignKey('autosalons.Showroom', related_name='histories_of_suppliers_to_showroom',
                                 on_delete=models.CASCADE)
    car = models.ForeignKey('autosalons.Car', related_name='histories', blank=True, null=True,
                            on_delete=models.SET_NULL)
    sale_date = models.DateTimeField(auto_now_add=True)
    """added field"""
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sale of {self.car} on {self.sale_date}"


class Supplier(BaseModel):
    name = models.CharField(max_length=100)
    year_founded = models.PositiveIntegerField()
    discount_suppliers = models.ManyToManyField(SupplierDiscount, blank=True, related_name="discount_suppliers")

    def __str__(self):
        return self.name
