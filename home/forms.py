from django import forms

from .models import Profile, Project


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'full_name',
            'title',
            'bio',
            'profile_image',
            'email',
            'phone',
            'location',
            'linkedin',
            'github',
            'twitter',
            'kaggle',
            'years_experience',
            'projects_count',
            'clients_count',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'description',
            'image',
            'technologies',
            'project_url',
            'github_url',
            'featured',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
