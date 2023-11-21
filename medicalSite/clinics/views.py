
from django.shortcuts import redirect, render
from django.http import HttpResponse

from treatment.models import Treatment
from .models import *
from django.db.models import Q
import json
from operator import attrgetter
import sys
from django.contrib import messages
from urllib.parse import unquote

import json

from google_currency import CODES

import pycountry
import threading
import time
from .codes import CODES

from forex_python.converter import CurrencyRates
 

one_usd_to_aed = 3.67

CODES = {
    "GBP": "Pound sterling",
    "AUD": "Australian Dollar",
    "EUR": "Euro",
    "CAD": "Canadian Dollar",
    "CHF": "Swiss Franc",
    "AED": "United Arab Emirates Dirham",
    "USD": "United States Dollar",
}

def thread_function():
    c = CurrencyRates()
    while True:
        # run for loop on CODES 
        # delete all the records from the table

        CurrencyPricesList = list()

        # get the latest prices from the API and save it to the database
        for code in list(CODES.keys()):
            # amount = float(json.loads(convert(code, 'USD', 1))['amount'])
            try:
                if code == 'AED':
                    amount = 1/one_usd_to_aed
                elif code == 'USD':
                    amount = 1
                else:
                    amount = float(c.convert(code, 'USD', 1))
            except Exception:
                continue
            print(code, amount)
            # CurrencyPrices.objects.create(code=code, price=amount)
            CurrencyPricesList.append(CurrencyPrices(code=code, price=amount))

        CurrencyPrices.objects.all().delete()
        CurrencyPrices.objects.bulk_create(CurrencyPricesList)
        # sleep for 12 hrs
        time.sleep(43200)


def run_interval():
    t = threading.Thread(target=thread_function)
    t.start()
    return HttpResponse("Hello, world. You're at the run_interval.")

def get_each_clinic(request, clinic_slug):
    random_treatments = []
    clinic_data = Clinic.objects.get(slug=clinic_slug, language=Language.objects.get(code=request.LANGUAGE_CODE), status= 'publish')
    clinic_images = json.dumps(
        [{"src": i.image.url, "subHtml": ""} for i in clinic_data.allimages.all()])
    cover_image = clinic_data.allimages.filter().first()


    treatments = clinic_data.alltreatments.filter(language__code=request.LANGUAGE_CODE).all()
    # get first 2 treatments
    for treatment in treatments:
        random_treatments.append(treatment)
        if len(random_treatments) == 2:
            break

    # join treatments
    two_random_treatments = ', '.join(map(str, random_treatments))

    # clinic packages
    clinic_packages = clinic_data.allpackagesforclinic.filter(language__code=request.LANGUAGE_CODE).all()
    return render(request, "clinic/clinic-page.html", {"cover_image": cover_image, "clinic_data": clinic_data, "clinic_images": clinic_images, "two_random_treatments": two_random_treatments, "clinic_packages": clinic_packages})


def get_reviews(request, clinic_slug):
    clinic_data = Clinic.objects.get(slug=clinic_slug, language=Language.objects.get(code=request.LANGUAGE_CODE), status= 'publish')
    all_countries = Country.objects.filter(language=Language.objects.get(code=request.LANGUAGE_CODE)).reverse()

    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        review = request.POST.get("review")

        quality_rating = request.POST.get('QualityStar')
        service_rating = request.POST.get('ServiceStar')
        cleanliness_rating = request.POST.get('CleanlinessStar')
        comfort_rating = request.POST.get('ComfortStar')
        communication_rating = request.POST.get('CommunicationStar')


        review_instance= ClinicReviews.objects.create(clinic=clinic_data, name=name, email=email, review=review,
        quality_rating=quality_rating, service_rating=service_rating, cleanliness_rating=cleanliness_rating, comfort_rating=comfort_rating, communication_rating=communication_rating)
        review_instance.save()
        if request.LANGUAGE_CODE == 'fr':
            messages.success(request, 'Votre avis a été envoyé avec succès.')
        else:
            messages.success(request, 'Your review has been submitted successfully.')
        return redirect(f'/{clinic_slug}')

    context = {
        "clinic_data": clinic_data, 
        "all_countries": all_countries
    }
    return render(request, "clinic/add-review.html", context)

def submit_form_request(request, treatment_name, clinic_slug=None):
    username = request.POST.get("name")
    email = request.POST.get("email")
    phone_code = request.POST.get("phone_code")
    phone_no = request.POST.get("phone_number")
    comment = request.POST.get("comments")


    if clinic_slug or treatment_name:
        clinic_data = Clinic.objects.get(slug=clinic_slug, language=Language.objects.get(code=request.LANGUAGE_CODE), status= 'publish')
        clinic_treatment_leads_instance= ClinicTreatmentLeads.objects.create(username=username, email=email, phone_code=phone_code, 
        phone_no=phone_no, comment = comment, treatment_detail = treatment_name, clinic=clinic_data)
    else:
        clinic_treatment_leads_instance= ClinicTreatmentLeads.objects.create(username=username, email=email, phone_code=phone_code, 
        phone_no=phone_no, comment = comment, treatment_detail = treatment_name)
    clinic_treatment_leads_instance.save()


def get_free_quote(request):
    all_countries = Country.objects.filter(language=Language.objects.get(code=request.LANGUAGE_CODE)).reverse()
    context = {'all_countries': all_countries}

    global clinic
    global treatment_name
    if request.method == 'POST':
        if request.POST.get('from_search'):
            clinic = request.POST.get('clinic_slug')
            treatment_name = request.POST.get('treatment_name', '')

            return render(request, "clinic/free-quote.html", context)
            
        submit_form_request(request, clinic_slug=clinic, treatment_name=treatment_name)
        if request.LANGUAGE_CODE == 'fr':
            messages.success(request, 'Votre demande a été envoyée avec succès.')
        else:
            messages.success(request, 'Your request has been submitted successfully.')
        return redirect(request.path_info)
    
    clinic=None
    treatment_name=''

    return render(request, "clinic/free-quote.html", context)


def destinations(request, search_country="", search_city=""):
    sort_by = request.GET.get('sort_by', None)
    country = request.GET.get("country", None)
    city = request.GET.get("city", None)
    score = request.GET.get("score", 0)

    search_country = unquote(search_country)
    search_city = unquote(search_city)

    search_country = country if country else search_country
    search_city = city if city else search_city

    search_city = search_city.replace("-", " ")


    RECORDS_LIMIT = 10

    page = int(request.GET.get('page', 1))

    clinics = Clinic.objects.filter(language=Language.objects.get(code=request.LANGUAGE_CODE), city__icontains=search_city, country__name__icontains=search_country, status= 'publish')
    if sort_by=='rating':
        clinics = sorted(clinics, key=attrgetter('get_avg_rating'), reverse=True)

    # if (search_country) and (not sort_by == 'rating'):
    #     clinics = clinics.filter(country__name=search_country)
    # elif (search_country) and (sort_by == 'rating'):
    #     clinics = [cl for cl in clinics if cl.country.name == search_country]

    # if (search_city):
    #     clinics = [cl for cl in clinics if cl.city == search_city]

    all_clinics = set()
    all_countries = set()
    all_cities = set()

    for cl in clinics:
        if (float(cl.get_avg_rating) >= float(score)):
            if (search_country) :
                all_cities.add(cl.city)
            else:
                all_countries.add(cl.country)

            all_clinics.add(cl)

    clinics_for_destinations = Clinic.objects.filter(language=Language.objects.get(code=request.LANGUAGE_CODE), status= 'publish')
    for cl in clinics_for_destinations:
        if (float(cl.get_avg_rating) >= float(score)):
            if search_country:
                if cl.country.name == search_country:
                    all_cities.add(cl.city)
            else:
                all_countries.add(cl.country)
    all_clinics = list(all_clinics)

    all_clinics = all_clinics[:(RECORDS_LIMIT*page)]

    next_page = int(page) + 1

    # show next page button if next page exists
    if clinics.__len__() > (RECORDS_LIMIT*page):
        next_page_exist = True
    else:
        next_page_exist = False

    # context
    context = {
        "page": page,
        "next_page": next_page,
        "next_page_exist": next_page_exist,
        "all_clinics": all_clinics,
        "sort_by": sort_by,
        "all_countries": all_countries,
        "search_country": search_country,
        "score": score,
        "all_cities": all_cities,
        "search_city": search_city,
        "country": search_country if search_country else None,
        "is_country": search_country if search_country else None,
        "is_city": search_city if search_city else None,

    }

    return render(request, "clinic/search.html", context)



def search_clinic(request, search_treatment= "", search_country = "", search_city=""):
    sort_by = request.GET.get('sort_by', '')
    country = request.GET.get("country", "")
    city = request.GET.get("city", "")
    price = request.GET.get("price", "")
    score = request.GET.get("score", 0)

    RECORDS_LIMIT = 10

    page = int(request.GET.get('page', 1))

    search_treatment = unquote(search_treatment)
    search_country = unquote(search_country)
    search_city = unquote(search_city)


    search_country = country if country else search_country
    search_city = city if city else search_city
    
    search_city = search_city.replace("-", " ")

    if not price:
        price = f"0-{sys.maxsize}"


    min_max_price_options = list()

    min_price = sys.maxsize
    max_price = 0
    treatments = []
    # if not search_country:
    #     treatments = Treatment.objects.filter(Q(slug__iexact=search_treatment)).filter(status= True, clinic__language__code=request.LANGUAGE_CODE, clinic__status= 'publish')
    # else:
    #     if city == "":
    treatments = Treatment.objects.filter(Q(slug__iexact=search_treatment) & Q(clinic__country__name__icontains=search_country) & Q(clinic__city__icontains=search_city)).filter(status= True, clinic__language__code=request.LANGUAGE_CODE, clinic__status= 'publish')
        # else:
        #     treatments = Treatment.objects.filter(Q(slug__iexact=search_treatment) & Q(
        #     clinic__country__name__iexact=search_country)).filter(status= True, clinic__language__code=request.LANGUAGE_CODE, clinic__status= 'publish', clinic__city=search_city)

  

    final_treatments = set()
    all_cities = set()
    all_countries = list()


    for i in treatments:
        convert_to = request.session.get('currency', i.currency.name)
        try:
                
            if convert_to.lower() == "usd":
                i.price = float(CurrencyPrices.objects.filter(code=str(i.currency.name).upper()).first().price) * float(i.price)
            else:
                price_in_usd = float(CurrencyPrices.objects.filter(code=str(i.currency.name).upper()).first().price) * float(i.price)
                price_of_currency_to = float(CurrencyPrices.objects.filter(code=str(convert_to).upper()).first().price)
                i.price = price_in_usd / price_of_currency_to
        except:
            pass

        i.price = int(i.price)
        if min_price > i.price:
            min_price = i.price
        if max_price < i.price:
            max_price = i.price
        if (float(i.clinic.get_avg_rating) >= float(score) and i.price <= int(float(price.split("-")[1])) and i.price >= int(float(price.split("-")[0]))) and i.clinic.language.code == request.LANGUAGE_CODE:
            final_treatments.add(i)

    obj = {
        "min_price": str(int(min_price)),
        "max_price": str(int(int((max_price-min_price)/3) + min_price))
    }
    min_max_price_options.append(obj)
    obj = {
        "min_price": str(int(int((max_price - min_price)/3) + min_price + 1)),
        "max_price": str(int(int(((max_price - min_price)/3) * 2) + min_price))
    }
    min_max_price_options.append(obj)

    obj = {
        "min_price": str(int(int(((max_price - min_price)/3) * 2) + min_price + 1)),
        "max_price": str(int(max_price))
    }
    min_max_price_options.append(obj)

    final_treatments = list(final_treatments)
    if not search_country:
        all_treatments = Treatment.objects.filter(Q(slug__iexact=search_treatment)).filter(status= True, clinic__language__code=request.LANGUAGE_CODE, clinic__status= 'publish').values('clinic__country__name', 'clinic__country__iso_code').distinct()
        temp = []


        for i in all_treatments:
            _country = str(i['clinic__country__name']).lower().split()
            if (_country not in temp):
            # all_countries.add(i['clinic__country__name'])
                all_countries.append({ "name": i['clinic__country__name'], "iso_code": i['clinic__country__iso_code'] })
                temp.append(_country)
    else:
        all_treatments = Treatment.objects.filter(Q(slug__iexact=search_treatment) & Q(clinic__country__name__iexact=search_country)).filter(status= True, clinic__language__code=request.LANGUAGE_CODE, clinic__status= 'publish').values('clinic__city').distinct()
        for i in all_treatments:
            all_cities.add(i['clinic__city'])

    if sort_by == 'price':
        final_treatments = sorted(final_treatments, key=attrgetter('price'))

    elif sort_by == 'rating':
        final_treatments = sorted(final_treatments, key=attrgetter('clinic.get_avg_rating'), reverse=True)
 


    treatments = final_treatments[:(RECORDS_LIMIT*page)]

    next_page = int(page) + 1

    # show next page button if next page exists
    if final_treatments.__len__() > (RECORDS_LIMIT*page):
        next_page_exist = True
    else:
        next_page_exist = False


    # context
    context = {
        "page": page,
        "next_page": next_page,
        "next_page_exist": next_page_exist,
        "search_treatment": search_treatment.replace('-', ' ').capitalize(),
        "original_search_treatment": search_treatment,
        "all_treatments": treatments,
        "sort_by": sort_by,
        "all_cities": all_cities,
        "all_countries": all_countries,
        "min_price": price.split("-")[0],
        "max_price": price.split("-")[1],
        "search_country": search_country if search_country else None,
        "is_country": True if search_country else False,
        "is_city": True if search_city else False,
        "search_city": search_city,
        "score": score,
        "min_max_price_options": min_max_price_options,
        "minimum_price": str(int(min_price)),
    }
    return render(request, "clinic/search.html", context)


def add_clinic(request):
    if request.method == "POST":
        clinic_name = request.POST.get("clinic_name")
        address_1 = request.POST.get("clinic_address1")
        address_2 = request.POST.get("clinic_address2")
        city = request.POST.get("clinic_city")
        state = request.POST.get("clinic_state")
        country = request.POST.get("clinic_country")
        postal_code = request.POST.get("clinic_zipcode")
        website = request.POST.get("clinic_website")
        email = request.POST.get("clinic_email")
        phone_code = request.POST.get("clinic_phone_code")
        phone_no = request.POST.get("clinic_phone_number")
        year_established = request.POST.get("clinic_est_year")
        message = request.POST.get("clinic_comments")
        clinic_instance = ClinicAdd.objects.create(clinic_name=clinic_name, address_1=address_1, address_2=address_2, city=city, state=state,
                                                   country=country, postal_code=postal_code, phone_code=phone_code, phone_no=phone_no, email=email, website=website, year_established=year_established, message=message)
        clinic_instance.save()
        if request.LANGUAGE_CODE == 'fr':
            messages.success(request, "Votre demande de clinique a été soumise avec succès")
        else:
            messages.success(request, "Your request for clinic has been submitted successfully")
        return redirect(request.path_info)
    all_countries = Country.objects.filter(language=Language.objects.get(code=request.LANGUAGE_CODE)).reverse()
    context = {
        'all_countries': all_countries
    }
    return render(request, "clinic/add-clinic.html", context)


def treatments(request):
    appended_treatments = []
    treatments = Treatment.objects.filter(language = Language.objects.get(code=request.LANGUAGE_CODE))
    # make treatments unique with attribute "searched_treatment"
    final_treatments = []
    for i in treatments:
        if str(i.searched_treatment).lower() not in appended_treatments:
            final_treatments.append(i)
            appended_treatments.append(str(i.searched_treatment).lower())

    context = {
        "treatments": final_treatments
    }
    return render(request, "clinic/treatment.html", context)


def rankings(request, category, country='', city=''):
    filter_cities = list()
    filter_countries = list()

    category = unquote(category)
    country = unquote(country)
    city = unquote(city)

    RECORDS_LIMIT = 20

    page = int(request.GET.get('page', 1))

    ranking_clinics = RankingClinics.objects.filter(category=category, country__icontains=country, city__icontains=city, language=Language.objects.get(code=request.LANGUAGE_CODE)).all()
    ranking_clinics_count = ranking_clinics.count()

    ranking_clinics = ranking_clinics[:(RECORDS_LIMIT*page)]

    for i in ranking_clinics:
        if Clinic.objects.filter(slug=i.slug, language=Language.objects.get(code=request.LANGUAGE_CODE)).exists():
            i.clinic_available = True

        if i.country_flag:
            table_country_name = pycountry.countries.get(alpha_2=i.country_flag)
        else:
            table_country_name = pycountry.countries.get(name=i.country)


        if table_country_name:
            i.table_country_name = table_country_name.alpha_3
        else:
            i.table_country_name = i.country

        i.feedback_score = i.feedback_score.__round__(2)
        i.quality_score = i.quality_score.__round__(2)
        i.final_score = i.final_score.__round__(2)

        i.rank = int(i.rank)
        if (i.old_rank):
            i.old_rank = int(i.old_rank)

    if not country:
        all_countries = RankingClinics.objects.filter(category=category, language= Language.objects.get(code=request.LANGUAGE_CODE)).values('country', 'country_flag').distinct()
        temp_countries = list()

        for i in all_countries:
            _country = str(i['country']).lower().split()

            if (_country not in temp_countries) and (i['country_flag']):
                filter_countries.append(i)
                temp_countries.append(_country)


    else:
        all_cities = RankingClinics.objects.filter(category=category, country__icontains=country, language=Language.objects.get(code=request.LANGUAGE_CODE)).values('city').distinct()
        temp_cities = list()

        for i in all_cities:
            _city = str(i['city']).lower().split()
            if _city not in temp_cities:
                filter_cities.append(i['city'])
                temp_cities.append(_city)

    
    next_page = int(page) + 1

    # show next page button if next page exists
    if ranking_clinics_count > (RECORDS_LIMIT*page):
        next_page_exist = True
    else:
        next_page_exist = False
    context = {
        "ranking_clinics": ranking_clinics,
        "category": category,
        "country": country if country else None,
        "city": city if city else None,
        "filter_destinations": filter_countries if not country else filter_cities,
        "page": page,
        "next_page": next_page,
        "next_page_exist": next_page_exist,
        "ranking_clinics_count": ranking_clinics_count
    }
    return render(request, "ranking/index.html", context)
