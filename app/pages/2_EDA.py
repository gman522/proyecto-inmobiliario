import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Análisis Exploratorio", page_icon="🔍", layout="wide")

st.title("🔍 Página 2 — Análisis Exploratorio de Datos (EDA)")

datasets = st.session_state.get("datasets", {})

if not datasets:
    st.warning("⚠️️ No hay archivos cargados. Ve a la **Página 1 (Contexto y Datos)** para subir tus archivos.")
    st.stop()

# Menú Lateral
st.sidebar.header("Opciones de Visualización")
modo = st.sidebar.radio("Ámbito del Análisis:", ["Archivo Individual", "Consolidado Multi-Archivo"])

if modo == "Archivo Individual":
    archivo_sel = st.sidebar.selectbox("Seleccionar Archivo:", list(datasets.keys()))
    df = datasets[archivo_sel].copy()
    nombre_fuente = archivo_sel
else:
    dfs = []
    for name, d in datasets.items():
        temp = d.copy()
        temp["Fuente_Archivo"] = name
        dfs.append(temp)
    df = pd.concat(dfs, ignore_index=True)
    nombre_fuente = "Consolidado de Archivos"

# Filtro por Comuna
if "Comuna" in df.columns:
    comunas = sorted([str(c) for c in df["Comuna"].dropna().unique()])
    comuna_sel = st.sidebar.selectbox("Filtrar por Comuna:", ["Todas las Comunas"] + comunas)
    if comuna_sel != "Todas las Comunas":
        df = df[df["Comuna"] == comuna_sel]
else:
    comuna_sel = "Todas las Comunas"

st.caption(f"📌 **Origen de Datos:** {nombre_fuente} | **Filtro Comuna:** {comuna_sel} | **Registros Analizados:** {len(df):,}")

# --- gráfico 1: Histograma de Precios en UF ---
if "Price_UF" in df.columns:
    st.subheader("1. Distribución de Precios de Propiedades")
    
    color_var = "Fuente_Archivo" if "Fuente_Archivo" in df.columns else None
    
    fig_hist = px.histogram(
        df[df["Price_UF"] > 0], 
        x="Price_UF", 
        color=color_var,
        nbins=50,
        title=f"Distribución Frecuencial del Precio de Oferta en UF ({comuna_sel})",
        labels={
            "Price_UF": "Precio de Publicación (Unidades de Fomento - UF)",
            "count": "Cantidad de Propiedades (Unidades)",
            "Fuente_Archivo": "Archivo de Origen"
        }
    )
    fig_hist.update_layout(
        xaxis_title="Precio de Publicación [UF]",
        yaxis_title="Frecuencia [Cantidad de Propiedades]",
        hovermode="x unified"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# --- gráfico 2: Dispersión m² Construidos vs Precio UF ---
if "Built Area" in df.columns and "Price_UF" in df.columns:
    st.subheader("2. Relación entre Superficie Construida (m²) y Precio (UF)")
    
    df_scat = df[(df["Built Area"] > 0) & (df["Built Area"] <= 1000) & (df["Price_UF"] > 0)]
    color_var = "Fuente_Archivo" if "Fuente_Archivo" in df_scat.columns else None
    
    hover_cols = [c for c in ["Comuna", "Dorms", "Baths", "Parking"] if c in df_scat.columns]
    
    fig_scat = px.scatter(
        df_scat,
        x="Built Area",
        y="Price_UF",
        color=color_var,
        hover_data=hover_cols,
        title=f"Dispersión de Superficie Construida (m²) vs. Precio de Oferta (UF) — {comuna_sel}",
        labels={
            "Built Area": "Superficie Construida [m²]",
            "Price_UF": "Precio de Oferta [UF]",
            "Dorms": "Dormitorios [Unidades]",
            "Baths": "Baños [Unidades]",
            "Fuente_Archivo": "Archivo de Origen"
        }
    )
    fig_scat.update_layout(
        xaxis_title="Superficie Construida [Metros Cuadrados - m²]",
        yaxis_title="Precio de Oferta [Unidades de Fomento - UF]"
    )
    st.plotly_chart(fig_scat, use_container_width=True)