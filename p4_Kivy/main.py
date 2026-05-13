import os
import webbrowser
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDIconButton
from kivymd.toast import toast

# Tus módulos existentes
import database as db
import utils
from questions import COURSES
from certificate import generate_module_certificate, check_and_generate_master

# Configuración
NOMBRE_APP = "EduLife - Aprendizaje Saludable"
BANNER = "recursos/banner_default.jpg"
CALIFICACION_MINIMA = 7


def mostrar_mensaje(texto):
    toast(texto)

def abrir_archivo(ruta):
    if os.path.exists(ruta):
        if os.name == 'nt':
            os.startfile(ruta)
        else:
            webbrowser.open(ruta)
    else:
        mostrar_mensaje(f"No se encontró el archivo: {ruta}")

def abrir_guia_estudio(curso):
    """Abre la guía de estudio en PDF correspondiente al curso."""
    # Mapeo exacto con los nombres de curso de questions.py
    guias = {
        "Nutrición y Alimentación Saludable": "guia_nutricion.pdf",
        "Ejercicio y Actividad Física": "guia_ejercicio.pdf",
        "Salud Mental y Bienestar Emocional": "guia_salud_mental.pdf",
        "Higiene y Prevención de Enfermedades": "guia_higiene.pdf",
        "Primeros Auxilios y Respuesta a Emergencias": "guia_primeros_auxilios.pdf",
    }
    nombre_pdf = guias.get(curso)
    if not nombre_pdf:
        mostrar_mensaje(f"No hay guía definida para el curso: {curso}")
        return
    ruta_pdf = os.path.join("recursos", nombre_pdf)
    if os.path.exists(ruta_pdf):
        abrir_archivo(ruta_pdf)
    else:
        mostrar_mensaje(f"Guía no encontrada: {ruta_pdf}")

# ============================================================
# CLASES DE TARJETAS (Cards)
# ============================================================
class CourseCard(MDCard):
    titulo = StringProperty("")
    descripcion = StringProperty("")
    progreso = NumericProperty(0)
    imagen = StringProperty("")
    curso = StringProperty("")

class ModuleCard(MDCard):
    titulo = StringProperty("")
    estado = StringProperty("")
    puntaje = NumericProperty(0)
    intentos = NumericProperty(0)
    modulo = StringProperty("")

class CertificateCard(MDCard):
    titulo = StringProperty("")
    subtitulo = StringProperty("")
    descripcion = StringProperty("")
    ruta_pdf = StringProperty("")

# ============================================================
# KV LANGUAGE (estilo mejorado)
# ============================================================
KV = """
#:import dp kivy.metrics.dp

<CourseCard>:
    orientation: "vertical"
    ripple_behavior: True
    radius: [22, 22, 22, 22]
    md_bg_color: 1, 1, 1, 1

    Image:
        source: root.imagen
        size_hint_y: None
        height: dp(125)

    MDBoxLayout:
        orientation: "vertical"
        padding: dp(14)
        spacing: dp(8)

        MDBoxLayout:
            orientation: "horizontal"
            size_hint_y: None
            height: dp(40)
            spacing: dp(10)

            MDLabel:
                text: root.titulo
                bold: True
                font_style: "H6"
                theme_text_color: "Primary"
                size_hint_x: 0.8

            MDIconButton:
                icon: "book-open-page-variant"
                theme_icon_color: "Primary"
                on_release: app.abrir_guia_curso(root.curso)
                size_hint_x: 0.2

        MDLabel:
            text: root.descripcion
            font_style: "Caption"
            theme_text_color: "Secondary"

        MDProgressBar:
            value: root.progreso

        MDLabel:
            text: "Progreso: " + str(root.progreso) + "%"
            halign: "right"
            font_style: "Caption"

<ModuleCard>:
    ripple_behavior: True
    md_bg_color: .98, .99, 1, 1

    MDBoxLayout:
        orientation: "vertical"
        padding: dp(15)
        spacing: dp(8)

        MDLabel:
            text: root.titulo
            bold: True
            font_style: "H6"

        MDLabel:
            text: "Estado: " + root.estado
            theme_text_color: "Secondary"

        MDLabel:
            text: "Mejor puntaje: " + str(root.puntaje) + "/10"
            theme_text_color: "Secondary"

        MDLabel:
            text: "Intentos: " + str(root.intentos)
            theme_text_color: "Secondary"

<CertificateCard>:
    ripple_behavior: True
    md_bg_color: 1, 1, 1, 1

    MDBoxLayout:
        orientation: "vertical"
        padding: dp(15)
        spacing: dp(6)

        MDLabel:
            text: root.titulo
            bold: True
            font_style: "Subtitle1"

        MDLabel:
            text: root.subtitulo
            theme_text_color: "Secondary"

        MDLabel:
            text: root.descripcion
            theme_text_color: "Secondary"

<SplashScreen>:
    MDFloatLayout:
        md_bg_color: .96, .98, 1, 1

        Image:
            source: "recursos/logo_cecytem.png"
            size_hint: .35, .35
            pos_hint: {"center_x": .5, "center_y": .62}

        MDLabel:
            text: "EduLife - Aprendizaje Saludable"
            halign: "center"
            bold: True
            font_style: "H5"
            pos_hint: {"center_y": .35}

<LoginScreen>:
    MDFloatLayout:
        md_bg_color: .97, .98, 1, 1

        MDCard:
            size_hint: .88, None
            height: dp(430)
            pos_hint: {"center_x": .5, "center_y": .5}
            padding: dp(25)
            spacing: dp(18)
            orientation: "vertical"
            radius: [25, 25, 25, 25]
            elevation: 5

            Image:
                source: "recursos/logo_cecytem.png"
                size_hint_y: None
                height: dp(95)

            MDLabel:
                text: "Iniciar Sesión"
                halign: "center"
                bold: True
                font_style: "H5"

            MDTextField:
                id: login_correo
                hint_text: "Correo electrónico"
                helper_text_mode: "on_focus"

            MDTextField:
                id: login_password
                hint_text: "Contraseña"
                password: True

            MDRaisedButton:
                text: "Ingresar"
                pos_hint: {"center_x": .5}
                on_release: app.login()

            MDTextButton:
                text: "Crear cuenta"
                pos_hint: {"center_x": .5}
                on_release: app.cambiar_pantalla("register")

<RegisterScreen>:
    MDFloatLayout:
        md_bg_color: .97, .98, 1, 1

        MDCard:
            size_hint: .88, None
            height: dp(500)
            pos_hint: {"center_x": .5, "center_y": .5}
            padding: dp(25)
            spacing: dp(18)
            orientation: "vertical"
            radius: [25, 25, 25, 25]
            elevation: 5

            MDLabel:
                text: "Registro"
                halign: "center"
                bold: True
                font_style: "H5"

            MDTextField:
                id: reg_nombre
                hint_text: "Nombre completo"

            MDTextField:
                id: reg_correo
                hint_text: "Correo electrónico"

            MDTextField:
                id: reg_password
                hint_text: "Contraseña"
                password: True

            MDRaisedButton:
                text: "Registrarme"
                pos_hint: {"center_x": .5}
                on_release: app.registrar()

            MDTextButton:
                text: "Volver"
                pos_hint: {"center_x": .5}
                on_release: app.volver("login")

<DashboardScreen>:
    MDBoxLayout:
        orientation: "vertical"
        padding: dp(20)
        spacing: dp(18)

        MDTopAppBar:
            title: "CECyTEM"
            elevation: 3

        MDLabel:
            id: bienvenida
            text: "Bienvenido"
            bold: True
            font_style: "H5"

        MDRaisedButton:
            text: "Entrar a Cursos"
            on_release: app.abrir_cursos()

        MDRaisedButton:
            text: "Mi Perfil"
            on_release: app.abrir_perfil()

        MDRaisedButton:
            text: "Certificados"
            on_release: app.abrir_certificados()

        MDRaisedButton:
            text: "Ajustes"
            on_release: app.abrir_ajustes()

        Widget:

        MDRaisedButton:
            text: "Cerrar Sesión"
            on_release: app.cerrar_sesion()

<CoursesScreen>:
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Cursos"
            left_action_items: [["arrow-left", lambda x: app.volver("dashboard")]]

        ScrollView:
            MDList:
                id: lista_cursos
                padding: dp(10)
                spacing: dp(14)
                size_hint_y: None
                height: self.minimum_height

<ModulesScreen>:
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            id: titulo_modulos
            title: "Módulos"
            left_action_items: [["arrow-left", lambda x: app.volver("courses")]]

        ScrollView:
            MDList:
                id: lista_modulos
                padding: dp(10)
                spacing: dp(12)
                size_hint_y: None
                height: self.minimum_height

<QuizScreen>:
    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(10)

        MDTopAppBar:
            title: "Evaluación"
            left_action_items: [["arrow-left", lambda x: app.volver("modules")]]
            elevation: 4

        MDBoxLayout:
            orientation: "vertical"
            padding: dp(15)
            spacing: dp(8)
            size_hint_y: None
            height: dp(80)
            md_bg_color: 0.95, 0.97, 1, 1

            MDLabel:
                id: titulo_quiz
                text: ""
                halign: "center"
                bold: True
                font_style: "H6"
                color: 0.2, 0.2, 0.2, 1

            MDLabel:
                id: subtitulo_quiz
                text: ""
                halign: "center"
                theme_text_color: "Secondary"
                font_style: "Subtitle2"

        ScrollView:
            do_scroll_x: False
            MDCard:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                radius: [20, 20, 20, 20]
                elevation: 6
                padding: dp(20)
                spacing: dp(15)
                md_bg_color: 1, 1, 1, 1

                MDLabel:
                    id: contador_preguntas
                    text: "Pregunta 1 de 10"
                    bold: True
                    font_style: "Subtitle2"
                    theme_text_color: "Primary"

                MDLabel:
                    id: pregunta_texto
                    text: ""
                    font_style: "Body1"
                    size_hint_y: None
                    height: self.texture_size[1]

                MDBoxLayout:
                    adaptive_height: True
                    spacing: dp(10)

                    MDCheckbox:
                        id: chk_a
                        group: "quiz_opciones"
                        on_active:
                            if self.active: app.respuesta_seleccionada(0)

                    MDLabel:
                        id: opcion_a
                        text: ""
                        valign: "middle"

                MDBoxLayout:
                    adaptive_height: True
                    spacing: dp(10)

                    MDCheckbox:
                        id: chk_b
                        group: "quiz_opciones"
                        on_active:
                            if self.active: app.respuesta_seleccionada(1)

                    MDLabel:
                        id: opcion_b
                        text: ""
                        valign: "middle"

                MDBoxLayout:
                    adaptive_height: True
                    spacing: dp(10)

                    MDCheckbox:
                        id: chk_c
                        group: "quiz_opciones"
                        on_active:
                            if self.active: app.respuesta_seleccionada(2)

                    MDLabel:
                        id: opcion_c
                        text: ""
                        valign: "middle"

                MDBoxLayout:
                    adaptive_height: True
                    spacing: dp(10)

                    MDCheckbox:
                        id: chk_d
                        group: "quiz_opciones"
                        on_active:
                            if self.active: app.respuesta_seleccionada(3)

                    MDLabel:
                        id: opcion_d
                        text: ""
                        valign: "middle"

        MDBoxLayout:
            orientation: "horizontal"
            size_hint_y: None
            height: dp(60)
            spacing: dp(20)
            padding: dp(15)

            MDRaisedButton:
                id: btn_anterior
                text: "Anterior"
                disabled: True
                on_release: app.anterior_pregunta()
                md_bg_color: 0.4, 0.6, 0.9, 1
                text_color: 1, 1, 1, 1

            MDRaisedButton:
                id: btn_siguiente
                text: "Siguiente"
                on_release: app.siguiente_pregunta()
                md_bg_color: 0.2, 0.7, 0.3, 1
                text_color: 1, 1, 1, 1

<ResultScreen>:
    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(10)

        MDTopAppBar:
            title: "Resultados"
            left_action_items: [["arrow-left", lambda x: app.volver("modules")]]
            elevation: 4

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(15)
                spacing: dp(15)
                size_hint_y: None
                height: self.minimum_height

                MDCard:
                    orientation: "vertical"
                    padding: dp(15)
                    spacing: dp(10)
                    radius: [20, 20, 20, 20]
                    elevation: 4
                    md_bg_color: 1, 1, 1, 1

                    MDLabel:
                        text: "Resumen del módulo"
                        bold: True
                        font_style: "H6"
                        halign: "center"

                    MDLabel:
                        id: resultado_curso
                        text: ""
                        halign: "center"
                        font_style: "Subtitle1"

                    MDLabel:
                        id: resultado_modulo
                        text: ""
                        halign: "center"
                        font_style: "Subtitle1"

                    MDSeparator:

                    MDLabel:
                        id: resultado_puntaje
                        text: ""
                        halign: "center"
                        bold: True
                        font_style: "H5"

                    MDLabel:
                        id: resultado_porcentaje
                        text: ""
                        halign: "center"
                        font_style: "H6"

                    MDLabel:
                        id: resultado_estado
                        text: ""
                        halign: "center"
                        bold: True
                        font_style: "H4"

                MDLabel:
                    text: "Detalle por pregunta"
                    bold: True
                    font_style: "Subtitle1"
                    size_hint_y: None
                    height: dp(30)

                MDBoxLayout:
                    id: detalles_container
                    orientation: "vertical"
                    spacing: dp(10)
                    size_hint_y: None
                    height: self.minimum_height

        MDBoxLayout:
            orientation: "horizontal"
            size_hint_y: None
            height: dp(60)
            spacing: dp(15)
            padding: dp(15)

            MDRaisedButton:
                text: "Generar certificado"
                on_release: app.generar_certificado()
                md_bg_color: 0.2, 0.6, 0.9, 1

            MDRaisedButton:
                text: "Abrir certificado"
                on_release: app.abrir_ultimo_certificado()
                md_bg_color: 0.4, 0.4, 0.4, 1

            MDRaisedButton:
                text: "Repetir módulo"
                on_release: app.repetir_modulo()
                md_bg_color: 0.9, 0.5, 0.1, 1

<ProfileScreen>:
    MDBoxLayout:
        orientation: "vertical"
        padding: dp(20)
        spacing: dp(15)

        MDTopAppBar:
            title: "Perfil"
            left_action_items: [["arrow-left", lambda x: app.volver("dashboard")]]

        MDLabel:
            id: perfil_nombre
            bold: True
            font_style: "H5"

        MDLabel:
            id: perfil_correo

        MDLabel:
            id: perfil_promedio

        MDLabel:
            id: perfil_modulos

        MDLabel:
            id: perfil_certificados

<CertificatesScreen>:
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Certificados"
            left_action_items: [["arrow-left", lambda x: app.volver("dashboard")]]

        ScrollView:
            MDList:
                id: lista_certificados
                padding: dp(10)
                spacing: dp(12)
                size_hint_y: None
                height: self.minimum_height

<SettingsScreen>:
    MDBoxLayout:
        orientation: "vertical"
        padding: dp(20)
        spacing: dp(20)

        MDTopAppBar:
            title: "Ajustes"
            left_action_items: [["arrow-left", lambda x: app.volver("dashboard")]]

        MDLabel:
            text: "Configuración básica"

        MDRaisedButton:
            text: "Limpiar campos"
            on_release: app.limpiar_campos()

        MDRaisedButton:
            text: "Cerrar sesión"
            on_release: app.cerrar_sesion()
"""

# ============================================================
# SCREENS (definiciones vacías, el KV las completa)
# ============================================================
class SplashScreen(Screen): pass
class LoginScreen(Screen): pass
class RegisterScreen(Screen): pass
class DashboardScreen(Screen): pass
class CoursesScreen(Screen): pass
class ModulesScreen(Screen): pass
class QuizScreen(Screen): pass
class ResultScreen(Screen): pass
class ProfileScreen(Screen): pass
class CertificatesScreen(Screen): pass
class SettingsScreen(Screen): pass

# ============================================================
# APLICACIÓN PRINCIPAL
# ============================================================
class EducationApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.usuario = None          # dict con id, nombre, correo
        self.curso_actual = None
        self.modulo_actual = None
        self.puntaje_actual = 0
        self.preguntas_lista = []
        self.indice_pregunta = 0
        self.respuestas_usuario = []
        self.quiz_finalizado = False

    def build(self):
        self.title = NOMBRE_APP
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"      # Azul institucional
        self.theme_cls.primary_hue = "800"           # Azul más oscuro
        self.theme_cls.accent_palette = "Orange"     # Dorado/anaranjado
        self.theme_cls.accent_hue = "500"

        Builder.load_string(KV)

        sm = ScreenManager(transition=FadeTransition(duration=0.35))
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(CoursesScreen(name="courses"))
        sm.add_widget(ModulesScreen(name="modules"))
        sm.add_widget(QuizScreen(name="quiz"))
        sm.add_widget(ResultScreen(name="result"))
        sm.add_widget(ProfileScreen(name="profile"))
        sm.add_widget(CertificatesScreen(name="certificates"))
        sm.add_widget(SettingsScreen(name="settings"))

        Clock.schedule_once(self.ir_login, 2.5)
        return sm

    def on_start(self):
        utils.ensure_folders()
        db.create_tables()
        mostrar_mensaje("Bienvenido a EduLife")

    # ============================================================
    # NAVEGACIÓN
    # ============================================================
    def cambiar_pantalla(self, pantalla):
        self.root.transition = SlideTransition(direction="left")
        self.root.current = pantalla

    def volver(self, pantalla):
        self.root.transition = SlideTransition(direction="right")
        self.root.current = pantalla

    def ir_login(self, *args):
        self.root.current = "login"

    # ============================================================
    # LOGIN Y REGISTRO (usando tu database.py)
    # ============================================================
    def login(self):
        pantalla = self.root.get_screen("login")
        correo = pantalla.ids.login_correo.text.strip()
        password = pantalla.ids.login_password.text.strip()

        if not correo or not password:
            mostrar_mensaje("Completa todos los campos")
            return

        user_id = db.login_user(correo, password)
        if user_id:
            user_data = db.get_user_by_id(user_id)
            self.usuario = {
                "id": user_id,
                "nombre": user_data[1],
                "correo": user_data[2]
            }
            dashboard = self.root.get_screen("dashboard")
            dashboard.ids.bienvenida.text = f"Bienvenido, {self.usuario['nombre']}"
            mostrar_mensaje("Inicio de sesión correcto")
            self.cambiar_pantalla("dashboard")
        else:
            mostrar_mensaje("Credenciales incorrectas")

    def registrar(self):
        pantalla = self.root.get_screen("register")
        nombre = pantalla.ids.reg_nombre.text.strip()
        correo = pantalla.ids.reg_correo.text.strip()
        password = pantalla.ids.reg_password.text.strip()

        if not nombre or not correo or not password:
            mostrar_mensaje("Completa todos los campos")
            return

        if db.register_user(nombre, correo, password):
            mostrar_mensaje("Registro exitoso. Inicia sesión.")
            pantalla.ids.reg_nombre.text = ""
            pantalla.ids.reg_correo.text = ""
            pantalla.ids.reg_password.text = ""
            self.volver("login")
        else:
            mostrar_mensaje("El correo ya está registrado")

    # ============================================================
    # DASHBOARD
    # ============================================================
    def abrir_cursos(self):
        self.cargar_cursos()
        self.cambiar_pantalla("courses")

    def abrir_perfil(self):
        if not self.usuario:
            return
        # Calcular estadísticas del usuario
        total_modulos = 0
        aprobados = 0
        for course_name, modules in COURSES.items():
            total_modulos += len(modules)
            for module_name in modules:
                prog = db.get_progress(self.usuario["id"], course_name, module_name)
                if prog and prog[6]:  # passed
                    aprobados += 1
        porcentaje = (aprobados / total_modulos * 100) if total_modulos > 0 else 0
        certificados = len(db.get_certificates(self.usuario["id"]))
        pantalla = self.root.get_screen("profile")
        pantalla.ids.perfil_nombre.text = f"Nombre: {self.usuario['nombre']}"
        pantalla.ids.perfil_correo.text = f"Correo: {self.usuario['correo']}"
        pantalla.ids.perfil_promedio.text = f"Progreso total: {porcentaje:.1f}%"
        pantalla.ids.perfil_modulos.text = f"Módulos aprobados: {aprobados}/{total_modulos}"
        pantalla.ids.perfil_certificados.text = f"Certificados emitidos: {certificados}"
        self.cambiar_pantalla("profile")

    def abrir_certificados(self):
        contenedor = self.root.get_screen("certificates").ids.lista_certificados
        contenedor.clear_widgets()
        certificados = db.get_certificates(self.usuario["id"])
        if not certificados:
            mostrar_mensaje("Aún no tienes certificados")
            self.cambiar_pantalla("certificates")
            return
        for cert in certificados:
            # cert: id, user_id, course_name, module_name, score, total, percentage, folio, date, hash, pdf_path
            card = CertificateCard(
                titulo=f"{cert[2]} - {cert[3]}",
                subtitulo=f"Calificación: {cert[4]}/{cert[5]} ({cert[6]:.0f}%)",
                descripcion=f"Folio: {cert[7]}",
                ruta_pdf=cert[10] if len(cert) > 10 else "",
                size_hint_y=None,
                height=dp(145),
                radius=[18, 18, 18, 18],
                elevation=2,
                padding=dp(10),
            )
            card.bind(on_release=lambda x, r=cert[10]: abrir_archivo(r) if r else None)
            contenedor.add_widget(card)
        # También mostrar certificados maestros
        master_certs = db.get_master_certificates(self.usuario["id"])
        for mc in master_certs:
            card = CertificateCard(
                titulo=f"CERTIFICADO MASTER - {mc[2]}",
                subtitulo="Curso completo",
                descripcion=f"Folio: {mc[3]}",
                ruta_pdf=mc[6],
                size_hint_y=None,
                height=dp(145),
                radius=[18, 18, 18, 18],
                elevation=2,
                padding=dp(10),
            )
            card.bind(on_release=lambda x, r=mc[6]: abrir_archivo(r))
            contenedor.add_widget(card)
        self.cambiar_pantalla("certificates")

    def abrir_ajustes(self):
        self.cambiar_pantalla("settings")

    def cerrar_sesion(self):
        self.limpiar_campos()
        self.usuario = None
        self.curso_actual = None
        self.modulo_actual = None
        self.root.current = "login"
        mostrar_mensaje("Sesión finalizada")

    def limpiar_campos(self):
        login = self.root.get_screen("login")
        register = self.root.get_screen("register")
        login.ids.login_correo.text = ""
        login.ids.login_password.text = ""
        register.ids.reg_nombre.text = ""
        register.ids.reg_correo.text = ""
        register.ids.reg_password.text = ""

    # ============================================================
    # GUÍAS DE ESTUDIO
    # ============================================================
    def abrir_guia_curso(self, curso):
        abrir_guia_estudio(curso)

    # ============================================================
    # CURSOS Y MÓDULOS (con CourseCard y ModuleCard)
    # ============================================================
    def cargar_cursos(self):
        contenedor = self.root.get_screen("courses").ids.lista_cursos
        contenedor.clear_widgets()
        banners = {
            "Nutrición y Alimentación Saludable": "recursos/banner_nutricion.jpg",
            "Ejercicio y Actividad Física": "recursos/banner_ejercicio.jpg",
            "Salud Mental y Bienestar Emocional": "recursos/banner_salud_mental.jpg",
            "Higiene y Prevención de Enfermedades": "recursos/banner_higiene.jpg",
            "Primeros Auxilios y Respuesta a Emergencias": "recursos/banner_primeros_auxilios.jpg",
        }

        # Calcular progreso por curso
        progreso_usuario = []
        for course_name, modules in COURSES.items():
            completados = 0
            total = len(modules)
            for module_name in modules:
                prog = db.get_progress(self.usuario["id"], course_name, module_name)
                if prog and prog[6]:
                    completados += 1
            progreso_curso = int((completados / total) * 100) if total > 0 else 0
            descripcion = COURSES[course_name].get("descripcion", "Curso de bienestar integral")
            card = CourseCard(
                titulo=course_name,
                descripcion=descripcion,
                progreso=progreso_curso,
                imagen=banners.get(course_name, BANNER),
                curso=course_name,
                size_hint_y=None,
                height=dp(230),
                radius=[22, 22, 22, 22],
                elevation=4,
                padding=0,
                spacing=0,
            )
            card.bind(on_release=lambda x, c=course_name: self.abrir_modulos(c))
            contenedor.add_widget(card)

    def abrir_modulos(self, curso):
        self.curso_actual = curso
        pantalla = self.root.get_screen("modules")
        pantalla.ids.titulo_modulos.text = curso
        self.cargar_modulos()
        self.cambiar_pantalla("modules")

    def cargar_modulos(self):
        contenedor = self.root.get_screen("modules").ids.lista_modulos
        contenedor.clear_widgets()
        modulos = COURSES.get(self.curso_actual, {})
        for modulo_nombre, preguntas in modulos.items():
            progreso = db.get_progress(self.usuario["id"], self.curso_actual, modulo_nombre)
            if progreso:
                estado = "Completado" if progreso[6] else "No aprobado"
                puntaje = progreso[4]  # best_score
                # Contar intentos desde la tabla attempts
                # (opcional, podrías contar intentos si lo deseas)
                intentos = 1  # placeholder
            else:
                estado = "Pendiente"
                puntaje = 0
                intentos = 0
            card = ModuleCard(
                titulo=modulo_nombre,
                estado=estado,
                puntaje=puntaje,
                intentos=intentos,
                modulo=modulo_nombre,
                size_hint_y=None,
                height=dp(150),
                radius=[18, 18, 18, 18],
                elevation=3,
                padding=dp(10),
            )
            card.bind(on_release=lambda x, m=modulo_nombre: self.iniciar_modulo(m))
            contenedor.add_widget(card)

    def iniciar_modulo(self, modulo):
        self.modulo_actual = modulo
        self.cargar_quiz()
        self.cambiar_pantalla("quiz")

    # ============================================================
    # QUIZ (pregunta a pregunta con checkboxes)
    # ============================================================
    def cargar_quiz(self):
        """Inicializa el cuestionario"""
        self.preguntas_lista = list(COURSES[self.curso_actual][self.modulo_actual])
        self.indice_pregunta = 0
        self.respuestas_usuario = [None] * len(self.preguntas_lista)
        self.quiz_finalizado = False

        pantalla = self.root.get_screen("quiz")
        pantalla.ids.titulo_quiz.text = self.curso_actual
        pantalla.ids.subtitulo_quiz.text = self.modulo_actual

        self.cargar_pregunta_actual()
        self.actualizar_botones_navegacion()

    def cargar_pregunta_actual(self):
        pantalla = self.root.get_screen("quiz")
        pregunta = self.preguntas_lista[self.indice_pregunta]

        pantalla.ids.pregunta_texto.text = pregunta["question"]
        opciones = pregunta["options"]
        pantalla.ids.opcion_a.text = f"A) {opciones[0]}"
        pantalla.ids.opcion_b.text = f"B) {opciones[1]}"
        pantalla.ids.opcion_c.text = f"C) {opciones[2]}"
        pantalla.ids.opcion_d.text = f"D) {opciones[3]}"

        # Resetear checkboxes
        chk_a = pantalla.ids.chk_a
        chk_b = pantalla.ids.chk_b
        chk_c = pantalla.ids.chk_c
        chk_d = pantalla.ids.chk_d
        chk_a.active = False
        chk_b.active = False
        chk_c.active = False
        chk_d.active = False

        resp = self.respuestas_usuario[self.indice_pregunta]
        if resp == 0:
            chk_a.active = True
        elif resp == 1:
            chk_b.active = True
        elif resp == 2:
            chk_c.active = True
        elif resp == 3:
            chk_d.active = True

        # Si el quiz ya terminó, deshabilitar checkboxes
        if self.quiz_finalizado:
            chk_a.disabled = True
            chk_b.disabled = True
            chk_c.disabled = True
            chk_d.disabled = True
        else:
            chk_a.disabled = False
            chk_b.disabled = False
            chk_c.disabled = False
            chk_d.disabled = False

        pantalla.ids.contador_preguntas.text = f"Pregunta {self.indice_pregunta + 1} de {len(self.preguntas_lista)}"

    def respuesta_seleccionada(self, opcion_idx):
        if self.quiz_finalizado:
            return
        self.respuestas_usuario[self.indice_pregunta] = opcion_idx

    def actualizar_botones_navegacion(self):
        pantalla = self.root.get_screen("quiz")
        pantalla.ids.btn_anterior.disabled = (self.indice_pregunta == 0)
        if self.indice_pregunta == len(self.preguntas_lista) - 1:
            pantalla.ids.btn_siguiente.text = "Finalizar"
        else:
            pantalla.ids.btn_siguiente.text = "Siguiente"

    def siguiente_pregunta(self):
        if self.quiz_finalizado:
            return
        if self.respuestas_usuario[self.indice_pregunta] is None:
            mostrar_mensaje("Selecciona una respuesta antes de continuar.")
            return

        if self.indice_pregunta == len(self.preguntas_lista) - 1:
            self.finalizar_quiz()
        else:
            self.indice_pregunta += 1
            self.cargar_pregunta_actual()
            self.actualizar_botones_navegacion()

    def anterior_pregunta(self):
        if self.quiz_finalizado:
            return
        if self.indice_pregunta > 0:
            self.indice_pregunta -= 1
            self.cargar_pregunta_actual()
            self.actualizar_botones_navegacion()

    def finalizar_quiz(self):
        if any(r is None for r in self.respuestas_usuario):
            mostrar_mensaje("Debes responder todas las preguntas antes de finalizar.")
            return

        self.quiz_finalizado = True
        self.cargar_pregunta_actual()  # para deshabilitar checkboxes

        aciertos = 0
        desglose = []
        for i, pregunta in enumerate(self.preguntas_lista):
            resp_user = self.respuestas_usuario[i]
            es_correcta = (resp_user == pregunta["answer"])
            if es_correcta:
                aciertos += 1
            desglose.append({
                "texto": pregunta["question"],
                "opciones": pregunta["options"],
                "correcta_idx": pregunta["answer"],
                "user_idx": resp_user,
                "correcta": es_correcta
            })

        self.puntaje_actual = aciertos
        total = len(self.preguntas_lista)
        porcentaje = (aciertos / total) * 100
        passed = aciertos >= 7

        # Guardar intento y progreso
        db.save_attempt(self.usuario["id"], self.curso_actual, self.modulo_actual, aciertos, total, passed)
        old_progress = db.get_progress(self.usuario["id"], self.curso_actual, self.modulo_actual)
        if old_progress is None:
            db.save_progress(self.usuario["id"], self.curso_actual, self.modulo_actual, aciertos, total, passed)
        else:
            old_best = old_progress[4]
            if aciertos > old_best:
                db.update_progress(self.usuario["id"], self.curso_actual, self.modulo_actual, aciertos, total, passed)

        # Mostrar resultados
        resultado_screen = self.root.get_screen("result")
        resultado_screen.ids.resultado_curso.text = self.curso_actual
        resultado_screen.ids.resultado_modulo.text = self.modulo_actual
        resultado_screen.ids.resultado_puntaje.text = f"{aciertos}/{total}"
        resultado_screen.ids.resultado_porcentaje.text = f"{porcentaje:.1f}%"

        if passed:
            resultado_screen.ids.resultado_estado.text = "APROBADO"
            resultado_screen.ids.resultado_estado.color = (0, 0.6, 0, 1)
        else:
            resultado_screen.ids.resultado_estado.text = "REPROBADO"
            resultado_screen.ids.resultado_estado.color = (0.85, 0, 0, 1)

        detalles_container = resultado_screen.ids.detalles_container
        detalles_container.clear_widgets()
        for idx, d in enumerate(desglose, 1):
            card = MDCard(
                orientation="vertical",
                size_hint_y=None,
                height=dp(160),
                radius=[12, 12, 12, 12],
                elevation=2,
                padding=dp(10),
                spacing=dp(5),
                md_bg_color=(1,1,1,1)
            )
            icono = "checkbox-marked-circle" if d["correcta"] else "close-circle"
            color_icono = (0,0.8,0,1) if d["correcta"] else (0.9,0.2,0,1)
            encabezado = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(30), spacing=dp(5))
            encabezado.add_widget(MDIcon(icon=icono, theme_text_color="Custom", text_color=color_icono))
            encabezado.add_widget(MDLabel(text=f"Pregunta {idx}: {d['texto'][:80]}", bold=True))
            card.add_widget(encabezado)

            letra_user = ["A", "B", "C", "D"][d["user_idx"]] if d["user_idx"] is not None else "Ninguna"
            texto_user = f"Tu respuesta: {letra_user}) {d['opciones'][d['user_idx']]}" if d["user_idx"] is not None else "Sin respuesta"
            card.add_widget(MDLabel(text=texto_user, size_hint_y=None, height=dp(25), font_style="Caption"))

            letra_correcta = ["A", "B", "C", "D"][d["correcta_idx"]]
            texto_correcta = f"Correcta: {letra_correcta}) {d['opciones'][d['correcta_idx']]}"
            card.add_widget(MDLabel(text=texto_correcta, size_hint_y=None, height=dp(25), font_style="Caption"))

            detalles_container.add_widget(card)

        self.cambiar_pantalla("result")

    # ============================================================
    # RESULTADOS Y CERTIFICADOS
    # ============================================================
    def generar_certificado(self):
        if self.puntaje_actual < 7:
            mostrar_mensaje(f"No alcanzaste la mínima aprobatoria ({CALIFICACION_MINIMA}/10)")
            return
        user_name = self.usuario["nombre"]
        user_id = self.usuario["id"]
        course = self.curso_actual
        module = self.modulo_actual
        score = self.puntaje_actual
        total = len(self.preguntas_lista)
        percentage = (score / total) * 100
        generate_module_certificate(user_id, user_name, course, module, score, total, percentage)
        check_and_generate_master(user_id, user_name, course)
        mostrar_mensaje("Certificado generado correctamente")

    def abrir_ultimo_certificado(self):
        certificados = db.get_certificates(self.usuario["id"])
        for cert in certificados:
            if cert[2] == self.curso_actual and cert[3] == self.modulo_actual:
                ruta = cert[10]
                if ruta and os.path.exists(ruta):
                    webbrowser.open(ruta)
                else:
                    mostrar_mensaje("El archivo PDF no se encuentra")
                return
        mostrar_mensaje("No hay certificado para este módulo")

    def repetir_modulo(self):
        self.cargar_quiz()
        self.volver("quiz")

if __name__ == "__main__":
    EducationApp().run()