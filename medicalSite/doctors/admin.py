from django.contrib import admin
from django.dispatch import receiver
from .models import *
from import_export.admin import ImportExportModelAdmin
from clinics.resources import DoctorResource, CountryResource
from import_export.formats import base_formats
from django.db.models.signals import post_save
from django.db.models import Q



class DoctorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = DoctorResource
    list_display = ['get_clinic_id', 'name']
    search_fields = ['clinic__code', 'name']
    
    def get_clinic_id(self, obj):
        try:
            return obj.clinic.code
        except Exception:
            return None

class CountryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = CountryResource
    def get_import_formats(self):
        formats = (
                base_formats.CSV,
        )
        return [f for f in formats if f().can_export()]

#### POPULAR TREATMENTS ####

class PopularTreatmentInline(admin.TabularInline):
    model = PopularTreatmentNames
    extra = 0

class PopularTreatmentAdmin(admin.ModelAdmin):
    resource_class = PopularTreatmentProxy
    inlines = [PopularTreatmentInline]


@receiver(post_save, sender=PopularTreatmentProxy)
def update_popular_treatment_imgs(sender, instance, **kwargs):
    obj = instance
    for treatment in PopularTreatment.objects.all().filter(~Q(id=obj.id)).filter(code=obj.code):
        treatment.img = obj.img
        treatment.save()


### POPULAR (HEADER) DESTINATIONS ###
class PopularDestinationsInline(admin.TabularInline):
    model = PopularDestinationsCityNames
    extra = 0

    # remove 'slug' field from the admin
    def get_fields(self, request, obj=None):
        fields = super(PopularDestinationsInline, self).get_fields(request, obj)
        fields.remove('slug')
        return fields

class PopularDestinationsAdmin(admin.ModelAdmin):
    resource_class = PopularDestinationsProxy
    inlines = [PopularDestinationsInline]
    

#### POPULAR FOOTER TREATMENTS ####

class PopularFooterTreatmentInline(admin.TabularInline):
    model = PopularFooterTreatmentNames
    extra = 0

class PopularFooterTreatmentAdmin(admin.ModelAdmin):
    resource_class = PopularFooterTreatmentProxy
    inlines = [PopularFooterTreatmentInline]


@receiver(post_save, sender=PopularFooterTreatmentProxy)
def update_popular_treatment_imgs(sender, instance, **kwargs):
    obj = instance
    for treatment in PopularFooterTreatment.objects.all().filter(~Q(id=obj.id)).filter(code=obj.code):
        treatment.img = obj.img
        treatment.save()


# Clinic Package &
class ClinicPackageBulletPointsInline(admin.TabularInline):
    model = ClinicPackageBulletPoints
    extra = 0

class ClinicPackageAdmin(admin.ModelAdmin):
    model = ClinicPackages
    inlines = [ClinicPackageBulletPointsInline]


# Register your models here.
# admin.site.register(Doctor, DoctorAdmin)
admin.site.register(LanguageProxy)
admin.site.register(ClinicLanguagesProxy)
admin.site.register(CurrencyProxy)
admin.site.register(CountryProxy, CountryAdmin)
admin.site.register(CertificatesProxy)
admin.site.register(ClinicCertficatesProxy)
admin.site.register(PopularTreatmentProxy, PopularTreatmentAdmin)
admin.site.register(PopularDestinationsProxy, PopularDestinationsAdmin)
admin.site.register(PopularFooterTreatmentProxy, PopularFooterTreatmentAdmin)
admin.site.register(TopDestinationsProxy)
admin.site.register(ClinicPackageProxy, ClinicPackageAdmin)
admin.site.register(ClinicPackageBulletPointProxy)