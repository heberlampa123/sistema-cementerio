import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
from database import db
from models.contrato_model import Contrato

def generar_pdf_contrato(id_contrato):
    contrato = Contrato.query.get(id_contrato)
    if not contrato:
        return None

    usuario = contrato.usuario
    asignacion = contrato.asignacion
    difunto = asignacion.difunto
    espacio = asignacion.espacio

    # Preparar carpeta
    carpeta = os.path.join("static", "contratos")
    os.makedirs(carpeta, exist_ok=True)

    archivo_pdf = f"contrato_{id_contrato}.pdf"
    ruta_pdf = os.path.join(carpeta, archivo_pdf)

    # PDF
    ancho, alto = letter
    margen = 60
    y = alto - 60

    c = canvas.Canvas(ruta_pdf, pagesize=letter)
    c.setTitle(f"Contrato N° {id_contrato}")

    def wrap_text(text, max_width, fontsize=11):
        words = text.split()
        lines = []
        current = ""
        for w in words:
            test = current + " " + w if current else w
            if c.stringWidth(test, "Helvetica", fontsize) <= max_width:
                current = test
            else:
                lines.append(current)
                current = w
        if current:
            lines.append(current)
        return lines

    # Titulo
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(ancho/2, y, "CONTRATO DE ASIGNACIÓN DE ESPACIO")
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(ancho/2, y, f"N° {id_contrato}")
    y -= 20

    c.line(margen, y, ancho-margen, y)
    y -= 25

    # --- DATOS DEL DIFUNTO ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margen, y, "DATOS DEL DIFUNTO:")
    y -= 18
    c.setFont("Helvetica", 11)

    c.drawString(margen, y, f"Nombre completo: {difunto.nombre} {difunto.paterno} {difunto.materno}")
    y -= 14
    c.drawString(margen, y, f"Fecha de fallecimiento: {difunto.fecha_dif or '—'}")
    y -= 22

    # --- DATOS DEL ESPACIO ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margen, y, "DATOS DEL ESPACIO:")
    y -= 18
    c.setFont("Helvetica", 11)

    c.drawString(margen, y, f"Tipo: {espacio.tipo}")
    y -= 14
    c.drawString(margen, y, f"Ubicación: {espacio.ubicacion}")
    y -= 14
    c.drawString(margen, y, f"Estado: {espacio.estado}")
    y -= 22

    # --- RESPONSABLE ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margen, y, "RESPONSABLE:")
    y -= 18
    c.setFont("Helvetica", 11)

    c.drawString(margen, y, f"Responsable: {asignacion.responsable}")
    y -= 14
    c.drawString(margen, y, f"CI: {asignacion.ci_responsable}")
    y -= 14
    c.drawString(margen, y, f"Teléfono: {asignacion.telef_responsable}")
    y -= 22

    # --- REGISTRO ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margen, y, "REGISTRO:")
    y -= 18
    c.setFont("Helvetica", 11)

    c.drawString(margen, y, f"Fecha del contrato: {contrato.fecha}")
    y -= 14
    c.drawString(margen, y, f"Precio: Bs. {asignacion.precio}")
    y -= 14
    c.drawString(margen, y, f"Registrado por: {usuario.nombre} ({usuario.rol})")
    y -= 22

    # --- CONDICIONES ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margen, y, "CONDICIONES:")
    y -= 18
    c.setFont("Helvetica", 11)

    condiciones_lines = wrap_text(
        contrato.condiciones, 
        max_width = ancho - 2*margen,
        fontsize = 11
    )

    for line in condiciones_lines:
        c.drawString(margen, y, line)
        y -= 14

    y -= 30

    # FIRMAS
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margen, y, "_____________________________")
    c.drawString(margen, y - 15, "Responsable")

    c.drawString(ancho - margen - 200, y, "_____________________________")
    c.drawString(ancho - margen - 200, y - 15, "Funcionario")

    c.showPage()
    c.save()

    return f"contratos/{archivo_pdf}"
