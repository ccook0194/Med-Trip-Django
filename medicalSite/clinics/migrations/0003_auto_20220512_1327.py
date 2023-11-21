# Generated by Django 3.2.12 on 2022-05-12 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClinicLanguages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('flag', models.ImageField(blank=True, upload_to='clinic_flag')),
            ],
        ),
        migrations.AddField(
            model_name='clinic',
            name='clinic_languages',
            field=models.ManyToManyField(blank=True, related_name='clinic_language', to='clinics.ClinicLanguages'),
        ),
    ]