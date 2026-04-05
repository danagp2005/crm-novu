import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("""
CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    telefono TEXT,
    producto TEXT,
    estado TEXT DEFAULT 'Nuevo',
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_entrega TEXT
)
""")

conn.close()

print("Base de datos creada")