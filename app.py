import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

from scipy.stats import shapiro
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm

# 1. Configuración de la página
st.title("Modelo Predictivo de Dosis de Zinc - Merrill-Crowe")

# 2. Carga de datos con caché para optimizar Streamlit
@st.cache_data
def load_data():
    archivo = "Dataset_Merrill_Crowe_Zinc_Predictivo.xlsx"
    return pd.read_excel(archivo)

try:
    df = load_data()
except FileNotFoundError:
    st.error("No se encontró el archivo Excel. Asegúrate de que esté en la misma ruta que el script.")
    st.stop()

st.subheader("Vista de los Datos")
st.dataframe(df.head())

st.subheader("Estadística Descriptiva")
st.dataframe(df.describe())

# 3. Definición de variables
X = df[['Pureza_Zinc_pct','pH','Oro_mg_L','Turbidez_NTU','Oxigeno_Disuelto_mg_L']]
y = df['Dosis_Zinc_Polvo_g_m3']
X_const = sm.add_constant(X)

# 4. Cálculo de VIF (Usando X_const para mayor precisión estadística)
vif = pd.DataFrame()
vif["Variable"] = X_const.columns
vif["VIF"] = [variance_inflation_factor(X_const.values, i) for i in range(X_const.shape[1])]

st.subheader("Análisis de Colinealidad (VIF)")
st.dataframe(vif)

# 5. Modelo OLS de Statsmodels
st.subheader("Resumen Modelo OLS")
modelo_ols = sm.OLS(y, X_const).fit()
# Se usa st.text para mantener el formato original del summary de OLS
st.text(modelo_ols.summary())

# 6. Preparación de datos para Machine Learning
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- REGRESIÓN LINEAL ---
lr = LinearRegression()
lr.fit(X_train, y_train)
pred_lr = lr.predict(X_test)

st.subheader("Resultados: Regresión Lineal")
st.write(f"**R2:** {r2_score(y_test, pred_lr):.4f}")
st.write(f"**MAE:** {mean_absolute_error(y_test, pred_lr):.4f}")
st.write(f"**RMSE:** {np.sqrt(mean_squared_error(y_test, pred_lr)):.4f}")

# --- RANDOM FOREST ---
rf = RandomForestRegressor(n_estimators=300, max_depth=12, random_state=42)
rf.fit(X_train, y_train)
pred_rf = rf.predict(X_test)

st.subheader("Resultados: Random Forest")
st.write(f"**R2:** {r2_score(y_test, pred_rf):.4f}")
st.write(f"**MAE:** {mean_absolute_error(y_test, pred_rf):.4f}")
st.write(f"**RMSE:** {np.sqrt(mean_squared_error(y_test, pred_rf)):.4f}")

# Validación Cruzada
scores = cross_val_score(rf, X, y, cv=5, scoring='r2')
st.write("**Cross Validation R2:**", scores)
st.write(f"**Promedio CV R2:** {scores.mean():.4f}")

# 7. Análisis de Residuos
residuos = y_test - pred_rf
stat, p_value = shapiro(residuos)
st.subheader("Shapiro-Wilk (Residuos de Random Forest)")
st.write(f"Estadístico: {stat:.4f}, p-valor: {p_value:.4f}")

# 8. Importancia de Variables
imp = pd.DataFrame({'Variable': X.columns, 'Importancia': rf.feature_importances_})
imp = imp.sort_values(by='Importancia', ascending=False)
st.subheader("Importancia de las Variables (Random Forest)")
st.dataframe(imp)

# 9. Cálculo Teórico Merrill-Crowe
st.header("Cálculos Teóricos")
reaccion = "2Au(CN)2- + Zn -> 2Au + Zn(CN)4(2-)"
st.code(reaccion, language="text")

st.markdown("""
* **PM Au** = 196.97 g/mol
* **PM Zn** = 65.38 g/mol

**Teóricamente:**
65.38 g Zn precipitan 393.94 g Au (=> **0.166 g Zn / g Au**)

*En planta se utilizan excesos de 2x a 20x debido a:*
* Oxígeno residual
* Impurezas
* Plata
* Cobre
* Pasivación
""")

# Corregido: Las variables estaban sin definir, las he comentado como explicación.
# Zn_real = Zn_teorico * factor_operacional

def zinc_teorico(oro_mg_l):
    return oro_mg_l * (65.38 / (2 * 196.97))

st.write("**Ejemplo: Zn teórico para 10 mg/L Au**")
st.info(f"{zinc_teorico(10):.4f} mg/L de Zn")

st.success("Modelo ejecutado exitosamente.")
