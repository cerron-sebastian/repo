import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

from scipy.stats import shapiro
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm

archivo = "Dataset_Merrill_Crowe_Zinc_Predictivo.xlsx"
df = pd.read_excel(archivo)

print(df.head())
print(df.describe())

X = df[['Pureza_Zinc_pct','pH','Oro_mg_L','Turbidez_NTU','Oxigeno_Disuelto_mg_L']]

y = df['Dosis_Zinc_Polvo_g_m3']

X_const = sm.add_constant(X)

vif = pd.DataFrame()
vif["Variable"] = X.columns
vif["VIF"] = [variance_inflation_factor(X.values, i)
              for i in range(X.shape[1])]

print("\nVIF")
print(vif)

modelo_ols = sm.OLS(y, X_const).fit()
print(modelo_ols.summary())

X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2,random_state=42)

lr = LinearRegression()
lr.fit(X_train, y_train)

pred_lr = lr.predict(X_test)

print("\nREGRESION LINEAL")
print("R2 =", r2_score(y_test, pred_lr))
print("MAE =", mean_absolute_error(y_test, pred_lr))
print("RMSE =", np.sqrt(mean_squared_error(y_test, pred_lr)))

rf = RandomForestRegressor(n_estimators=300,max_depth=12,random_state=42)
rf.fit(X_train, y_train)
pred_rf = rf.predict(X_test)

print("\nRANDOM FOREST")
print("R2 =", r2_score(y_test, pred_rf))
print("MAE =", mean_absolute_error(y_test, pred_rf))
print("RMSE =", np.sqrt(mean_squared_error(y_test, pred_rf)))

scores = cross_val_score(rf,X,y,cv=5,scoring='r2')

print("\nCross Validation R2")
print(scores)
print("Promedio =", scores.mean())

residuos = y_test - pred_rf

print("\nShapiro-Wilk residuos")
print(shapiro(residuos))

imp = pd.DataFrame({'Variable': X.columns,'Importancia': rf.feature_importances_})

imp = imp.sort_values(by='Importancia',ascending=False)

print("\nImportancia Variables")
print(imp)


reaccion = "2Au(CN)2- + Zn -> 2Au + Zn(CN)4(2-)"
print(reaccion)

#PM Au = 196.97 g/mol
#PM Zn = 65.38 g/mol

#Teoricamente:
#65.38 g Zn precipitan
#393.94 g Au

#=> 0.166 g Zn / g Au

#En planta se utilizan excesos de 2x a 20x debido a:
#- oxigeno residual
#- impurezas
#- plata
#- cobre
#- pasivacion

#Factor operacional sugerido:
Zn_real = Zn_teorico * factor_operacional


def zinc_teorico(oro_mg_l):
    return oro_mg_l * (65.38 / (2 * 196.97))

print("\nEjemplo Zn teorico para 10 mg/L Au")
print(zinc_teorico(10))

print("\nModelo listo.")
