# -*- coding: utf-8 -*-

import streamlit as st
import requests
import pandas as pd
from config import Config


# Validar configuración al inicio
def validate_configuration():
    """Valida que la configuración esté correcta."""
    is_valid, error_msg = Config.validate_required_vars()
    if not is_valid:
        st.error(f"⚠️ Error de Configuración: {error_msg}")
        st.info("""
        💡 **Tips de configuración:**
        - **Desarrollo local:** Copia `.env.example` a `.env` y configura tu API_KEY
        - **Streamlit Cloud:** Configura los secrets en Settings → Secrets de tu app
        """)
        st.stop()
    return True


@st.cache_data(show_spinner=False)
def fetch_data(api_url: str) -> pd.DataFrame:
    """
    Obtiene datos de la API y los convierte en un DataFrame.
    
    Args:
        api_url: URL del endpoint de la API
        
    Returns:
        DataFrame con los datos o DataFrame vacío si hay error
    """
    headers = Config.get_api_headers()
    
    try:
        response = requests.get(
            api_url,
            headers=headers,
            timeout=Config.API_TIMEOUT
        )
        
        # Verificar si la respuesta está vacía
        if not response.text.strip():
            st.error("⚠️ La API devolvió una respuesta vacía.")
            return pd.DataFrame()
        
        # Verificar código de estado HTTP
        response.raise_for_status()
        
        # Parsear JSON
        try:
            data = response.json()
        except ValueError as e:
            st.error(f"⚠️ Error al parsear la respuesta JSON: {e}")
            return pd.DataFrame()
        
        # Validar estructura de respuesta
        if not isinstance(data, dict):
            st.error("⚠️ La respuesta de la API no es un objeto JSON válido.")
            return pd.DataFrame()
            
        if "value" not in data:
            st.error("⚠️ La respuesta no contiene la clave 'value'.")
            return pd.DataFrame()
        
        if not isinstance(data["value"], list):
            st.error("⚠️ La clave 'value' no contiene una lista.")
            return pd.DataFrame()

        return pd.DataFrame(data["value"])
        
    except requests.exceptions.Timeout:
        st.error(f"⚠️ Timeout: La API tardó más de {Config.API_TIMEOUT} segundos en responder.")
        return pd.DataFrame()
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Error de conexión: No se pudo conectar con la API.")
        return pd.DataFrame()
    except requests.exceptions.HTTPError as e:
        st.error(f"⚠️ Error HTTP {e.response.status_code}: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"⚠️ Error inesperado al conectar con la API: {e}")
        return pd.DataFrame()


def apply_custom_design():
    """Aplica estilos personalizados ultra modernos a la aplicación."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Outfit:wght@300;400;500;600;700;800;900&display=swap');
        
        /* Variables CSS */
        :root {
            --primary-color: #ff0135;
            --primary-hover: #d6002c;
            --primary-light: #ff4d71;
            --gradient-primary: linear-gradient(135deg, #ff0135 0%, #ff4d71 50%, #ff6b8d 100%);
            --gradient-card: linear-gradient(145deg, #ffffff 0%, #fafafa 100%);
            --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.04);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -1px rgba(0, 0, 0, 0.04);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            --shadow-glow: 0 0 20px rgba(255, 1, 53, 0.3);
            --border-radius: 16px;
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        /* Base Styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        html, body, [class*="css"] {
            font-family: 'Inter', 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            font-feature-settings: 'cv02', 'cv03', 'cv04', 'cv11';
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #fafbfc 50%, #ffffff 100%);
            background-attachment: fixed;
        }
        
        /* Main Header - Ultra Modern */
        .main-header {
            background: var(--gradient-primary);
            padding: 2.5rem 3rem;
            border-radius: var(--border-radius);
            color: white;
            margin-bottom: 2.5rem;
            box-shadow: var(--shadow-xl), var(--shadow-glow);
            position: relative;
            overflow: hidden;
            transition: var(--transition);
            animation: slideInDown 0.5s ease-out;
        }
        
        .main-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, transparent 100%);
            pointer-events: none;
        }
        
        .main-header:hover {
            transform: translateY(-2px);
            box-shadow: 0 25px 30px -5px rgba(255, 1, 53, 0.25), 0 15px 15px -5px rgba(255, 1, 53, 0.2);
        }
        
        /* Buttons - Premium Design */
        .stButton>button {
            border-radius: 12px;
            background: var(--gradient-primary);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            font-size: 0.95rem;
            transition: var(--transition);
            width: 100%;
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow-md);
            letter-spacing: 0.3px;
        }
        
        .stButton>button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg), var(--shadow-glow);
            background: linear-gradient(135deg, var(--primary-hover) 0%, #ff0135 50%, var(--primary-light) 100%);
        }
        
        .stButton>button:hover::before {
            width: 300px;
            height: 300px;
        }
        
        .stButton>button:active {
            transform: translateY(0);
            box-shadow: var(--shadow-md);
        }
        
        /* Metric Cards - Modern Cards with Hover */
        .stMetric {
            background: var(--gradient-card);
            padding: 1.75rem;
            border-radius: var(--border-radius);
            border: 1px solid rgba(255, 1, 53, 0.1);
            box-shadow: var(--shadow-sm);
            transition: var(--transition);
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
            animation: fadeInUp 0.5s ease-out backwards;
        }
        
        .stMetric::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: var(--gradient-primary);
            transform: scaleX(0);
            transform-origin: left;
            transition: transform 0.3s ease;
        }
        
        .stMetric:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: var(--shadow-xl), 0 0 30px rgba(255, 1, 53, 0.15);
            border-color: rgba(255, 1, 53, 0.3);
            background: linear-gradient(145deg, #ffffff 0%, #fffafa 100%);
        }
        
        .stMetric:hover::before {
            transform: scaleX(1);
        }
        
        .stMetric:nth-child(1) { animation-delay: 0.1s; }
        .stMetric:nth-child(2) { animation-delay: 0.2s; }
        .stMetric:nth-child(3) { animation-delay: 0.3s; }
        .stMetric:nth-child(4) { animation-delay: 0.4s; }
        
        [data-testid="stMetricValue"] {
            color: var(--primary-color);
            font-size: 2.5rem;
            font-weight: 800;
            line-height: 1.2;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            transition: var(--transition);
        }
        
        .stMetric:hover [data-testid="stMetricValue"] {
            transform: scale(1.05);
        }
        
        [data-testid="stMetricLabel"] {
            color: #64748b;
            font-weight: 600;
            font-size: 0.9rem;
            letter-spacing: 0.2px;
            margin-top: 0.5rem;
            text-transform: uppercase;
            opacity: 0.8;
        }
        
        /* Sidebar - Glassmorphism */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%);
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(226, 232, 240, 0.8);
            box-shadow: 4px 0 20px rgba(0, 0, 0, 0.03);
        }
        
        section[data-testid="stSidebar"] .css-1d391kg {
            padding-top: 1.5rem;
        }
        
        /* Selectbox - Modern */
        .stSelectbox>div>div {
            background: white;
            border-radius: 12px;
            border: 2px solid rgba(226, 232, 240, 0.8);
            transition: var(--transition);
            box-shadow: var(--shadow-sm);
        }
        
        .stSelectbox>div>div:hover {
            border-color: var(--primary-color);
            box-shadow: var(--shadow-md);
            transform: translateY(-1px);
        }
        
        /* Tables and Dataframes - Premium */
        [data-testid="stDataFrame"] {
            border-radius: var(--border-radius);
            overflow: hidden;
            border: 1px solid rgba(226, 232, 240, 0.8);
            box-shadow: var(--shadow-md);
            background: white;
            transition: var(--transition);
        }
        
        [data-testid="stDataFrame"]:hover {
            box-shadow: var(--shadow-lg);
            border-color: rgba(255, 1, 53, 0.2);
        }
        
        /* Expander - Modern Cards */
        .streamlit-expanderHeader {
            background: white;
            border-radius: 12px;
            border: 2px solid rgba(226, 232, 240, 0.6);
            padding: 1rem 1.25rem;
            transition: var(--transition);
            box-shadow: var(--shadow-sm);
            font-weight: 600;
        }
        
        .streamlit-expanderHeader:hover {
            background: linear-gradient(145deg, #ffffff 0%, #fafafa 100%);
            border-color: var(--primary-color);
            box-shadow: var(--shadow-md);
            transform: translateY(-2px);
        }
        
        .streamlit-expanderContent {
            background: white;
            border-radius: 0 0 12px 12px;
            padding: 1.5rem;
            border: 2px solid rgba(226, 232, 240, 0.6);
            border-top: none;
            box-shadow: var(--shadow-sm);
        }
        
        /* Text Input - Modern */
        .stTextInput>div>div>input {
            border-radius: 12px;
            border: 2px solid rgba(226, 232, 240, 0.8);
            padding: 0.75rem 1rem;
            transition: var(--transition);
            box-shadow: var(--shadow-sm);
        }
        
        .stTextInput>div>div>input:focus {
            border-color: var(--primary-color);
            box-shadow: var(--shadow-md), 0 0 0 4px rgba(255, 1, 53, 0.1);
            outline: none;
        }
        
        /* Multiselect - Modern */
        .stMultiSelect>div>div {
            border-radius: 12px;
            border: 2px solid rgba(226, 232, 240, 0.8);
            transition: var(--transition);
            box-shadow: var(--shadow-sm);
        }
        
        .stMultiSelect>div>div:hover {
            border-color: var(--primary-color);
            box-shadow: var(--shadow-md);
        }
        
        /* Typography */
        h1 {
            color: #0f172a;
            font-weight: 800;
            font-size: 2.5rem;
            letter-spacing: -0.5px;
            line-height: 1.2;
        }
        
        h2, h3 {
            color: #1e293b;
            font-weight: 700;
            letter-spacing: -0.3px;
        }
        
        /* Divider */
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent 0%, rgba(226, 232, 240, 0.8) 50%, transparent 100%);
            margin: 2rem 0;
        }
        
        /* Info Box */
        [data-testid="stInfo"] {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(147, 51, 234, 0.1) 100%);
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 12px;
            padding: 1rem;
            box-shadow: var(--shadow-sm);
        }
        
        /* Download Button */
        .stDownloadButton>button {
            background: var(--gradient-primary);
            border-radius: 12px;
            font-weight: 600;
            transition: var(--transition);
            box-shadow: var(--shadow-md);
        }
        
        .stDownloadButton>button:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg), var(--shadow-glow);
        }
        
        /* Animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes slideInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Loading Spinner */
        .stSpinner>div {
            border-color: var(--primary-color) transparent transparent transparent;
        }
        
        /* Scrollbar - Modern */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--gradient-primary);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--primary-hover);
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .main-header {
                padding: 1.5rem 2rem;
            }
            
            .stMetric {
                padding: 1.25rem;
            }
            
            [data-testid="stMetricValue"] {
                font-size: 2rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)


def render_sidebar(endpoints: dict) -> tuple[str, bool]:
    """
    Renderiza la barra lateral y retorna la selección del usuario.
    
    Returns:
        tuple: (selected_endpoint, reload_data)
    """
    with st.sidebar:
        try:
            st.image(Config.LOGO_URL, width='stretch')
        except Exception:
            st.warning("⚠️ No se pudo cargar el logo. Verifica la URL en la configuración.")
        
        st.markdown("---")
        st.subheader("Configuración")
        selected_endpoint = st.selectbox(
            "Seleccionar Conjunto de Datos",
            options=list(endpoints.keys()),
            help="Elige qué datos deseas consultar de la API."
        )
        st.markdown("---")
        reload_data = st.button("Actualizar Datos", width='stretch')
        st.markdown("---")
        st.markdown("### Info")
        st.info(f"Visualizando datos de **{selected_endpoint}** directamente desde la API de INMO.")
    
    return selected_endpoint, reload_data


def render_metrics(df: pd.DataFrame, selected_endpoint: str) -> str:
    """
    Renderiza las métricas del dashboard.
    
    Returns:
        Nombre de la columna de estado si existe, None en caso contrario
    """
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(f"Total {selected_endpoint}", len(df))
    
    status_col = next(
        (c for c in df.columns if 'estado' in c.lower() or 'status' in c.lower()),
        None
    )
    
    if status_col:
        status_counts = df[status_col].value_counts()
        principal_status = status_counts.idxmax()
        principal_count = status_counts.max()
        
        m2.metric(f"Estado: {principal_status}", principal_count)
        
        if len(status_counts) > 1:
            sec_status = status_counts.index[1]
            sec_count = status_counts.values[1]
            m3.metric(f"Estado: {sec_status}", sec_count)
        else:
            m3.metric("Actualizado", pd.Timestamp.now().strftime("%H:%M"))
    else:
        m2.metric("Columnas", len(df.columns))
        m3.metric("Actualizado", pd.Timestamp.now().strftime("%H:%M"))

    m4.metric("Empresa", Config.EMPRESA_NOMBRE)
    
    return status_col


def render_status_breakdown(df: pd.DataFrame, status_col: str):
    """Renderiza el desglose detallado de estados."""
    if status_col and len(df[status_col].unique()) > 1:
        with st.expander("📊 Resumen Detallado de Estados", expanded=False):
            st.write("Conteo por cada estado detectado:")
            counts = df[status_col].value_counts()
            cols = st.columns(min(len(counts), 5))
            for i, (name, val) in enumerate(counts.items()):
                cols[i % 5].metric(name, val)


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica filtros al DataFrame basado en las selecciones del usuario.
    
    Returns:
        DataFrame filtrado
    """
    filter_df = df.copy()
    
    with st.expander("🔍 Filtros Avanzados", expanded=False):
        f_col1, f_col2 = st.columns([1, 2])
        
        # Búsqueda global
        search_query = f_col1.text_input(
            "🔍 Buscador global",
            "",
            help="Busca cualquier texto en todas las columnas"
        )
        
        # Filtros dinámicos por columna
        fraccion_col = next((c for c in df.columns if 'fraccion' in c.lower()), None)
        default_filters = []
        if fraccion_col:
            default_filters.append(fraccion_col)
        status_col = next((c for c in df.columns if 'estado' in c.lower() or 'status' in c.lower()), None)
        if status_col:
            default_filters.append(status_col)
        
        cols_to_filter = f_col2.multiselect(
            "Filtrar por columnas específicas",
            options=df.columns.tolist(),
            default=default_filters
        )
        
        if cols_to_filter:
            filter_cols = st.columns(3)
            for i, col in enumerate(cols_to_filter):
                unique_vals = sorted(df[col].dropna().unique().astype(str).tolist())
                selected_vals = filter_cols[i % 3].multiselect(
                    f"Valores en {col}",
                    options=unique_vals,
                    key=f"filter_{col}"
                )
                if selected_vals:
                    filter_df = filter_df[filter_df[col].astype(str).isin(selected_vals)]

        if search_query:
            # Búsqueda global en todas las columnas
            mask = df.astype(str).apply(
                lambda x: x.str.contains(search_query, case=False, na=False)
            ).any(axis=1)
            filter_df = filter_df[filter_df.index.isin(df[mask].index)]

    return filter_df


def render_export_section(filter_df: pd.DataFrame, df: pd.DataFrame, selected_endpoint: str):
    """Renderiza la sección de exportación de datos."""
    e1, e2 = st.columns([4, 1])
    with e2:
        try:
            csv = filter_df.to_csv(index=False, sep=";", encoding="utf-8-sig")
            st.download_button(
                label="⬇️ Exportar CSV",
                data=csv,
                file_name=f"{selected_endpoint.lower()}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                width='stretch'
            )
        except Exception as e:
            st.error(f"⚠️ Error al generar CSV: {e}")
    
    with e1:
        st.write(f"Mostrando **{len(filter_df)}** de **{len(df)}** registros.")


def main():
    """Función principal de la aplicación."""
    st.set_page_config(
        page_title="Inmo - Panel de Lotes",
        page_icon="🏗️",
        layout="wide"
    )
    
    # Validar configuración
    validate_configuration()
    
    apply_custom_design()
    
    # Obtener endpoints
    endpoints = Config.get_endpoints()
    
    # Sidebar
    selected_endpoint, reload_data = render_sidebar(endpoints)
    
    # Header principal
    st.markdown(f"""
        <div class="main-header">
            <h1 style="color: white; margin: 0;">Consulta de {selected_endpoint}</h1>
            <p style="margin: 0; opacity: 0.9;">Visualización avanzada y exportación de datos inmobiliarios</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Cargar datos
    if reload_data or f'df_{selected_endpoint}' not in st.session_state:
        with st.spinner(f"Consultando API de {selected_endpoint}..."):
            st.session_state[f'df_{selected_endpoint}'] = fetch_data(endpoints[selected_endpoint])

    df = st.session_state.get(f'df_{selected_endpoint}', pd.DataFrame())

    if not df.empty:
        # Métricas del dashboard
        status_col = render_metrics(df, selected_endpoint)
        
        # Desglose de estados
        render_status_breakdown(df, status_col)
        
        st.markdown("---")

        # Filtros
        filter_df = apply_filters(df)
        
        # Tabla de datos
        st.subheader(f"Catálogo de {selected_endpoint} ({len(filter_df)} registros)")
        st.dataframe(filter_df, width='stretch')

        st.markdown("---")
        
        # Exportación
        render_export_section(filter_df, df, selected_endpoint)
    else:
        st.info("💡 Presiona 'Actualizar Datos' en la barra lateral para comenzar.")


if __name__ == "__main__":
    main()
