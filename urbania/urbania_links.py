import pandas as pd

# Cargar el archivo CSV
archivo_csv = './urbania/urbania.csv'  
df = pd.read_csv(archivo_csv)

# Agregar 'https://urbania.pe/' al inicio de cada valor en la columna 'Link'
df['Link'] = 'https://urbania.pe' + df['Link'].astype(str)

# Eliminar tildes de los caracteres en la columna 'Dirección'
df['Dirección'] = df['Dirección'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

# Filtrar filas que contengan alguna de las localidades específicas en la columna 'Dirección'
df = df[
    (df['Dirección'].str.contains("San Miguel", regex=False, na=False)) |
    (df['Dirección'].str.contains("Pueblo Libre", regex=False, na=False)) |
    (df['Dirección'].str.contains("Magdalena", regex=False, na=False)) |
    (df['Dirección'].str.contains("Jesus Maria", regex=False, na=False)) |
    (df['Dirección'].str.contains("Lince", regex=False, na=False)) |
    (df['Dirección'].str.contains("San Isidro", regex=False, na=False)) |
    (df['Dirección'].str.contains("Miraflores", regex=False, na=False)) |
    (df['Dirección'].str.contains("Surquillo", regex=False, na=False)) |
    (df['Dirección'].str.contains("San Borja", regex=False, na=False)) |
    (df['Dirección'].str.contains("Santiago de Surco", regex=False, na=False)) |
    (df['Dirección'].str.contains("Barranco", regex=False, na=False))
]

# Eliminar filas duplicadas
df = df.drop_duplicates()

# Guardar el resultado en un nuevo archivo CSV
df.to_csv('./urbania/urbania_links.csv', index=False)
