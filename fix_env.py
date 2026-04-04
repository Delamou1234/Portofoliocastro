#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour corriger le fichier .env avec les bonnes valeurs Gemini API
"""

env_content = """GEMINI_API_KEY=AIzaSyBBbCaEDD11slzR62Xaci2ywh3vvEwDr9A
GEMINI_API_URL=https://generativelanguage.googleapis.com/v1beta/models
GEMINI_API_MODEL=gemini-2.5-flash-lite

# Configuration Email (optionnel)
EMAIL_HOST_USER=samakedelamou858@gmail.com
EMAIL_HOST_PASSWORD=
ADMIN_EMAIL=samakedelamou858@gmail.com
"""

env_path = ".env"

try:
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(env_content)
    print("[SUCCES] Fichier .env corrige avec succes !")
    print("\nContenu du fichier .env :")
    print("-" * 60)
    print(env_content)
    print("-" * 60)
    print("\nRedemarrez maintenant le serveur Django avec :")
    print("  python manage.py runserver")
except Exception as e:
    print(f"[ERREUR] Impossible de corriger le fichier .env: {e}")
