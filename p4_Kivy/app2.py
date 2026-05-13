from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import os
from datetime import datetime
from database import Database

def obtener_categoria(edad: int) -> str:
    if edad < 0:
        return "Edad inválida"
    elif edad <= 12:
        return "Niño/a"
    elif edad <= 17:
        return "Adolescente"
    elif edad <= 25:
        return "Joven adulto/a"
    elif edad <= 59:
        return "Adulto/a"
    else:
        return "Adulto/a mayor"

def guardar_usuario(nombre: str, edad: int) -> str:
    archivo = "usuarios.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    categoria = obtener_categoria(edad)
    try:
        with open(archivo, "a", encoding="utf-8") as f:
            f.write(
                f"[{timestamp}] Nombre: {nombre} | "
                f"Edad: {edad} | Categoria: {categoria}\n"
            )
        return os.path.abspath(archivo)
    except IOError as e:
        return f"Error al guardar: {e}"

class PantallaFormulario(Screen):
    pass

class PantallaResultado(Screen):
    pass

class PantallaHistorial(Screen):
    pass

KV = """
ScreenManager:
    PantallaFormulario:
        name: "formulario"
    PantallaResultado:
        name: "resultado"
    PantallaHistorial:
        name: "historial"

<PantallaFormulario>:
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Registro de Usuario"
            md_bg_color: app.theme_cls.primary_color
            specific_text_color: 1, 1, 1, 1
            elevation: 4

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: "28dp"
                spacing: "18dp"
                adaptive_height: True

                Widget:
                    size_hint_y: None
                    height: "24dp"

                MDLabel:
                    text: "Ingresa tus datos"
                    font_style: "H5"
                    halign: "center"
                    size_hint_y: None
                    height: self.texture_size[1]

                Widget:
                    size_hint_y: None
                    height: "12dp"

                MDTextField:
                    id: campo_nombre
                    hint_text: "Nombre completo"
                    icon_right: "account"
                    mode: "rectangle"

                MDTextField:
                    id: campo_edad
                    hint_text: "Edad (años)"
                    icon_right: "calendar"
                    mode: "rectangle"
                    input_filter: "int"

                MDLabel:
                    id: lbl_error
                    text: ""
                    halign: "center"
                    theme_text_color: "Error"
                    size_hint_y: None
                    height: "28dp"

                Widget:
                    size_hint_y: None
                    height: "8dp"

                MDRaisedButton:
                    text: "CONTINUAR"
                    pos_hint: {"center_x": .5}
                    md_bg_color: app.theme_cls.primary_color
                    on_release: app.validar_y_continuar()

                MDFlatButton:
                    text: "LIMPIAR"
                    pos_hint: {"center_x": .5}
                    on_release: app.limpiar_formulario()

<PantallaResultado>:
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Resultado"
            md_bg_color: app.theme_cls.primary_color
            specific_text_color: 1, 1, 1, 1
            elevation: 4
            left_action_items: [["arrow-left", lambda x: app.volver_formulario()]]

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: "28dp"
                spacing: "20dp"
                adaptive_height: True

                Widget:
                    size_hint_y: None
                    height: "20dp"

                MDCard:
                    orientation: "vertical"
                    padding: "24dp"
                    spacing: "14dp"
                    size_hint_y: None
                    height: self.minimum_height
                    elevation: 4
                    radius: [12]

                    MDLabel:
                        id: lbl_bienvenida
                        text: ""
                        font_style: "H5"
                        halign: "center"
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDSeparator:

                    MDLabel:
                        id: lbl_nombre
                        text: ""
                        halign: "center"
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDLabel:
                        id: lbl_edad
                        text: ""
                        halign: "center"
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDLabel:
                        id: lbl_categoria
                        text: ""
                        halign: "center"
                        font_style: "Subtitle1"
                        size_hint_y: None
                        height: self.texture_size[1]

                Widget:
                    size_hint_y: None
                    height: "12dp"

                MDRaisedButton:
                    text: "GUARDAR EN ARCHIVO"
                    pos_hint: {"center_x": .5}
                    md_bg_color: app.theme_cls.primary_color
                    on_release: app.guardar_datos()

                MDRectangleFlatButton:
                    text: "VER HISTORIAL"
                    pos_hint: {"center_x": .5}
                    on_release: app.ver_historial()

                MDFlatButton:
                    text: "VOLVER AL FORMULARIO"
                    pos_hint: {"center_x": .5}
                    on_release: app.volver_formulario()

                MDLabel:
                    id: lbl_guardado
                    text: ""
                    halign: "center"
                    theme_text_color: "Secondary"
                    font_style: "Caption"
                    size_hint_y: None
                    height: "48dp"

<PantallaHistorial>:
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Historial de Usuarios"
            md_bg_color: app.theme_cls.primary_color
            specific_text_color: 1, 1, 1, 1
            elevation: 4
            left_action_items: [["arrow-left", lambda x: app.volver_formulario()]]

        ScrollView:
            MDList:
                id: lista_usuarios
                padding: "16dp"
                spacing: "8dp"

        MDRectangleFlatButton:
            text: "ACTUALIZAR"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            on_release: app.cargar_historial()
"""

class RegistroApp(MDApp):
    _nombre_actual = ""
    _edad_actual = 0
    _datos_guardados = False
    db = None

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.theme_style = "Dark"
        self.db = Database()
        return Builder.load_string(KV)

    def limpiar_formulario(self):
        form = self.root.get_screen("formulario")
        form.ids.campo_nombre.text = ""
        form.ids.campo_edad.text = ""
        form.ids.lbl_error.text = ""

    def validar_y_continuar(self):
        sm = self.root
        form = sm.get_screen("formulario")
        nombre = form.ids.campo_nombre.text.strip()
        edad_s = form.ids.campo_edad.text.strip()

        form.ids.lbl_error.text = ""

        if not nombre:
            form.ids.lbl_error.text = "El nombre no puede estar vacio."
            return
        if any(ch.isdigit() for ch in nombre):
            form.ids.lbl_error.text = "El nombre no debe contener numeros."
            return
        if not edad_s:
            form.ids.lbl_error.text = "La edad no puede estar vacia."
            return

        try:
            edad = int(edad_s)
        except ValueError:
            form.ids.lbl_error.text = "La edad debe ser un numero valido."
            return

        if edad < 0 or edad > 120:
            form.ids.lbl_error.text = "Ingresa una edad valida (0 - 120)."
            return

        self._nombre_actual = nombre
        self._edad_actual = edad
        self._datos_guardados = False
        self._mostrar_resultado(nombre, edad)

    def _mostrar_resultado(self, nombre: str, edad: int):
        sm = self.root
        resultado = sm.get_screen("resultado")
        categoria = obtener_categoria(edad)

        resultado.ids.lbl_bienvenida.text = f"Hola, {nombre}!"
        resultado.ids.lbl_nombre.text = f"Nombre: {nombre}"
        resultado.ids.lbl_edad.text = f"Edad: {edad} años"
        resultado.ids.lbl_categoria.text = f"Categoria: {categoria}"
        resultado.ids.lbl_guardado.text = ""

        sm.current = "resultado"

    def guardar_datos(self):
        if self._datos_guardados:
            self.root.get_screen("resultado").ids.lbl_guardado.text = "Estos datos ya fueron guardados"
            return

        ruta = guardar_usuario(self._nombre_actual, self._edad_actual)
        categoria = obtener_categoria(self._edad_actual)
        self.db.guardar_usuario(self._nombre_actual, self._edad_actual, categoria)

        resultado = self.root.get_screen("resultado")

        if "Error" in ruta:
            resultado.ids.lbl_guardado.text = ruta
            resultado.ids.lbl_guardado.theme_text_color = "Error"
        else:
            resultado.ids.lbl_guardado.text = f"Guardado en:\n{ruta}\n✓ También guardado en SQLite"
            resultado.ids.lbl_guardado.theme_text_color = "Primary"
            self._datos_guardados = True

    def cargar_historial(self):
        from kivymd.uix.card import MDCard
        from kivymd.uix.label import MDLabel

        usuarios = self.db.obtener_usuarios()
        lista = self.root.get_screen("historial").ids.lista_usuarios
        lista.clear_widgets()

        if not usuarios:
            lbl_vacio = MDLabel(
                text="No hay usuarios registrados",
                halign="center",
                size_hint_y=None,
                height="50dp"
            )
            lista.add_widget(lbl_vacio)
            return

        for usuario in usuarios:
            card = MDCard(
                orientation="vertical",
                padding="12dp",
                spacing="8dp",
                size_hint_y=None,
                height="120dp",
                elevation=2,
                radius=[8]
            )

            lbl_nombre = MDLabel(
                text=f"👤 {usuario[1]}",
                font_style="H6",
                size_hint_y=None,
                height="30dp"
            )

            lbl_edad = MDLabel(
                text=f"📅 Edad: {usuario[2]} años - {usuario[3]}",
                size_hint_y=None,
                height="25dp"
            )

            lbl_fecha = MDLabel(
                text=f"🕒 {usuario[4]}",
                theme_text_color="Secondary",
                font_style="Caption",
                size_hint_y=None,
                height="25dp"
            )

            card.add_widget(lbl_nombre)
            card.add_widget(lbl_edad)
            card.add_widget(lbl_fecha)
            lista.add_widget(card)

    def ver_historial(self):
        self.cargar_historial()
        self.root.current = "historial"

    def volver_formulario(self):
        sm = self.root
        form = sm.get_screen("formulario")
        form.ids.campo_nombre.text = ""
        form.ids.campo_edad.text = ""
        form.ids.lbl_error.text = ""
        sm.current = "formulario"

    def on_stop(self):
        if self.db:
            self.db.cerrar()

if __name__ == "__main__":
    RegistroApp().run()