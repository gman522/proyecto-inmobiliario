import streamlit as st

st.set_page_config(
    page_title="Análisis Inmobiliario RM",
    page_icon="🏠",
    layout="wide"
)

if "df_marzo" not in st.session_state:
    st.session_state["df_marzo"] = None
if "df_julio" not in st.session_state:
    st.session_state["df_julio"] = None

st.title("🏠 Análisis dinámico de precios de viviendas en la región metropolitana")
st.markdown("""
### Bienvenido a la Aplicación

Esta plataforma te permite cargar tus propios archivos CSV o Excel para analizar la evolución y distribución de precios.

#### Instrucciones de uso:
1. Ve a la página **1_Contexto_y_Datos** en el menú lateral.
2. Sube tus archivos correspondientes a las muestras de datos.
3. Explora los gráficos interactivos en **2_Analisis_Exploratorio** y **3_Analisis_Pregunta**.
""")