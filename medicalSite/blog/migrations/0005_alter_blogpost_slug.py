# Generated by Django 3.2.12 on 2022-07-15 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_blogpost_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, max_length=250, null=True, unique=True),
        ),
    ]
