# 🚚 Optimiseur de Tournées Logistiques (Vehicle Routing Problem)

## 📝 Description
Ce projet est une application web interactive d'aide à la décision pour la logistique du dernier kilomètre. Elle permet d'optimiser les tournées de livraison d'une flotte de camions en minimisant la distance totale parcourue, tout en respectant les contraintes de capacité de charge de chaque véhicule.

L'application est construite avec **Streamlit** pour l'interface, **Google OR-Tools** pour la résolution mathématique du problème, et **PyDeck** pour la cartographie interactive.

## 🚀 Fonctionnalités
- **Optimisation multi-véhicules** : Répartition intelligente des clients entre plusieurs camions.
- **Contrainte de capacité** : Prise en compte du poids maximum transportable par camion.
- **Cartographie interactive** : Visualisation des itinéraires de chaque camion avec des couleurs distinctes.
- **Génération de données** : Script inclus pour générer 50 clients aléatoires autour d'un dépôt.

## 🛠️ Stack Technique
- **Python 3.10+**
- **OR-Tools** (Solveur de routage)
- **Streamlit** (Interface Web)
- **PyDeck** (Visualisation cartographique)
- **Pandas / Numpy** (Manipulation de données)
- **GeoPandas / Matplotlib** (EDA - dans le notebook)

## 📂 Structure du Projet
```text
Projet_Logistique/
│
├── data/
│   └── commandes.csv          # Données clients (Lat, Lon, Poids)
│
├── notebooks/
│   └── EDA.ipynb              # Exploration et génération des données
│
├── app.py                     # Application Streamlit
├── requirements.txt           # Dépendances Python
└── README.md                  # Ce fichier