from django.contrib import admin
from django.db import models
from .models import BlogPost, BlogContact
from tinymce.widgets import TinyMCE

class blogAdmin(admin.ModelAdmin):
   list_display = ["title"]
   formfield_overrides = {
   models.TextField: {'widget': TinyMCE()}
}

admin.site.register(BlogPost, blogAdmin)
admin.site.register(BlogContact)
