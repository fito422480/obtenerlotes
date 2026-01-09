# -*- coding: utf-8 -*-

import streamlit as st
import requests
import pandas as pd

API_URL = "https://shift.century.com.py/inmo/next/lotes/lotes"
API_KEY = "F5D8A1298A8642CFE053820001C704DD"


LOGO_URL = "https://inmo.com.py/wp-content/uploads/2024/05/inmoLogo2.000a43bf-1.png"

@st.cache_data(show_spinner=False)
def fetch_lotes():
    headers = {
        "ApiKey": API_KEY,
        "Accept": "application/json"
    }
    try:
        response = requests.get(API_URL, headers=headers, timeout=30)
        # Check if response is empty or not JSON
        if not response.text.strip():
            st.error("La API devolvió una respuesta vacía.")
            return pd.DataFrame()
        
        response.raise_for_status()
        data = response.json()

        if "value" not in data:
            st.error("La respuesta no contiene la clave 'value'")
            return pd.DataFrame()

        return pd.DataFrame(data["value"])
    except Exception as e:
        st.error(f"Error al conectar con la API: {e}")
        return pd.DataFrame()

def apply_custom_design():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        .main {
            background-color: #f8fafc;
        }
        
        .stButton>button {
            border-radius: 8px;
            background-color: #1e293b;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #334155;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        }
        
        .metric-card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
            border-left: 5px solid #1e293b;
        }
        
        .sidebar-content {
            padding: 1rem;
        }
        
        h1, h2, h3 {
            color: #1e293b;
            font-weight: 700;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Inmo - Panel de Lotes",
        page_icon="🏗️",
        layout="wide"
    )
    
    apply_custom_design()

    # Sidebar
    with st.sidebar:
        st.image(LOGO_URL, use_container_width=True)
        st.markdown("---")
        st.subheader("Configuración")
        reload_data = st.button("🔄 Actualizar Datos", use_container_width=True)
        st.markdown("---")
        st.markdown("### Info")
        st.info("Este panel permite visualizar y exportar la lista completa de lotes directamente desde la API de INMO.")

    # Main Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Consulta de Lotes - INMO")
        st.caption("Visualización avanzada y exportación de datos inmobiliarios")
    
    with col2:
        if reload_data or 'df_lotes' not in st.session_state:
            with st.spinner("Consultando API..."):
                st.session_state.df_lotes = fetch_lotes()

    df = st.session_state.get('df_lotes', pd.DataFrame())

    if not df.empty:
        # Dashboard Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Lotes", len(df))
        
        status_col = next((c for c in df.columns if 'estado' in c.lower() or 'status' in c.lower()), None)
        
        if status_col:
            # Full breakdown of statuses
            status_counts = df[status_col].value_counts()
            principal_status = status_counts.idxmax()
            principal_count = status_counts.max()
            
            # Show the most frequent status as a metric
            m2.metric(f"Estado: {principal_status}", principal_count)
            
            # Show the second most frequent if exists
            if len(status_counts) > 1:
                sec_status = status_counts.index[1]
                sec_count = status_counts.values[1]
                m3.metric(f"Estado: {sec_status}", sec_count)
            else:
                m3.metric("Actualizado", pd.Timestamp.now().strftime("%H:%M"))
        else:
            m2.metric("Columnas", len(df.columns))
            m3.metric("Actualizado", pd.Timestamp.now().strftime("%H:%M"))

        m4.metric("Empresa", "INMO SA")

        # Status Breakdown Expander
        if status_col and len(df[status_col].unique()) > 1:
            with st.expander("📊 Resumen Detallado de Estados", expanded=False):
                st.write("Conteo por cada estado detectado:")
                # Create horizontal metrics for all statuses
                counts = df[status_col].value_counts()
                cols = st.columns(min(len(counts), 5))
                for i, (name, val) in enumerate(counts.items()):
                    cols[i % 5].metric(name, val)

        st.markdown("---")

        # Filters Row
        filter_df = df.copy()
        with st.expander("🔍 Filtros Avanzados", expanded=True if df.empty else False):
            f_col1, f_col2 = st.columns([1, 2])
            
            # Global Search
            search_query = f_col1.text_input("🔍 Buscador global", "", help="Busca cualquier texto en todas las columnas")
            
            # Dynamic Filters by Column
            default_filters = []
            if status_col: default_filters.append(status_col)
            
            cols_to_filter = f_col2.multiselect(
                "Filtrar por columnas específicas", 
                options=df.columns.tolist(),
                default=default_filters
            )
            
            if cols_to_filter:
                filter_cols = st.columns(3)
                for i, col in enumerate(cols_to_filter):
                    unique_vals = sorted(df[col].dropna().unique().astype(str).tolist())
                    selected_vals = filter_cols[i % 3].multiselect(f"Valores en {col}", options=unique_vals, key=f"filter_{col}")
                    if selected_vals:
                        filter_df = filter_df[filter_df[col].astype(str).isin(selected_vals)]

            if search_query:
                # Global search across all columns
                mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
                filter_df = filter_df[filter_df.index.isin(df[mask].index)]

        # Data Table
        st.subheader(f"Catálogo de Lotes ({len(filter_df)} registros)")
        st.dataframe(
            filter_df, 
            use_container_width=True, 
            column_config={status_col: "Estado"} if status_col else {}
        )

        st.markdown("---")
        
        # Export Footer
        e1, e2 = st.columns([4, 1])
        with e2:
            csv = filter_df.to_csv(index=False, sep=";", encoding="utf-8-sig")
            st.download_button(
                label="⬇️ Exportar CSV",
                data=csv,
                file_name=f"lotes_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        with e1:
            st.write(f"Mostrando **{len(filter_df)}** de **{len(df)}** registros.")

    else:
        st.info("Presiona 'Actualizar Datos' en la barra lateral para comenzar.")


if __name__ == "__main__":
    main()
