import sqlite3
from datetime import datetime


class Database:
    def _init_(self, db_path: str = "usuarios.db"):
        # Definir atributos PRIMERO, antes de cualquier método
        self.db_path = db_path
        self.conn = None      # <-- explícito aquí
        self.cursor = None    # <-- explícito aquí
        self._conectar()
        self._crear_tabla()

    def _conectar(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"[Database] Error al conectar: {e}")
            self.conn = None
            self.cursor = None

    def _asegurar_cursor(self) -> bool:
        # Usar getattr para evitar AttributeError si algo falló
        conn = getattr(self, "conn", None)
        cursor = getattr(self, "cursor", None)

        if conn is None or cursor is None:
            print("[Database] Reconectando…")
            self._conectar()

        if getattr(self, "conn", None) is None or getattr(self, "cursor", None) is None:
            print("[Database] No se pudo establecer conexión.")
            return False
        return True

    def _crear_tabla(self):
        if not self._asegurar_cursor():
            return
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre    TEXT    NOT NULL,
                    edad      INTEGER NOT NULL,
                    categoria TEXT    NOT NULL,
                    fecha     TEXT    NOT NULL
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"[Database] Error al crear tabla: {e}")

    def guardar_usuario(self, nombre: str, edad: int, categoria: str) -> bool:
        if not self._asegurar_cursor():
            return False
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.cursor.execute(
                "INSERT INTO usuarios (nombre, edad, categoria, fecha) VALUES (?, ?, ?, ?)",
                (nombre, edad, categoria, fecha)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"[Database] Error al guardar usuario: {e}")
            return False

    def obtener_usuarios(self) -> list:
        if not self._asegurar_cursor():
            return []
        try:
            self.cursor.execute(
                "SELECT id, nombre, edad, categoria, fecha FROM usuarios ORDER BY fecha DESC"
            )
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[Database] Error al obtener usuarios: {e}")
            return []

    def eliminar_usuario(self, usuario_id: int) -> bool:
        if not self._asegurar_cursor():
            return False
        try:
            self.cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"[Database] Error al eliminar usuario: {e}")
            return False

    def cerrar(self):
        try:
            if getattr(self, "cursor", None):
                self.cursor.close()
        except sqlite3.Error:
            pass
        finally:
            self.cursor = None
        try:
            if getattr(self, "conn", None):
                self.conn.close()
        except sqlite3.Error:
            pass
        finally:
            self.conn = None