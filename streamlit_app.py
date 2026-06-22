import streamlit as st

st.set_page_config(
    page_title="Predicción de Dosificación de Zinc",
    page_icon="⚗️",
    layout="wide"
)

# ==========================
# ESTILOS
# ==========================

st.markdown("""
<style>
.main-header {
    font-size: 42px;
    font-weight: bold;
    color: #1f77b4;
}

.section-title {
    font-size: 26px;
    font-weight: bold;
    color: #2c3e50;
    margin-top:20px;
}

.info-box {
    background-color: #f8f9fa;
    padding: 15px;
    border-radius: 10px;
    border-left: 6px solid #1f77b4;
}

.result-box {
    background-color: #e8f5e9;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# TÍTULO
# ==========================

st.markdown(
    '<p class="main-header">⚗️ Predicción de Dosificación de Polvo de Zinc</p>',
    unsafe_allow_html=True
)

st.caption("Sistema de apoyo para operación Merrill-Crowe")

# ==========================
# EXPLICACIÓN
# ==========================

st.markdown(
    '<p class="section-title">¿Qué es el proceso Merrill-Crowe?</p>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="info-box">

El proceso <b>Merrill-Crowe</b> es una técnica utilizada en minería para recuperar
<b>oro (Au)</b> y <b>plata (Ag)</b> desde soluciones cianuradas.

Las etapas principales son:

1. Lixiviación del mineral.
2. Clarificación de la solución.
3. Desoxigenación.
4. Adición de polvo de zinc.
5. Precipitación de oro y plata.
6. Filtrado y recuperación del precipitado.

La correcta dosificación de zinc es importante porque:

- Una dosis baja reduce la recuperación de metales.
- Una dosis alta incrementa costos operacionales.

</div>
""", unsafe_allow_html=True)

# ==========================
# INPUTS
# ==========================

st.markdown(
    '<p class="section-title">Variables de Entrada</p>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    au = st.number_input(
        "Concentración de Oro (mg/L)",
        min_value=0.0,
        value=5.0
    )

    ag = st.number_input(
        "Concentración de Plata (mg/L)",
        min_value=0.0,
        value=50.0
    )

with col2:

    caudal = st.number_input(
        "Caudal de Solución (m³/h)",
        min_value=0.0,
        value=100.0
    )

    factor = st.slider(
        "Factor de Seguridad",
        1.0,
        2.0,
        1.2,
        0.05
    )

# ==========================
# INFO DE VARIABLES
# ==========================

with st.expander("📋 Información esperada de los datos"):

    st.markdown("""
    **Oro (Au):**
    - Unidad: mg/L
    - Concentración de oro disuelto.

    **Plata (Ag):**
    - Unidad: mg/L
    - Concentración de plata disuelta.

    **Caudal:**
    - Unidad: m³/h
    - Flujo de solución rica que ingresa al proceso.

    **Factor de Seguridad:**
    - Ajuste operacional para asegurar precipitación completa.
    """)

# ==========================
# BOTÓN
# ==========================

st.divider()

if st.button("🔍 Calcular Dosificación", use_container_width=True):

    # Fórmula DEMO
    zinc = (au + 0.5 * ag) * caudal * 0.0001
    zinc *= factor

    st.markdown(
        f"""
        <div class="result-box">
        <h2>Dosificación Recomendada</h2>
        <h1>{zinc:.3f} kg/h</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Consumo Diario",
            f"{zinc*24:.2f} kg/día"
        )

    with col2:
        st.metric(
            "Consumo Mensual",
            f"{zinc*24*30:.2f} kg/mes"
        )

# ==========================
# PIE
# ==========================

st.divider()

st.info(
    "Nota: la ecuación utilizada es referencial. "
    "Debe reemplazarse por el modelo metalúrgico o predictivo real."
)
