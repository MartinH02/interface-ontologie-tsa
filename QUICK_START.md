# 🚀 Déploiement rapide - Interface Web Ontologie TSA

## Option recommandée : Render.com (Gratuit)

### Étapes en 5 minutes :

1. **Créer un compte** sur https://render.com (gratuit)

2. **Créer un dépôt GitHub** (si pas déjà fait) :
   - Allez sur https://github.com/new
   - Créez un nouveau dépôt
   - Uploadez tous vos fichiers (ou utilisez Git)

3. **Sur Render.com** :
   - Cliquez sur "New +" → "Web Service"
   - Connectez votre compte GitHub
   - Sélectionnez votre dépôt

4. **Configuration** :
   ```
   Name: interface-ontologie-tsa
   Environment: Python 3
   Build Command: pip install -r web/requirements.txt
   Start Command: cd web && gunicorn app:app --bind 0.0.0.0:$PORT
   ```

5. **Cliquez sur "Create Web Service"**

6. **Attendez 2-3 minutes** → Vous obtiendrez un lien comme :
   `https://interface-ontologie-tsa.onrender.com`

7. **Partagez ce lien avec votre professeur !** 🎉

---

## ⚠️ Important

- Le service gratuit s'endort après 15 min d'inactivité
- Le premier démarrage après inactivité prend 30-60 secondes
- C'est normal et gratuit !

---

## Fichiers déjà préparés ✅

- ✅ `web/requirements.txt` - Toutes les dépendances
- ✅ `Procfile` - Configuration pour le déploiement
- ✅ `render.yaml` - Configuration Render (optionnel)
- ✅ Code modifié pour fonctionner en production

---

## Besoin d'aide ?

Consultez `README_DEPLOYMENT.md` pour plus de détails.

