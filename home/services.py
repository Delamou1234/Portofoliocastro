import json
import urllib.request
import urllib.error
import logging
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

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
        """Retourne le prompt système pour l'assistant."""
        return (
            "Tu es un assistant virtuel professionnel qui renseigne les visiteurs sur DELAMOU Samaké, un étudiant passionné en Licence 3 d'Informatique à l'Université de Labé, Guinée. "
            "Tu dois répondre de manière claire, professionnelle et concise en français.\n\n"
            "Informations sur DELAMOU Samaké :\n"
            "- Étudiant en Licence 3 d'Informatique à l'Université de Labé\n"
            "- Passionné par l'analyse de données et le Data Analysis\n"
            "- Compétences en développement : Python, SQL, bases en Power BI et Tableau\n"
            "- Spécialisé en analyse de données, visualisation, apprentissage automatique\n"
            "- Email: samakedelamou858@gmail.com\n"
            "- Téléphone: +223 629403019\n"
            "- Localisation: Labé, Guinée\n"
            "- GitHub: https://github.com/Delamou1234\n"
            "- Réalise des projets académiques et personnels en data analysis\n"
            "- Cherche des opportunités de stage et de collaboration\n\n"
            "Réponds aux questions des visiteurs sur ses études, ses compétences, ses projets et comment collaborer avec lui."
        )

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
