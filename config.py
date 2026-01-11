# -*- coding: utf-8 -*-
"""
Módulo de configuración para cargar y validar variables de entorno.
Soporta tanto .env local como Streamlit Secrets para producción.
"""

import os
from typing import Dict, Optional, Tuple

# Intentar cargar variables desde .env (solo funciona localmente)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv no está disponible, continuar sin él
    pass


def _get_config_value(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Obtiene un valor de configuración desde múltiples fuentes.
    
    Orden de prioridad:
    1. Streamlit Secrets (si está disponible)
    2. Variables de entorno del sistema (os.getenv)
    3. Valor por defecto
    
    Args:
        key: Nombre de la variable de configuración
        default: Valor por defecto si no se encuentra
        
    Returns:
        Valor de la configuración o None
    """
    # Intentar obtener desde Streamlit Secrets (Streamlit Cloud)
    try:
        import streamlit as st
        from streamlit.errors import StreamlitSecretNotFoundError
        if hasattr(st, 'secrets'):
            try:
                # Intentar acceder a los secrets
                secrets_dict = dict(st.secrets)
                value = secrets_dict.get(key, None)
                if value:
                    return str(value)
            except (AttributeError, KeyError, TypeError, StreamlitSecretNotFoundError):
                # Secrets no disponibles o no encontrados
                pass
    except (ImportError, RuntimeError, AttributeError):
        # Streamlit no está disponible o no está inicializado
        pass
    
    # Intentar obtener desde variables de entorno
    value = os.getenv(key)
    if value:
        return value
    
    # Usar valor por defecto
    return default


class Config:
    """Clase para manejar la configuración de la aplicación."""
    
    # API Configuration
    API_KEY: Optional[str] = _get_config_value("API_KEY")
    
    # API Endpoints
    ENDPOINT_LOTES: str = _get_config_value(
        "ENDPOINT_LOTES",
        "https://shift.century.com.py/inmo/next/lotes/lotes"
    ) or "https://shift.century.com.py/inmo/next/lotes/lotes"
    
    ENDPOINT_FRACCIONES: str = _get_config_value(
        "ENDPOINT_FRACCIONES",
        "https://shift.century.com.py/inmo/next/lotes/fracciones"
    ) or "https://shift.century.com.py/inmo/next/lotes/fracciones"
    
    ENDPOINT_CLIENTES: str = _get_config_value(
        "ENDPOINT_CLIENTES",
        "https://shift.century.com.py/inmo/next/lotes/clientes"
    ) or "https://shift.century.com.py/inmo/next/lotes/clientes"
    
    # Application Configuration
    LOGO_URL: str = _get_config_value(
        "LOGO_URL",
        "https://inmo.com.py/wp-content/uploads/2024/05/inmoLogo2.000a43bf-1.png"
    ) or "https://inmo.com.py/wp-content/uploads/2024/05/inmoLogo2.000a43bf-1.png"
    
    EMPRESA_NOMBRE: str = _get_config_value("EMPRESA_NOMBRE", "INMO SA") or "INMO SA"
    
    # API Request Configuration
    _api_timeout_str = _get_config_value("API_TIMEOUT", "30")
    API_TIMEOUT: int = int(_api_timeout_str) if _api_timeout_str else 30
    
    API_ACCEPT: str = _get_config_value("API_ACCEPT", "application/json") or "application/json"
    
    @classmethod
    def get_endpoints(cls) -> Dict[str, str]:
        """Retorna un diccionario con todos los endpoints configurados."""
        return {
            "Lotes": cls.ENDPOINT_LOTES,
            "Fracciones": cls.ENDPOINT_FRACCIONES,
            "Clientes": cls.ENDPOINT_CLIENTES
        }
    
    @classmethod
    def validate_required_vars(cls) -> Tuple[bool, Optional[str]]:
        """
        Valida que las variables de entorno requeridas estén configuradas.
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not cls.API_KEY:
            error_msg = (
                "API_KEY no está configurada. "
                "Por favor, configura tu API_KEY en:\n"
                "- Archivo .env (para desarrollo local)\n"
                "- Streamlit Secrets (para Streamlit Cloud)"
            )
            return False, error_msg
        
        return True, None
    
    @classmethod
    def get_api_headers(cls) -> Dict[str, str]:
        """Retorna los headers estándar para las peticiones a la API."""
        return {
            "ApiKey": cls.API_KEY or "",
            "Accept": cls.API_ACCEPT
        }
