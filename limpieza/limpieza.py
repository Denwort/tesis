import pandas as pd

df = pd.read_csv('./limpieza/nexoinmobiliario.csv')

# Limpiar las columnas

# Crear ID
df['index'] = df['referencia'] + ' (' + df['tipologia'] + ')'
cols = ['index'] + [col for col in df.columns if col != 'index']
df = df[cols]
df = df.drop(columns=['referencia', 'tipologia'])

# Limpieza de valores no importantes
df = df.drop(columns=['financiamiento', 'direccion', 'link'])

# Valores dudosos
df = df.drop(columns=['fecha_entrega', 'areas_comunes', 'piso'])

# **Filtrar por distritos específicos**
distritos_permitidos = [
    'San Miguel', 'Pueblo Libre', 'Magdalena', 'Jesus Maria', 'Lince',
    'San Isidro', 'Miraflores', 'Surquillo', 'San Borja',
    'Santiago de Surco', 'Barranco'
]
df = df[df['distrito'].isin(distritos_permitidos)]

# Convertir moneda
df['area'] = df['area'].str.replace(' m2', '')
df['moneda'] = df['precio'].apply(lambda x: 'PEN' if 'S/' in x else 'USD' if '$' in x else 'Unknown')
df['precio'] = df['precio'].str.replace('S/ ', '').str.replace('$ ', '').str.replace(',', '').str.strip()

# Convertir a número
df['latitud'] = df['latitud'].astype(float)
df['longitud'] = df['longitud'].astype(float)
df['dormitorios'] = df['dormitorios'].astype(int)
df['area'] = df['area'].astype(float)
df['precio'] = df['precio'].astype(float)

TASA_DE_CAMBIO = 3.75

df.loc[df['moneda'] == 'USD', 'precio'] *= TASA_DE_CAMBIO

df = df.drop(columns=['moneda'])

print(df.head())
df.to_csv('./limpieza/datos_limpios.csv', index=False)
