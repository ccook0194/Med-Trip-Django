# Generated by Django 4.0 on 2022-05-07 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('phone_code', models.CharField(blank=True, max_length=256, null=True)),
                ('phone_no', models.CharField(blank=True, max_length=256, null=True)),
                ('email', models.CharField(max_length=256)),
                ('comment', models.TextField()),
                ('created', models.DateTimeField(auto_now=True)),
                ('is_seen', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Blog Contact',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('about', models.CharField(max_length=250, null=True)),
                ('meta_description', models.CharField(max_length=250, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, unique=True)),
                ('cover_img', models.ImageField(upload_to='blog/')),
                ('author', models.CharField(max_length=250, null=True)),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
