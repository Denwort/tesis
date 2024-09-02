import pandas as pd

df = pd.read_csv('./limpieza/nexoinmobiliario.csv')

# Limpiar las columnas

# Crear ID
df['index'] = df['referencia'] + '(' + df['tipologia'] + ')'
cols = ['index'] + [col for col in df.columns if col != 'index']
df = df[cols]
df = df.drop(columns=['referencia'])
df = df.drop(columns=['tipologia'])

# Limpieza de valores no importantes
df = df.drop(columns=['areas_comunes']) # podria importar
df = df.drop(columns=['financiamiento'])
df = df.drop(columns=['piso']) # podria importar
df = df.drop(columns=['fecha_entrega']) # podria importar
df = df.drop(columns=['direccion']) # podria importar
df = df.drop(columns=['link'])

# Convertir moneda
df['area'] = df['area'].str.replace(' m2', '')
df['moneda'] = df['precio'].apply(lambda x: 'PEN' if 'S/' in x else 'USD' if '$' in x else 'Unknown')
df['precio'] = df['precio'].str.replace('S/ ', '').str.replace('$ ', '').str.replace(',', '').str.strip()

# Convertir a numero
df['latitud'] = df['latitud'].astype(float)
df['longitud'] = df['longitud'].astype(float)
#df['piso'] = df['piso'].str.replace('piso: ', '').astype(int)
df['dormitorios'] = df['dormitorios'].astype(int)
df['area'] = df['area'].astype(float)
df['precio'] = df['precio'].astype(float)

df.loc[df['moneda'] == 'USD', 'precio'] *= 3.75
df.loc[df['moneda'] == 'USD', 'moneda'] = 'PEN'

print(df.head())
df.to_csv('./limpieza/datos_limpios.csv', index=False)
