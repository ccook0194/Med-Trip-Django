
from django import template
from urllib.parse import unquote

from doctors.models import PopularTreatment
from doctors.models import PopularFooterTreatment


register = template.Library()
from clinics.models import Clinic, Language

@register.filter
def get_clinic_id(clinic, language):
    clinic = Clinic.objects.all().filter(code= clinic.code ,language=Language.objects.get(code=language))
    if clinic:
        return clinic[0].id
    return ""



@register.filter
def get_languages(clinic):
    clinics = Clinic.objects.all().filter(code= clinic.code)
    if clinics:
        languages = [clinic.language for clinic in clinics]
        return languages
    return []


@register.filter
def convert_byte_to_string(value):
    return unquote(value) if value else value


##### POPULAR TREATMENTS #####
@register.filter
def get_popular_treatment_id(p_treatment, language):
    popular_treatment = PopularTreatment.objects.all().filter(code= p_treatment.code ,language=Language.objects.get(code=language))
    if popular_treatment:
        return popular_treatment[0].id
    return ""

    
@register.filter
def get_popular_treatments_languages(p_treatment):
    popular_treatments = PopularTreatment.objects.all().filter(code = p_treatment.code)
    if popular_treatments:
        languages = [i.language for i in popular_treatments]
        return languages
    return []


##### POPULAR FOOTER TREATMENTS #####
@register.filter
def get_popular_footer_treatment_id(p_treatment, language):
    popular_treatment = PopularFooterTreatment.objects.all().filter(code= p_treatment.code ,language=Language.objects.get(code=language))
    if popular_treatment:
        return popular_treatment[0].id
    return ""

    
@register.filter
def get_popular_footer_treatments_languages(p_treatment):
    popular_treatments = PopularFooterTreatment.objects.all().filter(code = p_treatment.code)
    if popular_treatments:
        languages = [i.language for i in popular_treatments]
        return languages
    return []

