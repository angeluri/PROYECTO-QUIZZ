from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel


class Pantalla1(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.nombre_input = MDTextField(
            hint_text="Escribe tu nombre",
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            size_hint_x=0.8
        )

        boton = MDRaisedButton(
            text="Ir a la siguiente pantalla",
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            on_release=self.ir_pantalla2
        )

        self.add_widget(self.nombre_input)
        self.add_widget(boton)

    def ir_pantalla2(self, instance):
        nombre = self.nombre_input.text
        self.manager.get_screen("pantalla2").actualizar_mensaje(nombre)
        self.manager.current = "pantalla2"


class Pantalla2(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.label = MDLabel(
            text="",
            halign="center",
            pos_hint={"center_y": 0.6}
        )

        boton_regresar = MDRaisedButton(
            text="Regresar",
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            on_release=self.regresar
        )

        self.add_widget(self.label)
        self.add_widget(boton_regresar)

    def actualizar_mensaje(self, nombre):
        self.label.text = f"Hola {nombre}, bienvenido"

    def regresar(self, instance):
        self.manager.current = "pantalla1"


class MainApp(MDApp):
    def build(self):
        sm = MDScreenManager()
        sm.add_widget(Pantalla1(name="pantalla1"))
        sm.add_widget(Pantalla2(name="pantalla2"))
        return sm


if __name__ == "__main__":
    MainApp().run()