"""
Script pour configurer les variables d'environnement email.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DOTENV_PATH = BASE_DIR / '.env'

# Configuration email
EMAIL_CONFIG = f"""# Configuration Email Gmail
EMAIL_HOST_USER=samakedelamou858@gmail.com
EMAIL_HOST_PASSWORD=dwzv lvzs gsde skqx

# Configuration API Gemini (à compléter avec votre clé)
GEMINI_API_KEY=
GEMINI_API_URL=https://generativelanguage.googleapis.com/v1beta/models
GEMINI_API_MODEL=gemini-2.0-flash

# Email admin
ADMIN_EMAIL=samakedelamou858@gmail.com
"""

def setup_env():
    """Crée ou met à jour le fichier .env avec la configuration email."""
    existing_content = ""
    
    # Lire le contenu existant si le fichier existe
    if DOTENV_PATH.exists():
        with DOTENV_PATH.open(encoding='utf-8') as f:
            existing_content = f.read()
    
    # Parser les variables existantes
    existing_vars = {}
    for line in existing_content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line:
            key, value = line.split('=', 1)
            existing_vars[key.strip()] = value.strip().strip('"').strip("'")
    
    # Mettre à jour avec les nouvelles valeurs
    new_vars = {
        'EMAIL_HOST_USER': 'samakedelamou858@gmail.com',
        'EMAIL_HOST_PASSWORD': 'dwzv lvzs gsde skqx',
        'ADMIN_EMAIL': 'samakedelamou858@gmail.com',
    }
    
    # Garder les valeurs existantes pour Gemini si présentes
    if 'GEMINI_API_KEY' not in existing_vars:
        new_vars['GEMINI_API_KEY'] = ''
    if 'GEMINI_API_URL' not in existing_vars:
        new_vars['GEMINI_API_URL'] = 'https://generativelanguage.googleapis.com/v1beta/models'
    if 'GEMINI_API_MODEL' not in existing_vars:
        new_vars['GEMINI_API_MODEL'] = 'gemini-2.0-flash'
    
    existing_vars.update(new_vars)
    
    # Écrire le nouveau contenu
    with DOTENV_PATH.open('w', encoding='utf-8') as f:
        f.write("# Configuration du portfolio DELAMOU Samaké\n")
        f.write("# Généré automatiquement - NE PAS COMMITTER\n\n")
        
        f.write("# Email Gmail (mot de passe d'application)\n")
        f.write(f"EMAIL_HOST_USER={existing_vars.get('EMAIL_HOST_USER', '')}\n")
        f.write(f"EMAIL_HOST_PASSWORD={existing_vars.get('EMAIL_HOST_PASSWORD', '')}\n\n")
        
        f.write("# API Gemini\n")
        f.write(f"GEMINI_API_KEY={existing_vars.get('GEMINI_API_KEY', '')}\n")
        f.write(f"GEMINI_API_URL={existing_vars.get('GEMINI_API_URL', '')}\n")
        f.write(f"GEMINI_API_MODEL={existing_vars.get('GEMINI_API_MODEL', '')}\n\n")
        
        f.write("# Admin\n")
        f.write(f"ADMIN_EMAIL={existing_vars.get('ADMIN_EMAIL', '')}\n")
    
    print("Fichier .env configure avec succes!")
    print(f"   EMAIL_HOST_USER: {existing_vars.get('EMAIL_HOST_USER')}")
    print(f"   EMAIL_HOST_PASSWORD: {'****' + existing_vars.get('EMAIL_HOST_PASSWORD', '')[-4:]}")

if __name__ == '__main__':
    setup_env()
