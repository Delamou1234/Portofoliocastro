#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de test pour verifier la connexion a l'API Gemini
"""
import os
import sys
import django
import json
import urllib.request
import urllib.error

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Portofolio.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.conf import settings

print("=" * 60)
print("TEST DE L'API GEMINI")
print("=" * 60)

# Verifier la configuration
print("\nConfiguration actuelle :")
print(f"  GEMINI_API_KEY: {settings.GEMINI_API_KEY[:20]}..." if settings.GEMINI_API_KEY else "  GEMINI_API_KEY: NON DEFINIE [ERREUR]")
print(f"  GEMINI_API_URL: {settings.GEMINI_API_URL}")
print(f"  GEMINI_API_MODEL: {settings.GEMINI_API_MODEL}")

# Verifier si la cle API est definie
if not settings.GEMINI_API_KEY:
    print("\n[ERREUR] La cle API Gemini n'est pas definie !")
    print("   Verifiez votre fichier .env et assurez-vous qu'il contient :")
    print("   GEMINI_API_KEY=votre_cle_api")
    sys.exit(1)

# Verifier le format de la cle
if not settings.GEMINI_API_KEY.startswith('AIza'):
    print("\n[ATTENTION] La cle API ne semble pas avoir le bon format")
    print("   Les cles API Google commencent generalement par 'AIza'")
    print(f"   Votre cle commence par: {settings.GEMINI_API_KEY[:4]}")

# Tester la connexion a l'API
print("\nTest de connexion a l'API Gemini...")
print(f"   URL: {settings.GEMINI_API_URL}/{settings.GEMINI_API_MODEL}:generateContent")

test_message = "Bonjour, peux-tu dire 'Test reussi' en francais ?"

request_payload = {
    'contents': [
        {
            'role': 'user',
            'parts': [{'text': test_message}]
        }
    ],
    'generationConfig': {
        'temperature': 0.7,
        'topK': 40,
        'topP': 0.95,
        'maxOutputTokens': 100,
    }
}

try:
    full_url = f"{settings.GEMINI_API_URL}/{settings.GEMINI_API_MODEL}:generateContent?key={settings.GEMINI_API_KEY}"
    data = json.dumps(request_payload).encode('utf-8')
    
    req = urllib.request.Request(
        full_url,
        data=data,
        headers={'Content-Type': 'application/json'},
    )
    
    print("   Envoi de la requete...")
    with urllib.request.urlopen(req, timeout=30) as response:
        raw_response = json.loads(response.read().decode('utf-8'))
        
        print("\n[SUCCES] L'API Gemini repond correctement")
        print("\nReponse brute de l'API :")
        print(json.dumps(raw_response, indent=2, ensure_ascii=False))
        
        # Extraire le texte de la reponse
        if 'candidates' in raw_response and raw_response['candidates']:
            candidate = raw_response['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                for part in candidate['content']['parts']:
                    if 'text' in part:
                        print(f"\nReponse du modele: {part['text']}")
        
        print("\n" + "=" * 60)
        print("[TEST REUSSI] L'API Gemini fonctionne correctement !")
        print("=" * 60)
        
except urllib.error.HTTPError as e:
    print(f"\n[ERREUR HTTP {e.code}]")
    error_body = e.read().decode('utf-8') if e.fp else ''
    print(f"   Reponse: {error_body}")
    
    if e.code == 400:
        print("\nCauses possibles :")
        print("   - Format de requete incorrect")
        print("   - Modele non valide")
    elif e.code == 403:
        print("\nCauses possibles :")
        print("   - Cle API invalide ou expiree")
        print("   - API non activee pour ce projet Google Cloud")
        print("   - Quota depasse")
    elif e.code == 404:
        print("\nCauses possibles :")
        print("   - Modele non trouve")
        print("   - URL de l'API incorrecte")
        
except urllib.error.URLError as e:
    print(f"\n[ERREUR DE CONNEXION] {e.reason}")
    print("\nCauses possibles :")
    print("   - Pas de connexion internet")
    print("   - Pare-feu bloquant la connexion")
    print("   - Proxy non configure")
    
except Exception as e:
    print(f"\n[ERREUR INATTENDUE] {type(e).__name__}: {e}")

print("\n" + "=" * 60)
print("Si le test echoue, verifiez :")
print("   1. Votre fichier .env contient la bonne cle API")
print("   2. Vous avez redemarre le serveur Django")
print("   3. Votre cle API est active sur https://makersuite.google.com/")
print("=" * 60)
