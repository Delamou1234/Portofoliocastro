
import os
import django
from django.conf import settings
from django.core.mail import send_mail

# Configuration minimale de Django pour le script
if not settings.configured:
    settings.configure(
        DEBUG=True,
        EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
        EMAIL_HOST='smtp.gmail.com',
        EMAIL_PORT=587,
        EMAIL_USE_TLS=True,
        EMAIL_HOST_USER='samakedelamou858@gmail.com',
        EMAIL_HOST_PASSWORD='dwzv lvzs gsde skqx', # Mot de passe d'application récupéré précédemment
        DEFAULT_FROM_EMAIL='samakedelamou858@gmail.com',
    )
    django.setup()

def test_send():
    print("Tentative d'envoi d'email de test...")
    try:
        send_mail(
            'Test Portfolio SMTP',
            'Ceci est un test de configuration SMTP.',
            settings.EMAIL_HOST_USER,
            ['samakedelamou858@gmail.com'],
            fail_silently=False,
        )
        print("SUCCÈS : L'email a été envoyé !")
    except Exception as e:
        print(f"ERREUR : {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_send()
