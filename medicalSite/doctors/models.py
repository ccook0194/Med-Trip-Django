from django.db import models
from clinics.models import Clinic, Language
from treatment.models import Treatment

from django.utils.text import slugify
from urllib.parse import unquote


# Create your models here.
class Doctor(models.Model):
    clinic = models.ForeignKey(Clinic,on_delete=models.CASCADE,related_name='alldoctors', null=True)
    image=models.ImageField(upload_to='doctor/',blank= True)
    name = models.CharField(max_length= 250, blank= False, null= False)
    description = models.TextField(blank= True, null= True)
    language = models.ForeignKey(Language,on_delete=models.CASCADE, null=True)
    created= models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    class Meta:
        ordering=('-created',)
        verbose_name_plural='Doctors'

    def __str__(self):
        return str(self.name) 

# proxy models

from clinics.models import Language, Currency, Country, Certificates, ClinicReviews, ClinicCertficates, ClinicLanguages, ClinicPackages, ClinicPackageBulletPoints
class ClinicPackageProxy(ClinicPackages):
    class Meta:
        proxy=True
        verbose_name_plural='Clinic Packages'
        verbose_name='Clinic Package'
        ordering=('-created',)

class ClinicPackageBulletPointProxy(ClinicPackageBulletPoints):
    class Meta:
        proxy=True
        verbose_name_plural='Clinic Package Bullet Points'
        verbose_name='Clinic Package Bullet Point'
        ordering=('-created',)
        
class LanguageProxy(Language):
    class Meta:
        proxy = True
        verbose_name_plural='Language'
        verbose_name='Language'

class CurrencyProxy(Currency):
    class Meta:
        proxy = True
        verbose_name_plural='Currency'
        verbose_name='Currency'


class CountryProxy(Country):
    class Meta:
        proxy = True
        verbose_name_plural='Country'
        verbose_name='Country'

class CertificatesProxy(Certificates):
    class Meta:
        proxy = True
        verbose_name_plural='Certificates'
        verbose_name='Certificates'


class ClinicCertficatesProxy(ClinicCertficates):
    class Meta:
        proxy = True
        verbose_name_plural= 'Clinic Certificate'
        verbose_name = 'Clinic Certificate'

class ClinicLanguagesProxy(ClinicLanguages):
    class Meta:
        proxy = True
        verbose_name_plural= 'Clinic Languages'


class TopDestinations(models.Model):
    country = models.ForeignKey(Country,on_delete=models.CASCADE,related_name='alltopdestinations_country')
    language = models.ForeignKey(Language,on_delete=models.CASCADE,related_name='alltopdestinations_language')
    created= models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-created',)
        verbose_name_plural='Top Destinations'

    def __str__(self):
        return str(self.country.name)

class TopDestinationsProxy(TopDestinations):
    class Meta:
        proxy = True
        verbose_name_plural='Popular Main Page Destinations'
        verbose_name='Popular Main Page Destination'


### POPULAR TREATMENTS #### 

class PopularTreatment(models.Model):
    code = models.CharField(max_length= 256, blank= False, null= False)
    headline = models.CharField(max_length= 256, blank= False, null= False)
    img = models.ImageField(upload_to='popular_treatment/', blank= True, null= True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='language', blank= True, null=True)
    in_header = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.headline



class PopularTreatmentNames(models.Model):
    popular_treatment = models.ForeignKey(PopularTreatment,on_delete=models.CASCADE,related_name='allpopularnames')
    treatment_name = models.ForeignKey(Treatment,on_delete=models.CASCADE,related_name='allpopularnames')

    class Meta:
        verbose_name_plural='Treatments'
        verbose_name='Treatment'



class PopularTreatmentProxy(PopularTreatment):
    class Meta:
        proxy = True
        verbose_name_plural='Header/Main Page Treatments'
        verbose_name='Header/Main Page Treatment'



### POPULAR DESTINATIONS ###

class PopularDestinations(models.Model):
    country = models.ForeignKey(Country,on_delete=models.CASCADE,related_name='destinations_country', null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='header_destinations_language', blank= True, null=True)

    def __str__(self) -> str:
        return self.country.name



class PopularDestinationsCityNames(models.Model):
    popular_destinations = models.ForeignKey(PopularDestinations,on_delete=models.CASCADE,related_name='allpopulardestinations')
    city = models.CharField(max_length= 256, blank= False, null= False)
    slug = models.CharField(max_length= 256, blank= True, null= True)

    class Meta:
        verbose_name_plural='Cities'
        verbose_name='City'

    def save(self, *args, **kwargs):
        self.slug = slugify(unquote(self.city), allow_unicode=True)
        super(PopularDestinationsCityNames, self).save(*args, **kwargs)



class PopularDestinationsProxy(PopularDestinations):
    class Meta:
        proxy = True
        verbose_name_plural='Header Destinations'
        verbose_name='Header Destinations'


### POPULAR FOOTER TREATMENTS #### 

class PopularFooterTreatment(models.Model):
    code = models.CharField(max_length= 256, blank= False, null= False)
    headline = models.CharField(max_length= 256, blank= False, null= False)
    country = models.ForeignKey(Country,on_delete=models.CASCADE,related_name='allpopularfootertreatment_country', blank= True, null=True)
    country_flag = models.ImageField(upload_to='popular_footer_treatment/', blank= True, null= True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='popular_footer_language', blank= True, null=True)
    in_header = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.headline



class PopularFooterTreatmentNames(models.Model):
    popular_footer_treatment = models.ForeignKey(PopularFooterTreatment,on_delete=models.CASCADE,related_name='allpopularfooternames')
    treatment_name = models.ForeignKey(Treatment,on_delete=models.CASCADE,related_name='allpopularfooternames')

    class Meta:
        verbose_name_plural='Treatments'
        verbose_name='Treatment'


class PopularFooterTreatmentProxy(PopularFooterTreatment):
    class Meta:
        proxy = True
        verbose_name_plural='Footer Destinations'
        verbose_name='Footer Destination'