from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Profile(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    birthday = models.DateField()
    location = models.CharField(max_length=100)
    about_me = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SocialLink(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='social_links')
    name = models.CharField(max_length=50)
    url = models.URLField()
    icon_class = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.profile.name} - {self.name}"

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='services/', blank=True, null=True)
    icon_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_position = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    content = models.TextField()
    date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.client_name

class Client(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='clients/', blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    period = models.CharField(max_length=50)
    description = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['-order']

    def __str__(self):
        return f"{self.degree} at {self.institution}"

class Experience(models.Model):
    position = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    period = models.CharField(max_length=50)
    description = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['-order']

    def __str__(self):
        return f"{self.position} at {self.company}"

class Skill(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.IntegerField()
    category = models.CharField(max_length=50, default='general')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Project(models.Model):
    PROJECT_CATEGORIES = [
        ('web-design', 'Web Design'),
        ('applications', 'Applications'),
        ('web-development', 'Web Development'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=PROJECT_CATEGORIES)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    project_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title



class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)  # Yangi field
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=300)
    published_date = models.DateField(default=timezone.now)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

# Slugni avtomatik yaratish uchun signal
@receiver(pre_save, sender=BlogPost)
def create_blog_slug(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.title)
        slug = base_slug
        counter = 1
        while BlogPost.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        instance.slug = slug