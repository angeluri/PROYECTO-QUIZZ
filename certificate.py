"""
Módulo para generar certificados PDF profesionales (módulo y maestro).
Soporta reemplazo si mejora calificación.
"""
import os
from datetime import datetime
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

import database as db
import utils

# ============================================================
# CONFIGURACIÓN DE RECURSOS (ajusta las rutas según tu proyecto)
# ============================================================
LOGO_PATH = "assets/logo.png"           # Logo institucional (opcional)
FONDO_PATH = "assets/background.png"    # Fondo de agua (opcional)

# Colores institucionales
COLOR_AZUL = HexColor("#0B3C73")        # Azul oscuro
COLOR_DORADO = HexColor("#C8A75D")      # Dorado
COLOR_GRIS = HexColor("#666666")        # Gris para textos secundarios

# ============================================================
# FUNCIONES DE DIBUJO (extraídas del ejemplo)
# ============================================================
def dibujar_marco(pdf, width, height):
    """Marco decorativo premium (dorado exterior, azul interior)."""
    # Marco exterior dorado
    pdf.setStrokeColor(COLOR_DORADO)
    pdf.setLineWidth(6)
    pdf.rect(1.2 * cm, 1.2 * cm, width - 2.4 * cm, height - 2.4 * cm)
    # Marco interior azul
    pdf.setStrokeColor(COLOR_AZUL)
    pdf.setLineWidth(2)
    pdf.rect(1.6 * cm, 1.6 * cm, width - 3.2 * cm, height - 3.2 * cm)

def dibujar_fondo(pdf, width, height):
    """Fondo sutil (marca de agua)."""
    if os.path.exists(FONDO_PATH):
        try:
            pdf.drawImage(FONDO_PATH, 0, 0, width=width, height=height, preserveAspectRatio=False, mask='auto')
        except:
            pass

def dibujar_sello(pdf, width, height):
    """Logo como sello y marca de agua."""
    if not os.path.exists(LOGO_PATH):
        return
    try:
        # Marca de agua central (opaca)
        pdf.saveState()
        pdf.setFillAlpha(0.08)
        size = 8 * cm
        x = (width / 2) - (size / 2)
        y = (height / 2) - (size / 2)
        pdf.drawImage(LOGO_PATH, x, y, width=size, height=size, mask='auto')
        pdf.restoreState()
        # Sello en esquina inferior derecha
        pdf.drawImage(LOGO_PATH, width - 5 * cm, 2 * cm, width=2.5 * cm, height=2.5 * cm, mask='auto')
    except:
        pass

def dibujar_encabezado(pdf, width, titulo):
    """Encabezado institucional."""
    pdf.setFillColor(COLOR_AZUL)
    pdf.setFont("Helvetica-Bold", 28)
    pdf.drawCentredString(width / 2, 18 * cm, titulo)
    pdf.setFillColor(COLOR_GRIS)
    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(width / 2, 17 * cm, "Plataforma Académica de Refuerzo Educativo")

def dibujar_firma(pdf, width):
    """Firma decorativa."""
    x = width / 2
    pdf.setStrokeColor(black)
    pdf.line(x - 3 * cm, 3.5 * cm, x + 3 * cm, 3.5 * cm)
    pdf.setFont("Helvetica", 11)
    pdf.drawCentredString(x, 3 * cm, "Dirección Académica")
    pdf.drawCentredString(x, 2.4 * cm, "Cursos de Regularización CECyTEM")

# ============================================================
# FUNCIONES PRINCIPALES (interfaz compatible con el proyecto)
# ============================================================
def generate_module_certificate(user_id, user_name, course_name, module_name, score, total, percentage):
    """Genera o actualiza certificado de módulo. Reemplaza si mejora nota."""
    existing = db.get_certificate_by_module(user_id, course_name, module_name)
    if existing and existing[2] >= percentage:
        return False

    folio = utils.generate_folio(prefix="MOD")
    hash_ver = utils.generate_hash(f"{user_id}{course_name}{module_name}{utils.format_date()}{folio}")
    pdf_filename = f"cert_{folio}.pdf"
    pdf_path = os.path.join("certificados", pdf_filename)

    # Eliminar archivo antiguo si existe
    if existing and existing[5]:
        old_path = existing[5]
        if os.path.exists(old_path):
            os.remove(old_path)

    # Generar PDF con el nuevo estilo
    create_certificate_pdf(pdf_path, user_name, course_name, module_name, score, total, percentage, folio, hash_ver, is_master=False)

    if existing:
        db.update_certificate(existing[0], score, total, percentage, folio, hash_ver, pdf_path)
    else:
        db.save_certificate(user_id, course_name, module_name, score, total, percentage, folio, hash_ver, pdf_path)
    return True

def generate_master_certificate(user_id, user_name, course_name):
    """Genera certificado maestro de curso completo si no existe."""
    existing = db.get_master_certificate(user_id, course_name)
    if existing:
        return False

    folio = utils.generate_folio(prefix="MASTER")
    hash_ver = utils.generate_hash(f"{user_id}{course_name}master{utils.format_date()}")
    pdf_filename = f"master_{folio}.pdf"
    pdf_path = os.path.join("certificados", pdf_filename)

    create_certificate_pdf(pdf_path, user_name, course_name, "", 100, 100, 100, folio, hash_ver, is_master=True)
    db.save_master_certificate(user_id, course_name, folio, hash_ver, pdf_path)
    return True

def create_certificate_pdf(filepath, student_name, course_name, module_name, score, total, percentage, folio, hash_ver, is_master=False):
    """Construye el PDF con diseño profesional (estilo CECyTEM)."""
    width, height = landscape(A4)
    pdf = canvas.Canvas(filepath, pagesize=landscape(A4))

    # Fondo (marca de agua)
    dibujar_fondo(pdf, width, height)
    # Marco decorativo
    dibujar_marco(pdf, width, height)
    # Sello y logo
    dibujar_sello(pdf, width, height)
    # Encabezado institucional
    dibujar_encabezado(pdf, width, "Cursos de Regularización CECyTEM")

    # Título principal
    pdf.setFillColor(COLOR_DORADO)
    pdf.setFont("Helvetica-Bold", 30)
    if is_master:
        pdf.drawCentredString(width / 2, 14.4 * cm, "CERTIFICADO MAESTRO")
    else:
        pdf.drawCentredString(width / 2, 14.4 * cm, "CERTIFICADO DE ACREDITACIÓN")

    # Texto de reconocimiento
    pdf.setFillColor(black)
    pdf.setFont("Helvetica", 18)
    pdf.drawCentredString(width / 2, 12.5 * cm, "Se otorga a:")

    # Nombre del alumno
    pdf.setFont("Helvetica-Bold", 28)
    pdf.drawCentredString(width / 2, 11 * cm, student_name)

    # Descripción
    pdf.setFont("Helvetica", 16)
    if is_master:
        pdf.drawCentredString(width / 2, 9.5 * cm, "Por completar satisfactoriamente el curso completo:")
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawCentredString(width / 2, 8.2 * cm, course_name)
        pdf.setFillColor(COLOR_AZUL)
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawCentredString(width / 2, 6.8 * cm, f"Promedio final: {score}/{total} ({percentage:.0f}%)")
    else:
        pdf.drawCentredString(width / 2, 9.5 * cm, "Por acreditar satisfactoriamente el módulo académico:")
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawCentredString(width / 2, 8.5 * cm, f"Curso: {course_name}")
        pdf.drawCentredString(width / 2, 7.6 * cm, f"Módulo: {module_name}")
        pdf.setFillColor(COLOR_AZUL)
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawCentredString(width / 2, 6.3 * cm, f"Calificación: {score}/{total} ({percentage:.0f}%)")

    # Fecha
    pdf.setFillColor(COLOR_GRIS)
    pdf.setFont("Helvetica", 12)
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    pdf.drawCentredString(width / 2, 5.2 * cm, f"Fecha de emisión: {fecha_actual}")

    # Folio y hash (esquina inferior izquierda)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(2 * cm, 2 * cm, f"Folio: {folio}")
    pdf.setFont("Helvetica", 8)
    pdf.drawString(2 * cm, 1.5 * cm, f"Hash: {hash_ver[:40]}...")

    # Firma institucional
    dibujar_firma(pdf, width)

    pdf.save()
    return filepath

def check_and_generate_master(user_id, user_name, course_name):
    """Evalúa si el usuario aprobó todos los módulos del curso y genera el certificado maestro."""
    from questions import COURSES
    modules = COURSES.get(course_name, {})
    all_passed = True
    for mod_name in modules:
        prog = db.get_progress(user_id, course_name, mod_name)
        if not prog or not prog[6]:
            all_passed = False
            break
    if all_passed:
        generate_master_certificate(user_id, user_name, course_name)