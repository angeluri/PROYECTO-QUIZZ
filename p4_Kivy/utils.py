"""
Utilidades generales: hash de contraseñas, folios únicos, fechas, y verificación de carpetas.
"""
import hashlib
import datetime
import os

def hash_password(password):
    """Genera hash SHA-256 de la contraseña."""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_folio(prefix="CERT"):
    """Genera folio único basado en timestamp y aleatorio."""
    import time
    import random
    timestamp = int(time.time())
    rand = random.randint(1000, 9999)
    return f"{prefix}-{timestamp}-{rand}"

def generate_hash(data):
    """SHA-256 de una cadena para verificación de integridad."""
    return hashlib.sha256(data.encode()).hexdigest()

def format_date():
    """Fecha formateada para mostrar en certificados y UI."""
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

def ensure_folders():
    """Crea las carpetas necesarias si no existen."""
    folders = ["assets", "certificados", "backups"]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
    # Crear un archivo logo placeholder si no existe
    logo_path = os.path.join("assets", "logo.png")
    if not os.path.exists(logo_path):
        # No se crea logo real; el código de PDF lo maneja con try/except
        pass