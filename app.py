import streamlit as st
from pdf_exporter import exportar_a_pdf

st.set_page_config(page_title="Guías Japón - Tarifas", layout="centered")
st.title("Guías Japón - Cálculo de Tarifas")

cliente = st.text_input("Nombre del cliente", "Nombre del cliente")

fechas = st.date_input("Selecciona fechas de servicio", [], min_value=None)

resultados = []
total_general = 0

if fechas:
    for fecha in fechas:
        st.markdown(f"---\n### {fecha.strftime('%d/%m/%Y')}")
        horas = st.slider(f"Duración del servicio (horas) - {fecha}", 1, 8, 4, key=f"horas_{fecha}")
        guia_asistente = st.checkbox(f"Requiere Guía Asistente ({fecha})", key=f"asistente_{fecha}")
        guia_lider = st.checkbox(f"Requiere Guía Líder ({fecha})", key=f"lider_{fecha}")
        personas = st.number_input(f"Número de personas - {fecha}", 1, 30, key=f"personas_{fecha}")

        total_dia = 0
        descripcion = []

        if guia_asistente:
            if horas >= 4:
                tarifa = 65000
                descripcion.append("Guía Asistente (4–8 hrs)")
            else:
                tarifa = 32500
                descripcion.append("Guía Asistente (1–3 hrs)")
            total_dia += tarifa
            resultados.append({
                "fecha": fecha.strftime("%d/%m/%Y"),
                "tipo": "Guía Asistente",
                "descripcion": ", ".join(descripcion),
                "personas": personas,
                "tarifa": tarifa,
                "total_dia": tarifa
            })

        if guia_lider:
            if horas >= 4:
                base = 69000
                if personas <= 5:
                    tarifa = base
                elif 6 <= personas <= 10:
                    tarifa = base + (personas - 5) * 10000
                else:
                    tarifa = base + 5 * 10000 + (personas - 10) * 5000
                descripcion.append("Guía Líder (4–8 hrs)")
            else:
                base = 34500
                if personas <= 5:
                    tarifa = base
                elif 6 <= personas <= 10:
                    tarifa = base + (personas - 5) * 5000
                else:
                    tarifa = base + 5 * 5000 + (personas - 10) * 2500
                descripcion.append("Guía Líder (1–3 hrs)")

            total_dia += tarifa
            resultados.append({
                "fecha": fecha.strftime("%d/%m/%Y"),
                "tipo": "Guía Líder",
                "descripcion": ", ".join(descripcion),
                "personas": personas,
                "tarifa": tarifa,
                "total_dia": tarifa
            })

        total_general += total_dia

    st.markdown(f"### Total General: ¥{total_general:,}")

    if st.button("Generar PDF del Presupuesto"):
        exportar_a_pdf(cliente, resultados, total_general)
