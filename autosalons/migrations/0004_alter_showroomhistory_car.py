# Generated by Django 4.2.6 on 2023-12-02 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autosalons', '0003_alter_showroomcarrelationship_showroom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='showroomhistory',
            name='car',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='saled_cars', to='autosalons.car'),
        ),
    ]
