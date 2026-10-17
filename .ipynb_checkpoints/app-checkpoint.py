import streamlit as st
import pandas as pd
import pydeck as pdk
import math
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# --- Fonctions de calcul ---
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def solve_vrp(distance_matrix, demandes, capacite, num_vehicles):
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), num_vehicles, 0)
    routing = pywrapcp.RoutingModel(manager)

    # Callback distance
    def distance_callback(from_index, to_index):
        return distance_matrix[manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Callback capacité
    def demand_callback(from_index):
        return demandes[manager.IndexToNode(from_index)]
    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index, 0, [capacite] * num_vehicles, True, 'Capacity'
    )
    
    # Pénalité stricte
    capacity_dimension = routing.GetDimensionOrDie('Capacity')
    capacity_dimension.SetSpanCostCoefficientForAllVehicles(1000)

    # Paramètres de recherche (On augmente le temps pour les gros datasets)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    search_parameters.time_limit.seconds = 10 # 10 secondes de calcul max
    
    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        routes = []
        for vehicle_id in range(num_vehicles):
            index = routing.Start(vehicle_id)
            route = []
            while not routing.IsEnd(index):
                route.append(manager.IndexToNode(index))
                index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))
            routes.append(route)
        return routes
    return None

# --- Interface Streamlit ---
st.set_page_config(layout="wide", page_title="Optimisation Logistique")
st.title("🚚 Optimiseur de Tournées Logistiques")
st.write("Application d'optimisation pour 50 clients (générés aléatoirement).")

# Chargement des données
try:
    df = pd.read_csv('commandes.csv')
    data_loaded = True
except FileNotFoundError:
    st.error("⚠️ Fichier 'commandes.csv' introuvable. Veuillez exécuter le script de génération dans le notebook.")
    data_loaded = False

if data_loaded:
    st.sidebar.header("Paramètres")
    nb_camions = st.sidebar.number_input("Nombre de camions", min_value=1, max_value=20, value=5)
    # La capacité doit être suffisante pour diviser le poids total
    capacite = st.sidebar.number_input("Capacité max par camion (kg)", min_value=20, max_value=500, value=100)

    if st.sidebar.button("Lancer l'optimisation"):
        # Extraction des données
        locations = list(zip(df['Latitude'], df['Longitude']))
        villes = df['ID'].tolist()
        poids = df['Poids_Kg'].tolist()

        poids_total = sum(poids)
        capacite_totale = capacite * nb_camions

        if poids_total > capacite_totale:
            st.error(f"⚠️ Impossible : Le poids total ({poids_total} kg) dépasse la capacité totale de votre flotte ({capacite_totale} kg). Ajoutez des camions ou augmentez la capacité.")
        else:
            # 1. Matrice de distances
            with st.spinner("Calcul des distances..."):
                n = len(locations)
                # Optimisation : calcul vectorisé pour être plus rapide
                dist_matrix = [[int(haversine(locations[i][0], locations[i][1], locations[j][0], locations[j][1]) * 1000) for j in range(n)] for i in range(n)]

            # 2. Optimisation
            with st.spinner(f"Optimisation pour {nb_camions} camions..."):
                routes = solve_vrp(dist_matrix, poids, capacite, nb_camions)

            if routes:
                path_data = []
                point_data = []
                couleurs = [[255, 0, 0], [0, 0, 255], [0, 255, 0], [255, 165, 0], [128, 0, 128], 
                            [0, 255, 255], [255, 192, 203], [165, 42, 42], [128, 128, 0], [75, 0, 130]]
                
                for i, route in enumerate(routes):
                    if len(route) <= 2: continue # Ignorer camions vides
                    
                    path = [[locations[node][1], locations[node][0]] for node in route]
                    path_data.append({
                        "name": f"Camion {i+1}",
                        "path": path,
                        "color": couleurs[i % len(couleurs)]
                    })
                    
                    for node in route:
                        if node != 0: # On ne met pas de point sur le dépôt
                            point_data.append({
                                "nom": villes[node],
                                "lon": locations[node][1],
                                "lat": locations[node][0],
                                "couleur": couleurs[i % len(couleurs)] + [200]
                            })

                # Ajout du dépôt
                point_data.append({"nom": "Dépôt (Paris)", "lon": locations[0][1], "lat": locations[0][0], "couleur": [0, 0, 0, 255]})

                # 3. Affichage Carte
                st.subheader("🗺️ Carte des Itinéraires")
                st.pydeck_chart(pdk.Deck(
                    map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
                    initial_view_state=pdk.ViewState(latitude=48.8566, longitude=2.3522, zoom=5, pitch=30),
                    layers=[
                        pdk.Layer("PathLayer", data=path_data, get_path="path", get_color="color", width_scale=30, width_min_pixels=3, pickable=True),
                        # Points plus petits pour ne pas surcharger la carte avec 50 clients
                        pdk.Layer("ScatterplotLayer", data=point_data, get_position=["lon", "lat"], get_color="couleur", get_radius=5000, pickable=True)
                    ],
                    tooltip={"text": "{nom}"}
                ))

                # 4. Affichage Détails
                st.subheader("📋 Détails des Tournées")
                cols = st.columns(min(nb_camions, 4)) # On limite à 4 colonnes max pour la lisibilité
                for i, route in enumerate(routes):
                    if len(route) <= 2: continue
                    
                    with cols[i % 4]:
                        poids_total_camion = sum([poids[node] for node in route])
                        st.markdown(f"**Camion {i+1}** ({poids_total_camion} kg)")
                        # On affiche un résumé pour ne pas faire une liste de 50 lignes
                        st.write(f"*{len(route)-2} clients livrés*") 
                        with st.expander("Voir l'itinéraire"):
                            for node in route:
                                st.write(f"- {villes[node]}")