# Generated by Django 3.2.12 on 2022-07-23 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0009_populartreatment_in_header'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='popularfootertreatmentproxy',
            options={'verbose_name': 'Header and Footer Destination', 'verbose_name_plural': 'Header and Footer Destinations'},
        ),
        migrations.AddField(
            model_name='popularfootertreatment',
            name='in_header',
            field=models.BooleanField(default=False),
        ),
    ]
