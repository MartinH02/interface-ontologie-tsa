# Guide de déploiement rapide - Interface Web Ontologie TSA

## 🚀 Déploiement sur Render.com (Recommandé - Gratuit)

### Étape 1 : Préparer votre code sur GitHub

1. **Créer un dépôt GitHub** (si pas déjà fait) :
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Interface web ontologie TSA"
   git branch -M main
   git remote add origin https://github.com/VOTRE_USERNAME/VOTRE_REPO.git
   git push -u origin main
   ```

### Étape 2 : Déployer sur Render.com

1. **Créer un compte** : Allez sur https://render.com et créez un compte gratuit

2. **Créer un nouveau Web Service** :
   - Cliquez sur "New +" en haut à droite
   - Sélectionnez "Web Service"
   - Connectez votre compte GitHub et sélectionnez votre dépôt

3. **Configuration du service** :
   - **Name** : `interface-ontologie-tsa` (ou un nom de votre choix)
   - **Environment** : `Python 3`
   - **Region** : Choisissez la région la plus proche (ex: Frankfurt)
   - **Branch** : `main` (ou `master`)
   - **Root Directory** : Laissez vide (racine du projet)
   - **Build Command** : `pip install -r web/requirements.txt`
   - **Start Command** : `cd web && gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Plan** : Free (gratuit)

4. **Variables d'environnement** :
   - Aucune variable nécessaire pour le moment
   - Le `PORT` est automatiquement défini par Render

5. **Déployer** :
   - Cliquez sur "Create Web Service"
   - Render va automatiquement :
     - Cloner votre dépôt
     - Installer les dépendances
     - Démarrer l'application
   - Le déploiement prend environ 2-3 minutes

6. **Obtenir le lien** :
   - Une fois déployé, vous obtiendrez un lien du type :
     `https://interface-ontologie-tsa.onrender.com`
   - Ce lien est permanent et peut être partagé avec votre professeur

### ⚠️ Notes importantes

- **Premier démarrage** : Le service gratuit de Render peut prendre 30-60 secondes à démarrer après inactivité
- **Limitations du plan gratuit** :
  - Le service s'endort après 15 minutes d'inactivité
  - Le redémarrage prend quelques secondes
  - 750 heures gratuites par mois (suffisant pour un projet étudiant)

### 🔄 Mises à jour

Chaque fois que vous poussez du code sur GitHub, Render redéploiera automatiquement votre application.

---

## Alternative : PythonAnywhere (Gratuit pour étudiants)

Si Render ne fonctionne pas, vous pouvez utiliser PythonAnywhere :

1. Créez un compte sur https://www.pythonanywhere.com
2. Uploader vos fichiers via l'interface web
3. Configurez un Web App avec Flask
4. Votre URL sera : `https://VOTRE_USERNAME.pythonanywhere.com`

---

## Test local avant déploiement

Pour tester localement avant de déployer :

```bash
cd web
pip install -r requirements.txt
python app.py
```

Puis ouvrez http://localhost:5000 dans votre navigateur.

---

## Structure des fichiers

```
InterfaceWebOntologie/
├── web/
│   ├── app.py              # Application Flask principale
│   ├── requirements.txt    # Dépendances Python
│   ├── templates/          # Templates HTML
│   └── static/             # CSS et fichiers statiques
├── ontology_tsa_nlp-3.owl  # Fichier ontologie
├── Procfile                # Configuration pour Heroku/Railway
└── render.yaml             # Configuration pour Render
```

---

## Support

Si vous rencontrez des problèmes :
1. Vérifiez les logs dans Render (onglet "Logs")
2. Assurez-vous que tous les fichiers sont bien dans le dépôt GitHub
3. Vérifiez que `requirements.txt` contient toutes les dépendances

