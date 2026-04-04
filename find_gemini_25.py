#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour trouver le modele Gemini 2.5 Flash exact
"""
import os
import sys
import django
import json
import urllib.request

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Portofolio.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.conf import settings

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={settings.GEMINI_API_KEY}"

try:
    req = urllib.request.Request(url, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.loads(response.read().decode('utf-8'))
        
        print("=" * 60)
        print("MODELES GEMINI 2.5 FLASH DISPONIBLES")
        print("=" * 60)
        
        if 'models' in data:
            found = False
            for model in data['models']:
                name = model.get('name', '')
                # Chercher tous les modeles avec "2.5" et "flash" dans le nom
                if '2.5' in name.lower() and 'flash' in name.lower():
                    found = True
                    display_name = model.get('displayName', 'N/A')
                    methods = model.get('supportedGenerationMethods', [])
                    print(f"\nModele: {name}")
                    print(f"  Nom d'affichage: {display_name}")
                    print(f"  Methodes: {', '.join(methods)}")
                    
            if not found:
                print("\nAucun modele '2.5 Flash' trouve!")
                print("\nModeles Flash disponibles:")
                for model in data['models']:
                    name = model.get('name', '')
                    if 'flash' in name.lower() and 'generateContent' in model.get('supportedGenerationMethods', []):
                        display_name = model.get('displayName', 'N/A')
                        print(f"  - {name.replace('models/', '')} ({display_name})")
                        
except Exception as e:
    print(f"[ERREUR] {e}")
