from django.contrib import admin

from .models import Profile, Skill, Project, ContactMessage, Testimonial, ChatMessage


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'title', 'email', 'phone', 'location')
    search_fields = ('full_name', 'email', 'location')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'created_at', 'updated_at')
    search_fields = ('title', 'technologies')
    list_filter = ('featured',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('name', 'email', 'subject')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_company', 'rating', 'featured', 'created_at')
    list_filter = ('featured', 'rating')
    search_fields = ('client_name', 'client_company')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'created_at', 'message')
    list_filter = ('sender', 'created_at')
    search_fields = ('message',)
