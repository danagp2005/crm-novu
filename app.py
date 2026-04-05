from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "lkhafsdghkwgrefasd913237hj"


def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# 🔹 FORMULARIO (clientes)
@app.route('/')
def index():
    return render_template("index.html")


# 🔹 GUARDAR PEDIDO
@app.route('/guardar', methods=['POST'])
def guardar():
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    producto = request.form['producto']
    fecha_entrega = request.form['fecha_entrega']

    db = get_db()
    db.execute(
        "INSERT INTO pedidos (nombre, telefono, producto, fecha_entrega) VALUES (?, ?, ?, ?)",
        (nombre, telefono, producto, fecha_entrega)
    )
    db.commit()
    db.close()

    return redirect('/')

@app.route('/eliminar/<int:id>')
def eliminar(id):
    db = get_db()
    db.execute("DELETE FROM pedidos WHERE id=?", (id,))
    db.commit()
    db.close()
    return redirect('/pedidos')


# 🔐 LOGIN ADMIN (PASO 3)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']

        if password == "lkhafsdghkwgrefasd913237hj":
            session['admin'] = True
            return redirect('/pedidos')

    return render_template("login.html")


# 🔒 PANEL PROTEGIDO (PASO 4)
@app.route('/pedidos')
def pedidos():
    if not session.get('admin'):
        return redirect('/login')

    db = get_db()
    pedidos = db.execute("SELECT * FROM pedidos ORDER BY id DESC").fetchall()
    db.close()

    return render_template("pedidos.html", pedidos=pedidos)


# 🔄 CAMBIAR ESTADO
@app.route('/estado/<int:id>/<nuevo_estado>')
def cambiar_estado(id, nuevo_estado):
    if not session.get('admin'):
        return redirect('/login')

    db = get_db()
    db.execute("UPDATE pedidos SET estado=? WHERE id=?", (nuevo_estado, id))
    db.commit()
    db.close()

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)