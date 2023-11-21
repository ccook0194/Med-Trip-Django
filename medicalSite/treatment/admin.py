import csv
from django.contrib import admin
from django.http import HttpResponse

from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats
from clinics.resources import TreatmentResource
# import ListStyleAdminMixin from 'liststyle.admin.mixin'

# Register your models here.

class ExportCsvMixin:
    def __init__(self) -> None:
        self.field_names = []
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        self.field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(self.field_names)
        for obj in queryset:

            row = writer.writerow([getattr(obj, field) for field in self.field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class TreatmentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = TreatmentResource
    search_fields = ['searched_treatment', 'clinic__code' ]
    list_display = ['get_clinic_id', 'searched_treatment']

    # exclude slug
    exclude = ('slug',)
    
    def get_clinic_id(self, obj):
        return obj.clinic.code

    def get_import_formats(self):
        formats = (
                base_formats.CSV,
        )
        return [f for f in formats if f().can_export()]


class ContactAdmin(admin.ModelAdmin):
    exclude = ('is_seen',)
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        # print name of the object
        obj = self.model.objects.get(id=object_id)
        if not obj.is_seen:
            obj.is_seen = True
            obj.save()

        return super(ContactAdmin, self).changeform_view(request, object_id, form_url, extra_context)

    def contact_status(self, obj):
        if obj.status():
            return '<div style="width:100%%; height:100%%; background-color:orange;">%s</div>' % obj.status()
        return obj.status()
    contact_status.allow_tags = True
    list_display = ('name', 'is_seen',)

    show_model_count = True
    def get_count(self):
        # get columns from model
        return ContactProxy.objects.all().filter(is_seen=False).count()

class ClinicTreatmentLeadsAdmin(admin.ModelAdmin):
    show_model_count = True
    def get_count(self):
        return ClinicTreatmentLeadsProxy.objects.all().filter(is_seen=False).count()


class ClinicAddAdmin(admin.ModelAdmin):
    show_model_count = True
    def get_count(self):
        return ClinicAddProxy.objects.all().filter(is_seen=False).count()


class BlogContactAdmin(admin.ModelAdmin):
    show_model_count = True
    def get_count(self):
        return BlogContactProxy.objects.all().filter(is_seen=False).count()

class ClinicReviewsAdmin(admin.ModelAdmin):
    show_model_count = True
    def get_count(self):
        return ClinicReviewsProxy.objects.all().filter(is_seen=False).count()

# admin.site.register(Treatment, TreatmentAdmin)
admin.site.register(ClinicReviewsProxy, ClinicReviewsAdmin)
admin.site.register(ClinicTreatmentLeadsProxy, ClinicTreatmentLeadsAdmin)
admin.site.register(ClinicAddProxy, ClinicAddAdmin)
admin.site.register(ContactProxy, ContactAdmin)
admin.site.register(BlogContactProxy, BlogContactAdmin)
