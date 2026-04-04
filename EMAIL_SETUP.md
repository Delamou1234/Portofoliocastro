# 📧 Configuration du Service d'Envoi d'Emails

## 📋 Configuration Gmail pour Django

### 1. Activer la validation en deux étapes (2FA)

1. **Allez sur votre compte Google** : https://myaccount.google.com/
2. **Sécurité** → **Validation en deux étapes**
3. **Activez-la** si ce n'est pas déjà fait

### 2. Générer un mot de passe d'application

1. **Allez dans Sécurité** → **Mot de passe des applications**
   - Lien direct : https://myaccount.google.com/apppasswords
2. **Sélectionnez l'application** : "Autre (nom personnalisé)"
3. **Donnez un nom** : "Django Portfolio"
4. **Cliquez sur "Générer"**
5. **Copiez le mot de passe généré** (16 caractères sans espaces)

### 3. Configurer le fichier .env

Créez ou modifiez le fichier `.env` dans le dossier racine :

```env
# Configuration Email Gmail
EMAIL_HOST_USER=samakedelamou858@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
ADMIN_EMAIL=samakedelamou858@gmail.com
```

⚠️ **Important** : Le mot de passe d'application doit être copié sans espaces :
- ✅ Correct : `abcdefghijklmnop`
- ❌ Incorrect : `abcd efgh ijkl mnop`

### 4. Redémarrer le serveur

```bash
# Arrêtez le serveur (Ctrl+C)
# Redémarrez-le
python manage.py runserver
```

## 🧪 Tester l'envoi d'emails

### Option 1 : Via le formulaire de contact

1. Allez sur http://localhost:8000/#contact
2. Remplissez le formulaire avec :
   - Nom : "Test"
   - Email : "votre_email@test.com"
   - Sujet : "Test email"
   - Message : "Ceci est un test"
3. Cliquez sur "Envoyer"
4. Vérifiez votre boîte mail `samakedelamou858@gmail.com`

### Option 2 : Via Django Shell

```bash
python manage.py shell
```

```python
from django.core.mail import send_mail
send_mail(
    'Test Email Portfolio',
    'Ceci est un message de test depuis votre portfolio.',
    'samakedelamou858@gmail.com',
    ['samakedelamou858@gmail.com'],
    fail_silently=False,
)
```

## 🔧 Configuration actuelle

Le portfolio envoie automatiquement **2 emails** pour chaque message :

1. **Email au propriétaire** (vous) :
   - Destinataire : `samakedelamou858@gmail.com`
   - Contient : Nom, email, sujet et message du visiteur

2. **Email de confirmation** au visiteur :
   - Destinataire : L'email du visiteur
   - Contient : Confirmation de réception et vos coordonnées

## 🐛 Dépannage

### Erreur : "SMTPAuthenticationError"

**Cause** : Mot de passe d'application incorrect ou 2FA non activé

**Solution** :
1. Vérifiez que la 2FA est activée
2. Régénérez un nouveau mot de passe d'application
3. Copiez-le sans espaces dans `.env`

### Erreur : "Connection refused"

**Cause** : Problème de connexion au serveur SMTP

**Solution** :
1. Vérifiez votre connexion internet
2. Vérifiez que le port 587 n'est pas bloqué par votre pare-feu
3. Essayez avec le port 465 et `EMAIL_USE_SSL = True`

### Erreur : "TLS/SSL error"

**Cause** : Configuration SSL/TLS incorrecte

**Solution** : Dans `settings.py`, utilisez :
```python
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
```

### Les emails n'arrivent pas

**Vérifiez** :
1. Le dossier **Spam** / **Courrier indésirable**
2. Les logs Django dans la console pour les erreurs
3. Que le fichier `.env` est bien chargé (redémarrez le serveur)

## 📊 Monitoring des emails

### Voir les messages en base de données

1. Connectez-vous à l'admin : http://localhost:8000/admin
2. Allez dans **Contact Messages**
3. Tous les messages sont sauvegardés même si l'email échoue

### Voir les logs en développement

Les erreurs d'envoi d'email s'affichent dans la console Django :
- ✅ Succès : Pas de message
- ❌ Erreur : Exception affichée avec détails

## 🔒 Sécurité

⚠️ **Règles importantes** :

1. **Ne jamais** mettre le mot de passe Gmail réel dans le code
2. **Toujours** utiliser un mot de passe d'application
3. **Le fichier `.env`** est exclu de Git via `.gitignore`
4. **En production**, utilisez des variables d'environnement sécurisées

## 📝 Alternative : Utiliser un autre service

### Outlook/Hotmail

```python
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

### Yahoo Mail

```python
EMAIL_HOST = 'smtp.mail.yahoo.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
```

### SendGrid (Production)

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'votre_cle_api_sendgrid'
```

## ✅ Checklist de configuration

- [ ] 2FA activée sur le compte Google
- [ ] Mot de passe d'application généré
- [ ] Fichier `.env` créé avec les bonnes valeurs
- [ ] Serveur Django redémarré
- [ ] Test d'envoi réussi
- [ ] Emails reçus dans la boîte (pas dans les spams)
