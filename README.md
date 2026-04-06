# 🎓 Portfolio Doctoral - Dr. Eng. H. Castro

Bienvenue sur le dépôt officiel du portfolio professionnel et académique du **Dr. Eng. H. Castro**. Ce projet est une plateforme de présentation de haut niveau dédiée à l'expertise en Statistiques, Intelligence Artificielle, Santé Publique et Changement Climatique.

## 👤 Profil de l'Expert

**PhD in Statistics & Probability | AI & Machine Learning Expert**
*Senior Consultant in Public Health, Agriculture, Climate Change & Data Science*

- **Expertise Terrain** : 15+ ans d'expérience internationale.
- **Recherche** : 50+ Publications scientifiques et 20+ Certifications internationales.
- **Distinction** : World Top Scientist 2024 (Biostatistique) & Best Researcher Award 2025.

## 🚀 Fonctionnalités Clés

- **Dashboard de Recherche** : Interface d'administration personnalisée pour la gestion des publications et des expertises académiques.
- **Secrétariat Virtuel (IA)** : Assistant intelligent propulsé par **Gemini 2.5 Flash**, configuré avec une persona doctorale pour orienter les partenaires et clients.
- **Design Doctoral** : Esthétique sobre et prestigieuse avec typographie serif et système de thèmes (Clair/Sombre).
- **Gestion des Travaux** : Vitrine dynamique des publications de recherche et des interventions stratégiques.
- **Communication Sécurisée** : Formulaire de contact direct configuré pour l'adresse officielle de l'expert.

## 🛠️ Stack Technique

- **Framework** : Django 4.2 (Python 3.11)
- **Interface** : HTML5, CSS3 (Variables dynamiques), JavaScript ES6
- **IA** : Google Gemini API (gemini-2.5-flash)
- **Base de Données** : SQLite (développement) / PostgreSQL (production)
- **Déploiement** : Render avec WhiteNoise pour les fichiers statiques

---

## 🚀 DÉPLOIEMENT SUR RENDER

### Prérequis
1. Compte sur [Render](https://render.com)
2. Compte GitHub avec ce repository
3. Clé API Gemini (optionnel, pour l'assistant AI)
4. Compte Gmail avec mot de passe d'application (pour les emails)

### Variables d'environnement à configurer dans Render

| Variable | Description | Obligatoire |
|----------|-------------|-------------|
| `DJANGO_SECRET_KEY` | Clé secrète Django (générée automatiquement) | ✅ |
| `DJANGO_DEBUG` | `False` en production | ✅ |
| `DJANGO_ALLOWED_HOSTS` | `.onrender.com` | ✅ |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://votre-app.onrender.com` | ✅ |
| `DATABASE_URL` | URL PostgreSQL (auto-configuré par Render) | ✅ |
| `GEMINI_API_KEY` | Clé API Gemini | ❌ |
| `EMAIL_HOST_USER` | Email Gmail | ❌ |
| `EMAIL_HOST_PASSWORD` | Mot de passe d'application Gmail | ❌ |

### Étapes de déploiement

1. **Connecter le repository** : Dans Render, créez un nouveau Web Service et connectez votre repo GitHub
2. **Configuration automatique** : Render détectera le fichier `render.yaml`
3. **Base de données** : Créez une base de données PostgreSQL dans Render et liez-la au web service
4. **Variables d'environnement** : Configurez les variables dans le dashboard Render
5. **Déployer** : Cliquez sur "Apply" pour lancer le déploiement

---

## 📦 Installation Locale

### 1. Cloner le dépôt
```bash
git clone https://github.com/Delamou1234/castroHounmenou.git
cd castroHounmenou
```

### 2. Environnement Virtuel
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 3. Dépendances
```bash
pip install -r requirements.txt
```

### 4. Variables d'Environnement
Créez un fichier `.env` à la racine (copiez `.env.example`) :
```env
DJANGO_SECRET_KEY=votre_cle_secrete
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
GEMINI_API_KEY=votre_cle_gemini
EMAIL_HOST_USER=votre_email@gmail.com
EMAIL_HOST_PASSWORD=votre_mot_de_passe_app
ADMIN_EMAIL=votre_email@gmail.com
```

### 5. Initialisation
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 📁 Structure du Projet

```
Castro/
├── Portofolio/          # Configuration Django
│   ├── settings.py      # Paramètres (variables d'env)
│   ├── urls.py          # URLs principales
│   └── wsgi.py          # WSGI application
├── home/                # Application principale
│   ├── templates/       # Templates HTML
│   ├── static/          # Fichiers statiques
│   ├── models.py        # Modèles de données
│   └── views.py         # Vues
├── media/               # Fichiers uploadés
├── .env.example         # Exemple de configuration
├── requirements.txt     # Dépendances Python
├── render.yaml          # Configuration Render
├── build.sh             # Script de build Render
└── manage.py            # Script Django
```

---

## 🔒 Sécurité

- ✅ Variables d'environnement pour toutes les données sensibles
- ✅ `DEBUG=False` en production
- ✅ HTTPS forcé en production
- ✅ Cookies sécurisés (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE)
- ✅ CSRF protection avec trusted origins
- ✅ Fichiers statiques servis par WhiteNoise

---

## 📧 Configuration Email (Gmail)

1. Activez l'authentification à 2 facteurs sur votre compte Gmail
2. Générez un mot de passe d'application : https://myaccount.google.com/apppasswords
3. Utilisez ce mot de passe pour `EMAIL_HOST_PASSWORD`

---

## 🤖 Assistant AI (Gemini)

1. Obtenez une clé API sur [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Configurez `GEMINI_API_KEY` dans vos variables d'environnement

---

## 📞 Contact & Réseaux

- **Email** : [castrohounmenou@gmail.com](mailto:castrohounmenou@gmail.com)
- **WhatsApp** : +229 95 30 66 12
- **GitHub** : [castro2026](https://github.com/castro2026)
- **LinkedIn** : [Dr. Eng. H. Castro](https://www.linkedin.com/in/castro-g-hounmenou-048aa56b/)

---
*Propulsé par l'excellence académique et l'innovation technologique.*
