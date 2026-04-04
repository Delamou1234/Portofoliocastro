from django.db import models

class Profile(models.Model):
    full_name = models.CharField(max_length=100, default="DELAMOU Samaké")
    title = models.CharField(max_length=100, default="Data Analyst")
    bio = models.TextField(default="Passionné par l'analyse de données et l'extraction d'insights pertinents pour aider les entreprises à prendre des décisions éclairées.")
    profile_image = models.URLField(default="delamou.jpg")
    email = models.EmailField(default="delamou.samake@email.com")
    phone = models.CharField(max_length=20, default="+223 XX XX XX XX")
    location = models.CharField(max_length=100, default="Conakry, Guinée")
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    kaggle = models.URLField(blank=True, null=True)
    years_experience = models.PositiveIntegerField(default=3)
    projects_count = models.PositiveIntegerField(default=50)
    clients_count = models.PositiveIntegerField(default=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('analysis', 'Analyse de données'),
        ('programming', 'Programmation'),
        ('database', 'Bases de données'),
        ('bi', 'Business Intelligence'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    icon = models.CharField(max_length=50, default="fas fa-chart-line")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.URLField(default="placeholder.svg")
    technologies = models.CharField(max_length=500, help_text="Technologies separated by commas")
    project_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True, help_text="Détermine si le projet est affiché sur la page d'accueil")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_technologies_list(self):
        return [tech.strip() for tech in self.technologies.split(',')]

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class ChatMessage(models.Model):
    SENDER_CHOICES = [
        ('visitor', 'Visiteur'),
        ('bot', 'Assistant'),
    ]

    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_sender_display()}: {self.message[:50]}"


class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_company = models.CharField(max_length=100, blank=True)
    client_image = models.URLField(default="placeholder.svg")
    message = models.TextField()
    rating = models.PositiveIntegerField(default=5)  # 1-5 stars
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial from {self.client_name}"
