#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour mettre a jour le profil etudiant L3
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Portofolio.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from home.models import Profile

print("Mise a jour du profil DELAMOU Samake - Etudiant L3...")

try:
    profile = Profile.objects.get(pk=1)
    
    # Mise a jour des informations
    profile.full_name = 'DELAMOU Samaké'
    profile.title = 'Étudiant en Informatique L3 | Passionné Data Analyst'
    profile.bio = 'Étudiant en Licence 3 d\'Informatique à l\'Université de Labé, passionné par l\'analyse de données et l\'extraction d\'insights pertinents. Je développe mes compétences en Data Analysis pour aider les entreprises à prendre des décisions éclairées grâce à la data.'
    profile.email = 'samakedelamou858@gmail.com'
    profile.phone = '+223 629403019'
    profile.location = 'Labé, Guinée'
    profile.years_experience = 1
    profile.projects_count = 15
    profile.clients_count = 3
    profile.profile_image = 'delamou.jpg'
    
    profile.save()
    
    print(f"[SUCCES] Profil mis a jour:")
    print(f"   Nom: {profile.full_name}")
    print(f"   Titre: {profile.title}")
    print(f"   Location: {profile.location}")
    print(f"   Email: {profile.email}")
    print(f"   Experience: {profile.years_experience} an")
    print(f"   Projets: {profile.projects_count}")
    
except Profile.DoesNotExist:
    print("[ERREUR] Profil non trouve")
except Exception as e:
    print(f"[ERREUR] {e}")

print("\nLe profil reflète maintenant votre statut d'etudiant L3 a l'Universite de Labe!")
