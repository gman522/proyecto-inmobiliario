import streamlit as st
import pandas as pd

st.set_page_config(page_title="Carga de Datos", page_icon="📁", layout="wide")

st.title("📁 Carga Dinámica de Múltiples Archivos")
st.write("Sube todos los archivos (CSV o Excel) que necesites para consolidarlos en tu análisis.")

# Permitir múltiples archivos
archivos_subidos = st.file_uploader(
    "Selecciona o arrastra todos tus archivos aquí:",
    type=["csv", "xlsx", "xls"],
    accept_multiple_files=True,
    key="multi_uploader"
)

# Diccionario para almacenar datasets individualmente por nombre
if "datasets" not in st.session_state:
    st.session_state["datasets"] = {}

if archivos_subidos:
    for archivo in archivos_subidos:
        nombre = archivo.name
        try:
            if nombre.endswith(".csv"):
                # Intentar lectura estándar con coma o punto y coma
                try:
                    df = pd.read_csv(archivo)
                except Exception:
                    archivo.seek(0)
                    df = pd.read_csv(archivo, sep=";", encoding="latin1")
            else:
                df = pd.read_excel(archivo)
            
            # Guardar en Session State
            st.session_state["datasets"][nombre] = df
        except Exception as e:
            st.error(f"Error al procesar el archivo '{nombre}': {e}")

# Confirmación de archivos cargados
if st.session_state["datasets"]:
    st.success(f"✅ Se han cargado {len(st.session_state['datasets'])} archivos con éxito.")
    
    st.divider()
    st.subheader("Archivos Disponibles en Memoria")
    
    # Selector para previsualizar cualquiera de los archivos cargados
    nombre_sel = st.selectbox(
        "Selecciona un archivo para previsualizar y verificar sus columnas:",
        list(st.session_state["datasets"].keys())
    )
    
    df_sel = st.session_state["datasets"][nombre_sel]
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Filas", f"{len(df_sel):,}")
    c2.metric("Columnas", f"{len(df_sel.columns):,}")
    c3.metric("Nombre de Archivo", nombre_sel)
    
    st.dataframe(df_sel.head(50), use_container_width=True)
else:
    st.info("💡 Por favor, sube uno o más archivos arriba para iniciar.")