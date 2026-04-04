# 📊 Portfolio de DELAMOU Samaké

Bienvenue sur le dépôt de mon portfolio professionnel. Je suis un étudiant en Licence 3 d'Informatique à l'Université de Labé (Guinée), passionné par l'**Analyse de Données** et le **Développement Python**.

## 🚀 Fonctionnalités

-   **Dashboard d'Administration** : Gestion complète des projets, compétences et profil.
-   **Assistant IA (Gemini)** : Chatbot intelligent intégré pour répondre aux questions des visiteurs.
-   **Gestion de Projets** : Affichage dynamique des projets avec tags technologiques et liens (GitHub/Démo).
-   **Système de Compétences** : CRUD complet pour gérer les compétences par catégories.
-   **Formulaire de Contact** : Envoi automatique d'emails via SMTP Gmail.
-   **Sécurité** : Gestion robuste des secrets via variables d'environnement (`python-dotenv`).

## 🛠️ Stack Technique

-   **Backend** : Django 5.x (Python)
-   **Frontend** : HTML5, CSS3, JavaScript
-   **IA** : Google Gemini API (Modèle : gemini-2.5-flash-lite)
-   **Base de Données** : SQLite (Développement), PostgreSQL (Production ready)
-   **Email** : SMTP Gmail avec mot de passe d'application

## 📦 Installation et Configuration

### 1. Cloner le dépôt
```bash
git clone https://github.com/Delamou1234/DataAnalyst.git
cd DataAnalyst
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration des variables d'environnement
Copiez le fichier `.env.example` vers `.env` et remplissez vos informations :
```bash
cp .env.example .env
```
Assurez-vous de configurer les clés suivantes :
- `DJANGO_SECRET_KEY`
- `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD`
- `GEMINI_API_KEY`

### 5. Lancer les migrations
```bash
python manage.py migrate
```

### 6. Démarrer le serveur
```bash
python manage.py runserver
```

## 🛡️ Sécurité
Le projet est configuré pour ne **JAMAIS** exposer les fichiers sensibles (`.env`, `db.sqlite3`, scripts de test) sur GitHub grâce à un fichier `.gitignore` optimisé.

## 📧 Contact
- **Email** : samakedelamou858@gmail.com
- **LinkedIn** : [Profil LinkedIn](votre-lien-linkedin)
- **GitHub** : [Delamou1234](https://github.com/Delamou1234)

---
*Développé avec ❤️ par DELAMOU Samaké*
