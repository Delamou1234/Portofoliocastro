#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de test du chatbot avec questions reelles
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Portofolio.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from home.services import GeminiService

print("=" * 70)
print("TEST DU CHATBOT - GEMINI 2.5 FLASH")
print("Verification de la qualite des reponses sur DELAMOU Samake")
print("=" * 70)

# Initialiser le service
gemini = GeminiService()

# Questions de test
questions = [
    "Qui est DELAMOU Samake ?",
    "Quelles sont ses competences ?",
    "Comment puis-je le contacter ?",
    "Quels services propose-t-il ?",
    "Combien d'annees d'experience a-t-il ?",
]

print(f"\nModele utilise: {gemini.api_model}")
print(f"API configuree: {'Oui' if gemini.is_configured() else 'Non'}")
print("\n" + "=" * 70)

# Poser chaque question
for i, question in enumerate(questions, 1):
    print(f"\n[QUESTION {i}] {question}")
    print("-" * 70)
    
    reponse = gemini.generate_response(question)
    
    print(f"REPONSE:\n{reponse}")
    print("=" * 70)

print("\n[TEST TERMINE]")
print("Verifiez que les reponses sont:")
print("  1. Professionnelles et courtoises")
print("  2. Precises sur les informations de DELAMOU Samake")
print("  3. En francais correct")
print("  4. Utiles pour les visiteurs")
