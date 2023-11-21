from clinics.models import Currency, Language
from doctors.models import PopularFooterTreatment
from doctors.models import PopularTreatment
from doctors.models import PopularDestinations
from treatment.models import Treatment

# context_processors.py
def currency_processor(request):
    currencies = Currency.objects.all()

    if not (request.session.get('currency', None)): 
        if request.LANGUAGE_CODE == "fr":
            current_symbol = "€"
        else:
            current_symbol = "$"
    else:
        current_symbol = "$"
        try:
            current_symbol = Currency.objects.get(name=request.session['currency']).symbol
        except Currency.DoesNotExist:
            current_symbol = "$"

    context = {
        'currencies': currencies,
        'current_symbol': current_symbol,
        'language': request.LANGUAGE_CODE
    }
    return context


def language_processor(request):
    languages = Language.objects.all()
    # current_language = Language.objects.all().filter(code = request.LANGUAGE_CODE or 'en-us')[0]
    if not (request.session.get('currency', None)): 
        if request.LANGUAGE_CODE == "fr":
            request.session['currency'] = "EUR"
        else:
            request.session['currency'] = "USD"

    context = {
        'all_available_language': languages,
    }
    return context


def popular_footer_treatment(request):
    popular_footer_treatments = PopularFooterTreatment.objects.filter(language=Language.objects.get(code=request.LANGUAGE_CODE), in_header=False).all()
    popular_header_treatments = PopularTreatment.objects.filter(language=Language.objects.get(code=request.LANGUAGE_CODE), in_header=True).all()
    popular_header_destinations = PopularDestinations.objects.filter(language=Language.objects.get(code=request.LANGUAGE_CODE)).all()
    context = {
        'popular_footer_treatments': popular_footer_treatments,
        'popular_header_treatments': popular_header_treatments,
        'popular_header_destinations': popular_header_destinations,
    }
    return context
