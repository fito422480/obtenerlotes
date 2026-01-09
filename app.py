# -*- coding: utf-8 -*-

import streamlit as st
import requests
import pandas as pd

API_URL = "https://shift.century.com.py/inmo/next/lotes/lotes"
API_KEY = "F5D8A1298A8642CFE053820001C704DD"


@st.cache_data(show_spinner=False)
def fetch_lotes():
    headers = {
        "ApiKey": API_KEY,
        "Accept": "application/json"
    }

    response = requests.get(API_URL, headers=headers, timeout=30)
    response.raise_for_status()

    data = response.json()

    if "value" not in data:
        raise ValueError("La respuesta no contiene la clave 'value'")

    # DataFrame con TODOS los campos
    return pd.DataFrame(data["value"])


def main():
    st.set_page_config(
        page_title="Consulta de Lotes",
        layout="wide"
    )

    st.title("🏗️ Exportador de Lotes – Todos los Campos")
    st.caption("La estructura del CSV es idéntica a la API")

    if st.button("Cargar datos"):
        try:
            with st.spinner("Consultando API..."):
                df = fetch_lotes()

            st.success(f"Datos cargados correctamente ({len(df)} registros)")

            # Mostrar columnas detectadas
            st.subheader("Campos incluidos")
            st.write(df.columns.tolist())

            # Tabla completa
            st.subheader("Datos")
            st.dataframe(df, use_container_width=True)

            # Descargar CSV
            csv = df.to_csv(
                index=False,
                sep=";",
                encoding="utf-8-sig"
            )

            st.download_button(
                label="⬇Descargar CSV completo",
                data=csv,
                file_name="lotes_completo.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"Error: {e}")


if __name__ == "__main__":
    main()
