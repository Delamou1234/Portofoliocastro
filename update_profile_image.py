#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour mettre a jour l'image du profil
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Portofolio.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from home.models import Profile

print("Mise a jour de l'image du profil DELAMOU Samake...")

try:
    profile = Profile.objects.get(pk=1)
    profile.profile_image = 'delamou.jpg'
    profile.save()
    
    print(f"[SUCCES] Image du profil mise a jour: {profile.profile_image}")
    print(f"   Nom: {profile.full_name}")
    print(f"   Image URL: {profile.profile_image}")
    
except Profile.DoesNotExist:
    print("[ERREUR] Profil non trouve")
except Exception as e:
    print(f"[ERREUR] {e}")

print("\nL'image delamou.jpg sera maintenant chargee depuis le dossier asset/")
