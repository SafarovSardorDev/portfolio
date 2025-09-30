from django.contrib import admin
from .models import (
    Profile, SocialLink, Service, Testimonial, Client,
    Education, Experience, Skill, Project, BlogPost
)

class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email', 'phone', 'created_at']
    fields = ['name', 'title', 'avatar', 'email', 'phone', 'birthday', 'location', 'about_me']
    inlines = [SocialLinkInline]




@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    list_filter = ['title']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_position', 'date', 'is_active']
    list_filter = ['is_active', 'date']
    search_fields = ['client_name', 'content']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'website']
    search_fields = ['name']


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['institution', 'degree', 'period', 'order']
    list_editable = ['order']
    ordering = ['-order']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['position', 'company', 'period', 'order']
    list_editable = ['order']
    ordering = ['-order']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'percentage', 'category', 'order']
    list_editable = ['percentage', 'order']
    list_filter = ['category']
    ordering = ['order']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_active', 'order']
    list_filter = ['category', 'is_active']
    list_editable = ['is_active', 'order']
    search_fields = ['title', 'description']
    ordering = ['order']


# admin.py - BlogPostAdmin ga slug qo'shamiz
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'category', 'published_date', 'is_published']  # slug qo'shildi
    list_filter = ['category', 'is_published', 'published_date']
    search_fields = ['title', 'content', 'slug']  # slug qo'shildi
    list_editable = ['is_published']
    prepopulated_fields = {'slug': ('title',)}  # Slugni avtomatik to'ldirish
    date_hierarchy = 'published_date'