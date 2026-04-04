#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour lister les modeles Gemini disponibles
"""
import os
import sys
import django
import json
import urllib.request
import urllib.error

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Portofolio.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.conf import settings

print("=" * 60)
print("LISTE DES MODELES GEMINI DISPONIBLES")
print("=" * 60)

if not settings.GEMINI_API_KEY:
    print("[ERREUR] Cle API non definie")
    sys.exit(1)

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={settings.GEMINI_API_KEY}"

try:
    req = urllib.request.Request(url, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.loads(response.read().decode('utf-8'))
        
        print("\nModeles avec generateContent :\n")
        if 'models' in data:
            for model in data['models']:
                name = model.get('name', 'N/A')
                display_name = model.get('displayName', 'N/A')
                methods = model.get('supportedGenerationMethods', [])
                if 'generateContent' in methods:
                    print(f"  - {name.replace('models/', '')}")
                    print(f"    Nom: {display_name}")
                    print(f"    Methodes: {', '.join(methods)}")
                    print()
        else:
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
except Exception as e:
    print(f"[ERREUR] {e}")
