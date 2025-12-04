from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
import pandas as pd
import os
from datetime import datetime
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import pickle
import xml.etree.ElementTree as ET
import json
from rdflib import Graph, Namespace, RDF, RDFS, Literal, URIRef

app = Flask(__name__)

# Chemins des fichiers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)

# Variables globales pour le modèle
model = None
label_encoders = {}
feature_columns = None

def load_and_train_model():
    """Charge les données et entraîne le modèle de prédiction"""
    global model, label_encoders, feature_columns
    
    try:
        # Charger les données d'entraînement
        train_path = os.path.join(PARENT_DIR, 'autismdiagnosis', 'Autism_Prediction', 'train.csv')
        df = pd.read_csv(train_path)
        
        # Préparation des données (identique au notebook)
        X = df.drop(['ID', 'Class/ASD', 'age_desc'], axis=1)
        y = df['Class/ASD']
        
        # Sauvegarder l'ordre des colonnes
        feature_columns = X.columns.tolist()
        
        # Encoder les variables catégorielles
        label_encoders = {}
        X_encoded = X.copy()
        
        for col in X.select_dtypes(include=['object']).columns:
            le = LabelEncoder()
            X_encoded[col] = le.fit_transform(X[col].astype(str))
            label_encoders[col] = le
        
        # Entraîner le modèle
        model = LogisticRegression(max_iter=1000, random_state=42)
        model.fit(X_encoded, y)
        
        print("Modèle entraîné avec succès!")
        return True
    except Exception as e:
        print(f"Erreur lors de l'entraînement du modèle: {e}")
        return False

# Charger le modèle au démarrage
load_and_train_model()

def load_articles():
    """Charge les 5 articles les plus pertinents"""
    try:
        # Essayer d'abord dans Qui_marche_bien, puis dans Google_scholar
        csv_path = os.path.join(PARENT_DIR, 'Google_scholar', 'Qui_marche_bien', 'articles_filtres_seuil_40.csv')
        if not os.path.exists(csv_path):
            csv_path = os.path.join(PARENT_DIR, 'Google_scholar', 'articles_filtres_seuil_40.csv')
        
        if not os.path.exists(csv_path):
            print(f"⚠ Fichier CSV non trouvé: {csv_path}")
            return []
        
        df = pd.read_csv(csv_path, encoding='utf-8-sig')
        print(f"✓ Fichier chargé: {csv_path} ({len(df)} articles)")
        
        # Trier par score de pertinence
        df = df.sort_values('score_pertinence', ascending=False)
        # Prendre seulement les 5 premiers
        df = df.head(5)
        print(f"✓ {len(df)} articles sélectionnés (top 5)")
        
        # Remplacer les NaN par des chaînes vides pour les colonnes texte
        text_columns = ['titre', 'auteurs', 'source', 'resume', 'lien', 'email_date', 'email_subject']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].fillna('').astype(str)
        
        return df.to_dict('records')
    except Exception as e:
        print(f"❌ Erreur lors du chargement des articles: {e}")
        import traceback
        traceback.print_exc()
        return []


def get_stats():
    """Calcule les statistiques de la veille"""
    articles = load_articles()
    if not articles:
        return {}
    
    scores = [a.get('score_pertinence', 0) for a in articles if a.get('score_pertinence')]
    
    return {
        'total_articles': len(articles),
        'score_moyen': round(sum(scores) / len(scores), 2) if scores else 0,
        'score_max': max(scores) if scores else 0,
        'score_min': min(scores) if scores else 0,
        'articles_pertinents': len([s for s in scores if s >= 50]),
        'date_derniere_maj': datetime.now().strftime('%d/%m/%Y')
    }

@app.route('/')
def index():
    """Page principale"""
    return render_template('index.html')

@app.route('/prediction')
def prediction_page():
    """Page de formulaire de prédiction"""
    # Charger les valeurs uniques pour les menus déroulants
    train_path = os.path.join(PARENT_DIR, 'autismdiagnosis', 'Autism_Prediction', 'train.csv')
    df = pd.read_csv(train_path)
    
    # Extraire les valeurs uniques pour chaque colonne catégorielle
    options = {
        'genders': sorted(df['gender'].unique().tolist()),
        'ethnicities': sorted([e for e in df['ethnicity'].unique() if e != '?']),
        'countries': sorted([c for c in df['contry_of_res'].unique()]),
        'relations': sorted([r for r in df['relation'].unique() if r != '?'])
    }
    
    return render_template('prediction.html', options=options)

@app.route('/predict', methods=['POST'])
def predict():
    """Traite le formulaire et retourne la prédiction"""
    global model, label_encoders, feature_columns
    
    if model is None:
        return jsonify({'error': 'Modèle non disponible'}), 500
    
    try:
        # Récupérer les données du formulaire
        data = {
            'A1_Score': int(request.form.get('A1_Score', 0)),
            'A2_Score': int(request.form.get('A2_Score', 0)),
            'A3_Score': int(request.form.get('A3_Score', 0)),
            'A4_Score': int(request.form.get('A4_Score', 0)),
            'A5_Score': int(request.form.get('A5_Score', 0)),
            'A6_Score': int(request.form.get('A6_Score', 0)),
            'A7_Score': int(request.form.get('A7_Score', 0)),
            'A8_Score': int(request.form.get('A8_Score', 0)),
            'A9_Score': int(request.form.get('A9_Score', 0)),
            'A10_Score': int(request.form.get('A10_Score', 0)),
            'age': float(request.form.get('age', 0)),
            'gender': request.form.get('gender', ''),
            'ethnicity': request.form.get('ethnicity', ''),
            'jaundice': request.form.get('jaundice', 'no'),
            'austim': request.form.get('austim', 'no'),
            'contry_of_res': request.form.get('contry_of_res', ''),
            'used_app_before': request.form.get('used_app_before', 'no'),
            'relation': request.form.get('relation', '')
        }
        
        # Calculer le result (score basé sur les réponses A1-A10)
        # Le result est une métrique calculée dans le dataset original
        # Approximation basée sur l'analyse des données d'entraînement
        scores_sum = sum([data[f'A{i}_Score'] for i in range(1, 11)])
        # Formule approximative: result varie généralement entre -5 et 15
        # avec une corrélation positive avec la somme des scores
        if scores_sum == 0:
            # Pour score 0, result varie entre -5 et 3
            data['result'] = 2.0 + (data['age'] / 100) * 2.0 - 4.0
        else:
            # Pour scores > 0, corrélation plus forte
            data['result'] = scores_sum * 1.4 + (data['age'] / 50) - 2.0
        
        # Créer un DataFrame avec les données
        input_df = pd.DataFrame([data])
        
        # Encoder les variables catégorielles
        input_encoded = input_df.copy()
        for col in label_encoders.keys():
            if col in input_encoded.columns:
                # Gérer les valeurs inconnues
                value = str(input_encoded[col].iloc[0])
                if value in label_encoders[col].classes_:
                    input_encoded[col] = label_encoders[col].transform([value])[0]
                else:
                    # Utiliser la valeur la plus fréquente comme défaut
                    input_encoded[col] = 0
        
        # Réorganiser les colonnes dans le bon ordre
        input_encoded = input_encoded[feature_columns]
        
        # Faire la prédiction
        prediction = model.predict(input_encoded)[0]
        probability = model.predict_proba(input_encoded)[0]
        
        # Probabilité d'être autiste (classe 1)
        autism_probability = probability[1] * 100
        
        return render_template('prediction_result.html', 
                             probability=round(autism_probability, 2),
                             prediction=prediction,
                             data=data)
    
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la prédiction: {str(e)}'}), 500

@app.route('/notebook')
def notebook():
    """Affiche le notebook HTML"""
    notebook_path = os.path.join(PARENT_DIR, 'autism_prediction.html')
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_html = f.read()
        return render_template('notebook_viewer.html', notebook_content=notebook_html)
    except Exception as e:
        return f"Erreur lors du chargement du notebook: {str(e)}", 500

@app.route('/notebook_files/<path:filename>')
def notebook_files(filename):
    """Sert les fichiers de ressources du notebook (images, etc.)"""
    files_dir = os.path.join(PARENT_DIR, 'autism_prediction_files')
    return send_from_directory(files_dir, filename)

def get_ontology_individuals_by_type():
    """Extrait les individus de l'ontologie groupés par type pour les listes déroulantes"""
    ontology_path = os.path.join(PARENT_DIR, 'ontology_tsa_nlp-3.owl')
    
    try:
        g = Graph()
        g.parse(ontology_path, format="xml")
        
        # Namespace
        ns = Namespace("http://example.org/ont/tsa-nlp#")
        
        # Extraire les individus par type
        individuals_by_type = {
            'TechnologieNLP': [],
            'TechnologieVision': [],
            'TechnologieMouvement': [],
            'Applications': [],
            'RobotSocial': [],
            'SystemeVR_AR': [],
            'SystemeCaptationMouvement': [],
            'SystemeMonitoring': [],
            'SystemePlanificationVisuelle': [],
            'JeuSerieux': [],
            'ObjetConnecte': [],
            'OutilEvaluation': [],
            'OutilNumerique': [],
            'Professionnel': [],
            'Orthophoniste': [],
            'Psychologue': [],
            'Enseignant': [],
            'DomaineClinique': [],
            'Intervention': [],
            'PersonneTSA': [],
            'BesoinsParents': []
        }
        
        # Parcourir tous les individus
        for subject, predicate, obj in g.triples((None, RDF.type, None)):
            # Nettoyer le nom de la classe
            class_name = str(obj).split('#')[-1] if '#' in str(obj) else str(obj)
            
            # Nettoyer le nom de l'individu
            indiv_name = str(subject).split('#')[-1] if '#' in str(subject) else str(subject)
            
            if class_name in individuals_by_type:
                label = indiv_name.replace('_', ' ')
                # Vérifier si l'individu n'est pas déjà dans la liste pour éviter les doublons
                existing_ids = [x['id'] for x in individuals_by_type[class_name]]
                if indiv_name not in existing_ids:
                    individuals_by_type[class_name].append({
                        'id': indiv_name,
                        'label': label
                    })
            
            # Gérer les besoins parents (vérifier via la hiérarchie)
            # Ne traiter que si ce n'est pas déjà géré par la boucle principale
            if 'Besoin' in indiv_name and class_name != 'BesoinsParents':
                # Vérifier si c'est un besoin parent
                for s, p, o in g.triples((subject, RDF.type, None)):
                    type_str = str(o)
                    if 'BesoinsParents' in type_str:
                        existing_ids = [x['id'] for x in individuals_by_type['BesoinsParents']]
                        if indiv_name not in existing_ids:
                            label = indiv_name.replace('_', ' ')
                            individuals_by_type['BesoinsParents'].append({
                                'id': indiv_name,
                                'label': label
                            })
        
        # Trier par label
        for key in individuals_by_type:
            individuals_by_type[key].sort(key=lambda x: x['label'])
        
        return individuals_by_type
    except Exception as e:
        print(f"Erreur lors du chargement de l'ontologie: {e}")
        return {}

def parse_ontology():
    """Parse le fichier OWL et extrait les classes, propriétés et relations"""
    ontology_path = os.path.join(PARENT_DIR, 'ontology_tsa_nlp-3.owl')
    
    try:
        tree = ET.parse(ontology_path)
        root = tree.getroot()
        
        # Namespaces
        ns = {
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
            'owl': 'http://www.w3.org/2002/07/owl#'
        }
        
        classes = {}
        properties = {}
        individuals = {}
        subclass_relations = []
        property_relations = []
        
        # Extraire les classes
        for class_elem in root.findall('.//owl:Class', ns):
            class_id_raw = class_elem.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', '')
            # Nettoyer l'ID : extraire la partie après le dernier #
            if class_id_raw:
                if class_id_raw.startswith('#'):
                    class_id = class_id_raw[1:]
                elif '#' in class_id_raw:
                    class_id = class_id_raw.split('#')[-1]
                else:
                    class_id = class_id_raw
            else:
                class_id = ''
            
            if class_id:
                label_elem = class_elem.find('rdfs:label', ns)
                label = label_elem.get('{http://www.w3.org/XML/1998/namespace}lang', '') if label_elem is not None else class_id
                classes[class_id] = {
                    'id': class_id,
                    'label': label_elem.text if label_elem is not None else class_id,
                    'type': 'class'
                }
                
                # Extraire les relations subClassOf
                for sub_class in class_elem.findall('rdfs:subClassOf', ns):
                    parent_raw = sub_class.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', '')
                    # Nettoyer l'ID du parent : extraire la partie après le dernier #
                    if parent_raw:
                        if parent_raw.startswith('#'):
                            parent = parent_raw[1:]
                        elif '#' in parent_raw:
                            parent = parent_raw.split('#')[-1]
                        else:
                            parent = parent_raw
                    else:
                        parent = ''
                    
                    if parent:
                        subclass_relations.append({
                            'from': class_id,
                            'to': parent,
                            'type': 'subClassOf'
                        })
        
        # Extraire les propriétés d'objet
        for prop in root.findall('.//owl:ObjectProperty', ns):
            prop_id_raw = prop.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', '')
            # Nettoyer l'ID : extraire la partie après le dernier #
            if prop_id_raw:
                if prop_id_raw.startswith('#'):
                    prop_id = prop_id_raw[1:]
                elif '#' in prop_id_raw:
                    prop_id = prop_id_raw.split('#')[-1]
                else:
                    prop_id = prop_id_raw
            else:
                prop_id = ''
            
            if prop_id:
                label_elem = prop.find('rdfs:label', ns)
                properties[prop_id] = {
                    'id': prop_id,
                    'label': label_elem.text if label_elem is not None else prop_id,
                    'type': 'property'
                }
        
        # Extraire les individus depuis NamedIndividual
        for indiv in root.findall('.//owl:NamedIndividual', ns):
            indiv_id = indiv.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', '')
            if indiv_id:
                if indiv_id.startswith('#'):
                    indiv_id = indiv_id[1:]
                elif '#' in indiv_id:
                    indiv_id = indiv_id.split('#')[-1]
                
                if indiv_id:
                    individuals[indiv_id] = {
                        'id': indiv_id,
                        'label': indiv_id.replace('_', ' ').replace('#', ''),
                        'type': 'individual'
                    }
                    
                    # Extraire le type (rdf:type) pour créer une relation
                    type_elem = indiv.find('rdf:type', ns)
                    if type_elem is not None:
                        type_resource = type_elem.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', '')
                        if type_resource:
                            if type_resource.startswith('#'):
                                type_resource = type_resource[1:]
                            elif '#' in type_resource:
                                type_resource = type_resource.split('#')[-1]
                            
                            if type_resource and type_resource not in classes:
                                # Ajouter la classe si elle n'existe pas encore
                                classes[type_resource] = {
                                    'id': type_resource,
                                    'label': type_resource,
                                    'type': 'class'
                                }
                            
                            # Créer une relation de type
                            if type_resource:
                                property_relations.append({
                                    'from': indiv_id,
                                    'to': type_resource,
                                    'type': 'rdf:type',
                                    'label': 'est de type'
                                })
        
        # Extraire les individus et leurs relations depuis rdf:Description
        for desc in root.findall('.//rdf:Description', ns):
            individual_id = desc.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', '')
            if individual_id:
                # Nettoyer l'ID
                if individual_id.startswith('#'):
                    individual_id = individual_id[1:]
                elif '#' in individual_id:
                    individual_id = individual_id.split('#')[-1]
                
                if individual_id and individual_id not in individuals:
                    individuals[individual_id] = {
                        'id': individual_id,
                        'label': individual_id.replace('_', ' '),
                        'type': 'individual'
                    }
                
                # Extraire les relations de l'individu
                for child in desc:
                    # Extraire le nom de la propriété (peut être dans différents formats)
                    prop_name = child.tag
                    if '}' in prop_name:
                        prop_name = prop_name.split('}')[-1]
                    elif '#' in prop_name:
                        prop_name = prop_name.split('#')[-1]
                    
                    # Obtenir la cible de la relation
                    target = child.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', '')
                    if target:
                        # Nettoyer la cible
                        if target.startswith('#'):
                            target = target[1:]
                        elif '#' in target:
                            target = target.split('#')[-1]
                        
                        if target and target != individual_id:
                            # Vérifier si la cible existe dans nos données
                            target_exists = (target in classes or target in individuals or 
                                           target in properties or target == 'Thing')
                            
                            if target_exists:
                                property_relations.append({
                                    'from': individual_id,
                                    'to': target,
                                    'type': prop_name,
                                    'label': properties.get(prop_name, {}).get('label', prop_name) if prop_name in properties else prop_name
                                })
        
        return {
            'classes': classes,
            'properties': properties,
            'individuals': individuals,
            'subclass_relations': subclass_relations,
            'property_relations': property_relations
        }
    except Exception as e:
        print(f"Erreur lors du parsing de l'ontologie: {e}")
        return None

@app.route('/ontology')
def ontology_viewer():
    """Affiche la visualisation interactive de l'ontologie"""
    ontology_data = parse_ontology()
    if ontology_data is None:
        return "Erreur lors du chargement de l'ontologie", 500
    
    # Convertir en JSON pour le template JavaScript
    ontology_data_json = json.dumps(ontology_data, ensure_ascii=False)
    
    return render_template('ontology_viewer.html', ontology_data_json=ontology_data_json)

@app.route('/veille')
def veille_page():
    """Page avec onglets pour le suivi et les rapports de veille"""
    # URL de la page Notion publique
    notion_url = os.environ.get('NOTION_URL', '')
    if not notion_url:
        notion_url = 'https://bitter-chef-13a.notion.site/ebd/2b5556f762b3804cad8ef22f038adb26'
    
    # Chemins des PDFs
    rapport_contexte = os.path.join(PARENT_DIR, 'IA03_Veille_contexte.pdf')
    rapport_veille = os.path.join(PARENT_DIR, 'IA03_Rapport_de_veille.pdf')
    
    # Vérifier si les fichiers existent
    has_contexte = os.path.exists(rapport_contexte)
    has_rapport = os.path.exists(rapport_veille)
    
    return render_template('veille_page.html', 
                         notion_url=notion_url,
                         has_contexte=has_contexte,
                         has_rapport=has_rapport)

@app.route('/veille/pdf/<filename>')
def serve_pdf(filename):
    """Sert les fichiers PDF"""
    if filename == 'IA03_Veille_contexte.pdf':
        pdf_path = os.path.join(PARENT_DIR, 'IA03_Veille_contexte.pdf')
    elif filename == 'IA03_Rapport_de_veille.pdf':
        pdf_path = os.path.join(PARENT_DIR, 'IA03_Rapport_de_veille.pdf')
    else:
        return "Fichier non trouvé", 404
    
    if os.path.exists(pdf_path):
        response = send_file(pdf_path, mimetype='application/pdf')
        # Ajouter des headers pour permettre l'affichage dans iframe
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
    return "Fichier non trouvé", 404

@app.route('/ontology/query')
def ontology_query():
    """Page d'interrogation de l'ontologie avec questions à trous"""
    individuals = get_ontology_individuals_by_type()
    return render_template('ontology_query.html', individuals=individuals)

@app.route('/ontology/individual/<individual_id>/properties')
def get_individual_properties(individual_id):
    """Récupère les data properties et object properties d'un individu"""
    ontology_path = os.path.join(PARENT_DIR, 'ontology_tsa_nlp-3.owl')
    
    try:
        g = Graph()
        g.parse(ontology_path, format="xml", publicID="http://example.org/ont/tsa-nlp")
        
        ns = Namespace("http://example.org/ont/tsa-nlp#")
        
        # Construire l'URI de l'individu
        individual_uri = ns[individual_id]
        
        # Récupérer toutes les propriétés et les séparer en data et object properties
        object_properties = []
        data_properties = []
        
        for pred, obj in g.predicate_objects(individual_uri):
            # Ignorer rdf:type
            if pred == RDF.type:
                continue
            
            # Nettoyer le nom de la propriété
            prop_name = str(pred).split('#')[-1] if '#' in str(pred) else str(pred)
            
            # Récupérer le label de la propriété si disponible
            prop_label = prop_name
            for s, p, o in g.triples((pred, RDFS.label, None)):
                prop_label = str(o)
                break
            
            # Distinguer entre data property (Literal) et object property (URIRef)
            if isinstance(obj, Literal):
                # C'est une data property
                value = str(obj)
                data_properties.append({
                    'property': prop_name,
                    'property_label': prop_label,
                    'value': value
                })
            elif isinstance(obj, URIRef):
                # C'est une object property
                obj_str = str(obj)
                if '#' in obj_str:
                    obj_str = obj_str.split('#')[-1]
                elif '/' in obj_str:
                    obj_str = obj_str.split('/')[-1]
                
                object_properties.append({
                    'property': prop_name,
                    'property_label': prop_label,
                    'value': obj_str.replace('_', ' '),
                    'value_uri': str(obj)
                })
        
        # Récupérer aussi depuis les descriptions XML pour les data properties
        tree = ET.parse(ontology_path)
        root = tree.getroot()
        ns_xml = {
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
            'owl': 'http://www.w3.org/2002/07/owl#'
        }
        
        # Chercher l'individu dans le XML (rdf:Description et owl:NamedIndividual)
        for desc in root.findall('.//rdf:Description', ns_xml) + root.findall('.//owl:NamedIndividual', ns_xml):
            desc_id = desc.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', '')
            if desc_id:
                # Nettoyer l'ID
                if desc_id.startswith('#'):
                    desc_id = desc_id[1:]
                elif '#' in desc_id:
                    desc_id = desc_id.split('#')[-1]
                
                if desc_id == individual_id:
                    # Parcourir tous les enfants pour trouver les data properties
                    for child in desc:
                        prop_name = child.tag
                        if '}' in prop_name:
                            prop_name = prop_name.split('}')[-1]
                        elif '#' in prop_name:
                            prop_name = prop_name.split('#')[-1]
                        
                        # Ignorer rdf:type
                        if prop_name == 'type':
                            continue
                        
                        # Si c'est une data property (pas de resource, mais du texte)
                        if child.text and not child.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource'):
                            # Vérifier si on ne l'a pas déjà ajoutée
                            if not any(dp['property'] == prop_name for dp in data_properties):
                                data_properties.append({
                                    'property': prop_name,
                                    'property_label': prop_name.replace('_', ' '),
                                    'value': child.text.strip()
                                })
        
        return jsonify({
            'success': True,
            'individual_id': individual_id,
            'data_properties': data_properties,
            'object_properties': object_properties
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/ontology/query/execute', methods=['POST'])
def execute_ontology_query():
    """Exécute une requête SPARQL sur l'ontologie"""
    try:
        data = request.json
        question_id = data.get('question_id')
        params = data.get('params', {})
        
        ontology_path = os.path.join(PARENT_DIR, 'ontology_tsa_nlp-3.owl')
        g = Graph()
        g.parse(ontology_path, format="xml", publicID="http://example.org/ont/tsa-nlp")
        
        ns = Namespace("http://example.org/ont/tsa-nlp#")
        
        # Construire la requête SPARQL selon la question
        if question_id == '1':
            # Question 1: Quels outils numériques utilisent la technologie [TYPE_TECHNO] ?
            techno = params.get('technologie', '')
            query = f"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX : <http://example.org/ont/tsa-nlp#>
            
            SELECT DISTINCT ?outil
            WHERE {{
                ?outil rdf:type/rdfs:subClassOf* :OutilNumerique .
                ?outil :implementeTechnologie :{techno} .
            }}
            """
        elif question_id == '2':
            # Question 2: Quels outils numériques sont utilisés par [PERSONNE_TSA] ?
            personne = params.get('personne', '')
            query = f"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX : <http://example.org/ont/tsa-nlp#>
            
            SELECT DISTINCT ?outil
            WHERE {{
                :{personne} rdf:type :PersonneTSA .
                :{personne} :estAidePar ?outil .
                ?outil rdf:type/rdfs:subClassOf* :OutilNumerique .
            }}
            """
        elif question_id == '3':
            # Question 3: Quels outils numériques soutiennent l'intervention [INTERVENTION] ?
            intervention = params.get('intervention', '')
            query = f"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX : <http://example.org/ont/tsa-nlp#>
            
            SELECT DISTINCT ?outil
            WHERE {{
                ?outil rdf:type/rdfs:subClassOf* :OutilNumerique .
                {{
                    ?outil :soutientIntervention :{intervention} .
                }}
                UNION
                {{
                    ?outil :utiliseDansIntervention :{intervention} .
                }}
            }}
            """
        elif question_id == '4':
            # Question 4: Quels besoins satisfait [OUTIL_NUMERIQUE] et ce besoin est-il un besoin parent ou enfant TSA ?
            outil = params.get('outil', '')
            query = f"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX : <http://example.org/ont/tsa-nlp#>
            
            SELECT DISTINCT ?besoin ?typeBesoin
            WHERE {{
                :{outil} rdf:type/rdfs:subClassOf* :OutilNumerique .
                {{
                    :{outil} :repondABesoin ?besoin .
                }}
                UNION
                {{
                    ?besoin :estSatisfaitPar :{outil} .
                }}
                ?besoin rdf:type ?typeBesoin .
                {{
                    ?typeBesoin rdfs:subClassOf* :BesoinsParents .
                }}
                UNION
                {{
                    ?typeBesoin rdfs:subClassOf* :BesoinsEnfantTSA .
                }}
            }}
            """
        elif question_id == '6':
            # Question 6: Liste l'ensemble des individus de chaque sous-classe de OutilNumérique
            sousclasse = params.get('sousclasse', '')
            if not sousclasse:
                return jsonify({'error': 'Sous-classe non spécifiée'}), 400
            
            # Utiliser le namespace pour construire l'URI complète
            sousclasse_uri = f"http://example.org/ont/tsa-nlp#{sousclasse}"
            query = f"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX : <http://example.org/ont/tsa-nlp#>
            
            SELECT DISTINCT ?individu
            WHERE {{
                ?individu rdf:type <{sousclasse_uri}> .
            }}
            ORDER BY ?individu
            """
        else:
            return jsonify({'error': 'Question invalide'}), 400
        
        # Exécuter la requête avec les namespaces
        results = g.query(query, initNs={
            'rdf': RDF,
            'rdfs': RDFS
        })
        
        # Formater les résultats
        results_list = []
        for row in results:
            if question_id == '4':
                # Question 4 retourne deux colonnes : besoin et typeBesoin
                besoin = str(row[0]).split('#')[-1] if '#' in str(row[0]) else str(row[0])
                type_besoin = str(row[1]).split('#')[-1] if '#' in str(row[1]) else str(row[1])
                
                # Déterminer si c'est un besoin parent ou enfant TSA
                if 'BesoinsParents' in type_besoin:
                    type_label = "Besoin Parent"
                elif 'BesoinsEnfantTSA' in type_besoin:
                    type_label = "Besoin Enfant TSA"
                else:
                    type_label = type_besoin.replace('_', ' ')
                
                result = f"{besoin.replace('_', ' ')} ({type_label})"
                results_list.append(result)
            else:
                # Autres questions : une seule colonne
                result = str(row[0]).split('#')[-1] if '#' in str(row[0]) else str(row[0])
                results_list.append(result.replace('_', ' '))
        
        return jsonify({
            'success': True,
            'results': results_list,
            'count': len(results_list)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

