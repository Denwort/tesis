import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('./limpieza/poi_info_with_existing_data.csv')

sns.set(style='whitegrid')

# Crear un gráfico de densidad
plt.figure(figsize=(10, 6))
sns.histplot(df['precio'], kde=True, bins=10, color='blue', alpha=0.6)

# Agregar etiquetas y título
plt.title('Distribución de Precios de Departamentos')
plt.xlabel('Precio')
plt.ylabel('Frecuencia')

plt.show()


print(df.head())
