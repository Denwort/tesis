import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder
import numpy as np
import xgboost as xgb
import joblib

# Cargar
df = pd.read_csv('./limpieza/datos_limpios.csv')
df = df.drop(columns=['index'])

label_encoders = {}
for column in ['distrito', 'etapa', 'tipo']:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

X = df.drop(columns=['precio'])
y = df['precio'] 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 1. Modelo Random Forest Regressor
model_rf = RandomForestRegressor(n_estimators=100, random_state=42)
model_rf.fit(X_train, y_train)
y_pred_rf = model_rf.predict(X_test)

# 2. Modelo XGBoost Regressor
model_xgb = xgb.XGBRegressor(n_estimators=100, random_state=42)
model_xgb.fit(X_train, y_train)
y_pred_xgb = model_xgb.predict(X_test)

# 3. Modelo Linear Regression
model_lr = LinearRegression()
model_lr.fit(X_train, y_train)
y_pred_lr = model_lr.predict(X_test)

# Calcular métricas de evaluación
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

# Evaluar cada modelo
calcular_metrica(y_test, y_pred_rf, "Random Forest Regressor")
calcular_metrica(y_test, y_pred_xgb, "XGBoost Regressor")
calcular_metrica(y_test, y_pred_lr, "Linear Regression")

# Guardar los modelos entrenados
joblib.dump(model_rf, './modelo/random_forest.pkl')
joblib.dump(model_xgb, './modelo/xgboost.pkl')
joblib.dump(model_lr, './modelo/linear_regression.pkl')



# XAI
import shap

# Random Forest
explainer_rf = shap.TreeExplainer(model_rf)
shap_values_rf = explainer_rf(X_test)
print("SHAP Summary Plot para Random Forest:")
shap.summary_plot(shap_values_rf, X_test)


# XGBoost
explainer_xgb = shap.TreeExplainer(model_xgb)
shap_values_xgb = explainer_xgb(X_test)
print("SHAP Summary Plot para XGBoost:")
shap.summary_plot(shap_values_xgb, X_test)

# Linear Regression
explainer_lr = shap.Explainer(model_lr, X_train)
shap_values_lr = explainer_lr(X_test)
print("SHAP Summary Plot para Linear Regression:")
shap.summary_plot(shap_values_lr, X_test)

'''

# LIME
from lime.lime_tabular import LimeTabularExplainer

explainer_lime = LimeTabularExplainer(X_train.values, 
                                      training_labels=y_train.values,
                                      feature_names=X_train.columns, 
                                      verbose=True, 
                                      mode='regression')

# Explicación para una instancia específica (ejemplo: la primera instancia de X_test)
i = 0 

# Random Forest
print("Explicación LIME para Random Forest:")
def predict_rf(X):
    return model_rf.predict(pd.DataFrame(X, columns=X_train.columns))
exp_rf = explainer_lime.explain_instance(X_test.values[i], predict_rf, num_features=10)
exp_rf.save_to_file('./lime_explicacion_rf.html')

# XGBoost
print("Explicación LIME para XGBoost:")
def predict_xgb(X):
    return model_xgb.predict(pd.DataFrame(X, columns=X_train.columns))
exp_xgb = explainer_lime.explain_instance(X_test.values[i], predict_xgb, num_features=10)
exp_xgb.save_to_file('./lime_explicacion_xgb.html')

# Linear Regression
print("Explicación LIME para Linear Regression:")
def predict_lr(X):
    return model_lr.predict(pd.DataFrame(X, columns=X_train.columns))
exp_lr = explainer_lime.explain_instance(X_test.values[i], predict_lr, num_features=10)
exp_lr.save_to_file('./lime_explicacion_lr.html')

'''