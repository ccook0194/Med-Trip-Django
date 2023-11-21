"""medicalSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

#local imports
from . import settings
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('change-currency/', views.change_currency, name= 'change_currency'),
    path('create-slug/', views.create_slug, name='create_slug'),
    path('exists-in-treatments/', views.exists_in_treatments, name='exists_in_treatments'),
    path('show-error', views.show_error, name='show_error'),
    path('set-in-session/', views.setInSession, name="set_in_session")
]

urlpatterns += i18n_patterns(
    path('', views.Home, name= 'home'),
    path('blog/', include("blog.urls"), name="blog"),
    path('contact/', views.Contact, name= 'contact'),
    path('about-us/', views.About, name= 'about'),
    path('sitemap/', views.Sitemap, name= 'sitemap'),
    path('terms-and-conditions/', views.TermsAndConditions, name= 'terms_and_conditions'),
    path('ajax_calls/search/', views.autocompleteModel),
    path('ajax_calls/country/search/', views.autocompleteCountryModel),
    path('', include("clinics.urls"), name="clinics"),
    prefix_default_language=False
)
handler404 = 'medicalSite.views.error_404'
handler500 = 'medicalSite.views.error_500'

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)