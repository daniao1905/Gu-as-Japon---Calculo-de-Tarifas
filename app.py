import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title="Guías Escalonadas por Fecha", layout="centered")
st.title("Reserva de Guías y Asistentes por Fecha")

# Tabla de referencia
st.markdown("### Tabla de Precios de Referencia")
st.markdown("""
**Guía Líder / Asistente**

| Tipo de Tour | Personas        | Precio Base      | Precio adicional               |
|--------------|-----------------|------------------|--------------------------------|
| Medio (1–3h) | 1–5 pax         | ¥34,500 / ¥32,500| +¥10,000 por persona (6–10)    |
|              |                 |                  | +¥5,000 por persona (11–30)    |
| Completo (4–8h) | 1–5 pax       | ¥69,000 / ¥65,000| +¥10,000 por persona (6–10)    |
|              |                 |                  | +¥5,000 por persona (11–30)    |
| Horas extra  | -               | +¥5,000 cada hora|                                |
""")

st.markdown("---")
st.markdown("### Selecciona tus fechas")

# Selección de fechas
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
        horas = st.number_input(f"Duración en horas para {fecha}", min_value=1, max_value=8, step=1, key=f"horas_{fecha}")
        horas_extra = st.number_input(f"Horas extra para {fecha}", min_value=0, max_value=10, step=1, key=f"extra_{fecha}")

        is_completo = horas >= 4
        duracion_tipo = "Completo" if is_completo else "Medio"
        subtotal_fecha = 0

        for guia in tipo:
            if guia == "Guía Líder":
                base = 69000 if is_completo else 34500
            else:
                base = 65000 if is_completo else 32500

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
**{fecha.strftime('%d/%m/%Y')} - {guia} ({duracion_tipo})**
- Personas: {personas}
- Horas: {horas} + {horas_extra} extra
- Total día: ¥{total:,}\n
"""

        total_general += subtotal_fecha

    st.markdown("---")
    st.markdown("## Resumen general:")
    st.markdown(resumen)
    st.markdown(f"### Total por todas las fechas: ¥{total_general:,}")
