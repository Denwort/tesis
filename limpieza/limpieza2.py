import pandas as pd
import numpy as np

# Cargar el archivo CSV
file_path = './limpieza/poi_info_with_existing_data.csv'  # Reemplaza esto con la ruta correcta de tu archivo
csv_data = pd.read_csv(file_path)

# Define a function to calculate the distance between two latitude-longitude points using Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    # Earth radius in kilometers
    R = 6371.0
    # Convert latitude and longitude from degrees to radians
    lat1_rad, lon1_rad = np.radians(lat1), np.radians(lon1)
    lat2_rad, lon2_rad = np.radians(lat2), np.radians(lon2)
    
    # Compute differences between latitudes and longitudes
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Apply the Haversine formula
    a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c  # Distance in kilometers
    
    return distance

# Extract the latitud and longitud for the records
record_lat = csv_data['latitud']
record_lon = csv_data['longitud']

# List of all POIs to process
pois = [
    'Restaurants', 'Fast Food', 'Universities', 'Schools', 'Kindergartens', 
    'Hospitals', 'Pharmacies', 'Clinics', 'Malls', 'Supermarkets', 
    'Banks', 'Fitness Centres', 'Swimming Pools', 'Parks', 'Bus Stops'
]

# Calculate the distance for each POI and create the new column, then drop the lat/lon columns for that POI
for poi in pois:
    # Calculate distance if lat/lon are available (non-zero values)
    csv_data[f'{poi}_dist'] = csv_data.apply(
        lambda row: haversine(row['latitud'], row['longitud'], row[f'{poi}_Lat'], row[f'{poi}_Lon'])
        if (row[f'{poi}_Lat'] != 0 and row[f'{poi}_Lon'] != 0) else np.nan,
        axis=1
    )
    
    # Drop the Lat and Lon columns for the current POI
    csv_data.drop([f'{poi}_Lat', f'{poi}_Lon'], axis=1, inplace=True)

# Guardar el nuevo archivo CSV con las distancias calculadas
csv_data.to_csv('tengosueño.csv', index=False)

# Mostrar las primeras filas del dataframe actualizado
csv_data.head()
