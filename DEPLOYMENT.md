# Guide de déploiement de l'interface web

Ce guide explique comment déployer l'interface web d'interrogation de l'ontologie TSA-NLP gratuitement.

## Option 1 : Render.com (Recommandé - Gratuit)

### Étapes :

1. **Créer un compte sur Render.com** : https://render.com (gratuit)

2. **Créer un nouveau Web Service** :
   - Cliquez sur "New +" → "Web Service"
   - Connectez votre dépôt GitHub (ou créez-en un)

3. **Configuration** :
   - **Name** : `interface-ontologie-tsa` (ou autre nom)
   - **Environment** : `Python 3`
   - **Build Command** : `pip install -r web/requirements.txt`
   - **Start Command** : `cd web && gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Root Directory** : `/` (racine du projet)

4. **Variables d'environnement** (optionnel) :
   - `PORT` : sera défini automatiquement par Render

5. **Déployer** :
   - Cliquez sur "Create Web Service"
   - Render va automatiquement déployer votre application
   - Le lien sera disponible sous la forme : `https://interface-ontologie-tsa.onrender.com`

### Avantages :
- ✅ Gratuit (avec limitations)
- ✅ Déploiement automatique depuis GitHub
- ✅ SSL/HTTPS inclus
- ✅ Facile à configurer

---

## Option 2 : PythonAnywhere (Gratuit pour étudiants)

### Étapes :

1. **Créer un compte** : https://www.pythonanywhere.com (gratuit pour étudiants)

2. **Uploader les fichiers** :
   - Utilisez l'interface web pour uploader les fichiers
   - Ou utilisez Git : `git clone` votre dépôt

3. **Configuration** :
   - Créez un nouveau Web App
   - Sélectionnez "Manual configuration" → Python 3.10
   - Dans "Source code" : `/home/votreusername/InterfaceWebOntologie/web`
   - Dans "WSGI configuration file" : modifiez pour pointer vers `app.py`

4. **Installer les dépendances** :
   - Ouvrez une console Bash
   - `cd ~/InterfaceWebOntologie/web`
   - `pip3.10 install --user -r requirements.txt`

5. **Configurer WSGI** :
   - Modifiez le fichier WSGI pour pointer vers votre app Flask

---

## Option 3 : Railway.app (Gratuit avec limitations)

### Étapes :

1. **Créer un compte** : https://railway.app

2. **Nouveau projet** :
   - "New Project" → "Deploy from GitHub repo"

3. **Configuration** :
   - Railway détecte automatiquement Python
   - Assurez-vous que `requirements.txt` est dans le dossier `web/`
   - Railway utilisera automatiquement le port fourni

---

## Fichiers nécessaires

Les fichiers suivants sont déjà créés :
- ✅ `web/requirements.txt` - Dépendances Python
- ✅ `Procfile` - Configuration pour Heroku/Railway
- ✅ `render.yaml` - Configuration pour Render.com

## Notes importantes

- L'application utilise le port défini par la variable d'environnement `PORT` (fournie automatiquement par les plateformes)
- Les fichiers statiques (CSS, images) sont servis depuis `web/static/`
- Les templates HTML sont dans `web/templates/`
- L'ontologie `ontology_tsa_nlp-3.owl` doit être accessible depuis le dossier parent de `web/`

## Test local avant déploiement

```bash
cd web
pip install -r requirements.txt
python app.py
```

L'application sera accessible sur `http://localhost:5000`

