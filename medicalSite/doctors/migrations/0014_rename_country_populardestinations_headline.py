# Generated by Django 4.0.6 on 2022-08-03 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0013_alter_topdestinationsproxy_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='populardestinations',
            old_name='country',
            new_name='headline',
        ),
    ]