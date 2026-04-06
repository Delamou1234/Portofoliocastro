import json
import urllib.request
import urllib.error
import logging
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

class GitHubService:
    """Service pour interagir avec l'API GitHub."""
    
    def __init__(self):
        self.username = getattr(settings, 'GITHUB_USERNAME', 'Delamou1234')
        self.token = getattr(settings, 'GITHUB_TOKEN', '')
        self.base_url = "https://api.github.com"
        self.headers = {'Accept': 'application/vnd.github.v3+json'}
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'

    def get_user_stats(self):
        """Récupère les statistiques globales de l'utilisateur."""
        try:
            response = requests.get(f"{self.base_url}/users/{self.username}", headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    'repos': data.get('public_repos', 0),
                    'followers': data.get('followers', 0),
                    'following': data.get('following', 0),
                }
            return None
        except Exception as e:
            logger.error(f"Erreur GitHub stats: {str(e)}")
            return None

    def get_repositories(self, limit=6):
        """Récupère les dépôts publics triés par mise à jour."""
        try:
            response = requests.get(
                f"{self.base_url}/users/{self.username}/repos?sort=updated&per_page={limit}",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            logger.error(f"Erreur GitHub repos: {str(e)}")
            return []

class GeminiService:
    """Service pour interagir avec l'API Gemini de Google."""
    
    def __init__(self):
        self.api_key = getattr(settings, 'GEMINI_API_KEY', '')
        self.api_url = getattr(settings, 'GEMINI_API_URL', 'https://generativelanguage.googleapis.com/v1beta/models')
        self.api_model = getattr(settings, 'GEMINI_API_MODEL', 'gemini-2.0-flash')
        
    def is_configured(self):
        """Vérifie si la clé API est présente."""
        return bool(self.api_key)

    def get_system_prompt(self):
        """Retourne le prompt système pour l'assistant avec le maximum d'informations."""
        from .models import Profile, Project, Skill
        profile = Profile.objects.first()
        projects = Project.objects.filter(is_visible=True)
        skills = Skill.objects.all()
        
        # Préparation des données dynamiques
        projects_info = ""
        for p in projects:
            projects_info += f"- {p.title}: {p.description} (Expertise: {p.technologies})\n"
            
        skills_info = ""
        for s in skills:
            skills_info += f"- {s.name} ({s.get_category_display()})\n"
        
        bio_text = profile.bio if profile else "Expert en Statistiques et IA."
        location_text = profile.location if profile else "Bénin"
        email_text = profile.email if profile else "castrohounmenou@gmail.com"
        phone_text = profile.phone if profile else "+229 XX XX XX XX"
        
        prompt = (
            f"Tu es l'assistant de recherche et consultant virtuel du {profile.full_name if profile else 'Dr. Eng. H. Castro'}. "
            "Ton rôle est d'assister les partenaires, chercheurs et clients potentiels en fournissant des informations précises sur ses travaux de recherche, ses publications et son expertise senior.\n\n"
            "PROFIL ACADÉMIQUE ET PROFESSIONNEL :\n"
            f"- Nom complet : {profile.full_name if profile else 'Dr. Eng. H. Castro'}\n"
            f"- Titre : {profile.title if profile else 'PhD in Statistics & Probability | AI Expert'}\n"
            f"- Expertise : {bio_text}\n"
            f"- Localisation : {location_text}\n"
            f"- Contact : {email_text} | {phone_text}\n"
            f"- Expérience : {profile.years_experience if profile else '15'}+ ans d'expertise terrain\n\n"
            "DOMAINES DE RECHERCHE :\n"
            f"{skills_info if skills_info else '- Modélisation Avancée, Biostatistique, IA, SIG'}\n\n"
            "PUBLICATIONS ET TRAVAUX :\n"
            f"{projects_info if projects_info else '- Plus de 50 publications internationales en santé et climat'}\n\n"
            "DIRECTIVES DE COMMUNICATION :\n"
            "1. Adopte un ton formel, professionnel et académique (utilise le 'Vous').\n"
            "2. Valorise l'impact social et environnemental des travaux du Docteur.\n"
            "3. Oriente les demandes de collaboration vers l'email direct ou le formulaire.\n"
            "4. Réponds toujours en français de manière concise et structurée."
        )
        return prompt

    def generate_response(self, user_message):
        """Envoie une requête à l'API Gemini et retourne la réponse texte."""
        if not self.is_configured():
            return (
                f"Bonjour. Je suis l'assistant du {Profile.objects.first().full_name if Profile.objects.first() else 'Dr. Eng. H. Castro'}. "
                "Le module d'intelligence artificielle est en cours de maintenance. "
                "Pour toute demande urgente ou collaboration, veuillez envoyer un courriel à castrohounmenou@gmail.com."
            )

        # Ensure model name is correct for the API endpoint
        model_name = self.api_model if self.api_model.startswith('models/') else f"models/{self.api_model}"
        url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={self.api_key}"
        
        request_payload = {
            'contents': [
                {
                    'parts': [{'text': f"{self.get_system_prompt()}\n\nQuestion du visiteur: {user_message}"}]
                }
            ],
            'generationConfig': {
                'temperature': 0.7,
                'maxOutputTokens': 1024,
            }
        }

        try:
            data = json.dumps(request_payload).encode('utf-8')
            req = urllib.request.Request(
                url,
                data=data,
                headers={'Content-Type': 'application/json'},
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                return self._parse_response(result)
                
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else ''
            logger.error(f"Erreur HTTP Gemini API: {e.code} - {error_body}")
            return "Une erreur de communication est survenue. Veuillez contacter le Dr. Castro directement via le formulaire."
        except Exception as e:
            logger.error(f"Erreur inattendue Gemini Service: {str(e)}")
            return "Désolé, je ne peux pas répondre pour le moment. Veuillez réessayer plus tard."

    def _parse_response(self, raw_response):
        """Extrait le texte de la réponse brute de Gemini."""
        try:
            if 'candidates' in raw_response and raw_response['candidates']:
                candidate = raw_response['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    parts = candidate['content']['parts']
                    return "".join([part.get('text', '') for part in parts if 'text' in part])
            return "Je n'ai pas pu générer de réponse intelligible."
        except Exception as e:
            logger.error(f"Erreur lors du parsing Gemini: {str(e)}")
            return "Erreur lors de la lecture de la réponse de l'IA."

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import get_connection

def send_contact_email(name: str, sender_email: str, subject: str, message: str) -> None:
    """Envoie un message de contact au propriétaire du portfolio avec une connexion robuste."""
    email_subject = f"[Portfolio] {subject} - {name}"
    email_body = (
        f"Nouveau message envoyé depuis le portfolio du Dr. Eng. H. Castro.\n\n"
        f"Nom : {name}\n"
        f"Email : {sender_email}\n"
        f"Objet : {subject}\n\n"
        f"Message :\n{message}\n"
    )

    try:
        # Rendu du template HTML
        html_content = None
        try:
            html_content = render_to_string('home/contact_email.html', {
                'name': name,
                'sender_email': sender_email,
                'subject': subject,
                'message': message,
            })
        except Exception as e:
            logger.warning(f"Template HTML non trouvé ou erreur de rendu: {str(e)}")

        recipient = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
        
        # Création de l'email
        email = EmailMultiAlternatives(
            subject=email_subject,
            body=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
            reply_to=[sender_email]
        )
        
        if html_content:
            email.attach_alternative(html_content, "text/html")

        # Utilisation d'une connexion explicite pour plus de stabilité
        connection = get_connection(fail_silently=False)
        email.connection = connection
        email.send()
        
        logger.info(f"Email envoyé avec succès de {sender_email}")
    except Exception as e:
        logger.error(f"Erreur fatale dans send_contact_email: {str(e)}")
        raise e
