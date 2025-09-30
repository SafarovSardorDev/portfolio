from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import (
    Profile, Service, Testimonial, Client, 
    Education, Experience, Skill, Project, BlogPost
)


def get_profile():
    """Profile ma'lumotlarini olish yoki default yaratish"""
    profile = Profile.objects.first()
    if not profile:
        # Agar profile yo'q bo'lsa, default yaratamiz
        profile = Profile.objects.create(
            name="Your Name",
            title="Your Title",
            email="your.email@example.com",
            phone="+1234567890",
            birthday="1990-01-01",
            location="Your City, Your Country",
            about_me="Tell us about yourself here."
        )
    return profile


def index_view(request):
    """Bosh sahifa - About sahifasiga redirect"""
    return HttpResponseRedirect(reverse('about'))


def about_view(request):
    """About sahifasi uchun view"""
    profile = get_profile()
    services = Service.objects.all()
    testimonials = Testimonial.objects.filter(is_active=True)
    clients = Client.objects.all()
    
    # About me tekstni paragraflar bo'yicha ajratish
    about_paragraphs = profile.about_me.split('\n\n') if profile.about_me else []
    
    context = {
        'profile': profile,
        'services': services,
        'testimonials': testimonials,
        'clients': clients,
        'about_paragraphs': about_paragraphs,
        'current_page': 'about'
    }
    return render(request, 'about.html', context)


def resume_view(request):
    """Resume sahifasi uchun view"""
    profile = get_profile()
    educations = Education.objects.all()
    experiences = Experience.objects.all()
    skills = Skill.objects.all()
    
    context = {
        'profile': profile,
        'educations': educations,
        'experiences': experiences,
        'skills': skills,
        'current_page': 'resume'
    }
    return render(request, 'resume.html', context)


def portfolio_view(request):
    """Portfolio sahifasi uchun view"""
    profile = get_profile()
    projects = Project.objects.filter(is_active=True)
    
    context = {
        'profile': profile,
        'projects': projects,
        'current_page': 'portfolio'
    }
    return render(request, 'portfolio.html', context)


def blog_view(request):
    """Blog sahifasi uchun view"""
    profile = get_profile()
    blog_posts = BlogPost.objects.filter(is_published=True)
    
    context = {
        'profile': profile,
        'blog_posts': blog_posts,
        'current_page': 'blog'
    }
    return render(request, 'blog.html', context)


# views.py fayliga qo'shimcha
from .forms import ContactForm

def contact_view(request):
    """Contact sahifasi uchun view"""
    profile = get_profile()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            fullname = form.cleaned_data['fullname']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            try:
                # Email jo'natish
                subject = f'Portfolio Contact Form - {fullname}'
                email_message = f"""
                Yangi xabar portfolio saytidan:
                
                Ism: {fullname}
                Email: {email}
                
                Xabar:
                {message}
                """
                
                send_mail(
                    subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [profile.email],
                    fail_silently=False,
                )
                
                messages.success(request, 'Xabar muvaffaqiyatli jo\'natildi! Tez orada sizga javob beramiz.')
                return HttpResponseRedirect(reverse('contact'))
                
            except Exception as e:
                messages.error(request, f'Xatolik yuz berdi. Iltimos qayta urinib ko\'ring. Xato: {str(e)}')
        else:
            messages.error(request, 'Iltimos barcha maydonlarni to\'g\'ri to\'ldiring.')
    else:
        form = ContactForm()
    
    context = {
        'profile': profile,
        'current_page': 'contact',
        'form': form
    }
    return render(request, 'contact.html', context)

# views.py
def blog_detail_view(request, slug):
    """
    Blog detali sahifasi - slug bilan
    """
    blog = get_object_or_404(BlogPost, slug=slug, is_published=True)
    profile = get_profile()
    
    # ID bo'yicha tartiblash - eng ishonchli usul
    # Keyingi post (ID katta - yangi post)
    next_blog = BlogPost.objects.filter(
        id__gt=blog.id,
        is_published=True
    ).order_by('id').first()
    
    # Oldingi post (ID kichik - eski post)
    previous_blog = BlogPost.objects.filter(
        id__lt=blog.id,
        is_published=True
    ).order_by('-id').first()
    
    context = {
        'profile': profile,
        'current_page': 'blog',
        'blog': blog,
        'next_blog': next_blog,
        'previous_blog': previous_blog,
    }
    return render(request, 'blog_detail.html', context)