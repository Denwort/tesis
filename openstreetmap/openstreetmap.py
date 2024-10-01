import pandas as pd
import requests
import time

# Función para realizar la consulta Overpass con manejo de errores
def query_overpass(lat, lon, radius, count_only=True):
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    # Diferenciar entre consulta para conteo (dentro del radio) y para el más cercano (sin radio)
    if count_only:
        # Consulta dentro del radio especificado
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
    else:
        # Consulta sin restricción de radio para encontrar el más cercano
        overpass_query = f"""
        [out:json];
        (
          node(around:100000,{lat},{lon})["amenity"];
          way(around:100000,{lat},{lon})["amenity"];
          node(around:100000,{lat},{lon})["shop"];
          way(around:100000,{lat},{lon})["shop"];
          node(around:100000,{lat},{lon})["leisure"];
          way(around:100000,{lat},{lon})["leisure"];
          node(around:100000,{lat},{lon})["highway"="bus_stop"];
          way(around:100000,{lat},{lon})["highway"="bus_stop"];
        );
        out center;
        """
    
    try:
        response = requests.get(overpass_url, params={'data': overpass_query}, timeout=60)
        response.raise_for_status()  # Verifica si hubo un error HTTP
        return response.json()  # Intentar parsear la respuesta como JSON
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud HTTP: {e}")
        return None  # Devuelve None en caso de error
    except ValueError:
        print("Error al decodificar el JSON")
        return None

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

# Leer el archivo CSV proporcionado por el usuario
df = pd.read_csv('./openstreetmap/datos_limpios.csv')  # Cambia la ruta por la ubicación de tu archivo CSV

# Preparar un DataFrame para almacenar los resultados
columns = df.columns.tolist()  # Mantener las columnas originales
for poi in poi_types.values():
    columns.extend([f'{poi}_Count', f'{poi}_Lat', f'{poi}_Lon'])  # Agregar nuevas columnas para los POI

results_df = pd.DataFrame(columns=columns)

# Establecer el radio (around) en una variable modificable
radius = 1000  # Puedes cambiar este valor según sea necesario

# Iterar sobre el archivo CSV para cada latitud y longitud
for index, row in df.iterrows():
    lat, lon = row['latitud'], row['longitud']

    # Realizar la primera consulta a Overpass para contar POIs dentro del radio
    result_count = query_overpass(lat, lon, radius, count_only=True)
    
    if result_count is None:  # Si no hay resultados, continuar con la siguiente iteración
        print(f"No se obtuvieron resultados para la ubicación: {lat}, {lon}")
        continue

    elements_count = result_count.get('elements', [])

    # Inicializar conteo y datos del POI más cercano
    poi_data = {poi: {'count': 0, 'lat': 0, 'lon': 0} for poi in poi_types.values()}

    # Procesar la primera consulta (para contar POIs dentro del radio)
    for element in elements_count:
        if 'lat' in element and 'lon' in element:
            el_lat, el_lon = element['lat'], element['lon']
            
            if 'highway' in element['tags'] and element['tags']['highway'] == 'bus_stop':
                poi_type = "Bus Stops"
            else:
                poi = element['tags'].get('amenity', element['tags'].get('shop', element['tags'].get('leisure', '')))
                poi_type = poi_types.get(poi, None)
            
            if poi_type:
                poi_data[poi_type]['count'] += 1

    # Realizar la segunda consulta para obtener el POI más cercano (sin radio)
    result_nearest = query_overpass(lat, lon, radius, count_only=False)
    
    if result_nearest is None:
        print(f"No se pudo encontrar el POI más cercano para la ubicación: {lat}, {lon}")
        continue

    elements_nearest = result_nearest.get('elements', [])
    
    # Procesar la segunda consulta (para encontrar el POI más cercano)
    for element in elements_nearest:
        if 'lat' in element and 'lon' in element:
            el_lat, el_lon = element['lat'], element['lon']
            
            if 'highway' in element['tags'] and element['tags']['highway'] == 'bus_stop':
                poi_type = "Bus Stops"
            else:
                poi = element['tags'].get('amenity', element['tags'].get('shop', element['tags'].get('leisure', '')))
                poi_type = poi_types.get(poi, None)
            
            if poi_type:
                # Si encontramos un POI más cercano, actualizamos latitud y longitud
                if poi_data[poi_type]['lat'] == 0 and poi_data[poi_type]['lon'] == 0:
                    poi_data[poi_type]['lat'] = el_lat
                    poi_data[poi_type]['lon'] = el_lon

    # Crear fila con los datos originales y los nuevos POI
    row_data = row.to_dict()  # Convertir los datos originales en un diccionario
    for poi, data in poi_data.items():
        row_data[f'{poi}_Count'] = data['count']
        row_data[f'{poi}_Lat'] = data['lat']
        row_data[f'{poi}_Lon'] = data['lon']

    # Añadir la nueva fila al DataFrame final
    new_row = pd.DataFrame([row_data])
    results_df = pd.concat([results_df, new_row], ignore_index=True)

# Guardar los resultados en un nuevo archivo CSV
results_df.to_csv('ahoraSiqueSi.csv', index=False)

print("Información guardada en 'poi_info_with_existing_data.csv'.")
