import json
import urllib.request
import urllib.error
from urllib.parse import urlparse

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.templatetags.static import static

from .models import Profile, Project, Skill, ContactMessage, Testimonial, ChatMessage
from .forms import ProfileForm, ProjectForm, SkillForm
from .services import send_contact_email, GeminiService, GitHubService


def splash(request):
    """Vue pour la page de chargement doctorale (splash screen)."""
    return render(request, 'home/splash.html')


def index(request):
    profile, created = Profile.objects.get_or_create(
        pk=1,
        defaults={
            'full_name': 'DELAMOU Samaké',
            'title': 'Étudiant en Informatique L3 | Passionné Data Analyst',
            'bio': 'Étudiant en Licence 3 d\'Informatique à l\'Université de Labé, passionné par l\'analyse de données et l\'extraction d\'insights pertinents. Je développe mes compétences en Data Analysis pour aider les entreprises à prendre des décisions éclairées grâce à la data.',
            'email': 'samakedelamou858@gmail.com',
            'phone': '+223 629403019',
            'location': 'Labé, Guinée',
            'years_experience': 1,
            'projects_count': 15,
            'clients_count': 3,
            'profile_image': 'delamou.jpg',
        }
    )

    projects = Project.objects.filter(is_visible=True).order_by('-created_at')[:6]
    skills_analysis = Skill.objects.filter(category='analysis')
    skills_programming = Skill.objects.filter(category='programming')
    skills_database = Skill.objects.filter(category='database')
    skills_bi = Skill.objects.filter(category='bi')
    testimonials = Testimonial.objects.filter(featured=True)[:3]

    def resolve_image_url(value, use_fallback=False):
        if not value or 'via.placeholder.com' in value:
            return 'https://source.unsplash.com/featured/?artificial-intelligence,data' if use_fallback else static('home/placeholder.svg')
        if not urlparse(value).scheme:
            # Vérifier si l'image est dans media ou static
            import os
            from django.conf import settings
            if os.path.exists(os.path.join(settings.MEDIA_ROOT, value)):
                return settings.MEDIA_URL + value
            return static('home/' + value)
        return value

    profile_image_url = resolve_image_url(profile.profile_image, use_fallback=True)
    for project in projects:
        project.image = resolve_image_url(project.image)
    for testimonial in testimonials:
        testimonial.client_image = resolve_image_url(testimonial.client_image)

    project_count = Project.objects.count()

    # Statistiques GitHub
    github_service = GitHubService()
    github_stats = github_service.get_user_stats()
    github_repos = github_service.get_repositories(limit=3)

    context = {
        'profile': profile,
        'projects': projects,
        'skills_analysis': skills_analysis,
        'skills_programming': skills_programming,
        'skills_database': skills_database,
        'skills_bi': skills_bi,
        'testimonials': testimonials,
        'profile_image_url': profile_image_url,
        'project_count': project_count,
        'github_stats': github_stats,
        'github_repos': github_repos,
    }

    return render(request, 'home/index.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )

            try:
                send_contact_email(
                    name=name,
                    sender_email=email,
                    subject=subject,
                    message=message,
                )
                messages.success(request, 'Message envoyé avec succès ! Je vous répondrai dès que possible.')
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"ERREUR CRITIQUE SMTP : {str(e)}", exc_info=True)
                messages.error(request, "Désolé, une erreur technique est survenue lors de l'envoi. Veuillez réessayer plus tard.")
        else:
            messages.error(request, 'Veuillez remplir tous les champs.')

        return redirect('home')

    return redirect('home')


@require_POST
def chat_api(request):
    """Point d'entrée de l'API pour le chatbot."""
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'error': 'Format JSON invalide.'}, status=400)

    user_message = payload.get('message', '').strip()
    if not user_message:
        return JsonResponse({'error': 'Le message ne peut pas être vide.'}, status=400)

    # Sauvegarder le message du visiteur
    ChatMessage.objects.create(sender='visitor', message=user_message)

    # Utiliser le service Gemini
    gemini = GeminiService()
    answer = gemini.generate_response(user_message)

    # Sauvegarder la réponse de l'IA
    ChatMessage.objects.create(sender='bot', message=answer)

    return JsonResponse({'answer': answer})


def projects_list(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'home/projects.html', {'projects': projects})


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'home/project_detail.html', {'project': project})


@login_required
def dashboard(request):
    project_count = Project.objects.count()
    skill_count = Skill.objects.count()
    unread_messages = ContactMessage.objects.filter(is_read=False).count()
    latest_projects = Project.objects.all().order_by('-created_at')[:5]
    
    # Calcul des KPIs réels ou simulés de manière cohérente
    featured_projects = Project.objects.filter(featured=True).count()
    total_messages = ContactMessage.objects.count()
    
    # Simulation de croissance par rapport au mois dernier (exemple)
    growth_projects = "+12%" if project_count > 0 else "0%"
    growth_skills = "+8%" if skill_count > 0 else "0%"
    
    # Calcul de l'activité réelle (nombre de projets par jour sur les 7 derniers jours)
    from django.utils import timezone
    from datetime import timedelta
    
    end_date = timezone.now()
    start_date = end_date - timedelta(days=6)
    
    daily_activity = []
    days_labels = []
    days_map = {0: 'Lun', 1: 'Mar', 2: 'Mer', 3: 'Jeu', 4: 'Ven', 5: 'Sam', 6: 'Dim'}
    
    for i in range(7):
        current_day = start_date + timedelta(days=i)
        count = Project.objects.filter(
            created_at__year=current_day.year,
            created_at__month=current_day.month,
            created_at__day=current_day.day
        ).count()
        daily_activity.append(count)
        days_labels.append(days_map[current_day.weekday()])
    
    context = {
        'project_count': project_count,
        'skill_count': skill_count,
        'unread_messages': unread_messages,
        'latest_projects': latest_projects,
        'featured_count': featured_projects,
        'total_messages': total_messages,
        'growth_projects': growth_projects,
        'growth_skills': growth_skills,
        'daily_activity': json.dumps(daily_activity),
        'days_labels': json.dumps(days_labels),
    }
    return render(request, 'home/dashboard.html', context)

@login_required
def manage_projects(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Projet ajouté avec succès !")
            return redirect('dashboard_projects')
        else:
            messages.error(request, "Erreur lors de l'ajout du projet. Veuillez vérifier le formulaire.")
    else:
        form = ProjectForm()

    projects = Project.objects.all().order_by('-created_at')
    featured_count = projects.filter(featured=True).count()
    
    return render(request, 'home/project_manage.html', {
        'projects': projects,
        'featured_count': featured_count,
        'form': form
    })

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Projet mis à jour avec succès !")
            return redirect('dashboard_projects')
        else:
            messages.error(request, "Erreur lors de la modification du projet. Veuillez vérifier le formulaire.")
    else:
        form = ProjectForm(instance=project)
    return render(request, 'home/project_form.html', {'form': form, 'project': project})

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Projet supprimé avec succès !")
        return redirect('dashboard_projects')
    return render(request, 'home/project_confirm_delete.html', {'project': project})


@login_required
def toggle_project_visibility(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.is_visible = not project.is_visible
    project.save()
    status = "activée" if project.is_visible else "désactivée"
    messages.success(request, f"Visibilité du projet {status} !")
    return redirect('dashboard_projects')

@login_required
def site_settings(request):
    profile = Profile.objects.first()
    if not profile:
        profile = Profile.objects.create(full_name="DELAMOU Samaké")
        
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès !")
            return redirect('dashboard_settings')
        else:
            messages.error(request, "Erreur lors de la mise à jour du profil. Veuillez vérifier les champs.")
    else:
        form = ProfileForm(instance=profile)
        
    return render(request, 'home/site_settings.html', {'form': form})


@login_required
def manage_skills(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Compétence ajoutée avec succès !")
            return redirect('dashboard_skills')
        else:
            messages.error(request, "Erreur lors de l'ajout de la compétence.")
    else:
        form = SkillForm()

    skills = Skill.objects.all().order_by('category', 'name')
    return render(request, 'home/skill_manage.html', {
        'skills': skills,
        'form': form
    })


@login_required
def edit_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Compétence mise à jour !")
            return redirect('dashboard_skills')
    else:
        form = SkillForm(instance=skill)
    return render(request, 'home/skill_form.html', {'form': form, 'skill': skill})


@login_required
def delete_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, "Compétence supprimée !")
        return redirect('dashboard_skills')
    return render(request, 'home/skill_confirm_delete.html', {'skill': skill})
