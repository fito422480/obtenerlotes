# INMO - Exportador de Lotes

![INMO Logo](https://inmo.com.py/wp-content/uploads/2024/05/inmoLogo2.000a43bf-1.png)

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Una herramienta profesional diseñada para la **visualización, filtrado y exportación** de datos de lotes directamente desde la API de INMO. Ideal para equipos comerciales y administrativos que necesitan reportes rápidos y precisos.

## ✨ Características Principales

-   **🎯 Dashboard en Tiempo Real:** Visualiza métricas clave como total de lotes y disponibilidad al instante.
-   **🔍 Filtros Avanzados:** Filtra por estado, proyecto o cualquier campo de texto.
-   **📊 Tabla Dinámica:** Navega por los datos con una interfaz moderna y fluida.
-   **📥 Exportación Pro:** Descarga reportes en formato CSV compatible con Excel (UTF-8 con BOM).
-   **🎨 UI/UX Premium:** Diseño limpio basado en la identidad visual de INMO.

## 🚀 Instalación Rápida

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/obtenerlotes.git
    cd obtenerlotes
    ```

2.  **Crear y activar entorno virtual:**
    ```bash
    python -m venv venv
    ./venv/Scripts/activate  # En Windows
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar variables de entorno:**
    ```bash
    # Copia el archivo de ejemplo y edítalo con tus valores
    cp .env.example .env
    # Edita .env con tu editor preferido y configura tu API_KEY
    ```

## ⚙️ Configuración

La aplicación utiliza variables de entorno para su configuración. Soporta tanto `.env` para desarrollo local como **Streamlit Secrets** para producción en Streamlit Cloud.

### Variables Requeridas

- **`API_KEY`**: Tu clave de API para acceder a los servicios de INMO

### Variables Opcionales

- **`ENDPOINT_LOTES`**: URL del endpoint para lotes (tiene un valor por defecto)
- **`ENDPOINT_FRACCIONES`**: URL del endpoint para fracciones (tiene un valor por defecto)
- **`ENDPOINT_CLIENTES`**: URL del endpoint para clientes (tiene un valor por defecto)
- **`LOGO_URL`**: URL del logo de la empresa (tiene un valor por defecto)
- **`EMPRESA_NOMBRE`**: Nombre de la empresa (por defecto: "INMO SA")
- **`API_TIMEOUT`**: Tiempo de espera para las peticiones API en segundos (por defecto: 30)
- **`API_ACCEPT`**: Tipo de contenido aceptado (por defecto: "application/json")

### Configuración para Desarrollo Local

Copia el archivo `.env.example` a `.env` y configura tus variables:

```bash
cp .env.example .env
# Edita .env con tu editor preferido
```

Ejemplo de archivo `.env`:
```env
API_KEY=tu_api_key_aqui
ENDPOINT_LOTES=https://shift.century.com.py/inmo/next/lotes/lotes
ENDPOINT_FRACCIONES=https://shift.century.com.py/inmo/next/lotes/fracciones
ENDPOINT_CLIENTES=https://shift.century.com.py/inmo/next/lotes/clientes
LOGO_URL=https://inmo.com.py/wp-content/uploads/2024/05/inmoLogo2.000a43bf-1.png
EMPRESA_NOMBRE=INMO SA
API_TIMEOUT=30
API_ACCEPT=application/json
```

### Configuración para Streamlit Cloud

1. Ve a tu app en [Streamlit Cloud](https://share.streamlit.io/)
2. Click en **"Settings"** (⚙️) → **"Secrets"**
3. Pega el contenido del archivo `.streamlit/secrets.toml.example` y configura tus valores:

```.env
API_KEY = "tu_api_key_aqui"
ENDPOINT_LOTES = ""
ENDPOINT_FRACCIONES = ""
ENDPOINT_CLIENTES = ""
LOGO_URL = ""
EMPRESA_NOMBRE = ""
API_TIMEOUT = "30"
API_ACCEPT = "application/json"
```

> ⚠️ **Importante**: 
> - El archivo `.env` no debe ser subido al repositorio (ya está incluido en `.gitignore`)
> - Los secrets de Streamlit Cloud son privados y seguros

## 🛠️ Uso

Para iniciar la aplicación, ejecuta el siguiente comando en tu terminal:

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador predeterminado (usualmente en `http://localhost:8501`).

## 👨‍💻 Tecnologías

-   **Python:** Lógica del backend.
-   **Streamlit:** Interfaz de usuario interactiva.
-   **Pandas:** Procesamiento y limpieza de datos.
-   **Requests:** Comunicación con la API REST.
-   **python-dotenv:** Gestión de variables de entorno.

---
Desarrollado con ❤️ para **INMO S.A.**
