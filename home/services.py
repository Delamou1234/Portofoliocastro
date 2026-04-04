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
            projects_info += f"- {p.title}: {p.description} (Tech: {p.technologies})\n"
            
        skills_info = ""
        for s in skills:
            skills_info += f"- {s.name} ({s.get_category_display()})\n"
        
        bio_text = profile.bio if profile else "Passionné par l'analyse de données."
        location_text = profile.location if profile else "Labé, Guinée"
        email_text = profile.email if profile else "samakedelamou858@gmail.com"
        phone_text = profile.phone if profile else "+223 629403019"
        
        prompt = (
            "Tu es l'assistant virtuel intelligent et chaleureux de DELAMOU Samaké. "
            "Ton but est de fournir le maximum d'informations pertinentes aux visiteurs sur son profil, ses compétences et ses réalisations.\n\n"
            "IDENTITÉ ET CONTACT :\n"
            f"- Nom complet : {profile.full_name if profile else 'DELAMOU Samaké'}\n"
            f"- Titre : {profile.title if profile else 'Data Analyst'}\n"
            f"- Bio : {bio_text}\n"
            f"- Localisation : {location_text}\n"
            f"- Email : {email_text}\n"
            f"- Téléphone/WhatsApp : {phone_text}\n"
            f"- Expérience : {profile.years_experience if profile else '1'} an(s)\n\n"
            "COMPÉTENCES TECHNIQUES :\n"
            f"{skills_info if skills_info else '- Python, SQL, Power BI, Tableau, Analyse de données'}\n\n"
            "PROJETS RÉALISÉS :\n"
            f"{projects_info if projects_info else '- Divers projets en Data Analysis et Visualisation'}\n\n"
            "RÈGLES DE RÉPONSE :\n"
            "1. Sois très précis et donne des détails basés sur les infos ci-dessus.\n"
            "2. Si un visiteur pose une question sur un projet, explique ce qu'il a fait.\n"
            "3. Encourage toujours le visiteur à contacter Samaké via le formulaire ou WhatsApp.\n"
            "4. Réponds toujours en français de manière professionnelle mais accessible."
        )
        return prompt

    def generate_response(self, user_message):
        """Envoie une requête à l'API Gemini et retourne la réponse texte."""
        if not self.is_configured():
            return (
                "Bonjour ! Je suis l'assistant virtuel de DELAMOU Samaké. "
                "Le service intelligent n'est pas encore activé. "
                "Vous pouvez contacter DELAMOU directement à samakedelamou858@gmail.com."
            )

        full_url = f"{self.api_url}/{self.api_model}:generateContent?key={self.api_key}"
        
        request_payload = {
            'contents': [
                {
                    'role': 'user',
                    'parts': [{'text': f"{self.get_system_prompt()}\n\nQuestion du visiteur: {user_message}"}]
                }
            ],
            'generationConfig': {
                'temperature': 0.7,
                'topK': 40,
                'topP': 0.95,
                'maxOutputTokens': 1024,
            }
        }

        try:
            data = json.dumps(request_payload).encode('utf-8')
            req = urllib.request.Request(
                full_url,
                data=data,
                headers={'Content-Type': 'application/json'},
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                # Vérifier si l'API retourne une erreur dans le corps de la réponse
                if 'error' in result:
                    error_info = result['error']
                    error_code = error_info.get('code', 'unknown')
                    error_message = error_info.get('message', 'Erreur inconnue')
                    logger.error(f"Erreur API Gemini (code {error_code}): {error_message}")
                    
                    if error_code == 403:
                        return (
                            "Bonjour ! Je suis l'assistant virtuel de DELAMOU Samaké. "
                            "Le service intelligent n'est pas correctement configuré. "
                            "Veuillez contacter DELAMOU à samakedelamou858@gmail.com."
                        )
                    return "Une erreur est survenue lors de la communication avec l'IA. Veuillez réessayer."
                
                return self._parse_response(result)
                
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else ''
            logger.error(f"Erreur HTTP Gemini API: {e.code} - {error_body}")
            if e.code == 403:
                return (
                    "Bonjour ! Je suis l'assistant virtuel de DELAMOU Samaké. "
                    "Le service intelligent n'est pas correctement configuré. "
                    "Veuillez contacter DELAMOU à samakedelamou858@gmail.com."
                )
            return "Une erreur est survenue lors de la communication avec l'IA. Veuillez réessayer."
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

def send_contact_email(name: str, sender_email: str, subject: str, message: str) -> None:
    """Envoie un message de contact au propriétaire du portfolio."""
    email_subject = f"[Portfolio] {subject} - {name}"
    email_body = (
        f"Nouveau message envoyé depuis le portfolio de DELAMOU Samaké.\n\n"
        f"Nom : {name}\n"
        f"Email : {sender_email}\n"
        f"Objet : {subject}\n\n"
        f"Message :\n{message}\n"
    )

    try:
        # Essayer de rendre le template HTML
        try:
            html_message = render_to_string('home/contact_email.html', {
                'name': name,
                'sender_email': sender_email,
                'subject': subject,
                'message': message,
            })
        except Exception as e:
            logger.warning(f"Erreur lors du rendu du template HTML: {str(e)}")
            html_message = None

        # Envoi de l'email
        send_mail(
            subject=email_subject,
            message=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)],
            fail_silently=False,
            html_message=html_message,
        )
        logger.info(f"Email envoyé avec succès de {sender_email}")
    except Exception as e:
        logger.error(f"Erreur fatale dans send_contact_email: {str(e)}")
        raise e
