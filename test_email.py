"""
Script pour tester la configuration email.
"""
import os
import sys
from pathlib import Path

# Configurer Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Charger les variables d'environnement
DOTENV_PATH = BASE_DIR / '.env'
if DOTENV_PATH.exists():
    with DOTENV_PATH.open(encoding='utf-8') as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Portofolio.settings')

import django
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email():
    """Teste l'envoi d'un email."""
    print("Configuration email:")
    print(f"  HOST: {settings.EMAIL_HOST}")
    print(f"  PORT: {settings.EMAIL_PORT}")
    print(f"  USER: {settings.EMAIL_HOST_USER}")
    print(f"  TLS: {settings.EMAIL_USE_TLS}")
    print(f"  PASSWORD: {'****' + settings.EMAIL_HOST_PASSWORD[-4:] if settings.EMAIL_HOST_PASSWORD else 'NON DEFINI'}")
    print()
    
    try:
        print("Envoi d'un email de test...")
        send_mail(
            '[Portfolio] Test de configuration email',
            'Ceci est un email de test depuis le portfolio de DELAMOU Samaké.\n\nSi vous recevez cet email, la configuration fonctionne correctement!',
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],  # Envoyer à soi-même
            fail_silently=False,
        )
        print("SUCCES: Email envoye avec succes!")
        print(f"Verifiez votre boite de reception: {settings.EMAIL_HOST_USER}")
        return True
    except Exception as e:
        print(f"ERREUR: {type(e).__name__}: {e}")
        return False

if __name__ == '__main__':
    test_email()
