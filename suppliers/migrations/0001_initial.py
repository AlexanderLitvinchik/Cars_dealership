# Generated by Django 4.2.6 on 2023-11-27 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('autosalons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('year_founded', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SupplierDiscount',
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
            name='SupplierHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sale_date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('car', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='histories', to='autosalons.car')),
                ('showroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='histories_of_suppliers_to_showroom', to='autosalons.showroom')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='histories', to='suppliers.supplier')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='supplier',
            name='discount_suppliers',
            field=models.ManyToManyField(blank=True, related_name='discount_suppliers', to='suppliers.supplierdiscount'),
        ),
    ]
