from urllib.parse import unquote
from django.http import HttpResponse
from django.shortcuts import redirect, render
from clinics.models import Clinic, Country, Contact as ContactModel, Language, RankingClinics
from doctors.models import TopDestinations, PopularTreatment, PopularFooterTreatment
from treatment.models import Treatment

from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Q
import json
from django.utils.text import slugify

def error_404(request, exception):
        data = {}
        return render(request,'main/404.html', data)

def error_500(request):
        data = {}
        return render(request,'main/404.html', data)


def Home(request):
    # countries = [clinic.country.name for clinic in sorted(Clinic.objects.filter(status= 'publish'), key=lambda x: x.get_avg_rating, reverse=True)]
    # countries = Country.objects.filter(name__in = countries, language=Language.objects.filter(code=request.LANGUAGE_CODE).first()).order_by('name')[:8]
    countries = TopDestinations.objects.filter(language=Language.objects.get(code=request.LANGUAGE_CODE)).all()
    treatments = Treatment.objects.filter(language=Language.objects.get(code=request.LANGUAGE_CODE)).all()
    popular_treatments = PopularTreatment.objects.filter(language=Language.objects.get(code=request.LANGUAGE_CODE), in_header=False).all()
    
    # for i in RankingClinics.objects.all():
    #     # reset their old_ranks
    #     i.old_rank = None
    #     i.save()


    return render(request, 'main/index.html', {'countries': countries, 'treatments': treatments, 'popular_treatments': popular_treatments})

def exists_in_treatments(request):
    q = unquote(request.GET.get('term', ''))
    country_name = unquote(request.GET.get('country', ''))
    language = unquote(request.GET.get('language', ''))

    treatment = Treatment.objects.filter(language = Language.objects.get(code=language), searched_treatment__iexact=q)

    if country_name:
        country = Country.objects.filter(name=country_name, language=Language.objects.get(code=language))

        if treatment.exists() and country.exists():
            return HttpResponse(True)
        else:
            return HttpResponse(False)
    else:
        if treatment.exists():
            return HttpResponse(True)
        else:
            return HttpResponse(False)

def show_error(request):
    messages.error(request, "Please select from the available options.")
    return HttpResponse(True)

def Contact(request):
    if request.method == "POST":
        title = request.POST.get('title')
        name = request.POST.get('name')
        address_1 = request.POST.get('address1')
        address_2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        postal_code = request.POST.get('zipcode')
        phone_code = request.POST.get('phone_code')
        phone_no = request.POST.get('phone_number')
        email = request.POST.get('email')
        msg = request.POST.get('message')
        ContactModel.objects.create(title=title, name=name, address_1=address_1, address_2=address_2, city=city, state=state, country=country, postal_code=postal_code, phone_code=phone_code, phone_no=phone_no, email=email, msg=msg)
        if request.LANGUAGE_CODE == "fr":
            messages.success(request, "Votre message a été envoyé avec succès.")
        else:
            messages.success(request, "Your message has been sent successfully.")
        return redirect(request.path_info)
    all_countries = Country.objects.filter(language=Language.objects.get(code=request.LANGUAGE_CODE)).reverse()
    context = {
        'all_countries': all_countries
    }
    
    return render(request, 'main/contact.html', context)

def About(request):
    return render(request, 'main/about.html')

def TermsAndConditions(request):
    return render(request, 'main/terms-and-conditions.html')

def Sitemap(request):
    if request.LANGUAGE_CODE == "fr":
        return HttpResponse(open('sitemap_fr.xml').read(), content_type='text/xml')
    elif request.LANGUAGE_CODE == "ar":
        return HttpResponse(open('sitemap_ar.xml').read(), content_type='text/xml')
    else:
        return HttpResponse(open('sitemap_en.xml').read(), content_type='text/xml')
    
@csrf_exempt
def change_currency(request):
    if request.method=='POST':
        currency = request.POST.get('currency')
        request.session['currency'] = currency
        return HttpResponse('ok')

@csrf_exempt
def create_slug(request):
    if request.method=='POST':
        slug = request.POST.get('slug')
        return HttpResponse(slugify(unquote(slug), allow_unicode=True))


def autocompleteModel(request):
    q = request.GET.get('term', '').capitalize()
    language = request.GET.get('language')
    treatments = Treatment.objects.filter(language = Language.objects.get(code=language))

    # make treatments unique with attribute "searched_treatment"
    final_treatments = []
    for i in treatments:
        if (str(i.searched_treatment).capitalize() not in final_treatments) and (str(unquote(q)).lower().strip() in str(i.searched_treatment).lower().strip()):
            final_treatments.append(str(i.searched_treatment).capitalize())
    # send only first 5 treatments
    final_treatments = final_treatments[:5]
    data = json.dumps(final_treatments)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype) 


def autocompleteCountryModel(request):
    q = request.GET.get('term', '').lower().strip()
    language = request.GET.get('language')
    countries = Country.objects.filter(language = Language.objects.get(code=language))
    all_countries = [i.name for i in countries if q in str(i.name).lower().strip() ]
    data = json.dumps(all_countries[:5])
    mimetype = 'application/json'
    return HttpResponse(data, mimetype) 


phones_codes = [{'phone_code': '93', 'iso_code': 'af'}, {'phone_code': '93', 'iso_code': 'af'}, {'phone_code': '355', 'iso_code': 'al'}, {'phone_code': '213', 'iso_code': 'dz'}, {'phone_code': '1-684', 'iso_code': 'as'}, {'phone_code': '376', 'iso_code': 'ad'}, {'phone_code': '244', 'iso_code': 'ao'}, {'phone_code': '244', 'iso_code': 'ao'}, {'phone_code': '1-264', 'iso_code': 'ai'}, {'phone_code': '1-264', 'iso_code': 'ai'}, {'phone_code': '672', 'iso_code': 'aq'}, {'phone_code': '1-268', 'iso_code': 'ag'}, {'phone_code': '54', 'iso_code': 'ar'}, {'phone_code': '374', 'iso_code': 'am'}, {'phone_code': '297', 'iso_code': 'aw'}, {'phone_code': '297', 'iso_code': 'aw'}, {'phone_code': '61', 'iso_code': 'au'}, {'phone_code': '43', 'iso_code': 'at'}, {'phone_code': '994', 'iso_code': 'az'}, {'phone_code': '973', 'iso_code': 'bh'}, {'phone_code': '880', 'iso_code': 'bd'}, {'phone_code': '880', 'iso_code': 'bd'}, {'phone_code': '1-246', 'iso_code': 'bb'}, {'phone_code': '375', 'iso_code': 'by'}, {'phone_code': '32', 'iso_code': 'be'}, {'phone_code': '501', 'iso_code': 'bz'}, {'phone_code': '501', 'iso_code': 'bz'}, {'phone_code': '229', 'iso_code': 'bj'}, {'phone_code': '1-441', 'iso_code': 'bm'}, {'phone_code': '975', 'iso_code': 'bt'}, {'phone_code': '591', 'iso_code': 'bo'}, {'phone_code': '599', 'iso_code': 'bq'}, {'phone_code': '387', 'iso_code': 'ba'}, {'phone_code': '267', 'iso_code': 'bw'}, {'phone_code': '267', 'iso_code': 'bw'}, {'phone_code': '47', 'iso_code': 'bv'}, {'phone_code': '55', 'iso_code': 'br'}, {'phone_code': '246', 'iso_code': 'io'}, {'phone_code': '673', 'iso_code': 'bn'}, {'phone_code': '359', 'iso_code': 'bg'}, {'phone_code': '226', 'iso_code': 'bf'}, {'phone_code': '226', 'iso_code': 'bf'}, {'phone_code': '257', 'iso_code': 'bi'}, {'phone_code': '257', 'iso_code': 'bi'}, {'phone_code': '855', 'iso_code': 'kh'}, {'phone_code': '237', 'iso_code': 'cm'}, {'phone_code': '1', 'iso_code': 'ca'}, {'phone_code': '1', 'iso_code': 'ca'}, {'phone_code': '1-345', 'iso_code': 'ky'}, {'phone_code': '236', 'iso_code': 'cf'}, {'phone_code': '235', 'iso_code': 'td'}, {'phone_code': '235', 'iso_code': 'td'}, {'phone_code': '56', 'iso_code': 'cl'}, {'phone_code': '86', 'iso_code': 'cn'}, {'phone_code': '852', 'iso_code': 'cn'}, {'phone_code': '853', 'iso_code': 'cn'}, {'phone_code': '61', 'iso_code': 'cx'}, {'phone_code': '61', 'iso_code': 'cc'}, {'phone_code': '57', 'iso_code': 'co'}, {'phone_code': '269', 'iso_code': 'km'}, {'phone_code': '242', 'iso_code': 'cg'}, {'phone_code': '243', 'iso_code': 'cg'}, {'phone_code': '242', 'iso_code': 'cg'}, {'phone_code': '243', 'iso_code': 'cg'}, {'phone_code': '682', 'iso_code': 'ck'}, {'phone_code': '506', 'iso_code': 'cr'}, {'phone_code': '506', 'iso_code': 'cr'}, {'phone_code': '385', 'iso_code': 'hr'}, {'phone_code': '53', 'iso_code': 'cu'}, {'phone_code': '53', 'iso_code': 'cu'}, {'phone_code': '599', 'iso_code': 'cw'}, {'phone_code': '599', 'iso_code': 'cw'}, {'phone_code': '357', 'iso_code': 'cy'}, {'phone_code': '243', 'iso_code': 'cd'}, {'phone_code': '45', 'iso_code': 'dk'}, {'phone_code': '253', 'iso_code': 'dj'}, {'phone_code': '253', 'iso_code': 'dj'}, {'phone_code': '1-767', 'iso_code': 'dm'}, {'phone_code': '1-809,1-829,1-849', 'iso_code': 'dm'}, {'phone_code': '1-809,1-829,1-849', 'iso_code': 'dm'}, {'phone_code': '1-809,1-829,1-849', 'iso_code': 'do'}, {'phone_code': '593', 'iso_code': 'ec'}, {'phone_code': '20', 'iso_code': 'eg'}, {'phone_code': '503', 'iso_code': 'sv'}, {'phone_code': '503', 'iso_code': 'sv'}, {'phone_code': '240', 'iso_code': 'gq'}, {'phone_code': '291', 'iso_code': 'er'}, {'phone_code': '372', 'iso_code': 'ee'}, {'phone_code': '251', 'iso_code': 'et'}, {'phone_code': '500', 'iso_code': 'fk'}, {'phone_code': '298', 'iso_code': 'fo'}, {'phone_code': '358', 'iso_code': 'fi'}, {'phone_code': '358', 'iso_code': 'fi'}, {'phone_code': '33', 'iso_code': 'fr'}, {'phone_code': '33', 'iso_code': 'fr'}, {'phone_code': '594', 'iso_code': 'gf'}, {'phone_code': '689', 'iso_code': 'pf'}, {'phone_code': '262', 'iso_code': 'tf'}, {'phone_code': '241', 'iso_code': 'ga'}, {'phone_code': '241', 'iso_code': 'ga'}, {'phone_code': '995', 'iso_code': 'ge'}, {'phone_code': '500', 'iso_code': 'ge'}, {'phone_code': '49', 'iso_code': 'de'}, {'phone_code': '233', 'iso_code': 'gh'}, {'phone_code': '233', 'iso_code': 'gh'}, {'phone_code': '350', 'iso_code': 'gi'}, {'phone_code': '350', 'iso_code': 'gi'}, {'phone_code': '30', 'iso_code': 'gr'}, {'phone_code': '299', 'iso_code': 'gl'}, {'phone_code': '1-473', 'iso_code': 'gd'}, {'phone_code': '590', 'iso_code': 'gp'}, {'phone_code': '590', 'iso_code': 'gp'}, {'phone_code': '1-671', 'iso_code': 'gu'}, {'phone_code': '1-671', 'iso_code': 'gu'}, {'phone_code': '502', 'iso_code': 'gt'}, {'phone_code': '502', 'iso_code': 'gt'}, {'phone_code': '240', 'iso_code': 'gn'}, {'phone_code': '224', 'iso_code': 'gn'}, {'phone_code': '245', 'iso_code': 'gn'}, {'phone_code': '675', 'iso_code': 'gn'}, {'phone_code': '245', 'iso_code': 'gw'}, {'phone_code': '592', 'iso_code': 'gy'}, {'phone_code': '592', 'iso_code': 'gy'}, {'phone_code': '509', 'iso_code': 'ht'}, {'phone_code': '672', 'iso_code': 'hm'}, {'phone_code': '504', 'iso_code': 'hn'}, {'phone_code': '504', 'iso_code': 'hn'}, {'phone_code': '36', 'iso_code': 'hu'}, {'phone_code': '354', 'iso_code': 'is'}, {'phone_code': '246', 'iso_code': 'in'}, {'phone_code': '91', 'iso_code': 'in'}, {'phone_code': '62', 'iso_code': 'id'}, {'phone_code': '98', 'iso_code': 'ir'}, {'phone_code': '98', 'iso_code': 'ir'}, {'phone_code': '964', 'iso_code': 'iq'}, {'phone_code': '964', 'iso_code': 'iq'}, {'phone_code': '353', 'iso_code': 'ie'}, {'phone_code': '44', 'iso_code': 'ie'}, {'phone_code': '972', 'iso_code': 'il'}, {'phone_code': '39', 'iso_code': 'it'}, {'phone_code': '1-876', 'iso_code': 'jm'}, {'phone_code': '81', 'iso_code': 'jp'}, {'phone_code': '44', 'iso_code': 'je'}, {'phone_code': '44', 'iso_code': 'je'}, {'phone_code': '962', 'iso_code': 'jo'}, {'phone_code': '962', 'iso_code': 'jo'}, {'phone_code': '7', 'iso_code': 'kz'}, {'phone_code': '7', 'iso_code': 'kz'}, {'phone_code': '254', 'iso_code': 'ke'}, {'phone_code': '254', 'iso_code': 'ke'}, {'phone_code': '686', 'iso_code': 'ki'}, {'phone_code': '686', 'iso_code': 'ki'}, {'phone_code': '965', 'iso_code': 'kw'}, {'phone_code': '996', 'iso_code': 'kg'}, {'phone_code': '680', 'iso_code': 'la'}, {'phone_code': '371', 'iso_code': 'lv'}, {'phone_code': '961', 'iso_code': 'lb'}, {'phone_code': '266', 'iso_code': 'ls'}, {'phone_code': '266', 'iso_code': 'ls'}, {'phone_code': '231', 'iso_code': 'lr'}, {'phone_code': '218', 'iso_code': 'ly'}, {'phone_code': '423', 'iso_code': 'li'}, {'phone_code': '423', 'iso_code': 'li'}, {'phone_code': '370', 'iso_code': 'lt'}, {'phone_code': '352', 'iso_code': 'lu'}, {'phone_code': '352', 'iso_code': 'lu'}, {'phone_code': '389', 'iso_code': 'mk'}, {'phone_code': '261', 'iso_code': 'mg'}, {'phone_code': '261', 'iso_code': 'mg'}, {'phone_code': '265', 'iso_code': 'mw'}, {'phone_code': '265', 'iso_code': 'mw'}, {'phone_code': '60', 'iso_code': 'my'}, {'phone_code': '960', 'iso_code': 'mv'}, {'phone_code': '960', 'iso_code': 'mv'}, {'phone_code': '223', 'iso_code': 'ml'}, {'phone_code': '252', 'iso_code': 'ml'}, {'phone_code': '223', 'iso_code': 'ml'}, {'phone_code': '252', 'iso_code': 'ml'}, {'phone_code': '356', 'iso_code': 'mt'}, {'phone_code': '692', 'iso_code': 'mh'}, {'phone_code': '596', 'iso_code': 'mq'}, {'phone_code': '596', 'iso_code': 'mq'}, {'phone_code': '222', 'iso_code': 'mr'}, {'phone_code': '230', 'iso_code': 'mu'}, {'phone_code': '262', 'iso_code': 'yt'}, {'phone_code': '262', 'iso_code': 'yt'}, {'phone_code': '52', 'iso_code': 'mx'}, {'phone_code': '691', 'iso_code': 'fm'}, {'phone_code': '373', 'iso_code': 'md'}, {'phone_code': '373', 'iso_code': 'md'}, {'phone_code': '377', 'iso_code': 'mc'}, {'phone_code': '377', 'iso_code': 'mc'}, {'phone_code': '976', 'iso_code': 'mn'}, {'phone_code': '382', 'iso_code': 'me'}, {'phone_code': '1-664', 'iso_code': 'ms'}, {'phone_code': '1-664', 'iso_code': 'ms'}, {'phone_code': '212', 'iso_code': 'ma'}, {'phone_code': '258', 'iso_code': 'mz'}, {'phone_code': '258', 'iso_code': 'mz'}, {'phone_code': '95', 'iso_code': 'mm'}, {'phone_code': '95', 'iso_code': 'mm'}, {'phone_code': '264', 'iso_code': 'na'}, {'phone_code': '674', 'iso_code': 'nr'}, {'phone_code': '674', 'iso_code': 'nr'}, {'phone_code': '977', 'iso_code': 'np'}, {'phone_code': '31', 'iso_code': 'nl'}, {'phone_code': '687', 'iso_code': 'nc'}, {'phone_code': '64', 'iso_code': 'nz'}, {'phone_code': '505', 'iso_code': 'ni'}, {'phone_code': '505', 'iso_code': 'ni'}, {'phone_code': '227', 'iso_code': 'ne'}, {'phone_code': '234', 'iso_code': 'ne'}, {'phone_code': '227', 'iso_code': 'ne'}, {'phone_code': '234', 'iso_code': 'ng'}, {'phone_code': '683', 'iso_code': 'nu'}, {'phone_code': '672', 'iso_code': 'nf'}, {'phone_code': '1-670', 'iso_code': 'mp'}, {'phone_code': '47', 'iso_code': 'no'}, {'phone_code': '968', 'iso_code': 'om'}, {'phone_code': '968', 'iso_code': 'om'}, {'phone_code': '40', 'iso_code': 'om'}, {'phone_code': '92', 'iso_code': 'pk'}, {'phone_code': '92', 'iso_code': 'pk'}, {'phone_code': '680', 'iso_code': 'pw'}, {'phone_code': '507', 'iso_code': 'pa'}, {'phone_code': '507', 'iso_code': 'pa'}, {'phone_code': '675', 'iso_code': 'pg'}, {'phone_code': '595', 'iso_code': 'py'}, {'phone_code': '595', 'iso_code': 'py'}, {'phone_code': '51', 'iso_code': 'pe'}, {'phone_code': '63', 'iso_code': 'ph'}, {'phone_code': '63', 'iso_code': 'ph'}, {'phone_code': '48', 'iso_code': 'pl'}, {'phone_code': '351', 'iso_code': 'pt'}, {'phone_code': '351', 'iso_code': 'pt'}, {'phone_code': '1', 'iso_code': 'pr'}, {'phone_code': '974', 'iso_code': 'qa'}, {'phone_code': '974', 'iso_code': 'qa'}, {'phone_code': '40', 'iso_code': 'ro'}, {'phone_code': '7', 'iso_code': 'ru'}, {'phone_code': '250', 'iso_code': 'rw'}, {'phone_code': '250', 'iso_code': 'rw'}, {'phone_code': '290', 'iso_code': 'sh'}, {'phone_code': '1-869', 'iso_code': 'kn'}, {'phone_code': '1-758', 'iso_code': 'lc'}, {'phone_code': '508', 'iso_code': 'pm'}, {'phone_code': '1-784', 'iso_code': 'vc'}, {'phone_code': '1-684', 'iso_code': 'ws'}, {'phone_code': '685', 'iso_code': 'ws'}, {'phone_code': '1-684', 'iso_code': 'ws'}, {'phone_code': '685', 'iso_code': 'ws'}, {'phone_code': '378', 'iso_code': 'sm'}, {'phone_code': '239', 'iso_code': 'st'}, {'phone_code': '966', 'iso_code': 'sa'}, {'phone_code': '221', 'iso_code': 'sn'}, {'phone_code': '381', 'iso_code': 'rs'}, {'phone_code': '248', 'iso_code': 'sc'}, {'phone_code': '248', 'iso_code': 'sc'}, {'phone_code': '232', 'iso_code': 'sl'}, {'phone_code': '232', 'iso_code': 'sl'}, {'phone_code': '65', 'iso_code': 'sg'}, {'phone_code': '1-721', 'iso_code': 'sx'}, {'phone_code': '421', 'iso_code': 'sk'}, {'phone_code': '386', 'iso_code': 'si'}, {'phone_code': '677', 'iso_code': 'sb'}, {'phone_code': '252', 'iso_code': 'so'}, {'phone_code': '27', 'iso_code': 'za'}, {'phone_code': '500', 'iso_code': 'gs'}, {'phone_code': '211', 'iso_code': 'ss'}, {'phone_code': '34', 'iso_code': 'es'}, {'phone_code': '94', 'iso_code': 'lk'}, {'phone_code': '94', 'iso_code': 'lk'}, {'phone_code': '211', 'iso_code': 'sd'}, {'phone_code': '249', 'iso_code': 'sd'}, {'phone_code': '597', 'iso_code': 'sr'}, {'phone_code': '597', 'iso_code': 'sr'}, {'phone_code': '47', 'iso_code': 'sj'}, {'phone_code': '46', 'iso_code': 'se'}, {'phone_code': '41', 'iso_code': 'ch'}, {'phone_code': '963', 'iso_code': 'sy'}, {'phone_code': '992', 'iso_code': 'tj'}, {'phone_code': '255', 'iso_code': 'tz'}, {'phone_code': '66', 'iso_code': 'th'}, {'phone_code': '228', 'iso_code': 'tg'}, {'phone_code': '228', 'iso_code': 'tg'}, {'phone_code': '690', 'iso_code': 'tk'}, {'phone_code': '676', 'iso_code': 'to'}, {'phone_code': '676', 'iso_code': 'to'}, {'phone_code': '1-868', 'iso_code': 'tt'}, {'phone_code': '216', 'iso_code': 'tn'}, {'phone_code': '90', 'iso_code': 'tr'}, {'phone_code': '993', 'iso_code': 'tm'}, {'phone_code': '1-649', 'iso_code': 'tc'}, {'phone_code': '688', 'iso_code': 'tv'}, {'phone_code': '688', 'iso_code': 'tv'}, {'phone_code': '256', 'iso_code': 'ug'}, {'phone_code': '256', 'iso_code': 'ug'}, {'phone_code': '380', 'iso_code': 'ua'}, {'phone_code': '380', 'iso_code': 'ua'}, {'phone_code': '971', 'iso_code': 'ae'}, {'phone_code': '44', 'iso_code': 'gb'}, {'phone_code': '', 'iso_code': 'us'}, {'phone_code': '1-340', 'iso_code': 'us'}, {'phone_code': '1', 'iso_code': 'us'}, {'phone_code': '', 'iso_code': 'um'}, {'phone_code': '598', 'iso_code': 'uy'}, {'phone_code': '598', 'iso_code': 'uy'}, {'phone_code': '998', 'iso_code': 'uz'}, {'phone_code': '678', 'iso_code': 'vu'}, {'phone_code': '678', 'iso_code': 'vu'}, {'phone_code': '58', 'iso_code': 've'}, {'phone_code': '58', 'iso_code': 've'}, {'phone_code': '84', 'iso_code': 'vn'}, {'phone_code': '681', 'iso_code': 'wf'}, {'phone_code': '212', 'iso_code': 'eh'}, {'phone_code': '967', 'iso_code': 'ye'}, {'phone_code': '260', 'iso_code': 'zm'}, {'phone_code': '263', 'iso_code': 'zw'}, {'phone_code': '263', 'iso_code': 'zw'}]


def setInSession(request):
    for i in phones_codes:
        if "-" in str(i['phone_code']):
            continue
        try:
            phone_code = int(str(i['phone_code']).replace('+', ''))
        except:
            print("Error: ", i['phone_code'])
            continue
        countries = Country.objects.filter(phone_code=phone_code)
        for country in countries:
            country.iso_code = i['iso_code']
            country.save()

    return HttpResponse('ok')
