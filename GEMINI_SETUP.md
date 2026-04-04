# 🤖 Configuration du Chatbot Gemini

## 📋 Étapes pour activer le chatbot intelligent

### 1. Obtenir une clé API Gemini (Gratuite)

1. **Allez sur Google AI Studio** : https://makersuite.google.com/app/apikey
2. **Connectez-vous** avec votre compte Google
3. **Cliquez sur "Create API key"**
4. **Sélectionnez un projet** ou créez-en un nouveau
5. **Copiez la clé API** générée

### 2. Configurer le fichier .env

Créez un fichier `.env` dans le dossier racine du projet (à côté de `manage.py`) :

```env
GEMINI_API_KEY=AIzaSy...votre_clé_api_complète_ici
GEMINI_API_URL=https://generativelanguage.googleapis.com/v1beta/models
GEMINI_API_MODEL=gemini-2.0-flash-exp
```

### 3. Redémarrer le serveur Django

```bash
python manage.py runserver
```

### 4. Tester le chatbot

1. Ouvrez votre portfolio : http://localhost:8000
2. Cliquez sur le bouton "Assistance DELAMOU" en bas à droite
3. Posez une question, par exemple :
   - "Quelles sont les compétences de DELAMOU ?"
   - "Comment puis-je le contacter ?"
   - "Quels projets a-t-il réalisés ?"

## 🔧 Modèles disponibles

- `gemini-2.5-flash-preview-05-20` - Dernier modèle Flash 2.5 (recommandé, très rapide)
- `gemini-2.0-flash-exp` - Modèle expérimental Flash 2.0
- `gemini-1.5-flash` - Modèle Flash 1.5 stable
- `gemini-1.5-pro` - Modèle Pro plus avancé mais plus lent

## 📝 Fonctionnalités du chatbot

Le chatbot peut répondre aux questions sur :

- ✅ Les compétences techniques (Python, SQL, Power BI, etc.)
- ✅ L'expérience professionnelle (3 ans, 50+ projets)
- ✅ Les coordonnées de contact (email, téléphone)
- ✅ Les services proposés (dashboards, analyses, ML)
- ✅ La localisation (Conakry, Guinée)

## 🐛 Dépannage

### Le chatbot ne répond pas

1. **Vérifiez que le fichier .env existe** et contient votre clé API
2. **Vérifiez le format de la clé** : elle doit commencer par `AIzaSy`
3. **Redémarrez le serveur Django** après avoir modifié .env
4. **Vérifiez les logs** dans la console Django pour les erreurs

### Erreur "API Key invalid"

- Assurez-vous d'avoir copié la clé complète
- Vérifiez que la clé n'a pas d'espaces au début ou à la fin
- Régénérez une nouvelle clé si nécessaire

### Erreur "Quota exceeded"

- L'API Gemini gratuite a des limites de requêtes
- Attendez quelques minutes avant de réessayer
- Considérez passer à un plan payant si nécessaire

## 💡 Exemples de questions à poser

- "Quelles sont les compétences de DELAMOU en data analyse ?"
- "Comment puis-je contacter DELAMOU pour un projet ?"
- "Quels types de dashboards peut-il créer ?"
- "A-t-il de l'expérience en machine learning ?"
- "Quels sont ses projets les plus récents ?"

## 🔒 Sécurité

⚠️ **Important** :
- Ne partagez jamais votre clé API publiquement
- Le fichier `.env` est exclu de Git via `.gitignore`
- En production, utilisez des variables d'environnement sécurisées
