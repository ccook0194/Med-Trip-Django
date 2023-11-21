from django.utils.text import slugify
from django.db import models
from clinics.models import Clinic, Currency, Language, ClinicReviews

class ClinicReviewsProxy(ClinicReviews):
    class Meta:
        proxy = True
        verbose_name_plural='Clinic Reviews'
        verbose_name='Clinic Reviews'

# Create your models here.
class Treatment(models.Model):
    clinic = models.ForeignKey(Clinic,on_delete=models.CASCADE,related_name='alltreatments', null=True)
    slug = models.SlugField(null= True, blank= True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='treatmentlanguage', blank= True, null=True)
    searched_treatment = models.CharField(max_length= 256, blank= False, null= False)
    price = models.FloatField(blank= False, null= False)
    price_type = models.CharField(max_length= 256, blank= True, null= True)
    package_info_1 = models.CharField(max_length= 556, blank= True, null= True)
    package_info_2 = models.CharField(max_length= 556, blank= True, null= True)
    package_info_3 = models.CharField(max_length= 556, blank= True, null= True)
    package_info_4 = models.CharField(max_length= 556, blank= True, null= True)
    currency=models.ForeignKey(Currency,on_delete=models.CASCADE,related_name='currency',blank=True,null=True)
    created= models.DateTimeField(auto_now=True)
    status = models.BooleanField(default= True)

    class Meta:
        # unique_together = ('clinic', 'searched_treatment', 'language')
        ordering=('-created',)
        verbose_name_plural='Treatments'

    def __str__(self):
        return self.searched_treatment

    def save(self, *args, **kwargs):
        slug = self.searched_treatment
        self.slug = slugify(slug, allow_unicode=True)
        super(Treatment, self).save(*args, **kwargs)




# proxy models



from clinics.models import ClinicTreatmentLeads, Contact, ClinicAdd
from blog.models import BlogContact

class ClinicTreatmentLeadsProxy(ClinicTreatmentLeads):
    class Meta:
        proxy = True
        verbose_name_plural='Clinic Treatment Leads'
        verbose_name='Clinic Treatment Leads'
    
class ContactProxy(Contact):
    class Meta:
        proxy = True
        verbose_name_plural='Contacts'
        verbose_name='Contacts'

class ClinicAddProxy(ClinicAdd):
    class Meta:
        proxy = True
        verbose_name_plural='Clinic Add'
        verbose_name='Clinic Add'

class BlogContactProxy(BlogContact):
    class Meta:
        proxy = True
        verbose_name_plural='Blog Contact'
        verbose_name='Blog Contact'

