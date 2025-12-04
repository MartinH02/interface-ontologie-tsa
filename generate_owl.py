#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour générer le fichier OWL à partir de l'ontologie décrite dans arborescence_onto3.md
"""

from xml.etree.ElementTree import Element, SubElement, tostring, QName
from xml.dom import minidom
import xml.etree.ElementTree as ET

def prettify(elem):
    """Retourne une chaîne XML formatée"""
    rough_string = ET.tostring(elem, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

# Namespace
NS = "http://example.org/ont/tsa-nlp#"
NS_PREFIX = "tsa"

# Enregistrer les namespaces pour éviter les conflits et utiliser les bons préfixes
ET.register_namespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
ET.register_namespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
ET.register_namespace('owl', 'http://www.w3.org/2002/07/owl#')
ET.register_namespace('xsd', 'http://www.w3.org/2001/XMLSchema#')

# Créer l'élément racine
# ElementTree génère automatiquement les namespaces (rdf, rdfs, owl) quand on utilise {namespace}Tag
# On ne doit donc pas les déclarer manuellement pour éviter les duplications
rdf = Element('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF')
rdf.set('{http://www.w3.org/XML/1998/namespace}base', NS)

# Déclarer uniquement les namespaces qui ne sont pas générés automatiquement
rdf.set('xmlns:xsd', 'http://www.w3.org/2001/XMLSchema#')
# Utiliser le namespace par défaut avec le # pour que les propriétés soient reconnues comme property assertions
rdf.set('xmlns', NS)

# Ontology header
ontology = SubElement(rdf, '{http://www.w3.org/2002/07/owl#}Ontology')
ontology.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', NS)
label_onto = SubElement(ontology, '{http://www.w3.org/2000/01/rdf-schema#}label')
label_onto.text = 'Ontologie TSA et Outils Numériques'

# ========== CLASSES ==========
classes = {
    'Personne': None,
    'PersonneTSA': 'Personne',
    'Parent': 'Personne',
    'Professionnel': 'Personne',
    'Orthophoniste': 'Professionnel',
    'Psychologue': 'Professionnel',
    'Enseignant': 'Professionnel',
    'TherapeuteQualifie': 'Professionnel',
    'AspectClinique': None,
    'TroubleAssocieTSA': 'AspectClinique',
    'Comportement': 'AspectClinique',
    'Besoin': 'AspectClinique',
    'BesoinsParents': 'Besoin',
    'BesoinsEnfantTSA': 'Besoin',
    'Intervention': 'AspectClinique',
    'Procedure': None,
    'OutilNumerique': None,
    'Applications': 'OutilNumerique',
    'RobotSocial': 'OutilNumerique',
    'SystemeCaptationMouvement': 'OutilNumerique',
    'SystemeVR_AR': 'OutilNumerique',
    'JeuSerieux': 'OutilNumerique',
    'SystemeMonitoring': 'OutilNumerique',
    'ObjetConnecte': 'OutilNumerique',
    'SystemePlanificationVisuelle': 'OutilNumerique',
    'OutilEvaluation': 'OutilNumerique',
    'SupportNumerique': None,
    'Technologies': None,
    'TechnologieNLP': 'Technologies',
    'TechnologieVision': 'Technologies',
    'TechnologieMouvement': 'Technologies',
    'RealiteAugmentee': 'Technologies',
    'RealiteVirtuelle': 'Technologies',
    'IntelligenceArtificielleConversationnelle': 'Technologies',
    'InterfaceCerveauOrdinateur': 'Technologies',
    'DomaineClinique': None,
    'DispositifCAA': None,
}

# Créer les classes
for class_name, parent in classes.items():
    cls = SubElement(rdf, '{http://www.w3.org/2002/07/owl#}Class')
    cls.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', f'{NS}{class_name}')
    label = SubElement(cls, '{http://www.w3.org/2000/01/rdf-schema#}label')
    label.text = class_name
    if parent:
        subClassOf = SubElement(cls, '{http://www.w3.org/2000/01/rdf-schema#}subClassOf')
        subClassOf.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', f'{NS}{parent}')

# Ajouter les classes individuelles pour DomaineClinique
domaine_classes = ['Neurologie', 'Kinesitherapie', 'Orthophonie', 'Psychologie', 
                   'Ergotherapie', 'Psychomotricite', 'Pedopsychiatrie']
for dc in domaine_classes:
    cls = SubElement(rdf, '{http://www.w3.org/2002/07/owl#}Class')
    cls.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', f'{NS}{dc}')
    label = SubElement(cls, '{http://www.w3.org/2000/01/rdf-schema#}label')
    label.text = dc
    subClassOf = SubElement(cls, '{http://www.w3.org/2000/01/rdf-schema#}subClassOf')
    subClassOf.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', f'{NS}DomaineClinique')

# ========== OBJECT PROPERTIES ==========
object_properties = [
    'estParentDe', 'estSoutenuePar', 'estAidePar', 'suitIntervention', 'presenteTrouble',
    'aBesoinDe', 'utiliseSupport', 'utiliseOutilAvec', 'conduitIntervention', 'suitPersonneTSA',
    'recommandeOutil', 'evalueAvec', 'implementeTechnologie', 'repondABesoin', 'soutientIntervention',
    'utiliseDansIntervention', 'fonctionneSur', 'necessiteSupport', 'cibleComportement',
    'estMiseEnOeuvreParProcedure', 'utiliseOutil', 'conduitPar', 'concerneDomaine', 'utiliseTechnologie',
    'estLieATrouble', 'estCiblePar', 'estSatisfaitPar', 'estLieA', 'cadreIntervention',
    'doitEtreIntegreeDansOutil', 'estImplementeeDans', 'utiliseeDansIntervention', 'supporteOutil',
    'cibleParIntervention', 'evalueParDomaine'
]

for prop in object_properties:
    op = SubElement(rdf, '{http://www.w3.org/2002/07/owl#}ObjectProperty')
    op.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', f'{NS}{prop}')
    label = SubElement(op, '{http://www.w3.org/2000/01/rdf-schema#}label')
    label.text = prop

# ========== DATA PROPERTIES ==========
data_properties = [
    'description', 'lien', 'prix', 'dateCreation', 'langue', 'certificationMedicale',
    'accessibilite', 'age', 'dateNaissance', 'dateDiagnostic', 'niveauSeverite',
    'scoreADOS', 'scoreADI', 'langueMaternelle'
]

for prop in data_properties:
    dp = SubElement(rdf, '{http://www.w3.org/2002/07/owl#}DatatypeProperty')
    dp.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', f'{NS}{prop}')
    label = SubElement(dp, '{http://www.w3.org/2000/01/rdf-schema#}label')
    label.text = prop
    # S'assurer que ce n'est PAS une AnnotationProperty (pour qu'elle apparaisse dans Property assertions)
    # En OWL 2, les DatatypeProperty ne sont pas des AnnotationProperty par défaut
    # Définir le type de données
    if prop in ['prix', 'scoreADOS', 'scoreADI']:
        range_elem = SubElement(dp, '{http://www.w3.org/2000/01/rdf-schema#}range')
        range_elem.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', 'http://www.w3.org/2001/XMLSchema#decimal')
    elif prop in ['age']:
        range_elem = SubElement(dp, '{http://www.w3.org/2000/01/rdf-schema#}range')
        range_elem.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', 'http://www.w3.org/2001/XMLSchema#integer')
    elif prop in ['dateCreation', 'dateNaissance', 'dateDiagnostic']:
        range_elem = SubElement(dp, '{http://www.w3.org/2000/01/rdf-schema#}range')
        range_elem.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', 'http://www.w3.org/2001/XMLSchema#date')
    elif prop in ['certificationMedicale']:
        range_elem = SubElement(dp, '{http://www.w3.org/2000/01/rdf-schema#}range')
        range_elem.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', 'http://www.w3.org/2001/XMLSchema#boolean')
    elif prop in ['lien']:
        range_elem = SubElement(dp, '{http://www.w3.org/2000/01/rdf-schema#}range')
        range_elem.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', 'http://www.w3.org/2001/XMLSchema#anyURI')
    else:
        range_elem = SubElement(dp, '{http://www.w3.org/2000/01/rdf-schema#}range')
        range_elem.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', 'http://www.w3.org/2001/XMLSchema#string')

# ========== INDIVIDUS ==========
# Cette partie sera très longue, je vais créer une fonction pour ajouter un individu
def add_individual(rdf, name, class_type, properties=None, object_props=None):
    """Ajoute un individu à l'ontologie"""
    indiv = SubElement(rdf, '{http://www.w3.org/2002/07/owl#}NamedIndividual')
    indiv.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', f'{NS}{name}')
    
    # Type
    type_elem = SubElement(indiv, '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}type')
    type_elem.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', f'{NS}{class_type}')
    
    # Data properties
    if properties:
        for prop, value in properties.items():
            # Utiliser QName pour forcer l'utilisation du namespace par défaut
            # Le namespace par défaut est déclaré avec xmlns="http://example.org/ont/tsa-nlp#"
            # QName permet d'utiliser le namespace par défaut sans préfixe
            prop_elem = SubElement(indiv, QName(NS, prop))
            if isinstance(value, bool):
                prop_elem.text = str(value).lower()
            elif isinstance(value, (int, float)):
                prop_elem.text = str(value)
            else:
                prop_elem.text = str(value)
    
    # Object properties
    if object_props:
        for prop, targets in object_props.items():
            if not isinstance(targets, list):
                targets = [targets]
            for target in targets:
                # Utiliser QName pour forcer l'utilisation du namespace par défaut
                prop_elem = SubElement(indiv, QName(NS, prop))
                prop_elem.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', f'{NS}{target}')

# Personnes TSA
add_individual(rdf, 'Lucas_TSA', 'PersonneTSA', {
    'description': 'Enfant avec trouble du spectre de l\'autisme nécessitant un accompagnement spécialisé pour la communication et la motricité',
    'age': 8,
    'dateNaissance': '2016-03-15',
    'dateDiagnostic': '2019-06-20',
    'niveauSeverite': 'modéré',
    'scoreADOS': 12.5,
    'langueMaternelle': 'français'
}, {
    'estAidePar': ['Proloquo2Go', 'RobotNAO', 'Kinect', 'Auticiel_Agenda'],
    'suitIntervention': ['ExerciceCommunicationVerbale', 'ExerciceMotricite'],
    'presenteTrouble': ['TroubleCommunicationVerbale', 'TroubleMoteur'],
    'aBesoinDe': ['Besoin_CommunicationVerbale', 'Besoin_Motricite'],
    'utiliseSupport': ['Tablette', 'Smartphone']
})

add_individual(rdf, 'Eve_TSA', 'PersonneTSA', {
    'description': 'Enfant avec trouble du spectre de l\'autisme nécessitant un accompagnement spécialisé pour les compétences sociales et cognitives',
    'age': 10,
    'dateNaissance': '2014-07-22',
    'dateDiagnostic': '2017-11-10',
    'niveauSeverite': 'léger',
    'scoreADOS': 8.3,
    'langueMaternelle': 'français'
}, {
    'estAidePar': ['AppAutismeSpeech', 'Pepper', 'Oculus_Quest'],
    'suitIntervention': ['ExerciceSocial', 'ExerciceCognitif'],
    'presenteTrouble': ['TroubleSocial', 'TroubleCognitif'],
    'aBesoinDe': ['Besoin_Social', 'Besoin_Cognitif'],
    'utiliseSupport': ['Tablette', 'Ordinateur']
})

# Parents
for parent_name in ['Parent_Lucas1', 'Parent_Lucas2', 'Parent_Eve1', 'Parent_Eve2']:
    add_individual(rdf, parent_name, 'Parent')

# Relations parent-enfant
add_individual(rdf, 'Parent_Lucas1', 'Parent', object_props={'estParentDe': 'Lucas_TSA'})
add_individual(rdf, 'Parent_Lucas2', 'Parent', object_props={'estParentDe': 'Lucas_TSA'})
add_individual(rdf, 'Parent_Eve1', 'Parent', object_props={'estParentDe': 'Eve_TSA'})
add_individual(rdf, 'Parent_Eve2', 'Parent', object_props={'estParentDe': 'Eve_TSA'})

# Relations parent-outil (utiliseOutilAvec) - sera ajouté après la définition de add_relation_to_individual
parent_outils = {
    'Parent_Lucas1': ['BehaviorTracker_Pro', 'Proloquo2Go', 'Auticiel_Agenda'],
    'Parent_Lucas2': ['BehaviorTracker_Pro', 'Auticiel_Agenda'],
    'Parent_Eve1': ['ABC_Data_Collector', 'Otsimo_Progress_Tracker'],
    'Parent_Eve2': ['TSARA', 'Otsimo_Progress_Tracker']
}

# Professionnels
professionnels = {
    'DrMartin': 'Orthophoniste',
    'DrNaya': 'Orthophoniste',
    'Psychologue_Francois': 'Psychologue',
    'Psychologue_Jean': 'Psychologue',
    'Enseignant_Pierre': 'Enseignant',
    'Enseignant_Paul': 'Enseignant',
    'Therapeute_Laurent': 'TherapeuteQualifie',
    'Therapeute_Marie': 'TherapeuteQualifie'
}

for prof_name, prof_type in professionnels.items():
    add_individual(rdf, prof_name, prof_type)

# Relations professionnels
prof_relations = {
    'DrMartin': {'suitPersonneTSA': 'Lucas_TSA', 'estSoutenuePar': 'Lucas_TSA', 'conduitIntervention': 'ExerciceCommunicationVerbale', 'recommandeOutil': ['Proloquo2Go', 'GoTalk_Now'], 'evalueAvec': 'EchelleBOT2'},
    'DrNaya': {'suitPersonneTSA': 'Eve_TSA', 'estSoutenuePar': 'Eve_TSA', 'conduitIntervention': 'ExerciceCommunicationNonVerbale', 'recommandeOutil': ['AppAutismeSpeech', 'Pictello']},
    'Psychologue_Francois': {'suitPersonneTSA': 'Lucas_TSA', 'estSoutenuePar': 'Lucas_TSA', 'conduitIntervention': 'ExerciceSocial', 'recommandeOutil': ['RobotNAO', 'TSARA']},
    'Psychologue_Jean': {'suitPersonneTSA': 'Eve_TSA', 'estSoutenuePar': 'Eve_TSA', 'conduitIntervention': 'ExerciceCognitif', 'recommandeOutil': 'Pepper'},
    'Enseignant_Pierre': {'suitPersonneTSA': 'Lucas_TSA'},
    'Enseignant_Paul': {'suitPersonneTSA': 'Eve_TSA'},
    'Therapeute_Laurent': {'conduitIntervention': 'ExerciceMotricite', 'recommandeOutil': ['Kinect', 'Leap_Motion'], 'evalueAvec': ['EchelleBOT2', 'EchelleDCDQ']},
    'Therapeute_Marie': {'conduitIntervention': 'ExerciceEmotionnel', 'recommandeOutil': 'Oculus_Quest'}
}

# Ajouter les relations pour les professionnels
for prof, relations in prof_relations.items():
    prof_uri = f'{NS}{prof}'
    for elem in rdf.findall(f'.//{{http://www.w3.org/2002/07/owl#}}NamedIndividual[@{{http://www.w3.org/1999/02/22-rdf-syntax-ns#}}about="{{prof_uri}}"]'):
        for prop, targets in relations.items():
            if not isinstance(targets, list):
                targets = [targets]
            for target in targets:
                prop_elem = SubElement(elem, QName(NS, prop))
                prop_elem.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', f'{NS}{target}')

# Continuer avec les autres individus... (cette partie sera très longue)
# Pour l'instant, je vais créer les individus principaux et les relations principales

# Troubles
troubles = ['TroubleCommunication', 'TroubleCommunicationVerbale', 'TroubleCommunicationNonVerbale', 
            'TroubleMoteur', 'TroubleSocial', 'TroubleCognitif', 'TroubleEmotionnel']
for trouble in troubles:
    add_individual(rdf, trouble, 'TroubleAssocieTSA')

# Comportements
comportements = ['ComportementCommunicationVerbale', 'ComportementCommunicationNonVerbale',
                 'ComportementMotricite', 'ComportementSocial', 'ComportementCognitif', 'ComportementEmotionnel']
for comport in comportements:
    add_individual(rdf, comport, 'Comportement')

# Besoins
besoins = ['Besoin_Compréhension', 'Besoin_DetectionAutismeRapide', 'Besoin_CommunicationVerbale',
           'Besoin_CommunicationNonVerbale', 'Besoin_Motricite', 'Besoin_Social', 'Besoin_Cognitif', 'Besoin_Emotionnel']
for besoin in besoins:
    if besoin in ['Besoin_Compréhension', 'Besoin_DetectionAutismeRapide']:
        add_individual(rdf, besoin, 'BesoinsParents')
    else:
        add_individual(rdf, besoin, 'BesoinsEnfantTSA')

# Interventions
interventions = ['ExerciceCommunicationVerbale', 'ExerciceCommunicationNonVerbale', 'ExerciceMotricite',
                 'ExerciceSocial', 'ExerciceCognitif', 'ExerciceEmotionnel']
for interv in interventions:
    add_individual(rdf, interv, 'Intervention')

# Relations interventions
interv_relations = {
    'ExerciceCommunicationVerbale': {'cibleComportement': 'ComportementCommunicationVerbale', 'estMiseEnOeuvreParProcedure': 'ABA', 'conduitPar': 'DrMartin', 'concerneDomaine': 'Orthophonie', 'utiliseTechnologie': ['TraitementLangageNaturel', 'ReconnaissanceVocale'], 'utiliseOutil': ['Proloquo2Go', 'AppAutismeSpeech', 'Pepper']},
    'ExerciceCommunicationNonVerbale': {'cibleComportement': 'ComportementCommunicationNonVerbale', 'estMiseEnOeuvreParProcedure': 'ABA', 'conduitPar': 'DrNaya', 'concerneDomaine': 'Orthophonie'},
    'ExerciceMotricite': {'cibleComportement': 'ComportementMotricite', 'estMiseEnOeuvreParProcedure': 'ABA', 'conduitPar': 'Therapeute_Laurent', 'concerneDomaine': ['Kinesitherapie', 'Psychomotricite'], 'utiliseTechnologie': ['AnalyseMarche', 'ReconnaissanceGestes'], 'utiliseOutil': ['Kinect', 'Leap_Motion']},
    'ExerciceSocial': {'cibleComportement': 'ComportementSocial', 'estMiseEnOeuvreParProcedure': 'ABA', 'conduitPar': 'Psychologue_Francois', 'concerneDomaine': 'Psychologie', 'utiliseTechnologie': ['ReconnaissanceFaciale', 'DetectionEmotionsFaciales'], 'utiliseOutil': ['RobotNAO', 'Pepper', 'Oculus_Quest']},
    'ExerciceCognitif': {'cibleComportement': 'ComportementCognitif', 'estMiseEnOeuvreParProcedure': 'ABA', 'conduitPar': 'Psychologue_Jean', 'concerneDomaine': 'Psychologie', 'utiliseTechnologie': 'TraitementLangageNaturel', 'utiliseOutil': ['Oculus_Quest', 'AppAutismeSpeech']},
    'ExerciceEmotionnel': {'cibleComportement': 'ComportementEmotionnel', 'estMiseEnOeuvreParProcedure': 'ABA', 'conduitPar': 'Therapeute_Marie', 'concerneDomaine': ['Psychologie', 'Pedopsychiatrie'], 'utiliseTechnologie': 'DetectionEmotionsFaciales'}
}

for interv, relations in interv_relations.items():
    interv_uri = f'{NS}{interv}'
    for elem in rdf.findall(f'.//{{http://www.w3.org/2002/07/owl#}}NamedIndividual[@{{http://www.w3.org/1999/02/22-rdf-syntax-ns#}}about="{{interv_uri}}"]'):
        for prop, targets in relations.items():
            if not isinstance(targets, list):
                targets = [targets]
            for target in targets:
                prop_elem = SubElement(elem, QName(NS, prop))
                prop_elem.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', f'{NS}{target}')

# Procedure
add_individual(rdf, 'ABA', 'Procedure', {
    'description': 'Applied Behavior Analysis - Méthode d\'intervention comportementale intensive basée sur les principes de l\'analyse appliquée du comportement, utilisée pour enseigner des compétences et réduire les comportements problématiques chez les personnes avec TSA. Cette procédure structure les interventions en étapes mesurables et utilise le renforcement positif pour favoriser l\'apprentissage',
    'lien': 'https://dumas.ccsd.cnrs.fr/dumas-02101558/file/Bordenave%20Sophie.%20M%C3%A9moire.%20Orthophonie.%20%28UPJV%29.pdf'
}, {
    'cadreIntervention': ['ExerciceCommunicationVerbale', 'ExerciceSocial', 'ExerciceCognitif', 'ExerciceMotricite', 'ExerciceEmotionnel'],
    'doitEtreIntegreeDansOutil': ['BehaviorTracker_Pro', 'ABC_Data_Collector']
})

# Supports numériques
supports = ['Tablette', 'Smartphone', 'Ordinateur', 'Tableau_Intéractif_Haptique']
for support in supports:
    add_individual(rdf, support, 'SupportNumerique')

# Technologies
technologies_data = {
    'ReconnaissanceVocale': 'TechnologieNLP',
    'SyntheseVocale': 'TechnologieNLP',
    'TraitementLangageNaturel': 'TechnologieNLP',
    'ReconnaissanceGestesVocaux': 'TechnologieNLP',
    'ReconnaissanceFaciale': 'TechnologieVision',
    'DetectionEmotionsFaciales': 'TechnologieVision',
    'SuiviRegard': 'TechnologieVision',
    'ReconnaissanceGestes': 'TechnologieVision',
    'DetectionPostures': 'TechnologieVision',
    'AnalyseMarche': 'TechnologieMouvement',
    'DetectionStereotypies': 'TechnologieMouvement',
    'AR': 'RealiteAugmentee',
    'VR': 'RealiteVirtuelle',
    'EarlyBot': 'IntelligenceArtificielleConversationnelle',
    'BCI_Communication': 'InterfaceCerveauOrdinateur'
}

for tech, tech_type in technologies_data.items():
    add_individual(rdf, tech, tech_type)

# Domaines cliniques
for domaine in domaine_classes:
    add_individual(rdf, domaine, domaine)

# Dispositifs CAA
dispositifs = {
    'PECS': 'Picture Exchange Communication System - Système de communication par échange d\'images développé spécifiquement pour les personnes avec autisme. Méthode structurée en 6 phases permettant d\'enseigner la communication fonctionnelle via l\'échange de pictogrammes. Favorise l\'initiation de la communication et peut servir de base pour développer le langage verbal',
    'Makaton': 'Programme de communication multimodale combinant la parole, les signes et les symboles visuels. Utilisé pour soutenir la communication des personnes avec TSA en associant des gestes signés à la parole et des pictogrammes, facilitant ainsi la compréhension et l\'expression',
    'Tableaux_Communication': 'Supports visuels personnalisables contenant des pictogrammes, photos ou symboles organisés thématiquement. Permettent aux personnes avec TSA de pointer ou sélectionner des éléments pour communiquer leurs besoins, pensées et émotions. Peuvent être de basse technologie (papier) ou haute technologie (numérique)'
}

for disp, desc in dispositifs.items():
    add_individual(rdf, disp, 'DispositifCAA', {'description': desc})

# Outils numériques - Applications
outils_apps = {
    'Proloquo2Go': {'class': 'Applications', 'description': 'Application de communication alternative et augmentée (CAA) sur iPad permettant aux personnes non verbales ou ayant des difficultés de communication de s\'exprimer via des symboles visuels et une synthèse vocale. Personnalisable avec des grilles de communication adaptées, elle facilite l\'expression des besoins, pensées et émotions pour les personnes avec TSA', 'lien': 'file:///C:/Users/halbo/Downloads/SennottBowker2009ASHAPerspectivesonAAC.pdf', 'prix': 249.99, 'dateCreation': '2009-01-01', 'langue': 'français, anglais, espagnol', 'certificationMedicale': True, 'accessibilite': 'élevé'},
    'iCAN': {'class': 'Applications', 'description': 'Application mobile utilisant le traitement du langage naturel et la reconnaissance vocale pour aider les enfants avec TSA à améliorer leurs compétences de communication. L\'application propose des exercices interactifs adaptés aux besoins individuels', 'lien': 'file:///C:/Users/halbo/Documents/Cours_A25/IA03/Veille/Articles/Article%2019/1-s2.0-S107158191400086X-main.pdf', 'prix': 0.0, 'dateCreation': '2014-01-01', 'langue': 'anglais', 'certificationMedicale': False, 'accessibilite': 'modéré'},
    'AppAutismeSpeech': {'class': 'Applications', 'description': 'Application spécialisée utilisant le traitement du langage naturel et la reconnaissance vocale pour soutenir le développement du langage et de la communication chez les enfants avec TSA. Elle propose des exercices structurés et progressifs', 'lien': 'file:///C:/Users/halbo/Documents/Cours_A25/IA03/Veille/Articles/Articels_veille_que_ai_lu/children-08-01001.pdf', 'prix': 0.0, 'dateCreation': '2021-01-01', 'langue': 'français, anglais', 'certificationMedicale': False, 'accessibilite': 'modéré'},
    'SIGUEME': {'class': 'Applications', 'description': 'Application utilisant la reconnaissance faciale et le suivi du regard pour aider les enfants avec TSA à améliorer leurs compétences d\'attention conjointe et de communication sociale. L\'application suit les mouvements oculaires et les expressions faciales pour adapter les interactions', 'lien': 'file:///C:/Users/halbo/Documents/Cours_A25/IA03/Veille/Articles/Article%2020/children-08-01001.pdf', 'prix': 0.0, 'dateCreation': '2020-01-01', 'langue': 'espagnol', 'certificationMedicale': False, 'accessibilite': 'modéré'},
    'AutisMate': {'class': 'Applications', 'description': 'Application de communication et d\'apprentissage utilisant le traitement du langage naturel et la synthèse vocale pour créer des scénarios sociaux personnalisés et des exercices de communication adaptés aux besoins des personnes avec TSA', 'lien': 'https://www.researchgate.net/publication/333965915_Exploring_the_Effects_of_the_AutisMate_Application_on_a_12_year-old_boy_with_ASD_-_A_Case_Study', 'prix': 19.99, 'dateCreation': '2018-01-01', 'langue': 'anglais', 'certificationMedicale': False, 'accessibilite': 'modéré'},
    'GoTalk_Now': {'class': 'Applications', 'description': 'Application de communication alternative utilisant la synthèse vocale pour permettre aux personnes avec TSA de communiquer via des tableaux de communication personnalisables avec images, photos et symboles. Facilite l\'expression des besoins quotidiens', 'lien': 'file:///C:/Users/halbo/Documents/Cours_A25/IA03/Veille/Articles/Article%2021/MuharibCorreaWoodHaughneyAheadofPrint2018-1.pdf', 'prix': 79.99, 'dateCreation': '2012-01-01', 'langue': 'anglais', 'certificationMedicale': True, 'accessibilite': 'élevé'},
    'Pictello': {'class': 'Applications', 'description': 'Application de création d\'histoires visuelles et sociales utilisant la synthèse vocale pour créer des récits personnalisés avec photos, vidéos et texte. Aide les personnes avec TSA à comprendre les situations sociales et à développer leurs compétences narratives', 'lien': 'https://www.autisme-france.fr/f/8cb314444237c2c02f7cf1010d82d48793cf1133/SYNTHESE_NTIC.pdf', 'prix': 24.99, 'dateCreation': '2011-01-01', 'langue': 'français, anglais', 'certificationMedicale': False, 'accessibilite': 'élevé'}
}

# Fonction pour ajouter un outil avec toutes ses propriétés
def add_outil(outil_name, data):
    props = {k: v for k, v in data.items() if k != 'class' and k != 'object_props'}
    obj_props = data.get('object_props', {})
    add_individual(rdf, outil_name, data['class'], props, obj_props)

# Ajouter les applications avec leurs relations
for outil, data in outils_apps.items():
    add_outil(outil, data)

# Robots Sociaux
outils_robots = {
    'RobotNAO': {'class': 'RobotSocial', 'description': 'Robot humanoïde programmable de 58 cm de hauteur équipé de reconnaissance faciale et de détection d\'émotions faciales. Utilisé en thérapie pour améliorer les compétences sociales, la communication et les interactions des enfants avec TSA. Le robot propose des activités structurées et adaptatives', 'lien': 'https://hal.science/hal-04327431/document', 'prix': 10000.0, 'dateCreation': '2008-01-01', 'langue': 'français, anglais', 'certificationMedicale': False, 'accessibilite': 'modéré'},
    'Pepper': {'class': 'RobotSocial', 'description': 'Robot humanoïde social de 120 cm équipé de reconnaissance faciale et de traitement du langage naturel. Utilisé pour faciliter les interactions sociales et la communication chez les personnes avec TSA. Le robot peut engager des conversations et adapter son comportement', 'lien': 'file:///C:/Users/halbo/Documents/Cours_A25/IA03/Veille/Articles/Article%2022/Using_the_power_of_memes_The_Pepper_Robot_as_a_com.pdf', 'prix': 25000.0, 'dateCreation': '2014-01-01', 'langue': 'français, anglais', 'certificationMedicale': False, 'accessibilite': 'modéré'},
    'Kaspar': {'class': 'RobotSocial', 'description': 'Robot humanoïde de taille enfant conçu spécifiquement pour l\'intervention auprès d\'enfants avec autisme. Équipé de reconnaissance faciale et de détection d\'émotions, il aide à développer les compétences sociales et émotionnelles dans un environnement sécurisé et prévisible', 'lien': 'file:///C:/Users/halbo/Documents/Cours_A25/IA03/Veille/Articles/Article%2023/TheIterativeDevelopmentoftheHumanoidRobotKaspar-AnAssistiveRobotforChildrenwithAutism.pdf', 'prix': 15000.0, 'dateCreation': '2005-01-01', 'langue': 'anglais', 'certificationMedicale': False, 'accessibilite': 'modéré'},
    'Keepon': {'class': 'RobotSocial', 'description': 'Robot interactif simple et expressif conçu pour l\'intervention sociale auprès d\'enfants avec TSA. Sa simplicité et sa capacité à exprimer des émotions de base en font un outil efficace pour travailler l\'attention conjointe et les interactions sociales', 'prix': 250.0, 'dateCreation': '2007-01-01', 'langue': 'anglais', 'certificationMedicale': False, 'accessibilite': 'élevé'},
    'Milo': {'class': 'RobotSocial', 'description': 'Robot éducatif humanoïde conçu pour enseigner les compétences sociales aux enfants avec TSA. Utilise le traitement du langage naturel et la reconnaissance faciale pour créer des interactions structurées et progressives visant à améliorer la communication et les relations sociales', 'prix': 7500.0, 'dateCreation': '2015-01-01', 'langue': 'anglais', 'certificationMedicale': False, 'accessibilite': 'modéré'}
}

for outil, data in outils_robots.items():
    add_outil(outil, data)

# Systèmes de Captation de Mouvement
outils_mouvement = {
    'Kinect': {'class': 'SystemeCaptationMouvement', 'description': 'Système de captation de mouvement sans contact utilisant des caméras infrarouges pour suivre les mouvements du corps entier. Utilisé en thérapie motrice pour évaluer et entraîner la connaissance du corps, la coordination et la motricité globale chez les personnes avec TSA via des jeux interactifs', 'lien': 'file:///C:/Users/halbo/Downloads/nadel-2018-evaluer-et-entrainer-la-connaissance-du-corps-dans-lautisme-via-kinect-et-pictogram-room.pdf', 'prix': 100.0, 'dateCreation': '2010-01-01', 'langue': 'multilingue', 'certificationMedicale': False, 'accessibilite': 'modéré'},
    'Leap_Motion': {'class': 'SystemeCaptationMouvement', 'description': 'Capteur de mouvement des mains utilisant des caméras infrarouges pour suivre précisément les mouvements des doigts et des mains. Utilisé pour développer la motricité fine chez les enfants avec TSA à travers des jeux de correspondance et des exercices interactifs adaptés', 'lien': 'file:///C:/Users/halbo/Documents/Cours_A25/IA03/Veille/Articles/Article%2025/ASeriesofLeapMotion-BasedMatchingGamesforEnhancingtheFineMotorSkillsofChildrenwithAutism.pdf', 'prix': 80.0, 'dateCreation': '2012-01-01', 'langue': 'anglais', 'certificationMedicale': False, 'accessibilite': 'modéré'},
    'Myo_Armband': {'class': 'SystemeCaptationMouvement', 'description': 'Bracelet connecté captant les mouvements du bras et de la main via des capteurs électromyographiques et inertiels. Utilisé pour l\'entraînement et la rééducation de la motricité fine et des mouvements de la main chez les personnes avec TSA, avec retour en temps réel', 'lien': 'file:///C:/Users/halbo/Documents/Cours_A25/IA03/Veille/Articles/Article%2026/Recognition_of_Hand_Movement_for_Training_Motor_Sk.pdf', 'prix': 200.0, 'dateCreation': '2014-01-01', 'langue': 'anglais', 'certificationMedicale': False, 'accessibilite': 'modéré'}
}

for outil, data in outils_mouvement.items():
    add_outil(outil, data)

# Systèmes VR/AR
outils_vr_ar = {
    'Oculus_Quest': {'class': 'SystemeVR_AR', 'description': 'Casque de réalité virtuelle autonome permettant de créer des environnements immersifs contrôlés pour l\'entraînement des compétences sociales et cognitives chez les personnes avec TSA. Offre un environnement sécurisé pour pratiquer des situations sociales complexes', 'lien': 'file:///C:/Users/halbo/Documents/Cours_A25/IA03/Veille/Articles/Article%2027/fpubh-13-1628741.pdf', 'prix': 350.0, 'dateCreation': '2019-01-01', 'langue': 'multilingue', 'certificationMedicale': False, 'accessibilite': 'modéré'},
    'Microsoft_HoloLens': {'class': 'SystemeVR_AR', 'description': 'Casque de réalité augmentée permettant de superposer des informations numériques sur l\'environnement réel. Utilisé pour l\'entraînement des compétences motrices et sociales chez les personnes avec TSA, offrant des guidages visuels et des retours adaptés en temps réel', 'lien': 'file:///C:/Users/halbo/Documents/Cours_A25/IA03/Veille/Articles/Article%2027/fpubh-13-1628741.pdf', 'prix': 3500.0, 'dateCreation': '2016-01-01', 'langue': 'multilingue', 'certificationMedicale': False, 'accessibilite': 'faible'}
}

for outil, data in outils_vr_ar.items():
    add_outil(outil, data)

# Jeux Sérieux
outils_jeux = {
    'TSARA': {'class': 'JeuSerieux', 'description': 'Jeu sérieux éducatif en ligne conçu pour sensibiliser et former les professionnels et le grand public à la compréhension de l\'autisme. Propose des scénarios interactifs pour mieux comprendre les défis quotidiens des personnes avec TSA', 'lien': 'https://www.tsara-autisme.com/', 'prix': 0.0, 'dateCreation': '2015-01-01', 'langue': 'français', 'certificationMedicale': False, 'accessibilite': 'élevé'},
    'SmileMaze': {'class': 'JeuSerieux', 'description': 'Jeu sérieux conçu pour améliorer les compétences sociales et émotionnelles des enfants avec TSA. Utilise des mécaniques de jeu adaptées pour enseigner la reconnaissance des émotions et les interactions sociales de manière ludique', 'lien': 'file:///C:/Users/halbo/Documents/Cours_A25/IA03/Veille/Articles/Article%2028/Cockburn_FG2008.pdf', 'prix': 0.0, 'dateCreation': '2008-01-01', 'langue': 'anglais', 'certificationMedicale': False, 'accessibilite': 'modéré'}
}

for outil, data in outils_jeux.items():
    add_outil(outil, data)

# Systèmes de Monitoring
outils_monitoring = {
    'BehaviorTracker_Pro': {'class': 'SystemeMonitoring', 'description': 'Application mobile professionnelle permettant de suivre et analyser les comportements des personnes avec TSA. Permet l\'enregistrement en temps réel, l\'analyse des données comportementales et la génération de rapports pour les professionnels et les familles', 'lien': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC3120079/pdf/jaba-44-02-393.pdf', 'prix': 49.99, 'dateCreation': '2011-01-01', 'langue': 'anglais', 'certificationMedicale': True, 'accessibilite': 'modéré'},
    'ABC_Data_Collector': {'class': 'SystemeMonitoring', 'description': 'Application de collecte de données comportementales utilisant le modèle ABC (Antécédent-Comportement-Conséquence) pour analyser les comportements des personnes avec TSA. Facilite l\'identification des déclencheurs et des conséquences pour adapter les interventions', 'lien': 'file:///C:/Users/halbo/Documents/Cours_A25/IA03/Veille/Articles/Article%2029/1-s2.0-S0891422213002308-main.pdf', 'prix': 0.0, 'dateCreation': '2013-01-01', 'langue': 'anglais', 'certificationMedicale': False, 'accessibilite': 'modéré'},
    'Otsimo_Progress_Tracker': {'class': 'SystemeMonitoring', 'description': 'Système de suivi des progrès intégré à la plateforme Otsimo permettant de monitorer l\'évolution des compétences des enfants avec TSA. Génère des rapports détaillés sur les progrès dans différents domaines d\'apprentissage', 'lien': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC9222948/pdf/ijerph-19-07019.pdf', 'prix': 0.0, 'dateCreation': '2020-01-01', 'langue': 'anglais, turc', 'certificationMedicale': False, 'accessibilite': 'modéré'}
}

for outil, data in outils_monitoring.items():
    add_outil(outil, data)

# Objets Connectés
outils_connectes = {
    'Apple_Watch_TSA': {'class': 'ObjetConnecte', 'description': 'Montre connectée adaptée pour le suivi des personnes avec TSA, permettant de monitorer l\'activité physique, le sommeil, le stress et les comportements. Peut envoyer des alertes et des rappels pour faciliter l\'autonomie et la sécurité', 'lien': 'https://scholarshare.temple.edu/server/api/core/bitstreams/e6d6a875-f051-4df8-8be7-a1eb37af00b0/content', 'prix': 429.0, 'dateCreation': '2015-01-01', 'langue': 'multilingue', 'certificationMedicale': False, 'accessibilite': 'modéré'},
    'Garmin_Vivosmart_TSA': {'class': 'ObjetConnecte', 'description': 'Bracelet d\'activité connecté utilisé pour le suivi physiologique des personnes avec TSA. Mesure l\'activité physique, la fréquence cardiaque, le sommeil et peut détecter des patterns de stress ou d\'anxiété pour adapter les interventions', 'lien': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC6308558/pdf/sensors-18-04271.pdf', 'prix': 150.0, 'dateCreation': '2016-01-01', 'langue': 'multilingue', 'certificationMedicale': False, 'accessibilite': 'modéré'}
}

for outil, data in outils_connectes.items():
    add_outil(outil, data)

# Systèmes de Planification Visuelle
outils_planif = {
    'Auticiel_Agenda': {'class': 'SystemePlanificationVisuelle', 'description': 'Application d\'agenda visuel conçue spécifiquement pour les personnes avec TSA. Permet de structurer le temps avec des pictogrammes, des photos et des séquences visuelles pour réduire l\'anxiété et améliorer l\'autonomie dans la gestion des activités quotidiennes', 'lien': 'https://www.auticiel.com/fr/agenda/', 'prix': 9.99, 'dateCreation': '2014-01-01', 'langue': 'français', 'certificationMedicale': False, 'accessibilite': 'élevé'}
}

for outil, data in outils_planif.items():
    add_outil(outil, data)

# Outils d'Evaluation
outils_eval = {
    'EchelleBOT2': {'class': 'OutilEvaluation'},
    'EchelleDCDQ': {'class': 'OutilEvaluation'}
}

for outil, data in outils_eval.items():
    add_outil(outil, data)

# Fonction pour ajouter des relations à un individu existant
def add_relation_to_individual(rdf, indiv_name, prop_name, target_name):
    """Ajoute une relation object property à un individu existant"""
    indiv_uri = f'{NS}{indiv_name}'
    target_uri = f'{NS}{target_name}'
    # Utiliser QName pour forcer l'utilisation du namespace par défaut
    prop_qname = QName(NS, prop_name)
    # Rechercher l'individu avec le bon format XPath
    xpath_query = f'.//{{http://www.w3.org/2002/07/owl#}}NamedIndividual[@{{http://www.w3.org/1999/02/22-rdf-syntax-ns#}}about="{indiv_uri}"]'
    elems = rdf.findall(xpath_query)
    if not elems:
        print(f"ATTENTION: Individu '{indiv_name}' non trouvé pour ajouter la relation '{prop_name}' vers '{target_name}'")
        return
    for elem in elems:
        # Vérifier si la relation n'existe pas déjà
        # Chercher les relations existantes avec le même nom et la même cible
        existing = []
        for child in elem:
            # Comparer le tag (peut être une chaîne ou un QName)
            child_tag = str(child.tag) if hasattr(child.tag, '__str__') else child.tag
            prop_tag = str(prop_qname) if hasattr(prop_qname, '__str__') else prop_qname
            # Vérifier si le tag correspond (soit exactement, soit se termine par le nom de la propriété)
            if child_tag == prop_tag or (isinstance(child_tag, str) and child_tag.endswith(prop_name)):
                if child.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource') == target_uri:
                    existing.append(child)
        if not existing:
            prop_elem = SubElement(elem, prop_qname)
            prop_elem.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', target_uri)

# Ajouter toutes les relations implementeTechnologie
tech_relations = {
    'Proloquo2Go': ['ReconnaissanceVocale', 'SyntheseVocale'],
    'iCAN': ['TraitementLangageNaturel', 'ReconnaissanceVocale'],
    'AppAutismeSpeech': ['TraitementLangageNaturel', 'ReconnaissanceVocale'],
    'SIGUEME': ['ReconnaissanceFaciale', 'SuiviRegard'],
    'AutisMate': ['TraitementLangageNaturel', 'SyntheseVocale'],
    'GoTalk_Now': ['SyntheseVocale'],
    'Pictello': ['SyntheseVocale'],
    'RobotNAO': ['ReconnaissanceFaciale', 'DetectionEmotionsFaciales'],
    'Pepper': ['ReconnaissanceFaciale', 'TraitementLangageNaturel'],
    'Kaspar': ['ReconnaissanceFaciale', 'DetectionEmotionsFaciales'],
    'Keepon': ['DetectionEmotionsFaciales'],
    'Milo': ['TraitementLangageNaturel', 'ReconnaissanceFaciale'],
    'Kinect': ['ReconnaissanceGestes', 'DetectionPostures'],
    'Leap_Motion': ['ReconnaissanceGestes'],
    'Myo_Armband': ['AnalyseMarche'],
    'Oculus_Quest': ['VR'],
    'Microsoft_HoloLens': ['AR'],
    'EarlyBot': ['TraitementLangageNaturel']
}

for outil, techs in tech_relations.items():
    for tech in techs:
        add_relation_to_individual(rdf, outil, 'implementeTechnologie', tech)

# Ajouter les relations repondABesoin
besoin_relations = {
    'Proloquo2Go': ['Besoin_CommunicationVerbale'],
    'GoTalk_Now': ['Besoin_CommunicationVerbale'],
    'AppAutismeSpeech': ['Besoin_CommunicationVerbale'],
    'iCAN': ['Besoin_CommunicationVerbale'],
    'RobotNAO': ['Besoin_Social'],
    'Pepper': ['Besoin_Social'],
    'Kaspar': ['Besoin_Social'],
    'Kinect': ['Besoin_Motricite'],
    'Leap_Motion': ['Besoin_Motricite'],
    'Myo_Armband': ['Besoin_Motricite'],
    'Oculus_Quest': ['Besoin_Social', 'Besoin_Cognitif'],
    'Microsoft_HoloLens': ['Besoin_Motricite', 'Besoin_Social'],
    'TSARA': ['Besoin_Compréhension'],
    'Auticiel_Agenda': ['Besoin_Cognitif'],
    'BehaviorTracker_Pro': ['Besoin_DetectionAutismeRapide']
}

for outil, besoins in besoin_relations.items():
    for besoin in besoins:
        add_relation_to_individual(rdf, outil, 'repondABesoin', besoin)

# Ajouter les relations fonctionneSur
support_relations = {
    'Proloquo2Go': ['Tablette'],
    'iCAN': ['Smartphone', 'Tablette'],
    'AppAutismeSpeech': ['Tablette'],
    'SIGUEME': ['Tablette'],
    'AutisMate': ['Tablette'],
    'GoTalk_Now': ['Tablette'],
    'Pictello': ['Tablette'],
    'TSARA': ['Ordinateur', 'Tablette'],
    'BehaviorTracker_Pro': ['Smartphone', 'Tablette'],
    'ABC_Data_Collector': ['Smartphone'],
    'Otsimo_Progress_Tracker': ['Tablette'],
    'Auticiel_Agenda': ['Tablette', 'Smartphone']
}

for outil, supports in support_relations.items():
    for support in supports:
        add_relation_to_individual(rdf, outil, 'fonctionneSur', support)

# Ajouter les relations necessiteSupport
necessite_relations = {
    'Oculus_Quest': [],  # casque autonome
    'Microsoft_HoloLens': [],  # casque autonome
    'Kinect': ['Ordinateur'],
    'Leap_Motion': ['Ordinateur'],
    'Myo_Armband': ['Ordinateur'],
    'RobotNAO': [],  # robot autonome
    'Pepper': [],  # robot autonome
    'Kaspar': []  # robot autonome
}

for outil, supports in necessite_relations.items():
    for support in supports:
        add_relation_to_individual(rdf, outil, 'necessiteSupport', support)

# Ajouter les relations soutientIntervention et utiliseDansIntervention
intervention_relations = {
    'Proloquo2Go': {'soutientIntervention': ['ExerciceCommunicationVerbale'], 'utiliseDansIntervention': ['ExerciceCommunicationVerbale']},
    'AppAutismeSpeech': {'soutientIntervention': ['ExerciceCommunicationVerbale'], 'utiliseDansIntervention': ['ExerciceCommunicationVerbale', 'ExerciceCognitif']},
    'RobotNAO': {'soutientIntervention': ['ExerciceSocial'], 'utiliseDansIntervention': ['ExerciceSocial']},
    'Pepper': {'soutientIntervention': ['ExerciceSocial', 'ExerciceCommunicationVerbale'], 'utiliseDansIntervention': ['ExerciceSocial', 'ExerciceCommunicationVerbale']},
    'Kinect': {'soutientIntervention': ['ExerciceMotricite'], 'utiliseDansIntervention': ['ExerciceMotricite']},
    'Oculus_Quest': {'soutientIntervention': ['ExerciceSocial', 'ExerciceCognitif'], 'utiliseDansIntervention': ['ExerciceSocial', 'ExerciceCognitif']},
    'Microsoft_HoloLens': {'soutientIntervention': ['ExerciceMotricite', 'ExerciceSocial'], 'utiliseDansIntervention': ['ExerciceMotricite', 'ExerciceSocial']},
    'Auticiel_Agenda': {'soutientIntervention': ['ExerciceCognitif']}
}

for outil, relations in intervention_relations.items():
    for rel_type, interventions in relations.items():
        for interv in interventions:
            add_relation_to_individual(rdf, outil, rel_type, interv)

# Ajouter les relations estSatisfaitPar (inverse de repondABesoin)
for outil, besoins in besoin_relations.items():
    for besoin in besoins:
        add_relation_to_individual(rdf, besoin, 'estSatisfaitPar', outil)

# Ajouter les relations estLieA pour les besoins
besoin_domaine = {
    'Besoin_CommunicationVerbale': 'Orthophonie',
    'Besoin_CommunicationNonVerbale': 'Orthophonie',
    'Besoin_Motricite': ['Kinesitherapie', 'Psychomotricite'],
    'Besoin_Social': 'Psychologie',
    'Besoin_Cognitif': 'Psychologie',
    'Besoin_Emotionnel': ['Psychologie', 'Pedopsychiatrie']
}

for besoin, domaines in besoin_domaine.items():
    if isinstance(domaines, list):
        for domaine in domaines:
            add_relation_to_individual(rdf, besoin, 'estLieA', domaine)
    else:
        add_relation_to_individual(rdf, besoin, 'estLieA', domaines)

# Ajouter les relations estLieATrouble pour les comportements
comportement_trouble = {
    'ComportementCommunicationVerbale': 'TroubleCommunicationVerbale',
    'ComportementCommunicationNonVerbale': 'TroubleCommunicationNonVerbale',
    'ComportementMotricite': 'TroubleMoteur',
    'ComportementSocial': 'TroubleSocial',
    'ComportementCognitif': 'TroubleCognitif',
    'ComportementEmotionnel': 'TroubleEmotionnel'
}

for comport, trouble in comportement_trouble.items():
    add_relation_to_individual(rdf, comport, 'estLieATrouble', trouble)

# Ajouter les relations estCiblePar pour les comportements
comportement_intervention = {
    'ComportementCommunicationVerbale': 'ExerciceCommunicationVerbale',
    'ComportementCommunicationNonVerbale': 'ExerciceCommunicationNonVerbale',
    'ComportementMotricite': 'ExerciceMotricite',
    'ComportementSocial': 'ExerciceSocial',
    'ComportementCognitif': 'ExerciceCognitif',
    'ComportementEmotionnel': 'ExerciceEmotionnel'
}

for comport, interv in comportement_intervention.items():
    add_relation_to_individual(rdf, comport, 'estCiblePar', interv)

# Ajouter les relations estImplementeeDans (inverse de implementeTechnologie)
for outil, techs in tech_relations.items():
    for tech in techs:
        add_relation_to_individual(rdf, tech, 'estImplementeeDans', outil)

# Ajouter les relations utiliseeDansIntervention pour les technologies
tech_intervention = {
    'TraitementLangageNaturel': ['ExerciceCommunicationVerbale', 'ExerciceCognitif'],
    'ReconnaissanceVocale': ['ExerciceCommunicationVerbale'],
    'ReconnaissanceFaciale': ['ExerciceSocial'],
    'DetectionEmotionsFaciales': ['ExerciceSocial', 'ExerciceEmotionnel'],
    'AnalyseMarche': ['ExerciceMotricite'],
    'ReconnaissanceGestes': ['ExerciceMotricite']
}

for tech, interventions in tech_intervention.items():
    for interv in interventions:
        add_relation_to_individual(rdf, tech, 'utiliseeDansIntervention', interv)

# Ajouter les relations supporteOutil (inverse de fonctionneSur)
for outil, supports in support_relations.items():
    for support in supports:
        add_relation_to_individual(rdf, support, 'supporteOutil', outil)

# Ajouter les relations evalueParDomaine
domaine_eval = {
    'Kinesitherapie': 'EchelleBOT2',
    'Psychomotricite': ['EchelleBOT2', 'EchelleDCDQ']
}

for domaine, outils in domaine_eval.items():
    if isinstance(outils, list):
        for outil in outils:
            add_relation_to_individual(rdf, domaine, 'evalueParDomaine', outil)
    else:
        add_relation_to_individual(rdf, domaine, 'evalueParDomaine', outils)

# Ajouter les relations utiliseOutilAvec (Parent → OutilNumerique)
for parent, outils in parent_outils.items():
    for outil in outils:
        add_relation_to_individual(rdf, parent, 'utiliseOutilAvec', outil)

# Ajouter les relations estSoutenuePar (PersonneTSA → Professionnel)
soutien_relations = {
    'Lucas_TSA': ['DrMartin', 'Psychologue_Francois'],
    'Eve_TSA': ['DrNaya', 'Psychologue_Jean']
}

for personne, professionnels in soutien_relations.items():
    for pro in professionnels:
        add_relation_to_individual(rdf, personne, 'estSoutenuePar', pro)

# Ajouter les relations conduitIntervention (Professionnel → Intervention)
conduit_intervention = {
    'DrMartin': 'ExerciceCommunicationVerbale',
    'DrNaya': 'ExerciceCommunicationNonVerbale',
    'Psychologue_Francois': 'ExerciceSocial',
    'Psychologue_Jean': 'ExerciceCognitif',
    'Therapeute_Laurent': 'ExerciceMotricite',
    'Therapeute_Marie': 'ExerciceEmotionnel'
}

for pro, intervention in conduit_intervention.items():
    add_relation_to_individual(rdf, pro, 'conduitIntervention', intervention)

# Ajouter les relations suitPersonneTSA (Professionnel → PersonneTSA)
suit_personne = {
    'DrMartin': 'Lucas_TSA',
    'DrNaya': 'Eve_TSA',
    'Psychologue_Francois': 'Lucas_TSA',
    'Psychologue_Jean': 'Eve_TSA',
    'Enseignant_Pierre': 'Lucas_TSA',
    'Enseignant_Paul': 'Eve_TSA'
}

for pro, personne in suit_personne.items():
    add_relation_to_individual(rdf, pro, 'suitPersonneTSA', personne)

# Ajouter les relations recommandeOutil (Professionnel → OutilNumerique)
recommande_outil = {
    'DrMartin': ['Proloquo2Go', 'GoTalk_Now'],
    'DrNaya': ['AppAutismeSpeech', 'Pictello'],
    'Psychologue_Francois': ['RobotNAO', 'TSARA'],
    'Psychologue_Jean': 'Pepper',
    'Therapeute_Laurent': ['Kinect', 'Leap_Motion'],
    'Therapeute_Marie': 'Oculus_Quest'
}

for pro, outils in recommande_outil.items():
    if isinstance(outils, list):
        for outil in outils:
            add_relation_to_individual(rdf, pro, 'recommandeOutil', outil)
    else:
        add_relation_to_individual(rdf, pro, 'recommandeOutil', outils)

# Ajouter les relations evalueAvec (Professionnel → OutilEvaluation)
evalue_avec = {
    'DrMartin': 'EchelleBOT2',
    'Therapeute_Laurent': ['EchelleBOT2', 'EchelleDCDQ']
}

for pro, outils in evalue_avec.items():
    if isinstance(outils, list):
        for outil in outils:
            add_relation_to_individual(rdf, pro, 'evalueAvec', outil)
    else:
        add_relation_to_individual(rdf, pro, 'evalueAvec', outils)

# Ajouter les relations cibleComportement (Intervention → Comportement)
cible_comportement = {
    'ExerciceCommunicationVerbale': 'ComportementCommunicationVerbale',
    'ExerciceCommunicationNonVerbale': 'ComportementCommunicationNonVerbale',
    'ExerciceMotricite': 'ComportementMotricite',
    'ExerciceSocial': 'ComportementSocial',
    'ExerciceCognitif': 'ComportementCognitif',
    'ExerciceEmotionnel': 'ComportementEmotionnel'
}

for intervention, comportement in cible_comportement.items():
    add_relation_to_individual(rdf, intervention, 'cibleComportement', comportement)

# Ajouter les relations estMiseEnOeuvreParProcedure (Intervention → Procedure)
intervention_procedure = {
    'ExerciceCommunicationVerbale': 'ABA',
    'ExerciceCommunicationNonVerbale': 'ABA',
    'ExerciceSocial': 'ABA',
    'ExerciceCognitif': 'ABA',
    'ExerciceMotricite': 'ABA',
    'ExerciceEmotionnel': 'ABA'
}

for intervention, procedure in intervention_procedure.items():
    add_relation_to_individual(rdf, intervention, 'estMiseEnOeuvreParProcedure', procedure)

# Ajouter les relations utiliseOutil (Intervention → OutilNumerique)
intervention_outil = {
    'ExerciceCommunicationVerbale': ['Proloquo2Go', 'AppAutismeSpeech', 'Pepper'],
    'ExerciceSocial': ['RobotNAO', 'Pepper', 'Oculus_Quest'],
    'ExerciceMotricite': ['Kinect', 'Leap_Motion'],
    'ExerciceCognitif': ['Oculus_Quest', 'AppAutismeSpeech']
}

for intervention, outils in intervention_outil.items():
    for outil in outils:
        add_relation_to_individual(rdf, intervention, 'utiliseOutil', outil)

# Ajouter les relations conduitPar (Intervention → Professionnel)
intervention_pro = {
    'ExerciceCommunicationVerbale': 'DrMartin',
    'ExerciceCommunicationNonVerbale': 'DrNaya',
    'ExerciceSocial': 'Psychologue_Francois',
    'ExerciceCognitif': 'Psychologue_Jean',
    'ExerciceMotricite': 'Therapeute_Laurent',
    'ExerciceEmotionnel': 'Therapeute_Marie'
}

for intervention, pro in intervention_pro.items():
    add_relation_to_individual(rdf, intervention, 'conduitPar', pro)

# Ajouter les relations concerneDomaine (Intervention → DomaineClinique)
intervention_domaine = {
    'ExerciceCommunicationVerbale': 'Orthophonie',
    'ExerciceCommunicationNonVerbale': 'Orthophonie',
    'ExerciceMotricite': ['Kinesitherapie', 'Psychomotricite'],
    'ExerciceSocial': 'Psychologie',
    'ExerciceCognitif': 'Psychologie',
    'ExerciceEmotionnel': ['Psychologie', 'Pedopsychiatrie']
}

for intervention, domaines in intervention_domaine.items():
    if isinstance(domaines, list):
        for domaine in domaines:
            add_relation_to_individual(rdf, intervention, 'concerneDomaine', domaine)
    else:
        add_relation_to_individual(rdf, intervention, 'concerneDomaine', domaines)

# Ajouter les relations utiliseTechnologie (Intervention → Technologies)
intervention_tech = {
    'ExerciceCommunicationVerbale': ['TraitementLangageNaturel', 'ReconnaissanceVocale'],
    'ExerciceMotricite': ['AnalyseMarche', 'ReconnaissanceGestes'],
    'ExerciceSocial': ['ReconnaissanceFaciale', 'DetectionEmotionsFaciales'],
    'ExerciceCognitif': 'TraitementLangageNaturel',
    'ExerciceEmotionnel': 'DetectionEmotionsFaciales'
}

for intervention, techs in intervention_tech.items():
    if isinstance(techs, list):
        for tech in techs:
            add_relation_to_individual(rdf, intervention, 'utiliseTechnologie', tech)
    else:
        add_relation_to_individual(rdf, intervention, 'utiliseTechnologie', techs)

# Ajouter les relations cibleParIntervention (DomaineClinique → Intervention)
domaine_intervention = {
    'Orthophonie': ['ExerciceCommunicationVerbale', 'ExerciceCommunicationNonVerbale'],
    'Kinesitherapie': 'ExerciceMotricite',
    'Psychomotricite': 'ExerciceMotricite',
    'Psychologie': ['ExerciceSocial', 'ExerciceCognitif', 'ExerciceEmotionnel'],
    'Pedopsychiatrie': 'ExerciceEmotionnel'
}

for domaine, interventions in domaine_intervention.items():
    if isinstance(interventions, list):
        for intervention in interventions:
            add_relation_to_individual(rdf, domaine, 'cibleParIntervention', intervention)
    else:
        add_relation_to_individual(rdf, domaine, 'cibleParIntervention', interventions)

print("Génération du fichier OWL en cours...")

# Sauvegarder le fichier
tree = ET.ElementTree(rdf)
ET.indent(tree, space="  ")
tree.write('ontology_tsa_nlp-3.owl', encoding='utf-8', xml_declaration=True)

# Post-traiter le fichier pour remplacer ns3: par le namespace par défaut (sans préfixe)
# Cela permet aux propriétés d'être reconnues comme "Property assertions" dans Protégé
with open('ontology_tsa_nlp-3.owl', 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacer ns3: par rien (namespace par défaut) pour les éléments de propriétés
# Mais garder xmlns:ns3 dans la déclaration pour éviter les erreurs
content = content.replace('<ns3:', '<')
content = content.replace('</ns3:', '</')
# Supprimer la déclaration xmlns:ns3 qui n'est plus nécessaire
content = content.replace(' xmlns:ns3="http://example.org/ont/tsa-nlp#"', '')

with open('ontology_tsa_nlp-3.owl', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fichier OWL créé: ontology_tsa_nlp-3.owl")

