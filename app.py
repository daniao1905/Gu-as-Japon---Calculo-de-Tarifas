import streamlit as st
from pdf_exporter import exportar_a_pdf

st.title("Simulación PDF - Guías Japón")

cliente = st.text_input("Nombre del cliente", "Ejemplo Cliente")

if st.button("Simular PDF"):
    detalles = [
        {
            "fecha": "01/04/2025",
            "tipo": "Guía Líder",
            "descripcion": "Tour completo en Kyoto",
            "personas": 7,
            "tarifa": 119000,
            "extras": 10000,
            "total_dia": 129000
        },
        {
            "fecha": "02/04/2025",
            "tipo": "Guía Asistente",
            "descripcion": "Medio tour en Tokyo",
            "personas": 4,
            "tarifa": 32500,
            "total_dia": 32500
        }
    ]
    total_general = sum(item["total_dia"] for item in detalles)
    exportar_a_pdf(cliente, detalles, total_general)
