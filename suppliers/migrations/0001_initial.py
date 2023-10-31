# Generated by Django 4.2.6 on 2023-10-31 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('autosalons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier_Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('discount_percentage', models.FloatField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('year_founded', models.PositiveIntegerField()),
                ('discount_suppliers', models.ManyToManyField(blank=True, related_name='discount_suppliers', to='suppliers.supplier_discount')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sales_of_suppliers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sale_date', models.DateTimeField(auto_now_add=True)),
                ('autosalon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_of_suppliers_to_autosalon', to='autosalons.autosalon')),
                ('car', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales_of_suppliers_car', to='autosalons.carmodel')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_of_supplier', to='suppliers.supplier')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
