from django.shortcuts import render, redirect

from clinics.models import Country, Language
from .models import BlogPost, BlogContact
from django.core.paginator import Paginator
from django.contrib import messages
from urllib.parse import unquote

# Create your views here.

def index(request):
    posts = BlogPost.objects.filter(language__code=request.LANGUAGE_CODE).all().order_by('-timestamp')
    # pagination
    paginator = Paginator(posts, 10)
    page_no = request.GET.get('page', 1)
    current_page = paginator.page(page_no)

    # context
    context = {
        'posts': current_page.object_list,
        "paginator": paginator,
        "current_page": current_page,
        "page_no": page_no,
    }
    return render(request, 'blog/index.html', context)


def blog_post(request, slug):
    slug = unquote(slug)
    post = BlogPost.objects.get(slug=slug)
    countries = Country.objects.filter(language=Language.objects.get(code=request.LANGUAGE_CODE)).reverse()

    if request.method == "POST":
        comment = request.POST.get('comment')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_code = request.POST.get("phone_code")
        phone_no = request.POST.get('phone_no')
        blogcontact_instance= BlogContact.objects.create(name = name, email=email, phone_code=phone_code, phone_no=phone_no, comment = comment)
        blogcontact_instance.save()
        if request.LANGUAGE_CODE == "fr":
            messages.success(request, "Votre message a été envoyé avec succès.")
        else:
            messages.success(request, "Your message has been sent successfully.")
        return redirect(request.path_info)

    context = {
        'post': post,
        "all_countries": countries
    }
    
    return render(request, 'blog/post.html', context)
