import requests

def obtener_detalles_lugar(api_key, latitud, longitud):
    # URL de la API de Google Places para buscar lugares cercanos
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    # Parámetros de la solicitud
    params = {
        "location": f"{latitud},{longitud}",
        "radius": 5000,  # Aumenta el radio de búsqueda a 5000 metros
        "key": api_key
    }
    
    # Realizar la solicitud a la API
    respuesta = requests.get(url, params=params)
    
    # Verificar si la solicitud fue exitosa
    if respuesta.status_code == 200:
        datos = respuesta.json()
        
        # Imprimir la respuesta completa para depuración
        print(datos)
        
        # Comprobar si se encontraron lugares
        if datos['results']:
            lugar_id = datos['results'][0]['place_id']
            
            # Obtener detalles del lugar utilizando el place_id
            detalles_url = "https://maps.googleapis.com/maps/api/place/details/json"
            detalles_params = {
                "place_id": lugar_id,
                "key": api_key
            }
            
            detalles_respuesta = requests.get(detalles_url, params=detalles_params)
            
            if detalles_respuesta.status_code == 200:
                detalles_datos = detalles_respuesta.json()
                if detalles_datos.get("result"):
                    return detalles_datos["result"]
                else:
                    return "No se encontraron detalles para el lugar especificado."
            else:
                return f"Error al obtener detalles del lugar. Código de estado: {detalles_respuesta.status_code}"
        else:
            return "No se encontraron lugares en la ubicación proporcionada."
    else:
        return f"Error en la solicitud a la API de Google Places. Código de estado: {respuesta.status_code}"

# Ejemplo de uso
api_key = "TU_CLAVE_API_AQUI"  # Reemplaza con tu clave API
latitud = -12.1220869  # Ejemplo: Latitud
longitud = -76.9926445  # Ejemplo: Longitud

detalles = obtener_detalles_lugar(api_key, latitud, longitud)
print(detalles)
