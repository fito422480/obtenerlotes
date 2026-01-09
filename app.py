# -*- coding: utf-8 -*-

import streamlit as st
import requests
import pandas as pd

API_KEY = "F5D8A1298A8642CFE053820001C704DD"

ENDPOINTS = {
    "Lotes": "https://shift.century.com.py/inmo/next/lotes/lotes",
    "Fracciones": "https://shift.century.com.py/inmo/next/lotes/fracciones",
    "Clientes": "https://shift.century.com.py/inmo/next/lotes/clientes"
}

LOGO_URL = "https://inmo.com.py/wp-content/uploads/2024/05/inmoLogo2.000a43bf-1.png"

@st.cache_data(show_spinner=False)
def fetch_data(api_url):
    headers = {
        "ApiKey": API_KEY,
        "Accept": "application/json"
    }
    try:
        response = requests.get(api_url, headers=headers, timeout=30)
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
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
        
        html, body, [class*="css"] {{
            font-family: 'Outfit', sans-serif;
        }}
        
        .stApp {{
            background-color: #ffffff;
        }}
        
        /* Main Header Styling */
        .main-header {{
            background: linear-gradient(90deg, #ff0135 0%, #ff4d71 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 10px 15px -3px rgba(255, 1, 53, 0.2);
        }}
        
        /* Buttons */
        .stButton>button {{
            border-radius: 10px;
            background-color: #ff0135;
            color: white;
            border: none;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            width: 100%;
        }}
        
        .stButton>button:hover {{
            background-color: #d6002c;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(255, 1, 53, 0.3);
            border: none;
            color: white;
        }}
        
        /* Metric Cards */
        [data-testid="stMetricValue"] {{
            color: #ff0135;
            font-size: 2.2rem;
            font-weight: 700;
        }}
        
        [data-testid="stMetricLabel"] {{
            color: #4b5563;
            font-weight: 500;
        }}
        
        .stMetric {{
            background-color: #fffafa;
            padding: 1.2rem;
            border-radius: 12px;
            border: 1px solid #ffebeb;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        }}
        
        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background-color: #f8fafc;
            border-right: 1px solid #e2e8f0;
        }}
        
        /* Tables and Dataframes */
        [data-testid="stDataFrame"] {{
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #e2e8f0;
        }}
        
        /* Expander */
        .streamlit-expanderHeader {{
            background-color: #ffffff;
            border-radius: 10px;
            border: 1px solid #e2e8f0;
        }}
        
        h1 {{ color: #111827; font-weight: 800; }}
        h2, h3 {{ color: #1f2937; font-weight: 700; }}
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
        st.image(LOGO_URL, width='stretch')
        st.markdown("---")
        st.subheader("Configuración")
        selected_endpoint = st.selectbox(
            "Seleccionar Conjunto de Datos",
            options=list(ENDPOINTS.keys()),
            help="Elige qué datos deseas consultar de la API."
        )
        st.markdown("---")
        reload_data = st.button("Actualizar Datos", width='stretch')
        st.markdown("---")
        st.markdown("### Info")
        st.info(f"Visualizando datos de **{selected_endpoint}** directamente desde la API de INMO.")

    # Main Header
    st.markdown(f"""
        <div class="main-header">
            <h1 style="color: white; margin: 0;">Consulta de {selected_endpoint} - INMO</h1>
            <p style="margin: 0; opacity: 0.9;">Visualización avanzada y exportación de datos inmobiliarios</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    # col1 empty now as header is above, col2 for data loading logic
    with col2:
        # If selection changes, we should reload or handle it
        if reload_data or f'df_{selected_endpoint}' not in st.session_state:
            with st.spinner(f"Consultando API de {selected_endpoint}..."):
                st.session_state[f'df_{selected_endpoint}'] = fetch_data(ENDPOINTS[selected_endpoint])

    df = st.session_state.get(f'df_{selected_endpoint}', pd.DataFrame())

    if not df.empty:
        # Dashboard Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(f"Total {selected_endpoint}", len(df))
        
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
            fraccion_col = next((c for c in df.columns if 'fraccion' in c.lower()), None)
            default_filters = []
            if fraccion_col: default_filters.append(fraccion_col)
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
        st.subheader(f"Catálogo de {selected_endpoint} ({len(filter_df)} registros)")
        st.dataframe(
            filter_df, 
            width='stretch'
        )

        st.markdown("---")
        
        # Export Footer
        e1, e2 = st.columns([4, 1])
        with e2:
            csv = filter_df.to_csv(index=False, sep=";", encoding="utf-8-sig")
            st.download_button(
                label="⬇️ Exportar CSV",
                data=csv,
                file_name=f"{selected_endpoint.lower()}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                width='stretch'
            )
        with e1:
            st.write(f"Mostrando **{len(filter_df)}** de **{len(df)}** registros.")

    else:
        st.info("Presiona 'Actualizar Datos' en la barra lateral para comenzar.")


if __name__ == "__main__":
    main()
