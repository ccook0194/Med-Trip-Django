from django.urls import path
from . import views
app_name='clinics'

urlpatterns=[
    path('add-clinic/',views.add_clinic, name="clinics_add_clinic"),
    path("clinic", views.search_clinic, name="clinics_search"),
    path('treatments/', views.treatments, name="clinic_treatments"),
    path("destinations", views.destinations, name="clinic_destinations"),
    path("destinations/<str:search_country>", views.destinations, name="clinic_destinations"),
    path("destinations/<str:search_country>/<str:search_city>", views.destinations, name="clinic_destinations"),

    path('free-quote/', views.get_free_quote, name= "free_quote_without_clinic"),
    path('<slug:clinic_slug>/', views.get_each_clinic, name= "clinics_each_detail"),
    path('<slug:clinic_slug>/add-review', views.get_reviews, name= "clinics_reviews"),
    path("clinic/<str:search_treatment>", views.search_clinic, name="clinics_search"),
    path("clinic/<str:search_treatment>/<str:search_country>", views.search_clinic, name="clinics_search"),
    path("clinic/<str:search_treatment>/<str:search_country>/<str:search_city>", views.search_clinic, name="clinics_search"),
    path("rankings/<str:category>", views.rankings, name="clinics_rankings"),
    path("rankings/<str:category>/<str:country>", views.rankings, name="clinics_rankings"),
    path("rankings/<str:category>/<str:country>/<str:city>", views.rankings, name="clinics_rankings"),
    path('run-interval', views.run_interval, name="run_interval"),
]
