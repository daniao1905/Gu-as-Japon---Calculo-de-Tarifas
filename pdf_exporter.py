import tempfile
from fpdf import FPDF

def exportar_a_pdf(cliente, detalles_por_fecha, total_general):
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", 'B', 14)
            self.cell(0, 10, "Presupuesto de Servicios", ln=True, align="C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Cliente: {cliente}", ln=True)
    pdf.ln(5)

    for detalle in detalles_por_fecha:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f"{detalle['fecha']} - {detalle['tipo']}", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.cell(0, 8, f"{detalle['descripcion']}", ln=True)
        pdf.cell(0, 8, f"Personas: {detalle['personas']}", ln=True)
        pdf.cell(0, 8, f"Tarifa: ¥{detalle['tarifa']:,}", ln=True)
        if detalle.get("extras"):
            pdf.cell(0, 8, f"Extras: ¥{detalle['extras']:,}", ln=True)
        pdf.set_text_color(255, 0, 0)
        pdf.cell(0, 8, f"Total Día: ¥{detalle['total_dia']:,}", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)

    pdf.set_font("Arial", 'B', 13)
    pdf.cell(0, 10, f"Total General: ¥{total_general:,}", ln=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        with open(tmp.name, "rb") as f:
            st.download_button("Descargar PDF", f.read(), file_name=f"Presupuesto_{cliente}.pdf")
