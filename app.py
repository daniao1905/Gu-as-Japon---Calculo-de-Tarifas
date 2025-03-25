import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title="Guías por Fecha", layout="centered")
st.title("Reserva de Guías y Asistentes por Fecha")

# Selección de rango de fechas
st.markdown("Selecciona un rango de fechas para el servicio:")
fecha_inicio = st.date_input("Desde", date.today())
fecha_fin = st.date_input("Hasta", date.today() + timedelta(days=1))

if fecha_inicio > fecha_fin:
    st.error("La fecha final debe ser posterior a la fecha inicial.")
else:
    fechas = [fecha_inicio + timedelta(days=i) for i in range((fecha_fin - fecha_inicio).days + 1)]
    total_general = 0
    resumen = ""

    for fecha in fechas:
        st.markdown(f"---\n### {fecha.strftime('%A, %d %B %Y')}")

        tipo = st.multiselect(f"Tipo de guía para {fecha}", ["Guía Líder", "Asistente"], key=f"tipo_{fecha}")
        personas = st.number_input(f"Número de personas para {fecha}", min_value=1, max_value=30, step=1, key=f"personas_{fecha}")
        horas = st.number_input(f"Duración (horas) para {fecha}", min_value=1, max_value=10, step=1, key=f"horas_{fecha}")
        horas_extra = st.number_input(f"Horas extra para {fecha}", min_value=0, max_value=10, step=1, key=f"extra_{fecha}")

        subtotal_fecha = 0

        for guia in tipo:
            base = 0
            extra = horas_extra * 5000

            if guia == "Guía Líder":
                if horas <= 4:
                    if personas <= 5:
                        base = 34500
                    elif personas <= 10:
                        base = 5000 * personas
                    else:
                        base = 2500 * personas
                else:  # 4–8 hrs
                    if personas <= 5:
                        base = 69000
                    elif personas <= 10:
                        base = 10000 * personas
                    else:
                        base = 5000 * personas
            elif guia == "Asistente":
                if horas <= 4:
                    base = 32500
                else:
                    base = 65000

            total = base + extra
            subtotal_fecha += total

            resumen += f"""
**{fecha.strftime('%d/%m/%Y')} - {guia}**
- Personas: {personas}
- Horas: {horas} + {horas_extra} extra
- Base: ¥{base:,}
- Extra: ¥{extra:,}
- Subtotal: ¥{total:,}\n
"""

        total_general += subtotal_fecha

    st.markdown("---")
    st.markdown("## Resumen general:")
    st.markdown(resumen)
    st.markdown(f"### Total por todas las fechas: ¥{total_general:,}")
