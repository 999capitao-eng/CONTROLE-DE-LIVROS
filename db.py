
import sqlite3
from pathlib import Path

ESQUEMA = Path(__file__).with_name("schema.sql")


def conectar(caminho="biblioteca.db"):
    conn = sqlite3.connect(caminho)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def preparar_banco(conn):
    conn.executescript(
        ESQUEMA.read_text(encoding="utf-8")
    )
    conn.commit()
