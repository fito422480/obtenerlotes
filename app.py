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
        
        # Try to guess status column or some useful info
        status_col = next((c for c in df.columns if 'estado' in c.lower() or 'status' in c.lower()), None)
        if status_col:
            activos = len(df[df[status_col].astype(str).str.lower().str.contains('activ|libre|dispon', na=False)])
            m2.metric("Disponibles", activos)
            m3.metric("Ocupados/Vendidos", len(df) - activos)
        else:
            m2.metric("Columnas", len(df.columns))
            m3.metric("Última Actualización", pd.Timestamp.now().strftime("%H:%M"))

        m4.metric("Empresa", "INMO SA")

        st.markdown("---")

        # Filters Row
        with st.expander("🔍 Filtros Avanzados", expanded=False):
            f_col1, f_col2, f_col3 = st.columns(3)
            
            # Search filter
            search_query = f_col1.text_input("Buscar por cualquier campo", "")
            
            # Status filter if exists
            filter_df = df.copy()
            if status_col:
                selected_status = f_col2.multiselect("Estado", options=df[status_col].unique())
                if selected_status:
                    filter_df = filter_df[filter_df[status_col].isin(selected_status)]
            
            # Project filter if exists
            project_col = next((c for c in df.columns if 'proyect' in c.lower() or 'nombre' in c.lower()), None)
            if project_col:
                selected_projects = f_col3.multiselect("Proyecto", options=df[project_col].unique())
                if selected_projects:
                    filter_df = filter_df[filter_df[project_col].isin(selected_projects)]

            if search_query:
                # Simple global search across all string columns
                filter_df = filter_df[filter_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)]

        # Data Table
        st.subheader("Catálogo de Lotes")
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
