import pandas as pd
import requests

# Función para realizar la consulta Overpass
def query_overpass(lat, lon, radius):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      node(around:{radius},{lat},{lon})["amenity"];
      way(around:{radius},{lat},{lon})["amenity"];
      node(around:{radius},{lat},{lon})["shop"];
      way(around:{radius},{lat},{lon})["shop"];
      node(around:{radius},{lat},{lon})["leisure"];
      way(around:{radius},{lat},{lon})["leisure"];
      node(around:{radius},{lat},{lon})["highway"="bus_stop"];
      way(around:{radius},{lat},{lon})["highway"="bus_stop"];
    );
    out center;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    return response.json()

# Mapeo de tipos de POI
poi_types = {
    "restaurant": "Restaurants",
    "fast_food": "Fast Food",
    "university": "Universities",
    "school": "Schools",
    "kindergarten": "Kindergartens",
    "hospital": "Hospitals",
    "pharmacy": "Pharmacies",
    "clinic": "Clinics",
    "mall": "Malls",
    "supermarket": "Supermarkets",
    "bank": "Banks",
    "fitness_centre": "Fitness Centres",
    "swimming_pool": "Swimming Pools",
    "park": "Parks",
    "bus_stop": "Bus Stops"
}

# Leer el archivo CSV
df = pd.read_csv('./nexoinmobiliario.csv')

# Preparar un DataFrame para almacenar los resultados
columns = ['Latitude', 'Longitude']
for poi in poi_types.values():
    columns.extend([f'{poi}_Count', f'{poi}_Lat', f'{poi}_Lon'])

results_df = pd.DataFrame(columns=columns)

# Establecer el radio (around) en una variable modificable
radius = 1000  # Puedes cambiar este valor según sea necesario

for index, row in df.iterrows():
    lat, lon = row['latitud'], row['longitud']
    result = query_overpass(lat, lon, radius)
    

    elements = result.get('elements', [])
    
    # Inicializar conteo y datos del POI más cercano
    poi_data = {poi: {'count': 0, 'lat': 0, 'lon': 0} for poi in poi_types.values()}
    
    for element in elements:
        if 'lat' in element and 'lon' in element:
            el_lat, el_lon = element['lat'], element['lon']
            
            if 'highway' in element['tags'] and element['tags']['highway'] == 'bus_stop':
                poi_type = "Bus Stops"
            else:
                poi = element['tags'].get('amenity', element['tags'].get('shop', element['tags'].get('leisure', '')))
                poi_type = poi_types.get(poi, None)
            
            if poi_type:
                poi_data[poi_type]['count'] += 1
                # Solo actualizar latitud y longitud si aún no se ha encontrado uno
                if poi_data[poi_type]['lat'] == 0 and poi_data[poi_type]['lon'] == 0:
                    poi_data[poi_type]['lat'] = el_lat
                    poi_data[poi_type]['lon'] = el_lon
    
    # Crear fila con datos
    row_data = {
        'Latitude': lat,
        'Longitude': lon
    }
    for poi, data in poi_data.items():
        row_data[f'{poi}_Count'] = data['count']
        row_data[f'{poi}_Lat'] = data['lat']
        row_data[f'{poi}_Lon'] = data['lon']
    
    new_row = pd.DataFrame([row_data])
    results_df = pd.concat([results_df, new_row], ignore_index=True)

# Guardar los resultados en un nuevo archivo CSV
results_df.to_csv('poi_info_with_counts_and_coordinates.csv', index=False)

print("Información guardada en 'poi_info_with_counts_and_coordinates.csv'.")
