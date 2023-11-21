from django.db import models
from django.utils.text import slugify
from tinymce.widgets import TinyMCE

from clinics.models import Language

from unidecode import unidecode

from slugify import slugify

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    about = models.CharField(max_length=250, null=True)
    meta_description = models.CharField(max_length=250, null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='bloglanguage', blank= True, null=True)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True, allow_unicode=True)
    cover_img = models.ImageField(upload_to='blog/')
    author = models.CharField(max_length=250, null= True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)

    def __str__(self):
        # sort by date
        return self.title


class BlogContact(models.Model):
    name = models.CharField(max_length=250, blank= False, null= False)
    phone_code = models.CharField(max_length= 256, blank= True, null= True)
    phone_no = models.CharField(max_length= 256, blank= True, null= True)
    email = models.CharField(max_length= 256, blank= False, null= False)
    comment = models.TextField(blank= False, null= False)
    created= models.DateTimeField(auto_now=True)
    is_seen  = models.BooleanField(default= False)
    
    class Meta:
        ordering=('-created',)
        verbose_name_plural='Blog Contact'

    def __str__(self):
        return str(self.name)