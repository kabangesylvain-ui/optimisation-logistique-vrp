
---

### 📑 2. Fichier `Rapport.md`

Créez un fichier nommé `Rapport.md` et collez ceci. C'est la structure idéale pour un mémoire ou une présentation orale.

```markdown
# Rapport de Projet : Analyse de la Logistique et Optimisation de Tournées

## 1. Introduction et Contexte
La logistique du dernier kilomètre représente une part majeure des coûts opérationnels des entreprises de livraison. Une mauvaise planification des tournées entraîne une surconsommation de carburant, des retards de livraison et une augmentation de l'empreinte carbone. 

L'objectif de ce projet est de développer un outil d'aide à la décision capable de résoudre le **Vehicle Routing Problem (VRP)** : trouver les itinéraires optimaux pour une flotte de véhicules devant desservir un ensemble de clients géographiquement dispersés.

## 2. Méthodologie et Architecture

Le projet est divisé en trois grandes phases :

### Phase 1 : Analyse Exploratoire et Préparation des Données (EDA)
- **Génération/Nettoyage** : Création d'un jeu de données de 50 clients avec des coordonnées GPS (Latitude/Longitude) et des poids de colis aléatoires.
- **Visualisation** : Utilisation de `Matplotlib` et `GeoPandas` pour cartographier les points de livraison et le dépôt central.

### Phase 2 : Modélisation Mathématique et Optimisation
- **Matrice de distances** : Calcul des distances entre tous les points en utilisant la formule de **Haversine** (distance à vol d'oiseau).
- **Solveur OR-Tools** : Implémentation du solveur de Google. Nous avons défini :
  - Un coût d'arc basé sur la distance.
  - Une dimension de capacité (`AddDimensionWithVehicleCapacity`) pour s'assurer qu'aucun camion ne dépasse son poids maximal.
  - Une pénalité stricte (`SetSpanCostCoefficientForAllVehicles`) pour forcer le respect de la capacité.

### Phase 3 : Développement de l'Application Web
- **Streamlit** : Création d'une interface interactive.
- **PyDeck** : Intégration d'une carte 3D interactive avec un fond de carte clair (Carto Positron). Les itinéraires sont tracés avec des couleurs différentes par camion.

## 3. Résultats et Démonstration
*(À compléter avec vos captures d'écran)*
- L'application répartit intelligemment les 50 clients entre les camions disponibles.
- Les clients sont regroupés par zones géographiques (ex: un camion pour le Nord, un pour le Sud), minimisant ainsi les croisements de routes.
- L'interface affiche le poids total transporté par chaque camion pour vérifier le respect des contraintes.

## 4. Limites du Modèle Actuel
1. **Distances à vol d'oiseau** : La formule de Haversine ne prend pas en compte le réseau routier réel.
2. **Absence de fenêtres de temps** : Le modèle ne gère pas les horaires de disponibilité des clients (ex: livraison uniquement le matin).
3. **Flotte homogène** : Tous les camions ont la même capacité.

## 5. Perspectives d'Amélioration
- **Intégration d'une API de routage** (ex: OSRM ou Google Maps API) pour obtenir les distances routières réelles.
- **Ajout de contraintes horaires** (Time Windows) via OR-Tools pour respecter les créneaux de livraison.
- **Hétérogénéité de la flotte** : Prendre en compte des camions de tailles différentes.

## 6. Conclusion
Ce projet démontre la puissance des outils de recherche opérationnelle (OR-Tools) couplés au développement web (Streamlit) pour résoudre des problématiques industrielles complexes. L'application développée permet non seulement de calculer des tournées optimales, mais aussi de visualiser et de valider ces résultats de manière intuitive.