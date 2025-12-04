# Documentation des Requêtes SPARQL - Interface d'Interrogation de l'Ontologie

Ce document présente toutes les requêtes SPARQL disponibles dans l'interface d'interrogation de l'ontologie TSA-NLP.

---

## Question 1 : Quels outils numériques utilisent la technologie [TECHNOLOGIE] ?

**Question à laquelle elle répond :** Trouve tous les outils numériques qui implémentent une technologie spécifique (NLP, Vision ou Mouvement).

**Code SPARQL :**
```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX : <http://example.org/ont/tsa-nlp#>

SELECT DISTINCT ?outil
WHERE {
    ?outil rdf:type/rdfs:subClassOf* :OutilNumerique .
    ?outil :implementeTechnologie :{technologie} .
}
```

**Explication :** La requête sélectionne tous les outils numériques (y compris leurs sous-classes) qui ont une relation `implementeTechnologie` avec la technologie spécifiée. Elle utilise `rdfs:subClassOf*` pour inclure toutes les sous-classes de OutilNumerique (Applications, RobotSocial, etc.).

---

## Question 2 : Quels outils numériques sont utilisés par [PERSONNE_TSA] ?

**Question à laquelle elle répond :** Trouve tous les outils numériques qui sont utilisés par une personne avec TSA spécifique.

**Code SPARQL :**
```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX : <http://example.org/ont/tsa-nlp#>

SELECT DISTINCT ?outil
WHERE {
    :{personne} rdf:type :PersonneTSA .
    :{personne} :estAidePar ?outil .
    ?outil rdf:type/rdfs:subClassOf* :OutilNumerique .
}
```

**Explication :** La requête vérifie d'abord que l'individu est bien une personne TSA, puis trouve tous les outils liés via la relation `estAidePar`. Elle filtre ensuite pour ne garder que les outils numériques en vérifiant leur type.

---

## Question 3 : Quels outils numériques soutiennent l'intervention [INTERVENTION] ?

**Question à laquelle elle répond :** Trouve tous les outils numériques qui soutiennent ou sont utilisés dans une intervention spécifique.

**Code SPARQL :**
```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX : <http://example.org/ont/tsa-nlp#>

SELECT DISTINCT ?outil
WHERE {
    ?outil rdf:type/rdfs:subClassOf* :OutilNumerique .
    {
        ?outil :soutientIntervention :{intervention} .
    }
    UNION
    {
        ?outil :utiliseDansIntervention :{intervention} .
    }
}
```

**Explication :** La requête utilise un `UNION` pour trouver les outils qui ont soit une relation `soutientIntervention` soit `utiliseDansIntervention` avec l'intervention spécifiée. Cela permet de capturer toutes les relations possibles entre outils et interventions.

---

## Question 4 : Quels besoins satisfait [OUTIL_NUMERIQUE]. Ce besoin est-il un besoin parent ou enfant TSA ?

**Question à laquelle elle répond :** Trouve tous les besoins satisfaits par un outil numérique et détermine si ces besoins sont des besoins parents ou des besoins d'enfant TSA.

**Code SPARQL :**
```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX : <http://example.org/ont/tsa-nlp#>

SELECT DISTINCT ?besoin ?typeBesoin
WHERE {
    :{outil} rdf:type/rdfs:subClassOf* :OutilNumerique .
    {
        :{outil} :repondABesoin ?besoin .
    }
    UNION
    {
        ?besoin :estSatisfaitPar :{outil} .
    }
    ?besoin rdf:type ?typeBesoin .
    {
        ?typeBesoin rdfs:subClassOf* :BesoinsParents .
    }
    UNION
    {
        ?typeBesoin rdfs:subClassOf* :BesoinsEnfantTSA .
    }
}
```

**Explication :** La requête utilise deux blocs `UNION` : le premier trouve les besoins via les relations `repondABesoin` ou `estSatisfaitPar`, le second filtre pour ne garder que les besoins de type BesoinsParents ou BesoinsEnfantTSA. Elle retourne le besoin et son type pour identifier la catégorie.

---

## Question 6 : Lister l'ensemble des exemples de chaque [TYPE DE OUTIL_NUMERIQUE]

**Question à laquelle elle répond :** Liste tous les individus (exemples) d'une sous-classe spécifique de OutilNumérique (Applications, RobotSocial, SystemeVR_AR, etc.).

**Code SPARQL :**
```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX : <http://example.org/ont/tsa-nlp#>

SELECT DISTINCT ?individu
WHERE {
    ?individu rdf:type <http://example.org/ont/tsa-nlp#{sousclasse}> .
}
ORDER BY ?individu
```

**Explication :** La requête recherche directement tous les individus qui ont le type de la sous-classe spécifiée (par exemple Applications, RobotSocial). Elle utilise une URI complète pour éviter les problèmes de résolution de préfixes et trie les résultats par ordre alphabétique.

---

## Notes techniques

- Toutes les requêtes utilisent `rdfs:subClassOf*` pour inclure les sous-classes dans la hiérarchie
- Le préfixe `:` représente le namespace `http://example.org/ont/tsa-nlp#`
- Les requêtes utilisent `SELECT DISTINCT` pour éviter les doublons dans les résultats
- La question 6 utilise une URI complète au lieu d'un préfixe pour garantir la résolution correcte du type
