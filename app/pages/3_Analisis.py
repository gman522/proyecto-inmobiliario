import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Análisis Comparativo", page_icon="📈", layout="wide")

st.title("📈 Página 3 — Concentración Territorial y Variaciones de Precios")

datasets = st.session_state.get("datasets", {})

if not datasets:
    st.warning("⚠️️ No hay archivos cargados. Ve a la **Página 1 (Contexto y Datos)** para subir tus archivos.")
    st.stop()

# --- gráfica 1: Comparativa de Precio Mediano por Comuna ---
st.subheader("1. Valor Mediano del Precio de Viviendas por Comuna")

resumenes = []
for name, df in datasets.items():
    if "Comuna" in df.columns and "Price_UF" in df.columns:
        res = df.groupby("Comuna")["Price_UF"].median().reset_index()
        res["Fuente_Archivo"] = name
        resumenes.append(res)

if resumenes:
    df_comp = pd.concat(resumenes, ignore_index=True)
    
    fig_bar = px.bar(
        df_comp,
        x="Price_UF",
        y="Comuna",
        color="Fuente_Archivo",
        barmode="group",
        height=750,
        title="Comparativo del Precio Mediano de Oferta (UF) según Comuna y Archivo Base",
        labels={
            "Price_UF": "Precio Mediano [UF]",
            "Comuna": "Comuna de Ubicación",
            "Fuente_Archivo": "Archivo Evaluado"
        }
    )
    fig_bar.update_layout(
        xaxis_title="Precio Mediano de Oferta [Unidades de Fomento - UF]",
        yaxis_title="Comuna",
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.info("No se encontraron las columnas 'Comuna' y 'Price_UF' en los datos.")

# --- gráfico 2: Análisis de Variación Temporal entre 2 Muestras ---
keys = list(datasets.keys())
if len(keys) >= 2:
    st.divider()
    st.subheader("2. Distribución Porcentual de Variación de Precios entre Dos Períodos")
    
    col_a, col_b = st.columns(2)
    f1 = col_a.selectbox("Seleccionar Período A (Base):", keys, index=0)
    f2 = col_b.selectbox("Seleccionar Período B (Comparativo):", keys, index=1 if len(keys) > 1 else 0)
    
    df1 = datasets[f1]
    df2 = datasets[f2]
    
    if "id" in df1.columns and "id" in df2.columns and "Price_UF" in df1.columns and "Price_UF" in df2.columns:
        m = df1[["id", "Price_UF"]].merge(df2[["id", "Price_UF"]], on="id", suffixes=("_Base", "_Comp"))
        m["Diferencia_UF"] = m["Price_UF_Comp"] - m["Price_UF_Base"]
        
        def clasificar(d):
            if d > 0: return "Incremento de Precio (> 0 UF)"
            elif d < 0: return "Disminución de Precio (< 0 UF)"
            return "Sin Variación (0 UF)"
            
        m["Estado_Variacion"] = m["Diferencia_UF"].apply(clasificar)
        res_estado = m["Estado_Variacion"].value_counts().reset_index()
        res_estado.columns = ["Estado de Variación", "Cantidad de Propiedades"]
        
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown(f"**Comparación de Propiedades Reincidentes (ID):**")
            st.metric("Total Propiedades Matheadas", f"{len(m):,} unidades")
            st.dataframe(res_estado, use_container_width=True)
            
        with c2:
            fig_pie = px.pie(
                res_estado, 
                names="Estado de Variación", 
                values="Cantidad de Propiedades", 
                hole=0.4,
                title=f"Proporción de Cambios de Precio [UF] ({f1} vs {f2})",
                labels={"Cantidad de Propiedades": "Número de Publicaciones [Unidades]"}
            )
            fig_pie.update_traces(textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)