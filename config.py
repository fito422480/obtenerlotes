# -*- coding: utf-8 -*-
"""
Módulo de configuración para cargar y validar variables de entorno.
"""

import os
from typing import Dict, Optional, Tuple
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()


class Config:
    """Clase para manejar la configuración de la aplicación."""
    
    # API Configuration
    API_KEY: Optional[str] = os.getenv("API_KEY")
    
    # API Endpoints
    ENDPOINT_LOTES: str = os.getenv(
        "ENDPOINT_LOTES",
        "https://shift.century.com.py/inmo/next/lotes/lotes"
    )
    ENDPOINT_FRACCIONES: str = os.getenv(
        "ENDPOINT_FRACCIONES",
        "https://shift.century.com.py/inmo/next/lotes/fracciones"
    )
    ENDPOINT_CLIENTES: str = os.getenv(
        "ENDPOINT_CLIENTES",
        "https://shift.century.com.py/inmo/next/lotes/clientes"
    )
    
    # Application Configuration
    LOGO_URL: str = os.getenv(
        "LOGO_URL",
        "https://inmo.com.py/wp-content/uploads/2024/05/inmoLogo2.000a43bf-1.png"
    )
    EMPRESA_NOMBRE: str = os.getenv("EMPRESA_NOMBRE", "INMO SA")
    
    # API Request Configuration
    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "30"))
    API_ACCEPT: str = os.getenv("API_ACCEPT", "application/json")
    
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
            return False, "API_KEY no está configurada. Por favor, configura tu API_KEY en el archivo .env"
        
        return True, None
    
    @classmethod
    def get_api_headers(cls) -> Dict[str, str]:
        """Retorna los headers estándar para las peticiones a la API."""
        return {
            "ApiKey": cls.API_KEY or "",
            "Accept": cls.API_ACCEPT
        }
