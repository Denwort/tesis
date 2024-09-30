import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder
import numpy as np
import xgboost as xgb
import joblib

# Cargar el CSV
df = pd.read_csv('./limpieza/poi_info_with_existing_data.csv')

# Eliminar columna 'index' si no es relevante para el análisis
df = df.drop(columns=['index'])

# Codificar variables categóricas
label_encoders = {}
for column in ['distrito', 'etapa', 'tipo']:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

# Definir variables independientes y dependientes
X = df.drop(columns=['precio'])
y = df['precio']

# Dividir en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 1. Modelo Random Forest Regressor con GridSearchCV
param_grid_rf = {
    'n_estimators': [100, 200, 300],
    'criterion': ['squared_error', 'absolute_error'],
    'max_features': ['auto', 'sqrt', 'log2'],
    'max_depth': [None, 10, 20, 30]
}

grid_rf = GridSearchCV(estimator=RandomForestRegressor(random_state=42), param_grid=param_grid_rf, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
grid_rf.fit(X_train, y_train)

# Imprimir los mejores hiperparámetros encontrados para Random Forest
print(f"Best params for Random Forest: {grid_rf.best_params_}")

# Predecir usando el mejor modelo encontrado
y_pred_rf = grid_rf.best_estimator_.predict(X_test)

# 2. Modelo XGBoost Regressor con GridSearchCV
param_grid_xgb = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.1, 0.3],
    'max_depth': [3, 6, 10]
}

grid_xgb = GridSearchCV(estimator=xgb.XGBRegressor(random_state=42), param_grid=param_grid_xgb, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
grid_xgb.fit(X_train, y_train)

# Imprimir los mejores hiperparámetros encontrados para XGBoost
print(f"Best params for XGBoost: {grid_xgb.best_params_}")

# Predecir usando el mejor modelo encontrado
y_pred_xgb = grid_xgb.best_estimator_.predict(X_test)

# 3. Modelo Linear Regression (sin ajuste de hiperparámetros)
model_lr = LinearRegression()
model_lr.fit(X_train, y_train)
y_pred_lr = model_lr.predict(X_test)

# Función para calcular las métricas
def calcular_metrica(y_test, y_pred, model_name):
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    
    print(f'{model_name}')
    print(f'R² (R Squared): {r2}')
    print(f'RMSE (Root Mean Squared Error): {rmse}')
    print(f'MAE (Mean Absolute Error): {mae}')
    print(f'MAPE (Mean Absolute Percentage Error): {mape}%\n')

# Evaluar los modelos
calcular_metrica(y_test, y_pred_rf, "Random Forest Regressor (con GridSearchCV)")
calcular_metrica(y_test, y_pred_xgb, "XGBoost Regressor (con GridSearchCV)")
calcular_metrica(y_test, y_pred_lr, "Linear Regression")

# Guardar los mejores modelos
joblib.dump(grid_rf.best_estimator_, './modelo/random_forest_optimizado.pkl')
joblib.dump(grid_xgb.best_estimator_, './modelo/xgboost_optimizado.pkl')
joblib.dump(model_lr, './modelo/linear_regression.pkl')
