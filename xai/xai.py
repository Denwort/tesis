import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder
import numpy as np
import xgboost as xgb
import joblib
import pickle

# Cargar
df = pd.read_csv('./tengosueño.csv')
df = df.fillna(1) # Borrar cuando Piero arregle el csv
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
model_rf = RandomForestRegressor(n_estimators=300, criterion="squared_error", max_features="sqrt", max_depth=30, random_state=42)
model_rf.fit(X_train, y_train)
y_pred_rf = model_rf.predict(X_test)

# 2. Modelo XGBoost Regressor
model_xgb = xgb.XGBRegressor(n_estimators=300, learning_rate= 0.3, max_depth=3, random_state=42)
model_xgb.fit(X_train, y_train)
y_pred_xgb = model_xgb.predict(X_test)

# 3. Modelo Linear Regression
model_lr = LinearRegression()
model_lr.fit(X_train, y_train)
y_pred_lr = model_lr.predict(X_test)





'''
# XAI global
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



'''
# PFI
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt
# Random Forest
pfi = permutation_importance(model_rf, X_test, y_test, n_repeats=10, random_state=42)
importances = pfi.importances_mean
importances_std = pfi.importances_std
indices = np.argsort(importances)[::-1]
plt.figure(figsize=(8, 6))
plt.title("Permuted Feature Importance (PFI)")
plt.bar(range(X.shape[1]), importances[indices], yerr=importances_std[indices], align="center")
plt.xticks(range(X.shape[1]), np.array(X_train.columns)[indices], rotation=90)
plt.xlabel("Características")
plt.ylabel("Importancia")
plt.tight_layout()
plt.show()
# XGBoost
importances = pfi.importances_mean
importances_std = pfi.importances_std
indices = np.argsort(importances)[::-1]
plt.figure(figsize=(8, 6))
plt.title("Permuted Feature Importance (PFI)")
plt.bar(range(X.shape[1]), importances[indices], yerr=importances_std[indices], align="center")
plt.xticks(range(X.shape[1]), np.array(X_train.columns)[indices], rotation=90)
plt.xlabel("Características")
plt.ylabel("Importancia")
plt.tight_layout()
plt.show()
# Linear Regression
pfi = permutation_importance(model_lr, X_test, y_test, n_repeats=10, random_state=42)
importances = pfi.importances_mean
importances_std = pfi.importances_std
indices = np.argsort(importances)[::-1]
plt.figure(figsize=(8, 6))
plt.title("Permuted Feature Importance (PFI)")
plt.bar(range(X.shape[1]), importances[indices], yerr=importances_std[indices], align="center")
plt.xticks(range(X.shape[1]), np.array(X_train.columns)[indices], rotation=90)
plt.xlabel("Características")
plt.ylabel("Importancia")
plt.tight_layout()
plt.show()
'''






# SHAP local
import shap
instance_idx = 0
# Random Forest
explainer = shap.Explainer(model_rf)
shap_values = explainer(X)
#local_values = shap_values[0][instance_idx]
shap.plots.scatter(shap_values[:, "Schools_Count"])

#shap.initjs()
#shap.force_plot(explainer.expected_value, shap_values[0, :], X.iloc[0, :])
# XGBoost
explainer = shap.Explainer(model_xgb)
explanation = explainer(X_test)
#shap.initjs()
#shap.force_plot(explainer.expected_value[1], explanation.values[0, :], X_test.iloc[0, :])
# Linear Regression
explainer = shap.Explainer(model_lr, X_train)
explanation = explainer(X_test)
#shap.initjs()
#shap.force_plot(explainer.expected_value[1], explanation.values[0, :], X_test.iloc[0, :])



'''
# LIME
from lime.lime_tabular import LimeTabularExplainer
explainer_lime = LimeTabularExplainer(X_train.values, 
                                      training_labels=y_train.values,
                                      feature_names=X_train.columns, 
                                      verbose=True, 
                                      mode='regression')
# Instancia
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



