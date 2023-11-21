from unicodedata import category
from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from tinymce import models as tinymce_models
import pycountry

# Create your models here.
class Language(models.Model):
    name = models.CharField(max_length=50, unique= True, blank= False, null= False)
    code = models.CharField(max_length=50, unique= True, blank= False, null= False)
    #currency = models.ForeignKey('Currency', on_delete=models.CASCADE, related_name='lang_currency', blank= True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Languages'

    def __str__(self):
        return self.code

class Country(models.Model):
    name = models.CharField(max_length= 256, blank= False, null= False)
    img = models.ImageField(upload_to= 'country_img', blank= True)
    phone_code = models.CharField(max_length= 256, blank= False, null= False)
    iso_code = models.CharField(max_length= 10, blank= True, null= True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='country_language')
    created= models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'language')
        ordering=('-created',)
        verbose_name_plural='Country'

    def __str__(self):
        return str(self.name) + ' ' + str(self.language)


SIZE_CHOICES = (
    ("pending", "Pending"),
    ("publish", "Publish")
)
min = 0
max = 5


class ClinicLanguages(models.Model):
    name = models.CharField(max_length= 256, blank= False, null= False, unique=True)
    flag = models.ImageField(upload_to= 'clinic_flag', blank= True)

    def __str__(self) -> str:
        return self.name

class Clinic(models.Model):
    code = models.CharField(max_length= 10, blank= False, null= False)
    name = models.CharField(max_length= 256, blank= False, null= False)
    slug = models.SlugField(null= True, blank= True)
    # country = models.CharField(max_length= 256, blank= False, null= False)
    city = models.CharField(max_length= 256, blank= False, null= False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='allcliniccountry', blank= True, null=True)
    score = models.FloatField(blank= False, null= False, default= 2, validators=[MinValueValidator(min), MaxValueValidator(max)])
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='allclinicslanguage', blank= True)
    # about = models.TextField(blank= True, null= True)
    clinic_languages = models.ManyToManyField(ClinicLanguages, related_name='clinic_language', blank= True)

    about = tinymce_models.HTMLField(blank= True, null= True)
    created= models.DateTimeField(auto_now=True)
    status = models.CharField(max_length= 30, choices= SIZE_CHOICES, default= 'pending', blank= False, null= False)

    class Meta:
        unique_together = ('language', 'code')
        ordering=('-created',)
        verbose_name_plural='Clinics'

    def __str__(self):
        return str(self.name) + ' - ' + str(self.language)

    def get_url(self):
        return reverse('clinics:clinics_each_detail',args=[self.slug])
    
    @property
    def get_cover_image(self):
        cover_image = self.allimages.filter(is_cover_image=True).first()
        if cover_image:
            return cover_image
        en_clinic = Clinic.objects.filter(language__code='en-us', code=self.code).first()
        return en_clinic.allimages.first()

    def save(self, *args, **kwargs):
        slug = self.name
        self.slug = slugify(slug)
        super(Clinic, self).save(*args, **kwargs)

    @property
    def get_avg_rating(self):
        total_rating = self.score 
        count = 1
        for review in self.allreviews.filter(status_choice= 'accept', clinic=self):
            total_rating += (review.service_rating + review.cleanliness_rating + review.comfort_rating + review.quality_rating + review.communication_rating)/5
            count += 1
        return f"{total_rating/count:.1f}"

    @property
    def count_reviews(self):
        return self.allreviews.filter(status_choice='accept', clinic=self).count()

    @property
    def count_doctors(self):
        return self.alldoctors.filter(status=True, clinic=self, language=self.language).count()

    def get_doctors(self):
        return self.alldoctors.filter(status=True, clinic=self, language=self.language)

    def get_reviews(self):
        return self.allreviews.filter(status_choice='accept', clinic=self)

from django.db.models import Q

class ClinicImage(models.Model):
    clinic=models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='allimages')
    image=models.ImageField(upload_to='clinic/', blank= False)
    is_cover_image = models.BooleanField(default=False)
    created= models.DateTimeField(auto_now=True)
    # create a field that for selecting default image among all images
    
    class Meta:
        ordering=('-created',)
        verbose_name_plural='Clinic Images'
    
    def save(self, *args, **kwargs):
        if self.is_cover_image:
            qs = type(self).objects.filter(clinic=self.clinic, is_cover_image=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            qs.update(is_cover_image=False) 

                # for cl in Clinic.objects.all().filter(~Q(id=self.clinic.id)).filter(code=self.clinic.code):
                #     for clinic_image in cl.allimages.all():
                #         if clinic_image.image==self.image:
                #             clinic_image.is_cover_image = True
                #         else:
                #             clinic_image.is_cover_image = False
                #         clinic_image.save_base(raw=True)


        super(ClinicImage, self).save(*args, **kwargs)

    # def save_without_signals(self):
    #     """
    #     This allows for updating the model from code running inside post_save()
    #     signals without going into an infinite loop:
    #     """
    #     self._disable_signals = True
    #     self.save()
    #     self._disable_signals = False


    def __str__(self):
        return str(self.clinic) + "_image"

class ClinicBeforeAfterImage(models.Model):
    clinic=models.ForeignKey(Clinic,on_delete=models.CASCADE,related_name='allimagesafter')
    afterImage=models.ImageField(upload_to='clinic/after/',blank= False)
    beforeImage=models.ImageField(upload_to='clinic/before/',blank= False)
    created= models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-created',)
        verbose_name_plural='Clinic Before/After Images'

    def __str__(self):
        return str(self.clinic) + "_before_after_image"


VERIFY_REVIEW_CHOICES = (
    ("accept", "Accept"),
    ("delete", "Delete")
)
TITLE_CHOICES = (
    ("mr", "Mr"),
    ("mrs", "Mrs")
)
class ClinicReviews(models.Model):
    clinic=models.ForeignKey(Clinic,on_delete=models.CASCADE,related_name='allreviews')
    name = models.CharField(max_length= 256, blank= False, null= True)
    email = models.CharField(max_length= 256, blank= False, null= False)
    review = models.TextField(blank= True, null= True)
    service_rating = models.FloatField(blank= False, null= False, default= 4, validators= [MinValueValidator(min), MaxValueValidator(max)])
    cleanliness_rating = models.FloatField(blank= False, null= False, default= 4, validators= [MinValueValidator(min), MaxValueValidator(max)])
    comfort_rating = models.FloatField(blank= False, null= False, default= 4, validators= [MinValueValidator(min), MaxValueValidator(max)])
    quality_rating = models.FloatField(blank= False, null= False, default= 4, validators= [MinValueValidator(min), MaxValueValidator(max)])
    communication_rating = models.FloatField(blank= False, null= False, default= 4, validators= [MinValueValidator(min), MaxValueValidator(max)])
    created= models.DateTimeField(auto_now=True)
    status_choice = models.CharField(max_length= 30, choices= VERIFY_REVIEW_CHOICES, default= 'delete', blank= False, null= False)
    is_seen  = models.BooleanField(default= False)

    class Meta:
        ordering=('-created',)
        verbose_name_plural='Clinic Reviews C'

    @property
    def avg_review_rating(self):
        return f"{(self.service_rating + self.cleanliness_rating + self.comfort_rating + self.quality_rating + self.communication_rating)/5:.1f}"

    def __str__(self):
        return str(self.clinic) + "_" + str(self.name)


class ClinicTreatmentLeads(models.Model):
    clinic=models.ForeignKey(Clinic,on_delete=models.CASCADE,related_name='allrequests', blank= True, null= True)
    phone_code = models.CharField(max_length= 256, blank= True, null= True)
    phone_no = models.CharField(max_length= 256, blank= True, null= True)
    email = models.CharField(max_length= 256, blank= False, null= False)
    username = models.CharField(max_length= 256, blank= False, null= False)
    comment = models.TextField(blank= True, null= True)
    treatment_detail = models.CharField(max_length= 256, blank= True, null= True)
    created= models.DateTimeField(auto_now=True)
    is_seen = models.BooleanField(default= False)
    
    class Meta:
        ordering=('-created',)
        verbose_name_plural='Clinic Treatment Leads'

    def __str__(self):
        return str(self.username)


class Contact(models.Model):
    title = models.CharField(max_length= 10, choices= TITLE_CHOICES, default= 'mr', blank= False, null= False)
    name = models.CharField(max_length= 256, blank= False, null= False)
    address_1 = models.CharField(max_length= 556, blank= True, null= True)
    address_2 = models.CharField(max_length= 556, blank= True, null= True)
    city = models.CharField(max_length= 256, blank= True, null= True)
    state = models.CharField(max_length= 256, blank= True, null= True)
    country = models.CharField(max_length= 256, blank= True, null= True)
    postal_code = models.CharField(max_length= 256, blank= True, null= True)
    email = models.CharField(max_length= 256, blank= False, null= False)
    phone_code = models.CharField(max_length= 256, blank= True, null= True)
    phone_no = models.CharField(max_length= 256, blank= True, null= True)
    msg = models.TextField(blank= False, null= False)
    created= models.DateTimeField(auto_now=True)
    is_seen = models.BooleanField(default= False)

    class Meta:
        ordering=('-created',)
        verbose_name_plural='Contact Leads'

    def status(self):
        return self.is_seen

    def __str__(self):
        return str(self.title) + '_' + str(self.name)


CLINIC_ADD_CHOICES = (
    ("new_lead", "New Lead"),
    ("reviewd", "Reviewed")
)
class ClinicAdd(models.Model):
    clinic_name = models.CharField(max_length= 256, blank= False, null= False)
    address_1 = models.CharField(max_length= 256, blank= False, null= False)
    address_2 = models.CharField(max_length= 256, blank= True, null= True)
    city = models.CharField(max_length= 256, blank= False, null= False)
    state = models.CharField(max_length= 256, blank= False, null= False)
    country = models.CharField(max_length= 256, blank= False, null= False)
    postal_code = models.CharField(max_length= 256, blank= False, null= False)
    website = models.CharField(max_length= 256, default = "NA")
    email = models.CharField(max_length= 256, blank= False, null= False)
    phone_code = models.CharField(max_length= 256, blank= True, null= True)
    phone_no = models.CharField(max_length= 256, blank= False, null= False)
    year_established = models.CharField(max_length= 256, blank= False, null= False)
    message = models.CharField(max_length= 256, blank= False, null= False)
    created= models.DateTimeField(auto_now=True)
    status = models.CharField(max_length= 20, choices= CLINIC_ADD_CHOICES, default= 'new_lead', blank= False, null= False)
    is_seen = models.BooleanField(default= False)

    class Meta:
        ordering=('-created',)
        verbose_name_plural='New Clinic Leads'

    def __str__(self):
        return str(self.clinic_name) + '_' + str(self.year_established)


class Certificates(models.Model):
    name = models.CharField(max_length= 256, blank= False, null= False)
    created= models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-created',)
        verbose_name_plural='Certificates'

    def __str__(self):
        return str(self.name)


class ClinicCertficates(models.Model):
    clinic=models.ForeignKey(Clinic,on_delete=models.CASCADE,related_name='allcertificatesforclinic')
    certificates = models.ForeignKey(Certificates,on_delete=models.CASCADE,related_name='allcertificates')
    created= models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('clinic', 'certificates')
        ordering=('-created',)
        verbose_name_plural='Clinic Certificate'

    def __str__(self):
        return str(self.clinic) + "_" + str(self.certificates)


class Currency(models.Model):
    name = models.CharField(max_length= 256, blank= True, null= False)
    symbol = models.CharField(max_length= 256, blank= True, null= False)
    created= models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-created',)
        verbose_name_plural='Currency'

    def __str__(self):
        return str(self.name)

# dropdown for category in RankingClinics
category_choices = (
    ("dentals", "Dentals"),
    ("aesthetic", "Aesthetic"),
    ("hair-transplant", "Hair Transplant"),
)

country_choices = ()
for country in pycountry.countries:
    country_choices += ((country.alpha_2.lower(), country.name),)

class CurrencyPrices(models.Model):
    code = models.CharField(max_length= 256, blank= False, null= False)
    price = models.FloatField(blank= False, null= False)


class ClinicPackages(models.Model):
    clinic = models.ForeignKey(Clinic,on_delete=models.CASCADE,related_name='allpackagesforclinic')
    package_name = models.CharField(max_length= 256, blank= False, null= False)
    package_price = models.FloatField(blank= False, null= False)
    language = models.ForeignKey(Language,on_delete=models.CASCADE,related_name='allpackagesforlanguage', null=True)
    created= models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('clinic', 'package_name')
        ordering=('-created',)
        verbose_name_plural='Clinic Package'

    def __str__(self):
        return str(self.package_name)

class ClinicPackageBulletPoints(models.Model):
    package = models.ForeignKey(ClinicPackages,on_delete=models.CASCADE,related_name='allbulletpointsforpackage')
    bullet_point = models.CharField(max_length= 256, blank= False, null= False)
    created= models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('package', 'bullet_point')
        ordering=('-created',)
        verbose_name_plural='Clinic Package Bullet Point'

    def __str__(self):
        return str(self.package) + "_" + str(self.bullet_point)
    


class RankingClinics(models.Model):
    code = models.IntegerField(blank= True, null= True)
    name = models.CharField(max_length= 256, blank= True, null= False)
    slug = models.SlugField(max_length= 256, blank= True, null= False)
    category = models.CharField(max_length= 256, choices= category_choices, default= 'dentals', blank= False, null= False)
    city = models.CharField(max_length= 256, blank= False, null= False)
    country = models.CharField(max_length= 256, null= False, blank=False)
    country_flag = models.CharField(max_length= 256, null= True, blank=True, choices= country_choices)
    logo = models.ImageField(upload_to='clinic_logo/', blank= True, null= True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='clinic_ranking_language', blank= False, null = False)
    feedback_score = models.FloatField(blank= True, null= True)
    quality_score = models.FloatField(blank= True, null= True)
    final_score = models.FloatField(blank= True, null= True)
    rank = models.IntegerField(blank= True, null= True)
    old_rank = models.IntegerField(blank= True, null= True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('rank',)
        verbose_name_plural='Clinic Ranking'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        for clinic in RankingClinics.objects.all().filter(~Q(id=self.id)).filter(name=self.name):

            clinic.feedback_score = self.feedback_score
            clinic.quality_score = self.quality_score
            clinic.final_score = self.final_score
            clinic.logo = self.logo
            clinic.save_base()
        all_clinics = RankingClinics.objects.filter(language=self.language, category=self.category).all()

        if len(all_clinics) == 0 or (len(all_clinics) == 1 and all_clinics[0].id == self.id):
            self.rank = 1
            super(RankingClinics, self).save(*args, **kwargs)

        else:
            super(RankingClinics, self).save(*args, **kwargs)

            # sort using the final score and update each clinic's rank
            all_clinics = all_clinics.order_by('-final_score')
            for i, clinic in enumerate(all_clinics):
                if (clinic.rank != (i+1)) and (clinic.id == self.id):
                    clinic.old_rank = clinic.rank
                clinic.rank = i + 1
                super(RankingClinics, clinic).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        all_clinics = RankingClinics.objects.filter(language=self.language, category=self.category).all()
        # sort using the final score and update each clinic's rank
        all_clinics = all_clinics.order_by('-final_score')
        super(RankingClinics, self).delete(*args, **kwargs)
        for i, clinic in enumerate(all_clinics):
            clinic.rank = i + 1
            super(RankingClinics, clinic).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


# proxy models

from doctors.models import Doctor
from treatment.models import Treatment

class DoctorProxy(Doctor):
    class Meta:
        proxy = True
        verbose_name_plural='Doctor'
        verbose_name='Doctor'

class TreatmentProxy(Treatment):
    class Meta:
        proxy = True
        verbose_name_plural='Treatment'
        verbose_name='Treatment'

