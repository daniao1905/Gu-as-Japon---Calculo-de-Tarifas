import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title="Guías por Fecha", layout="centered")
st.title("Reserva de Guías y Asistentes por Fecha")

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

        guia_lider = st.checkbox(f"¿Requiere Guía Líder para {fecha}?", key=f"lider_{fecha}")
        asistente = st.checkbox(f"¿Requiere Asistente para {fecha}?", key=f"asis_{fecha}")
        personas = st.number_input(f"Número de personas para {fecha}", min_value=1, max_value=30, step=1, key=f"personas_{fecha}")
        horas = st.number_input(f"Duración (horas) para {fecha}", min_value=1, max_value=8, step=1, key=f"horas_{fecha}")
        horas_extra = st.number_input(f"Horas extra para {fecha}", min_value=0, max_value=10, step=1, key=f"extra_{fecha}")

        is_completo = horas >= 4
        duracion_tipo = "Completo" if is_completo else "Medio"
        subtotal_fecha = 0

        for tipo, activo in [("Guía Líder", guia_lider), ("Asistente", asistente)]:
            if not activo:
                continue

            base = 69000 if (tipo == "Guía Líder" and is_completo) else 34500 if tipo == "Guía Líder" else 65000 if is_completo else 32500

            # Precio adicional por personas
            if personas > 5:
                extras = 0
                if personas <= 10:
                    extras = (personas - 5) * 10000
                else:
                    extras = 5 * 10000 + (personas - 10) * 5000
                base += extras

            extra_fee = horas_extra * 5000
            total = base + extra_fee
            subtotal_fecha += total

            resumen += f"""
**{fecha.strftime('%d/%m/%Y')} - {tipo} ({duracion_tipo})**
- Personas: {personas}
- Horas: {horas} + {horas_extra} extra
- Total día: ¥{total:,}\n
"""

        total_general += subtotal_fecha

    st.markdown("---")
    st.markdown("## Resumen general:")
    st.markdown(resumen)
    st.markdown(f"### Total por todas las fechas: ¥{total_general:,}")
