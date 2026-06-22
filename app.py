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

st.set_page_config(page_title="Optimización de Zinc", page_icon="🏭", layout="wide")

st.title("Modelo Predictivo de Dosis de Zinc")
st.markdown("Optimización del consumo de zinc en el proceso **Merrill-Crowe** utilizando Machine Learning.")
st.divider()

@st.cache_data
def load_data():
    archivo = "Dataset_Merrill_Crowe_Zinc_Predictivo.xlsx"
    return pd.read_excel(archivo)

try:
    df = load_data()
except FileNotFoundError:
    st.error("No se encontró el archivo Excel. Asegúrate de que esté en la misma ruta que el script.")
    st.stop()

X = df[['Pureza_Zinc_pct','pH','Oro_mg_L','Turbidez_NTU','Oxigeno_Disuelto_mg_L']]
y = df['Dosis_Zinc_Polvo_g_m3']
X_const = sm.add_constant(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf = RandomForestRegressor(n_estimators=300, max_depth=12, random_state=42)
rf.fit(X_train, y_train)
pred_rf = rf.predict(X_test)

st.sidebar.header("Simulador de Dosis")
st.sidebar.markdown("Ajusta los parámetros operativos:")

val_pureza = st.sidebar.slider("Pureza del Zinc (%)", min_value=90.0, max_value=100.0, value=float(df['Pureza_Zinc_pct'].mean()), step=0.1)
val_ph = st.sidebar.slider("pH", min_value=9.0, max_value=12.0, value=float(df['pH'].mean()), step=0.1)
val_oro = st.sidebar.slider("Oro (mg/L)", min_value=0.0, max_value=20.0, value=float(df['Oro_mg_L'].mean()), step=0.1)
val_turbidez = st.sidebar.slider("Turbidez (NTU)", min_value=0.0, max_value=5.0, value=float(df['Turbidez_NTU'].mean()), step=0.1)
val_oxigeno = st.sidebar.slider("Oxígeno Disuelto (mg/L)", min_value=0.0, max_value=3.0, value=float(df['Oxigeno_Disuelto_mg_L'].mean()), step=0.1)

input_usuario = pd.DataFrame({
    'Pureza_Zinc_pct': [val_pureza],
    'pH': [val_ph],
    'Oro_mg_L': [val_oro],
    'Turbidez_NTU': [val_turbidez],
    'Oxigeno_Disuelto_mg_L': [val_oxigeno]
})

dosis_predicha = rf.predict(input_usuario)[0]

st.sidebar.divider()
st.sidebar.subheader("Resultado Sugerido:")
st.sidebar.success(f"**{dosis_predicha:.2f} g/m³ de Zinc**")

tab1, tab2, tab3 = st.tabs(["Datos y Exploración", "Rendimiento del Modelo", "Fundamento Teórico"])

with tab1:
    st.subheader("Vista Rápida del Dataset")
    st.dataframe(df.head(), use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Estadística Descriptiva")
        st.dataframe(df.describe(), use_container_width=True)
        
    with col2:
        st.subheader("Análisis de Colinealidad (VIF)")
        vif = pd.DataFrame()
        vif["Variable"] = X_const.columns
        vif["VIF"] = [variance_inflation_factor(X_const.values, i) for i in range(X_const.shape[1])]
        st.dataframe(vif, use_container_width=True)

with tab2:
    st.header("Métricas de Modelos Predictivos")
    
    st.subheader("Random Forest (Modelo Principal)")
    rf_col1, rf_col2, rf_col3 = st.columns(3)
    rf_col1.metric("R² (Exactitud)", f"{r2_score(y_test, pred_rf):.4f}")
    rf_col2.metric("MAE (Error Absoluto)", f"{mean_absolute_error(y_test, pred_rf):.4f}")
    rf_col3.metric("RMSE (Error Cuadrático)", f"{np.sqrt(mean_squared_error(y_test, pred_rf)):.4f}")
    
    st.markdown("---")
    
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        st.subheader("📈 Importancia de Variables")
        imp = pd.DataFrame({'Importancia': rf.feature_importances_}, index=X.columns)
        imp = imp.sort_values(by='Importancia', ascending=True)
        st.bar_chart(imp)
        
    with col_der:
        st.subheader("Validación y Residuos")
        scores = cross_val_score(rf, X, y, cv=5, scoring='r2')
        st.write(f"**Promedio Cross Validation R²:** {scores.mean():.4f}")
        
        residuos = y_test - pred_rf
        stat, p_value = shapiro(residuos)
        st.write("**Prueba de Normalidad de Residuos (Shapiro-Wilk):**")
        st.info(f"Estadístico: {stat:.4f} | p-valor: {p_value:.4f}")
    
    with st.expander("Ver Resumen Estadístico de Regresión Lineal (OLS)"):
        lr = LinearRegression()
        lr.fit(X_train, y_train)
        pred_lr = lr.predict(X_test)
        st.write(f"**R²:** {r2_score(y_test, pred_lr):.4f} | **MAE:** {mean_absolute_error(y_test, pred_lr):.4f}")
        
        modelo_ols = sm.OLS(y, X_const).fit()
        st.text(modelo_ols.summary())

with tab3:
    st.header("Cálculos Teóricos Merrill-Crowe")
    
    st.latex(r"2\mathrm{Au(CN)_2^-} + \mathrm{Zn} \rightarrow 2\mathrm{Au} + \mathrm{Zn(CN)_4^{2-}}")
    
    st.markdown("""
    * **Peso Molecular Au:** 196.97 g/mol
    * **Peso Molecular Zn:** 65.38 g/mol

    **Relación Estequiométrica:**
    65.38 g de Zn precipitan 393.94 g de Au (Equivale a **0.166 g Zn / g Au**).
    
    > **Nota Operativa:** En planta se utilizan excesos de 2x a 20x respecto al cálculo teórico debido a la presencia de oxígeno residual, impurezas metálicas (plata, cobre) y la pasivación mecánica de las partículas de polvo de zinc.
    """)
    
    def zinc_teorico(oro_mg_l):
        return oro_mg_l * (65.38 / (2 * 196.97))
    
    st.subheader("Calculadora Teórica Rápida")
    oro_input = st.number_input("Ingresa la concentración de Oro (mg/L):", min_value=0.0, value=10.0, step=0.5)
    st.info(f"Consumo puramente teórico para {oro_input} mg/L de Au: **{zinc_teorico(oro_input):.4f} mg/L de Zn**")
