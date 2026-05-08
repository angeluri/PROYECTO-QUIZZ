from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
import sqlite3
import hashlib
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import random
import string
from email.header import Header

# ==========================================================
# PALETA PREMIUM (Teal & Gold)
# ==========================================================
PRIMARY = (0.10, 0.37, 0.48, 1)
PRIMARY_DARK = (0.05, 0.23, 0.31, 1)
ACCENT = (0.98, 0.70, 0.14, 1)
BG = (0.96, 0.98, 0.98, 1)
CARD = (1, 1, 1, 1)
TEXT = (0.12, 0.16, 0.20, 1)
GRAY = (0.55, 0.60, 0.65, 1)
SUCCESS = (0.22, 0.72, 0.34, 1)
ERROR = (0.90, 0.25, 0.25, 1)

RADIUS = [24]
ELEVATION = 6

# ==========================================================
# CONFIGURACIÓN DE CORREO (opcional)
# ==========================================================
EMAIL_USER = "tu_correo@gmail.com"        # Cambia por tu email real
EMAIL_PASSWORD = "tu_contraseña_o_app_password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(destinatario, asunto, cuerpo):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = destinatario
        msg['Subject'] = Header(asunto, 'utf-8')
        msg.attach(MIMEText(cuerpo, 'plain', 'utf-8'))
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False

# ==========================================================
# BASE DE DATOS MEJORADA
# ==========================================================
class Database:
    def __init__(self):
        # Si existe base antigua sin campo 'ultimo_intento', la eliminamos (opcional)
        if os.path.exists('habitos_saludables.db'):
            try:
                conn_old = sqlite3.connect('habitos_saludables.db')
                cursor_old = conn_old.cursor()
                cursor_old.execute("PRAGMA table_info(progreso)")
                columns = [col[1] for col in cursor_old.fetchall()]
                conn_old.close()
                if 'ultimo_intento' not in columns:
                    os.remove('habitos_saludables.db')
                    print("Base de datos antigua eliminada. Creando nueva estructura...")
            except:
                pass
        
        self.conn = sqlite3.connect('habitos_saludables.db')
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                fecha_registro TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS progreso (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                curso TEXT NOT NULL,
                modulo TEXT NOT NULL,
                puntaje INTEGER NOT NULL,
                total_preguntas INTEGER NOT NULL,
                completado INTEGER DEFAULT 0,
                fecha_completado TEXT,
                certificado_emitido INTEGER DEFAULT 0,
                ultimo_intento TEXT,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
                UNIQUE(usuario_id, curso, modulo)
            )
        ''')
        self.conn.commit()
    
    def registrar_usuario(self, nombre, email, password):
        cursor = self.conn.cursor()
        try:
            hashed = hashlib.sha256(password.encode()).hexdigest()
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO usuarios (nombre, email, password, fecha_registro) VALUES (?, ?, ?, ?)",
                (nombre, email, hashed, fecha)
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    def login_usuario(self, email, password):
        cursor = self.conn.cursor()
        hashed = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute(
            "SELECT id, nombre FROM usuarios WHERE email = ? AND password = ?",
            (email, hashed)
        )
        return cursor.fetchone()
    
    def existe_email(self, email):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
        return cursor.fetchone() is not None
    
    def guardar_progreso_modulo(self, usuario_id, curso, modulo, puntaje, total_preguntas):
        cursor = self.conn.cursor()
        completado = 1 if puntaje >= total_preguntas * 0.7 else 0
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if completado else None
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT OR REPLACE INTO progreso 
            (usuario_id, curso, modulo, puntaje, total_preguntas, completado, fecha_completado, certificado_emitido, ultimo_intento)
            VALUES (?, ?, ?, ?, ?, ?, ?, COALESCE((SELECT certificado_emitido FROM progreso WHERE usuario_id = ? AND curso = ? AND modulo = ?), 0), ?)
        ''', (usuario_id, curso, modulo, puntaje, total_preguntas, completado, fecha, usuario_id, curso, modulo, ahora))
        self.conn.commit()
        return completado
    
    def reiniciar_modulo(self, usuario_id, curso, modulo):
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM progreso WHERE usuario_id = ? AND curso = ? AND modulo = ?",
            (usuario_id, curso, modulo)
        )
        self.conn.commit()
    
    def obtener_progreso_curso(self, usuario_id, curso):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT modulo, puntaje, total_preguntas, completado, certificado_emitido FROM progreso WHERE usuario_id = ? AND curso = ?",
            (usuario_id, curso)
        )
        return cursor.fetchall()
    
    def obtener_progreso_modulo(self, usuario_id, curso, modulo):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT puntaje, total_preguntas, completado, certificado_emitido, ultimo_intento FROM progreso WHERE usuario_id = ? AND curso = ? AND modulo = ?",
            (usuario_id, curso, modulo)
        )
        return cursor.fetchone()
    
    def obtener_certificados_usuario(self, usuario_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT DISTINCT curso, modulo FROM progreso WHERE usuario_id = ? AND completado = 1 AND certificado_emitido = 1",
            (usuario_id,)
        )
        return cursor.fetchall()
    
    def marcar_certificado_emitido(self, usuario_id, curso, modulo):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE progreso SET certificado_emitido = 1 WHERE usuario_id = ? AND curso = ? AND modulo = ?",
            (usuario_id, curso, modulo)
        )
        self.conn.commit()
    
    def obtener_datos_usuario(self, usuario_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT nombre, email FROM usuarios WHERE id = ?", (usuario_id,))
        return cursor.fetchone()
    
    def close(self):
        self.conn.close()

db = Database()

# ==========================================================
# FUNCIONES PARA GENERAR PDF DEL CERTIFICADO
# ==========================================================
def generar_pdf_certificado(nombre_usuario, curso, modulo, puntaje, total, fecha_str):
    os.makedirs("certificados", exist_ok=True)
    codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    nombre_limpio = nombre_usuario.replace(" ", "_").replace("ñ", "n").replace("Ñ", "N")
    curso_limpio = curso.replace(" ", "_").replace(":", "").replace("ñ", "n")[:20]
    filename = f"certificados/certificado_{nombre_limpio}_{curso_limpio}_{codigo}.pdf"

    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        c.setFont('Helvetica', 12)
        c.setStrokeColorRGB(*ACCENT[:3])
        c.setLineWidth(4)
        c.rect(30, 30, width-60, height-60)
        c.setFont("Helvetica-Bold", 28)
        c.setFillColorRGB(*PRIMARY[:3])
        c.drawCentredString(width/2, height-100, "CERTIFICADO DE APROBACIÓN")
        c.setFillColorRGB(*ACCENT[:3])
        c.rect(width/2 - 100, height-120, 200, 3, fill=1, stroke=0)
        c.setFont("Helvetica", 16)
        c.setFillColorRGB(*TEXT[:3])
        c.drawCentredString(width/2, height-170, "Se otorga el presente certificado a:")
        c.setFont("Helvetica-Bold", 24)
        c.setFillColorRGB(*PRIMARY[:3])
        c.drawCentredString(width/2, height-220, nombre_usuario)
        c.setFont("Helvetica", 16)
        c.setFillColorRGB(*TEXT[:3])
        c.drawCentredString(width/2, height-270, f"Por haber completado el módulo:")
        c.setFont("Helvetica-Bold", 18)
        c.setFillColorRGB(*ACCENT[:3])
        c.drawCentredString(width/2, height-310, modulo[:40])
        c.setFont("Helvetica", 14)
        c.setFillColorRGB(*TEXT[:3])
        c.drawCentredString(width/2, height-350, f"del curso: {curso[:40]}")
        c.setFont("Helvetica", 14)
        c.drawCentredString(width/2, height-390, f"Obteniendo un puntaje de {puntaje}/{total} puntos")
        c.setFont("Helvetica-Oblique", 12)
        c.drawCentredString(width/2, height-430, f"Fecha de emisión: {fecha_str}")
        c.setFont("Helvetica", 10)
        c.setFillColorRGB(*GRAY[:3])
        c.drawCentredString(width/2, height-470, f"Código de verificación: {codigo}")
        c.setStrokeColorRGB(*ACCENT[:3])
        c.setFillColorRGB(1, 1, 1, 0)
        c.circle(width-80, 80, 40, fill=0, stroke=1)
        c.setFont("Helvetica", 8)
        c.setFillColorRGB(*PRIMARY[:3])
        c.drawCentredString(width-80, 80, "VÁLIDO")
        c.save()
        return filename
    except Exception as e:
        print(f"Error generando PDF: {e}")
        return None

# ==========================================================
# GENERAR PREGUNTAS PARA CADA MÓDULO (10 por módulo)
# ==========================================================

# ---- Curso Estrés (ya existía) ----
def generar_preguntas_estres_modulo1():
    return [
        {"pregunta": "¿Qué es un detonante de estrés?", "opciones": ["Una persona que causa estrés", "Un evento o situación que desencadena estrés", "Un medicamento", "Un tipo de respiración"], "correcta": 1, "explicacion": "Un detonante activa la respuesta de estrés."},
        {"pregunta": "¿Cuál es el primer paso para manejar el estrés?", "opciones": ["Ignorar síntomas", "Identificar la causa", "Tomar medicamentos", "Dormir más"], "correcta": 1, "explicacion": "Identificar la causa es fundamental."},
        {"pregunta": "¿Qué hormona se libera durante el estrés?", "opciones": ["Serotonina", "Cortisol", "Melatonina", "Dopamina"], "correcta": 1, "explicacion": "El cortisol es la hormona del estrés."},
        {"pregunta": "¿El estrés crónico puede afectar el sistema inmune?", "opciones": ["Sí", "No", "Solo en niños", "Solo en ancianos"], "correcta": 0, "explicacion": "El estrés crónico debilita el sistema inmune."},
        {"pregunta": "¿Qué es la ansiedad?", "opciones": ["Miedo irracional", "Preocupación excesiva por el futuro", "Tristeza profunda", "Felicidad intensa"], "correcta": 1, "explicacion": "La ansiedad es preocupación anticipatoria."},
        {"pregunta": "¿Cuál NO es un síntoma de estrés?", "opciones": ["Dolor de cabeza", "Insomnio", "Euforia extrema", "Tensión muscular"], "correcta": 2, "explicacion": "La euforia no es típica del estrés."},
        {"pregunta": "¿Qué técnica ayuda a identificar detonantes?", "opciones": ["Diario de estrés", "Meditación", "Ejercicio", "Dormir"], "correcta": 0, "explicacion": "Llevar un diario ayuda a identificar patrones."},
        {"pregunta": "¿El perfeccionismo puede aumentar el estrés?", "opciones": ["Sí", "No", "Solo en el trabajo", "Solo en casa"], "correcta": 0, "explicacion": "El perfeccionismo genera presión adicional."},
        {"pregunta": "¿Qué porcentaje de enfermedades está relacionado con el estrés?", "opciones": ["10%", "30%", "50-80%", "95%"], "correcta": 2, "explicacion": "La mayoría de enfermedades tienen componente de estrés."},
        {"pregunta": "¿Cuál es una señal temprana de estrés?", "opciones": ["Irritabilidad", "Sueño profundo", "Apetito excesivo", "Fiebre"], "correcta": 0, "explicacion": "La irritabilidad es una señal común."},
    ]

def generar_preguntas_estres_modulo2():
    return [
        {"pregunta": "¿Cuál es la técnica de respiración 4-7-8?", "opciones": ["Inhalar 4s, sostener 7s, exhalar 8s", "Inhalar 8s, sostener 4s, exhalar 7s", "Respiración rápida", "Contar hasta 100"], "correcta": 0, "explicacion": "La técnica 4-7-8 calma el sistema nervioso."},
        {"pregunta": "¿Qué porcentaje de oxígeno ingresa con respiración diafragmática?", "opciones": ["50%", "70%", "90%", "30%"], "correcta": 2, "explicacion": "La respiración profunda oxigena mejor."},
        {"pregunta": "¿Cuántos minutos de respiración profunda reducen la ansiedad?", "opciones": ["1 minuto", "3-5 minutos", "30 minutos", "1 hora"], "correcta": 1, "explicacion": "Pocos minutos son suficientes para calmarse."},
        {"pregunta": "¿Qué sistema nervioso activa la respiración profunda?", "opciones": ["Simpático", "Parasimpático", "Central", "Periférico"], "correcta": 1, "explicacion": "Activa el sistema de relajación."},
        {"pregunta": "¿Qué es la relajación muscular progresiva?", "opciones": ["Tensar y relajar músculos", "Meditar", "Respirar", "Hacer yoga"], "correcta": 0, "explicacion": "Tensar y relajar reduce la tensión muscular."},
        {"pregunta": "¿Cuál es la mejor posición para respirar profundamente?", "opciones": ["Acostado boca arriba", "Sentado", "Parado", "Todas son válidas"], "correcta": 3, "explicacion": "Funciona en cualquier posición cómoda."},
        {"pregunta": "¿La meditación mindfulness reduce el estrés?", "opciones": ["Sí", "No", "Solo para expertos", "Solo 1 hora"], "correcta": 0, "explicacion": "Mindfulness es efectivo contra el estrés."},
        {"pregunta": "¿Con qué frecuencia practicar respiración para resultados?", "opciones": ["Una vez al mes", "1-2 veces al día", "10 veces al día", "Semanal"], "correcta": 1, "explicacion": "La práctica diaria es más efectiva."},
        {"pregunta": "¿Qué efecto tiene la respiración lenta en el corazón?", "opciones": ["Aumenta ritmo", "Disminuye ritmo", "No afecta", "Irregular"], "correcta": 1, "explicacion": "Disminuye la frecuencia cardíaca."},
        {"pregunta": "¿Qué aplicación puede ayudar con la respiración?", "opciones": ["Headspace", "Facebook", "Instagram", "Twitter"], "correcta": 0, "explicacion": "Headspace tiene ejercicios de respiración."},
    ]

def generar_preguntas_estres_modulo3():
    return [
        {"pregunta": "¿Qué es la técnica Pomodoro?", "opciones": ["25 min trabajo/5 descanso", "50/10", "1 hora trabajo", "Sin descanso"], "correcta": 0, "explicacion": "Pomodoro mejora la productividad."},
        {"pregunta": "¿Cuántas horas de sueño necesita un adulto?", "opciones": ["4-5", "7-9", "10-12", "2-3"], "correcta": 1, "explicacion": "7-9 horas son ideales."},
        {"pregunta": "¿Qué es la matriz de Eisenhower?", "opciones": ["Clasifica tareas por urgencia", "Lista de compras", "Calendario", "Cronómetro"], "correcta": 0, "explicacion": "Ayuda a priorizar tareas."},
        {"pregunta": "¿Cuál es el mejor momento para planificar el día?", "opciones": ["Por la mañana", "La noche anterior", "Al mediodía", "Cuando surja"], "correcta": 1, "explicacion": "Planificar la noche anterior reduce la ansiedad matutina."},
        {"pregunta": "¿Qué porcentaje del tiempo se pierde en multitarea?", "opciones": ["10%", "20-40%", "50%", "70%"], "correcta": 1, "explicacion": "La multitarea reduce la eficiencia."},
        {"pregunta": "¿Cuántas tareas debe tener una lista diaria?", "opciones": ["1-3", "5-7", "10-15", "20+"], "correcta": 0, "explicacion": "Pocas tareas son más manejables."},
        {"pregunta": "¿Qué técnica ayuda contra la procrastinación?", "opciones": ["Regla de 5 minutos", "Esperar motivación", "Hacer todo junto", "Ignorar"], "correcta": 0, "explicacion": "Comenzar con 5 minutos ayuda a vencer la inercia."},
        {"pregunta": "¿Qué es el time blocking?", "opciones": ["Bloquear horarios específicos", "Trabajar sin parar", "Dormir mucho", "Ver TV"], "correcta": 0, "explicacion": "Asignar bloques de tiempo para cada actividad."},
        {"pregunta": "¿Qué porcentaje del día se recomienda para imprevistos?", "opciones": ["5%", "15-20%", "50%", "0%"], "correcta": 1, "explicacion": "Dejar espacio para lo inesperado reduce el estrés."},
        {"pregunta": "¿Qué herramienta ayuda a organizar tareas?", "opciones": ["Trello", "Word", "Excel", "Paint"], "correcta": 0, "explicacion": "Trello es excelente para organización visual."},
    ]

def generar_preguntas_estres_modulo4():
    return [
        {"pregunta": "¿Cuánto tiempo se recomienda de redes sociales al día?", "opciones": ["30 minutos", "2-3 horas", "5 horas", "Sin límite"], "correcta": 0, "explicacion": "Limitar reduce la ansiedad digital."},
        {"pregunta": "¿Qué es el doomscrolling?", "opciones": ["Ver noticias negativas excesivamente", "Hacer ejercicio", "Meditar", "Dormir"], "correcta": 0, "explicacion": "Consumir exceso de noticias negativas aumenta el estrés."},
        {"pregunta": "¿Qué color de luz afecta el sueño?", "opciones": ["Luz azul", "Luz roja", "Luz amarilla", "Luz verde"], "correcta": 0, "explicacion": "La luz azul altera el ritmo circadiano."},
        {"pregunta": "¿Cuánto antes de dormir apagar pantallas?", "opciones": ["30 min", "1-2 horas", "15 min", "5 min"], "correcta": 1, "explicacion": "1-2 horas es lo ideal."},
        {"pregunta": "¿Qué es un detox digital?", "opciones": ["Desconectarse de dispositivos", "Formatear PC", "Comprar nuevo celular", "Borrar fotos"], "correcta": 0, "explicacion": "Desconectar voluntariamente de la tecnología."},
        {"pregunta": "¿Cuántas notificaciones se reciben en promedio al día?", "opciones": ["10-20", "50-100", "200+", "5"], "correcta": 1, "explicacion": "Las notificaciones excesivas fragmentan la atención."},
        {"pregunta": "¿Qué función de teléfono ayuda al bienestar?", "opciones": ["Modo no molestar", "Modo avión", "Ambas", "Ninguna"], "correcta": 2, "explicacion": "Ambas ayudan a reducir interrupciones."},
        {"pregunta": "¿Qué porcentaje de personas sufre nomofobia?", "opciones": ["10%", "30%", "50%", "70%"], "correcta": 1, "explicacion": "Miedo a estar sin celular."},
        {"pregunta": "¿Qué es el FOMO?", "opciones": ["Miedo a perderse algo", "Miedo a volar", "Ansiedad social", "Pánico"], "correcta": 0, "explicacion": "Fear Of Missing Out."},
        {"pregunta": "¿Qué ayuda a reducir el uso de redes?", "opciones": ["Establecer horarios", "Eliminar apps", "Ambas", "Ninguna"], "correcta": 2, "explicacion": "Combinar estrategias es más efectivo."},
    ]

def generar_preguntas_estres_modulo5():
    return [
        {"pregunta": "¿Qué actividades incluir en un plan de bienestar?", "opciones": ["Ejercicio, descanso, social", "Solo trabajo", "Solo TV", "Solo comer"], "correcta": 0, "explicacion": "El bienestar es holístico."},
        {"pregunta": "¿Con qué frecuencia revisar el plan?", "opciones": ["Semanal", "Mensual", "Anual", "Unica vez"], "correcta": 0, "explicacion": "La revisión semanal permite ajustes."},
        {"pregunta": "¿Qué es un hobby restaurativo?", "opciones": ["Actividad que recarga energía", "Ver TV", "Trabajar", "Dormir"], "correcta": 0, "explicacion": "Actividades que revitalizan."},
        {"pregunta": "¿Cuántos minutos de ejercicio diario recomienda la OMS?", "opciones": ["10 min", "30 min", "1 hora", "2 horas"], "correcta": 1, "explicacion": "30 minutos diarios de actividad moderada."},
        {"pregunta": "¿Qué es el autocuidado?", "opciones": ["Cuidado personal proactivo", "Ser egoísta", "Ignorar necesidades", "Solo belleza"], "correcta": 0, "explicacion": "Atender necesidades físicas y emocionales."},
        {"pregunta": "¿Qué técnica ayuda a mantener hábitos?", "opciones": ["Registro de progreso", "Olvidar metas", "Esperar resultados", "Compararse"], "correcta": 0, "explicacion": "Monitorear el progreso motiva."},
        {"pregunta": "¿Qué es la resiliencia?", "opciones": ["Capacidad de recuperarse", "Evitar problemas", "Ignorar dificultades", "Quejarse"], "correcta": 0, "explicacion": "Adaptarse y superar adversidades."},
        {"pregunta": "¿Qué rol juegan las relaciones sociales?", "opciones": ["Apoyo emocional clave", "No importan", "Causan estrés", "Solo complican"], "correcta": 0, "explicacion": "El apoyo social protege contra el estrés."},
        {"pregunta": "¿Qué es un diario de gratitud?", "opciones": ["Escribir cosas positivas", "Lista de quejas", "Agenda", "Lista de compras"], "correcta": 0, "explicacion": "Fomenta el pensamiento positivo."},
        {"pregunta": "¿Qué porcentaje de felicidad depende de hábitos?", "opciones": ["10%", "40%", "80%", "95%"], "correcta": 1, "explicacion": "Gran parte de la felicidad viene de hábitos intencionales."},
    ]

# ---- Curso Ergonomía ----
def generar_preguntas_ergo_modulo1():
    return [
        {"pregunta": "¿Cuál es el ángulo recomendado para los codos al teclear?", "opciones": ["90°", "45°", "120°", "180°"], "correcta": 0, "explicacion": "Los codos deben formar un ángulo de 90° para evitar tensión."},
        {"pregunta": "¿Dónde debe estar la parte superior de la pantalla?", "opciones": ["A la altura de los ojos", "Por debajo de la barbilla", "A la altura del pecho", "En el suelo"], "correcta": 0, "explicacion": "La parte superior de la pantalla debe estar a la altura de los ojos."},
        {"pregunta": "¿Qué apoya la curvatura lumbar?", "opciones": ["Un cojín lumbar", "Un reposapiés", "Apoyabrazos", "Almohada cervical"], "correcta": 0, "explicacion": "El cojín lumbar mantiene la curva natural de la espalda."},
        {"pregunta": "¿Qué distancia debe haber entre ojos y pantalla?", "opciones": ["20 cm", "50-70 cm", "1 metro", "2 metros"], "correcta": 1, "explicacion": "Un brazo de distancia aprox."},
        {"pregunta": "¿Los pies deben estar...?", "opciones": ["Colgando", "Apoyados en el suelo o reposapiés", "Cruzados", "Sobre la silla"], "correcta": 1, "explicacion": "Apoyados planos para buena circulación."},
        {"pregunta": "¿Qué problema causa la mala postura?", "opciones": ["Dolor cervical", "Mejora la vista", "Aumenta energía", "Fortalece músculos"], "correcta": 0, "explicacion": "La mala postura provoca dolores de cuello y espalda."},
        {"pregunta": "¿Cada cuánto cambiar de postura?", "opciones": ["Cada 8 horas", "Cada 30-60 minutos", "Una vez al día", "Nunca"], "correcta": 1, "explicacion": "Cambiar cada hora evita rigidez."},
        {"pregunta": "¿Qué silla es mejor?", "opciones": ["Silla ergonómica ajustable", "Silla fija de madera", "Sillón mullido", "Banco sin respaldo"], "correcta": 0, "explicacion": "La silla ergonómica permite ajustes personalizados."},
        {"pregunta": "¿Cómo deben estar los hombros al escribir?", "opciones": ["Relajados y hacia atrás", "Encogidos", "Hacia adelante", "Arriba"], "correcta": 0, "explicacion": "Hombros relajados evitan tensión en trapecios."},
        {"pregunta": "¿Qué es el síndrome del túnel carpiano?", "opciones": ["Compresión del nervio mediano", "Dolor de espalda", "Visión borrosa", "Mareo"], "correcta": 0, "explicacion": "Causado por malas posturas de muñeca."},
    ]

def generar_preguntas_ergo_modulo2():
    return [
        {"pregunta": "¿Cuánto debe durar una pausa activa?", "opciones": ["30 segundos", "5 minutos", "30 minutos", "1 hora"], "correcta": 1, "explicacion": "5 minutos cada hora son suficientes."},
        {"pregunta": "¿Qué estiramiento ayuda al cuello?", "opciones": ["Rotación suave izquierda/derecha", "Saltos", "Flexiones", "Sentadillas"], "correcta": 0, "explicacion": "Rotación suave reduce tensión cervical."},
        {"pregunta": "¿Qué ejercicio de manos previene el túnel carpiano?", "opciones": ["Abrir y cerrar puño", "Levantar pesas", "Correr", "Bailar"], "correcta": 0, "explicacion": "Moviliza los tendones."},
        {"pregunta": "¿Cada cuánto hacer una pausa activa?", "opciones": ["Cada 20 min", "Cada hora", "Cada 4 horas", "Solo al inicio"], "correcta": 1, "explicacion": "Ideal cada 60 minutos."},
        {"pregunta": "¿Qué beneficio tiene la pausa activa?", "opciones": ["Mejora circulación", "Aumenta fatiga", "Distrae", "Ninguno"], "correcta": 0, "explicacion": "Activa la circulación y previene lesiones."},
        {"pregunta": "¿Qué hacer si hay dolor de espalda durante la pausa?", "opciones": ["Estirar suavemente", "Ignorar", "Seguir trabajando", "Acostarse"], "correcta": 0, "explicacion": "Estiramientos suaves ayudan."},
        {"pregunta": "¿Qué rutina incluye rotar muñecas?", "opciones": ["Movilidad articular", "Cardio", "Fuerza", "Equilibrio"], "correcta": 0, "explicacion": "Rotaciones mantienen la movilidad."},
        {"pregunta": "¿Cuántos segundos mantener cada estiramiento?", "opciones": ["2 segundos", "15-30 segundos", "1 minuto", "5 minutos"], "correcta": 1, "explicacion": "15-30 segundos es óptimo."},
        {"pregunta": "¿Qué aplicación recuerda pausas activas?", "opciones": ["Stretchly", "Facebook", "WhatsApp", "Twitter"], "correcta": 0, "explicacion": "Stretchly es gratuita y efectiva."},
        {"pregunta": "¿El ejercicio de mirar lejos relaja los ojos?", "opciones": ["Sí", "No", "Solo con lentes", "Nunca"], "correcta": 0, "explicacion": "Enfocar lejos reduce fatiga visual."},
    ]

def generar_preguntas_ergo_modulo3():
    return [
        {"pregunta": "¿En qué consiste la regla 20-20-20?", "opciones": ["20 min, mirar 20 pies, 20 seg", "20 seg, 20 cm, 20 veces", "20 horas, 20 pasos, 20 respiros", "20 parpadeos, 20 seg, 20 m"], "correcta": 0, "explicacion": "Cada 20 min, mira a 20 pies (6m) por 20 seg."},
        {"pregunta": "¿Qué produce la fatiga visual?", "opciones": ["Ojos secos", "Mejor visión", "Mayor concentración", "Energía extra"], "correcta": 0, "explicacion": "El uso prolongado de pantallas reseca los ojos."},
        {"pregunta": "¿Qué lágrimas artificiales usar?", "opciones": ["Sin conservantes", "Con conservantes", "Cualquiera", "Agua común"], "correcta": 0, "explicacion": "Sin conservantes para uso frecuente."},
        {"pregunta": "¿Qué color de pantalla es mejor de noche?", "opciones": ["Luz cálida", "Luz azul", "Blanco brillante", "Verde"], "correcta": 0, "explicacion": "La luz cálida (modo nocturno) respeta el sueño."},
        {"pregunta": "¿Qué filtro reduce la luz azul?", "opciones": ["Filtro físico o software", "Gafas de sol", "Lentes de aumento", "Ninguno"], "correcta": 0, "explicacion": "Hay filtros para pantalla y gafas especiales."},
        {"pregunta": "¿Qué hábito empeora la fatiga visual?", "opciones": ["Parpadear poco", "Usar lágrimas", "Descansar", "Ajustar brillo"], "correcta": 0, "explicacion": "El parpadeo se reduce al 30% frente a pantallas."},
        {"pregunta": "¿Cada cuánto descansar los ojos?", "opciones": ["Cada 20 minutos", "Cada hora", "Cada 5 horas", "Solo al final"], "correcta": 0, "explicacion": "Regla 20-20-20."},
        {"pregunta": "¿Qué posición de pantalla evita reflejos?", "opciones": ["Perpendicular a ventanas", "Frente a ventana", "A espaldas de ventana", "Apagada"], "correcta": 0, "explicacion": "Evita reflejos molestos."},
        {"pregunta": "¿La visión borrosa temporal es normal?", "opciones": ["Sí, por fatiga", "No, siempre patología", "Solo niños", "Nunca"], "correcta": 0, "explicacion": "Con descanso mejora; si persiste, acude al especialista."},
        {"pregunta": "¿Qué tamaño de letra es cómodo?", "opciones": ["12-14 px mínimo", "8 px", "6 px", "20 px"], "correcta": 0, "explicacion": "Fuente legible evita forzar la vista."},
    ]

def generar_preguntas_ergo_modulo4():
    return [
        {"pregunta": "¿El teclado debe estar...?", "opciones": ["Plano o ligeramente inclinado negativo", "Muy inclinado", "Vertical", "Encima del monitor"], "correcta": 0, "explicacion": "Inclinación neutral evita extensión de muñeca."},
        {"pregunta": "¿Qué es un reposamuñecas?", "opciones": ["Apoyo blando para muñecas", "Una almohada", "Un teclado", "Un mouse"], "correcta": 0, "explicacion": "Mantiene la muñeca recta."},
        {"pregunta": "¿Altura recomendada del escritorio?", "opciones": ["68-72 cm", "50 cm", "100 cm", "Al azar"], "correcta": 0, "explicacion": "Estándar para personas promedio."},
        {"pregunta": "¿Qué es un escritorio regulable?", "opciones": ["Altura ajustable (sentado/parado)", "Fijo", "Plegable", "Con ruedas"], "correcta": 0, "explicacion": "Permite alternar posturas."},
        {"pregunta": "¿El mouse debe moverse desde...?", "opciones": ["El codo", "La muñeca", "El hombro", "Los dedos"], "correcta": 0, "explicacion": "Mover desde el codo evita lesiones de muñeca."},
        {"pregunta": "¿Qué relación debe haber entre silla y escritorio?", "opciones": ["Muslos paralelos al suelo", "Rodillas a 120°", "Pies colgando", "Espalda curvada"], "correcta": 0, "explicacion": "Los muslos deben estar horizontales."},
        {"pregunta": "¿Qué accesorio ayuda a la espalda?", "opciones": ["Soporte lumbar", "Colchón", "Cojín para pies", "Gafas"], "correcta": 0, "explicacion": "El soporte lumbar mantiene la curva."},
        {"pregunta": "¿Cuál es la mejor distribución de pantallas duales?", "opciones": ["Ambas al mismo nivel y frente al usuario", "Una al lado pero alta", "Encimadas", "Una detrás"], "correcta": 0, "explicacion": "Evita girar el cuello constantemente."},
        {"pregunta": "¿Qué iluminación es mejor?", "opciones": ["Indirecta y regulable", "Luz directa al monitor", "Oscuridad total", "Neón"], "correcta": 0, "explicacion": "Previene reflejos y fatiga."},
        {"pregunta": "¿Los documentos deben ir...?", "opciones": ["En un soporte junto a la pantalla", "En el regazo", "En el suelo", "Detrás del monitor"], "correcta": 0, "explicacion": "A la misma altura y distancia que la pantalla."},
    ]

def generar_preguntas_ergo_modulo5():
    return [
        {"pregunta": "¿Qué es el síndrome del túnel carpiano?", "opciones": ["Compresión del nervio mediano", "Dolor lumbar", "Tendinitis de hombro", "Fatiga visual"], "correcta": 0, "explicacion": "Por movimientos repetitivos de muñeca."},
        {"pregunta": "¿Síntoma de epicondilitis (codo de tenista)?", "opciones": ["Dolor en codo", "Dolor de cabeza", "Mareo", "Visión doble"], "correcta": 0, "explicacion": "Inflamación de tendones del codo."},
        {"pregunta": "¿Qué previene la tendinitis?", "opciones": ["Pausas y estiramientos", "Trabajar más horas", "Usar muñequeras metálicas", "No moverse"], "correcta": 0, "explicacion": "Descansos regulares y estiramientos."},
        {"pregunta": "¿Qué hacer ante dolor persistente?", "opciones": ["Descansar y consultar médico", "Ignorar", "Trabajar más duro", "Aplicar calor extremo"], "correcta": 0, "explicacion": "No automedicarse, buscar especialista."},
        {"pregunta": "¿Ejercicio para muñeca?", "opciones": ["Flexión/extensión suave", "Saltos", "Fuerza con pesas pesadas", "Inmovilizar"], "correcta": 0, "explicacion": "Mantiene la movilidad."},
        {"pregunta": "¿Qué teclado reduce riesgo de lesiones?", "opciones": ["Ergonómico dividido", "Teclado numérico grande", "Teclado mecánico ruidoso", "Teclado flexible"], "correcta": 0, "explicacion": "Permite posición natural de manos."},
        {"pregunta": "¿Qué postura de manos al teclear es correcta?", "opciones": ["Muñecas rectas", "Muñecas flexionadas", "Manos colgando", "Dedos rígidos"], "correcta": 0, "explicacion": "Neutral evita compresión."},
        {"pregunta": "¿Qué frecuencia de pausas activas en trabajo intensivo?", "opciones": ["5 min cada hora", "15 min cada 4 horas", "30 min cada día", "Sin pausas"], "correcta": 0, "explicacion": "Microdescansos cada hora."},
        {"pregunta": "¿El uso de voz en lugar de tecleo ayuda?", "opciones": ["Sí, reduce repetición", "No, es peor", "Solo si gritas", "Nunca"], "correcta": 0, "explicacion": "Alternativas como dictado reducen estrés repetitivo."},
        {"pregunta": "¿Cuál es el mejor ejercicio para hombros?", "opciones": ["Encogimientos controlados", "Saltar la cuerda", "Flexiones extremas", "Correr"], "correcta": 0, "explicacion": "Encoger y soltar relaja el trapecio."},
    ]

# ---- Curso Comidas ----
def generar_preguntas_comida_modulo1():
    return [
        {"pregunta": "¿Qué es batch cooking?", "opciones": ["Cocinar varias porciones una vez a la semana", "Cocinar cada día", "Comer crudo", "Pedir delivery"], "correcta": 0, "explicacion": "Ahorra tiempo y mantiene alimentación saludable."},
        {"pregunta": "¿Qué día es mejor para batch cooking?", "opciones": ["Domingo", "Lunes", "Miércoles", "Viernes noche"], "correcta": 0, "explicacion": "Prep para toda la semana."},
        {"pregunta": "¿Qué alimentos no congelar bien?", "opciones": ["Lechuga", "Carnes", "Legumbres", "Sopas"], "correcta": 0, "explicacion": "Las verduras de hoja se marchitan."},
        {"pregunta": "¿Cuánto duran las comidas cocinadas en nevera?", "opciones": ["3-4 días", "1 día", "2 semanas", "1 mes"], "correcta": 0, "explicacion": "Máximo 4 días por seguridad."},
        {"pregunta": "¿Qué recipiente es mejor?", "opciones": ["Vidrio hermético", "Plástico desechable", "Bolsa de papel", "Lata abierta"], "correcta": 0, "explicacion": "Vidrio no absorbe olores ni manchas."},
        {"pregunta": "¿Qué grano básico cocinar en batch?", "opciones": ["Arroz integral", "Pan", "Pastas frescas", "Galletas"], "correcta": 0, "explicacion": "Arroz, quinoa, cuscús."},
        {"pregunta": "¿Qué proteína es fácil de batch?", "opciones": ["Pollo desmenuzado", "Filete a la plancha cada día", "Huevos duros (5 min)", "Tofu marinado"], "correcta": 0, "explicacion": "Pollo desmenuzado versátil."},
        {"pregunta": "¿Qué verdura asar en batch?", "opciones": ["Calabacín y berenjena", "Lechuga", "Espinaca cruda", "Pepino"], "correcta": 0, "explicacion": "Asadas mantienen sabor y textura."},
        {"pregunta": "¿Cómo recalentar sin perder nutrientes?", "opciones": ["Vapor o microondas tapado", "Freír de nuevo", "Hervir mucho", "Comer frío"], "correcta": 0, "explicacion": "Recalentar suavemente preserva vitaminas."},
        {"pregunta": "¿Qué beneficio principal del batch cooking?", "opciones": ["Ahorro de tiempo y dinero", "Comer más procesados", "Aumentar delivery", "Saltarse comidas"], "correcta": 0, "explicacion": "Reduce la tentación de comida chatarra."},
    ]

def generar_preguntas_comida_modulo2():
    return [
        {"pregunta": "¿Qué proporción del plato deben ser verduras?", "opciones": ["1/2", "1/4", "1/3", "2/3"], "correcta": 0, "explicacion": "Método del plato: 50% verduras."},
        {"pregunta": "¿Proteína debe ocupar qué parte?", "opciones": ["1/4", "1/2", "1/3", "1/5"], "correcta": 0, "explicacion": "25% del plato."},
        {"pregunta": "¿Carbohidratos complejos ejemplos?", "opciones": ["Arroz integral, quinoa", "Pan blanco", "Galletas", "Azúcar"], "correcta": 0, "explicacion": "Aportan fibra y energía sostenida."},
        {"pregunta": "¿Grasas saludables fuente?", "opciones": ["Aguacate, aceite oliva", "Manteca", "Margarina", "Tocino"], "correcta": 0, "explicacion": "Grasas insaturadas."},
        {"pregunta": "¿Qué es un plato colorido?", "opciones": ["Diferentes vegetales", "Mucho arroz", "Salsa roja", "Comida rápida"], "correcta": 0, "explicacion": "Más colores = más nutrientes."},
        {"pregunta": "¿Qué hidrata mejor?", "opciones": ["Agua", "Jugos azucarados", "Gaseosa", "Café"], "correcta": 0, "explicacion": "Agua sin calorías."},
        {"pregunta": "¿Cuál es el tamaño de porción de fruta?", "opciones": ["1 pieza mediana", "3 piezas", "Medio kilo", "Jugo"], "correcta": 0, "explicacion": "Una manzana, naranja, etc."},
        {"pregunta": "¿Proteína vegetal ejemplo?", "opciones": ["Lentejas", "Carne", "Pollo", "Pescado"], "correcta": 0, "explicacion": "Legumbres."},
        {"pregunta": "¿Qué lácteo es saludable?", "opciones": ["Yogur natural sin azúcar", "Yogur de fresa", "Queso crema", "Leche condensada"], "correcta": 0, "explicacion": "Sin azúcares añadidos."},
        {"pregunta": "¿Qué evitas si usas el método del plato?", "opciones": ["Exceso de calorías", "Variedad", "Saciedad", "Vitaminas"], "correcta": 0, "explicacion": "Controlas porciones."},
    ]

def generar_preguntas_comida_modulo3():
    return [
        {"pregunta": "¿Dónde debe ir la carne cruda en la nevera?", "opciones": ["Estante inferior", "Puerta", "Estante superior", "Cajón de verduras"], "correcta": 0, "explicacion": "Evita contaminación cruzada."},
        {"pregunta": "¿Temperatura segura de nevera?", "opciones": ["4°C o menos", "10°C", "15°C", "0°C"], "correcta": 0, "explicacion": "Inhibe bacterias."},
        {"pregunta": "¿Cuánto duran las sobras cocinadas en congelador?", "opciones": ["2-3 meses", "1 semana", "1 año", "Indefinido"], "correcta": 0, "explicacion": "Calidad óptima 2-3 meses."},
        {"pregunta": "¿Qué etiquetar en recipientes?", "opciones": ["Contenido y fecha", "Solo fecha", "Solo contenido", "Nada"], "correcta": 0, "explicacion": "Saber qué es y cuándo se hizo."},
        {"pregunta": "¿Cómo descongelar seguro?", "opciones": ["Refrigerador", "A temperatura ambiente", "Agua caliente", "Microondas sin vigilancia"], "correcta": 0, "explicacion": "Descongelación lenta en nevera."},
        {"pregunta": "¿Qué alimentos no deben recalentarse?", "opciones": ["Arroz (riesgo Bacillus cereus)", "Pollo", "Verduras", "Sopas"], "correcta": 0, "explicacion": "El arroz mal refrigerado puede intoxicar."},
        {"pregunta": "¿Síntoma de intoxicación alimentaria?", "opciones": ["Diarrea, vómito", "Fiebre alta solo", "Erupción", "Tos"], "correcta": 0, "explicacion": "Gastroenteritis."},
        {"pregunta": "¿Cuánto tiempo puede estar la comida a temperatura ambiente?", "opciones": ["Máx 2 horas", "4 horas", "Todo el día", "1 hora"], "correcta": 0, "explicacion": "Zona de peligro 4-60°C."},
        {"pregunta": "¿Qué es la contaminación cruzada?", "opciones": ["Transferencia de bacterias entre alimentos", "Cocinar dos cosas juntas", "Congelar fresco", "Lavar la tabla"], "correcta": 0, "explicacion": "Usa tablas separadas para crudos y cocidos."},
        {"pregunta": "¿Cada cuánto limpiar la nevera?", "opciones": ["Cada mes", "Cada año", "Cada semana", "Nunca"], "correcta": 0, "explicacion": "Previene moho y malos olores."},
    ]

def generar_preguntas_comida_modulo4():
    return [
        {"pregunta": "¿Primer paso antes de ir al súper?", "opciones": ["Revisar despensa y nevera", "Ir con hambre", "Llevar niños", "No llevar lista"], "correcta": 0, "explicacion": "Evita comprar duplicados."},
        {"pregunta": "¿Lista por zonas?", "opciones": ["Sí, agrupar por sección", "No, al azar", "Solo productos de limpieza", "Solo frutas"], "correcta": 0, "explicacion": "Ahorra tiempo y evita olvidos."},
        {"pregunta": "¿Qué hacer con productos de temporada?", "opciones": ["Comprar más y congelar", "Ignorarlos", "Comprar solo importados", "Desechar"], "correcta": 0, "explicacion": "Son más baratos y sabrosos."},
        {"pregunta": "¿Ir al súper después de comer ayuda?", "opciones": ["Sí, reduces compras impulsivas", "No, da igual", "Solo si tienes hambre", "Es peor"], "correcta": 0, "explicacion": "El hambre impulsa lo no saludable."},
        {"pregunta": "¿Qué mirar en etiquetas?", "opciones": ["Lista de ingredientes y azúcar añadido", "Solo fecha", "Precio", "Diseño"], "correcta": 0, "explicacion": "Evita productos ultraprocesados."},
        {"pregunta": "¿Los productos 'light' son siempre saludables?", "opciones": ["No, pueden tener más azúcar", "Sí", "Solo si son bajos en grasa", "Siempre"], "correcta": 0, "explicacion": "Compara etiquetas."},
        {"pregunta": "¿Qué comprar a granel?", "opciones": ["Legumbres, cereales", "Carnes", "Lácteos", "Pescado"], "correcta": 0, "explicacion": "Reduce plástico y ahorra."},
        {"pregunta": "¿Qué evitar en la lista?", "opciones": ["Snacks ultraprocesados", "Frutas", "Verduras", "Huevos"], "correcta": 0, "explicacion": "Galletas, papas fritas, refrescos."},
        {"pregunta": "¿Cómo almacenar hierbas frescas?", "opciones": ["En un vaso con agua (como flores)", "En bolsa cerrada", "Congeladas enteras", "Al sol"], "correcta": 0, "explicacion": "Duran más así."},
        {"pregunta": "¿Qué marca de calidad-precio buscar?", "opciones": ["Marca blanca en básicos", "La más cara", "Solo ecológico", "Importado"], "correcta": 0, "explicacion": "Lentejas, arroz, latas sin marca."},
    ]

def generar_preguntas_comida_modulo5():
    return [
        {"pregunta": "¿Receta rápida con garbanzos?", "opciones": ["Hummus", "Sopa de sobre", "Hervidos solos", "Fritos"], "correcta": 0, "explicacion": "Hummus en 5 min con procesador."},
        {"pregunta": "¿How to hacer un batido saludable?", "opciones": ["Leche vegetal + fruta + espinaca", "Leche entera + azúcar", "Jugo de naranja + azúcar", "Solo agua"], "correcta": 0, "explicacion": "Añade verduras de hoja verde."},
        {"pregunta": "¿Qué cena rápida y ligera?", "opciones": ["Revuelto de espinacas con huevo", "Pizza congelada", "Hamburguesa", "Patatas fritas"], "correcta": 0, "explicacion": "Listo en 5 minutos."},
        {"pregunta": "¿Qué aliño básico?", "opciones": ["AOVE, vinagre, sal", "Mayonesa", "Kétchup", "Salsa barbacoa"], "correcta": 0, "explicacion": "Aceite de oliva virgen extra."},
        {"pregunta": "¿Postre saludable en 2 minutos?", "opciones": ["Yogur con fruta picada", "Flan de sobre", "Galletas", "Helado"], "correcta": 0, "explicacion": "Proteína y fibra."},
        {"pregunta": "¿Cómo hacer avena instantánea?", "opciones": ["Remojar en leche la noche anterior", "Cocer 30 min", "Microondas 5 min", "Comer cruda"], "correcta": 0, "explicacion": "Avena nocturna (overnight oats)."},
        {"pregunta": "¿Qué snack salado rápido?", "opciones": ["Palitos de zanahoria con hummus", "Patatas fritas", "Galletas saladas", "Palomitas de microondas"], "correcta": 0, "explicacion": "Crudités."},
        {"pregunta": "¿Huevo duro cuánto tarda?", "opciones": ["9-10 min", "3 min", "20 min", "30 min"], "correcta": 0, "explicacion": "Perfecto para llevar."},
        {"pregunta": "¿Qué hacer con verduras que se van a echar a perder?", "opciones": ["Salteado o sopa", "Tirarlas", "Congelarlas crudas sin más", "Dejarlas"], "correcta": 0, "explicacion": "Aprovechar en revueltos o cremas."},
        {"pregunta": "¿Qué aliño sin aceite?", "opciones": ["Limón y especias", "Mantequilla", "Nata", "Salsa rosa"], "correcta": 0, "explicacion": "Bajo en calorías."},
    ]

# ---- Curso Sueño ----
def generar_preguntas_sueno_modulo1():
    return [
        {"pregunta": "¿Cuántos ciclos de sueño se recomiendan por noche?", "opciones": ["4-6 ciclos (7-9 horas)", "1-2 ciclos", "8-10 ciclos", "3 ciclos"], "correcta": 0, "explicacion": "Cada ciclo dura 90 min aprox."},
        {"pregunta": "¿Qué fase del sueño es reparadora?", "opciones": ["Sueño profundo (NREM 3)", "REM", "NREM 1", "Vigilia"], "correcta": 0, "explicacion": "Fase de ondas lentas, restaura el cuerpo."},
        {"pregunta": "¿Qué hormona regula el ritmo circadiano?", "opciones": ["Melatonina", "Cortisol", "Adrenalina", "Serotonina"], "correcta": 0, "explicacion": "Se produce con oscuridad."},
        {"pregunta": "¿A qué hora se libera naturalmente la melatonina?", "opciones": ["Al anochecer", "Al mediodía", "A las 3 am", "Por la mañana"], "correcta": 0, "explicacion": "Con poca luz."},
        {"pregunta": "¿Qué es el ritmo circadiano?", "opciones": ["Reloj biológico de 24h", "Frecuencia cardíaca", "Respiración", "Ciclo menstrual"], "correcta": 0, "explicacion": "Regula sueño-vigilia."},
        {"pregunta": "¿Qué altera el ritmo circadiano?", "opciones": ["Luz azul nocturna", "Ejercicio diurno", "Comer saludable", "Meditación"], "correcta": 0, "explicacion": "Pantallas antes de dormir."},
        {"pregunta": "¿Sueño REM qué función tiene?", "opciones": ["Memoria y aprendizaje", "Crecimiento muscular", "Digestión", "Termorregulación"], "correcta": 0, "explicacion": "Consolida recuerdos."},
        {"pregunta": "¿Qué sucede con sueño insuficiente crónico?", "opciones": ["Riesgo cardiovascular", "Mejora memoria", "Aumenta energía", "Reduce apetito"], "correcta": 0, "explicacion": "Asociado a hipertensión y diabetes."},
        {"pregunta": "¿Qué es la deuda de sueño?", "opciones": ["Diferencia entre horas necesarias y reales", "Tener pesadillas", "Dormir mucho", "Insomnio"], "correcta": 0, "explicacion": "Se acumula y afecta salud."},
        {"pregunta": "¿Los adolescentes necesitan más sueño que adultos?", "opciones": ["Sí (~8-10h)", "No", "Igual", "Menos"], "correcta": 0, "explicacion": "El desarrollo lo requiere."},
    ]

def generar_preguntas_sueno_modulo2():
    return [
        {"pregunta": "¿Cuánto antes de dormir apagar pantallas?", "opciones": ["1-2 horas", "5 minutos", "30 segundos", "No es necesario"], "correcta": 0, "explicacion": "La luz azul inhibe melatonina."},
        {"pregunta": "¿Rutina de relajación ejemplo?", "opciones": ["Baño tibio, lectura, respiración", "Ejercicio intenso", "Ver TV", "Cenar pesado"], "correcta": 0, "explicacion": "Señales de descanso al cerebro."},
        {"pregunta": "¿Qué temperatura ambiente ideal?", "opciones": ["18-20°C", "25-27°C", "30°C", "15°C"], "correcta": 0, "explicacion": "Fresca favorece el sueño."},
        {"pregunta": "¿Qué no hacer en la cama?", "opciones": ["Trabajar o usar celular", "Dormir", "Leer un libro", "Meditar"], "correcta": 0, "explicacion": "Asocia la cama solo al sueño."},
        {"pregunta": "¿Cenar pesado antes de dormir produce?", "opciones": ["Reflujo y malestar", "Mejor sueño", "Más energía", "Pesadillas positivas"], "correcta": 0, "explicacion": "Digestión interfiere."},
        {"pregunta": "¿Qué música ayuda a dormir?", "opciones": ["Sonidos relajantes o ruido blanco", "Rock fuerte", "Música electrónica", "Silencio absoluto"], "correcta": 0, "explicacion": "Disminuye la frecuencia cardíaca."},
        {"pregunta": "¿Cuánto tiempo de rutina antes de dormir?", "opciones": ["30-60 minutos", "10 minutos", "2 horas", "5 minutos"], "correcta": 0, "explicacion": "Tiempo para desacelerar."},
        {"pregunta": "¿Qué bebida ayuda a conciliar el sueño?", "opciones": ["Infusión de manzanilla", "Café", "Bebida energética", "Refresco de cola"], "correcta": 0, "explicacion": "Efecto sedante suave."},
        {"pregunta": "¿Qué hacer si no puedes dormir tras 20 min?", "opciones": ["Levantarse a actividad tranquila", "Forzarse a dormir", "Mirar el reloj", "Tomar pastillas"], "correcta": 0, "explicacion": "Evita asociar cama con frustración."},
        {"pregunta": "¿La meditación guiada funciona?", "opciones": ["Sí, reduce ansiedad", "No, solo distrae", "Solo para monjes", "No hay evidencia"], "correcta": 0, "explicacion": "Aplicaciones como Calm o Headspace."},
    ]

def generar_preguntas_sueno_modulo3():
    return [
        {"pregunta": "¿Cuánto antes de dormir dejar la cafeína?", "opciones": ["6 horas", "1 hora", "2 horas", "12 horas"], "correcta": 0, "explicacion": "La vida media de la cafeína es 5 horas."},
        {"pregunta": "¿Qué efecto tiene el alcohol en el sueño?", "opciones": ["Fragmenta el sueño REM", "Mejora la calidad", "Induce sueño profundo continuo", "No afecta"], "correcta": 0, "explicacion": "Despierta en la madrugada."},
        {"pregunta": "¿Comer picante antes de dormir puede provocar?", "opciones": ["Pesadillas o acidez", "Somnolencia", "Mejor digestión", "Hipotermia"], "correcta": 0, "explicacion": "Aumenta temperatura corporal y reflujo."},
        {"pregunta": "¿Qué nutriente ayuda al sueño?", "opciones": ["Triptófano (pavo, plátano)", "Cafeína", "Azúcar", "Grasas trans"], "correcta": 0, "explicacion": "Precursor de serotonina y melatonina."},
        {"pregunta": "¿La cena debe ser...?", "opciones": ["Ligera y temprano", "Abundante y tarde", "Alta en grasas", "Salada"], "correcta": 0, "explicacion": "Al menos 2-3 horas antes."},
        {"pregunta": "¿Por qué la nicotina perjudica el sueño?", "opciones": ["Estimulante", "Relajante", "No afecta", "Induce sueño"], "correcta": 0, "explicacion": "La nicotina activa el sistema nervioso."},
        {"pregunta": "¿El chocolate negro con leche?", "opciones": ["Contiene teobromina (estimulante)", "Ayuda a dormir", "Neutro", "Solo si es sin azúcar"], "correcta": 0, "explicacion": "Evitar por la noche."},
        {"pregunta": "¿Qué cantidad de agua beber antes de dormir?", "opciones": ["Moderada, para no despertar al baño", "Muy poca (sed)", "1 litro", "Nada"], "correcta": 0, "explicacion": "Equilibrio sin interrupciones."},
        {"pregunta": "¿Qué suplemento natural puede ayudar?", "opciones": ["Melatonina (baja dosis)", "Cafeína", "Ginseng", "Guarana"], "correcta": 0, "explicacion": "Consultar médico."},
        {"pregunta": "¿Comer quesos curados muy tarde afecta?", "opciones": ["Sí, contienen tiramina (estimulante)", "No", "Solo si eres alérgico", "Mejoran el sueño"], "correcta": 0, "explicacion": "Pueden dar energía."},
    ]

def generar_preguntas_sueno_modulo4():
    return [
        {"pregunta": "¿Qué color de pared favorece el sueño?", "opciones": ["Azul suave o gris claro", "Rojo intenso", "Amarillo fluorescente", "Negro mate"], "correcta": 0, "explicacion": "Colores relajantes."},
        {"pregunta": "¿Cortinas blackout?", "opciones": ["Bloquean toda luz exterior", "Solo decorativas", "Dejan pasar luz", "No sirven"], "correcta": 0, "explicacion": "Oscuridad total mejora melatonina."},
        {"pregunta": "¿Colchón y almohada deben ser...?", "opciones": ["De acuerdo a tu postura y peso", "Los más caros", "Los más baratos", "De plumas siempre"], "correcta": 0, "explicacion": "Ergonómicos evitan dolores."},
        {"pregunta": "¿Ruido blanco beneficio?", "opciones": ["Enmascara ruidos molestos", "Distrae", "Despierta", "No tiene efecto"], "correcta": 0, "explicacion": "Ventilador o máquina de ruido blanco."},
        {"pregunta": "¿Mascotas en la cama?", "opciones": ["Pueden interrumpir sueño", "Siempre bien", "Nunca", "Solo gatos"], "correcta": 0, "explicacion": "Movimientos y alergias."},
        {"pregunta": "¿La humedad ideal en dormitorio?", "opciones": ["40-60%", "10%", "80%", "100%"], "correcta": 0, "explicacion": "Evita resequedad y moho."},
        {"pregunta": "¿Ventilar la habitación antes de dormir?", "opciones": ["Sí, renueva el aire", "No, enfría", "Da igual", "Solo en invierno"], "correcta": 0, "explicacion": "Aumenta oxígeno."},
        {"pregunta": "¿Qué usar para bloquear la luz?", "opciones": ["Antifaz (mascarilla)", "Luz de noche", "Pantalla encendida", "Lámpara led"], "correcta": 0, "explicacion": "Útil si no tienes blackout."},
        {"pregunta": "¿El celular en modo avión?", "opciones": ["Reduce radiación y notificaciones", "No afecta", "Consume más batería", "Es peligroso"], "correcta": 0, "explicacion": "Evita distracciones nocturnas."},
        {"pregunta": "¿La planta de lavanda ayuda?", "opciones": ["Su aroma es relajante", "No, alergénica", "Solo si la comes", "Es mito"], "correcta": 0, "explicacion": "Aceite esencial reduce ansiedad."},
    ]

def generar_preguntas_sueno_modulo5():
    return [
        {"pregunta": "¿Se puede recuperar el sueño perdido durmiendo más el fin de semana?", "opciones": ["Parcialmente, pero mejor mantener horarios", "Sí, totalmente", "No, es imposible", "Solo se recupera el 50%"], "correcta": 0, "explicacion": "El jet lag social también afecta."},
        {"pregunta": "¿Qué es la siesta ideal?", "opciones": ["20-30 minutos", "2 horas", "90 minutos", "10 minutos"], "correcta": 0, "explicacion": "Evita inercia del sueño."},
        {"pregunta": "¿A qué hora mejor para siesta?", "opciones": ["14:00-15:00 (post almuerzo)", "9:00", "18:00", "21:00"], "correcta": 0, "explicacion": "Bajada natural de energía."},
        {"pregunta": "¿Cómo combatir el sueño diurno por falta nocturna?", "opciones": ["Luz natural y actividad", "Cafeína en exceso", "Dormir en el trabajo", "No hacer nada"], "correcta": 0, "explicacion": "Exposición solar regula ritmo circadiano."},
        {"pregunta": "¿Qué es la higiene del sueño?", "opciones": ["Hábitos y ambiente para buen descanso", "Limpieza de sábanas", "Ducharse antes", "Cepillarse dientes"], "correcta": 0, "explicacion": "Conjunto de prácticas."},
        {"pregunta": "¿Dormir más de 9 horas siempre es malo?", "opciones": ["No necesariamente, pero si es crónico puede indicar problemas", "Sí, siempre", "Es lo ideal", "Solo en niños"], "correcta": 0, "explicacion": "Posible hipersomnia."},
        {"pregunta": "¿Qué hacer si roncas mucho?", "opciones": ["Consultar por apnea del sueño", "Dormir boca arriba", "Comer más", "Ignorar"], "correcta": 0, "explicacion": "La apnea reduce oxigenación."},
        {"pregunta": "¿El ejercicio diurno mejora el sueño?", "opciones": ["Sí, pero no intenso antes de acostarse", "No, quita energía", "Solo por la mañana", "Empeora"], "correcta": 0, "explicacion": "Ideal por la mañana o tarde."},
        {"pregunta": "¿Qué trastorno impide conciliar el sueño?", "opciones": ["Insomnio", "Hipersomnia", "Narcolepsia", "Sonambulismo"], "correcta": 0, "explicacion": "Dificultad para iniciar o mantener sueño."},
        {"pregunta": "¿A qué especialista acudir por problemas de sueño?", "opciones": ["Médico del sueño", "Dermatólogo", "Cardiólogo", "Traumatólogo"], "correcta": 0, "explicacion": "Neurólogo o neumólogo con unidad del sueño."},
    ]

# ---- Curso Hábitos ----
def generar_preguntas_habitos_modulo1():
    return [
        {"pregunta": "¿Qué es la regla del 1%?", "opciones": ["Mejorar 1% cada día", "Ahorrar 1% del sueldo", "Comer 1% menos", "Correr 1% más"], "correcta": 0, "explicacion": "Los pequeños cambios compuestos generan grandes resultados."},
        {"pregunta": "¿Cuánto mejora en un año el 1% diario?", "opciones": ["37 veces mejor (1.01^365)", "3.7 veces", "100%", "1%"], "correcta": 0, "explicacion": "Efecto compuesto."},
        {"pregunta": "¿Qué libro popularizó este concepto?", "opciones": ["Hábitos atómicos", "El poder del ahora", "Padre rico padre pobre", "El monje que vendió su Ferrari"], "correcta": 0, "explicacion": "James Clear."},
        {"pregunta": "¿Por qué fallan los cambios drásticos?", "opciones": ["No son sostenibles", "Son más efectivos", "Son más rápidos", "Motivan más"], "correcta": 0, "explicacion": "La consistencia supera la intensidad."},
        {"pregunta": "¿Ejemplo de mejora del 1%?", "opciones": ["Leer 2 páginas al día", "Correr una maratón", "Ayunar 3 días", "Dormir 4 horas"], "correcta": 0, "explicacion": "Pequeño hábito fácil."},
        {"pregunta": "¿Qué sistema usar para rastrear 1%?", "opciones": ["Trazador de hábitos (habit tracker)", "Calendario anual", "Diario de sueños", "Lista de compras"], "correcta": 0, "explicacion": "Registro visual motiva."},
        {"pregunta": "¿Qué peligro tiene esperar motivación?", "opciones": ["No es confiable, mejor disciplina", "Es lo correcto", "Da igual", "Solo funciona para deportistas"], "correcta": 0, "explicacion": "La motivación fluctúa, la rutina no."},
        {"pregunta": "¿Qué es la ley de los rendimientos compuestos?", "opciones": ["Pequeñas acciones se acumulan exponencialmente", "Los rendimientos decrecen", "Siempre se obtiene lo mismo", "No aplica a hábitos"], "correcta": 0, "explicacion": "Así funciona el interés compuesto."},
        {"pregunta": "¿Cómo aplicar 1% en ejercicio?", "opciones": ["5 min de estiramientos diarios", "1 hora un día a la semana", "No hacer nada", "Entrenar 6 horas cada domingo"], "correcta": 0, "explicacion": "Empieza ridículamente pequeño."},
        {"pregunta": "¿Qué actitud clave?", "opciones": ["Centrarse en el proceso, no en el resultado", "Obsesionarse con metas", "Compararse", "Buscar atajos"], "correcta": 0, "explicacion": "El resultado es consecuencia."},
    ]

def generar_preguntas_habitos_modulo2():
    return [
        {"pregunta": "¿Qué es la técnica de 'apilamiento de hábitos'?", "opciones": ["Añadir un nuevo hábito después de uno existente", "Hacer todo a la vez", "Apilar objetos", "Competir con otros"], "correcta": 0, "explicacion": "Ej: después de cepillarme, meditar 1 min."},
        {"pregunta": "¿Cuál es un desencadenante efectivo?", "opciones": ["Señal clara (hora, lugar, emoción)", "Decisión vaga", "Intentar recordarlo", "Depender de memoria"], "correcta": 0, "explicacion": "Haré [hábito] a las [hora] en [lugar]."},
        {"pregunta": "¿Qué es la 'regla de los 2 minutos'?", "opciones": ["Comenzar el hábito en ≤ 2 min", "Hacer 2 minutos de todo", "Dos minutos de descanso", "Cronómetro"], "correcta": 0, "explicacion": "Supera la inercia inicial."},
        {"pregunta": "¿Por qué es importante diseñar el entorno?", "opciones": ["Facilita la acción", "No influye", "Solo decoración", "Da pereza"], "correcta": 0, "explicacion": "Si quieres leer, deja un libro en la almohada."},
        {"pregunta": "¿Qué hace más fácil mantener un hábito?", "opciones": ["Recompensa inmediata", "Recompensa a largo plazo", "Castigo", "Ignorarlo"], "correcta": 0, "explicacion": "El cerebro busca gratificaciones rápidas."},
        {"pregunta": "¿Ejemplo de recompensa?", "opciones": ["Marcar un check en el calendario", "Comprar un coche", "Dormir más", "Ver TV"], "correcta": 0, "explicacion": "El simple hecho de tachar es gratificante."},
        {"pregunta": "¿Qué sabotearía un hábito nuevo?", "opciones": ["Hacerlo demasiado difícil", "Empezar muy pequeño", "Tener recordatorios", "Celebrar logros"], "correcta": 0, "explicacion": "Reducir la fricción."},
        {"pregunta": "¿Qué hacer si fallas un día?", "opciones": ["No te pierdas dos veces seguidas", "Abandonar el hábito", "Castigarte", "Compensar el doble"], "correcta": 0, "explicacion": "Un tropiezo no es fracaso."},
        {"pregunta": "¿Cuánto tiempo toma formar un hábito?", "opciones": ["Variable (18-254 días, promedio 66)", "21 días exactos", "1 mes", "1 semana"], "correcta": 0, "explicacion": "Depende de la complejidad."},
        {"pregunta": "¿Qué papel juega la identidad?", "opciones": ["Cree que eres ese tipo de persona", "No importa", "Solo metas", "Fuerza de voluntad"], "correcta": 0, "explicacion": "Yo no fumo vs. estoy dejando de fumar."},
    ]

def generar_preguntas_habitos_modulo3():
    return [
        {"pregunta": "¿Qué es una recaída en hábitos?", "opciones": ["Volver a comportamientos antiguos", "Mejorar", "Avanzar", "Superar meta"], "correcta": 0, "explicacion": "Es normal, lo importante es retomar."},
        {"pregunta": "¿Primer paso tras una recaída?", "opciones": ["Analizar qué lo causó", "Sentir culpa excesiva", "Rendirse", "Compensar con más"], "correcta": 0, "explicacion": "Aprender del detonante."},
        {"pregunta": "¿Cómo evitar el 'efecto qué-diablos'?", "opciones": ["Perdonarte y seguir al día siguiente", "Abandonar la semana", "Comer más", "Culparte"], "correcta": 0, "explicacion": "'Ya rompí la dieta, mejor como todo'."},
        {"pregunta": "¿Qué ayuda a prevenir recaídas?", "opciones": ["Identificar situaciones de alto riesgo", "Evitar pensar en ellas", "Tener un plan de contingencia", "A y C"], "correcta": 3, "explicacion": "Anticipar es clave."},
        {"pregunta": "¿Qué hacer si tienes un antojo?", "opciones": ["Técnica de 'surfear la urgencia' (esperar 10 min)", "Ceder inmediatamente", "Ignorarlo", "Comer mucho"], "correcta": 0, "explicacion": "La urgencia pasa como una ola."},
        {"pregunta": "¿Es mejor la abstinencia total o la moderación?", "opciones": ["Depende de la adicción; para muchos hábitos, moderación es más sostenible", "Siempre abstinencia", "Siempre moderación", "No hay diferencia"], "correcta": 0, "explicacion": "Ej: azúcar vs. alcohol."},
        {"pregunta": "¿Qué es 'contrato de compromiso'?", "opciones": ["Acuerdo contigo mismo o con otro", "Documento legal", "Comprar algo", "Castigo físico"], "correcta": 0, "explicacion": "Ej: pagar 50€ si no cumples."},
        {"pregunta": "¿Qué emoción suele llevar a recaída?", "opciones": ["Estrés o aburrimiento", "Alegría", "Motivación", "Energía"], "correcta": 0, "explicacion": "Las emociones negativas son detonantes comunes."},
        {"pregunta": "¿Cómo volver al hábito tras una recaída?", "opciones": ["Empezar con la versión más pequeña", "Esperar al lunes", "Hacer doble", "Esperar un mes"], "correcta": 0, "explicacion": "Retoma con un micro-hábito."},
        {"pregunta": "¿Qué representa el 'mapa de recaídas'?", "opciones": ["Registro de situaciones y soluciones", "Un mapa físico", "Un diario de comida", "Un calendario"], "correcta": 0, "explicacion": "Herramienta de prevención."},
    ]

def generar_preguntas_habitos_modulo4():
    return [
        {"pregunta": "¿Por qué el apoyo social ayuda?", "opciones": ["Responsabilidad compartida", "No ayuda", "Solo para deportes", "Genera dependencia"], "correcta": 0, "explicacion": "Te sientes observado y animado."},
        {"pregunta": "¿Qué es un 'compañero de rendición de cuentas'?", "opciones": ["Alguien con quien revisas progreso", "Un rival", "Un jefe", "Un familiar"], "correcta": 0, "explicacion": "Ej: amigo con mismo objetivo."},
        {"pregunta": "¿Dónde encontrar comunidades de hábitos?", "opciones": ["Foros, grupos de WhatsApp, Reddit", "En el cine", "En el trabajo", "Solo presencial"], "correcta": 0, "explicacion": "Online o grupos locales."},
        {"pregunta": "¿Qué es la presión positiva de grupo?", "opciones": ["Competencia sana y motivante", "Acoso", "Crítica destructiva", "Indiferencia"], "correcta": 0, "explicacion": "Ver a otros lograr te empuja."},
        {"pregunta": "¿Cuál es la ventaja de un grupo?", "opciones": ["Aprendizaje colectivo", "Menor responsabilidad", "Mayor procrastinación", "Confusión"], "correcta": 0, "explicacion": "Compartir consejos."},
        {"pregunta": "¿Qué es un desafío grupal (ej. 30 días)?", "opciones": ["Actividad conjunta con meta común", "Competencia individual", "Aislarse", "No hacer nada"], "correcta": 0, "explicacion": "Ej: 'Plancha 30 días'."},
        {"pregunta": "¿Cómo encontrar un mentor?", "opciones": ["Buscar a alguien que ya tenga el hábito", "Pagar un curso", "Leer libros", "Ver videos"], "correcta": 0, "explicacion": "Un modelo a seguir."},
        {"pregunta": "¿Qué red social puede ser positiva?", "opciones": ["Grupos de hábitos en Facebook", "TikTok de chismes", "Instagram de famosos", "Twitter político"], "correcta": 0, "explicacion": "Sigue comunidades de mejora."},
        {"pregunta": "¿Qué herramienta de comunidad recomiendas?", "opciones": ["Discord o Telegram", "Tinder", "LinkedIn para trabajo", "Snapchat"], "correcta": 0, "explicacion": "Canales específicos."},
        {"pregunta": "¿El voluntariado puede ayudar a crear hábitos?", "opciones": ["Sí, estructura y compromiso", "No", "Solo si pagas", "Es lo mismo"], "correcta": 0, "explicacion": "Responsabilidad y horarios."},
    ]

def generar_preguntas_habitos_modulo5():
    return [
        {"pregunta": "¿Qué es un detonante (cue) en el ciclo del hábito?", "opciones": ["Señal que inicia el hábito", "La recompensa", "La rutina", "El anhelo"], "correcta": 0, "explicacion": "Ej: notificación, hora, lugar."},
        {"pregunta": "¿Qué parte del cerebro controla los hábitos?", "opciones": ["Ganglios basales", "Corteza prefrontal", "Amígdala", "Hipotálamo"], "correcta": 0, "explicacion": "Procesos automáticos."},
        {"pregunta": "¿Cómo cambiar un mal hábito?", "opciones": ["Identificar detonante, reemplazar rutina", "Eliminar detonante por completo", "Ignorarlo", "Usar fuerza de voluntad pura"], "correcta": 0, "explicacion": "Método de Charles Duhigg."},
        {"pregunta": "¿Qué es la 'rutina' en el bucle?", "opciones": ["Comportamiento en sí", "La señal", "La satisfacción", "La creencia"], "correcta": 0, "explicacion": "Ej: fumar un cigarrillo."},
        {"pregunta": "¿Qué es la recompensa?", "opciones": ["Beneficio que refuerza el hábito", "El detonante", "El contexto", "Un castigo"], "correcta": 0, "explicacion": "Nicotina, azúcar, dopamina."},
        {"pregunta": "¿Cómo reemplazar un mal hábito?", "opciones": ["Mantener detonante y recompensa, cambiar rutina", "Eliminar todo", "Cambiar recompensa", "No hacer nada"], "correcta": 0, "explicacion": "Ej: cuando sientas ansiedad (detonante), en lugar de comer azúcar, respira."},
        {"pregunta": "¿Qué papel juega la creencia?", "opciones": ["Necesaria para superar recaídas", "Irrelevante", "Solo en religión", "Estorba"], "correcta": 0, "explicacion": "Creer que puedes cambiar."},
        {"pregunta": "¿Qué es la 'ley de Hebb'?", "opciones": ["Neuronas que se activan juntas, se conectan", "Ley de la gravedad", "Teoría de la evolución", "Principio de incertidumbre"], "correcta": 0, "explicacion": "Los hábitos fortalecen conexiones sinápticas."},
        {"pregunta": "¿Cuánto tiempo se necesita para deshacer un hábito?", "opciones": ["Puede ser más que crearlo", "Igual que crearlo", "Una semana", "Un día"], "correcta": 0, "explicacion": "Requiere reemplazo y tiempo."},
        {"pregunta": "¿Qué es la 'intención de implementación'?", "opciones": ["Plan específico: Si X, entonces Y", "Pensar en metas", "Visualizar éxito", "Hacer listas"], "correcta": 0, "explicacion": "Reduce ambigüedad."},
    ]

# Diccionario de cursos
CURSO_ESTRES = {
    "nombre": "🌿 Manejo del Estrés y Ansiedad",
    "icono": "🌿",
    "descripcion": "Técnicas prácticas para reducir el estrés en la vida diaria",
    "modulos": {
        "Módulo 1: Identifica tus detonantes de estrés": generar_preguntas_estres_modulo1(),
        "Módulo 2: Respiración y relajación en 5 minutos": generar_preguntas_estres_modulo2(),
        "Módulo 3: Organización del tiempo para reducir ansiedad": generar_preguntas_estres_modulo3(),
        "Módulo 4: Uso saludable de tecnología y redes sociales": generar_preguntas_estres_modulo4(),
        "Módulo 5: Creación de un plan de bienestar emocional": generar_preguntas_estres_modulo5(),
    }
}

CURSO_ERGONOMIA = {
    "nombre": "💻 Ergonomía y Salud Digital",
    "icono": "💻",
    "descripcion": "Cuidado del cuerpo y la mente para personas que pasan horas frente a pantallas",
    "modulos": {
        "Módulo 1: Postura correcta frente al computador": generar_preguntas_ergo_modulo1(),
        "Módulo 2: Ejercicios de pausa activa (5 min)": generar_preguntas_ergo_modulo2(),
        "Módulo 3: Fatiga visual y regla 20-20-20": generar_preguntas_ergo_modulo3(),
        "Módulo 4: Configuración ergonómica del espacio de trabajo": generar_preguntas_ergo_modulo4(),
        "Módulo 5: Prevención de lesiones por movimientos repetitivos": generar_preguntas_ergo_modulo5(),
    }
}

CURSO_COMIDA = {
    "nombre": "🥗 Planificación de Comidas Saludables",
    "icono": "🥗",
    "descripcion": "Organiza tus comidas semanales para comer sano sin pasar horas en la cocina",
    "modulos": {
        "Módulo 1: Principios del batch cooking": generar_preguntas_comida_modulo1(),
        "Módulo 2: Cómo armar un plato balanceado": generar_preguntas_comida_modulo2(),
        "Módulo 3: Almacenamiento seguro de alimentos": generar_preguntas_comida_modulo3(),
        "Módulo 4: Lista de compras inteligente": generar_preguntas_comida_modulo4(),
        "Módulo 5: Recetas rápidas para principiantes": generar_preguntas_comida_modulo5(),
    }
}

CURSO_SUENO = {
    "nombre": "😴 Higiene del Sueño",
    "icono": "😴",
    "descripcion": "Mejora la calidad de tu descanso con hábitos simples y efectivos",
    "modulos": {
        "Módulo 1: Ciclos del sueño y ritmo circadiano": generar_preguntas_sueno_modulo1(),
        "Módulo 2: Rutina de preparación para dormir": generar_preguntas_sueno_modulo2(),
        "Módulo 3: El impacto de la cafeína y la cena nocturna": generar_preguntas_sueno_modulo3(),
        "Módulo 4: Creando un ambiente ideal para dormir": generar_preguntas_sueno_modulo4(),
        "Módulo 5: Cómo recuperar horas de sueño perdidas": generar_preguntas_sueno_modulo5(),
    }
}

CURSO_HABITOS = {
    "nombre": "🔄 Cambio de Hábitos y Comunidad",
    "icono": "🔄",
    "descripcion": "Aprende a crear hábitos duraderos con apoyo comunitario",
    "modulos": {
        "Módulo 1: Regla del 1% mejor cada día": generar_preguntas_habitos_modulo1(),
        "Módulo 2: Estrategias para crear hábitos nuevos": generar_preguntas_habitos_modulo2(),
        "Módulo 3: Manejo de recaídas": generar_preguntas_habitos_modulo3(),
        "Módulo 4: Apoyo comunitario": generar_preguntas_habitos_modulo4(),
        "Módulo 5: Detonantes y rutinas": generar_preguntas_habitos_modulo5(),
    }
}

CURSOS = [CURSO_ESTRES, CURSO_ERGONOMIA, CURSO_COMIDA, CURSO_SUENO, CURSO_HABITOS]

# ==========================================================
# CLASE PARA FONDO CON COLOR SÓLIDO
# ==========================================================
class ColoredBackground(Screen):
    def __init__(self, color=PRIMARY, **kwargs):
        super().__init__(**kwargs)
        self.color = color
        with self.canvas.before:
            Color(*self.color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
    
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

# ==========================================================
# PANTALLA DE BIENVENIDA (con ScrollView)
# ==========================================================
class WelcomeScreen(ColoredBackground):
    def __init__(self, **kwargs):
        super().__init__(color=PRIMARY, **kwargs)
        scroll = ScrollView()
        layout = MDBoxLayout(orientation='vertical', padding=dp(40), spacing=dp(25), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        logo_layout = MDBoxLayout(orientation='vertical', size_hint_y=None, height=dp(150))
        if os.path.exists('logo_saludable.jpg'):
            logo = Image(source='logo_saludable.jpg', size_hint=(None, None), size=(dp(120), dp(120)), pos_hint={'center_x': 0.5})
            logo_layout.add_widget(logo)
        else:
            logo_text = MDLabel(text="🎓", font_style='H1', halign='center', theme_text_color="Custom", text_color=(1,1,1,1), size_hint_y=None, height=dp(100))
            logo_layout.add_widget(logo_text)
        
        layout.add_widget(logo_layout)
        
        title_card = MDCard(orientation='vertical', padding=dp(25), size_hint_y=None, height=dp(200), elevation=ELEVATION, radius=[32], md_bg_color=(1,1,1,0.95), pos_hint={"center_x": 0.5})
        title_label = MDLabel(text="📚 Academia Hábito+", font_style='H2', halign='center', theme_text_color="Custom", text_color=PRIMARY)
        subtitle = MDLabel(text="Certificación en Bienestar Integral", halign='center', theme_text_color="Custom", text_color=PRIMARY_DARK, font_style='H5')
        title_card.add_widget(title_label)
        title_card.add_widget(subtitle)
        layout.add_widget(title_card)
        
        desc = MDLabel(text="5 cursos | 25 módulos | 250 preguntas | Certificados digitales\n¡Mejora tu calidad de vida!", halign='center', theme_text_color="Custom", text_color=(1,1,1,0.95), font_style='Body1', size_hint_y=None, height=dp(80))
        layout.add_widget(desc)
        
        btn_login = MDRaisedButton(text="INICIAR SESIÓN", size_hint=(0.7, None), height=dp(55), pos_hint={'center_x': 0.5}, md_bg_color=ACCENT, font_size="16sp", on_release=lambda x: self.go_to_login())
        layout.add_widget(btn_login)
        
        btn_register = MDFlatButton(text="REGISTRARSE", size_hint=(0.7, None), height=dp(55), pos_hint={'center_x': 0.5}, theme_text_color="Custom", text_color=(1,1,1,1), font_size="16sp", on_release=lambda x: self.go_to_register())
        layout.add_widget(btn_register)
        
        scroll.add_widget(layout)
        self.add_widget(scroll)
    
    def go_to_login(self):
        self.manager.current = "login"
    
    def go_to_register(self):
        self.manager.current = "register"

# ==========================================================
# PANTALLA DE LOGIN (con ScrollView)
# ==========================================================
class LoginScreen(ColoredBackground):
    def __init__(self, **kwargs):
        super().__init__(color=PRIMARY, **kwargs)
        scroll = ScrollView()
        layout = MDBoxLayout(orientation='vertical', padding=dp(40), spacing=dp(20), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        if os.path.exists('logo_saludable.jpg'):
            logo = Image(source='logo_saludable.jpg', size_hint=(None, None), size=(dp(60), dp(60)), pos_hint={'center_x': 0.5})
            layout.add_widget(logo)
        
        card = MDCard(orientation='vertical', padding=dp(25), spacing=dp(15), size_hint=(0.9, None), height=dp(380), pos_hint={'center_x': 0.5}, elevation=ELEVATION, radius=RADIUS, md_bg_color=(1,1,1,0.95))
        
        title = MDLabel(text="Bienvenido de nuevo", font_style='H5', halign='center', theme_text_color="Custom", text_color=PRIMARY, size_hint_y=None, height=dp(50))
        card.add_widget(title)
        
        self.email_input = MDTextField(hint_text="Correo electrónico", mode="fill", size_hint_y=None, height=dp(65), line_color_normal=PRIMARY, line_color_focus=ACCENT, fill_color_normal=(1,1,1,1))
        card.add_widget(self.email_input)
        
        self.password_input = MDTextField(hint_text="Contraseña", mode="fill", password=True, size_hint_y=None, height=dp(65), line_color_normal=PRIMARY, line_color_focus=ACCENT, fill_color_normal=(1,1,1,1))
        card.add_widget(self.password_input)
        
        btn_login = MDRaisedButton(text="INGRESAR", size_hint=(0.8, None), height=dp(50), pos_hint={'center_x': 0.5}, md_bg_color=PRIMARY, on_release=self.do_login)
        card.add_widget(btn_login)
        
        btn_back = MDFlatButton(text="← Volver", size_hint=(0.8, None), height=dp(40), pos_hint={'center_x': 0.5}, theme_text_color="Custom", text_color=GRAY, on_release=lambda x: self.go_back())
        card.add_widget(btn_back)
        
        layout.add_widget(card)
        scroll.add_widget(layout)
        self.add_widget(scroll)
    
    def do_login(self, instance):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()
        if not email or not password:
            self.mostrar_dialogo("Error", "Completa todos los campos")
            return
        usuario = db.login_usuario(email, password)
        if usuario:
            usuario_id, nombre = usuario
            app = MDApp.get_running_app()
            app.usuario_actual = {"id": usuario_id, "nombre": nombre, "email": email}
            self.manager.current = "courses"
        else:
            self.mostrar_dialogo("Error", "Email o contraseña incorrectos")
    
    def mostrar_dialogo(self, titulo, mensaje):
        dialog = MDDialog(title=titulo, text=mensaje, buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())])
        dialog.open()
    
    def go_back(self):
        self.manager.current = "welcome"

# ==========================================================
# PANTALLA DE REGISTRO (con ScrollView)
# ==========================================================
class RegisterScreen(ColoredBackground):
    def __init__(self, **kwargs):
        super().__init__(color=PRIMARY, **kwargs)
        scroll = ScrollView()
        layout = MDBoxLayout(orientation='vertical', padding=dp(40), spacing=dp(20), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        card = MDCard(orientation='vertical', padding=dp(25), spacing=dp(15), size_hint=(0.9, None), height=dp(530), pos_hint={'center_x': 0.5}, elevation=ELEVATION, radius=RADIUS, md_bg_color=(1,1,1,0.95))
        
        title = MDLabel(text="Crear cuenta", font_style='H5', halign='center', theme_text_color="Custom", text_color=PRIMARY, size_hint_y=None, height=dp(50))
        card.add_widget(title)
        
        self.name_input = MDTextField(hint_text="Nombre completo", mode="fill", size_hint_y=None, height=dp(65), line_color_normal=PRIMARY, line_color_focus=ACCENT, fill_color_normal=(1,1,1,1))
        card.add_widget(self.name_input)
        
        self.email_input = MDTextField(hint_text="Correo electrónico", mode="fill", size_hint_y=None, height=dp(65), line_color_normal=PRIMARY, line_color_focus=ACCENT, fill_color_normal=(1,1,1,1))
        card.add_widget(self.email_input)
        
        self.password_input = MDTextField(hint_text="Contraseña", mode="fill", password=True, size_hint_y=None, height=dp(65), line_color_normal=PRIMARY, line_color_focus=ACCENT, fill_color_normal=(1,1,1,1))
        card.add_widget(self.password_input)
        
        self.confirm_input = MDTextField(hint_text="Confirmar contraseña", mode="fill", password=True, size_hint_y=None, height=dp(65), line_color_normal=PRIMARY, line_color_focus=ACCENT, fill_color_normal=(1,1,1,1))
        card.add_widget(self.confirm_input)
        
        btn_register = MDRaisedButton(text="REGISTRARSE", size_hint=(0.8, None), height=dp(50), pos_hint={'center_x': 0.5}, md_bg_color=PRIMARY, on_release=self.do_register)
        card.add_widget(btn_register)
        
        btn_back = MDFlatButton(text="← Volver", size_hint=(0.8, None), height=dp(40), pos_hint={'center_x': 0.5}, theme_text_color="Custom", text_color=GRAY, on_release=lambda x: self.go_back())
        card.add_widget(btn_back)
        
        layout.add_widget(card)
        scroll.add_widget(layout)
        self.add_widget(scroll)
    
    def do_register(self, instance):
        nombre = self.name_input.text.strip()
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()
        confirm = self.confirm_input.text.strip()
        
        if not nombre or not email or not password:
            self.mostrar_dialogo("Error", "Completa todos los campos")
            return
        if password != confirm:
            self.mostrar_dialogo("Error", "Las contraseñas no coinciden")
            return
        if len(password) < 4:
            self.mostrar_dialogo("Error", "La contraseña debe tener al menos 4 caracteres")
            return
        
        usuario_id = db.registrar_usuario(nombre, email, password)
        if usuario_id:
            self.mostrar_dialogo("Éxito", "Registro completado. Ahora inicia sesión.")
            self.manager.current = "login"
        else:
            self.mostrar_dialogo("Error", "El email ya está registrado")
    
    def mostrar_dialogo(self, titulo, mensaje):
        dialog = MDDialog(title=titulo, text=mensaje, buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())])
        dialog.open()
    
    def go_back(self):
        self.manager.current = "welcome"

# ==========================================================
# PANTALLA DE LISTA DE CURSOS (mejorado)
# ==========================================================
class CoursesScreen(ColoredBackground):
    def __init__(self, **kwargs):
        super().__init__(color=PRIMARY, **kwargs)
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        layout = MDBoxLayout(orientation='vertical', spacing=dp(0))
        
        toolbar = MDTopAppBar(title="Mis Cursos", elevation=4, md_bg_color=PRIMARY_DARK, specific_text_color=(1,1,1,1))
        toolbar.left_action_items = [["logout", lambda x: self.logout()]]
        toolbar.right_action_items = [["account", lambda x: self.show_profile()], ["certificate", lambda x: self.ver_certificados()]]
        layout.add_widget(toolbar)
        
        content = MDBoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))
        
        app = MDApp.get_running_app()
        if app.usuario_actual:
            greeting = MDLabel(text=f"👋 ¡Hola, {app.usuario_actual['nombre']}!", font_style='H5', theme_text_color="Custom", text_color=(1,1,1,1), size_hint_y=None, height=dp(50), halign='center')
            content.add_widget(greeting)
        
        scroll = ScrollView()
        courses_grid = MDBoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None)
        courses_grid.bind(minimum_height=courses_grid.setter('height'))
        
        for curso in CURSOS:
            card = self.create_course_card(curso)
            courses_grid.add_widget(card)
        
        scroll.add_widget(courses_grid)
        content.add_widget(scroll)
        
        layout.add_widget(content)
        self.add_widget(layout)
    
    def create_course_card(self, curso):
        app = MDApp.get_running_app()
        # Altura dinámica basada en contenido
        card = MDCard(orientation='vertical', padding=dp(15), spacing=dp(8), size_hint_y=None, elevation=ELEVATION, radius=[16], md_bg_color=(1,1,1,0.95))
        
        title_layout = MDBoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))
        icon_label = MDLabel(text=curso["icono"], font_style='H4', size_hint_x=None, width=dp(50))
        title_label = MDLabel(text=curso["nombre"], font_style='H6', theme_text_color="Custom", text_color=PRIMARY)
        title_layout.add_widget(icon_label)
        title_layout.add_widget(title_label)
        card.add_widget(title_layout)
        
        desc_label = MDLabel(text=curso["descripcion"], theme_text_color="Custom", text_color=GRAY, size_hint_y=None, height=dp(40), font_style='Caption')
        card.add_widget(desc_label)
        
        total_modulos = len(curso["modulos"])
        completados = 0
        if app.usuario_actual:
            progresos = db.obtener_progreso_curso(app.usuario_actual['id'], curso["nombre"])
            completados = sum(1 for p in progresos if p[3] == 1)
            stats_text = f"📚 Progreso: {completados}/{total_modulos} módulos"
            if completados == total_modulos:
                stats_text += " 🎉 Curso completado!"
        else:
            stats_text = f"📚 {total_modulos} módulos (10 preguntas c/u)"
        
        stats_label = MDLabel(text=stats_text, theme_text_color="Custom", text_color=SUCCESS if completados == total_modulos else PRIMARY, size_hint_y=None, height=dp(30), font_style='Caption')
        card.add_widget(stats_label)
        
        btn_ver = MDRaisedButton(text="VER MÓDULOS", size_hint=(0.5, None), height=dp(35), pos_hint={'center_x': 0.5}, md_bg_color=ACCENT, on_release=lambda x, c=curso: self.ver_modulos(c))
        card.add_widget(btn_ver)
        
        # Ajustar altura final
        card.height = dp(50+40+30+35+8*4) # aprox 180 dp
        return card
    
    def ver_modulos(self, curso):
        modulos_screen = self.manager.get_screen("modulos")
        modulos_screen.set_curso(curso)
        self.manager.current = "modulos"
    
    def show_profile(self):
        app = MDApp.get_running_app()
        if app.usuario_actual:
            dialog = MDDialog(title="Mi Perfil", text=f"👤 {app.usuario_actual['nombre']}\n📧 {app.usuario_actual['email']}", buttons=[MDFlatButton(text="Cerrar", on_release=lambda x: dialog.dismiss())])
            dialog.open()
    
    def ver_certificados(self):
        app = MDApp.get_running_app()
        if app.usuario_actual:
            certificados = db.obtener_certificados_usuario(app.usuario_actual['id'])
            if certificados:
                texto = "Tus certificados:\n\n"
                for c in certificados:
                    texto += f"✅ {c[1]} ({c[0]})\n"
            else:
                texto = "Aún no tienes certificados. Completa módulos con 70% o más (7/10 preguntas)."
            dialog = MDDialog(title="📜 Certificados", text=texto, buttons=[MDFlatButton(text="Cerrar", on_release=lambda x: dialog.dismiss())])
            dialog.open()
    
    def logout(self):
        app = MDApp.get_running_app()
        app.usuario_actual = None
        self.manager.current = "welcome"
    
    def on_enter(self):
        self.build_ui()

# ==========================================================
# PANTALLA DE MÓDULOS DE UN CURSO (mejorado)
# ==========================================================
class ModulosScreen(ColoredBackground):
    def __init__(self, **kwargs):
        super().__init__(color=PRIMARY, **kwargs)
        self.curso_actual = None
    
    def set_curso(self, curso):
        self.curso_actual = curso
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        if not self.curso_actual:
            return
        
        layout = MDBoxLayout(orientation='vertical', spacing=dp(0))
        
        toolbar = MDTopAppBar(title=self.curso_actual["nombre"], elevation=4, md_bg_color=PRIMARY_DARK, specific_text_color=(1,1,1,1))
        toolbar.left_action_items = [["arrow-left", lambda x: self.volver_cursos()]]
        layout.add_widget(toolbar)
        
        content = MDBoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        desc_label = MDLabel(text=self.curso_actual["descripcion"], theme_text_color="Custom", text_color=(1,1,1,0.95), size_hint_y=None, height=dp(50), font_style='Body2')
        content.add_widget(desc_label)
        
        info_label = MDLabel(text="📊 Cada módulo tiene 10 preguntas. Necesitas 7 correctas para aprobar.", theme_text_color="Custom", text_color=ACCENT, size_hint_y=None, height=dp(30), font_style='Caption')
        content.add_widget(info_label)
        
        scroll = ScrollView()
        modulos_grid = MDBoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        modulos_grid.bind(minimum_height=modulos_grid.setter('height'))
        
        app = MDApp.get_running_app()
        for modulo_nombre, preguntas in self.curso_actual["modulos"].items():
            card = self.create_modulo_card(modulo_nombre, len(preguntas), app.usuario_actual)
            modulos_grid.add_widget(card)
        
        scroll.add_widget(modulos_grid)
        content.add_widget(scroll)
        
        layout.add_widget(content)
        self.add_widget(layout)
    
    def create_modulo_card(self, modulo_nombre, total_preguntas, usuario):
        card = MDCard(orientation='vertical', padding=dp(15), spacing=dp(8), size_hint_y=None, elevation=ELEVATION, radius=[16], md_bg_color=(1,1,1,0.95))
        
        titulo = MDLabel(text=modulo_nombre, font_style='H6', theme_text_color="Custom", text_color=PRIMARY, size_hint_y=None, height=dp(40))
        card.add_widget(titulo)
        
        estado_text = ""
        estado_color = GRAY
        reiniciar_visible = False
        if usuario:
            progreso = db.obtener_progreso_modulo(usuario['id'], self.curso_actual["nombre"], modulo_nombre)
            if progreso:
                puntaje, total, completado, certificado, ultimo = progreso
                estado_text = f"📊 Puntaje: {puntaje}/{total} | {'✅ Aprobado' if completado else '📝 Pendiente'}"
                estado_color = SUCCESS if completado else GRAY
                if completado:
                    reiniciar_visible = False  # No mostrar reiniciar si ya aprobó (opcional)
                else:
                    reiniciar_visible = True
            else:
                estado_text = f"📝 0/{total_preguntas} preguntas | No iniciado"
                estado_color = GRAY
                reiniciar_visible = False
        else:
            estado_text = f"📝 {total_preguntas} preguntas (mínimo 70% para aprobar)"
            estado_color = GRAY
        
        estado_label = MDLabel(text=estado_text, theme_text_color="Custom", text_color=estado_color, size_hint_y=None, height=dp(30), font_style='Caption')
        card.add_widget(estado_label)
        
        btn_layout = MDBoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(40))
        btn_iniciar = MDRaisedButton(text="INICIAR MÓDULO", size_hint=(0.6, None), height=dp(35), md_bg_color=ACCENT, on_release=lambda x, m=modulo_nombre: self.iniciar_modulo(m))
        btn_layout.add_widget(btn_iniciar)
        if reiniciar_visible:
            btn_reiniciar = MDFlatButton(text="REINICIAR", size_hint=(0.3, None), height=dp(35), theme_text_color="Custom", text_color=ERROR, on_release=lambda x, m=modulo_nombre: self.reiniciar_modulo(m))
            btn_layout.add_widget(btn_reiniciar)
        card.add_widget(btn_layout)
        
        card.height = dp(40+30+40+15+8)  # Ajuste
        return card
    
    def reiniciar_modulo(self, modulo_nombre):
        app = MDApp.get_running_app()
        if app.usuario_actual:
            db.reiniciar_modulo(app.usuario_actual['id'], self.curso_actual["nombre"], modulo_nombre)
            self.build_ui()  # Refrescar pantalla
    
    def iniciar_modulo(self, modulo_nombre):
        app = MDApp.get_running_app()
        app.modulo_actual = modulo_nombre
        app.curso_actual_nombre = self.curso_actual["nombre"]
        quiz_name = f"quiz_{self.curso_actual['nombre']}_{modulo_nombre}".replace(" ", "_")[:50]
        if not self.manager.has_screen(quiz_name):
            self.manager.add_widget(QuizScreen(name=quiz_name, curso=self.curso_actual, modulo=modulo_nombre))
        self.manager.current = quiz_name
    
    def volver_cursos(self):
        self.manager.current = "courses"

# ==========================================================
# PANTALLA DEL QUIZ (mejorado layout sin encimamientos)
# ==========================================================
class QuizScreen(Screen):
    def __init__(self, curso, modulo, **kwargs):
        super().__init__(**kwargs)
        self.curso = curso
        self.modulo_nombre = modulo
        self.questions = curso["modulos"][modulo]
        self.current_index = 0
        self.score = 0
        self.selected_option = -1
        self.answered = False
        self.option_items = []  # Para gestionar selección
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', spacing=dp(0))
        
        toolbar = MDTopAppBar(title=self.modulo_nombre[:25] + "..." if len(self.modulo_nombre) > 25 else self.modulo_nombre, elevation=4, md_bg_color=PRIMARY, specific_text_color=(1,1,1,1))
        toolbar.left_action_items = [["arrow-left", lambda x: self.volver_menu()]]
        layout.add_widget(toolbar)
        
        content = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        self.progress_label = MDLabel(text="", halign='center', size_hint_y=None, height=dp(30), theme_text_color="Custom", text_color=PRIMARY)
        content.add_widget(self.progress_label)
        
        scroll = ScrollView(do_scroll_x=False, do_scroll_y=True)
        scroll_content = MDBoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None)
        scroll_content.bind(minimum_height=scroll_content.setter('height'))
        
        self.question_label = MDLabel(text="", font_style='H6', size_hint_y=None, height=dp(80), halign='left', valign='top', theme_text_color="Custom", text_color=TEXT)
        scroll_content.add_widget(self.question_label)
        
        # Usar MDBoxLayout en lugar de MDList para mejor control
        self.options_box = MDBoxLayout(orientation='vertical', spacing=dp(8), size_hint_y=None)
        self.options_box.bind(minimum_height=self.options_box.setter('height'))
        scroll_content.add_widget(self.options_box)
        
        scroll.add_widget(scroll_content)
        content.add_widget(scroll)
        
        self.check_button = MDRaisedButton(text="✓ Verificar respuesta", pos_hint={'center_x': 0.5}, size_hint=(0.9, None), height=dp(50), md_bg_color=ACCENT, on_release=self.check_answer)
        content.add_widget(self.check_button)
        
        self.feedback_label = MDLabel(text="", halign='center', size_hint_y=None, height=dp(80), theme_text_color="Custom")
        content.add_widget(self.feedback_label)
        
        nav_layout = MDBoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))
        self.prev_button = MDFlatButton(text="◀ Anterior", on_release=self.prev_question, disabled=True)
        self.next_button = MDRaisedButton(text="Siguiente ▶", on_release=self.next_question, disabled=True)
        nav_layout.add_widget(self.prev_button)
        nav_layout.add_widget(self.next_button)
        content.add_widget(nav_layout)
        
        layout.add_widget(content)
        self.add_widget(layout)
        self.load_question()
    
    def volver_menu(self):
        self.manager.current = "modulos"
        if self.manager.has_screen(self.name):
            self.manager.remove_widget(self)
    
    def load_question(self):
        q = self.questions[self.current_index]
        self.question_label.text = q["pregunta"]
        self.progress_label.text = f"📋 Pregunta {self.current_index+1} de {len(self.questions)}"
        self.options_box.clear_widgets()
        self.selected_option = -1
        self.answered = False
        self.check_button.disabled = False
        self.feedback_label.text = ""
        self.next_button.disabled = True
        self.option_items = []
        
        for i, opcion in enumerate(q["opciones"]):
            # Crear un botón plano o etiqueta clickeable
            opt_btn = MDFlatButton(text=f"{chr(65+i)}) {opcion}", size_hint_y=None, height=dp(48), theme_text_color="Custom", text_color=TEXT, md_bg_color=(0.95,0.95,0.95,1))
            opt_btn.bind(on_release=lambda btn, idx=i: self.select_option(idx))
            self.options_box.add_widget(opt_btn)
            self.option_items.append(opt_btn)
        
        self.options_box.height = len(self.option_items) * dp(52)
        self.prev_button.disabled = (self.current_index == 0)
    
    def select_option(self, idx):
        if self.answered:
            return
        self.selected_option = idx
        for i, btn in enumerate(self.option_items):
            if i == idx:
                btn.md_bg_color = (0.98, 0.70, 0.14, 0.4)
                btn.text_color = PRIMARY_DARK
            else:
                btn.md_bg_color = (0.95,0.95,0.95,1)
                btn.text_color = TEXT
    
    def check_answer(self, instance):
        if self.selected_option == -1:
            self.feedback_label.text = "⚠️ Por favor selecciona una opción."
            self.feedback_label.color = ERROR
            return
        q = self.questions[self.current_index]
        correcta = q["correcta"]
        self.answered = True
        self.check_button.disabled = True
        self.next_button.disabled = False
        
        if self.selected_option == correcta:
            self.score += 1
            self.feedback_label.text = f"✅ ¡Correcto! {q['explicacion']}"
            self.feedback_label.color = SUCCESS
        else:
            respuesta_correcta = q["opciones"][correcta]
            self.feedback_label.text = f"❌ Incorrecto. Respuesta correcta: {respuesta_correcta}\n📖 {q['explicacion']}"
            self.feedback_label.color = ERROR
        
        if self.current_index == len(self.questions)-1:
            self.next_button.text = "🏁 Finalizar"
    
    def next_question(self, instance):
        if not self.answered:
            return
        if self.current_index < len(self.questions)-1:
            self.current_index += 1
            self.load_question()
            self.next_button.text = "Siguiente ▶"
        else:
            self.guardar_y_finalizar()
    
    def prev_question(self, instance):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_question()
            self.next_button.text = "Siguiente ▶"
    
    def guardar_y_finalizar(self):
        app = MDApp.get_running_app()
        total = len(self.questions)
        aprobado = db.guardar_progreso_modulo(app.usuario_actual['id'], self.curso["nombre"], self.modulo_nombre, self.score, total)
        porcentaje = (self.score / total) * 100
        
        mensaje = f"📊 Puntaje: {self.score}/{total} ({porcentaje:.0f}%)\n\n"
        if aprobado:
            mensaje += "🎉 ¡FELICIDADES! Has aprobado el módulo.\n✅ Se ha generado tu certificado PDF."
            fecha_str = datetime.now().strftime("%d/%m/%Y")
            usuario = db.obtener_datos_usuario(app.usuario_actual['id'])
            pdf_path = generar_pdf_certificado(usuario[0], self.curso["nombre"], self.modulo_nombre, self.score, total, fecha_str)
            db.marcar_certificado_emitido(app.usuario_actual['id'], self.curso["nombre"], self.modulo_nombre)
            if pdf_path:
                mensaje += f"\n📄 Guardado en: {pdf_path}"
        else:
            mensaje += f"📚 Necesitas al menos {int(total * 0.7)}/{total} (70%) para aprobar.\n🔄 ¡Repite el módulo para certificarte!"
        
        dialog = MDDialog(title="📝 Resultado", text=mensaje, buttons=[MDFlatButton(text="Volver", on_release=lambda x: self.volver_final(dialog))])
        dialog.open()
    
    def volver_final(self, dialog):
        dialog.dismiss()
        self.manager.current = "modulos"
        if self.manager.has_screen(self.name):
            self.manager.remove_widget(self)

# ==========================================================
# APP PRINCIPAL
# ==========================================================
class HealthyHabitsApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.usuario_actual = None
        self.modulo_actual = None
        self.curso_actual_nombre = None

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(CoursesScreen(name="courses"))
        sm.add_widget(ModulosScreen(name="modulos"))
        return sm
    
    def on_stop(self):
        db.close()

if __name__ == "__main__":
    HealthyHabitsApp().run()