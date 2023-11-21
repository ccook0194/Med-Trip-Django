from django.urls import path
from . import views
app_name='blog'

urlpatterns=[
    path('',views.index, name='blog'),
    path('post/<str:slug>', views.blog_post, name="blog_post")
]
