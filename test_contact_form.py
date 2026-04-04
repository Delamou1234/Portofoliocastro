"""
Script pour tester l'envoi d'email via le formulaire de contact.
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

from home.services import send_contact_email

def test_contact_email():
    """Teste l'envoi d'un email de contact."""
    print("=" * 50)
    print("TEST DU FORMULAIRE DE CONTACT")
    print("=" * 50)
    
    # Simuler les donnees du formulaire
    test_data = {
        'name': 'Visiteur Test',
        'sender_email': 'test@example.com',
        'subject': 'Test du formulaire de contact',
        'message': 'Ceci est un message de test envoye depuis le formulaire de contact du portfolio.'
    }
    
    print(f"\nDonnees du formulaire:")
    print(f"  Nom: {test_data['name']}")
    print(f"  Email: {test_data['sender_email']}")
    print(f"  Sujet: {test_data['subject']}")
    print(f"  Message: {test_data['message'][:50]}...")
    
    try:
        print("\nEnvoi de l'email...")
        send_contact_email(
            name=test_data['name'],
            sender_email=test_data['sender_email'],
            subject=test_data['subject'],
            message=test_data['message'],
        )
        print("\nSUCCES! Email envoye avec succes!")
        print("Verifiez la boite de reception: samakedelamou858@gmail.com")
        return True
    except Exception as e:
        print(f"\nERREUR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_contact_email()
