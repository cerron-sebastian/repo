import streamlit as st

# Configuración de página
st.set_page_config(
    page_title="Dosificación de Zinc - Merrill Crowe",
    page_icon="⚙️",
    layout="centered"
)

st.title("Dosificación de Polvo de Zinc")
st.subheader("Proceso Merrill-Crowe")

st.write(
    "Ingrese los parámetros de operación para estimar "
    "la dosificación de polvo de zinc."
)

# Entradas
au = st.number_input(
    "Concentración de Oro (mg/L)",
    min_value=0.0,
    value=5.0,
    step=0.1
)

ag = st.number_input(
    "Concentración de Plata (mg/L)",
    min_value=0.0,
    value=50.0,
    step=0.1
)

caudal = st.number_input(
    "Caudal de Solución (m³/h)",
    min_value=0.0,
    value=100.0,
    step=1.0
)

factor_seguridad = st.slider(
    "Factor de Seguridad",
    min_value=1.0,
    max_value=2.0,
    value=1.2,
    step=0.05
)

st.divider()

# Cálculo
if st.button("Calcular Dosificación"):

    # Fórmula de ejemplo
    zinc_kg_h = (au + 0.5 * ag) * caudal * 0.0001
    zinc_kg_h *= factor_seguridad

    st.success(
        f"Dosificación recomendada: {zinc_kg_h:.3f} kg/h"
    )

    st.metric(
        "Consumo diario estimado",
        f"{zinc_kg_h * 24:.2f} kg/día"
    )

    st.metric(
        "Consumo mensual estimado",
        f"{zinc_kg_h * 24 * 30:.2f} kg/mes"
    )

    st.info(
        "La fórmula utilizada es únicamente referencial. "
        "Debe reemplazarse por el modelo o criterio metalúrgico real."
    )

# Pie
st.divider()
st.caption("Herramienta de apoyo para operaciones Merrill-Crowe")
