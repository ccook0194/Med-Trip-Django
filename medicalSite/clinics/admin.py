
from dataclasses import fields
from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from .resources import ClinicResource, ClinicRankingResource
from doctors.models import Doctor
from import_export.formats import base_formats
from doctors.admin import DoctorAdmin
from treatment.admin import TreatmentAdmin
from django.db.models import Q

from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver

from django import forms

class MyModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MyModelForm, self).__init__(*args, **kwargs)
        self.fields['is_cover_image'].widget.attrs['class'] = 'default-img'
    class Meta:
        model = ClinicImage
        exclude = ()

    class Media:
        js = ('js/formset_handlers.js',)


admin.site.site_title = 'MyTripMed Admin'
admin.site.site_header = 'MyTripMed Admin'

class ClinicImageInline(admin.TabularInline):
    model = ClinicImage
    extra = 0
    form = MyModelForm
    ordering = ("pk",)
    


class ClinicCertificateInline(admin.TabularInline):
    model = ClinicCertficates
    extra = 0


class ClinicBeforeAfterImageInline(admin.TabularInline):
    model = ClinicBeforeAfterImage
    extra = 0


class ClinicDoctorsInline(admin.TabularInline):
    model = Doctor
    extra = 0

@admin.action(description='Change status to Publish')
def change_to_publish(modeladmin, request, queryset):
    queryset.update(status='publish')


@admin.action(description='Change status to Pending')
def change_to_pending(modeladmin, request, queryset):
    queryset.update(status='pending')

class ClinicAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ClinicResource
    inlines = [ClinicImageInline, ClinicCertificateInline,
               ClinicBeforeAfterImageInline, ClinicDoctorsInline]
    search_fields = ['name', 'code']
    list_display = ['code', 'name', 'status']
    list_filter = ('language',)
    actions = [change_to_publish,change_to_pending]

    def get_import_formats(self):
        formats = (
            base_formats.CSV,
        )
        return [f for f in formats if f().can_export()]

class RankingClinicsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ClinicRankingResource
    readonly_fields=('rank', 'old_rank')
    search_fields = ('name', 'code')
    list_display = ('code', 'name', 'rank', 'final_score')

    def get_import_formats(self):
        formats = (
            base_formats.CSV,
        )
        return [f for f in formats if f().can_export()]
    


@receiver(post_save, sender=ClinicImage)
@receiver(post_delete, sender=ClinicImage)
def clinic_image_handler(sender, instance, **kwargs):
    obj = instance
    for clinic in Clinic.objects.all().filter(~Q(id=obj.clinic.id)).filter(code=obj.clinic.code):
        post_delete.disconnect(clinic_image_handler, sender=ClinicImage)
        ClinicImage.objects.all().filter(clinic=clinic).delete()
        post_delete.connect(clinic_image_handler, sender=ClinicImage)
        for image in obj.clinic.allimages.filter().all().reverse():
            post_save.disconnect(clinic_image_handler, sender=sender)
            if (image.is_cover_image):
                is_cover_image = True
            else:
                is_cover_image = False
            ClinicImage.objects.create(clinic=clinic, image=image.image, is_cover_image=is_cover_image)
            post_save.connect(clinic_image_handler, sender=sender)

@receiver(post_save, sender=ClinicBeforeAfterImage)
@receiver(post_delete, sender=ClinicBeforeAfterImage)
def clinic_before_after_image_handler(sender, instance, **kwargs):
    obj = instance
    for clinic in Clinic.objects.all().filter(~Q(id=obj.clinic.id)).filter(code=obj.clinic.code):
        post_delete.disconnect(clinic_before_after_image_handler, sender=sender)
        ClinicBeforeAfterImage.objects.all().filter(clinic= clinic).delete()
        post_delete.connect(clinic_before_after_image_handler, sender=sender)
        post_save.disconnect(clinic_before_after_image_handler, sender=sender)
        for image in obj.clinic.allimagesafter.all().reverse():
            ClinicBeforeAfterImage.objects.create(clinic=clinic, afterImage=image.afterImage, beforeImage= image.beforeImage)
        post_save.connect(clinic_before_after_image_handler, sender=sender)


@receiver(post_save, sender=ClinicCertficates)
@receiver(post_delete, sender=ClinicCertficates)
def clinic_certificate_handler(sender, instance, **kwargs):
    obj = instance
    for clinic in Clinic.objects.all().filter(~Q(id=obj.clinic.id)).filter(code=obj.clinic.code):
        post_delete.disconnect(clinic_certificate_handler, sender=sender)
        ClinicCertficates.objects.all().filter(clinic= clinic).delete()
        post_delete.connect(clinic_certificate_handler, sender=sender)
        post_save.disconnect(clinic_certificate_handler, sender=sender)
        for certificate in obj.clinic.allcertificatesforclinic.all().reverse():
            ClinicCertficates.objects.create(clinic=clinic, certificates=certificate.certificates)
        post_save.connect(clinic_certificate_handler, sender=sender)


@receiver(m2m_changed, sender=Clinic.clinic_languages.through)
def clinic_handler(sender, instance, action, reverse, model, **kwargs):
    if action == 'post_add' or action == 'post_remove':
        print(instance)
        for clinic in Clinic.objects.all().filter(~Q(id=instance.id)).filter(code=instance.code):
            clinic.clinic_languages.clear()
            for i in instance.clinic_languages.all().reverse():
                m2m_changed.disconnect(clinic_handler, sender=sender)
                clinic.clinic_languages.add(i)
                m2m_changed.connect(clinic_handler, sender=sender)
                
admin.site.register(Clinic, ClinicAdmin)
admin.site.register(DoctorProxy, DoctorAdmin)
admin.site.register(TreatmentProxy, TreatmentAdmin)
admin.site.register(RankingClinics, RankingClinicsAdmin)
