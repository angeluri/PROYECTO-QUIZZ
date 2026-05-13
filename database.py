"""
Módulo de base de datos SQLite para usuarios, progreso, certificados.
"""
import sqlite3
import hashlib
import os

DB_NAME = "education.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Progreso por módulo
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            course_name TEXT,
            module_name TEXT,
            best_score INTEGER,
            total_questions INTEGER,
            passed BOOLEAN,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(user_id, course_name, module_name)
        )
    ''')

    # Intentos de quiz
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            course_name TEXT,
            module_name TEXT,
            score INTEGER,
            total INTEGER,
            passed BOOLEAN,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Certificados de módulo (uno por módulo, puede actualizarse)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            course_name TEXT,
            module_name TEXT,
            score INTEGER,
            total INTEGER,
            percentage REAL,
            folio TEXT UNIQUE,
            hash_verification TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            pdf_path TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Certificados maestros (curso completo)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS master_certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            course_name TEXT,
            folio TEXT UNIQUE,
            hash_verification TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            pdf_path TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()

# ---------- Usuarios ----------
def register_user(name, email, password):
    """Registra usuario, retorna True si éxito, False si email existe."""
    import utils
    hashed = utils.hash_password(password)
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                       (name, email, hashed))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(email, password):
    """Retorna user_id si credenciales correctas, else None."""
    import utils
    hashed = utils.hash_password(password)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ? AND password = ?", (email, hashed))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row

# ---------- Progreso ----------
def get_progress(user_id, course_name, module_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT id, user_id, course_name, module_name, best_score, total_questions, passed 
                      FROM progress WHERE user_id=? AND course_name=? AND module_name=?''',
                   (user_id, course_name, module_name))
    row = cursor.fetchone()
    conn.close()
    return row

def save_progress(user_id, course_name, module_name, best_score, total_questions, passed):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO progress (user_id, course_name, module_name, best_score, total_questions, passed)
                      VALUES (?,?,?,?,?,?)''',
                   (user_id, course_name, module_name, best_score, total_questions, passed))
    conn.commit()
    conn.close()

def update_progress(user_id, course_name, module_name, new_score, total_questions, passed):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''UPDATE progress SET best_score=?, total_questions=?, passed=?, date=CURRENT_TIMESTAMP
                      WHERE user_id=? AND course_name=? AND module_name=?''',
                   (new_score, total_questions, passed, user_id, course_name, module_name))
    conn.commit()
    conn.close()

# ---------- Intentos ----------
def save_attempt(user_id, course_name, module_name, score, total, passed):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO attempts (user_id, course_name, module_name, score, total, passed)
                      VALUES (?,?,?,?,?,?)''',
                   (user_id, course_name, module_name, score, total, passed))
    conn.commit()
    conn.close()

# ---------- Certificados de módulo ----------
def get_certificate_by_module(user_id, course_name, module_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT id, score, total, percentage, folio, pdf_path 
                      FROM certificates WHERE user_id=? AND course_name=? AND module_name=?''',
                   (user_id, course_name, module_name))
    row = cursor.fetchone()
    conn.close()
    return row

def save_certificate(user_id, course_name, module_name, score, total, percentage, folio, hash_ver, pdf_path):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO certificates 
                      (user_id, course_name, module_name, score, total, percentage, folio, hash_verification, pdf_path)
                      VALUES (?,?,?,?,?,?,?,?,?)''',
                   (user_id, course_name, module_name, score, total, percentage, folio, hash_ver, pdf_path))
    conn.commit()
    conn.close()

def update_certificate(cert_id, score, total, percentage, folio, hash_ver, pdf_path):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''UPDATE certificates 
                      SET score=?, total=?, percentage=?, folio=?, hash_verification=?, pdf_path=?, date=CURRENT_TIMESTAMP
                      WHERE id=?''',
                   (score, total, percentage, folio, hash_ver, pdf_path, cert_id))
    conn.commit()
    conn.close()

def get_certificates(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT id, user_id, course_name, module_name, score, total, percentage, folio, date, hash_verification, pdf_path
                      FROM certificates WHERE user_id=? ORDER BY date DESC''', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# ---------- Certificados maestros ----------
def get_master_certificate(user_id, course_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT id, folio, pdf_path FROM master_certificates 
                      WHERE user_id=? AND course_name=?''', (user_id, course_name))
    row = cursor.fetchone()
    conn.close()
    return row

def save_master_certificate(user_id, course_name, folio, hash_ver, pdf_path):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO master_certificates (user_id, course_name, folio, hash_verification, pdf_path)
                      VALUES (?,?,?,?,?)''', (user_id, course_name, folio, hash_ver, pdf_path))
    conn.commit()
    conn.close()

def get_master_certificates(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT id, user_id, course_name, folio, date, hash_verification, pdf_path
                      FROM master_certificates WHERE user_id=? ORDER BY date DESC''', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows