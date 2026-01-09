# 🏗️ INMO - Exportador de Lotes

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
    pip install -r requeriments.txt
    ```

## 🛠️ Uso

Para iniciar la aplicación, ejecuta el siguiente comando en tu terminal:

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador predeterminado (usualmente en `http://localhost:8501`).

## ⚙️ Configuración

Actualmente, la aplicación utiliza una `API_KEY` configurada internamente para acceder a:
`https://shift.century.com.py/inmo/next/lotes/lotes`

## 👨‍💻 Tecnologías

-   **Python:** Lógica del backend.
-   **Streamlit:** Interfaz de usuario interactiva.
-   **Pandas:** Procesamiento y limpieza de datos.
-   **Requests:** Comunicación con la API REST.

---
Desarrollado con ❤️ para **INMO S.A.**
