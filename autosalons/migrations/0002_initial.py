# Generated by Django 4.2.6 on 2023-10-26 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('suppliers', '0001_initial'),
        ('customers', '0001_initial'),
        ('autosalons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier_specification_price',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplier_specification_prices', to='suppliers.supplier'),
        ),
        migrations.AddField(
            model_name='specification',
            name='autosalon',
            field=models.ManyToManyField(related_name='specification_autosalons', to='autosalons.autosalon'),
        ),
        migrations.AddField(
            model_name='specification',
            name='discount_supplier',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='specification_discount_supplier', to='suppliers.supplier_discount'),
        ),
        migrations.AddField(
            model_name='specification',
            name='supplier',
            field=models.ManyToManyField(related_name='specification_suppliers', to='suppliers.supplier'),
        ),
        migrations.AddField(
            model_name='discount_autosalon',
            name='autosalons',
            field=models.ManyToManyField(related_name='discount_autosalons', to='autosalons.autosalon'),
        ),
        migrations.AddField(
            model_name='carmodel',
            name='autosolons',
            field=models.ManyToManyField(related_name='cars_in_autosalon', to='autosalons.autosalon'),
        ),
        migrations.AddField(
            model_name='carmodel',
            name='discount_autosalon',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cars_autosalon_discount', to='autosalons.discount_autosalon'),
        ),
        migrations.AddField(
            model_name='carmodel',
            name='specification',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='car_specification', to='autosalons.specification'),
        ),
        migrations.AddField(
            model_name='autosalon_sales',
            name='autosalon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='autosalon_sales', to='autosalons.autosalon'),
        ),
        migrations.AddField(
            model_name='autosalon_sales',
            name='car',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='saled_cars', to='autosalons.carmodel'),
        ),
        migrations.AddField(
            model_name='autosalon_sales',
            name='unique_customers',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customers_purchases', to='customers.customer'),
        ),
        migrations.AddField(
            model_name='autosalon',
            name='car',
            field=models.ManyToManyField(related_name='autosalons', to='autosalons.carmodel'),
        ),
        migrations.AddField(
            model_name='autosalon',
            name='dicount_autosalon',
            field=models.ManyToManyField(related_name='autosalons_diccount', to='autosalons.discount_autosalon'),
        ),
        migrations.AddField(
            model_name='autosalon',
            name='specifications',
            field=models.ManyToManyField(related_name='autosalons_specification', to='autosalons.specification'),
        ),
    ]
