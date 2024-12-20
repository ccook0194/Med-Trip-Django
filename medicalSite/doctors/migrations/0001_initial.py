# Generated by Django 4.0 on 2022-05-07 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clinics', '0001_initial'),
        ('treatment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PopularTreatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=256)),
                ('headline', models.CharField(max_length=256)),
                ('img', models.ImageField(upload_to='popular_treatment/')),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='language', to='clinics.language')),
            ],
        ),
        migrations.CreateModel(
            name='CertificatesProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Certificates',
                'verbose_name_plural': 'Certificates',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('clinics.certificates',),
        ),
        migrations.CreateModel(
            name='ClinicCertficatesProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Clinic Certificate',
                'verbose_name_plural': 'Clinic Certificate',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('clinics.cliniccertficates',),
        ),
        migrations.CreateModel(
            name='CountryProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Country',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('clinics.country',),
        ),
        migrations.CreateModel(
            name='CurrencyProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currency',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('clinics.currency',),
        ),
        migrations.CreateModel(
            name='LanguageProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Language',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('clinics.language',),
        ),
        migrations.CreateModel(
            name='TopDestinations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alltopdestinations_country', to='clinics.country')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alltopdestinations_language', to='clinics.language')),
            ],
            options={
                'verbose_name_plural': 'Top Destinations',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='PopularTreatmentNames',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('popular_treatment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allpopularnames', to='doctors.populartreatment')),
                ('treatment_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allpopularnames', to='treatment.treatment')),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='doctor/')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=False)),
                ('clinic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alldoctors', to='clinics.clinic')),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='clinics.language')),
            ],
            options={
                'verbose_name_plural': 'Doctors',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='PopularTreatmentProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Popular Treatment',
                'verbose_name_plural': 'Popular Treatment',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('doctors.populartreatment',),
        ),
        migrations.CreateModel(
            name='TopDestinationsProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Popular Destinations',
                'verbose_name_plural': 'Popular Destinations',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('doctors.topdestinations',),
        ),
    ]
