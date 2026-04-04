from django import forms

from .models import Profile, Project, Skill


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
            'is_visible',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'category', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ex: Python, Tableau...'}),
            'icon': forms.TextInput(attrs={'placeholder': 'Ex: fab fa-python...'}),
        }
