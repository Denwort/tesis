import pandas as pd
import requests

# Función para realizar la consulta Overpass
def query_overpass(lat, lon, radius):
    overpass_url = "http://overpass-api.de/api/interpreter"
    # Añadiendo múltiples tipos de POI en la consulta
    overpass_query = f"""
    [out:json];
    (
      node["amenity"="restaurant"](around:{radius},{lat},{lon});
      way["amenity"="restaurant"](around:{radius},{lat},{lon});
      node["amenity"="fast_food"](around:{radius},{lat},{lon});
      way["amenity"="fast_food"](around:{radius},{lat},{lon});
      node["amenity"="university"](around:{radius},{lat},{lon});
      way["amenity"="university"](around:{radius},{lat},{lon});
      node["amenity"="school"](around:{radius},{lat},{lon});
      way["amenity"="school"](around:{radius},{lat},{lon});
      node["amenity"="kindergarten"](around:{radius},{lat},{lon});
      way["amenity"="kindergarten"](around:{radius},{lat},{lon});
      node["amenity"="hospital"](around:{radius},{lat},{lon});
      way["amenity"="hospital"](around:{radius},{lat},{lon});
      node["amenity"="pharmacy"](around:{radius},{lat},{lon});
      way["amenity"="pharmacy"](around:{radius},{lat},{lon});
      node["amenity"="clinic"](around:{radius},{lat},{lon});
      way["amenity"="clinic"](around:{radius},{lat},{lon});
      node["amenity"="bus_station"](around:{radius},{lat},{lon});
      way["amenity"="bus_station"](around:{radius},{lat},{lon});
      node["shop"="mall"](around:{radius},{lat},{lon});
      way["shop"="mall"](around:{radius},{lat},{lon});
      node["shop"="supermarket"](around:{radius},{lat},{lon});
      way["shop"="supermarket"](around:{radius},{lat},{lon});
      node["amenity"="bank"](around:{radius},{lat},{lon});
      way["amenity"="bank"](around:{radius},{lat},{lon});
      node["leisure"="fitness_centre"](around:{radius},{lat},{lon});
      way["leisure"="fitness_centre"](around:{radius},{lat},{lon});
      node["leisure"="swimming_pool"](around:{radius},{lat},{lon});
      way["leisure"="swimming_pool"](around:{radius},{lat},{lon});
      node["natural"="beach"](around:{radius},{lat},{lon});
      way["natural"="beach"](around:{radius},{lat},{lon});
    );
    out center;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    return response.json()

# Leer el archivo CSV
df = pd.read_csv('./urbania/urbania_vf.csv') 

# Preparar un DataFrame para almacenar los resultados
results_df = pd.DataFrame()

# Establecer el radio (around) en una variable modificable
radius = 1000  # Puedes cambiar este valor según sea necesario

for index, row in df.iterrows():
    lat, lon = row['latitud'], row['longitud']
    result = query_overpass(lat, lon, radius)
    elements = result.get('elements', [])
    for element in elements:
        # Aquí podrías extraer y manejar más información específica de cada POI
        poi_type = element['tags'].get('amenity', element['tags'].get('shop', ''))
        poi_name = element['tags'].get('name', 'Nombre no disponible')
        # Agregar nueva fila al DataFrame
        new_row = pd.DataFrame({
            'Latitude': [lat],
            'Longitude': [lon],
            'POI Type': [poi_type],
            'POI Name': [poi_name]
        })
        results_df = pd.concat([results_df, new_row], ignore_index=True)

# Guardar los resultados en un nuevo archivo CSV
results_df.to_csv('poi_info.csv', index=False)

print("Información guardada en 'poi_info.csv'.")