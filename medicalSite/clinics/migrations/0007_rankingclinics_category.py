# Generated by Django 3.2.12 on 2022-06-10 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0006_alter_rankingclinics_country_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='rankingclinics',
            name='category',
            field=models.CharField(choices=[('dentals', 'Dentals'), ('aesthetic', 'Aesthetic'), ('hair transplant', 'Hair Transplant')], default='dentals', max_length=256),
        ),
    ]